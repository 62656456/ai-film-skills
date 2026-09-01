#!/usr/bin/env python3
"""Validate the GitHub README visual-language gallery and its provenance."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


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


def main() -> int:
    errors: list[str] = []
    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: invalid style-gallery manifest: {exc}")
        return 1
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
        readme_path = f"docs/style-gallery/{relative}"
        image_pattern = rf'<img\s+src="{re.escape(readme_path)}"[^>]+alt="[^"]+"'
        if not re.search(image_pattern, readme):
            errors.append(f"style gallery image missing from README or lacks alt text: {relative}")
        guide_root = "docs/skills/en"
        if f'{guide_root}/{skill}.md' not in readme:
            errors.append(f"style gallery Skill guide missing from README: {skill}")
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
    for term in (
        "## Explore the visual language",
        "Seven frames were newly designed",
        "two prior original atlas panels",
        "Experimental · self-audit only",
        "not a claim that the Skill alone generated it",
        "docs/style-gallery/manifest.json",
    ):
        if term not in readme:
            errors.append(f"README missing style-gallery disclosure: {term}")

    print(f"Style gallery items checked: {len(items)}")
    print(f"Unique gallery hashes: {len(hashes)}")
    print(f"Errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
