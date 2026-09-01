#!/usr/bin/env python3
"""Validate the dependency-free GitHub Pages landing page."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
import hashlib
import json
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
        self.title_text = ""
        self.in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        self.tags.append((tag, values))
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_text += data


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
    if any(tag == "script" for tag, _ in parser.tags):
        errors.append("Pages HTML must not contain scripts or tracking code")

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
        if tag in {"a", "link", "img"}:
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
        "@media (max-width: 800px)",
        "@media (max-width: 520px)",
        "@media (prefers-reduced-motion: reduce)",
        "color-scheme: dark",
    )
    for term in required_css:
        if term not in css:
            errors.append(f"Pages CSS missing quality term: {term}")

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
                if str(relative) not in readme:
                    errors.append(f"media preview is not embedded in README: {relative}")
                payload = path.read_bytes()
                if not payload.startswith((b"GIF87a", b"GIF89a")):
                    errors.append(f"README preview is not a GIF: {relative}")
                elif len(payload) >= 10:
                    width = int.from_bytes(payload[6:8], "little")
                    height = int.from_bytes(payload[8:10], "little")
                    if width != item.get("preview_width") or height != item.get("preview_height"):
                        errors.append(f"README preview dimensions mismatch: {relative}")
                    frame_count = payload.count(b"\x21\xf9\x04")
                    if frame_count != item.get("preview_frames"):
                        errors.append(f"README preview frame count mismatch: {relative}")
        for boundary_field in ("status", "proves", "does_not_prove", "preview_derivation"):
            if not str(item.get(boundary_field, "")).strip():
                errors.append(f"media evidence item missing {boundary_field}: {item.get('id')}")

    for required_readme_term in (
        "## See the Skills in motion",
        "https://62656456.github.io/ai-film-skills/media/previs-blocking-5s.mp4",
        "https://62656456.github.io/ai-film-skills/media/rigged-contact-gate-2.8s.mp4",
        "not finished AI films",
        "unpublished local previs executor",
    ):
        if required_readme_term not in readme:
            errors.append(f"README missing direct media showcase term: {required_readme_term}")

    print(f"Pages HTML tags checked: {len(parser.tags)}")
    print(f"Pages IDs checked: {len(parser.ids)}")
    print(f"Errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
