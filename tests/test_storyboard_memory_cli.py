from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "skills/ai-storyboard-director/scripts/design_memory.py"


class StoryboardMemoryCLITests(unittest.TestCase):
    def call(self, root: Path, command: str, *args: str):
        process = subprocess.run([sys.executable, "-B", str(CLI), command, "--project-root", str(root), *args],
                                 capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=15)
        self.assertFalse(process.stderr.strip(), process.stderr)
        return process.returncode, json.loads(process.stdout)

    def initialize(self, root: Path):
        (root / "screenplay.txt").write_text("A person opens a door.\n", encoding="utf-8")
        code, payload = self.call(root, "init", "--project-id", "memory-test", "--source", "screenplay.txt")
        self.assertEqual(code, 0, payload)
        return payload

    def commit_scenes(self, root: Path, second_axis: str = "needs_geometry_review"):
        initialized = self.initialize(root)
        state = initialized["state"]
        state["film_intent"] = {"intent": "Observe the door", "rationale": "Keep the entrance readable"}
        for number in (1, 2):
            previous = state["scenes"][-1] if state["scenes"] else None
            axis_status = "defined" if number == 1 else second_axis
            axis = ({"status": "defined", "start": [0, 0], "end": [2, 0], "allowed_side": "positive"}
                    if axis_status == "defined" else {"status": axis_status, "reason": "Recorded scene-specific scope"})
            state["scenes"].append({
                "scene_id": f"scene-{number}", "source_lines": [1, 1],
                "dramatic_change": "The person waits at the door", "director_intent": "Show the waiting",
                "enter_state": {"door": "closed"}, "exit_state": {"door": "closed"},
                "previous_scene": ({"scene_id": previous["scene_id"], "sha256": hashlib.sha256(
                    json.dumps(previous, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
                ).hexdigest()} if previous else None),
                "duration_seconds": 4, "design_questions": ["Is the entrance readable?"],
                "knowledge_topics": ["framing"], "axis": axis,
                "shots": [{"shot_id": f"shot-{number}", "start": 0, "end": 4,
                           "viewing_task": "See the person and door", "framing": "Both remain visible",
                           "camera": {"path": [[1, 3]]}, "motion": {"description": "Fixed camera"},
                           "ending": "The person waits", "enter_state": {"door": "closed"},
                           "exit_state": {"door": "closed"}}],
            })
        (root / "proposal.json").write_text(json.dumps(state), encoding="utf-8")
        code, payload = self.call(root, "commit", "--input", "proposal.json",
                                 "--expected-revision", "0", "--expected-sha256", initialized["state_sha256"])
        self.assertEqual(code, 0, payload)
        (root / "delivery.txt").write_text("The person waits beside the closed door.\n", encoding="utf-8")
        return payload

    def export(self, root: Path, current: dict, scene: str, *extra: str):
        return self.call(root, "export", "--scene", scene, "--text", "delivery.txt", "--output", "receipt.json",
                         "--expected-revision", str(current["revision"]),
                         "--expected-sha256", current["state_sha256"], *extra)

    def test_init_and_compact_context_use_the_bundled_framing_references(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.initialize(root)
            code, payload = self.call(root, "context", "--compact", "--topics", "framing")
            self.assertEqual(code, 0, payload)
            self.assertNotIn("state", payload)
            self.assertFalse(payload["design_ready"])
            self.assertTrue(any(Path(entry["path"]).name == "framing-and-axis.md" for entry in payload["knowledge"]))
            for entry in payload["knowledge"]:
                path = Path(entry["path"])
                self.assertTrue(path.is_relative_to(CLI.parent.parent))
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), entry["sha256"])

    def test_reinitialization_never_overwrites_existing_decisions(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.initialize(root)
            state = root / ".director_design/state.json"
            before = state.read_bytes()
            code, payload = self.call(root, "init", "--project-id", "replacement", "--source", "screenplay.txt")
            self.assertEqual(code, 1)
            self.assertEqual(payload["error"], "STATE_EXISTS")
            self.assertEqual(state.read_bytes(), before)

    def test_changed_script_is_rejected_without_rewriting_memory(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.initialize(root)
            state = root / ".director_design/state.json"
            before = state.read_bytes()
            (root / "screenplay.txt").write_text("A different story.\n", encoding="utf-8")
            code, payload = self.call(root, "context", "--compact")
            self.assertEqual(code, 1)
            self.assertIn("SOURCE", payload["error"])
            self.assertEqual(state.read_bytes(), before)

    def test_checked_scene_exports_with_its_own_geometry_status(self):
        for other_axis in ("needs_geometry_review", "not_applicable"):
            with self.subTest(other_axis=other_axis), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                current = self.commit_scenes(root, other_axis)
                code, checked = self.call(root, "check", "--scene", "scene-1")
                self.assertEqual(code, 0, checked)
                self.assertTrue(checked["ready"])
                self.assertEqual(checked["needs_geometry_review"], [])
                code, exported = self.export(root, current, "scene-1")
                self.assertEqual(code, 0, exported)
                self.assertTrue(exported["ready"])
                self.assertTrue(exported["geometry_verified"])
                self.assertEqual(exported["needs_geometry_review"], [])
                code, context = self.call(root, "context", "--compact")
                self.assertEqual(code, 0, context)
                self.assertEqual(context["design_ready"], other_axis != "needs_geometry_review")

    def test_selected_pending_scene_requires_explicit_candidate_export(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            current = self.commit_scenes(root)
            code, checked = self.call(root, "check", "--scene", "scene-2")
            self.assertEqual(code, 0, checked)
            self.assertFalse(checked["ready"])
            self.assertEqual(checked["needs_geometry_review"], ["scene-2"])
            code, rejected = self.export(root, current, "scene-2")
            self.assertEqual(code, 1)
            self.assertEqual(rejected["error"], "NEEDS_GEOMETRY_REVIEW")
            self.assertFalse((root / "receipt.json").exists())
            code, candidate = self.export(root, current, "scene-2", "--allow-unverified-geometry",
                                          "--review-note", "Owner will review the curved path")
            self.assertEqual(code, 0, candidate)
            self.assertFalse(candidate["ready"])
            self.assertFalse(candidate["geometry_verified"])
            self.assertEqual(candidate["needs_geometry_review"], ["scene-2"])
            self.assertEqual(candidate["delivery_status"], "unverified_candidate")

    def test_other_scene_structural_error_still_blocks_selected_export(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            current = self.commit_scenes(root)
            state_path = root / ".director_design/state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["scenes"][1]["shots"][0]["end"] = 3
            state_path.write_text(json.dumps(state), encoding="utf-8")
            before = state_path.read_bytes()
            current["state_sha256"] = hashlib.sha256(before).hexdigest()
            code, payload = self.export(root, current, "scene-1")
            self.assertEqual(code, 1)
            self.assertEqual(payload["error"], "TIME_GAP_OR_OVERLAP")
            self.assertEqual(state_path.read_bytes(), before)
            self.assertFalse((root / "receipt.json").exists())

    def test_initialization_rejects_all_internal_source_files(self):
        for filename in ("state.json", "source.txt"):
            with self.subTest(filename=filename), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                internal = root / ".director_design"
                internal.mkdir()
                source = internal / filename
                source.write_text("Internal work record\n", encoding="utf-8")
                before = source.read_bytes()
                code, payload = self.call(root, "init", "--project-id", "memory-test", "--source",
                                          f".director_design/{filename}")
                self.assertEqual(code, 1)
                self.assertEqual(payload["error"], "RESERVED_SOURCE")
                self.assertEqual(source.read_bytes(), before)

    def test_commit_rejects_legacy_internal_source_without_rewriting_state(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            initialized = self.initialize(root)
            internal = root / ".director_design/source.txt"
            internal.write_text("Internal work record\n", encoding="utf-8")
            state = initialized["state"]
            state["source"] = {"path": ".director_design/source.txt",
                               "sha256": hashlib.sha256(internal.read_bytes()).hexdigest(), "line_count": 1}
            state_path = root / ".director_design/state.json"
            state_path.write_text(json.dumps(state), encoding="utf-8")
            before = state_path.read_bytes()
            (root / "proposal.json").write_bytes(before)
            code, payload = self.call(root, "commit", "--input", "proposal.json", "--expected-revision", "0",
                                      "--expected-sha256", hashlib.sha256(before).hexdigest())
            self.assertEqual(code, 1)
            self.assertEqual(payload["error"], "RESERVED_SOURCE")
            self.assertEqual(state_path.read_bytes(), before)

    def test_amendment_cannot_replace_source_with_the_state_it_will_overwrite(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            initialized = self.initialize(root)
            state_path = root / ".director_design/state.json"
            before = state_path.read_bytes()
            proposal = initialized["state"]
            proposal["source"] = {"path": ".director_design/state.json",
                                  "sha256": hashlib.sha256(before).hexdigest(),
                                  "line_count": len(before.decode("utf-8").splitlines())}
            (root / "proposal.json").write_text(json.dumps(proposal), encoding="utf-8")
            code, payload = self.call(root, "commit", "--input", "proposal.json", "--amend",
                                      "--change-reason", "Explicit screenplay revision", "--expected-revision", "0",
                                      "--expected-sha256", initialized["state_sha256"])
            self.assertEqual(code, 1)
            self.assertEqual(payload["error"], "RESERVED_SOURCE")
            self.assertEqual(state_path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
