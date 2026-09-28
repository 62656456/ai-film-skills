from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_skill_suite import run_gate


class QualityGateTests(unittest.TestCase):
    def test_failed_check_stops_before_later_checks(self):
        with tempfile.TemporaryDirectory() as t:
            calls = []
            def runner(argv, **kwargs):
                calls.append(argv)
                return subprocess.CompletedProcess(argv, 1, "", "deliberate check failure")
            report = run_gate(profile="A", temporary=Path(t), sample=None, allow_external=False, run=runner)
            self.assertEqual(report["status"], "failed")
            self.assertEqual(len(calls), 1)

    def test_B_cannot_silently_pass_without_its_review(self):
        with tempfile.TemporaryDirectory() as t:
            def runner(*args, **kwargs):
                self.fail("no process should start without B prerequisites")
            report = run_gate(profile="B", temporary=Path(t), sample=None, allow_external=False, run=runner)
            self.assertEqual(report["status"], "failed")
            self.assertEqual(report["semantic_review"], "not_performed")

    def test_runtime_drift_invalidates_successful_checks(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "skills").mkdir()
            target = root / "skills" / "SKILL.md"
            target.write_text("before", encoding="utf-8")
            def runner(argv, **kwargs):
                target.write_text("changed", encoding="utf-8")
                return subprocess.CompletedProcess(argv, 0, "", "")
            report = run_gate(profile="A", temporary=root, sample=None, allow_external=False,
                              root=root, run=runner)
            self.assertEqual(report["status"], "failed")
            self.assertEqual(report["code"], "runtime_changed_during_checks")


if __name__ == "__main__":
    unittest.main()
