"""Tests for the provider-neutral semantic routing map builder."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_routing_map.py"
SPEC = importlib.util.spec_from_file_location("build_routing_map", MODULE_PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


class RoutingMapTests(unittest.TestCase):
    def write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def fixture(self, root: Path) -> tuple[Path, Path, Path]:
        roles = root / "roles"
        personas = root / "personas"
        skills = root / "skills"
        self.write(
            roles / "office" / "SKILL.md",
            """---
name: office-coordinator
type: boss-agent
description: >
  Coordinates administrative work.
orchestrates:
  experts: [tax-expert]
---
""",
        )
        self.write(
            roles / "tax" / "SKILL.md",
            """---
name: tax-expert
type: expert
description: Handles employee tax records.
parent_agents: [office-coordinator]
skills: [employee-tax]
---
""",
        )
        self.write(
            personas / "theodor.md",
            """---
name: tax-expert
type: persona
description: Meticulous and precise.
persona:
  display_name: Theodor
  short_name: THEODOR
skills: [employee-tax]
parent_agents: [office-coordinator]
---
""",
        )
        self.write(
            skills / "employee-tax" / "SKILL.md",
            """---
name: employee-tax
description: Organizes employee tax records and receipts.
---
""",
        )
        return roles, personas, skills

    def test_explicit_route_and_persona_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            roles, personas, skills = self.fixture(Path(tmp))
            result = module.build_map(
                module.scan_markdown(roles, "SKILL.md"),
                module.scan_markdown(personas),
                module.scan_markdown(skills, "SKILL.md"),
                3,
            )
            expert = result["roles"]["experts"][0]
            self.assertEqual(
                [{"skill": "employee-tax", "resolution": "explicit"}],
                expert["endpoint_skills"],
            )
            self.assertEqual([], result["gaps"])
            self.assertIn("theodor", result["personas"][0]["id"])

    def test_unresolved_expert_is_a_visible_gap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            roles, personas, skills = self.fixture(Path(tmp))
            tax_file = roles / "tax" / "SKILL.md"
            tax_file.write_text(
                tax_file.read_text(encoding="utf-8").replace(
                    "skills: [employee-tax]\n",
                    "",
                ),
                encoding="utf-8",
            )
            result = module.build_map(
                module.scan_markdown(roles, "SKILL.md"),
                module.scan_markdown(personas),
                [],
                3,
            )
            self.assertEqual(
                [{"expert": "tax-expert", "reason": "no-verified-endpoint"}],
                result["gaps"],
            )

    def test_generic_description_words_do_not_create_candidates(self) -> None:
        expert = {
            "metadata": {
                "name": "funding-planner",
                "description": "Creates documentation and reports",
            }
        }
        skills = [
            {
                "id": "document-sync",
                "name": "document-sync",
                "description": "Creates documentation",
                "category": "utilities",
                "tags": ["documents"],
            }
        ]
        self.assertEqual([], module.lexical_candidates(expert, skills, 3))


if __name__ == "__main__":
    unittest.main()
