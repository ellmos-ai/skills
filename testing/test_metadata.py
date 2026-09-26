from __future__ import annotations

import json
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPOSITORY_ROOT / "registry" / "components.json"
LLMS_PATH = REPOSITORY_ROOT / "llms.txt"
README_EN_PATH = REPOSITORY_ROOT / "README.md"
README_DE_PATH = REPOSITORY_ROOT / "README_de.md"
PYPROJECT_PATH = REPOSITORY_ROOT / "pyproject.toml"
CHANGELOG_PATH = REPOSITORY_ROOT / "CHANGELOG.md"
SECURITY_PATH = REPOSITORY_ROOT / "SECURITY.md"
CI_WORKFLOW_PATH = REPOSITORY_ROOT / ".github" / "workflows" / "tests.yml"
SKILL_VAL_PATH = REPOSITORY_ROOT / ".github" / "workflows" / "skill-validation.yml"
ASSIST_SCHEMA_PATH = REPOSITORY_ROOT / "schemas" / "assist-v1.schema.json"
THIRD_PARTY_LICENSES_PATH = REPOSITORY_ROOT / "THIRD_PARTY_LICENSES.md"
NOTICE_PATH = REPOSITORY_ROOT / "NOTICE"


class MetadataAndManifestParityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertTrue(REGISTRY_PATH.is_file(), f"Registry file {REGISTRY_PATH} missing")
        self.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_registry_structure_and_components_exist(self) -> None:
        self.assertIn("summary", self.registry)
        self.assertIn("components", self.registry)

        summary = self.registry["summary"]
        self.assertEqual(summary.get("schema_version"), "public-catalog-v1")
        self.assertEqual(summary.get("component_count"), len(self.registry["components"]))

        # Verify all categories tally correctly
        cat_counts = summary.get("categories", {})
        total_from_cats = sum(cat_counts.values())
        self.assertEqual(total_from_cats, summary.get("component_count"))

        # Verify each component has mandatory public fields and existing file
        required_fields = {"id", "name", "type", "category", "path", "version", "status", "description", "languages"}
        for comp in self.registry["components"]:
            for field in required_fields:
                self.assertIn(field, comp, f"Component {comp.get('id')} missing required field '{field}'")

            skill_path = REPOSITORY_ROOT / comp["path"]
            self.assertTrue(skill_path.is_file(), f"Skill file {skill_path} does not exist on disk")
            self.assertTrue(comp["languages"], f"Component {comp.get('id')} has empty language list")

    def test_assist_type_is_allowed_by_referenced_component_schema(self) -> None:
        assist_schema = json.loads(ASSIST_SCHEMA_PATH.read_text(encoding="utf-8"))
        component_ref = assist_schema["allOf"][0]["$ref"]
        assist_type = assist_schema["allOf"][1]["properties"]["type"]["const"]
        component_schema = json.loads(
            (ASSIST_SCHEMA_PATH.parent / component_ref).read_text(encoding="utf-8")
        )

        self.assertIn(assist_type, component_schema["properties"]["type"]["enum"])

    def test_security_policy_integrity(self) -> None:
        self.assertTrue(SECURITY_PATH.is_file(), "SECURITY.md missing")
        content = SECURITY_PATH.read_text(encoding="utf-8")

        # Bilingual structure
        self.assertIn("## English", content)
        self.assertIn("## Deutsch", content)

        # Core security guarantees
        self.assertIn("Zero-Egress", content)
        self.assertIn("Fail-Closed Privacy Boundary", content)
        self.assertIn("Non-Elevation", content)
        self.assertIn("security@ellmos.ai", content)
        self.assertIn("support@lukasgeiger.com", content)
        self.assertIn("github.com/ellmos-ai/skills/security/advisories", content)
        self.assertIn("THIRD_PARTY_LICENSES.md", content)

    def test_ci_workflows_integrity(self) -> None:
        self.assertTrue(CI_WORKFLOW_PATH.is_file(), ".github/workflows/tests.yml missing")
        tests_content = CI_WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn("actions/checkout@v4", tests_content)
        self.assertIn("actions/setup-python@v5", tests_content)
        self.assertIn("ubuntu-latest", tests_content)
        self.assertIn("windows-latest", tests_content)
        self.assertIn("macos-latest", tests_content)
        self.assertIn('"3.10"', tests_content)
        self.assertIn('"3.13"', tests_content)
        self.assertIn("ruff check .", tests_content)
        self.assertIn("python -m pytest", tests_content)
        self.assertIn("testing/privacy_gate.py", tests_content)

        self.assertTrue(SKILL_VAL_PATH.is_file(), ".github/workflows/skill-validation.yml missing")

    def test_pyproject_toml_configuration_and_pep621(self) -> None:
        self.assertTrue(PYPROJECT_PATH.is_file(), "pyproject.toml missing")
        content = PYPROJECT_PATH.read_text(encoding="utf-8")

        self.assertIn('name = "ellmos-skills"', content)
        self.assertIn('version = "1.4.4"', content)
        self.assertIn('license-files = ["LICENSE", "NOTICE", "THIRD_PARTY_LICENSES.md"]', content)
        self.assertIn("[tool.pytest.ini_options]", content)
        self.assertIn('minversion = "7.0"', content)
        self.assertIn("norecursedirs", content)
        self.assertIn('addopts = "-ra -v"', content)
        self.assertIn("[tool.ruff]", content)
        self.assertIn("pythonpath", content)
        self.assertIn("Programming Language :: Python :: 3.13", content)
        self.assertIn("Operating System :: OS Independent", content)
        self.assertIn('"zero-egress"', content)
        self.assertIn("[project.urls]", content)
        self.assertIn("Homepage", content)
        self.assertIn("Security", content)
        self.assertIn("Notice", content)
        self.assertIn("Changelog", content)
        self.assertIn("Parent Organization", content)
        self.assertIn("Umbrella Ecosystem", content)
        self.assertIn("Third-Party Licenses", content)
        self.assertIn("LLM Context", content)

    def test_llms_txt_header_and_parity(self) -> None:
        self.assertTrue(LLMS_PATH.is_file(), "llms.txt missing")
        content = LLMS_PATH.read_text(encoding="utf-8")

        self.assertIn("## Last-checked: 2026-09-24", content)
        self.assertIn("305 passing pytest tests", content)
        self.assertIn("ellmos-ai/skills", content)
        self.assertIn("https://github.com/ellmos-ai/skills", content)
        self.assertIn("MIT", content)
        self.assertIn("registry/components.json", content)
        self.assertIn("SECURITY.md", content)
        self.assertIn("NOTICE", content)
        self.assertIn("THIRD_PARTY_LICENSES.md", content)
        self.assertIn("dev-bricks", content)
        self.assertIn("open-bricks", content)

    def test_readmes_badges_and_crosslinks(self) -> None:
        for readme_path, lang in [(README_EN_PATH, "EN"), (README_DE_PATH, "DE")]:
            self.assertTrue(readme_path.is_file(), f"{readme_path.name} missing")
            content = readme_path.read_text(encoding="utf-8")

            self.assertIn("ellmos-ai/skills", content)
            self.assertIn("open-bricks", content)
            self.assertIn("llms.txt", content)
            self.assertIn("SECURITY.md", content)
            self.assertIn("NOTICE", content)
            self.assertIn("THIRD_PARTY_LICENSES.md", content)
            self.assertIn("registry/components.json", content)
            self.assertIn("```mermaid", content)
            self.assertIn("1.4.4", content)
            self.assertIn("305", content)
            self.assertIn("142", content)
            self.assertIn("2026-09-24", content)

    def test_changelog_exists_and_updated(self) -> None:
        self.assertTrue(CHANGELOG_PATH.is_file(), "CHANGELOG.md missing")
        content = CHANGELOG_PATH.read_text(encoding="utf-8")
        self.assertIn("## [Unreleased] - 2026-09-24", content)
        self.assertIn("T-20260920-167562623", content)
        self.assertIn("2026-09-20", content)
        self.assertIn("1.4.4", content)
        self.assertIn("2026-09-13", content)
        self.assertIn("1.4.3", content)
        self.assertIn("2026-09-11", content)
        self.assertIn("1.4.2", content)

    def test_gitignore_hygiene(self) -> None:
        gitignore_path = REPOSITORY_ROOT / ".gitignore"
        self.assertTrue(gitignore_path.is_file(), ".gitignore missing")
        content = gitignore_path.read_text(encoding="utf-8")
        self.assertIn("*-conflict-*", content)
        self.assertIn("*.sync-conflict-*", content)
        self.assertIn("*conflicted copy*", content)
        self.assertIn("LOCK.*", content)
        self.assertIn("LOCK.user.*", content)
        self.assertIn("LOCK.condition.*", content)
        self.assertIn("LOCK.permissions.json", content)
        self.assertIn(".automation-lock", content)
        self.assertIn("!package-lock.json", content)
        self.assertIn("uv.lock", content)
        self.assertIn(".coverage.*", content)
        self.assertIn(".hypothesis/", content)

    def test_ci_workflow_extended_gates(self) -> None:
        content = CI_WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn("concurrency:", content)
        self.assertIn("cancel-in-progress: true", content)
        self.assertIn("timeout-minutes: 15", content)
        self.assertIn("python -m compileall -q testing skills", content)
        self.assertIn("python -m pytest -ra -v", content)

    def test_security_supported_versions(self) -> None:
        content = SECURITY_PATH.read_text(encoding="utf-8")
        self.assertIn("1.4.x", content)

    def test_target_personas_discoverability_parity(self) -> None:
        en_content = README_EN_PATH.read_text(encoding="utf-8")
        de_content = README_DE_PATH.read_text(encoding="utf-8")

        self.assertIn("#target-personas--discoverability", en_content)
        self.assertIn("Autonomous AI Agents & Swarms", en_content)
        self.assertIn("Enterprise DevOps & Platform Engineers", en_content)
        self.assertIn("Local-First, Privacy & SecOps Specialists", en_content)
        self.assertIn("Domain Skill Authors & Research Engineers", en_content)

        self.assertIn("#zielgruppen--auffindbarkeit", de_content)
        self.assertIn("Autonome KI-Agenten & Multi-Agenten-Schwärme", de_content)
        self.assertIn("Enterprise DevOps & Platform Engineers", de_content)
        self.assertIn("Local-First, Privacy & SecOps Spezialisten", de_content)
        self.assertIn("Domain Skill Autoren & Research Engineers", de_content)

    def test_comparative_matrix_parity(self) -> None:
        en_content = README_EN_PATH.read_text(encoding="utf-8")
        de_content = README_DE_PATH.read_text(encoding="utf-8")

        self.assertIn("#comparative-matrix-vs-alternatives", en_content)
        self.assertIn("Ad-Hoc System Prompts", en_content)
        self.assertIn("Tool/Function Calling Only", en_content)
        self.assertIn("Centralized Cloud Hubs", en_content)
        self.assertIn("Heavyweight Frameworks (LangChain/CrewAI)", en_content)

        self.assertIn("#vergleichsmatrix-gegenueber-alternativen", de_content)
        self.assertIn("Ad-hoc System-Prompts", de_content)
        self.assertIn("Tool/Function-Calling ohne Playbooks", de_content)
        self.assertIn("Zentrale Cloud-Hubs", de_content)
        self.assertIn("Schwergewichtige Frameworks (LangChain/CrewAI)", de_content)

    def test_third_party_licenses_inventory_and_invariants(self) -> None:
        self.assertTrue(THIRD_PARTY_LICENSES_PATH.is_file(), "THIRD_PARTY_LICENSES.md missing")
        content = THIRD_PARTY_LICENSES_PATH.read_text(encoding="utf-8")

        self.assertIn("0% Copyleft", content)
        self.assertIn("ZERO external runtime dependencies", content)
        self.assertIn("**Audit Date:** 2026-09-20", content)
        self.assertIn("Pfad A Technical Hygiene", content)
        for i in range(1, 11):
            inv_prefix = "INV-"
            self.assertTrue(any(line.startswith(f"| **{inv_prefix}") for line in content.splitlines()), "Invariant missing")

        invariants = [
            "INV-LOCAL-01",
            "INV-PRIVACY-02",
            "INV-UNPRIV-03",
            "INV-SCHEMA-04",
            "INV-ISOLATION-05",
            "INV-PORTABLE-06",
            "INV-DISCOVERY-07",
            "INV-PLATFORM-08",
            "INV-SYNC-09",
            "INV-SLA-10",
        ]
        for inv in invariants:
            self.assertIn(inv, content, f"Invariant {inv} missing in THIRD_PARTY_LICENSES.md")
            self.assertTrue(any(f"| **{inv}**" in line for line in content.splitlines()), f"Invariant table row missing for {inv}")


    def test_ci_job_timeouts_and_concurrency_across_all_workflows(self) -> None:
        workflow_dir = REPOSITORY_ROOT / ".github" / "workflows"
        self.assertTrue(workflow_dir.is_dir(), ".github/workflows missing")
        for yml_file in workflow_dir.glob("*.yml"):
            content = yml_file.read_text(encoding="utf-8")
            self.assertIn(
                "timeout-minutes:",
                content,
                f"Workflow {yml_file.name} missing timeout-minutes runaway protection",
            )

    def test_pep621_license_files_and_distribution_assets(self) -> None:
        license_path = REPOSITORY_ROOT / "LICENSE"
        self.assertTrue(license_path.is_file(), "LICENSE missing")
        self.assertTrue(NOTICE_PATH.is_file(), "NOTICE missing")
        self.assertTrue(THIRD_PARTY_LICENSES_PATH.is_file(), "THIRD_PARTY_LICENSES.md missing")
        pyproject_content = PYPROJECT_PATH.read_text(encoding="utf-8")
        self.assertIn('license-files = ["LICENSE", "NOTICE", "THIRD_PARTY_LICENSES.md"]', pyproject_content)

    def test_notice_file_integrity(self) -> None:
        self.assertTrue(NOTICE_PATH.is_file(), "NOTICE file missing")
        content = NOTICE_PATH.read_text(encoding="utf-8")
        self.assertIn("ellmos-skills", content)
        self.assertIn("Copyright (c) 2026 Lukas Geiger", content)
        self.assertIn("ellmos-ai", content)
        self.assertIn("open-bricks", content)
        self.assertIn("THIRD_PARTY_LICENSES.md", content)

    def test_mermaid_architecture_metrics_parity(self) -> None:
        en_content = README_EN_PATH.read_text(encoding="utf-8")
        de_content = README_DE_PATH.read_text(encoding="utf-8")

        self.assertIn('Registry["Public Skill Registry (142 Catalog / 380 Tracked)"]', en_content)
        self.assertIn('Registry["Öffentliche Skill-Registry (142 Katalog / 380 getrackt)"]', de_content)

        for content in [en_content, de_content]:
            self.assertIn('Dev["dev (25)"]', content)
            self.assertIn('Infra["infrastructure (32)"]', content)
            self.assertIn('Utils["utilities (29)"]', content)
            self.assertIn("305", content)

    def test_quick_navigation_and_mutual_anchor_parity(self) -> None:
        en_content = README_EN_PATH.read_text(encoding="utf-8")
        de_content = README_DE_PATH.read_text(encoding="utf-8")

        en_nav_lines = [
            line.strip()
            for line in en_content.split("## Quick Navigation")[1].split("---")[0].splitlines()
            if line.strip().startswith("- [")
        ]
        de_nav_lines = [
            line.strip()
            for line in de_content.split("## Schnellnavigation")[1].split("---")[0].splitlines()
            if line.strip().startswith("- [")
        ]

        self.assertEqual(len(en_nav_lines), 16, f"Expected 16 Quick Navigation points in EN, got {len(en_nav_lines)}")
        self.assertEqual(len(de_nav_lines), 16, f"Expected 16 Schnellnavigation points in DE, got {len(de_nav_lines)}")


if __name__ == "__main__":
    unittest.main()
