from __future__ import annotations

import contextlib
import io
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from repository_safety import (
    SafetyError,
    commit_staging_output,
    package_source_files,
    safe_source_files,
    validate_output_target,
    write_output_marker,
)
from build_skill_packages import build_one
from install_skill import install


def temporary_directory() -> tempfile.TemporaryDirectory:
    return tempfile.TemporaryDirectory(dir=os.environ.get("SKILL_RELEASE_TEST_TEMP"))


class RepositorySafetyTests(unittest.TestCase):
    def test_repository_root_is_never_an_output(self) -> None:
        with self.assertRaises(SafetyError):
            validate_output_target(ROOT, ROOT)

    def test_non_empty_unowned_internal_output_is_rejected(self) -> None:
        with temporary_directory() as raw:
            repo = Path(raw) / "repo"
            target = repo / "dist" / "packages"
            target.mkdir(parents=True)
            (target / "sentinel.txt").write_text("keep", encoding="utf-8")
            with self.assertRaises(SafetyError):
                validate_output_target(target, repo)
            self.assertEqual((target / "sentinel.txt").read_text(encoding="utf-8"), "keep")

    def test_external_output_requires_explicit_flag(self) -> None:
        with temporary_directory() as raw:
            target = Path(raw) / "packages"
            with self.assertRaises(SafetyError):
                validate_output_target(target, ROOT)
            self.assertEqual(
                validate_output_target(target, ROOT, allow_external=True), target.resolve()
            )

    def test_source_symlink_is_rejected(self) -> None:
        with temporary_directory() as raw:
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
        with temporary_directory() as raw:
            repo = Path(raw) / "repo"
            (repo / "dist").mkdir(parents=True)
            outside = Path(raw) / "outside"
            outside.mkdir()
            link = repo / "dist" / "linked-output-test"
            try:
                os.symlink(outside, link, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"directory symlink creation unavailable: {exc}")
            try:
                with self.assertRaises(SafetyError):
                    validate_output_target(link, repo)
            finally:
                link.unlink(missing_ok=True)

    @unittest.skipUnless(os.name == "nt", "Windows junction test")
    def test_source_junction_is_rejected(self) -> None:
        with temporary_directory() as raw:
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
        with temporary_directory() as raw:
            skill = Path(raw) / "skill"
            cache = skill / "scripts" / "__pycache__"
            cache.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: skill\ndescription: test\n---\n", encoding="utf-8"
            )
            (cache / "helper.pyc").write_bytes(b"cache")
            relative = [path.relative_to(skill).as_posix() for path in package_source_files(skill)]
            self.assertEqual(relative, ["SKILL.md"])

    def test_cli_refuses_unowned_output_without_deleting_sentinel(self) -> None:
        with temporary_directory() as raw:
            output = Path(raw) / "packages"
            output.mkdir()
            sentinel = output / "sentinel.txt"
            sentinel.write_text("keep", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "build_skill_packages.py"),
                    "--output",
                    str(output),
                    "--allow-external-output",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")

    def test_zip_and_install_exclude_private_local_files_but_keep_runtime(self) -> None:
        with temporary_directory() as raw:
            base = Path(raw)
            skill = base / "skill"
            public = {
                "SKILL.md": "---\nname: skill\ndescription: test\n---\n",
                "LICENSE": "license bytes\n",
                "LICENSE-MIT": "extra license bytes\n",
                "NOTICE": "notice bytes\n",
                "agents/openai.yaml": "display_name: test\n",
                "references/guide.md": "public reference\n",
                "scripts/helper.py": "print('runtime')\n",
                "assets/reference.png": "reference image fixture",
            }
            private = [
                ".env", ".env.local", ".ENV.production", "scripts/.env.secret",
                ".git/config", ".git/objects/local.txt", ".gitignore",
                "logs/session.json", "build/generated.md", "dist/output.json",
                "node_modules/local.json", ".cache/local.json", "run.log",
                "credentials.json", "credentials.production.json",
                "secrets/session.json", "private.pem", "local.bin", "notes.md~",
                "scripts/__pycache__/helper.pyc",
            ]
            for relative, content in public.items():
                path = skill / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content.encode("utf-8"))
            for relative in private:
                path = skill / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("LOCAL-SECRET-DO-NOT-DISTRIBUTE", encoding="utf-8")
            output = base / "packages"
            output.mkdir()
            item = build_one(skill, output)
            with zipfile.ZipFile(output / item["file"]) as archive:
                self.assertIsNone(archive.testzip())
                self.assertEqual(
                    set(archive.namelist()), {f"skill/{relative}" for relative in public}
                )
                for relative, content in public.items():
                    self.assertEqual(archive.read(f"skill/{relative}"), content.encode())
            destination = install(skill, base / "installed", force=False)
            self.assertEqual(
                {path.relative_to(destination).as_posix() for path in destination.rglob("*") if path.is_file()},
                set(public),
            )
            for relative, content in public.items():
                self.assertEqual((destination / relative).read_text(encoding="utf-8"), content)
            self.assertTrue(all((skill / relative).exists() for relative in private))

    def test_committed_output_survives_backup_cleanup_failure(self) -> None:
        with temporary_directory() as raw:
            base = Path(raw)
            output = base / "packages"
            staging = base / "staging"
            for directory, value in [(output, "old"), (staging, "new")]:
                directory.mkdir()
                write_output_marker(directory)
                (directory / "artifact.zip").write_text(value, encoding="utf-8")
            error = io.StringIO()
            with mock.patch("repository_safety.remove_owned_output", side_effect=PermissionError("busy")):
                with contextlib.redirect_stderr(error):
                    commit_staging_output(staging, output)
            backups = list(base.glob(".packages.backup-*"))
            self.assertEqual((output / "artifact.zip").read_text(encoding="utf-8"), "new")
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0] / "artifact.zip").read_text(encoding="utf-8"), "old")
            self.assertIn(str(backups[0]), error.getvalue())
            self.assertIn("output committed", error.getvalue())

    def test_committed_install_survives_backup_and_staging_cleanup_failures(self) -> None:
        with temporary_directory() as raw:
            base = Path(raw)
            source = base / "skill"
            source.mkdir()
            (source / "SKILL.md").write_text("new skill", encoding="utf-8")
            target = base / "installed"
            previous = target / "skill"
            previous.mkdir(parents=True)
            (previous / "SKILL.md").write_text("old skill", encoding="utf-8")
            error = io.StringIO()
            with mock.patch("install_skill.shutil.rmtree", side_effect=PermissionError("busy")):
                with contextlib.redirect_stderr(error):
                    destination = install(source, target, force=True)
            backups = list(target.glob(".skill.backup-*"))
            staging = list(target.glob(".skill-install-*"))
            self.assertEqual(destination, previous)
            self.assertEqual((destination / "SKILL.md").read_text(encoding="utf-8"), "new skill")
            self.assertEqual(len(backups), 1)
            self.assertEqual(len(staging), 1)
            self.assertEqual((backups[0] / "SKILL.md").read_text(encoding="utf-8"), "old skill")
            self.assertIn(str(backups[0]), error.getvalue())
            self.assertIn(str(staging[0]), error.getvalue())
            self.assertIn("installation committed", error.getvalue())

    def test_failed_output_swap_restores_previous_artifact(self) -> None:
        with temporary_directory() as raw:
            base = Path(raw)
            output = base / "packages"
            staging = base / "staging"
            for directory, value in [(output, "old"), (staging, "new")]:
                directory.mkdir()
                write_output_marker(directory)
                (directory / "artifact.zip").write_text(value, encoding="utf-8")
            original_rename = Path.rename

            def fail_staging_swap(path: Path, target: Path) -> Path:
                if path == staging:
                    raise PermissionError("destination busy")
                return original_rename(path, target)

            with mock.patch.object(Path, "rename", fail_staging_swap):
                with self.assertRaises(PermissionError):
                    commit_staging_output(staging, output)
            self.assertEqual((output / "artifact.zip").read_text(encoding="utf-8"), "old")
            self.assertEqual((staging / "artifact.zip").read_text(encoding="utf-8"), "new")
            self.assertEqual(list(base.glob(".packages.backup-*")), [])


if __name__ == "__main__":
    unittest.main()
