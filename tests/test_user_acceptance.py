"""Read-only activation gate tests; an explicit task TEMP directory is required."""
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
import zipfile


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify_user_acceptance.py"
SPEC = importlib.util.spec_from_file_location("verify_user_acceptance", SCRIPT)
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


class UserAcceptanceTests(unittest.TestCase):
    def setUp(self):
        parent = os.environ.get("SKILL_RELEASE_TEST_TEMP") or os.environ.get("TEMP")
        if not parent or not Path(parent).is_absolute() or not Path(parent).is_dir():
            raise RuntimeError("Set an existing absolute task TEMP or SKILL_RELEASE_TEST_TEMP")
        self.workspace = tempfile.TemporaryDirectory(prefix="user-acceptance-test-", dir=parent)
        self.root = Path(self.workspace.name)
        self.state_path = self.root / "PROJECT_STATE.json"
        self.artifact = self.root / "candidate-A.zip"
        with zipfile.ZipFile(self.artifact, "w") as archive:
            archive.writestr("SKILL.md", "candidate A")
        self.artifact_sha = hashlib.sha256(self.artifact.read_bytes()).hexdigest()
        self.record = {"status": "user_test_passed", "evidence_author": "user",
                       "user_quote": "我实际测试了A版，A版测试通过，可以设为正式默认。",
                       "source": {"conversation": "fixture-private-source", "turn": "fixture-turn"},
                       "reviewed_artifact_sha256": self.artifact_sha, "scope": ["formal_activation"]}
        self.payload = {"canonical_project_id": "fixture", "project_root": str(self.root), "revision": 1,
                        "acceptance": {gate.ACCEPTANCE_KEY: {"profiles": {"A": self.record}}}}
        self.write_state()

    def tearDown(self):
        self.workspace.cleanup()

    def write_state(self):
        self.state_path.write_text(json.dumps(self.payload, ensure_ascii=False), encoding="utf-8")

    def decision(self, profile="A", artifact=None):
        self.write_state()
        return gate.verify_user_acceptance(self.state_path, profile, artifact or self.artifact,
                                           expected_project_id="fixture")

    def test_explicit_user_pass_correct_hash_is_enough_without_three_trials(self):
        result = self.decision()
        self.assertTrue(result["ready"], result)
        self.assertTrue(result["formal_activation_authorized"])
        self.assertFalse(result["external_publication_authorized"])
        self.assertEqual(result["missing_or_invalid"], [])

    def test_no_acceptance_is_refused(self):
        self.payload["acceptance"] = {}
        self.assertFalse(self.decision()["ready"])

    def test_internal_pass_and_assistant_evidence_are_refused(self):
        self.record.update(status="internal_pass", evidence_author="assistant")
        result = self.decision()
        self.assertIn("USER_TEST_PASS_STATUS_REQUIRED", result["missing_or_invalid"])
        self.assertIn("USER_AUTHORED_EVIDENCE_REQUIRED", result["missing_or_invalid"])

    def test_selection_start_and_temporary_use_do_not_mean_pass(self):
        for quote in ("选择A", "开始", "先用A", "先启用A吧", "同意开始A版本测试", "A看起来不错"):
            with self.subTest(quote=quote):
                self.record["user_quote"] = quote
                self.assertFalse(self.decision()["ready"])

    def test_negative_conditional_or_internal_pass_is_refused(self):
        quotes = ["A测试未通过", "A没通过", "不是说A通过了", "A不能算通过", "A测试通过不了",
                  "如果A测试通过，再设为默认", "A通过后再上线", "A应该能通过", "A通过了吗？",
                  "A内部测试通过", "A单元测试通过", "A自动化检查通过", "A测试通过，但不能算验收通过",
                  "我还没实际测试，但A通过", "A has not passed", "If A passed, activate it"]
        for quote in quotes:
            with self.subTest(quote=quote):
                self.record["user_quote"] = quote
                self.assertFalse(self.decision()["ready"])

    def test_admission_rules_are_not_a_real_pass_even_if_status_was_mistakenly_filled(self):
        for quote in ("必须通过我的测试，过了再升正式，没过不能上线", "A版必须测试通过才能升为正式版",
                      "等我测试通过再上线", "如果A测试通过，就升为正式", "只有A测试通过才能正式启用",
                      "A需要测试通过", "A测试通过才升正式", "只要A测试通过就升正式", "A测试通过的话就转正式",
                      "我测试过了，不是没问题，转正式", "等我测试过了，没问题再转正式"):
            with self.subTest(quote=quote):
                self.record["user_quote"] = quote
                self.assertFalse(self.decision()["ready"])

    def test_explicit_real_trial_and_colloquial_formal_acceptance_are_supported(self):
        for quote in ("A版这次实际测试通过，可以升为正式版", "这版我测试过了，没问题，转正式"):
            with self.subTest(quote=quote):
                self.record["user_quote"] = quote
                self.assertTrue(self.decision()["ready"])

    def test_ambiguous_wording_requires_review_and_never_activates(self):
        self.record["user_quote"] = "A这一版还可以吧"
        result = self.decision()
        self.assertFalse(result["ready"])
        self.assertEqual(result["status"], "needs_review")
        self.assertFalse(result["formal_activation_authorized"])

    def test_b_cannot_borrow_a_acceptance(self):
        self.assertFalse(self.decision("B")["ready"])
        self.payload["acceptance"][gate.ACCEPTANCE_KEY]["profiles"]["B"] = dict(self.record)
        self.assertFalse(self.decision("B")["ready"])

    def test_b_cannot_borrow_a_zip_even_with_b_wording(self):
        artifact_b = self.root / "candidate-B.zip"
        with zipfile.ZipFile(artifact_b, "w") as archive:
            archive.writestr("SKILL.md", "candidate B")
        self.payload["acceptance"][gate.ACCEPTANCE_KEY]["profiles"]["B"] = {
            **self.record, "user_quote": "B版实测通过"}
        result = self.decision("B", artifact_b)
        self.assertIn("REVIEWED_ARTIFACT_SHA256_MISMATCH", result["missing_or_invalid"])

    def test_changed_artifact_is_not_the_approved_version(self):
        with zipfile.ZipFile(self.artifact, "a") as archive:
            archive.writestr("changed.md", "changed after user review")
        result = self.decision()
        self.assertIn("REVIEWED_ARTIFACT_SHA256_MISMATCH", result["missing_or_invalid"])

    def test_missing_source_quote_or_scope_is_refused(self):
        for field, value in (("source", ""), ("source", {}), ("source", {"turn": " "}),
                             ("user_quote", ""), ("scope", []), ("scope", ["formal_activation_pending"]),
                             ("reviewed_artifact_sha256", "")):
            with self.subTest(field=field, value=value):
                old = self.record[field]
                self.record[field] = value
                self.assertFalse(self.decision()["ready"])
                self.record[field] = old

    def test_one_direct_pass_in_context_and_english_pass_are_supported(self):
        for quote in ("通过", "确认通过", "这个版本验收通过", "A passed my test", "I tested A and approved it"):
            with self.subTest(quote=quote):
                self.record["user_quote"] = quote
                self.assertTrue(self.decision()["ready"])

    def test_other_profile_negative_does_not_reverse_this_profile_pass(self):
        self.record["user_quote"] = "A测试通过，B没有通过"
        self.assertTrue(self.decision()["ready"])

    def test_canonical_identity_project_and_filename_must_match(self):
        self.payload["project_root"] = str(self.root / "wrong")
        self.assertFalse(self.decision()["ready"])
        self.payload["project_root"] = str(self.root)
        self.payload["canonical_project_id"] = "different-project"
        self.assertIn("PROJECT_ID_MISMATCH", self.decision()["missing_or_invalid"])
        alias = self.root / "state-copy.json"
        alias.write_bytes(self.state_path.read_bytes())
        self.assertFalse(gate.verify_user_acceptance(alias, "A", self.artifact)["ready"])

    def test_invalid_json_non_zip_and_unknown_profile_are_refused(self):
        self.state_path.write_text("broken", encoding="utf-8")
        self.assertFalse(gate.verify_user_acceptance(self.state_path, "A", self.artifact)["ready"])
        self.write_state()
        bad = self.root / "not-really.zip"
        bad.write_bytes(b"not a zip")
        self.assertFalse(gate.verify_user_acceptance(self.state_path, "A", bad)["ready"])
        self.assertFalse(gate.verify_user_acceptance(self.state_path, "C", self.artifact)["ready"])

    def test_readonly_and_output_does_not_repeat_private_evidence(self):
        before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in (self.state_path, self.artifact)}
        result = gate.verify_user_acceptance(self.state_path, "A", self.artifact)
        self.assertTrue(result["ready"])
        rendered = json.dumps(result, ensure_ascii=False)
        self.assertNotIn(self.record["user_quote"], rendered)
        self.assertNotIn("fixture-private-source", rendered)
        self.assertNotIn(str(self.root), rendered)
        for path, original in before.items():
            self.assertEqual((path.read_bytes(), path.stat().st_mtime_ns), original)

    def test_concurrent_state_decision_change_is_refused(self):
        real_check = gate._quote_confirms_pass
        def change_state(quote, profile):
            self.state_path.write_text(self.state_path.read_text(encoding="utf-8") + " ", encoding="utf-8")
            return real_check(quote, profile)
        with mock.patch.object(gate, "_quote_confirms_pass", side_effect=change_state):
            result = gate.verify_user_acceptance(self.state_path, "A", self.artifact)
        self.assertIn("STATE_CHANGED_DURING_CHECK", result["missing_or_invalid"])

    def test_cli_failure_nonzero_and_pass_zero_without_private_quote(self):
        command = [sys.executable, "-B", str(SCRIPT), "--state", str(self.state_path), "--profile", "A",
                   "--artifact", str(self.artifact), "--project-id", "fixture"]
        ok = subprocess.run(command, cwd=self.root, capture_output=True, text=True, check=False)
        self.assertEqual(ok.returncode, 0, ok.stderr)
        self.assertNotIn("fixture-private-source", ok.stdout)
        self.record["user_quote"] = "先启用A"
        self.write_state()
        refused = subprocess.run(command, cwd=self.root, capture_output=True, text=True, check=False)
        self.assertNotEqual(refused.returncode, 0)
        self.assertFalse(json.loads(refused.stdout)["ready"])


if __name__ == "__main__":
    unittest.main()
