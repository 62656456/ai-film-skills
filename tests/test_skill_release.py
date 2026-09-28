"""Run with TEMP/TMP (or SKILL_RELEASE_TEST_TEMP) explicitly on a task temp volume.

Uses real byte changes and rollback in isolated directories; never a live Skill.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "skill_release.py"
SPEC = importlib.util.spec_from_file_location("skill_release", SCRIPT)
release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release)


class SkillReleaseTests(unittest.TestCase):
    def setUp(self):
        explicit = os.environ.get("SKILL_RELEASE_TEST_TEMP") or os.environ.get("TEMP")
        if not explicit or not Path(explicit).is_absolute() or not Path(explicit).is_dir():
            raise RuntimeError("Set an existing absolute SKILL_RELEASE_TEST_TEMP or TEMP directory")
        self.workspace = tempfile.TemporaryDirectory(prefix="skill-release-test-", dir=explicit)
        self.base = Path(self.workspace.name)
        self.root = self.base / "target"
        self.candidate = self.base / "candidate"
        self.staging = self.base / "temporary"
        for path in (self.root, self.candidate, self.staging):
            path.mkdir()
        self.original = b"uncommitted working tree\r\n\xe4\xb8\xad\xe6\x96\x87\r\n"
        (self.root / "SKILL.md").write_bytes(self.original)
        (self.root / "other.md").write_bytes(b"preserve exactly\n")
        self.config = self.make_config(self.root, ["SKILL.md", "other.md"])
        self.baseline = self.base / "baseline"
        self.deployment = self.base / "deployment"

    def tearDown(self):
        self.workspace.cleanup()

    @staticmethod
    def make_config(root, paths):
        return {"roots": [{"id": "repo", "root": str(root), "paths": paths}]}

    def snapshot(self, config=None, output=None):
        folder = output or self.baseline
        release.snapshot(config or self.config, folder, self.staging)
        return folder / "manifest.json"

    def deploy(self, *, add=False, delete=False):
        manifest = self.snapshot()
        (self.candidate / "SKILL.md").write_bytes(b"candidate approved\n")
        paths = ["SKILL.md"]
        if add:
            paths.append("new/references.md")
            (self.candidate / "new").mkdir()
            (self.candidate / "new" / "references.md").write_bytes(b"new module\n")
        candidate_config = self.make_config(self.candidate, paths)
        if delete:
            candidate_config["delete"] = [{"root_id": "repo", "path": "other.md"}]
        release.apply_candidate(manifest, candidate_config, self.deployment, self.staging, apply=True)
        return manifest, self.deployment / "deployment.json"

    def test_snapshot_keeps_actual_uncommitted_bytes_and_hashes(self):
        manifest = self.snapshot()
        payload = release.verify(manifest)
        self.assertEqual(payload["files"][0]["sha256"], hashlib.sha256(self.original).hexdigest())
        with zipfile.ZipFile(self.baseline / "snapshot.zip") as archive:
            self.assertEqual(archive.read("files/repo/SKILL.md"), self.original)
        self.assertFalse(list(self.staging.iterdir()))

    def test_snapshot_missing_file_and_nested_output_are_supported(self):
        config = self.make_config(self.root, ["SKILL.md", "future.md"])
        output = self.root / "local-backup"
        payload = release.verify(self.snapshot(config, output))
        self.assertEqual(payload["files"][1], {"root_id": "repo", "path": "future.md", "exists": False})
        self.assertFalse((self.root / "future.md").exists())

    def test_nested_roots_with_disjoint_explicit_files(self):
        sub = self.root / "skills"
        sub.mkdir()
        (sub / "one.md").write_text("nested", encoding="utf-8")
        config = {"roots": [{"id": "top", "root": str(self.root), "paths": ["SKILL.md"]},
                            {"id": "child", "root": str(sub), "paths": ["one.md"]}]}
        self.assertEqual(len(release.verify(self.snapshot(config))["files"]), 2)

    def test_duplicate_physical_path_in_nested_roots_refused(self):
        config = {"roots": [{"id": "top", "root": str(self.root), "paths": ["SKILL.md"]},
                            {"id": "alias", "root": str(self.root), "paths": ["SKILL.md"]}]}
        with self.assertRaises(release.ReleaseError):
            self.snapshot(config)

    def test_archive_tampering_refused_before_restore(self):
        manifest, deployment = self.deploy()
        with (self.baseline / "snapshot.zip").open("ab") as stream:
            stream.write(b"tampered")
        with self.assertRaisesRegex(release.ReleaseError, "Archive SHA mismatch"):
            release.restore(manifest, deployment, self.base / "before", self.staging, apply=True)
        self.assertEqual((self.root / "SKILL.md").read_bytes(), b"candidate approved\n")
        self.assertFalse((self.base / "before").exists())

    def test_manifest_tampering_refused(self):
        manifest = self.snapshot()
        manifest.write_text(manifest.read_text(encoding="utf-8") + " ", encoding="utf-8")
        with self.assertRaisesRegex(release.ReleaseError, "Record SHA mismatch"):
            release.verify(manifest)

    def test_zip_slip_and_unexpected_members_refused_even_with_updated_archive_hash(self):
        manifest = self.snapshot()
        payload = release.checked_record(manifest)
        with zipfile.ZipFile(self.baseline / "snapshot.zip", "a") as archive:
            archive.writestr("../../outside.txt", b"escape")
        payload["archive_sha256"] = release.sha_file(self.baseline / "snapshot.zip")
        release.save_record(manifest, payload, self.staging)
        with self.assertRaises(release.ReleaseError):
            release.verify(manifest)
        self.assertFalse((self.base / "outside.txt").exists())

    def test_archived_symlink_refused_even_with_matching_hashes(self):
        manifest = self.snapshot()
        payload = release.checked_record(manifest)
        with zipfile.ZipFile(self.baseline / "snapshot.zip", "w") as archive:
            for item in payload["files"]:
                info = zipfile.ZipInfo(item["member"])
                info.create_system = 3
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
                archive.writestr(info, (self.root / item["path"]).read_bytes())
        payload["archive_sha256"] = release.sha_file(self.baseline / "snapshot.zip")
        release.save_record(manifest, payload, self.staging)
        with self.assertRaisesRegex(release.ReleaseError, "Nonregular"):
            release.verify(manifest)

    def test_apply_dry_run_changes_no_file_and_creates_no_output(self):
        manifest = self.snapshot()
        (self.candidate / "SKILL.md").write_text("candidate", encoding="utf-8")
        result = release.apply_candidate(manifest, self.make_config(self.candidate, ["SKILL.md"]),
                                         self.deployment, self.staging)
        self.assertEqual(result["status"], "dry_run")
        self.assertEqual((self.root / "SKILL.md").read_bytes(), self.original)
        self.assertFalse(self.deployment.exists())

    def test_real_apply_restore_hash_conservation_and_undo_restore(self):
        before_hashes = {p.name: release.sha_file(p) for p in self.root.iterdir()}
        manifest, deployment = self.deploy(add=True, delete=True)
        self.assertFalse((self.root / "other.md").exists())
        self.assertTrue((self.root / "new" / "references.md").is_file())
        (self.root / "unrelated.md").write_bytes(b"not deployment-owned")
        before_restore = self.base / "before-restore"
        result = release.restore(manifest, deployment, before_restore, self.staging, apply=True)
        self.assertEqual(result["status"], "applied")
        for path, digest in before_hashes.items():
            self.assertEqual(release.sha_file(self.root / path), digest)
        self.assertFalse((self.root / "new" / "references.md").exists())
        self.assertTrue((self.root / "new").is_dir())
        self.assertEqual((self.root / "unrelated.md").read_bytes(), b"not deployment-owned")
        release.verify(before_restore / "manifest.json")
        release.restore(before_restore / "manifest.json", before_restore / "deployment.json",
                        self.base / "undo-restore", self.staging, apply=True)
        self.assertEqual((self.root / "SKILL.md").read_bytes(), b"candidate approved\n")
        self.assertFalse((self.root / "other.md").exists())
        self.assertEqual((self.root / "new" / "references.md").read_bytes(), b"new module\n")
        self.assertFalse(list(self.staging.iterdir()))

    def test_restore_dry_run_is_default_and_creates_no_backup(self):
        manifest, deployment = self.deploy()
        output = self.base / "before-restore"
        result = release.restore(manifest, deployment, output, self.staging)
        self.assertEqual(result["status"], "dry_run")
        self.assertFalse(output.exists())
        self.assertEqual((self.root / "SKILL.md").read_bytes(), b"candidate approved\n")

    def test_restore_refuses_target_drift_and_preserves_external_edit(self):
        manifest, deployment = self.deploy(add=True)
        (self.root / "new" / "references.md").write_bytes(b"concurrent external edit")
        with self.assertRaisesRegex(release.ReleaseError, "Target drift"):
            release.restore(manifest, deployment, self.base / "before", self.staging, apply=True)
        self.assertEqual((self.root / "new" / "references.md").read_bytes(), b"concurrent external edit")
        self.assertFalse((self.base / "before").exists())

    def test_apply_refuses_baseline_drift(self):
        manifest = self.snapshot()
        (self.root / "SKILL.md").write_bytes(b"external change")
        (self.candidate / "SKILL.md").write_bytes(b"candidate")
        with self.assertRaisesRegex(release.ReleaseError, "Target drift"):
            release.apply_candidate(manifest, self.make_config(self.candidate, ["SKILL.md"]),
                                    self.deployment, self.staging, apply=True)
        self.assertEqual((self.root / "SKILL.md").read_bytes(), b"external change")

    def test_new_candidate_never_overwrites_unlisted_existing_file(self):
        manifest = self.snapshot()
        (self.root / "new.md").write_bytes(b"outside baseline")
        (self.candidate / "new.md").write_bytes(b"candidate")
        with self.assertRaisesRegex(release.ReleaseError, "already exists"):
            release.apply_candidate(manifest, self.make_config(self.candidate, ["new.md"]),
                                    self.deployment, self.staging, apply=True)
        self.assertEqual((self.root / "new.md").read_bytes(), b"outside baseline")

    def test_missing_candidate_is_not_a_delete_request(self):
        manifest = self.snapshot()
        with self.assertRaisesRegex(release.ReleaseError, "Candidate file is missing"):
            release.apply_candidate(manifest, self.make_config(self.candidate, ["SKILL.md"]),
                                    self.deployment, self.staging, apply=True)
        self.assertEqual((self.root / "SKILL.md").read_bytes(), self.original)

    def test_path_traversal_secrets_globs_and_git_are_refused(self):
        for name in ("../escape", "C:/escape", "C:escape", "/escape", ".git/config", ".env",
                     ".env.local", "private.pem", "dir/id_rsa", "auth.json", "*.md", "dir//x",
                     "file:stream", "NUL", "dir/../x", "dir/./x", "secret.txt", "secrets",
                     "api-key.json", "access_token.txt"):
            with self.subTest(name=name), self.assertRaises(release.ReleaseError):
                self.snapshot(self.make_config(self.root, [name]))

    def test_directories_and_output_overlap_are_refused(self):
        (self.root / "folder").mkdir()
        with self.assertRaises(release.ReleaseError):
            self.snapshot(self.make_config(self.root, ["folder"]))
        with self.assertRaises(release.ReleaseError):
            self.snapshot(output=self.root)

    def test_symlink_source_and_parent_are_refused(self):
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "secret.md").write_text("outside", encoding="utf-8")
        try:
            (self.root / "link").symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            self.skipTest("OS does not permit symlink creation: " + str(exc))
        with self.assertRaisesRegex(release.ReleaseError, "reparse"):
            self.snapshot(self.make_config(self.root, ["link/secret.md"]))

    def test_reparse_attribute_detection(self):
        info = mock.Mock(st_mode=stat.S_IFDIR, st_file_attributes=0x400)
        with mock.patch.object(Path, "lstat", return_value=info):
            self.assertTrue(release.is_link(self.root))

    def test_cross_volume_staging_refused_without_writing(self):
        with mock.patch.object(release, "same_volume", side_effect=release.ReleaseError("same volume")):
            with self.assertRaises(release.ReleaseError):
                self.snapshot()
        self.assertFalse(self.baseline.exists())

    def test_bad_deployment_checksum_refused(self):
        manifest, deployment = self.deploy()
        deployment.write_bytes(deployment.read_bytes() + b" ")
        with self.assertRaisesRegex(release.ReleaseError, "Record SHA mismatch"):
            release.restore(manifest, deployment, self.base / "before", self.staging, apply=True)

    def test_changed_candidate_during_staging_refused(self):
        manifest = self.snapshot()
        source = self.candidate / "SKILL.md"
        source.write_bytes(b"candidate")
        real_commit = release.commit_plan
        def change_then_commit(*args, **kwargs):
            source.write_bytes(b"changed after plan")
            return real_commit(*args, **kwargs)
        with mock.patch.object(release, "commit_plan", side_effect=change_then_commit):
            with self.assertRaisesRegex(release.ReleaseError, "changed while staging"):
                release.apply_candidate(manifest, self.make_config(self.candidate, ["SKILL.md"]),
                                        self.deployment, self.staging, apply=True)
        self.assertEqual((self.root / "SKILL.md").read_bytes(), self.original)
        self.assertFalse(list(self.staging.iterdir()))

    def test_partial_apply_failure_retains_an_exact_restorable_record(self):
        manifest = self.snapshot()
        (self.candidate / "SKILL.md").write_bytes(b"new skill")
        (self.candidate / "other.md").write_bytes(b"new other")
        real_replace = release.os.replace
        def fail_second_target(source, destination):
            if Path(destination) == self.root / "other.md":
                raise OSError("simulated target write failure")
            return real_replace(source, destination)
        with mock.patch.object(release.os, "replace", side_effect=fail_second_target):
            with self.assertRaisesRegex(OSError, "simulated"):
                release.apply_candidate(manifest, self.make_config(self.candidate, ["SKILL.md", "other.md"]),
                                        self.deployment, self.staging, apply=True)
        record = release.checked_record(self.deployment / "deployment.json")
        self.assertEqual(record["status"], "apply_failed")
        self.assertEqual((self.root / "SKILL.md").read_bytes(), b"new skill")
        self.assertEqual((self.root / "other.md").read_bytes(), b"preserve exactly\n")
        release.restore(manifest, self.deployment / "deployment.json", self.base / "before-restore",
                        self.staging, apply=True)
        self.assertEqual((self.root / "SKILL.md").read_bytes(), self.original)
        self.assertEqual((self.root / "other.md").read_bytes(), b"preserve exactly\n")
        self.assertFalse(list(self.staging.iterdir()))

    @unittest.skipUnless(os.name == "nt", "Windows junction test")
    def test_windows_junction_source_is_refused(self):
        outside = self.base / "junction-outside"
        outside.mkdir()
        (outside / "document.md").write_bytes(b"outside target")
        link = self.root / "junction"
        result = subprocess.run(["cmd.exe", "/d", "/c", "mklink", "/J", str(link), str(outside)],
                                capture_output=True, cwd=self.base, check=False)
        if result.returncode:
            self.skipTest("Windows junction creation unavailable")
        try:
            self.assertTrue(release.is_link(link))
            with self.assertRaisesRegex(release.ReleaseError, "reparse"):
                self.snapshot(self.make_config(self.root, ["junction/document.md"]))
            self.assertEqual((outside / "document.md").read_bytes(), b"outside target")
        finally:
            # Remove the known junction itself, never traverse or delete its target.
            self.assertEqual(link.parent, self.root)
            os.rmdir(link)

    def test_cli_snapshot_verify_and_restore_dry_run(self):
        config_path = self.base / "roots.json"
        config_path.write_text(json.dumps(self.config), encoding="utf-8")
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), "snapshot", "--config", str(config_path),
                                 "--output-dir", str(self.baseline), "--temp-dir", str(self.staging)],
                                capture_output=True, text=True, cwd=self.base, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), "verify", "--manifest",
                                 str(self.baseline / "manifest.json")],
                                capture_output=True, text=True, cwd=self.base, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "verified")
        (self.candidate / "SKILL.md").write_bytes(b"CLI candidate")
        candidate_config = self.base / "candidate-roots.json"
        candidate_config.write_text(json.dumps(self.make_config(self.candidate, ["SKILL.md"])), encoding="utf-8")
        apply_command = [sys.executable, "-B", str(SCRIPT), "apply", "--manifest",
                         str(self.baseline / "manifest.json"), "--candidate-config", str(candidate_config),
                         "--output-dir", str(self.deployment), "--temp-dir", str(self.staging)]
        result = subprocess.run(apply_command, capture_output=True, text=True, cwd=self.base, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "dry_run")
        self.assertEqual((self.root / "SKILL.md").read_bytes(), self.original)
        result = subprocess.run([*apply_command, "--apply"], capture_output=True, text=True, cwd=self.base, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        restore_command = [sys.executable, "-B", str(SCRIPT), "restore", "--manifest",
                           str(self.baseline / "manifest.json"), "--deployment", str(self.deployment / "deployment.json"),
                           "--output-dir", str(self.base / "cli-before"), "--temp-dir", str(self.staging)]
        result = subprocess.run(restore_command, capture_output=True, text=True, cwd=self.base, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "dry_run")
        self.assertEqual((self.root / "SKILL.md").read_bytes(), b"CLI candidate")
        result = subprocess.run([*restore_command, "--apply"], capture_output=True, text=True, cwd=self.base, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.root / "SKILL.md").read_bytes(), self.original)

    def test_state_snapshots_cannot_bypass_project_cas(self):
        (self.root / "PROJECT_STATE.json").write_bytes(b'{"revision":1}')
        manifest = self.snapshot(self.make_config(self.root, ["PROJECT_STATE.json"]))
        (self.candidate / "PROJECT_STATE.json").write_bytes(b'{"revision":2}')
        with self.assertRaisesRegex(release.ReleaseError, "state CAS"):
            release.apply_candidate(manifest, self.make_config(self.candidate, ["PROJECT_STATE.json"]),
                                    self.deployment, self.staging, apply=True)
        self.assertEqual((self.root / "PROJECT_STATE.json").read_bytes(), b'{"revision":1}')

    def test_runtime_subset_apply_survives_unrelated_state_cas_change(self):
        (self.root / "PROJECT_STATE.json").write_bytes(b'{"revision":1}')
        manifest = self.snapshot(self.make_config(self.root, ["SKILL.md", "PROJECT_STATE.json"]))
        (self.root / "PROJECT_STATE.json").write_bytes(b'{"revision":2}')
        (self.candidate / "SKILL.md").write_bytes(b"candidate after CAS")
        release.apply_candidate(manifest, self.make_config(self.candidate, ["SKILL.md"]),
                                self.deployment, self.staging, apply=True)
        self.assertEqual((self.root / "SKILL.md").read_bytes(), b"candidate after CAS")
        self.assertEqual((self.root / "PROJECT_STATE.json").read_bytes(), b'{"revision":2}')
        release.restore(manifest, self.deployment / "deployment.json", self.base / "before",
                        self.staging, apply=True)
        self.assertEqual((self.root / "SKILL.md").read_bytes(), self.original)
        self.assertEqual((self.root / "PROJECT_STATE.json").read_bytes(), b'{"revision":2}')

    def test_capture_dry_run_and_record_leave_managed_bytes_and_mtimes_unchanged(self):
        manifest = self.snapshot()
        (self.root / "SKILL.md").write_bytes(b"human edited candidate")
        observed = self.make_config(self.root, ["SKILL.md", "other.md"])
        before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in self.root.iterdir()}
        result = release.capture(manifest, observed, self.deployment, self.staging)
        self.assertEqual(result["status"], "dry_run")
        self.assertEqual(result["operation"], "observed_edits")
        self.assertEqual(result["unchanged_files"], 1)
        self.assertFalse(self.deployment.exists())
        result = release.capture(manifest, observed, self.deployment, self.staging, apply=True)
        self.assertEqual(result["status"], "captured")
        self.assertFalse(result["managed_files_modified"])
        for path, value in before.items():
            self.assertEqual((path.read_bytes(), path.stat().st_mtime_ns), value)
        record = release.checked_record(self.deployment / "deployment.json")
        self.assertEqual(record["status"], "captured")
        self.assertEqual(record["operation"], "observed_edits")
        self.assertEqual(len(record["files"]), 1)

    def test_capture_then_restore_real_changes_added_deleted_and_state_untouched(self):
        (self.root / "PROJECT_STATE.json").write_bytes(b'{"revision":1}')
        manifest = self.snapshot(self.make_config(self.root, ["SKILL.md", "other.md", "planned.md", "PROJECT_STATE.json"]))
        (self.root / "SKILL.md").write_bytes(b"edited in workspace")
        (self.root / "other.md").unlink()
        (self.root / "planned.md").write_bytes(b"planned addition")
        (self.root / "new.md").write_bytes(b"operator declared new")
        (self.root / "unrelated.md").write_bytes(b"not in capture scope")
        (self.root / "PROJECT_STATE.json").write_bytes(b'{"revision":2}')
        observed = self.make_config(self.root, ["SKILL.md", "other.md", "planned.md", "new.md"])
        observed["new_files"] = [{"root_id": "repo", "path": "new.md"}]
        release.capture(manifest, observed, self.deployment, self.staging, apply=True)
        record = release.checked_record(self.deployment / "deployment.json")
        self.assertEqual(record["files"][-1]["before_source"], "operator_declared_new_file")
        self.assertEqual(record["files"][2]["before_source"], "baseline")
        result = release.restore(manifest, self.deployment / "deployment.json", self.base / "before",
                                 self.staging, apply=True)
        self.assertEqual(result["status"], "applied")
        self.assertEqual((self.root / "SKILL.md").read_bytes(), self.original)
        self.assertEqual((self.root / "other.md").read_bytes(), b"preserve exactly\n")
        self.assertFalse((self.root / "planned.md").exists())
        self.assertFalse((self.root / "new.md").exists())
        self.assertEqual((self.root / "unrelated.md").read_bytes(), b"not in capture scope")
        self.assertEqual((self.root / "PROJECT_STATE.json").read_bytes(), b'{"revision":2}')

    def test_capture_requires_explicit_declaration_for_unlisted_new_file(self):
        manifest = self.snapshot()
        (self.root / "new.md").write_bytes(b"could predate baseline")
        with self.assertRaisesRegex(release.ReleaseError, "new_files declaration"):
            release.capture(manifest, self.make_config(self.root, ["new.md"]),
                            self.deployment, self.staging, apply=True)
        self.assertFalse(self.deployment.exists())

    def test_capture_rejects_other_roots_state_files_and_new_file_alias(self):
        manifest = self.snapshot({"roots": [
            {"id": "repo", "root": str(self.root), "paths": ["SKILL.md"]},
            {"id": "alias", "root": str(self.root), "paths": ["other.md"]}]})
        with self.assertRaisesRegex(release.ReleaseError, "match baseline"):
            release.capture(manifest, self.make_config(self.candidate, ["SKILL.md"]),
                            self.deployment, self.staging, apply=True)
        (self.root / "PROJECT_STATE.json").write_bytes(b'{"revision":2}')
        observed = self.make_config(self.root, ["PROJECT_STATE.json"])
        observed["new_files"] = [{"root_id": "repo", "path": "PROJECT_STATE.json"}]
        with self.assertRaisesRegex(release.ReleaseError, "state CAS"):
            release.capture(manifest, observed, self.deployment, self.staging, apply=True)
        observed = {"roots": [{"id": "alias", "root": str(self.root), "paths": ["SKILL.md"]}],
                    "new_files": [{"root_id": "alias", "path": "SKILL.md"}]}
        with self.assertRaisesRegex(release.ReleaseError, "root aliases"):
            release.capture(manifest, observed, self.deployment, self.staging, apply=True)

    def test_capture_no_change_creates_no_record(self):
        manifest = self.snapshot()
        result = release.capture(manifest, self.config, self.deployment, self.staging, apply=True)
        self.assertEqual(result["status"], "no_changes")
        self.assertFalse(self.deployment.exists())

    def test_capture_concurrent_change_during_recording_is_not_accepted(self):
        manifest = self.snapshot()
        (self.root / "SKILL.md").write_bytes(b"edited before capture")
        real_save = release.save_record
        calls = []
        def change_after_record(path, payload, temporary):
            real_save(path, payload, temporary)
            if not calls:
                calls.append(True)
                (self.root / "SKILL.md").write_bytes(b"concurrent edit during capture")
        with mock.patch.object(release, "save_record", side_effect=change_after_record):
            with self.assertRaisesRegex(release.ReleaseError, "Target drift"):
                release.capture(manifest, self.make_config(self.root, ["SKILL.md"]),
                                self.deployment, self.staging, apply=True)
        self.assertEqual(release.checked_record(self.deployment / "deployment.json")["status"], "capture_failed")
        with self.assertRaises(release.ReleaseError):
            release.restore(manifest, self.deployment / "deployment.json", self.base / "before", self.staging, apply=True)

    def test_captured_record_scope_and_new_file_declaration_must_remain_bound(self):
        manifest = self.snapshot()
        (self.root / "new.md").write_bytes(b"new file")
        observed = self.make_config(self.root, ["new.md"])
        observed["new_files"] = [{"root_id": "repo", "path": "new.md"}]
        release.capture(manifest, observed, self.deployment, self.staging, apply=True)
        record = release.checked_record(self.deployment / "deployment.json")
        record["operator_declared_new_files"] = []
        release.save_record(self.deployment / "deployment.json", record, self.staging)
        with self.assertRaisesRegex(release.ReleaseError, "declared scope"):
            release.restore(manifest, self.deployment / "deployment.json", self.base / "before", self.staging, apply=True)
        self.assertEqual((self.root / "new.md").read_bytes(), b"new file")

    def test_cli_capture_default_dry_run_then_record_only(self):
        manifest = self.snapshot()
        (self.root / "SKILL.md").write_bytes(b"edit before CLI capture")
        observed_config = self.base / "observed.json"
        observed_config.write_text(json.dumps(self.make_config(self.root, ["SKILL.md"])), encoding="utf-8")
        command = [sys.executable, "-B", str(SCRIPT), "capture", "--manifest", str(manifest),
                   "--config", str(observed_config), "--output-dir", str(self.deployment),
                   "--temp-dir", str(self.staging)]
        result = subprocess.run(command, capture_output=True, text=True, cwd=self.base, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "dry_run")
        self.assertFalse(self.deployment.exists())
        result = subprocess.run([*command, "--apply"], capture_output=True, text=True, cwd=self.base, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "captured")
        self.assertEqual((self.root / "SKILL.md").read_bytes(), b"edit before CLI capture")


if __name__ == "__main__":
    unittest.main()
