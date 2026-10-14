from __future__ import annotations

import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "skills/ai-storyboard-director"


def module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, PACKAGE / "scripts" / filename)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


motion = module("fcml_motion", "fcml_motion.py")
source = module("fcml_source_audit", "fcml_source_audit.py")


class FCMLMotionTests(unittest.TestCase):
    def setUp(self):
        self.library = motion.load_library()

    def test_current_source_and_canonical_counts_are_derived_not_an_expected_website_number(self):
        self.assertEqual(motion.validate_library(self.library), [])
        summary = motion.audit_summary(self.library)
        records = self.library["source_records"]
        categories = self.library["source_audit"]["categories"]
        self.assertEqual(summary["catalog_count"], len(records))
        self.assertEqual(summary["catalog_count"], sum(c["actual_items"] for c in categories))
        self.assertEqual(summary["full_content_read_count"], sum(r["full_prompt_read"] for r in records))
        self.assertEqual(summary["canonical_count"], len(self.library["motions"]))
        self.assertEqual(summary["mapped_source_count"], len(records))
        for row in records:
            item = motion.get_motion(self.library, row["source_id"])
            self.assertEqual(item["id"], row["canonical_id"])
            self.assertIn(row["source_id"], item["source_ids"])

    def test_catalog_and_full_content_reading_are_separate(self):
        tiny = [{"id": "system-test", "name": "Test inventory", "categories": [
            {"id": "test-category", "name": "Test category", "items": [
                {"id": "test-a", "name": "Has full content", "prompt": "Synthetic test fixture only"},
                {"id": "test-b", "name": "Unread title", "prompt": ""}]}]}]
        script = "const fixture = JSON.parse(" + repr(json.dumps(tiny)) + ");"
        audit = source.inspect(script)
        self.assertEqual(audit["catalog_count"], 2)
        self.assertEqual(audit["full_content_available_count"], 1)
        self.assertIsNone(audit["coverage_denominator"])
        self.assertIsNone(audit["full_content_coverage"])
        self.assertFalse(audit["enumeration_complete"])
        verified = source.inspect(script, enumeration_verified=True)
        self.assertEqual(verified["full_content_coverage"], 0.5)
        self.assertFalse(verified["records"][1]["complete_prompt_available"])

    def test_incomplete_enumeration_cannot_claim_a_complete_denominator(self):
        self.library["source_audit"]["enumeration_complete"] = False
        summary = motion.audit_summary(self.library)
        self.assertIsNone(summary["coverage_denominator"])
        self.assertIsNone(summary["directory_coverage"])
        self.assertIsNone(summary["full_content_coverage"])
        self.assertIn("incomplete_enumeration_claimed_complete", motion.validate_library(self.library))
        self.assertTrue(any(e.startswith("unverified_denominator") for e in motion.validate_library(self.library)))

    def test_unread_prompt_is_not_repaired_by_adjusting_the_success_count(self):
        self.library["source_records"][0]["full_prompt_read"] = False
        self.library["source_records"][0]["missing_reason"] = "Full expanded content was not available"
        self.library["source_audit"]["full_content_read_count"] -= 1
        self.assertIn("content_or_mapping_gap_claimed_complete", motion.validate_library(self.library))
        summary = motion.audit_summary(self.library)
        self.assertLess(summary["full_content_coverage"], 1)
        self.assertFalse(summary["gaps"][0]["full_prompt_read"])

    def test_read_claim_needs_available_content_and_real_hash(self):
        self.library["source_records"][0]["complete_prompt_available"] = False
        self.library["source_records"][0]["prompt_sha256"] = "title only"
        self.assertTrue(any(e.startswith("unsupported_full_read:") for e in motion.validate_library(self.library)))

    def test_duplicate_mapping_failure_is_visible(self):
        duplicate = next(r for r in self.library["source_records"] if r["duplicate_of"])
        other = next(m for m in self.library["motions"] if m["id"] != duplicate["canonical_id"])
        duplicate["canonical_id"] = other["id"]
        self.assertIn("invalid_duplicate_mapping:" + duplicate["source_id"], motion.validate_library(self.library))

    def test_same_broad_mechanism_with_different_stage_or_viewpoint_is_not_deleted(self):
        resume = motion.get_motion(self.library, "yj055")
        stop = motion.get_motion(self.library, "yj070")
        self.assertNotEqual(resume["id"], stop["id"])
        self.assertIn("freeze_resume", [o["mode"] for o in resume["operations"]])
        self.assertIn("freeze", [o["mode"] for o in stop["operations"]])
        for left, right in (("yj107", "yj114"), ("yj099", "yj108"), ("yj052", "yj113")):
            self.assertNotEqual(motion.get_motion(self.library, left)["id"], motion.get_motion(self.library, right)["id"])

    def test_placeholder_and_missing_mechanism_fields_fail_structure_validation(self):
        item = self.library["motions"][0]
        item["purpose"] = "TODO"
        item["phases"][1]["camera_and_attention"] = " "
        item["template_zh"] = "{起始构图}。{终点构图}。{环境承接}。"
        item["variables"] = ["起始构图", "终点构图", "环境承接"]
        errors = motion.validate_library(self.library)
        self.assertIn("unusable_text:" + item["id"] + ":purpose", errors)
        self.assertIn("process_missing:" + item["id"], errors)
        self.assertIn("mechanism_missing:" + item["id"], errors)

    def test_translation_orientation_optics_and_roll_have_distinct_operation_contracts(self):
        expected = {
            "yj001": {"translation"}, "yj034": {"focal_length"},
            "yj022": {"translation"}, "yj021": {"orientation"},
            "yj029": {"translation"}, "yj019": {"orientation"},
            "yj025": {"translation", "orientation"}, "yj046": {"orientation"},
        }
        for sid, kinds in expected.items():
            self.assertEqual(set(motion.get_motion(self.library, sid)["operation_types"]), kinds)
        self.assertEqual(motion.get_motion(self.library, "yj046")["operations"][0]["mode"], "roll")
        self.assertEqual(motion.get_motion(self.library, "yj019")["operations"][0]["mode"], "tilt_up")
        self.assertEqual(motion.get_motion(self.library, "yj029")["operations"][0]["mode"], "up")

    def test_bound_camera_paragraph_distinguishes_dolly_from_stationary_zoom(self):
        dolly = motion.adapt(motion.get_motion(self.library, "fcml-001"), {"variables": {
            "起始构图": "摄影机在洁净大厅南侧，面向北墙的圆形壁钟",
            "可走路径": "大厅中央原有无障碍通道", "主体": "北墙壁钟",
            "终点构图": "停在钟面可辨且左右壁板仍可见的中近景",
            "环境承接": "顶窗照明稳定，厅内无人且地面干燥"}})
        zoom = motion.adapt(motion.get_motion(self.library, "fcml-034"), {"variables": {
            "起始构图": "摄影机在洁净大厅南侧，面向北墙的圆形壁钟",
            "变焦阶段": "既定辨认阶段", "起始范围": "北墙与钟的全景", "细节对象": "钟面",
            "终点构图": "停在钟面可辨且左右壁板仍可见的中近景",
            "环境承接": "顶窗照明稳定，厅内无人且地面干燥"}})
        self.assertIn("保持焦距", dolly)
        self.assertIn("前后景视差", dolly)
        self.assertIn("摄影机中心及朝向固定", zoom)
        self.assertIn("增加焦距", zoom)
        self.assertNotIn("增加焦距", dolly)
        self.assertNotIn("摄影机中心及朝向固定", dolly)

    def test_variable_binding_does_not_copy_source_plot_duration_or_sound(self):
        item = motion.get_motion(self.library, "fcml-049")
        result = motion.adapt(item, {"variables": {
            "起始构图": "从人物右后方看其进入已定连接走廊，二维手绘风格",
            "主体": "已定人物", "跟随路径": "走廊右侧可走路线", "跟随距离": "约定的肩后距离",
            "空间地标": "两房之间已有门框", "揭示对象": "第二房间尽头的已有窗",
            "终点构图": "人物停下，摄影机留在门内，背景窗保持可辨",
            "环境承接": "窗外已定车辆继续向东行进，干燥地面不变"}, "locked_medium": "二维手绘"})
        for retained in ("门框", "第二房间", "窗外已定车辆继续", "二维手绘"):
            self.assertIn(retained, result)
        for borrowed in ("10 秒", "少年", "玉佩", "长剑", "60fps", "HDR", "背景音乐"):
            self.assertNotIn(borrowed, result)
        with self.assertRaises(motion.LibraryError):
            motion.adapt(item, {"variables": {"主体": "已定人物"}})

    def test_nonphysical_effect_is_preserved_as_candidate_then_requires_adoption(self):
        found = motion.search(self.library, "冻结", ["time"], 6)
        self.assertTrue(found)
        item = motion.get_motion(self.library, "fcml-070")
        variables = {key: "既有已定" + key for key in item["variables"]}
        with self.assertRaises(motion.LibraryError):
            motion.adapt(item, {"variables": variables})
        result = motion.adapt(item, {"variables": variables, "adopted_effects": ["freeze_vfx"]})
        self.assertIn("暂停", result)
        self.assertIn("每个冻结物体保持位置和光照", result)

    def test_medium_transition_needs_an_explicit_adopted_change(self):
        item = motion.get_motion(self.library, "fcml-099")
        values = {key: "既有已定" + key for key in item["variables"]}
        with self.assertRaises(motion.LibraryError):
            motion.adapt(item, {"variables": values, "locked_medium": "二维水墨", "adopted_effects": ["medium_vfx"]})
        result = motion.adapt(item, {"variables": values, "locked_medium": "二维水墨",
                                    "adopted_effects": ["medium_vfx"], "approved_medium_transition": True})
        self.assertIn("布局与动作连续", result)

    def test_source_ai_category_does_not_force_an_ai_only_classification(self):
        item = motion.get_motion(self.library, "yj093")
        record = next(r for r in self.library["source_records"] if r["source_id"] == "yj093")
        self.assertEqual(record["system_id"], "system2")
        self.assertEqual(item["effect_policy"]["kind"], "none")
        self.assertTrue(any("实拍" in x for x in item["source_corrections"]))
        self.assertIsNone(item["validation"]["platform"])
        self.assertEqual(item["validation"]["media_test"], "not_run")

    def test_package_does_not_redistribute_full_source_prompts(self):
        forbidden_keys = {"prompt", "logic", "effect", "original_prompt", "original_text"}
        for record in self.library["source_records"]:
            self.assertFalse(forbidden_keys & record.keys())
            self.assertEqual(len(record["prompt_sha256"]), 64)
        self.assertFalse(self.library["source_audit"]["copyright"]["raw_source_text_in_package"])

    def test_normalized_path_and_time_relations_survive_variable_binding(self):
        # Explicit mechanism relationships, not the website's example durations.
        expectations = {
            "fcml-028": ("one_complete_closed_orbit", "闭合整周", "先慢速", "中段加速", "末段放缓"),
            "fcml-040": ("one_complete_wide_closed_orbit", "完整闭合绕行", "回到起始观看方位"),
            "fcml-054": ("half_orbit_to_opposite_side", "起始侧到相对侧", "动作始终有进度"),
            "fcml-070": ("one_complete_closed_orbit", "一次闭合整周", "终点继续停在同一冻结时刻"),
            "fcml-075": ("stepwise_segments_sum_to_one_complete_orbit", "每次停顿内", "下一节点恢复", "累计闭合一整周"),
            "fcml-076": ("one_complete_detail_orbit", "一个闭合整周", "过程仍有可辨进度"),
        }
        for mid, (relation, *phrases) in expectations.items():
            item = motion.get_motion(self.library, mid)
            self.assertEqual(item["mechanism_invariants"]["path_coverage"], relation)
            values = {key: "现行方案已定" + key for key in item["variables"]}
            context = {"variables": values, "adopted_effects": [item["effect_policy"]["kind"]]}
            text = motion.adapt(item, context)
            for phrase in phrases:
                self.assertIn(phrase, text)
            self.assertNotIn("10 秒", text)
        barrel = motion.get_motion(self.library, "fcml-056")
        self.assertEqual(barrel["mechanism_invariants"]["orientation"], "one_complete_optical_axis_roll")
        self.assertIn("完整滚转回合", barrel["template_zh"])
        self.assertIn("起始地平线方向", barrel["template_zh"])

    def test_breath_pulse_radial_time_and_dive_phase_relations_are_explicit(self):
        breath = motion.get_motion(self.library, "fcml-093")
        self.assertEqual(breath["mechanism_invariants"]["phase_direction"],
                         {"inhale": "small_backward", "exhale": "small_forward"})
        self.assertIn("吸气时轻微退离、呼气时轻微接近", breath["template_zh"])
        pulse = motion.get_motion(self.library, "fcml-094")
        self.assertEqual(pulse["mechanism_invariants"]["trigger_relation"], "one_impulse_one_camera_response")
        self.assertIn("每个脉冲对应一次", pulse["template_zh"])
        self.assertIn("运动幅度", pulse["template_zh"])
        radial = motion.get_motion(self.library, "fcml-079")
        self.assertEqual(radial["mechanism_invariants"]["time_relation"], "center_frozen_outer_regions_progressively_faster")
        for phrase in ("暂停区域", "越向外层", "越快演进", "时间边界的外扩"):
            self.assertIn(phrase, radial["template_zh"])
        dive = motion.get_motion(self.library, "fcml-042")
        self.assertEqual(dive["mechanism_invariants"]["phase_order"],
                         ["high_position_stationary_hold", "rapid_descent", "braking", "stable_endpoint_hold"])
        self.assertIn("先保持静止", dive["template_zh"])

    def test_basic_follow_does_not_require_an_unrequested_reveal_object(self):
        item = motion.get_motion(self.library, "fcml-049")
        context = {"variables": {"起始构图": "人物背后中景", "主体": "已定人物", "跟随路径": "既有走廊右侧",
                                 "跟随距离": "既定肩后距离", "终点构图": "人物停在已有窗前",
                                 "环境承接": "窗外车辆继续行驶，灯光状态不变"}}
        text = motion.adapt(item, context)
        self.assertIn("人物始终可读", text)
        self.assertNotIn("揭示对象", text)
        self.assertNotIn("依真实遮挡顺序进入", text)
        self.assertNotIn("停步后", text)
        self.assertEqual(item["mechanism_invariants"]["subject_action"], "follow_locked_action_without_adding_stop")
        context["variables"]["终点构图"] = "人物持续向前，摄影机保持肩后关系至本段切点"
        continued = motion.adapt(item, context)
        self.assertIn("人物持续向前", continued)
        self.assertNotIn("停步", continued)
        context["variables"]["空间地标"] = "现有门框"
        with self.assertRaises(motion.LibraryError):
            motion.adapt(item, context)

    def test_cli_preserves_chinese_json_with_legacy_stdout_encoding(self):
        env = dict(os.environ, PYTHONIOENCODING="cp1252", PYTHONUTF8="0", PYTHONDONTWRITEBYTECODE="1")
        probe = subprocess.run([sys.executable, "-B", "-c", "import sys; print(sys.stdout.encoding)"],
                               env=env, capture_output=True, text=True, encoding="ascii", timeout=15)
        self.assertEqual(probe.returncode, 0, probe.stderr)
        self.assertEqual(probe.stdout.strip().lower(), "cp1252")
        cli = PACKAGE / "scripts/fcml_motion.py"
        for args in (("get", "--id", "fcml-049"), ("search", "--query", "跟随"),
                     ("audit",), ("validate",), ("get", "--id", "不存在")):
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, "-B", str(cli), *args], env=env,
                                        capture_output=True, timeout=15)
                body = result.stdout.decode("utf-8")
                self.assertFalse(result.stderr, result.stderr)
                payload = json.loads(body)
                self.assertEqual(result.returncode, int(args[-1] == "不存在"), body)
                if args[:2] == ("get", "--id") and result.returncode == 0:
                    expected = motion.get_motion(self.library, "fcml-049")
                    self.assertEqual(payload["motions"][0], expected)
                    self.assertIn(expected["name"].encode("utf-8"), result.stdout)
                elif args[0] == "validate":
                    self.assertTrue(payload["passed"])
                elif result.returncode:
                    self.assertEqual(payload["error"], "Unknown or unmapped mechanism: 不存在")

    def test_isolated_package_lookup_and_audit_work_with_network_blocked(self):
        with tempfile.TemporaryDirectory() as raw:
            destination = Path(raw) / "isolated-skill"
            for folder in ("scripts", "assets", "references"):
                shutil.copytree(PACKAGE / folder, destination / folder,
                                ignore=shutil.ignore_patterns("__pycache__"))
            cli = destination / "scripts/fcml_motion.py"
            code = (
                "import socket,runpy,sys; "
                "socket.create_connection=lambda *a,**k: (_ for _ in ()).throw(RuntimeError('network forbidden')); "
                "socket.socket=lambda *a,**k: (_ for _ in ()).throw(RuntimeError('network forbidden')); "
                "sys.argv=[sys.argv[1]]+sys.argv[2:]; runpy.run_path(sys.argv[0],run_name='__main__')"
            )
            env = dict(os.environ, PYTHONPATH="", PYTHONDONTWRITEBYTECODE="1")
            for args in (("validate",), ("get", "--id", "fcml-049"), ("audit",)):
                result = subprocess.run([sys.executable, "-B", "-c", code, str(cli), *args], cwd=raw,
                                        env=env, capture_output=True, text=True, encoding="utf-8", timeout=15)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertFalse(result.stderr.strip(), result.stderr)
                payload = json.loads(result.stdout)
                if args[0] == "get":
                    self.assertEqual(payload["motions"][0]["id"], "fcml-049")
                elif args[0] == "validate":
                    self.assertTrue(payload["passed"])


if __name__ == "__main__":
    unittest.main()
