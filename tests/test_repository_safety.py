from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from repository_safety import (
    SafetyError,
    package_source_files,
    safe_source_files,
    validate_output_target,
)


class RepositorySafetyTests(unittest.TestCase):
    def test_repository_root_is_never_an_output(self) -> None:
        with self.assertRaises(SafetyError):
            validate_output_target(ROOT, ROOT)

    def test_non_empty_unowned_internal_output_is_rejected(self) -> None:
        (ROOT / "dist").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / "dist") as raw:
            target = Path(raw)
            (target / "sentinel.txt").write_text("keep", encoding="utf-8")
            with self.assertRaises(SafetyError):
                validate_output_target(target, ROOT)
            self.assertEqual((target / "sentinel.txt").read_text(encoding="utf-8"), "keep")

    def test_external_output_requires_explicit_flag(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = Path(raw) / "packages"
            with self.assertRaises(SafetyError):
                validate_output_target(target, ROOT)
            self.assertEqual(
                validate_output_target(target, ROOT, allow_external=True), target.resolve()
            )

    def test_source_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            skill = base / "skill"
            skill.mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: skill\ndescription: test\n---\n", encoding="utf-8"
            )
            outside = base / "secret.txt"
            outside.write_text("secret", encoding="utf-8")
            link = skill / "leak.txt"
            try:
                os.symlink(outside, link)
            except OSError as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")
            with self.assertRaises(SafetyError):
                safe_source_files(skill)

    def test_output_symlink_is_rejected(self) -> None:
        (ROOT / "dist").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory() as raw:
            outside = Path(raw) / "outside"
            outside.mkdir()
            link = ROOT / "dist" / "linked-output-test"
            try:
                os.symlink(outside, link, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"directory symlink creation unavailable: {exc}")
            try:
                with self.assertRaises(SafetyError):
                    validate_output_target(link, ROOT)
            finally:
                link.unlink(missing_ok=True)

    @unittest.skipUnless(os.name == "nt", "Windows junction test")
    def test_source_junction_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            skill = base / "skill"
            outside = base / "outside"
            skill.mkdir()
            outside.mkdir()
            (skill / "SKILL.md").write_text(
                "---\nname: skill\ndescription: test\n---\n", encoding="utf-8"
            )
            (outside / "secret.txt").write_text("secret", encoding="utf-8")
            junction = skill / "linked-directory"
            result = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(junction), str(outside)],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                self.skipTest(f"junction creation unavailable: {result.stderr or result.stdout}")
            try:
                with self.assertRaises(SafetyError):
                    safe_source_files(skill)
            finally:
                junction.rmdir()

    def test_interpreter_caches_are_not_packaged(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            skill = Path(raw) / "skill"
            cache = skill / "scripts" / "__pycache__"
            cache.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: skill\ndescription: test\n---\n", encoding="utf-8"
            )
            (cache / "helper.pyc").write_bytes(b"cache")
            relative = [path.relative_to(skill).as_posix() for path in package_source_files(skill)]
            self.assertEqual(relative, ["SKILL.md"])

    def test_cli_refuses_repository_root_without_deleting_sentinel(self) -> None:
        sentinel = ROOT / "safety-test-sentinel.txt"
        sentinel.write_text("keep", encoding="utf-8")
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "build_skill_packages.py"),
                    "--output",
                    str(ROOT),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")
        finally:
            sentinel.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
