#!/usr/bin/env python3
"""Validate the dependency-free GitHub Pages landing page."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INDEX = DOCS / "index.html"
CSS = DOCS / "site.css"


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str]]] = []
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.title_text = ""
        self.in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        self.tags.append((tag, values))
        if values.get("id"):
            if values["id"] in self.ids:
                self.duplicate_ids.add(values["id"])
            self.ids.add(values["id"])
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_text += data


def markup_errors(parser: SiteParser) -> list[str]:
    errors = [f"Pages HTML duplicate id: {value}" for value in sorted(parser.duplicate_ids)]
    for tag, attrs in parser.tags:
        if tag == "script":
            errors.append("Pages HTML must not contain scripts or tracking code")
        if any(name.lower().startswith("on") for name in attrs):
            errors.append(f"Pages HTML must not contain executable event attributes: {tag}")
        if any(attrs.get(name, "").strip().lower().startswith(("javascript:", "data:text/html")) for name in ("href", "src", "action")):
            errors.append(f"Pages HTML must not contain executable URLs: {tag}")
        if tag == "a" and attrs.get("href", "").startswith("#") and attrs["href"][1:] not in parser.ids:
            errors.append(f"Pages HTML broken section link: {attrs['href']}")
    return errors


def has_whitebox_route(text: str) -> bool:
    return bool(re.search(r"experimental/whitebox-previs-executor|docs/skills/(?:en|zh-CN)/whitebox-previs-executor\.md", text))


def has_previs_nonfilm_boundary(text: str) -> bool:
    return bool(re.search(r"(?:not|不证明|不是|不代表|不等于)[^\n]{0,100}(?:finished\s+AI\s+films|final\s+AI\s+films|(?:最终|完整)\s*AI\s*成片)", text, re.I))


def has_linked_image(text: str, image_source: str, video_url: str) -> bool:
    """Require an actual image inside the link that opens its original video."""
    text = re.sub(r"^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$", "", text, flags=re.M | re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    class LinkedImageParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.links: list[str] = []
            self.found = False

        def handle_starttag(self, tag, attrs):
            values = dict(attrs)
            if tag == "a":
                self.links.append(values.get("href", ""))
            elif tag == "img" and values.get("src") == image_source and video_url in self.links:
                self.found = True

        def handle_endtag(self, tag):
            if tag == "a" and self.links:
                self.links.pop()

    parser = LinkedImageParser()
    parser.feed(text)
    if parser.found:
        return True
    return bool(re.search(r"\[!\[[^\]]*\]\(<?" + re.escape(image_source) +
                          r">?\)\]\(<?" + re.escape(video_url) + r">?\)", text))


def gif_metadata(payload: bytes) -> dict[str, int | None]:
    """Read GIF blocks, never mistaking compressed bytes for frame controls."""
    if len(payload) < 13 or payload[:6] not in {b"GIF87a", b"GIF89a"}:
        raise ValueError("invalid or truncated GIF header")
    width, height = int.from_bytes(payload[6:8], "little"), int.from_bytes(payload[8:10], "little")
    if not width or not height:
        raise ValueError("GIF canvas dimensions must be positive")
    offset = 13

    def take(size: int) -> bytes:
        nonlocal offset
        if offset + size > len(payload):
            raise ValueError("truncated GIF block")
        data = payload[offset:offset + size]
        offset += size
        return data

    def subblocks() -> bytes:
        chunks = bytearray()
        while True:
            size = take(1)[0]
            if size == 0:
                return bytes(chunks)
            chunks.extend(take(size))

    packed = payload[10]
    if packed & 128:
        take(3 * 2 ** ((packed & 7) + 1))
    frames, duration, delay, loop = 0, 0, 0, None
    while offset < len(payload):
        marker = take(1)[0]
        if marker == 0x3B:
            if not frames:
                raise ValueError("GIF has no image frames")
            return {"width": width, "height": height, "frames": frames,
                    "duration_ms": duration, "loop": loop}
        if marker == 0x21:
            label = take(1)[0]
            if label == 0xF9:
                if take(1)[0] != 4:
                    raise ValueError("invalid GIF graphic control size")
                control = take(4)
                if take(1)[0] != 0:
                    raise ValueError("unterminated GIF graphic control")
                delay = int.from_bytes(control[1:3], "little") * 10
            else:
                data = subblocks()
                if label == 0xFF and data[:11] in {b"NETSCAPE2.0", b"ANIMEXTS1.0"}:
                    if len(data) != 14 or data[11] != 1:
                        raise ValueError("invalid GIF animation loop extension")
                    loop = int.from_bytes(data[12:14], "little")
        elif marker == 0x2C:
            descriptor = take(9)
            if not int.from_bytes(descriptor[4:6], "little") or not int.from_bytes(descriptor[6:8], "little"):
                raise ValueError("GIF frame dimensions must be positive")
            if descriptor[8] & 128:
                take(3 * 2 ** ((descriptor[8] & 7) + 1))
            take(1)  # LZW minimum code size; the image data itself is not decoded here.
            subblocks()
            frames += 1
            duration += delay
            delay = 0
        else:
            raise ValueError(f"unknown GIF block marker: {marker:#x}")
    raise ValueError("GIF is missing its trailer")


def preview_metadata_errors(payload: bytes, item: dict) -> list[str]:
    try:
        actual = gif_metadata(payload)
    except ValueError as exc:
        return [f"invalid archived GIF preview: {exc}"]
    pairs = (("width", "preview_width"), ("height", "preview_height"),
             ("frames", "preview_frames"), ("duration_ms", "preview_duration_ms"))
    return [f"archived GIF {key} mismatch: expected {item.get(field)}, found {actual[key]}"
            for key, field in pairs if actual[key] != item.get(field)]


def main() -> int:
    errors: list[str] = []
    for required in (INDEX, CSS, DOCS / ".nojekyll"):
        if not required.is_file():
            errors.append(f"missing Pages file: {required.relative_to(ROOT)}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    html = INDEX.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    parser = SiteParser()
    parser.feed(html)

    if not parser.title_text.strip():
        errors.append("Pages HTML has no title")
    for required_id in ("main", "top", "outcomes", "proof", "install"):
        if required_id not in parser.ids:
            errors.append(f"Pages HTML missing id: {required_id}")
    if "media" not in parser.ids:
        errors.append("Pages HTML missing id: media")
    errors.extend(markup_errors(parser))

    meta_names = {attrs.get("name") for tag, attrs in parser.tags if tag == "meta"}
    meta_props = {attrs.get("property") for tag, attrs in parser.tags if tag == "meta"}
    for name in ("viewport", "description", "twitter:card"):
        if name not in meta_names:
            errors.append(f"Pages HTML missing meta name: {name}")
    for prop in ("og:title", "og:description", "og:image", "og:url"):
        if prop not in meta_props:
            errors.append(f"Pages HTML missing Open Graph property: {prop}")

    for tag, attrs in parser.tags:
        if tag == "img":
            for required in ("src", "alt", "width", "height"):
                if not attrs.get(required):
                    errors.append(f"Pages image missing {required}: {attrs.get('src', '<unknown>')}")
        if tag == "video":
            for required in ("controls", "preload", "poster", "width", "height", "aria-label"):
                if required not in attrs or (required != "controls" and not attrs.get(required)):
                    errors.append(f"Pages video missing {required}: {attrs.get('poster', '<unknown>')}")
            if attrs.get("preload") != "metadata":
                errors.append("Pages video preload must be metadata")
            if "autoplay" in attrs:
                errors.append("Pages videos must not autoplay")
        if tag in {"a", "link", "img", "source"}:
            value = attrs.get("href") or attrs.get("src")
            if not value or value.startswith(("#", "mailto:")):
                continue
            parsed = urlparse(value)
            if parsed.scheme:
                if parsed.scheme != "https":
                    errors.append(f"non-HTTPS public URL: {value}")
                continue
            target = (DOCS / parsed.path).resolve()
            try:
                target.relative_to(DOCS.resolve())
            except ValueError:
                errors.append(f"Pages relative asset escapes docs/: {value}")
                continue
            if not target.is_file():
                errors.append(f"Pages broken relative asset: {value}")

    required_html = (
        "npx --yes skills@latest add 62656456/ai-film-skills --list",
        "SELF-AUDIT",
        "https://skills.sh/62656456/ai-film-skills",
        "https://github.com/62656456/ai-film-skills/discussions/7",
    )
    for term in required_html:
        if term not in html:
            errors.append(f"Pages HTML missing evidence or action term: {term}")
    required_css = (
        ":focus-visible",
        "@media (prefers-reduced-motion: reduce)",
    )
    for term in required_css:
        if term not in css:
            errors.append(f"Pages CSS missing quality term: {term}")
    if not re.search(r"@media[^{}]*\((?:max|min)-width\s*:", css):
        errors.append("Pages CSS must contain a responsive width breakpoint")

    media_manifest = DOCS / "media" / "media-manifest.json"
    try:
        media = json.loads(media_manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid media evidence manifest: {exc}")
        media = {}
    items = media.get("items", [])
    if not isinstance(items, list) or len(items) != 2:
        errors.append("media evidence manifest must contain exactly two approved items")
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict):
            errors.append("media evidence item must be an object")
            continue
        for field, hash_field, size_field in (
            ("video", "video_sha256", "video_bytes"),
            ("poster", "poster_sha256", "poster_bytes"),
            ("readme_preview", "preview_sha256", "preview_bytes"),
        ):
            relative = item.get(field)
            path = DOCS / "media" / str(relative)
            if not path.is_file():
                errors.append(f"missing media evidence file: {relative}")
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest().upper()
            if digest != str(item.get(hash_field, "")).upper():
                errors.append(f"media evidence hash mismatch: {relative}")
            if path.stat().st_size != item.get(size_field):
                errors.append(f"media evidence byte-size mismatch: {relative}")
            if field != "readme_preview" and str(relative) not in html:
                errors.append(f"media evidence is not linked from Pages HTML: {relative}")
            if field == "readme_preview":
                errors.extend(f"{relative}: {error}" for error in preview_metadata_errors(path.read_bytes(), item))
        if item.get("readme_display") != "poster_link_to_video":
            errors.append(f"media README display must be a static poster linked to video: {item.get('id')}")
        source = "docs/media/" + str(item.get("poster"))
        video_url = "https://62656456.github.io/ai-film-skills/media/" + str(item.get("video"))
        if not has_linked_image(readme, source, video_url):
            errors.append(f"media poster is not an image linked to its original video in README: {source}")
        for boundary_field in ("status", "proves", "does_not_prove", "preview_derivation"):
            if not str(item.get(boundary_field, "")).strip():
                errors.append(f"media evidence item missing {boundary_field}: {item.get('id')}")

    if re.search(r"<img\b[^>]*\bsrc\s*=\s*[\"'][^\"']+\.gif[\"']|!\[[^\]]*\]\([^)]*\.gif\)", readme, re.I):
        errors.append("README must use static posters, with animation opened by the user")

    for required_readme_term in (
        "https://62656456.github.io/ai-film-skills/media/previs-blocking-5s.mp4",
        "https://62656456.github.io/ai-film-skills/media/rigged-contact-gate-2.8s.mp4",
    ):
        if required_readme_term not in readme:
            errors.append(f"README missing direct media showcase term: {required_readme_term}")
    if not has_previs_nonfilm_boundary(readme):
        errors.append("README must distinguish bounded previs evidence from finished AI films")
    if not has_whitebox_route(readme):
        errors.append("README must link the experimental whitebox source or its design guide")

    print(f"Pages HTML tags checked: {len(parser.tags)}")
    print(f"Pages IDs checked: {len(parser.ids)}")
    print(f"Errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
