import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "bridge.py"
SPEC = importlib.util.spec_from_file_location("agents_bridge", MODULE_PATH)
BRIDGE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(BRIDGE)


class BridgeTests(unittest.TestCase):
    def test_discovery_marks_existing_surface(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)
            (home / "CLAUDE.md").write_text("# rules", encoding="utf-8")
            surfaces = BRIDGE.candidate_surfaces(home)
        claude = next(item for item in surfaces if item["provider_hint"] == "claude")
        self.assertTrue(claude["exists"])

    def test_project_discovery_is_optional(self):
        with tempfile.TemporaryDirectory() as temp:
            surfaces = BRIDGE.candidate_surfaces(Path(temp))
        self.assertFalse(any(item["scope"] == "project" for item in surfaces))

    def test_render_preserves_explicit_order(self):
        output = BRIDGE.render_loader(["first.md", "second.md"], "p1", "codex")
        self.assertLess(output.index("first.md"), output.index("second.md"))
        self.assertIn("Truth profile: p1", output)
        self.assertIn("Target kind: codex", output)

    def test_render_rejects_empty_truth(self):
        with self.assertRaises(ValueError):
            BRIDGE.render_loader([], "p1", "generic")


if __name__ == "__main__":
    unittest.main()
