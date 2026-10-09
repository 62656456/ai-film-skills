from __future__ import annotations

import copy
import hashlib
import json
import struct
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generate_skill_guides import download_link
from validate_pages_site import (SiteParser, markup_errors, has_previs_nonfilm_boundary,
                                 has_linked_image, gif_metadata, preview_metadata_errors)
from validate_repository import (validate_public_counts, public_count_files,
                                 validate_launch_assets, validate_director_example,
                                 REQUIRED_LAUNCH_ASSETS)
from validate_style_gallery import validate_showcase, webp_dimensions


def webp_container(kind: bytes, data: bytes) -> bytes:
    chunk = kind + len(data).to_bytes(4, "little") + data + (b"\0" if len(data) % 2 else b"")
    return b"RIFF" + (len(chunk) + 4).to_bytes(4, "little") + b"WEBP" + chunk


class PublicContractTests(unittest.TestCase):
    def test_current_counts_follow_registry_and_dated_history_is_allowed(self):
        self.assertEqual(validate_public_counts("20 modules and 40 bilingual guides", 20), [])
        self.assertTrue(validate_public_counts("19 modules and 38 guides", 20))
        self.assertEqual(validate_public_counts("Historical v1.3.0: 19 modules and 38 guides", 20), [])

    def test_regular_experimental_and_multilingual_counts_follow_inventory(self):
        samples = ("18 regular and 3 experimental packages; 21 modules; 42 guides",
                   "18项常规＋3项实验＝21个独立模块；42份中英指南",
                   "通常18＋実験3＝21モジュール; 計42ページ", "일반 18개＋실험 3개＝21개 모듈; 42개 가이드",
                   "regular_packages-18 experimental_packages-3 bilingual_guides-42")
        for text in samples:
            with self.subTest(text=text):
                self.assertEqual(validate_public_counts(text, 21, 18, 3), [])
                self.assertTrue(validate_public_counts(text, 22, 18, 4))
        self.assertTrue(validate_public_counts("两项隔离实验。", 21, 18, 3))
        self.assertEqual(validate_public_counts("21 generated English guides; 21 generated Simplified Chinese guides", 21, 18, 3), [])
        self.assertTrue(validate_public_counts("20 module guides", 21, 18, 3))

    def test_historical_sections_preserve_counts_but_do_not_hide_current_sections(self):
        history = "## Historical v1.2.0\n20 modules and 40 guides\n### Details\n2 experimental packages\n"
        self.assertEqual(validate_public_counts(history, 21, 18, 3), [])
        self.assertTrue(validate_public_counts(history + "## Current release\n20 modules\n", 21, 18, 3))

    def test_public_counts_include_catalog_scope_and_all_overview_languages(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            names = ("SKILL_CATALOG.md", "PUBLICATION_SCOPE.md", "docs/index.html", "docs/skills/INDEX.md",
                     "docs/i18n/ja/README.md", "docs/i18n/ko/README.md", "docs/i18n/zh-CN/README.md")
            for name in names:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("21 modules", encoding="utf-8")
            checked = {p.relative_to(root).as_posix() for p in public_count_files(root)}
            self.assertTrue(set(names) <= checked)

    def test_missing_director_example_reports_error_without_a_traceback(self):
        with tempfile.TemporaryDirectory() as raw:
            errors = validate_director_example(Path(raw))
            self.assertEqual(len(errors), 1)
            self.assertIn("cannot read", errors[0])

    def test_launch_assets_reject_missing_or_duplicate_entries(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            folder = root / "docs/assets"
            folder.mkdir(parents=True)
            entries = []
            for name in sorted(REQUIRED_LAUNCH_ASSETS):
                data = (b"\x89PNG\r\n\x1a\n" + b"\0\0\0\rIHDR" + struct.pack(">II", 4, 3)
                        if name.endswith(".png") else b"<svg/>")
                (folder / name).write_bytes(data)
                entries.append({"path": name, "sha256": hashlib.sha256(data).hexdigest(), "width": 4, "height": 3})
            path = folder / "launch-assets.json"
            path.write_text(json.dumps({"assets": entries}), encoding="utf-8")
            self.assertEqual(validate_launch_assets(root), [])
            for changed, expected in ((entries[:-1], "inventory mismatch"), (entries + [entries[0]], "duplicate paths")):
                path.write_text(json.dumps({"assets": changed}), encoding="utf-8")
                self.assertTrue(any(expected in e for e in validate_launch_assets(root)))

    def test_clickable_preview_requires_image_inside_the_original_video_link(self):
        source, video = "docs/media/poster.png", "https://example.org/clip.mp4"
        good = f'<a href="{video}"><img src="{source}" alt="Preview" /></a>'
        self.assertTrue(has_linked_image(good, source, video))
        self.assertTrue(has_linked_image(f"[![Preview]({source})]({video})", source, video))
        for text in (f'<a href="{video}">{source}</a>', f'<img src="{source}"><a href="{video}">Play</a>',
                     good.replace(video, "https://example.org/other.mp4"), "```html\n" + good + "\n```"):
            with self.subTest(text=text):
                self.assertFalse(has_linked_image(text, source, video))

    def test_gif_metadata_counts_image_blocks_and_real_delays(self):
        # Container metadata fixtures do not claim full pixel decoding or visual validity.
        header = b"GIF89a" + struct.pack("<HH", 4, 3) + b"\0\0\0"
        loop = b"\x21\xff\x0bNETSCAPE2.0\x03\x01\0\0\0"
        descriptor = b"\x2c" + struct.pack("<HHHH", 0, 0, 4, 3) + b"\0\x02"
        image_data = b"\x06\x21\xf9\x04abc\0"
        first = b"\x21\xf9\x04\0\x0c\0\0\0" + descriptor + image_data
        second = b"\x21\xf9\x04\0\x0d\0\0\0" + descriptor + b"\x02\x44\x01\0"
        payload = header + loop + first + second + b"\x3b"
        self.assertEqual(gif_metadata(payload), {"width": 4, "height": 3, "frames": 2, "duration_ms": 250, "loop": 0})
        item = {"preview_width": 4, "preview_height": 3, "preview_frames": 2, "preview_duration_ms": 250}
        self.assertEqual(preview_metadata_errors(payload, item), [])
        for field in item:
            changed = dict(item, **{field: 999999})
            self.assertTrue(preview_metadata_errors(payload, changed), field)
        for broken in (payload[:-1], payload[:-5], b"GIF89a", header + b"\x3b"):
            with self.subTest(broken=broken), self.assertRaises(ValueError):
                gif_metadata(broken)

    def test_published_snapshot_links_exact_release_and_rejects_wrong_asset(self):
        page = ROOT / "docs/skills/en/example.md"
        item = {"name": "example", "download": {"state": "published_snapshot", "tag": "v1.4.0",
                "asset": "example.zip", "note": {"en": "Published source snapshot."}}}
        link, _ = download_link(item, page, "en")
        self.assertIn("releases/download/v1.4.0/example.zip", link)
        self.assertNotIn("Historical", link)
        item["download"]["asset"] = "another.zip"
        with self.assertRaises(ValueError):
            download_link(item, page, "en")

    def test_downloads_distinguish_current_source_and_historical_assets(self):
        page = ROOT / "docs/skills/en/example.md"
        historical = {"name": "ai-storyboard-director", "download": {"state": "historical_snapshot", "tag": "v1.3.0", "asset": "ai-storyboard-director.zip", "note": {"en": "Historical 5.4.4; current source is 5.6.0."}}}
        link, note = download_link(historical, page, "en")
        self.assertIn("releases/download/v1.3.0/ai-storyboard-director.zip", link)
        self.assertNotIn("latest", link)
        self.assertIn("5.4.4", note)
        current = {"name": "whitebox-previs-executor", "download": {"state": "source_only", "source_install": "docs/INSTALLATION.md#experimental-packages", "note": {"en": "No release asset yet."}}}
        link, _ = download_link(current, page, "en")
        self.assertIn("../../INSTALLATION.md#experimental-packages", link)
        self.assertNotIn(".zip", link)

    def test_download_contract_rejects_asset_identity_or_path_escape(self):
        page = ROOT / "docs/skills/en/example.md"
        for download in ({"state": "historical_snapshot", "tag": "v1.3.0", "asset": "another-skill.zip", "note": "history"}, {"state": "source_only", "source_install": "../outside.md", "note": "source"}, {"state": "invented", "note": "unknown"}):
            with self.subTest(download=download), self.assertRaises(ValueError):
                download_link({"name": "example", "download": download}, page, "en")

    def test_static_page_rejects_script_event_handler_and_missing_anchor(self):
        parser = SiteParser()
        parser.feed('<main id="main"><a href="#missing">jump</a><img src="x.png" onerror="alert(1)"><script>run()</script></main><div id="main"></div>')
        errors = markup_errors(parser)
        for expected in ("duplicate id", "event attributes", "must not contain scripts", "broken section link"):
            self.assertTrue(any(expected in value for value in errors), errors)

    def test_previs_nonfilm_boundary_accepts_equivalent_english_and_chinese(self):
        self.assertTrue(has_previs_nonfilm_boundary("These clips are not finished AI films."))
        self.assertTrue(has_previs_nonfilm_boundary("这些历史片段不证明任意完整打斗、最终AI成片或新的用户接受。"))
        self.assertFalse(has_previs_nonfilm_boundary("These previews prove finished AI films."))

    def test_webp_metadata_parses_vp8_vp8l_and_rejects_truncated_or_animated_containers(self):
        lossless = b"\x2f" + ((4 - 1) | ((3 - 1) << 14)).to_bytes(4, "little")
        self.assertEqual(webp_dimensions(webp_container(b"VP8L", lossless)), (4, 3))
        lossy = b"\0\0\0\x9d\x01\x2a" + (4).to_bytes(2, "little") + (3).to_bytes(2, "little")
        self.assertEqual(webp_dimensions(webp_container(b"VP8 ", lossy)), (4, 3))
        self.assertIsNone(webp_dimensions(webp_container(b"VP8L", lossless)[:-1]))
        extended = b"\x02\0\0\0" + (3).to_bytes(3, "little") + (2).to_bytes(3, "little")
        self.assertIsNone(webp_dimensions(webp_container(b"VP8X", extended)))


class ShowcaseContractTests(unittest.TestCase):
    def fixture(self, root: Path) -> tuple[Path, dict]:
        # Metadata-parser fixtures do not claim decoded image or aesthetic validity.
        folder = root / "docs/showcase"
        (folder / "originals").mkdir(parents=True)
        preview = webp_container(b"VP8L", b"\x2f" + ((4 - 1) | ((3 - 1) << 14)).to_bytes(4, "little"))
        original = b"\x89PNG\r\n\x1a\n" + (13).to_bytes(4, "big") + b"IHDR" + struct.pack(">II", 8, 6)
        (folder / "one.webp").write_bytes(preview)
        (folder / "originals/one.png").write_bytes(original)
        skill = root / "skills/cyberpunk-design"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("test runtime", encoding="utf-8")
        item = {"id": "one", "skill": "cyberpunk-design", "genre": "赛博朋克", "genre_en": "Cyberpunk", "title": "样本", "title_en": "Sample", "file": "one.webp", "width": 4, "height": 3, "bytes": len(preview), "sha256": hashlib.sha256(preview).hexdigest(), "original_file": "originals/one.png", "original_width": 8, "original_height": 6, "original_bytes": len(original), "original_sha256": hashlib.sha256(original).hexdigest(), "source_kind": "original_builtin_imagegen", "status": "user_accepted", "availability": "packaged", "visible_contract": "One reviewed sample, not a stability claim."}
        manifest = {"schema_version": "1.0", "publication": "test", "inventory_freeze": "2026-09-07", "expected_count": 1, "expected_genre_count": 1, "rights_basis": "original and authorized", "acceptance_scope": "one sample", "items": [item]}
        return folder / "manifest.json", manifest

    def validate(self, root: Path, path: Path, manifest: dict) -> list[str]:
        path.write_text(json.dumps(manifest), encoding="utf-8")
        return validate_showcase(root, require_links=False)

    def test_showcase_hashes_and_metadata_are_checked(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            path, manifest = self.fixture(root)
            self.assertEqual(self.validate(root, path, manifest), [])
            manifest["items"][0]["original_sha256"] = "0" * 64
            self.assertTrue(any("hash mismatch" in e for e in self.validate(root, path, manifest)))

    def test_showcase_requires_readme_preview_and_original_without_a_website(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            path, manifest = self.fixture(root)
            path.write_text(json.dumps(manifest), encoding="utf-8")
            preview = '<img src="docs/showcase/one.webp" alt="sample" />'
            original = '<a href="docs/showcase/originals/one.png">Original</a>'
            readme = root / "README.md"
            readme.write_text(preview + original, encoding="utf-8")
            self.assertFalse((root / "docs/index.html").exists())
            self.assertEqual(validate_showcase(root), [])
            for missing, content in (("original_file", preview), ("file", original)):
                with self.subTest(missing=missing):
                    readme.write_text(content, encoding="utf-8")
                    errors = validate_showcase(root)
                    self.assertTrue(any(f"{missing} must be linked from README" in e for e in errors), errors)

    def test_showcase_rejects_path_escape_and_unsupported_external_skill(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            path, manifest = self.fixture(root)
            manifest["items"][0]["file"] = "../private.webp"
            manifest["items"][0]["availability"] = "external_not_redistributed"
            errors = self.validate(root, path, manifest)
            self.assertTrue(any("unsafe file" in e for e in errors), errors)
            self.assertTrue(any("unsupported external Skill" in e for e in errors), errors)

    def test_showcase_rejects_duplicate_identity_or_changed_aspect_ratio(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            path, manifest = self.fixture(root)
            manifest["items"].append(copy.deepcopy(manifest["items"][0]))
            self.assertTrue(any("duplicate showcase id" in e for e in self.validate(root, path, manifest)))
            manifest["items"] = manifest["items"][:1]
            item = manifest["items"][0]
            original = b"\x89PNG\r\n\x1a\n" + (13).to_bytes(4, "big") + b"IHDR" + struct.pack(">II", 16, 6)
            (path.parent / item["original_file"]).write_bytes(original)
            item.update({"original_width": 16, "original_height": 6, "original_bytes": len(original), "original_sha256": hashlib.sha256(original).hexdigest()})
            self.assertTrue(any("aspect ratio" in e for e in self.validate(root, path, manifest)))

    def test_showcase_accepts_browser_screenshot_only_for_web_design(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            path, manifest = self.fixture(root)
            item = manifest["items"][0]
            web_skill = root / "skills/web-design-director"
            web_skill.mkdir(parents=True)
            (web_skill / "SKILL.md").write_text("test runtime", encoding="utf-8")
            item.update({"skill": "web-design-director", "source_kind": "original_browser_screenshot"})
            self.assertEqual(self.validate(root, path, manifest), [])
            item["skill"] = "cyberpunk-design"
            self.assertTrue(any("unsupported source provenance" in e for e in self.validate(root, path, manifest)))


if __name__ == "__main__":
    unittest.main()
