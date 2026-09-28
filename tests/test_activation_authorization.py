"""Explicit activation authorization tests use ordinary files, never ZIPs."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify_activation_authorization.py"
SPEC = importlib.util.spec_from_file_location("verify_activation_authorization", SCRIPT)
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


class ActivationAuthorizationTests(unittest.TestCase):
    def setUp(self):
        parent = os.environ.get("SKILL_RELEASE_TEST_TEMP") or os.environ.get("TEMP")
        if not parent or not Path(parent).is_absolute() or not Path(parent).is_dir():
            raise RuntimeError("Set an existing absolute task TEMP or SKILL_RELEASE_TEST_TEMP")
        self.workspace = tempfile.TemporaryDirectory(prefix="activation-authorization-test-", dir=parent)
        self.root = Path(self.workspace.name)
        self.state = self.root / "PROJECT_STATE.json"
        self.artifact = self.root / "candidate-A.txt"
        self.artifact.write_bytes(b"the exact frozen candidate bytes")
        self.sha = hashlib.sha256(self.artifact.read_bytes()).hexdigest()
        self.record = {
            "status": "approved_by_user_instruction", "evidence_author": "user",
            "user_quote": "可以上传到git仓库里面然后现在就启用最新版本",
            "source": {"conversation": "private-fixture-chat", "turn": "activation-turn"},
            "selection_source": {"user_quote": "先启用A，B保留",
                                 "source": {"conversation": "private-fixture-chat", "turn": "selection-turn"}},
            "profile": "A", "version": "5.7.1", "artifact_sha256": self.sha,
            "scope": ["local_activation"]}
        self.profile = {"version": "5.7.1", "artifact_sha256": self.sha,
                        "status": "pending_user_test", "user_test_status": "known_issues"}
        self.group = {gate.AUTHORIZATION_KEY: self.record, "profiles": {"A": self.profile},
                      "user_aesthetic_acceptance": "not_claimed", "real_video_validation": "not_performed"}
        self.payload = {"canonical_project_id": "fixture", "project_root": str(self.root), "revision": 1,
                        "acceptance": {gate.ACCEPTANCE_KEY: self.group}}
        self.write_state()

    def tearDown(self):
        self.workspace.cleanup()

    def write_state(self):
        self.state.write_text(json.dumps(self.payload, ensure_ascii=False), encoding="utf-8")

    def decision(self, profile="A", version="5.7.1", artifact=None):
        self.write_state()
        return gate.verify_activation_authorization(self.state, profile, version, artifact or self.artifact,
                                                    expected_project_id="fixture")

    def test_exact_current_user_instruction_authorizes_local_activation_only(self):
        result = self.decision()
        self.assertTrue(result["ready"], result)
        self.assertEqual(result["authorization_basis"], "explicit_user_instruction")
        self.assertTrue(result["local_activation_authorized"])
        self.assertFalse(result["external_publication_authorized"])
        self.assertEqual(result["user_test_status"], "known_issues")
        self.assertEqual(result["missing_or_invalid"], [])

    def test_pending_test_status_does_not_block_instruction_or_become_passed(self):
        for status in ("pending", "known_issues", "pending_user_test"):
            with self.subTest(status=status):
                self.profile["user_test_status"] = status
                result = self.decision()
                self.assertTrue(result["ready"], result)
                self.assertEqual(result["user_test_status"], status)
                saved = json.loads(self.state.read_text(encoding="utf-8"))
                self.assertEqual(saved, self.payload)
                self.assertEqual(self.profile["status"], "pending_user_test")

    def test_explicit_version_instruction_and_other_profile_retention_are_supported(self):
        for quote in ("现在就启用A 5.7.1，B保留", "请启用A版5.7.1", "直接启用最新版本",
                      "A还没通过测试，但现在就启用A", "现在启用A，B不要启用"):
            with self.subTest(quote=quote):
                self.record["user_quote"] = quote
                self.assertTrue(self.decision()["ready"])

    def test_trial_discussion_selection_and_future_conditions_are_not_activation(self):
        quotes = ["选择A", "A作为候选保留", "先试用A", "现在启用A试用一下",
                  "只是讨论现在就启用A", "考虑现在就启用A", "是否现在就启用A？",
                  "模型建议现在就启用A", "如果测试通过，现在就启用A", "等A测试通过，再启用",
                  "A通过后启用", "只有A通过才启用", "A测试完再启用", "明天启用A",
                  "稍后启用A", "可以等会儿启用A", "现在先测试A，确认没问题后，现在就启用A",
                  "只是举例：现在就启用A", "现在就启用A这句话不代表授权",
                  "可以上传到git仓库里面", "A结构检查通过"]
        for quote in quotes:
            with self.subTest(quote=quote):
                self.record["user_quote"] = quote
                result = self.decision()
                self.assertFalse(result["ready"])
                self.assertIn("PRESENT_USER_ACTIVATION_INSTRUCTION_REQUIRED", result["missing_or_invalid"])

    def test_denial_or_withdrawal_cannot_be_bypassed_by_positive_prefix(self):
        for quote in ("现在不要启用A", "不能现在就启用A", "我未授权现在就启用A",
                      "现在就启用A，但不要启用", "现在启用A，撤回启用授权", "现在就启用A吗？",
                      "Do not activate A now", "If approved, activate A now"):
            with self.subTest(quote=quote):
                self.record["user_quote"] = quote
                self.assertFalse(self.decision()["ready"])

    def test_assistant_or_model_cannot_supply_user_authorization(self):
        for author in ("assistant", "model", "system", None):
            with self.subTest(author=author):
                self.record["evidence_author"] = author
                self.assertIn("USER_AUTHORED_EVIDENCE_REQUIRED", self.decision()["missing_or_invalid"])
        self.record["evidence_author"] = "user"
        for quote in ("助手说可以现在就启用A", "AI已经批准现在启用A", "作为模型，我批准现在就启用A"):
            with self.subTest(quote=quote):
                self.record["user_quote"] = quote
                self.assertFalse(self.decision()["ready"])

    def test_status_and_exact_scope_are_required(self):
        for status in ("user_test_passed", "internal_pass", "pending", "approved", None):
            with self.subTest(status=status):
                self.record["status"] = status
                self.assertIn("EXPLICIT_USER_INSTRUCTION_STATUS_REQUIRED", self.decision()["missing_or_invalid"])
        self.record["status"] = "approved_by_user_instruction"
        for scope in ([], ["git_publication"], ["local_activation_pending"], None):
            with self.subTest(scope=scope):
                self.record["scope"] = scope
                self.assertIn("LOCAL_ACTIVATION_SCOPE_REQUIRED", self.decision()["missing_or_invalid"])
        self.record["scope"] = ["local_activation", "git_publication"]
        self.assertTrue(self.decision()["ready"])
        self.assertFalse(self.decision()["external_publication_authorized"])

    def test_instruction_source_and_original_quote_are_required(self):
        for field, value in (("source", None), ("source", {}), ("source", {"turn": " "}),
                             ("source", True), ("user_quote", ""), ("user_quote", None)):
            with self.subTest(field=field, value=value):
                original = self.record[field]
                self.record[field] = value
                self.assertFalse(self.decision()["ready"])
                self.record[field] = original

    def test_selection_needs_user_quote_source_and_matching_profile(self):
        original = self.record["selection_source"]
        for selection in (None, "先启用A", {}, {"user_quote": "先启用A", "source": {}},
                          {"user_quote": "选择B，A保留", "source": "prior-turn"},
                          {"user_quote": "如果通过就选A", "source": "prior-turn"},
                          {"user_quote": "不要选择A", "source": "prior-turn"},
                          {"user_quote": "别用A", "source": "prior-turn"},
                          {"user_quote": "先试用A", "source": "prior-turn"},
                          {"user_quote": "先启用A", "source": "prior-turn", "evidence_author": "assistant"},
                          {"user_quote": "助手建议先启用A", "source": "prior-turn"}):
            with self.subTest(selection=selection):
                self.record["selection_source"] = selection
                self.assertIn("EXPLICIT_PROFILE_SELECTION_SOURCE_REQUIRED", self.decision()["missing_or_invalid"])
        self.record["selection_source"] = original
        self.assertTrue(self.decision()["ready"])

    def test_profile_and_version_must_match_request_record_quote_and_canonical_profile(self):
        self.assertFalse(self.decision(profile="B")["ready"])
        self.assertFalse(self.decision(version="5.7.0")["ready"])
        self.record["profile"] = "B"
        self.assertIn("AUTHORIZED_PROFILE_MISMATCH", self.decision()["missing_or_invalid"])
        self.record["profile"] = "A"
        self.record["version"] = "5.7.0"
        self.assertIn("AUTHORIZED_VERSION_MISMATCH", self.decision()["missing_or_invalid"])
        self.record["version"] = "5.7.1"
        for quote in ("现在启用B", "现在启用B，然后现在就启用最新版本",
                      "现在启用A 5.6.5", "现在启用A5.6.5", "现在启用A和B"):
            with self.subTest(quote=quote):
                self.record["user_quote"] = quote
                self.assertFalse(self.decision()["ready"])
        self.record["user_quote"] = "现在就启用最新版本"
        self.profile["version"] = "5.7.0"
        self.assertIn("PROFILE_STATE_VERSION_MISMATCH", self.decision()["missing_or_invalid"])

    def test_hash_binds_both_authorization_and_canonical_profile_to_ordinary_bytes(self):
        self.record["artifact_sha256"] = "0" * 64
        self.assertIn("AUTHORIZED_ARTIFACT_SHA256_MISMATCH", self.decision()["missing_or_invalid"])
        self.record["artifact_sha256"] = self.sha
        self.profile["artifact_sha256"] = "1" * 64
        self.assertIn("PROFILE_STATE_ARTIFACT_SHA256_MISMATCH", self.decision()["missing_or_invalid"])
        self.profile["artifact_sha256"] = self.sha
        self.artifact.write_bytes(b"different bytes after authorization")
        self.assertIn("AUTHORIZED_ARTIFACT_SHA256_MISMATCH", self.decision()["missing_or_invalid"])

    def test_missing_records_invalid_hash_and_invalid_state_are_refused(self):
        self.group.pop(gate.AUTHORIZATION_KEY)
        self.assertIn("EXPLICIT_ACTIVATION_AUTHORIZATION_MISSING", self.decision()["missing_or_invalid"])
        self.group[gate.AUTHORIZATION_KEY] = self.record
        self.group["profiles"] = {}
        self.assertIn("CANONICAL_PROFILE_RECORD_REQUIRED", self.decision()["missing_or_invalid"])
        self.group["profiles"] = {"A": self.profile}
        self.record["artifact_sha256"] = "not-a-hash"
        self.assertIn("AUTHORIZED_ARTIFACT_SHA256_REQUIRED", self.decision()["missing_or_invalid"])
        self.state.write_text("broken", encoding="utf-8")
        self.assertFalse(gate.verify_activation_authorization(self.state, "A", "5.7.1", self.artifact)["ready"])

    def test_canonical_identity_revision_filename_and_requested_project_are_checked(self):
        self.payload["project_root"] = str(self.root / "elsewhere")
        self.assertIn("CANONICAL_STATE_IDENTITY_INVALID", self.decision()["missing_or_invalid"])
        self.payload["project_root"] = str(self.root)
        self.payload["canonical_project_id"] = "another-project"
        self.assertIn("PROJECT_ID_MISMATCH", self.decision()["missing_or_invalid"])
        self.payload["canonical_project_id"] = "fixture"
        for revision in (0, True, "1"):
            self.payload["revision"] = revision
            self.assertIn("STATE_REVISION_INVALID", self.decision()["missing_or_invalid"])
        self.payload["revision"] = 1
        self.write_state()
        copy = self.root / "state-copy.json"
        copy.write_bytes(self.state.read_bytes())
        self.assertFalse(gate.verify_activation_authorization(copy, "A", "5.7.1", self.artifact)["ready"])
        self.assertFalse(self.decision(profile="C")["ready"])

    def test_read_only_and_private_evidence_is_not_echoed(self):
        before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in (self.state, self.artifact)}
        result = gate.verify_activation_authorization(self.state, "A", "5.7.1", self.artifact)
        self.assertTrue(result["ready"], result)
        rendered = json.dumps(result, ensure_ascii=False)
        self.assertNotIn(self.record["user_quote"], rendered)
        self.assertNotIn("private-fixture-chat", rendered)
        self.assertNotIn(str(self.root), rendered)
        for path, expected in before.items():
            self.assertEqual((path.read_bytes(), path.stat().st_mtime_ns), expected)
        self.assertEqual(list(self.root.glob("*.zip")), [])

    def test_concurrent_state_and_artifact_changes_are_refused(self):
        original = gate._quote_authorizes_activation
        for changed in (self.state, self.artifact):
            with self.subTest(changed=changed.name):
                self.artifact.write_bytes(b"the exact frozen candidate bytes")
                self.write_state()
                def mutate(quote, profile, version):
                    changed.write_bytes(changed.read_bytes() + b" ")
                    return original(quote, profile, version)
                with mock.patch.object(gate, "_quote_authorizes_activation", side_effect=mutate):
                    result = gate.verify_activation_authorization(self.state, "A", "5.7.1", self.artifact)
                expected = "STATE_CHANGED_DURING_CHECK" if changed == self.state else "ARTIFACT_CHANGED_DURING_CHECK"
                self.assertIn(expected, result["missing_or_invalid"])

    def test_revocation_during_final_artifact_read_is_refused(self):
        original = gate._hash_stable_file
        calls = 0
        def hash_then_revoke(path):
            nonlocal calls
            result = original(path)
            calls += 1
            if calls == 2:
                self.state.write_bytes(self.state.read_bytes() + b" ")
            return result
        with mock.patch.object(gate, "_hash_stable_file", side_effect=hash_then_revoke):
            result = gate.verify_activation_authorization(self.state, "A", "5.7.1", self.artifact)
        self.assertIn("STATE_CHANGED_DURING_CHECK", result["missing_or_invalid"])

    def test_cli_exit_status_and_no_publication_or_private_quote(self):
        command = [sys.executable, "-B", str(SCRIPT), "--state", str(self.state), "--profile", "A",
                   "--version", "5.7.1", "--artifact", str(self.artifact), "--project-id", "fixture"]
        ok = subprocess.run(command, cwd=self.root, capture_output=True, text=True, encoding="utf-8", check=False)
        self.assertEqual(ok.returncode, 0, ok.stderr)
        self.assertTrue(json.loads(ok.stdout)["ready"])
        self.assertFalse(json.loads(ok.stdout)["external_publication_authorized"])
        self.assertNotIn("private-fixture-chat", ok.stdout)
        self.record["user_quote"] = "如果测试通过再启用A"
        self.write_state()
        refused = subprocess.run(command, cwd=self.root, capture_output=True, text=True, encoding="utf-8", check=False)
        self.assertEqual(refused.returncode, 1, refused.stderr)
        self.assertFalse(json.loads(refused.stdout)["ready"])


if __name__ == "__main__":
    unittest.main()
