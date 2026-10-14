from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "skills/ai-storyboard-director/scripts/design_memory.py"


class StoryboardMemoryCLITests(unittest.TestCase):
    def call(self, root: Path, command: str, *args: str, cli: Path = CLI):
        process = subprocess.run([sys.executable, "-B", str(cli), command, "--project-root", str(root), *args],
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

    @staticmethod
    def scene_hash(scene: dict):
        return hashlib.sha256(json.dumps(scene, ensure_ascii=False, sort_keys=True,
                                         separators=(",", ":")).encode("utf-8")).hexdigest()

    def commit_proposal(self, root: Path, current: dict, proposal: dict):
        (root / "proposal.json").write_text(json.dumps(proposal), encoding="utf-8")
        return self.call(root, "commit", "--input", "proposal.json",
                         "--expected-revision", str(current["revision"]),
                         "--expected-sha256", current["state_sha256"])

    def optional_contracts(self, root: Path, current: dict):
        state = json.loads((root / ".director_design/state.json").read_text(encoding="utf-8"))
        for scene in state["scenes"]:
            scene.update({
                "spatial_contract": {"entrance": "south wall", "table": {"location": "center"}},
                "visual_design": {"first_visual_focus": "table", "color_roles": {"accent": "dark green"},
                                  "critical_retention": ["Keep the entrance visible"]},
                "environment_baseline": {"time_weather": "morning", "ongoing_elements": [],
                                         "stable_conditions": ["dry indoor floor"]},
                "filming_conditions": {"walkable_routes": ["south entrance to table"],
                                       "camera_accessible_regions": ["southwest aisle"],
                                       "useful_occluders": [], "forbidden_passages": ["walls", "table"]},
            })
            shot = scene["shots"][0]
            shot["critical_retention"] = ["Keep the doorway readable",
                                          {"id": "paper-final", "description": "Paper rests on the table"}]
            shot["motion"].update({"fcml_ids": ["fcml-001"], "operations": [{"type": "translation", "mode": "forward"}],
                                   "stages": [{"trigger": "doorway revealed", "path": "southwest aisle",
                                               "ending": {"paper": "table"}}]})
        state["scenes"][1]["previous_scene"]["sha256"] = self.scene_hash(state["scenes"][0])
        code, payload = self.commit_proposal(root, current, state)
        self.assertEqual(code, 0, payload)
        return payload

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

    def test_legacy_and_optional_records_restore_and_export_without_synthetic_fields(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            current = self.commit_scenes(root, "defined")
            path = root / ".director_design/state.json"
            legacy_bytes = path.read_bytes()
            code, legacy = self.call(root, "context", "--scene", "scene-1", "--compact")
            self.assertEqual(code, 0, legacy)
            for field in ("spatial_contract", "visual_design", "environment_baseline", "filming_conditions"):
                self.assertNotIn(field, legacy["scene"])
            self.assertNotIn("critical_retention", legacy["scene"]["shots"][0])
            self.assertEqual(legacy["scene"]["shots"][0]["motion"], {"description": "Fixed camera"})
            self.assertEqual(path.read_bytes(), legacy_bytes)

            current = self.optional_contracts(root, current)
            stored = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(stored["schema_version"], 1)
            self.assertEqual(set(stored), {"schema_version", "project_id", "revision", "source", "film_intent",
                                           "locked_facts", "candidate_decisions", "scenes", "history"})
            before = path.read_bytes()
            for flags in ((), ("--compact",)):
                code, restored = self.call(root, "context", "--scene", "scene-1", *flags)
                self.assertEqual(code, 0, restored)
                self.assertEqual(restored["scene"], stored["scenes"][0])
                self.assertEqual(restored["scene_sha256"], self.scene_hash(stored["scenes"][0]))
                self.assertFalse(restored["text_semantics_verified"])
            code, exported = self.export(root, current, "scene-1")
            self.assertEqual(code, 0, exported)
            self.assertEqual(exported["scene"], stored["scenes"][0])
            receipt = json.loads((root / "receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt["scene"], stored["scenes"][0])
            self.assertEqual(receipt["scene_sha256"], self.scene_hash(receipt["scene"]))
            self.assertEqual(path.read_bytes(), before)

    def test_local_shot_edit_preserves_scene_contracts_and_other_scenes(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            current = self.optional_contracts(root, self.commit_scenes(root, "defined"))
            path = root / ".director_design/state.json"
            before = json.loads(path.read_text(encoding="utf-8"))
            proposal = copy.deepcopy(before)
            proposal["scenes"][1]["shots"][0]["framing"] = "Face and doorway share the frame"
            code, saved = self.commit_proposal(root, current, proposal)
            self.assertEqual(code, 0, saved)
            code, restored = self.call(root, "context", "--scene", "scene-2", "--compact")
            self.assertEqual(code, 0, restored)
            after = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(after["scenes"][0], before["scenes"][0])
            for field in ("spatial_contract", "visual_design", "environment_baseline", "filming_conditions"):
                self.assertEqual(restored["scene"][field], before["scenes"][1][field])
            for field in ("critical_retention", "motion", "camera"):
                self.assertEqual(restored["scene"]["shots"][0][field], before["scenes"][1]["shots"][0][field])
            self.assertEqual(restored["scene"]["shots"][0]["framing"], "Face and doorway share the frame")

    def test_selected_library_operations_round_trip_without_a_second_motion_schema(self):
        library = json.loads((CLI.parent.parent / "assets/fcml-motion-library.json").read_text(encoding="utf-8"))
        chosen = next(m for m in library["motions"] if "translation" in m["operation_types"]
                      and "orientation" in m["operation_types"])
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            current = self.commit_scenes(root, "defined")
            baseline = json.loads((root / ".director_design/state.json").read_text(encoding="utf-8"))
            baseline["scenes"][1]["shots"][0]["motion"].update(
                fcml_ids=[chosen["id"]], operations=copy.deepcopy(chosen["operations"]))
            code, saved = self.commit_proposal(root, current, baseline)
            self.assertEqual(code, 0, saved)
            code, restored = self.call(root, "context", "--scene", "scene-2", "--compact")
            self.assertEqual(code, 0, restored)
            self.assertEqual(restored["scene"]["shots"][0]["motion"]["operations"], chosen["operations"])
            # Older operation-label lists remain readable without rewriting them.
            baseline = json.loads((root / ".director_design/state.json").read_text(encoding="utf-8"))
            baseline["scenes"][1]["shots"][0]["motion"]["operations"] = ["translation"]
            code, saved = self.commit_proposal(root, saved, baseline)
            self.assertEqual(code, 0, saved)
            code, restored = self.call(root, "context", "--scene", "scene-2", "--compact")
            self.assertEqual(code, 0, restored)
            self.assertEqual(restored["scene"]["shots"][0]["motion"]["operations"], ["translation"])

    def test_visual_and_camera_decisions_restore_and_export_without_reselection(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            current = self.optional_contracts(root, self.commit_scenes(root, "defined"))
            path = root / ".director_design/state.json"
            proposal = json.loads(path.read_text(encoding="utf-8"))
            scene = proposal["scenes"][1]
            scene["visual_design"]["decision_record"] = {
                "alternatives": [{"id": "whole", "composition_sketch": "Door, table and chair share equal space"},
                                 {"id": "boundary", "composition_sketch": "Near table edge bounds an open doorway"}],
                "selected": "boundary", "selection_basis": "Keep the walkable entrance legible beside the table edge"}
            scene["visual_design"]["light_sources"] = [
                {"name": "existing east window", "world_position": "east wall",
                 "softness": "directional with a distinct edge", "relative_intensity": "dominant",
                 "occlusion": "existing frame divides the bright floor area"}]
            scene["visual_design"]["camera_white_balance_intent"] = "Daylight; pale wood keeps its own color"
            scene["visual_design"]["decision_record"]["structural_delta"] = [
                "A defined lit floor shape beside the dark table underside replaces even illumination"]
            scene["shots"][0]["camera"]["decision_record"] = {
                "alternatives": [{"id": "follow", "frames": ["door", "person enters", "table"]},
                                 {"id": "wait", "frames": ["table and door", "person approaches", "hand and table"]}],
                "selected": "wait", "selection_basis": "Let the person change scale without moving the camera"}
            scene["shots"][0]["camera"]["decision_record"]["selected_frames"] = [
                {"phase": "start", "visible_scale": "full person beside doorway", "focus": ["person", "door"]},
                {"phase": "end", "visible_scale": "hand large beside table edge", "focus": ["hand", "table"]}]
            code, saved = self.commit_proposal(root, current, proposal)
            self.assertEqual(code, 0, saved)
            code, restored = self.call(root, "context", "--scene", "scene-2", "--compact")
            self.assertEqual(code, 0, restored)
            self.assertEqual(restored["scene"]["visual_design"]["decision_record"], scene["visual_design"]["decision_record"])
            self.assertEqual(restored["scene"]["visual_design"], scene["visual_design"])
            self.assertEqual(restored["scene"]["shots"][0]["camera"]["decision_record"], scene["shots"][0]["camera"]["decision_record"])
            code, exported = self.export(root, saved, "scene-2")
            self.assertEqual(code, 0, exported)
            self.assertEqual(exported["scene"], restored["scene"])
            self.assertFalse(exported["text_semantics_verified"])

    def test_invalid_decision_record_types_are_rejected_without_writing(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            current = self.optional_contracts(root, self.commit_scenes(root, "defined"))
            path = root / ".director_design/state.json"
            before = path.read_bytes()
            for owner, value in (("visual_design", []), ("camera", "chosen shot")):
                proposal = json.loads(before)
                scene = proposal["scenes"][1]
                target = scene[owner] if owner == "visual_design" else scene["shots"][0][owner]
                target["decision_record"] = value
                code, rejected = self.commit_proposal(root, current, proposal)
                self.assertEqual(code, 1, rejected)
                self.assertEqual(path.read_bytes(), before)

    def test_selected_frame_change_is_bound_to_scene_hash_and_revision(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            current = self.commit_scenes(root, "defined")
            path = root / ".director_design/state.json"
            proposal = json.loads(path.read_text(encoding="utf-8"))
            previous_hash = self.scene_hash(proposal["scenes"][1])
            proposal["scenes"][1]["shots"][0]["camera"]["decision_record"] = {
                "selected": "Keep table and doorway simultaneously visible"}
            code, saved = self.commit_proposal(root, current, proposal)
            self.assertEqual(code, 0, saved)
            code, restored = self.call(root, "context", "--scene", "scene-2", "--compact")
            self.assertEqual(code, 0, restored)
            self.assertNotEqual(restored["scene_sha256"], previous_hash)
            before = path.read_bytes()
            code, rejected = self.commit_proposal(root, current, json.loads(before))
            self.assertEqual(code, 1, rejected)
            self.assertEqual(rejected["error"], "STALE_REVISION")
            self.assertEqual(path.read_bytes(), before)

    def test_invalid_optional_fields_are_rejected_before_state_write(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            current = self.optional_contracts(root, self.commit_scenes(root, "defined"))
            path = root / ".director_design/state.json"
            before = path.read_bytes()
            baseline = json.loads(before)
            cases = [("scene", field, []) for field in (
                "spatial_contract", "visual_design", "environment_baseline", "filming_conditions")]
            cases += [("shot", "critical_retention", "one item"),
                      ("shot", "critical_retention", [42]),
                      ("shot", "critical_retention", [{"id": "paper", "description": []}]),
                      ("motion", "fcml_ids", "fcml-001"), ("motion", "fcml_ids", [42]),
                      ("motion", "fcml_ids", ["duplicate", "duplicate"]),
                      ("motion", "operations", {}), ("motion", "operations", [True]),
                      ("motion", "operations", [{"type": "translation"}]),
                      ("motion", "operations", [{"type": "translation", "mode": []}]),
                      ("motion", "operations", ["translation", "translation"]),
                      ("motion", "stages", {}), ("motion", "stages", ["not an object"])]
            for owner, field, value in cases:
                with self.subTest(owner=owner, field=field, value=value):
                    proposal = copy.deepcopy(baseline)
                    scene = proposal["scenes"][1]
                    target = scene if owner == "scene" else scene["shots"][0]
                    if owner == "motion":
                        target = target["motion"]
                    target[field] = value
                    code, rejected = self.commit_proposal(root, current, proposal)
                    self.assertEqual(code, 1, rejected)
                    self.assertIn(rejected["error"], {"INVALID_FORMAT", "MISSING_INFORMATION", "DUPLICATE_ID"})
                    self.assertEqual(path.read_bytes(), before)
                    self.assertFalse((root / ".director_design/write.lock").exists())

    def test_optional_scene_changes_affect_upstream_hash_and_cas(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            current = self.optional_contracts(root, self.commit_scenes(root, "defined"))
            path = root / ".director_design/state.json"
            before = path.read_bytes()
            proposal = json.loads(before)
            original_hash = self.scene_hash(proposal["scenes"][0])
            proposal["scenes"][0]["environment_baseline"]["stable_conditions"].append("no wind")
            changed_hash = self.scene_hash(proposal["scenes"][0])
            self.assertNotEqual(changed_hash, original_hash)
            code, rejected = self.commit_proposal(root, current, proposal)
            self.assertEqual(code, 1, rejected)
            self.assertEqual(rejected["error"], "STALE_UPSTREAM")
            self.assertEqual(path.read_bytes(), before)
            proposal["scenes"][1]["previous_scene"]["sha256"] = changed_hash
            code, saved = self.commit_proposal(root, current, proposal)
            self.assertEqual(code, 0, saved)
            self.assertNotEqual(saved["state_sha256"], current["state_sha256"])
            self.assertEqual(saved["revision"], current["revision"] + 1)
            after = path.read_bytes()
            code, stale = self.commit_proposal(root, current, proposal)
            self.assertEqual(code, 1, stale)
            self.assertEqual(stale["error"], "STALE_REVISION")
            self.assertEqual(path.read_bytes(), after)

    def test_concurrent_writers_keep_one_cas_winner_and_preserve_optional_contracts(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            current = self.optional_contracts(root, self.commit_scenes(root, "defined"))
            path = root / ".director_design/state.json"
            baseline = json.loads(path.read_text(encoding="utf-8"))
            processes = []
            for index in (1, 2):
                proposal = copy.deepcopy(baseline)
                proposal["scenes"][1]["shots"][0]["framing"] = f"Writer {index} revised framing"
                filename = f"proposal-{index}.json"
                (root / filename).write_text(json.dumps(proposal), encoding="utf-8")
                processes.append(subprocess.Popen(
                    [sys.executable, "-B", str(CLI), "commit", "--project-root", str(root),
                     "--input", filename, "--expected-revision", str(current["revision"]),
                     "--expected-sha256", current["state_sha256"]],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8"))
            outcomes = []
            for process in processes:
                stdout, stderr = process.communicate(timeout=15)
                self.assertFalse(stderr.strip(), stderr)
                outcomes.append((process.returncode, json.loads(stdout)))
            self.assertEqual(sorted(code for code, _ in outcomes), [0, 1], outcomes)
            rejected = next(payload for code, payload in outcomes if code == 1)
            self.assertIn(rejected["error"], {"LOCK_EXISTS", "STALE_REVISION"})
            stored = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(stored["revision"], current["revision"] + 1)
            self.assertEqual(stored["scenes"][0], baseline["scenes"][0])
            for field in ("spatial_contract", "visual_design", "environment_baseline", "filming_conditions"):
                self.assertEqual(stored["scenes"][1][field], baseline["scenes"][1][field])
            self.assertFalse((root / ".director_design/write.lock").exists())

    def test_isolated_bundle_motion_and_visual_context_returns_readable_local_references(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self.optional_contracts(root, self.commit_scenes(root, "defined"))
            bundle = root / "bundle/ai-storyboard-director"
            shutil.copytree(CLI.parent.parent, bundle)
            code, restored = self.call(root, "context", "--scene", "scene-1", "--compact",
                                       "--topics", "motion", "visual", cli=bundle / "scripts/design_memory.py")
            self.assertEqual(code, 0, restored)
            names = [Path(entry["path"]).name for entry in restored["knowledge"]]
            self.assertIn("fcml-motion-index.md", names)
            self.assertEqual(names.count("fcml-motion-index.md"), 1)
            self.assertTrue(all(not name.endswith(".json") for name in names))
            for entry in restored["knowledge"]:
                reference = Path(entry["path"])
                self.assertTrue(reference.is_relative_to(bundle))
                self.assertTrue(reference.is_file())
                self.assertEqual(hashlib.sha256(reference.read_bytes()).hexdigest(), entry["sha256"])
            self.assertIn("production-contract.md", names)
            self.assertIn("spatial_contract", restored["scene"])


if __name__ == "__main__":
    unittest.main()
