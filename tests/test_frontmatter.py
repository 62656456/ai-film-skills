from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_repository import parse_frontmatter


class FrontmatterTests(unittest.TestCase):
    def test_folded_yaml_description_is_parsed(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "SKILL.md"
            path.write_text(
                "---\nname: folded-skill\ndescription: >\n  first line\n  second line\n---\n",
                encoding="utf-8",
            )
            values, keys, error = parse_frontmatter(path)
            self.assertIsNone(error)
            self.assertEqual(keys, {"name", "description"})
            self.assertEqual(values["description"], "first line second line")

    def test_duplicate_yaml_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "SKILL.md"
            path.write_text(
                "---\nname: one\nname: two\ndescription: test\n---\n",
                encoding="utf-8",
            )
            _, _, error = parse_frontmatter(path)
            self.assertIsNotNone(error)
            self.assertIn("duplicate key", error or "")


if __name__ == "__main__":
    unittest.main()
