from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_review_profiles as builder
from repository_safety import MARKER_PAYLOAD, OUTPUT_MARKER, SafetyError


class ReviewProfileTests(unittest.TestCase):
    def setUp(self):
        self.area = tempfile.TemporaryDirectory(prefix="review-profile-test-")
        self.addCleanup(self.area.cleanup)
        self.base = Path(self.area.name)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        self.temp = self.base / "scratch"
        self.temp.mkdir()
        self.output = self.base / "output"
        (self.repo / "LICENSE").write_bytes(b"Repository license.\n")
        (self.repo / "NOTICE").write_bytes(b"Repository notice.\n")
        for area, names in (("skills", builder.REGULAR), ("experimental", builder.EXPERIMENTAL)):
            for name in names:
                skill = self.repo / area / name
                skill.mkdir(parents=True)
                content = f"---\nname: {name}\ndescription: fixture\n---\n"
                if name == "ai-storyboard-director":
                    content += f"维护版本 **{builder.VERSION}**。\n"
                (skill / "SKILL.md").write_text(content, encoding="utf-8")
        custom = self.repo / "skills/noir-design"
        (custom / "license.txt").write_bytes(b"Package-specific license.\n")
        (custom / "third-party").mkdir()
        (custom / "third-party/LICENSE").write_bytes(b"Third-party terms.\n")
        (self.repo / "scripts").mkdir()
        self.semantic = b'"""Standalone optional reviewer fixture."""\nprint("fixture")\n'
        (self.repo / "scripts/semantic_review.py").write_bytes(self.semantic)

    def build(self, output=None):
        return builder.build_profiles(self.repo, output or self.output, self.temp, allow_external=True)

    def read_zip(self, name):
        with zipfile.ZipFile(self.output / name) as archive:
            self.assertIsNone(archive.testzip())
            return {entry: archive.read(entry) for entry in archive.namelist()}

    def test_shared_core_is_identical_and_jev_overlay_is_narrow(self):
        result = self.build()
        a = self.read_zip(result["artifacts"][0]["file"])
        b = self.read_zip(result["artifacts"][1]["file"])
        expected_extra = {builder.STORYBOARD + "references/semantic-review.md", builder.STORYBOARD + "scripts/semantic_review.py"}
        self.assertEqual(set(b) - set(a), expected_extra)
        self.assertFalse(set(a) - set(b))
        differing = {path for path in a if a[path] != b[path]}
        self.assertEqual(differing, {"PROFILE.json", builder.STORYBOARD + "SKILL.md", builder.STORYBOARD + "VERSION_MANIFEST.json", builder.STORYBOARD + "VERSION_MANIFEST.sha256"})
        expected_b = a[builder.STORYBOARD + "SKILL.md"].decode().replace("**5.7.1**", "**5.7.1-jev**") + builder.B_SECTION
        self.assertEqual(b[builder.STORYBOARD + "SKILL.md"].decode(), expected_b)
        self.assertEqual(b[builder.STORYBOARD + "scripts/semantic_review.py"], self.semantic)
        self.assertNotIn("scripts/check_skill_suite.py", a)
        self.assertNotIn("scripts/check_skill_suite.py", b)
        for profile, files in (("A", a), ("B", b)):
            payload = json.loads(files["PROFILE.json"])
            self.assertEqual(payload["profile"], profile)
            self.assertEqual(payload["status"], "candidate")
            self.assertEqual(payload["user_test_status"], "pending")
            self.assertFalse(payload["default_network"])
            self.assertFalse(payload["default_enabled"])
            self.assertEqual(payload["common_core_digest"], result["common_core_digest"])
            self.assertEqual(len(payload["packages"]), 21)
            version_data = files[builder.STORYBOARD + "VERSION_MANIFEST.json"]
            self.assertIs(json.loads(version_data)["cross_version_runtime_references_allowed"], False)
            self.assertEqual(files[builder.STORYBOARD + "VERSION_MANIFEST.sha256"].decode().split()[0], hashlib.sha256(version_data).hexdigest())
            for item in json.loads(version_data)["runtime_files"]:
                self.assertEqual(hashlib.sha256(files[builder.STORYBOARD + item["path"]]).hexdigest(), item["sha256"])
        recomputed = [{"path": x["path"], "sha256": hashlib.sha256(a[x["path"]]).hexdigest()} for x in result["common_core_files"]]
        self.assertEqual(builder.sha(builder.json_bytes(recomputed)), result["common_core_digest"])
        self.assertEqual(list(self.temp.iterdir()), [])

    def test_archive_is_repeatable_and_licenses_close_each_package(self):
        first = self.build()
        other = self.base / "another-output"
        second = self.build(other)
        self.assertEqual(first, second)
        for item in first["artifacts"]:
            self.assertEqual((self.output / item["file"]).read_bytes(), (other / item["file"]).read_bytes())
            with zipfile.ZipFile(self.output / item["file"]) as archive:
                for package in first["packages"]:
                    license_name = "license.txt" if package["name"] == "noir-design" else "LICENSE"
                    self.assertIn(package["path"] + "/" + license_name, archive.namelist())
                for notice in first["licenses"]:
                    self.assertEqual(builder.sha(archive.read(notice["path"])), notice["sha256"])
                self.assertEqual(archive.read("skills/noir-design/third-party/LICENSE"), b"Third-party terms.\n")
                self.assertTrue(all(info.date_time == builder.packages.FIXED_TIME for info in archive.infolist()))

    def test_refuses_nonempty_target_even_with_tool_marker(self):
        self.output.mkdir()
        sentinel = self.output / "important.txt"
        sentinel.write_bytes(b"Keep me")
        (self.output / OUTPUT_MARKER).write_text(json.dumps(MARKER_PAYLOAD), encoding="utf-8")
        with self.assertRaises(SafetyError):
            self.build()
        self.assertEqual(sentinel.read_bytes(), b"Keep me")
        self.assertEqual(list(self.temp.iterdir()), [])

    def test_external_output_and_repository_temp_require_explicit_boundaries(self):
        with self.assertRaises(SafetyError):
            builder.build_profiles(self.repo, self.output, self.temp)
        internal_temp = self.repo / "tmp"
        internal_temp.mkdir()
        with self.assertRaises(SafetyError):
            builder.build_profiles(self.repo, self.output, internal_temp, allow_external=True)
        with self.assertRaises(SafetyError):
            builder.build_profiles(self.repo, self.repo / "skills/new-output", self.temp, allow_external=True)
        self.assertFalse(self.output.exists())

    def test_linked_destination_or_source_is_rejected_without_mutation(self):
        # Emulate a Windows junction even where unprivileged symlinks are unavailable.
        linked = self.base / "linked"
        linked.mkdir()
        real_check = builder.is_link_like
        with mock.patch.object(builder, "is_link_like", side_effect=lambda p: p == linked or real_check(p)):
            with self.assertRaises(SafetyError):
                self.build(linked / "output")
        source = self.repo / "skills/ai-storyboard-director/SKILL.md"
        with mock.patch.object(builder, "is_link_like", side_effect=lambda p: p == source or real_check(p)):
            with self.assertRaises(SafetyError):
                self.build()
        self.assertEqual(list(linked.iterdir()), [])
        self.assertFalse(self.output.exists())

    def test_private_file_or_literal_credential_refuses_archive(self):
        private = self.repo / "skills/prop-asset/.env"
        private.write_bytes(b"PRIVATE=fixture\n")
        with self.assertRaises(SafetyError):
            self.build()
        private.unlink()
        target = self.repo / "skills/prop-asset/SKILL.md"
        target.write_text(target.read_text(encoding="utf-8") + "\n" + "ghp_" + "A" * 36, encoding="utf-8")
        with self.assertRaises(SafetyError):
            self.build()
        self.assertFalse(self.output.exists())

    def test_bare_jev_credential_is_refused_without_echoing_its_value(self):
        target = self.repo / "skills/prop-asset/SKILL.md"
        fake = "api" + "key_" + "a" * 36 + "_" + "b" * 64
        target.write_text(target.read_text(encoding="utf-8") + "\n" + fake, encoding="utf-8")
        with self.assertRaises(SafetyError) as caught:
            self.build()
        self.assertNotIn(fake, str(caught.exception))
        self.assertIn("possible credential refused", str(caught.exception))
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
