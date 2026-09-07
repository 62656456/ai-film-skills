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


if __name__ == "__main__":
    unittest.main()
