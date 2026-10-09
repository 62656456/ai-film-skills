"""Verify fixed font inputs without changing published art."""
import hashlib
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import render_social_preview as social
import render_storyboard_proof as proof


class RenderAssetsTests(unittest.TestCase):
    def test_default_fonts_ignore_host_windows_directory(self):
        with mock.patch.dict(os.environ, {"WINDIR": "/unrelated/fonts"}, clear=True):
            self.assertEqual(social.font_dir_default(), social.PINNED_FONT_DIR)
            self.assertEqual(social.font(14).getname()[0], "DejaVu Sans")

    def test_modified_font_input_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "DejaVuSans.ttf"
            candidate.write_bytes(b"unexpected font")
            with self.assertRaisesRegex(ValueError, "pinned DejaVu"):
                social.font(14, font_dir=Path(directory))

    def test_both_renderers_repeat_with_same_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            for renderer in (social.render, proof.render):
                first = Path(directory) / "first.png"
                second = Path(directory) / "second.png"
                renderer(first, social.PINNED_FONT_DIR)
                renderer(second, social.PINNED_FONT_DIR)
                self.assertEqual(hashlib.sha256(first.read_bytes()).digest(),
                                 hashlib.sha256(second.read_bytes()).digest())


if __name__ == "__main__":
    unittest.main()
