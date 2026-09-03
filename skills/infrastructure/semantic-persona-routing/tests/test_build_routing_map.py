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

    def test_duplicate_skill_ids_choose_a_deterministic_source_and_issue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            roles, personas, skills = self.fixture(Path(tmp))
            self.write(
                skills / "translations" / "SKILL.md",
                """---
name: employee-tax
description: Localized duplicate that must not create a second ID.
---
""",
            )
            result = module.build_map(
                module.scan_markdown(roles, "SKILL.md"),
                module.scan_markdown(personas),
                list(reversed(module.scan_markdown(skills, "SKILL.md"))),
                3,
            )
            self.assertEqual(["employee-tax"], [skill["id"] for skill in result["skills"]])
            self.assertEqual(
                [
                    {
                        "kind": "duplicate-skill-id",
                        "skill": "employee-tax",
                        "canonical_source_ref": "employee-tax/SKILL.md",
                        "duplicate_source_refs": ["translations/SKILL.md"],
                    }
                ],
                [issue for issue in result["issues"] if issue["kind"] == "duplicate-skill-id"],
            )

    def test_invalid_source_skill_id_is_skipped_with_safe_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            roles, personas, skills = self.fixture(Path(tmp))
            self.write(
                skills / "invalid" / "SKILL.md",
                """---
name: ###
description: Must never become an empty stable ID.
---
""",
            )
            self.write(
                skills / "not-stable" / "SKILL.md",
                """---
name: Employee Tax
description: Whitespace is not a stable exported ID.
---
""",
            )
            result = module.build_map(
                module.scan_markdown(roles, "SKILL.md"),
                module.scan_markdown(personas),
                module.scan_markdown(skills, "SKILL.md"),
                3,
            )
            self.assertEqual(["employee-tax"], [skill["id"] for skill in result["skills"]])
            self.assertTrue(all(skill["id"] for skill in result["skills"]))
            self.assertIn(
                {
                    "kind": "invalid-skill-id",
                    "source_ref": "invalid/SKILL.md",
                    "reference": "###",
                },
                result["issues"],
            )
            self.assertIn(
                {
                    "kind": "invalid-skill-id",
                    "source_ref": "not-stable/SKILL.md",
                    "reference": "Employee Tax",
                },
                result["issues"],
            )

    def test_persona_reference_is_normalized_only_when_the_skill_is_known(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            roles, personas, skills = self.fixture(Path(tmp))
            persona_file = personas / "theodor.md"
            persona_file.write_text(
                persona_file.read_text(encoding="utf-8").replace(
                    "skills: [employee-tax]",
                    "skills: ['employee-tax    # system/skills/employee-tax/SKILL.md']",
                ),
                encoding="utf-8",
            )
            result = module.build_map(
                module.scan_markdown(roles, "SKILL.md"),
                module.scan_markdown(personas),
                module.scan_markdown(skills, "SKILL.md"),
                3,
            )
            self.assertEqual(["employee-tax"], result["personas"][0]["skills"])
            self.assertIn(
                {
                    "kind": "normalized-skill-reference",
                    "owner_kind": "persona",
                    "owner": "theodor",
                    "reference": "employee-tax    # system/skills/employee-tax/SKILL.md",
                    "normalized": "employee-tax",
                },
                result["issues"],
            )

    def test_unknown_or_empty_persona_references_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            roles, personas, skills = self.fixture(Path(tmp))
            persona_file = personas / "theodor.md"
            persona_file.write_text(
                persona_file.read_text(encoding="utf-8").replace(
                    "skills: [employee-tax]",
                    "skills: ['unknown-skill', '  # annotation only']",
                ),
                encoding="utf-8",
            )
            result = module.build_map(
                module.scan_markdown(roles, "SKILL.md"),
                module.scan_markdown(personas),
                module.scan_markdown(skills, "SKILL.md"),
                3,
            )
            self.assertEqual([], result["personas"][0]["skills"])
            self.assertIn(
                {
                    "kind": "unknown-skill-reference",
                    "owner_kind": "persona",
                    "owner": "theodor",
                    "reference": "unknown-skill",
                    "normalized": "unknown-skill",
                },
                result["issues"],
            )
            self.assertIn(
                {
                    "kind": "invalid-skill-reference",
                    "owner_kind": "persona",
                    "owner": "theodor",
                    "reference": "  # annotation only",
                },
                result["issues"],
            )

class CatalogLayoutTests(unittest.TestCase):
    def write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def skill(self, name: str) -> str:
        return f"---\nname: {name}\ntype: skill\ndescription: Example skill {name}.\n---\n"

    def test_catalog_layout_keeps_one_canonical_file_per_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            self.write(root / "dev" / "employee-tax" / "SKILL.md", self.skill("employee-tax"))
            self.write(root / "_archive" / "dev" / "employee-tax" / "SKILL.md", self.skill("employee-tax"))
            self.write(root / "_reference" / "vendor-tool" / "SKILL.md", self.skill("vendor-tool"))
            self.write(root / "dev" / "employee-tax" / "_templates" / "SKILL.md", self.skill("employee-tax"))
            self.write(root / "dev" / "employee-tax" / "nested" / "SKILL.md", self.skill("employee-tax"))
            recursive = module.scan_markdown(root, "SKILL.md")
            catalog = module.scan_markdown(root, "SKILL.md", layout="catalog")
        self.assertEqual(5, len(recursive))
        self.assertEqual(["dev/employee-tax/SKILL.md"], [r["source_ref"] for r in catalog])
        self.assertTrue(module.is_catalog_path(module.PurePosixPath("dev/employee-tax/SKILL.md")))
        self.assertFalse(module.is_catalog_path(module.PurePosixPath("_archive/dev/employee-tax/SKILL.md")))
        self.assertFalse(module.is_catalog_path(module.PurePosixPath("dev/SKILL.md")))

    def test_catalog_layout_removes_duplicate_id_issues_from_the_map(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            self.write(root / "dev" / "employee-tax" / "SKILL.md", self.skill("employee-tax"))
            self.write(root / "_archive" / "old" / "employee-tax" / "SKILL.md", self.skill("employee-tax"))
            noisy = module.build_map([], [], module.scan_markdown(root, "SKILL.md"), 3)
            clean = module.build_map([], [], module.scan_markdown(root, "SKILL.md", layout="catalog"), 3)
        self.assertTrue(any(issue["kind"] == "duplicate-skill-id" for issue in noisy["issues"]))
        self.assertEqual([], [issue for issue in clean["issues"] if issue["kind"] == "duplicate-skill-id"])

    def test_unknown_layout_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            module.scan_markdown(Path("."), "SKILL.md", layout="flat")


if __name__ == "__main__":
    unittest.main()
