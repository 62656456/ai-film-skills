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
from validate_pages_site import SiteParser, markup_errors, has_previs_nonfilm_boundary
from validate_repository import validate_public_counts
from validate_style_gallery import validate_showcase, webp_dimensions


def webp_container(kind: bytes, data: bytes) -> bytes:
    chunk = kind + len(data).to_bytes(4, "little") + data + (b"\0" if len(data) % 2 else b"")
    return b"RIFF" + (len(chunk) + 4).to_bytes(4, "little") + b"WEBP" + chunk


class PublicContractTests(unittest.TestCase):
    def test_current_counts_follow_registry_and_dated_history_is_allowed(self):
        self.assertEqual(validate_public_counts("20 modules and 40 bilingual guides", 20), [])
        self.assertTrue(validate_public_counts("19 modules and 38 guides", 20))
        self.assertEqual(validate_public_counts("Historical v1.3.0: 19 modules and 38 guides", 20), [])

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


if __name__ == "__main__":
    unittest.main()
