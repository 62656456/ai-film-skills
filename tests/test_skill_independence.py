from __future__ import annotations

import sys
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_skill_independence as independence


def make_skill(root: Path, name: str, body: str = "") -> Path:
    skill = root / name
    skill.mkdir()
    (skill / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: standalone test\n---\n\n{body}\n",
        encoding="utf-8",
    )
    return skill


class SkillIndependenceTests(unittest.TestCase):
    def call(self, *roots: Path) -> subprocess.CompletedProcess[str]:
        process = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/validate_skill_independence.py"),
                                  *(str(root) for root in roots)], capture_output=True, text=True,
                                 encoding="utf-8", errors="replace", timeout=15)
        self.assertFalse(process.stderr.strip(), process.stderr)
        return process

    def test_current_repository_skills_are_independent(self) -> None:
        skills = independence.skill_dirs()
        names = {independence.frontmatter_name(skill) for skill in skills}
        errors = [
            error
            for skill in skills
            for error in independence.validate_skill(skill, names)
        ]
        self.assertEqual(errors, [])

    def test_sibling_skill_reference_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            alpha = make_skill(root, "alpha-skill", "Call beta-skill for its internal section.")
            make_skill(root, "beta-skill")
            errors = independence.validate_skill(alpha, {"alpha-skill", "beta-skill"})
            self.assertTrue(any("references sibling Skill" in error for error in errors))

    def test_machine_local_knowledge_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            skill = make_skill(root, "alpha-skill", r"Read E:\\private\\knowledge before acting.")
            errors = independence.validate_skill(skill, {"alpha-skill"})
            self.assertTrue(any("machine-local path" in error for error in errors))

    def test_missing_packaged_reference_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            skill = make_skill(root, "alpha-skill", "Read `references/missing.md`.")
            errors = independence.validate_skill(skill, {"alpha-skill"})
            self.assertTrue(any("missing packaged dependency" in error for error in errors))

    def test_second_hop_missing_reference_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            skill = make_skill(root, "alpha-skill", "Read `references/route.md`.")
            references = skill / "references"
            references.mkdir()
            (references / "route.md").write_text("Read `missing.md` before acting.\n", encoding="utf-8")
            errors = independence.validate_skill(skill, {"alpha-skill"})
            self.assertTrue(any("missing packaged dependency" in error for error in errors))

    def test_unlisted_personal_skill_reference_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            skill = make_skill(root, "alpha-skill", "Call xianxia-visual-director for story packets.")
            errors = independence.validate_skill(skill, {"alpha-skill"})
            self.assertTrue(any("references sibling Skill" in error for error in errors))

    def test_legacy_card_identifier_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            skill = make_skill(root, "alpha-skill", "Read A3-15 before dialogue revision.")
            errors = independence.validate_skill(skill, {"alpha-skill"})
            self.assertTrue(any("legacy runtime instruction" in error for error in errors))

    def test_unc_and_posix_machine_paths_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            skill = make_skill(root, "alpha-skill", "Read \\\\server\\share\\rules.md and /home/user/rules.md.")
            errors = independence.validate_skill(skill, {"alpha-skill"})
            self.assertTrue(any("UNC runtime path" in error for error in errors))
            self.assertTrue(any("POSIX machine-local path" in error for error in errors))

    def test_toml_runtime_pointer_is_scanned(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            skill = make_skill(root, "alpha-skill")
            (skill / "runtime.toml").write_text('rules = "C:\\\\private\\\\rules.md"\n', encoding="utf-8")
            errors = independence.validate_skill(skill, {"alpha-skill"})
            self.assertTrue(any("machine-local path" in error for error in errors))

    def test_negative_knowledge_statement_is_not_a_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            skill = make_skill(root, "alpha-skill", "Do not read a private knowledge base.")
            errors = independence.validate_skill(skill, {"alpha-skill"})
            self.assertFalse(any("external runtime instruction" in error for error in errors))

    def test_unregistered_external_skill_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            skill = make_skill(root, "alpha-skill", "Call outside-private-skill for its rules.")
            errors = independence.validate_skill(skill, {"alpha-skill"})
            self.assertTrue(any("references unregistered Skill" in error for error in errors))

    def test_normal_unregistered_skill_names_are_rejected(self) -> None:
        for body in ("Call create-data-context for its rules.", "Call outside-agent before acting.", "Call outside-agent.",
                     "Use `create-data-context` for its extraction rules.", "Load Skill outside-router."):
            with self.subTest(body=body), tempfile.TemporaryDirectory() as raw:
                skill = make_skill(Path(raw), "alpha-skill", body)
                errors = independence.validate_skill(skill, {"alpha-skill"})
                self.assertTrue(any("references unregistered Skill" in error for error in errors), errors)

    def test_hyphenated_output_and_rig_types_are_not_skills(self) -> None:
        for body in ("Use read-only output.", "Use `text-only` output.", "使用 `two-arm-hover`，只绘制两条手臂。"):
            with self.subTest(body=body), tempfile.TemporaryDirectory() as raw:
                skill = make_skill(Path(raw), "alpha-skill", body)
                self.assertEqual(independence.validate_skill(skill, {"alpha-skill"}), [])

    def test_second_hop_missing_shell_reference_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            skill = make_skill(Path(raw), "alpha-skill", "Read `references/route.md`.")
            references = skill / "references"
            references.mkdir()
            (references / "route.md").write_text("Read `run.sh` before acting.\n", encoding="utf-8")
            errors = independence.validate_skill(skill, {"alpha-skill"})
            self.assertTrue(any("missing packaged dependency" in error and "run.sh" in error for error in errors))

    def test_numbered_legacy_chain_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            skill = make_skill(root, "alpha-skill", "02 receives assets; 03 receives shots; 04 receives prompts; 06 receives QC.")
            errors = independence.validate_skill(skill, {"alpha-skill"})
            self.assertTrue(any("legacy runtime instruction" in error for error in errors))

    def test_unrelated_negation_does_not_hide_positive_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            skill = make_skill(root, "alpha-skill", "Do not skip validation; read the private knowledge base before acting.")
            errors = independence.validate_skill(skill, {"alpha-skill"})
            self.assertTrue(any("external runtime instruction" in error for error in errors))

    def test_comma_and_conjunction_do_not_extend_unrelated_negation(self) -> None:
        for body in ("Do not skip validation, read the private knowledge base before acting.",
                     "Do not skip validation and load the private knowledge base.",
                     "Do not read the screenplay, load the private knowledge base.",
                     "Do not read the screenplay and load the private knowledge base.",
                     "不得跳过检查，读取私人知识库后执行。", "不省略检查并加载私人知识库。"):
            with self.subTest(body=body), tempfile.TemporaryDirectory() as raw:
                skill = make_skill(Path(raw), "alpha-skill", body)
                errors = independence.validate_skill(skill, {"alpha-skill"})
                self.assertTrue(any("external runtime instruction" in error for error in errors), errors)

    def test_direct_and_coordinated_negative_runtime_calls_are_preserved(self) -> None:
        for body in ("Do not automatically load a private knowledge base.",
                     "Never read or load the private knowledge base.", "不读取或加载外部知识库。",
                     "Do not call outside-agent.", "不调用 outside-agent。"):
            with self.subTest(body=body), tempfile.TemporaryDirectory() as raw:
                skill = make_skill(Path(raw), "alpha-skill", body)
                self.assertEqual(independence.validate_skill(skill, {"alpha-skill"}), [])

    def test_explicit_missing_and_empty_roots_fail_the_cli(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            empty = root / "empty"
            empty.mkdir()
            for target in (empty, root / "does-not-exist"):
                with self.subTest(target=target):
                    process = self.call(target)
                    self.assertEqual(process.returncode, 1, process.stdout)
                    self.assertIn("explicit root contains no Skills", process.stdout)

    def test_each_explicit_root_must_contain_a_skill(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            valid = make_skill(root, "alpha-skill")
            empty = root / "empty"
            empty.mkdir()
            passing = self.call(valid)
            self.assertEqual(passing.returncode, 0, passing.stdout)
            self.assertIn("Isolation copies checked: 1", passing.stdout)
            rejected = self.call(valid, empty)
            self.assertEqual(rejected.returncode, 1, rejected.stdout)
            self.assertIn("explicit root contains no Skills", rejected.stdout)

    def test_shell_runtime_file_is_scanned(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            skill = make_skill(root, "alpha-skill")
            (skill / "run.sh").write_text('RULES="/home/user/private.md"\n', encoding="utf-8")
            errors = independence.validate_skill(skill, {"alpha-skill"})
            self.assertTrue(any("POSIX machine-local path" in error for error in errors))

    def test_chinese_attached_negation_preserves_independence(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            skill = make_skill(Path(raw), "alpha-skill", "本包独立运行，不依赖外部知识库。")
            self.assertEqual(independence.validate_skill(skill, {"alpha-skill"}), [])

    def test_chinese_negation_does_not_hide_later_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            skill = make_skill(Path(raw), "alpha-skill", "不依赖外部知识库；读取私人知识库后执行。")
            self.assertTrue(any("external runtime instruction" in e for e in independence.validate_skill(skill, {"alpha-skill"})))

    def test_python_dispatch_is_not_a_markdown_link(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            skill = make_skill(Path(raw), "alpha-skill")
            (skill / "run.py").write_text("handlers[args.command](args, root)\n", encoding="utf-8")
            self.assertEqual(independence.validate_skill(skill, {"alpha-skill"}), [])

    def test_python_comment_dependency_is_still_checked(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            skill = make_skill(Path(raw), "alpha-skill")
            (skill / "run.py").write_text("# Read [required rules](missing.md) first.\n", encoding="utf-8")
            self.assertTrue(any("missing packaged dependency" in e for e in independence.validate_skill(skill, {"alpha-skill"})))


if __name__ == "__main__":
    unittest.main()
