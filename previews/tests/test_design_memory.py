#!/usr/bin/env python3
"""Behavioral subprocess tests for 5.6.0 design memory; no third-party packages."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ai-storyboard-director-preview" / "scripts" / "design_memory.py"
TEMP_ROOT = Path(os.environ.get("PREVIEW_TEST_TMP", tempfile.gettempdir())) / "storyboard-preview-tests"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def scene_sha(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                          allow_nan=False).encode("utf-8"))


def shot(shot_id, start, end, holder="father"):
    return {"shot_id": shot_id, "start": start, "end": end,
            "viewing_task": "Keep the invitation and the empty seat readable.",
            "framing": "Father, daughter and empty chair remain visible together.",
            "camera": {"path": [[1, 3], [1.1, 3.1]], "orientation": "Toward the empty chair"},
            "motion": {"description": "A small move follows the daughter's hesitation."},
            "ending": "She remains standing, still beside the empty chair.",
            "enter_state": {"prop_holder": holder}, "exit_state": {"prop_holder": holder}}


def scene():
    return {"scene_id": "S1", "source_lines": [1, 2],
            "dramatic_change": "An invitation is declined without leaving.",
            "director_intent": "Hold the refusal and continued presence together.",
            "enter_state": {"prop_holder": "father"}, "exit_state": {"prop_holder": "father"},
            "previous_scene": None, "duration_seconds": 6,
            "design_questions": ["How can the unoccupied seat remain readable?"],
            "knowledge_topics": ["framing", "continuity", "motion"],
            "axis": {"status": "defined", "start": [0, 0], "end": [2, 0], "allowed_side": "positive"},
            "shots": [shot("S1-01", 0, 3), shot("S1-02", 3, 6)]}


class DesignMemoryTests(unittest.TestCase):
    def setUp(self):
        TEMP_ROOT.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="case-", dir=TEMP_ROOT)
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "work"
        self.root.mkdir()
        self.source = self.root / "script.md"
        self.source.write_text("Father offers the empty chair.\nDaughter stays standing.\n", encoding="utf-8")
        self.state_path = self.root / ".director_design" / "state.json"
        self.initial = self.cli("init", "--project-id", "test:empty-chair", "--source", "script.md")
        self.current = self.initial
        self.design = copy.deepcopy(self.initial["state"])
        self.design["film_intent"] = {"intent": "Observe the relationship without resolving it.",
                                      "rationale": "The empty chair makes the refusal visible."}
        self.design["locked_facts"] = [{"id": "L1", "statement": "The daughter does not sit."}]
        self.design["candidate_decisions"] = [{"id": "C1", "decision": "Keep the chair visible.",
                                               "rationale": "It connects the invitation to refusal."}]
        self.design["scenes"] = [scene()]

    def cli(self, command, *args, error=None):
        completed = subprocess.run([sys.executable, "-B", str(SCRIPT), command,
                                    "--project-root", str(self.root), *map(str, args)],
                                   capture_output=True, text=True, encoding="utf-8",
                                   env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                                   timeout=20)
        self.assertTrue(completed.stdout.strip(), completed.stderr)
        try:
            value = json.loads(completed.stdout)
        except json.JSONDecodeError:
            self.fail(f"Non-JSON output: {completed.stdout}\n{completed.stderr}")
        if error is None:
            self.assertEqual(completed.returncode, 0, value)
            self.assertTrue(value["ok"], value)
        else:
            self.assertNotEqual(completed.returncode, 0, value)
            self.assertFalse(value["ok"])
            self.assertEqual(value["error"], error, value)
        return value

    def token(self, version=None):
        version = version or self.current
        return ["--expected-revision", str(version["revision"]), "--expected-sha256", version["state_sha256"]]

    def proposal(self, value):
        path = self.root / "proposal.json"
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        return path

    def commit(self, value=None, *, error=None, extra=(), version=None):
        value = copy.deepcopy(value if value is not None else self.design)
        value["revision"] = (version or self.current)["revision"]
        path = self.proposal(value)
        before = self.state_path.read_bytes()
        response = self.cli("commit", "--input", path.name, *self.token(version), *extra, error=error)
        if error is not None:
            self.assertEqual(self.state_path.read_bytes(), before, "Failed operation changed state bytes")
        else:
            self.current = response
        return response

    def saved(self):
        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def delivery(self, *, error=None, version=None, output="delivery.json", extra=()):
        (self.root / "delivery.md").write_text("同框保留父亲、女儿和空椅。女儿没有坐下，也没有离开。\n", encoding="utf-8")
        before = self.state_path.read_bytes()
        response = self.cli("export", "--scene", "S1", "--text", "delivery.md",
                            "--output", output, *self.token(version), *extra, error=error)
        self.assertEqual(self.state_path.read_bytes(), before)
        return response

    def test_fresh_process_restores_exact_decisions_and_core_knowledge(self):
        self.commit()
        # Every cli call is a fresh process with no conversational state.
        first = self.cli("context", "--scene", "S1")
        second = self.cli("context", "--scene", "S1")
        self.assertEqual(first, second)
        self.assertEqual(first["film_intent"], self.design["film_intent"])
        self.assertEqual(first["locked_facts"], self.design["locked_facts"])
        self.assertEqual(first["scene"], self.design["scenes"][0])
        self.assertEqual(first["source_excerpt"][0]["text"], "Father offers the empty chair.")
        for item in first["knowledge"]:
            path = Path(item["path"])
            self.assertTrue(path.is_relative_to(SCRIPT.parent.parent / "references"))
            self.assertEqual(item["sha256"], sha(path.read_bytes()))
        self.assertFalse(first["text_semantics_verified"])

    def test_new_scene_can_read_knowledge_before_any_scene_is_saved(self):
        result = self.cli("context", "--topics", "motion", "optics")
        self.assertEqual(result["state"]["scenes"], [])
        names = {Path(item["path"]).name for item in result["knowledge"]}
        self.assertIn("framing-and-axis.md", names)
        self.assertIn("shot-design-engine.md", names)
        self.assertIn("production-contract.md", names)

    def test_ordinary_commit_cannot_drop_or_rewrite_a_lock(self):
        self.commit()
        for locks in ([], [{"id": "L1", "statement": "She now sits."}]):
            with self.subTest(locks=locks):
                changed = self.saved()
                changed["locked_facts"] = locks
                self.commit(changed, error="LOCKED_FACT_CHANGED")

    def test_timing_gaps_overlap_negative_and_zero_duration_fail_without_writes(self):
        for start, end, expected in [(3.1, 6, "TIME_GAP_OR_OVERLAP"),
                                     (2.9, 6, "TIME_GAP_OR_OVERLAP"),
                                     (-1, 6, "INVALID_TIME"),
                                     (3, 3, "INVALID_TIME")]:
            with self.subTest(start=start, end=end):
                changed = copy.deepcopy(self.design)
                changed["scenes"][0]["shots"][1].update(start=start, end=end)
                self.commit(changed, error=expected)
        changed = copy.deepcopy(self.design)
        changed["scenes"][0]["shots"][1]["end"] = 5
        self.commit(changed, error="TIME_GAP_OR_OVERLAP")

    def test_unrecorded_holder_change_and_between_shot_jump_fail(self):
        changed = copy.deepcopy(self.design)
        changed["scenes"][0]["shots"][0]["exit_state"]["prop_holder"] = "daughter"
        self.commit(changed, error="UNEXPLAINED_STATE_CHANGE")
        changed = copy.deepcopy(self.design)
        changed["scenes"][0]["shots"][1]["enter_state"]["prop_holder"] = "daughter"
        self.commit(changed, error="CONTINUITY_BREAK")
        changed = copy.deepcopy(self.design)
        s = changed["scenes"][0]
        s["shots"][0]["exit_state"]["prop_holder"] = "daughter"
        s["shots"][0]["state_changes"] = [{"key": "prop_holder", "from": "father", "to": "daughter",
                                            "action": "Father hands her the cup in the continuous view."}]
        s["shots"][1]["enter_state"]["prop_holder"] = "daughter"
        s["shots"][1]["exit_state"]["prop_holder"] = "daughter"
        s["exit_state"]["prop_holder"] = "daughter"
        self.commit(changed)

    def test_axis_checks_all_path_points_not_just_endpoints(self):
        changed = copy.deepcopy(self.design)
        changed["scenes"][0]["shots"][0]["camera"]["path"] = [[1, 3], [1, -0.1], [1, 3]]
        self.commit(changed, error="AXIS_CROSSING")
        changed["scenes"][0]["shots"][0]["camera"]["path"] = [[1, 3], [1, 0], [1, 3]]
        self.commit(changed, error="AXIS_CROSSING")
        changed["scenes"][0]["shots"][0]["camera"]["path"] = [[1, 3], [0.8, 2], [1, 3]]
        self.commit(changed)

    def test_legitimate_empty_establishing_shot_needs_no_character_or_axis(self):
        changed = copy.deepcopy(self.design)
        s = changed["scenes"][0]
        s.update(enter_state={}, exit_state={}, axis={"status": "not_applicable", "reason": "Unpeopled establishing view with no directional action."})
        for sh in s["shots"]:
            sh.update(enter_state={}, exit_state={}, camera={"description": "Fixed architectural view."})
        self.commit(changed)
        self.assertTrue(self.cli("check", "--scene", "S1")["ready"])

    def test_equivalent_natural_language_is_not_keyword_scored(self):
        changed = copy.deepcopy(self.design)
        s = changed["scenes"][0]
        s["director_intent"] = "让观众同时看到邀请落空和女儿仍然在场。"
        s["shots"][0]["framing"] = "椅子保持可见，两个人仍在画面里面。"
        s["shots"][0]["motion"] = {"description": "观察位置保持安静。"}
        self.commit(changed)
        self.assertTrue(self.cli("check", "--scene", "S1")["ready"])

    def test_source_drift_blocks_restore_commit_and_export(self):
        self.commit()
        before = self.state_path.read_bytes()
        changed = self.saved()
        self.source.write_text("The user has now changed the scene.\n", encoding="utf-8")
        self.cli("context", error="SOURCE_DRIFT")
        self.commit(changed, error="SOURCE_DRIFT")
        self.delivery(error="SOURCE_DRIFT")
        self.assertEqual(self.state_path.read_bytes(), before)
        self.assertFalse((self.root / "delivery.json").exists())

    def test_old_revision_or_hash_blocks_commit_and_export(self):
        self.commit()
        self.commit(self.saved(), version=self.initial, error="STALE_REVISION")
        self.delivery(version=self.initial, error="STALE_REVISION")
        invalid_hash = {**self.current, "state_sha256": "0" * 64}
        self.commit(self.saved(), version=invalid_hash, error="STALE_REVISION")
        self.delivery(version=invalid_hash, error="STALE_REVISION")
        self.assertFalse((self.root / "delivery.json").exists())

    def test_export_binds_exact_text_without_claiming_semantic_success(self):
        self.commit()
        output = self.delivery()
        receipt = json.loads((self.root / "delivery.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["text"], (self.root / "delivery.md").read_bytes().decode("utf-8"))
        self.assertEqual(receipt["text_sha256"], sha((self.root / "delivery.md").read_bytes()))
        self.assertEqual(receipt["state_sha256"], self.current["state_sha256"])
        self.assertEqual(receipt["scene_sha256"], scene_sha(self.design["scenes"][0]))
        self.assertTrue(receipt["machine_constraints_only"])
        self.assertFalse(receipt["text_semantics_verified"])
        self.assertEqual(output["delivery_status"], "machine_checked_awaiting_semantic_and_visual_review")

    def test_malformed_missing_duplicate_and_nonfinite_data_fail_without_writes(self):
        for mutate, error in [
            (lambda s: s["scenes"][0]["shots"][0].pop("camera"), "MISSING_INFORMATION"),
            (lambda s: s["scenes"].append(copy.deepcopy(s["scenes"][0])), "DUPLICATE_ID"),
            (lambda s: s["scenes"][0]["shots"][1].update(shot_id="S1-01"), "DUPLICATE_ID"),
            (lambda s: s["scenes"][0].update(source_lines=[1, 999]), "SOURCE_RANGE"),
            (lambda s: s["scenes"][0]["shots"][0].update(start=float("nan")), "NONFINITE_NUMBER"),
            (lambda s: s["scenes"][0]["shots"][0].update(start=float("inf")), "NONFINITE_NUMBER"),
        ]:
            with self.subTest(error=error):
                changed = copy.deepcopy(self.design)
                mutate(changed)
                self.commit(changed, error=error)
        raw = json.dumps(self.design)
        for malformed, error in [("{", "INVALID_JSON"), ('{"x":1,"x":2}', "DUPLICATE_KEY"),
                                 (raw.replace('"start": 0', '"start": 1e999', 1), "NONFINITE_NUMBER")]:
            with self.subTest(error=error):
                (self.root / "proposal.json").write_text(malformed, encoding="utf-8")
                before = self.state_path.read_bytes()
                self.cli("commit", "--input", "proposal.json", *self.token(), error=error)
                self.assertEqual(self.state_path.read_bytes(), before)

    def test_existing_lock_is_never_removed(self):
        lock = self.root / ".director_design" / "write.lock"
        lock.write_text("other-process", encoding="utf-8")
        self.commit(error="LOCK_EXISTS")
        self.assertEqual(lock.read_text(encoding="utf-8"), "other-process")
        lock.unlink()

    def test_init_and_export_do_not_overwrite_existing_files(self):
        before = self.state_path.read_bytes()
        self.cli("init", "--project-id", "other", "--source", "script.md", error="STATE_EXISTS")
        self.assertEqual(self.state_path.read_bytes(), before)
        self.commit()
        self.delivery()
        receipt = (self.root / "delivery.json").read_bytes()
        self.delivery(error="OUTPUT_EXISTS")
        self.assertEqual((self.root / "delivery.json").read_bytes(), receipt)

    def test_upstream_hash_binding_and_scene_state_handoff(self):
        second = copy.deepcopy(self.design["scenes"][0])
        second["scene_id"] = "S2"
        for i, item in enumerate(second["shots"]):
            item["shot_id"] = f"S2-0{i + 1}"
        second["previous_scene"] = {"scene_id": "S1", "sha256": scene_sha(self.design["scenes"][0])}
        self.design["scenes"].append(second)
        self.commit()
        changed = self.saved()
        changed["scenes"][0]["director_intent"] = "An intentionally changed upstream directing decision."
        self.commit(changed, error="STALE_UPSTREAM")
        changed["scenes"][1]["previous_scene"]["sha256"] = scene_sha(changed["scenes"][0])
        changed["scenes"][1]["enter_state"]["prop_holder"] = "daughter"
        self.commit(changed, error="CONTINUITY_BREAK")

    def test_explicit_amendment_preserves_old_design_and_invalidates_current_scenes(self):
        self.commit()
        old = self.saved()
        changed = copy.deepcopy(old)
        self.source.write_text("Father invites her.\nDaughter now sits, following the latest user change.\n", encoding="utf-8")
        changed["source"] = {"path": "script.md", "sha256": sha(self.source.read_bytes()), "line_count": 2}
        changed["locked_facts"] = [{"id": "L1", "statement": "The daughter now sits."}]
        self.commit(changed, extra=["--amend", "--change-reason", "User explicitly changed the action."],
                    error="AMEND_REQUIRES_REDESIGN")
        changed["scenes"] = []
        self.commit(changed, extra=["--amend"], error="MISSING_INFORMATION")
        self.commit(changed, extra=["--amend", "--change-reason", "User explicitly changed the action."])
        state = self.saved()
        self.assertEqual(state["scenes"], [])
        self.assertEqual(state["history"][0]["previous_state"]["scenes"], old["scenes"])
        self.assertEqual(state["history"][0]["previous_state"]["locked_facts"], old["locked_facts"])
        self.assertFalse(self.cli("context")["design_ready"])
        self.delivery(error="SCENE_MISSING")

    def test_declared_complex_axis_is_preserved_and_export_requires_review(self):
        self.design["scenes"][0]["axis"] = {
            "status": "needs_geometry_review",
            "reason": "The camera deliberately crosses during a continuously readable actor move."}
        self.design["scenes"][0]["shots"][0]["camera"]["path"] = [[1, 3], [1, -3]]
        self.commit()
        self.assertEqual(self.saved()["scenes"][0]["shots"][0]["camera"]["path"], [[1, 3], [1, -3]])
        report = self.cli("check", "--scene", "S1")
        self.assertFalse(report["ready"])
        self.assertEqual(report["status"], "needs_geometry_review")
        self.delivery(error="NEEDS_GEOMETRY_REVIEW")
        self.assertFalse((self.root / "delivery.json").exists())


    def test_scripted_cross_scene_ellipsis_has_an_explicit_transition(self):
        second = copy.deepcopy(self.design["scenes"][0])
        second["scene_id"] = "S2"
        second["previous_scene"] = {"scene_id": "S1", "sha256": scene_sha(self.design["scenes"][0])}
        second["enter_state"] = second["exit_state"] = {"prop_holder": "daughter"}
        for i, item in enumerate(second["shots"]):
            item["shot_id"] = f"S2-0{i + 1}"
            item["enter_state"] = item["exit_state"] = {"prop_holder": "daughter"}
        self.design["scenes"].append(second)
        self.commit(error="CONTINUITY_BREAK")
        second["entry_changes"] = [{"key": "prop_holder", "from": "father", "to": "daughter",
                                     "action": "The script cuts to later, after the cup was handed over."}]
        self.commit()
        self.assertTrue(self.cli("check", "--scene", "S2")["ready"])
        changed = self.saved()
        changed["scenes"][1]["entry_changes"][0]["from"] = "someone else"
        self.commit(changed, error="STATE_CHANGE_MISMATCH")

    def test_unverified_geometry_can_be_exported_as_visible_candidate_only(self):
        self.design["scenes"][0]["axis"] = {"status": "needs_geometry_review",
                                             "reason": "Deliberate continuously visible crossing."}
        self.design["scenes"][0]["shots"][0]["camera"]["path"] = [[1, 3], [1, -3]]
        self.commit()
        self.delivery(extra=["--allow-unverified-geometry"], error="MISSING_INFORMATION")
        result = self.delivery(extra=["--allow-unverified-geometry", "--review-note",
                                      "Show the candidate for an independent spatial review."])
        self.assertFalse(result["ready"])
        self.assertFalse(result["geometry_verified"])
        self.assertFalse(result["text_semantics_verified"])
        self.assertEqual(result["delivery_status"], "unverified_candidate")
        self.assertEqual(result["needs_geometry_review"], ["S1"])
        # Flags never waive stale hashes.
        self.delivery(extra=["--allow-unverified-geometry", "--review-note", "Candidate only"],
                      version=self.initial, output="stale.json", error="STALE_REVISION")
        self.assertFalse((self.root / "stale.json").exists())

    def test_geometry_candidate_flag_cannot_waive_an_actual_undeclared_crossing(self):
        self.commit()
        damaged = self.saved()
        damaged["scenes"][0]["shots"][0]["camera"]["path"] = [[1, 3], [1, -3]]
        # Simulate an external edit, independently of commit's rejection.
        self.state_path.write_text(json.dumps(damaged), encoding="utf-8")
        version = {"revision": damaged["revision"], "state_sha256": sha(self.state_path.read_bytes())}
        self.delivery(extra=["--allow-unverified-geometry", "--review-note", "Candidate only"],
                      version=version, error="AXIS_CROSSING")
        self.assertFalse((self.root / "delivery.json").exists())

    def test_omitting_a_saved_scene_cannot_silently_lose_previous_design(self):
        self.commit()
        omitted = self.saved()
        omitted["scenes"] = []
        self.commit(omitted, error="SCENE_REMOVED")


    def test_compact_scene_restore_keeps_global_decisions_without_unrelated_bodies_or_history(self):
        original = self.design["scenes"][0]
        original["director_intent"] = "UNRELATED_PRECEDING_SCENE_BODY"
        middle = copy.deepcopy(original)
        middle["scene_id"] = "S2"
        middle["director_intent"] = "CURRENT_SCENE_BODY"
        middle["previous_scene"] = {"scene_id": "S1", "sha256": scene_sha(original)}
        for i, item in enumerate(middle["shots"]):
            item["shot_id"] = f"S2-{i + 1}"
        last = copy.deepcopy(middle)
        last["scene_id"] = "S3"
        last["director_intent"] = "UNRELATED_FOLLOWING_SCENE_BODY"
        last["previous_scene"] = {"scene_id": "S2", "sha256": scene_sha(middle)}
        for i, item in enumerate(last["shots"]):
            item["shot_id"] = f"S3-{i + 1}"
        self.design["scenes"] = [original, middle, last]
        self.commit()
        amended = self.saved()
        amended["scenes"] = []
        self.commit(amended, extra=["--amend", "--change-reason", "HISTORY_BODY_MUST_NOT_BE_RETURNED"])
        restored = self.saved()
        restored["scenes"] = copy.deepcopy(self.design["scenes"])
        self.commit(restored)
        before = self.state_path.read_bytes()
        compact = self.cli("context", "--scene", "S2", "--compact")
        serialized = json.dumps(compact)
        self.assertEqual(self.state_path.read_bytes(), before)
        self.assertNotIn("state", compact)
        self.assertNotIn("history", compact)
        for marker in ("UNRELATED_PRECEDING_SCENE_BODY", "UNRELATED_FOLLOWING_SCENE_BODY",
                       "HISTORY_BODY_MUST_NOT_BE_RETURNED"):
            self.assertNotIn(marker, serialized)
        self.assertEqual(compact["scene"], middle)
        self.assertEqual(compact["film_intent"], self.design["film_intent"])
        self.assertEqual(compact["locked_facts"], self.design["locked_facts"])
        self.assertEqual(compact["candidate_decisions"], self.design["candidate_decisions"])
        self.assertEqual(compact["previous_scene"], middle["previous_scene"])
        self.assertEqual([item["scene_id"] for item in compact["scene_index"]], ["S1", "S2"])
        self.assertEqual(compact["state_sha256"], sha(before))
        self.assertEqual(compact["scene_sha256"], scene_sha(middle))
        self.assertEqual(compact["source_excerpt"][0]["line"], 1)
        self.assertTrue(compact["knowledge"])
        self.assertEqual(compact["history_count"], 1)
        # Default behavior remains compatible for editing complete proposals.
        full = self.cli("context", "--scene", "S2")
        self.assertEqual(full["state"], self.saved())

    def test_compact_without_scene_returns_only_directory_and_global_decisions(self):
        self.commit()
        compact = self.cli("context", "--compact", "--topics", "motion")
        self.assertNotIn("state", compact)
        self.assertNotIn("history", compact)
        self.assertIsNone(compact["scene"])
        self.assertIsNone(compact["source_excerpt"])
        self.assertEqual(compact["locked_facts"], self.design["locked_facts"])
        self.assertEqual(compact["scene_index"], [{"scene_id": "S1",
                                                   "sha256": scene_sha(self.design["scenes"][0]),
                                                   "source_lines": [1, 2]}])
        self.assertNotIn("Hold the refusal and continued presence together.", json.dumps(compact))

    def test_absolute_relative_and_junction_escape_are_rejected(self):
        outside = self.base / "outside"
        outside.mkdir()
        outside_source = outside / "script.md"
        outside_source.write_text("outside", encoding="utf-8")
        self.cli("init", "--project-id", "escape", "--source", outside_source, error="PATH_ESCAPE")
        self.cli("init", "--project-id", "escape", "--source", "../outside/script.md", error="PATH_ESCAPE")
        link = self.root / "outside-link"
        if os.name == "nt":
            # The verified target and link are both within this test's temporary directory.
            command = ["powershell", "-NoProfile", "-NonInteractive", "-Command",
                       "New-Item -ItemType Junction -Path $args[0] -Target $args[1] | Out-Null",
                       str(link), str(outside)]
            # PowerShell -Command does not reliably bind trailing path arguments across versions.
            command[-3:] = ["New-Item -ItemType Junction -Path '" + str(link).replace("'", "''") +
                             "' -Target '" + str(outside).replace("'", "''") + "' | Out-Null"]
            completed = subprocess.run(command, capture_output=True, text=True, timeout=20)
            self.assertEqual(completed.returncode, 0, completed.stderr)
        else:
            link.symlink_to(outside, target_is_directory=True)
        try:
            self.cli("init", "--project-id", "escape", "--source", "outside-link/script.md", error="PATH_ESCAPE")
            self.commit()
            self.delivery(output="outside-link/export.json", error="PATH_ESCAPE")
            self.assertFalse((outside / "export.json").exists())
        finally:
            if os.name == "nt":
                os.rmdir(link)  # Removes only the test-created junction, not its target.
            else:
                link.unlink()


if __name__ == "__main__":
    unittest.main(verbosity=2)
