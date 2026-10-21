import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/priorities.py"
spec = importlib.util.spec_from_file_location("priorities", SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class PrioritiesTests(unittest.TestCase):
    def test_corrupt_store_controlled_error(self):
        for invalid in [
            [],
            {"schema": "session-priorities.v1", "revision": True, "items": "bad"},
            {"schema": "session-priorities.v1", "revision": 0, "items": [False]},
        ]:
            with tempfile.TemporaryDirectory() as directory:
                path = m.state_path("codex", "A", Path(directory))
                path.parent.mkdir(parents=True)
                path.write_text(json.dumps(invalid), encoding="utf-8")
                with self.assertRaises(ValueError):
                    m.read(path)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_sessions_and_providers_isolated(self):
        a = m.state_path("codex", "A", self.root)
        m.update(a, m.parse_items("Betrieb; Aufgaben"), 0)
        for provider, sid in [("codex", "B"), ("claude", "A")]:
            self.assertEqual(m.read(m.state_path(provider, sid, self.root))["items"], [])

    def test_missing_or_global_id_rejected(self):
        for sid in ["", " ", "default", "global"]:
            with self.assertRaises(ValueError):
                m.state_path("codex", sid, self.root)

    def test_namespace_traversal_rejected(self):
        with self.assertRaises(ValueError):
            m.state_path("../bad", "A", self.root)

    def test_weights_and_umlauts(self):
        self.assertEqual(m.parse_items("40::Prüfen; 100::Übernehmen")[0], {"text": "Übernehmen", "weight": 100})
        with self.assertRaises(ValueError):
            m.parse_items("101::bad")

    def test_stale_revision_keeps_current(self):
        p = m.state_path("codex", "A", self.root)
        current = m.update(p, m.parse_items("Original"), 0)
        with self.assertRaises(ValueError):
            m.update(p, m.parse_items("stale"), 0)
        self.assertEqual(m.read(p), current)

    def test_busy_lock_not_removed(self):
        p = m.state_path("codex", "A", self.root)
        p.parent.mkdir(parents=True)
        lock = p.with_suffix(".lock")
        lock.write_text("foreign")
        with self.assertRaises(FileExistsError):
            m.update(p, [], 0)
        self.assertEqual(lock.read_text(), "foreign")

    def test_goal_file_unchanged(self):
        goal = self.root / "goal.json"
        goal.write_text(json.dumps({"criteria": list(range(124))}))
        before = goal.read_bytes()
        m.update(m.state_path("codex", "A", self.root), m.parse_items("Gewichten"), 0)
        self.assertEqual(goal.read_bytes(), before)

    def test_cli_and_clear(self):
        args = [
            sys.executable,
            str(SCRIPT),
            "set",
            "Prüfen",
            "--provider",
            "codex",
            "--session-id",
            "A",
            "--root",
            str(self.root),
            "--if-revision",
            "0",
        ]
        out = subprocess.run(args, capture_output=True, encoding="utf-8")
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertEqual(json.loads(out.stdout)["revision"], 1)
        m.update(m.state_path("codex", "A", self.root), [], 1)
        self.assertEqual(m.read(m.state_path("codex", "A", self.root))["items"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
