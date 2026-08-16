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

    def test_llms_txt_header_and_parity(self) -> None:
        self.assertTrue(LLMS_PATH.is_file(), "llms.txt missing")
        content = LLMS_PATH.read_text(encoding="utf-8")

        self.assertIn("## Last-checked: 2026-08-16", content)
        self.assertIn("ellmos-ai/skills", content)
        self.assertIn("https://github.com/ellmos-ai/skills", content)
        self.assertIn("MIT", content)
        self.assertIn("registry/components.json", content)
        self.assertIn("dev-bricks", content)
        self.assertIn("open-bricks", content)

    def test_readmes_badges_and_crosslinks(self) -> None:
        for readme_path, lang in [(README_EN_PATH, "EN"), (README_DE_PATH, "DE")]:
            self.assertTrue(readme_path.is_file(), f"{readme_path.name} missing")
            content = readme_path.read_text(encoding="utf-8")

            self.assertIn("ellmos-ai/skills", content)
            self.assertIn("open-bricks", content)
            self.assertIn("llms.txt", content)
            self.assertIn("registry/components.json", content)
            self.assertIn("```mermaid", content)

    def test_pyproject_toml_configuration(self) -> None:
        self.assertTrue(PYPROJECT_PATH.is_file(), "pyproject.toml missing")
        content = PYPROJECT_PATH.read_text(encoding="utf-8")

        self.assertIn('name = "ellmos-skills"', content)
        self.assertIn("[tool.pytest.ini_options]", content)
        self.assertIn("[tool.ruff]", content)
        self.assertIn("pythonpath", content)

    def test_changelog_exists_and_updated(self) -> None:
        self.assertTrue(CHANGELOG_PATH.is_file(), "CHANGELOG.md missing")
        content = CHANGELOG_PATH.read_text(encoding="utf-8")
        self.assertIn("2026-08-16", content)


if __name__ == "__main__":
    unittest.main()
