from __future__ import annotations

import sys
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

    def test_shell_runtime_file_is_scanned(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            skill = make_skill(root, "alpha-skill")
            (skill / "run.sh").write_text('RULES="/home/user/private.md"\n', encoding="utf-8")
            errors = independence.validate_skill(skill, {"alpha-skill"})
            self.assertTrue(any("POSIX machine-local path" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
