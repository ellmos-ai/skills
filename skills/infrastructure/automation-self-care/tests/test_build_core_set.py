"""Tests for the provider-neutral automation core-set builder."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_core_set.py"
SPEC = importlib.util.spec_from_file_location("build_core_set", MODULE_PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


class CoreSetTests(unittest.TestCase):
    def profile(self, capabilities: list[str]) -> dict:
        return {
            "schema": "automation-self-care.provider.v1",
            "actor_id": "example-app@example-host",
            "provider": "example",
            "app_class": "desktop-app",
            "capabilities": capabilities,
            "native_surface": {"kind": "api", "identifier": "example"},
        }

    def test_compact_topology_has_five_tasks(self) -> None:
        plan = module.build_plan(self.profile([]), "compact")
        self.assertEqual(5, len(plan["tasks"]))
        self.assertEqual("plan-only", plan["installation_state"])

    def test_missing_write_capability_blocks_mutating_task(self) -> None:
        plan = module.build_plan(
            self.profile(["inventory", "run-history"]),
            "compact",
        )
        tasks = {task["task_id"]: task for task in plan["tasks"]}
        self.assertEqual("ready", tasks["automation-care.hygiene"]["readiness"])
        self.assertEqual(
            "blocked",
            tasks["automation-care.prompt-quality"]["readiness"],
        )

    def test_full_topology_preserves_nine_responsibilities(self) -> None:
        plan = module.build_plan(self.profile([]), "full")
        self.assertEqual(9, len(plan["tasks"]))
        self.assertIn(
            "automation-care.permissions",
            {task["task_id"] for task in plan["tasks"]},
        )


if __name__ == "__main__":
    unittest.main()
