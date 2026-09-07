#!/usr/bin/env python3
"""Validate the GitHub README visual-language gallery and its provenance."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import struct
from pathlib import Path
from html.parser import HTMLParser

from repository_safety import is_link_like


ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "docs" / "style-gallery"
MANIFEST = GALLERY / "manifest.json"
README = ROOT / "README.md"
EXPECTED = {
    "cyberpunk-design",
    "epic-design",
    "fantasy-design",
    "horror-design",
    "noir-design",
    "romance-design",
    "war-design",
    "wuxia-design",
    "hard-sci-fi-visual-director",
}


def jpeg_dimensions(payload: bytes) -> tuple[int, int] | None:
    if not payload.startswith(b"\xff\xd8"):
        return None
    index = 2
    sof_markers = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while index + 4 <= len(payload):
        if payload[index] != 0xFF:
            index += 1
            continue
        while index < len(payload) and payload[index] == 0xFF:
            index += 1
        if index >= len(payload):
            break
        marker = payload[index]
        index += 1
        if marker in {0xD8, 0xD9}:
            continue
        if index + 2 > len(payload):
            break
        length = int.from_bytes(payload[index:index + 2], "big")
        if length < 2 or index + length > len(payload):
            break
        if marker in sof_markers and length >= 7:
            height = int.from_bytes(payload[index + 3:index + 5], "big")
            width = int.from_bytes(payload[index + 5:index + 7], "big")
            return width, height
        index += length
    return None


def validate_legacy_gallery() -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid style-gallery manifest: {exc}"]
    readme = README.read_text(encoding="utf-8")
    items = manifest.get("items")
    if not isinstance(items, list) or len(items) != 9:
        errors.append("style gallery must contain exactly nine items")
        items = items if isinstance(items, list) else []
    skills = {item.get("skill") for item in items if isinstance(item, dict)}
    if skills != EXPECTED:
        errors.append(f"style gallery Skill set mismatch: {sorted(skills)}")
    if sum(item.get("release_state") == "deployed" for item in items) != 8:
        errors.append("style gallery must contain eight deployed examples")
    if sum(item.get("release_state") == "experimental" for item in items) != 1:
        errors.append("style gallery must contain one experimental example")
    if sum(item.get("source_kind") == "new_builtin_imagegen" for item in items) != 7:
        errors.append("style gallery must record seven new ImageGen outputs")
    if sum(item.get("source_kind") == "reused_original_atlas_panel" for item in items) != 2:
        errors.append("style gallery must record two reused original atlas panels")

    hashes: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            errors.append("style gallery item must be an object")
            continue
        skill = str(item.get("skill", "<unknown>"))
        relative = str(item.get("file", ""))
        path = GALLERY / relative
        if not path.is_file():
            errors.append(f"missing style gallery image: {relative}")
            continue
        payload = path.read_bytes()
        digest = hashlib.sha256(payload).hexdigest().upper()
        if digest != str(item.get("sha256", "")).upper():
            errors.append(f"style gallery hash mismatch: {relative}")
        if digest in hashes:
            errors.append(f"duplicate style gallery image content: {relative}")
        hashes.add(digest)
        if len(payload) != item.get("bytes"):
            errors.append(f"style gallery byte-size mismatch: {relative}")
        if len(payload) > 500_000:
            errors.append(f"style gallery image exceeds 500 KB: {relative}")
        dimensions = jpeg_dimensions(payload)
        if dimensions != (item.get("width"), item.get("height")):
            errors.append(f"style gallery JPEG dimensions mismatch: {relative}")
        for field in ("visible_contract", "status", "source_kind", "source_sha256"):
            if not str(item.get(field, "")).strip():
                errors.append(f"style gallery item missing {field}: {skill}")
        if "user" not in str(item.get("status", "")).lower():
            errors.append(f"style gallery item lacks user-acceptance boundary: {skill}")
        if item.get("source_kind") == "reused_original_atlas_panel":
            if not item.get("source_file") or not isinstance(item.get("crop_box"), list):
                errors.append(f"reused style gallery item lacks source crop provenance: {skill}")

    inventory = manifest.get("inventory", {})
    if inventory.get("generated_archive_files") != inventory.get("readable_files"):
        errors.append("generated archive contains unreadable files")
    if inventory.get("generated_archive_files") != inventory.get("unique_sha256"):
        errors.append("generated archive inventory is not content-unique")
    if inventory.get("duplicate_files") != 0:
        errors.append("generated archive duplicate count must remain explicit and zero at this freeze")
    for field in ("scan_scope", "selection_rule", "selection_result"):
        if not str(inventory.get(field, "")).strip():
            errors.append(f"style gallery inventory missing {field}")
    if "does not prove" not in str(manifest.get("global_boundary", "")):
        errors.append("style gallery manifest lacks global evidence boundary")
    if "docs/style-gallery/manifest.json" not in readme:
        errors.append("README must keep the frozen legacy style-gallery provenance link")
    if not ("historical" in readme.lower() or "历史" in readme):
        errors.append("README must distinguish the historical gallery from current samples")

    print(f"Historical style gallery items checked: {len(items)}")
    return errors


def webp_dimensions(payload: bytes) -> tuple[int, int] | None:
    """Read static WebP container dimensions without an imaging dependency."""
    if len(payload) < 20 or payload[:4] != b"RIFF" or payload[8:12] != b"WEBP":
        return None
    if int.from_bytes(payload[4:8], "little") + 8 != len(payload):
        return None
    position = 12
    canvas = None
    image_size = None
    while position + 8 <= len(payload):
        kind = payload[position:position + 4]
        size = int.from_bytes(payload[position + 4:position + 8], "little")
        start = position + 8
        if start + size > len(payload):
            return None
        data = payload[start:start + size]
        if kind in {b"ANIM", b"ANMF"}:
            return None
        if kind == b"VP8X":
            if len(data) != 10 or data[0] & 2:
                return None
            canvas = (int.from_bytes(data[4:7], "little") + 1, int.from_bytes(data[7:10], "little") + 1)
        elif kind == b"VP8 ":
            if len(data) < 10 or data[3:6] != b"\x9d\x01\x2a":
                return None
            image_size = (int.from_bytes(data[6:8], "little") & 0x3FFF,
                          int.from_bytes(data[8:10], "little") & 0x3FFF)
        elif kind == b"VP8L":
            if len(data) < 5 or data[0] != 0x2F:
                return None
            bits = int.from_bytes(data[1:5], "little")
            image_size = ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
        position = start + size + size % 2
    if position != len(payload) or not image_size or min(image_size) <= 0:
        return None
    if canvas and canvas != image_size:
        return None
    return canvas or image_size


def png_dimensions(payload: bytes) -> tuple[int, int] | None:
    if len(payload) < 24 or payload[:8] != b"\x89PNG\r\n\x1a\n" or payload[12:16] != b"IHDR":
        return None
    dimensions = struct.unpack(">II", payload[16:24])
    return dimensions if min(dimensions) > 0 else None


def confined_file(base: Path, relative: object) -> Path | None:
    if not isinstance(relative, str) or not relative or "\\" in relative or ":" in relative:
        return None
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        return None
    candidate = base / path
    if not candidate.resolve().is_relative_to(base.resolve()):
        return None
    if any(is_link_like(p) for p in [candidate, *candidate.parents] if p != base.parent and p.is_relative_to(base)):
        return None
    return candidate if candidate.is_file() else None


class AssetLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: set[str] = set()

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {"src", "href"} and value:
                self.links.add(value)


def asset_links(text: str, markdown: bool = False) -> set[str]:
    parser = AssetLinks()
    parser.feed(text)
    if markdown:
        parser.links.update(re.findall(r"!?\[[^\]]*\]\(([^)\s]+)\)", text))
    return parser.links


def validate_showcase(root: Path = ROOT, require_links: bool = True) -> list[str]:
    errors: list[str] = []
    directory = root / "docs" / "showcase"
    try:
        manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid current showcase manifest: {exc}"]
    if not isinstance(manifest, dict) or manifest.get("schema_version") != "1.0":
        return ["current showcase schema_version must be 1.0"]
    for field in ("publication", "inventory_freeze", "rights_basis", "acceptance_scope"):
        if not isinstance(manifest.get(field), str) or not manifest[field].strip():
            errors.append(f"current showcase missing {field}")
    items = manifest.get("items")
    if not isinstance(items, list):
        return errors + ["current showcase items must be a list"]
    for field, actual in (("expected_count", len(items)), ("expected_genre_count", len({a.get('skill') for a in items if isinstance(a, dict) and isinstance(a.get('skill'), str)}))):
        if type(manifest.get(field)) is not int or manifest[field] <= 0 or manifest[field] != actual:
            errors.append(f"current showcase {field} does not match actual inventory")
    page_links: set[str] = set()
    readme_links: set[str] = set()
    if require_links:
        try:
            page_links = asset_links((root / "docs" / "index.html").read_text(encoding="utf-8"))
            readme_links = asset_links((root / "README.md").read_text(encoding="utf-8"), markdown=True)
        except OSError as exc:
            errors.append(f"cannot verify showcase entry links: {exc}")
    ids: set[str] = set()
    originals: set[str] = set()
    previews: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            errors.append("current showcase item must be an object")
            continue
        identifier = item.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", identifier) or identifier in ids:
            errors.append(f"invalid or duplicate showcase id: {identifier}")
        ids.add(str(identifier))
        for field in ("skill", "genre", "genre_en", "title", "title_en", "visible_contract"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"showcase {identifier} missing {field}")
        skill = item.get("skill")
        availability = item.get("availability")
        if isinstance(availability, str) and availability in {"packaged", "experimental"}:
            base = "skills" if availability == "packaged" else "experimental"
            if not isinstance(skill, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill) or not (root / base / skill / "SKILL.md").is_file():
                errors.append(f"showcase {identifier} has wrong package availability: {skill}")
        elif availability == "external_not_redistributed":
            if skill != "xianxia-visual-director" or any((root / base / str(skill)).exists() for base in ("skills", "experimental")):
                errors.append(f"showcase {identifier} has unsupported external Skill provenance")
        else:
            errors.append(f"showcase {identifier} has invalid availability")
        if item.get("source_kind") != "original_builtin_imagegen":
            errors.append(f"showcase {identifier} must identify original ImageGen provenance")
        if item.get("status") != "user_accepted":
            errors.append(f"showcase {identifier} lacks the declared user acceptance")
        if item.get("file") != f"{identifier}.webp" or item.get("original_file") != f"originals/{identifier}.png":
            errors.append(f"showcase {identifier} preview/original file naming does not match its id")
        dimensions = {}
        for prefix, key, expected_suffix, parser in (("", "file", ".webp", webp_dimensions), ("original_", "original_file", ".png", png_dimensions)):
            relative = item.get(key)
            path = confined_file(directory, relative)
            if path is None or path.suffix != expected_suffix:
                errors.append(f"showcase {identifier} missing or unsafe {key}: {relative}")
                continue
            payload = path.read_bytes()
            digest = hashlib.sha256(payload).hexdigest().upper()
            if digest != str(item.get(prefix + "sha256", "")).upper():
                errors.append(f"showcase {identifier} {key} hash mismatch")
            seen = originals if prefix else previews
            if digest in seen:
                errors.append(f"showcase {identifier} duplicates another {key}")
            seen.add(digest)
            if len(payload) != item.get(prefix + "bytes"):
                errors.append(f"showcase {identifier} {key} byte-size mismatch")
            actual_size = parser(payload)
            expected_size = (item.get(prefix + "width"), item.get(prefix + "height"))
            if actual_size is None or actual_size != expected_size or any(type(v) is not int or v <= 0 for v in expected_size):
                errors.append(f"showcase {identifier} {key} dimensions mismatch or invalid static image header")
            else:
                dimensions[prefix] = actual_size
            if require_links and f"showcase/{relative}" not in page_links:
                errors.append(f"showcase {identifier} {key} must be linked from the actual Pages markup")
            if require_links and not prefix and f"docs/showcase/{relative}" not in readme_links:
                errors.append(f"showcase {identifier} preview must be linked from README")
        if "" in dimensions and "original_" in dimensions:
            width, height = dimensions[""]
            ow, oh = dimensions["original_"]
            if width > ow or height > oh:
                errors.append(f"showcase {identifier} preview must not upscale the original")
            if abs(width * oh - height * ow) > max(ow, oh):
                errors.append(f"showcase {identifier} preview changes the original aspect ratio")
    return errors


def main() -> int:
    errors = validate_legacy_gallery() + validate_showcase()
    print(f"Errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
