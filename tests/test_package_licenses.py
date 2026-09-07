from __future__ import annotations

import copy
import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_skill_packages as builder
import generate_skill_guides as guides
from repository_safety import SafetyError


class PackageLicenseTests(unittest.TestCase):
    def make_repository(self, root: Path) -> Path:
        (root / "LICENSE").write_bytes(b"Repository license contents.\n")
        output = root / "output"
        output.mkdir()
        return output

    def make_skill(self, root: Path, name: str) -> Path:
        skill = root / "skills" / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(f"---\nname: {name}\ndescription: fixture\n---\n", encoding="utf-8")
        return skill

    def assert_license_manifest_matches(self, output: Path, item: dict):
        with zipfile.ZipFile(output / item["file"]) as archive:
            self.assertIsNone(archive.testzip())
            for notice in item["licenses"]:
                self.assertEqual(hashlib.sha256(archive.read(notice["path"])).hexdigest(), notice["sha256"])

    def test_single_package_attaches_repository_license_without_touching_source(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            output = self.make_repository(root)
            skill = self.make_skill(root, "sample-skill")
            before = {p.relative_to(skill): p.read_bytes() for p in skill.rglob("*") if p.is_file()}
            with mock.patch.object(builder, "ROOT", root):
                item = builder.build_one(skill, output)
            with zipfile.ZipFile(output / item["file"]) as archive:
                self.assertEqual(archive.read("sample-skill/LICENSE"), (root / "LICENSE").read_bytes())
            self.assertEqual(item["licenses"][0]["source"], "repository_default")
            self.assertEqual(before, {p.relative_to(skill): p.read_bytes() for p in skill.rglob("*") if p.is_file()})
            self.assert_license_manifest_matches(output, item)

    def test_guide_links_injected_notices_without_claiming_historical_archives_changed(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.make_repository(root)
            skill = self.make_skill(root, "sample-skill")
            page = root / "docs/skills/en/sample-skill.md"
            with mock.patch.object(builder, "ROOT", root), mock.patch.object(guides, "ROOT", root):
                text = "\n".join(guides.resources(page, skill, "en"))
            self.assertIn("[`LICENSE`](../../../LICENSE)", text)
            self.assertIn("Historical release archives are unchanged", text)
            self.assertFalse((skill / "LICENSE").exists())

    def test_own_license_is_preserved_in_single_and_complete_packages(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            output = self.make_repository(root)
            director = self.make_skill(root, "director-agent")
            custom = self.make_skill(root, "custom-skill")
            (custom / "license.txt").write_bytes(b"Different package license; retain these terms.\n")
            with mock.patch.object(builder, "ROOT", root):
                single = builder.build_one(custom, output)
                complete = builder.build_complete([director, custom], output)
            with zipfile.ZipFile(output / single["file"]) as archive:
                self.assertNotIn("custom-skill/LICENSE", archive.namelist())
                self.assertEqual(archive.read("custom-skill/license.txt"), (custom / "license.txt").read_bytes())
            with zipfile.ZipFile(output / complete["file"]) as archive:
                self.assertEqual(archive.read("skills/director-agent/LICENSE"), (root / "LICENSE").read_bytes())
                self.assertEqual(archive.read("skills/custom-skill/license.txt"), (custom / "license.txt").read_bytes())
                self.assertNotIn("skills/custom-skill/LICENSE", archive.namelist())
            self.assertEqual(single["licenses"][0]["source"], "package")
            self.assert_license_manifest_matches(output, single)
            self.assert_license_manifest_matches(output, complete)

    def test_nested_third_party_terms_and_package_notice_are_not_overwritten(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            output = self.make_repository(root)
            (root / "NOTICE").write_bytes(b"Repository notice.\n")
            skill = self.make_skill(root, "sample-skill")
            third_party = skill / "third-party"
            third_party.mkdir()
            (third_party / "LICENSE").write_bytes(b"Third-party terms stay distinct.\n")
            (skill / "NOTICE").write_bytes(b"Package-specific attribution.\n")
            with mock.patch.object(builder, "ROOT", root):
                item = builder.build_one(skill, output)
            with zipfile.ZipFile(output / item["file"]) as archive:
                self.assertEqual(archive.read("sample-skill/LICENSE"), (root / "LICENSE").read_bytes())
                self.assertEqual(archive.read("sample-skill/third-party/LICENSE"), (third_party / "LICENSE").read_bytes())
                self.assertEqual(archive.read("sample-skill/NOTICE"), (skill / "NOTICE").read_bytes())
            self.assertEqual(next(n["source"] for n in item["licenses"] if "third-party" in n["path"]), "package")
            self.assert_license_manifest_matches(output, item)

    def test_inherited_repository_notice_is_included_when_present(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            output = self.make_repository(root)
            (root / "NOTICE").write_bytes(b"Repository attribution.\n")
            skill = self.make_skill(root, "sample-skill")
            with mock.patch.object(builder, "ROOT", root):
                item = builder.build_one(skill, output)
            with zipfile.ZipFile(output / item["file"]) as archive:
                self.assertEqual(archive.read("sample-skill/NOTICE"), (root / "NOTICE").read_bytes())
            self.assertEqual(len(item["licenses"]), 2)

    def test_missing_or_link_like_repository_license_is_rejected_before_zip_creation(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            output = self.make_repository(root)
            skill = self.make_skill(root, "sample-skill")
            with mock.patch.object(builder, "ROOT", root), mock.patch.object(builder, "is_link_like", return_value=True):
                with self.assertRaises(SafetyError):
                    builder.build_one(skill, output)
            self.assertFalse((output / "sample-skill.zip").exists())
            (root / "LICENSE").unlink()
            with mock.patch.object(builder, "ROOT", root), self.assertRaises(SafetyError):
                builder.build_one(skill, output)
            self.assertFalse((output / "sample-skill.zip").exists())

    def test_existing_package_license_does_not_require_or_inherit_repository_license(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            output = self.make_repository(root)
            skill = self.make_skill(root, "sample-skill")
            (skill / "COPYING").write_bytes(b"Self-contained package permission.\n")
            (root / "LICENSE").unlink()
            with mock.patch.object(builder, "ROOT", root):
                item = builder.build_one(skill, output)
            self.assertEqual(item["licenses"][0]["path"], "sample-skill/COPYING")
            self.assertEqual(item["licenses"][0]["source"], "package")

    def test_named_dual_license_files_do_not_gain_an_unrequested_default_license(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            output = self.make_repository(root)
            skill = self.make_skill(root, "sample-skill")
            (skill / "LICENSE-MIT").write_bytes(b"Package option one.\n")
            (skill / "LICENSE-BSD.txt").write_bytes(b"Package option two.\n")
            with mock.patch.object(builder, "ROOT", root):
                item = builder.build_one(skill, output)
            with zipfile.ZipFile(output / item["file"]) as archive:
                self.assertNotIn("sample-skill/LICENSE", archive.namelist())
            self.assertEqual(len(item["licenses"]), 2)
            self.assertTrue(all(entry["source"] == "package" for entry in item["licenses"]))

    def test_empty_own_license_cannot_be_misreported_as_a_licensed_package(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            output = self.make_repository(root)
            skill = self.make_skill(root, "sample-skill")
            (skill / "LICENSE.md").write_bytes(b" \n")
            with mock.patch.object(builder, "ROOT", root), self.assertRaisesRegex(SafetyError, "must not be empty"):
                builder.build_one(skill, output)
            self.assertFalse((output / "sample-skill.zip").exists())

    def test_license_bytes_are_verified_and_packages_remain_deterministic(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            output = self.make_repository(root)
            second = root / "second-output"
            second.mkdir()
            skill = self.make_skill(root, "director-agent")
            with mock.patch.object(builder, "ROOT", root):
                first_single = builder.build_one(skill, output)
                second_single = builder.build_one(skill, second)
                first_complete = builder.build_complete([skill], output)
                second_complete = builder.build_complete([skill], second)
            self.assertEqual(first_single, second_single)
            self.assertEqual(first_complete, second_complete)
            tampered = copy.deepcopy(first_single["licenses"])
            tampered[0]["sha256"] = "0" * 64
            with self.assertRaisesRegex(RuntimeError, "license bytes differ"):
                builder.verify_archive(output / first_single["file"], "director-agent/SKILL.md", tampered)


if __name__ == "__main__":
    unittest.main()
