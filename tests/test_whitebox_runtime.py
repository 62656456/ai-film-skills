from __future__ import annotations

import copy
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from contextlib import redirect_stderr
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "experimental" / "whitebox-previs-executor" / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load_runtime(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ordinary = load_runtime("whitebox_ordinary", "run_blender_previs.py")
rigged = load_runtime("whitebox_rigged", "run_blender_rigged_fight.py")
legacy = load_runtime("whitebox_legacy", "render_previs.py")


def compiled_spec() -> dict:
    return {
        "schema_version": "previs-compiler/1.0",
        "meta": {"title": "runtime smoke", "prediction_claim": False},
        "playback": {"fps": 10, "duration_s": 0.2, "resolution": [320, 180]},
        "scene": {"geometry": [
            {"id": "floor", "proxy_type": "grid_plane", "center": [0, 0, 0], "size": [8, 8]},
            {"id": "box", "proxy_type": "box", "center": [0, 0, 0.5], "size": [1, 1, 1]},
        ]},
        "cast": [],
        "camera": {"sensor_width_mm": 36, "rigs": [{"id": "camera", "keys": [
            {"time_s": 0, "position": [4, -6, 3], "look_at": [0, 0, 0.5], "lens_mm": 35},
            {"time_s": 0.2, "position": [3.8, -6, 3], "look_at": [0, 0, 0.5], "lens_mm": 35},
        ]}]},
        "timeline": {"shots": [{"id": "shot", "start_s": 0, "end_s": 0.2, "camera_id": "camera"}]},
    }


def action_spec() -> dict:
    spec = compiled_spec()
    spec["meta"]["execution_backend"] = "rigged_joint_solver_v1"
    spec["validation_targets"] = {"require_attack_block_contact_recoil_readability": True}
    spec["action_program"] = {
        "schema_version": "previs-action/1.0", "backend": "baked_joint_ik",
        "profile": "test_preflight_only", "contact_frame": 1, "hold_frames": 1,
        "constraints": {"weapon_grips": ["left", "right"], "weapon_contact_socket": "weapon",
                        "defense_contact_sockets": ["defender"], "single_shared_contact": True,
                        "no_root_only_fight": True},
        "beats": [{"id": "contact", "start_frame": 1, "end_frame": 2}],
    }
    return spec


class WhiteboxRuntimeTests(unittest.TestCase):
    def run_launcher(self, folder: Path, spec: object, filename: str, blender: str | None = None):
        spec_path = folder / "spec.json"
        spec_path.write_text(json.dumps(spec), encoding="utf-8")
        command = [sys.executable, "-B", str(SCRIPTS / filename), "--spec", str(spec_path),
                   "--output", str(folder / "outputs" / "preview.mp4"),
                   "--project", str(folder / "outputs" / "preview.blend"),
                   "--validation", str(folder / "outputs" / "validation.json"),
                   "--runtime-dir", str(folder / "runtime")]
        if blender:
            command.extend(["--blender", blender])
        env = os.environ.copy()
        env.update({"PATH": "", "WHITEBOX_BLENDER": "", "PYTHONDONTWRITEBYTECODE": "1"})
        return subprocess.run(command, cwd=folder, env=env, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=90)

    def main_arguments(self, folder: Path, spec: dict):
        path = folder / "spec.json"
        path.write_text(json.dumps(spec), encoding="utf-8")
        return SimpleNamespace(blender=sys.executable, spec=str(path),
                               output=str(folder / "outputs/preview.mp4"),
                               project=str(folder / "outputs/preview.blend"),
                               validation=str(folder / "outputs/validation.json"),
                               runtime_dir=str(folder / "runtime"), frames_dir=None)

    def test_existing_non_blender_files_fail_preflight_without_task_directories(self):
        for filename, spec in (("run_blender_previs.py", compiled_spec()), ("run_blender_rigged_fight.py", action_spec())):
            for kind in ("README.md", "broken.exe", "python"):
                with self.subTest(launcher=filename, executable=kind), tempfile.TemporaryDirectory() as raw:
                    folder = Path(raw)
                    executable = Path(sys.executable) if kind == "python" else folder / kind
                    if kind != "python":
                        executable.write_bytes(b"This is not an executable Blender binary.\n")
                    result = self.run_launcher(folder, spec, filename, str(executable))
                    self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
                    self.assertIn("Blender", result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertFalse((folder / "runtime").exists())
                    self.assertFalse((folder / "outputs").exists())

    def test_version_timeout_and_nonzero_status_fail_before_creating_runtime(self):
        for runtime, spec in ((ordinary, compiled_spec()), (rigged, action_spec())):
            for outcome in (subprocess.TimeoutExpired(["blender", "--version"], 10), subprocess.CompletedProcess([], 9, "Blender 5.2.1\n", "failure")):
                with self.subTest(launcher=runtime.__name__, outcome=type(outcome).__name__), tempfile.TemporaryDirectory() as raw:
                    folder = Path(raw)
                    args = self.main_arguments(folder, spec)
                    stderr = io.StringIO()
                    behavior = {"side_effect": outcome} if isinstance(outcome, Exception) else {"return_value": outcome}
                    with mock.patch.object(runtime, "arguments", return_value=args), mock.patch.object(runtime, "find_blender", return_value=Path(sys.executable)), mock.patch.object(runtime.subprocess, "run", **behavior) as call, redirect_stderr(stderr):
                        self.assertEqual(runtime.main(), 3)
                    self.assertEqual(call.call_count, 1)
                    self.assertEqual(call.call_args.kwargs["timeout"], 10)
                    self.assertNotIn("Traceback", stderr.getvalue())
                    self.assertFalse((folder / "runtime").exists())
                    self.assertFalse((folder / "outputs").exists())

    def test_final_launch_failure_is_reported_and_existing_outputs_are_preserved(self):
        for runtime, spec in ((ordinary, compiled_spec()), (rigged, action_spec())):
            for outcome, expected_code in ((OSError("executable became unavailable after version check"), 3), (subprocess.CompletedProcess([], 7), 7)):
                with self.subTest(launcher=runtime.__name__, outcome=type(outcome).__name__), tempfile.TemporaryDirectory() as raw:
                    folder = Path(raw)
                    args = self.main_arguments(folder, spec)
                    (folder / "outputs").mkdir()
                    existing = [Path(args.output), Path(args.project), Path(args.validation)]
                    for path in existing:
                        path.write_bytes(b"existing output must remain unchanged")
                    stderr = io.StringIO()
                    probe = subprocess.CompletedProcess([], 0, "Blender 5.2.1\n", "")
                    with mock.patch.object(runtime, "arguments", return_value=args), mock.patch.object(runtime, "find_blender", return_value=Path(sys.executable)), mock.patch.object(runtime.subprocess, "run", side_effect=[probe, outcome]) as call, redirect_stderr(stderr):
                        self.assertEqual(runtime.main(), expected_code)
                    self.assertEqual(call.call_count, 2)
                    self.assertIn("failed", stderr.getvalue())
                    self.assertNotIn("Traceback", stderr.getvalue())
                    for path in existing:
                        self.assertEqual(path.read_bytes(), b"existing output must remain unchanged")

    def test_missing_blender_returns_three_without_output_or_runtime_directories(self):
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            result = self.run_launcher(folder, compiled_spec(), "run_blender_previs.py")
            self.assertEqual(result.returncode, 3, result.stderr)
            self.assertIn("Blender was not found", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertFalse((folder / "outputs").exists())
            self.assertFalse((folder / "runtime").exists())

    def test_invalid_spec_is_rejected_before_dependency_or_output_creation(self):
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            result = self.run_launcher(folder, [], "run_blender_previs.py")
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("JSON object", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertFalse((folder / "runtime").exists())

    def test_timeline_gap_is_rejected_before_blender(self):
        with tempfile.TemporaryDirectory() as raw:
            spec = compiled_spec()
            spec["timeline"]["shots"][0]["start_s"] = 0.1
            result = self.run_launcher(Path(raw), spec, "run_blender_previs.py")
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("gap or overlap", result.stderr)

    def test_ordinary_backend_cannot_accept_a_rigged_fight_contract(self):
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            result = self.run_launcher(folder, action_spec(), "run_blender_previs.py")
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("require run_blender_rigged_fight.py", result.stderr)
            self.assertFalse((folder / "runtime").exists())

    def test_rigged_backend_requires_an_action_program(self):
        with tempfile.TemporaryDirectory() as raw:
            result = self.run_launcher(Path(raw), compiled_spec(), "run_blender_rigged_fight.py")
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("requires a valid previs-action/1.0", result.stderr)

    def test_rigged_missing_dependency_does_not_start_a_fallback_renderer(self):
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            result = self.run_launcher(folder, action_spec(), "run_blender_rigged_fight.py")
            self.assertEqual(result.returncode, 3, result.stderr)
            self.assertFalse((folder / "outputs").exists())
            self.assertFalse((folder / "runtime").exists())

    def test_configured_blender_precedes_path_and_invalid_configuration_fails(self):
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            chosen = folder / "chosen-blender"
            explicit = folder / "explicit-blender"
            chosen.write_bytes(b"test executable locator only")
            explicit.write_bytes(b"test executable locator only")
            for runtime in (ordinary, rigged):
                with self.subTest(runtime=runtime.__name__), mock.patch.dict(os.environ, {"WHITEBOX_BLENDER": str(chosen)}), mock.patch.object(runtime.shutil, "which", return_value="unused"):
                    self.assertEqual(runtime.find_blender(None, folder), chosen.resolve())
                    self.assertEqual(runtime.find_blender(str(explicit), folder), explicit.resolve())
                with mock.patch.dict(os.environ, {"WHITEBOX_BLENDER": str(folder / "missing")}), mock.patch.object(runtime.shutil, "which", return_value=str(explicit)):
                    with self.assertRaises(FileNotFoundError):
                        runtime.find_blender(None, folder)

    def test_ffmpeg_explicit_environment_and_path_precedence(self):
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            explicit = folder / "explicit-ffmpeg"
            configured = folder / "configured-ffmpeg"
            explicit.write_bytes(b"locator test")
            configured.write_bytes(b"locator test")
            with mock.patch.dict(os.environ, {"WHITEBOX_FFMPEG": str(configured)}), mock.patch.object(legacy.shutil, "which", return_value="on-path"):
                self.assertEqual(legacy.find_ffmpeg(str(explicit)), str(explicit.resolve()))
                self.assertEqual(legacy.find_ffmpeg(None), str(configured.resolve()))
            with mock.patch.dict(os.environ, {"WHITEBOX_FFMPEG": str(folder / "missing")}), mock.patch.object(legacy.shutil, "which", return_value="on-path"):
                self.assertIsNone(legacy.find_ffmpeg(None))
            with mock.patch.dict(os.environ, {"WHITEBOX_FFMPEG": ""}), mock.patch.object(legacy.shutil, "which", return_value="on-path"):
                self.assertEqual(legacy.find_ffmpeg(None), "on-path")

    def test_ffprobe_sibling_name_matches_ffmpeg_platform(self):
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            output = folder / "preview.mp4"
            output.write_bytes(b"probe input placeholder")
            for suffix in ("", ".exe"):
                probe = folder / ("ffprobe" + suffix)
                probe.write_bytes(b"locator test")
                with mock.patch.dict(os.environ, {"WHITEBOX_FFPROBE": ""}), mock.patch.object(legacy.shutil, "which", return_value=None), mock.patch.object(legacy.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, '{"streams": []}', "")) as call:
                    self.assertEqual(legacy.probe(str(folder / ("ffmpeg" + suffix)), output), {"streams": []})
                    self.assertEqual(call.call_args.args[0][0], str(probe))

    @unittest.skipUnless(os.environ.get("WHITEBOX_TEST_BLENDER"), "set WHITEBOX_TEST_BLENDER for the opt-in two-frame real Blender smoke")
    def test_real_blender_executes_and_decodes_a_two_frame_movie(self):
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            result = self.run_launcher(folder, compiled_spec(), "run_blender_previs.py", os.environ["WHITEBOX_TEST_BLENDER"])
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            video = folder / "outputs" / "preview.mp4"
            self.assertGreater(video.stat().st_size, 0)
            report = json.loads((folder / "outputs" / "validation.json").read_text(encoding="utf-8"))
            self.assertEqual(report["frames_expected"], 2)
            self.assertEqual(report["decoded_frames"], 2)
            self.assertEqual(report["decoded_size"], [320, 180])


if __name__ == "__main__":
    unittest.main()
