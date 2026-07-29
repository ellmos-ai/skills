"""Tests for the provider-neutral automation core-set builder."""

from __future__ import annotations

import importlib.util
import copy
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
            "app_display_name": "EXAMPLE",
            "app_class": "desktop-app",
            "capabilities": capabilities,
            "native_surface": {"kind": "api", "identifier": "example"},
            "recovery_floor": {"minimum_core_runs_per_day": 1},
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

    def test_codex_titles_use_display_prefix_without_changing_machine_ids(self) -> None:
        profile = self.profile([])
        profile["provider"] = "openai"
        profile["app_display_name"] = "CODEX"
        plan = module.build_plan(profile, "compact")

        self.assertEqual("CODEX", plan["app_display_name"])
        self.assertEqual(
            [
                "automation-care.hygiene",
                "automation-care.prompt-quality",
                "automation-care.scheduler-tuning",
                "automation-care.resources",
                "automation-care.cross-system",
            ],
            [task["task_id"] for task in plan["tasks"]],
        )
        self.assertTrue(
            all(task["title"].startswith("CODEX — ") for task in plan["tasks"])
        )
        self.assertFalse(plan["identity_and_reconciliation"]["title_is_identity"])

    def test_legacy_profile_derives_visible_name_and_records_migration(self) -> None:
        profile = self.profile([])
        del profile["app_display_name"]
        plan = module.build_plan(profile, "compact")
        self.assertEqual("EXAMPLE", plan["app_display_name"])
        self.assertTrue(plan["profile_warnings"])

    def test_plan_lint_detects_wrong_prefix_without_changing_task_id(self) -> None:
        plan = module.build_plan(self.profile([]), "compact")
        original_id = plan["tasks"][0]["task_id"]
        plan["tasks"][0]["title"] = "WRONG — Automation definition hygiene"
        errors = module.validate_plan(plan)
        self.assertTrue(any("APP_DISPLAY_NAME" in error for error in errors))
        self.assertEqual(original_id, plan["tasks"][0]["task_id"])

    def test_plan_lint_blocks_semantic_duplicates(self) -> None:
        plan = module.build_plan(self.profile([]), "compact")
        duplicate = copy.deepcopy(plan["tasks"][0])
        duplicate["title"] = module.format_visible_title(
            plan["app_display_name"], "Second visible title"
        )
        duplicate["care_title"] = "Second visible title"
        plan["tasks"].append(duplicate)
        errors = module.validate_plan(plan)
        self.assertTrue(any("duplicate task_id" in error for error in errors))
        self.assertTrue(any("semantic_role" in error for error in errors))

    def test_invalid_app_display_name_is_rejected(self) -> None:
        profile = self.profile([])
        profile["app_display_name"] = "CODEX — forged"
        with self.assertRaisesRegex(ValueError, "separator"):
            module.build_plan(profile, "compact")


if __name__ == "__main__":
    unittest.main()
