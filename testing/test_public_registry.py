from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPOSITORY_ROOT / "registry" / "components.json"
PUBLIC_FIELDS = {
    "id",
    "name",
    "type",
    "category",
    "path",
    "version",
    "status",
    "description",
    "languages",
}
PRIVATE_FIELDS = {
    "ownership",
    "privacy",
    "fork",
    "branch",
    "warnings",
    "content_hash",
    "provenance",
    "git_commit",
}


import build_public_registry as registry_builder
from build_public_registry import (
    LANGUAGE_CODES,
    available_languages,
    canonical_core_language_errors,
    list_public_skill_files,
    read_frontmatter,
    serialized_registry,
    unknown_language_variant_errors,
)


class PublicRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_registry_matches_public_skill_tree(self) -> None:
        public_paths = set()
        for path in list_public_skill_files():
            if path.parent.parent.name.startswith("_"):
                continue
            metadata = read_frontmatter(path)
            visibility = str(metadata.get("visibility") or "public").strip().lower()
            if visibility in {"private", "private-only", "private profile", "no-push"}:
                continue
            public_paths.add(path.relative_to(REPOSITORY_ROOT).as_posix())

        registry_paths = {item["path"] for item in self.registry["components"]}
        self.assertEqual(public_paths, registry_paths)
        self.assertEqual(len(public_paths), self.registry["summary"]["component_count"])

    def test_components_expose_only_public_discovery_fields(self) -> None:
        for component in self.registry["components"]:
            self.assertEqual(PUBLIC_FIELDS, set(component))
            self.assertTrue(PRIVATE_FIELDS.isdisjoint(component))

    def test_core_language_audit_requires_flat_de_en_pair(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as temporary:
            root = Path(temporary)
            skill_dir = root / "skills" / "dev" / "example"
            skill_dir.mkdir(parents=True)
            canonical = skill_dir / "SKILL.md"
            canonical.write_text(
                "---\nname: example\nlanguage: en\nvisibility: public\n---\n",
                encoding="utf-8",
            )
            legacy = skill_dir / "EN"
            legacy.mkdir()
            (legacy / "SKILL.md").write_text(
                "---\nname: example\nlanguage: en\n---\n",
                encoding="utf-8",
            )

            errors = canonical_core_language_errors([canonical])

            self.assertEqual(2, len(errors))
            self.assertTrue(any("language: de" in error for error in errors))
            self.assertTrue(any("missing canonical sibling SKILL.en.md" in error for error in errors))

    def test_core_language_audit_accepts_flat_de_en_pair(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as temporary:
            root = Path(temporary)
            skill_dir = root / "skills" / "dev" / "example"
            skill_dir.mkdir(parents=True)
            canonical = skill_dir / "SKILL.md"
            canonical.write_text(
                "---\nname: example\nlanguage: de\nvisibility: public\n---\n",
                encoding="utf-8",
            )
            (skill_dir / "SKILL.en.md").write_text(
                "---\nname: example\nlanguage: en\n---\n",
                encoding="utf-8",
            )

            self.assertEqual([], canonical_core_language_errors([canonical]))

    def test_world_language_files_are_discovered_in_catalog_order(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as temporary:
            skill_dir = Path(temporary) / "example"
            skill_dir.mkdir()
            for code in LANGUAGE_CODES[1:]:
                (skill_dir / f"SKILL.{code}.md").write_text("", encoding="utf-8")

            self.assertEqual(
                list(LANGUAGE_CODES),
                available_languages(skill_dir, {"language": "de"}),
            )

    def test_legacy_language_directories_remain_discoverable(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as temporary:
            skill_dir = Path(temporary) / "example"
            (skill_dir / "FR").mkdir(parents=True)
            (skill_dir / "FR" / "SKILL.md").write_text("", encoding="utf-8")
            (skill_dir / "hi").mkdir()
            (skill_dir / "hi" / "SKILL.md").write_text("", encoding="utf-8")

            self.assertEqual(
                ["de", "fr", "hi"],
                available_languages(skill_dir, {"language": "de"}),
            )

    def test_unknown_language_suffixes_and_legacy_directories_are_reported(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as temporary:
            skill_dir = Path(temporary) / "example"
            skill_dir.mkdir()
            (skill_dir / "SKILL.it.md").write_text("", encoding="utf-8")
            (skill_dir / "IT").mkdir()
            (skill_dir / "IT" / "SKILL.md").write_text("", encoding="utf-8")

            errors = unknown_language_variant_errors(skill_dir)

            self.assertEqual(2, len(errors))
            self.assertTrue(any("SKILL.it.md" in error for error in errors))
            self.assertTrue(any("IT/SKILL.md" in error for error in errors))

    def test_check_becomes_stale_after_world_language_file_is_added(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as temporary:
            root = Path(temporary)
            skill_dir = root / "skills" / "dev" / "example"
            skill_dir.mkdir(parents=True)
            canonical = skill_dir / "SKILL.md"
            canonical.write_text(
                "---\nname: example\ntype: skill\nlanguage: de\nvisibility: public\n---\n",
                encoding="utf-8",
            )
            output = root / "components.json"
            with (
                mock.patch.object(registry_builder, "REPOSITORY_ROOT", root),
                mock.patch.object(
                    registry_builder,
                    "list_public_skill_files",
                    return_value=[canonical],
                ),
            ):
                output.write_text(serialized_registry(), encoding="utf-8")
                (skill_dir / "SKILL.fr.md").write_text("", encoding="utf-8")
                changed_registry = serialized_registry()

            with (
                mock.patch.object(
                    registry_builder,
                    "serialized_registry",
                    return_value=changed_registry,
                ),
                mock.patch.object(
                    registry_builder,
                    "registry_language_errors",
                    return_value=[],
                ),
                mock.patch.object(
                    sys,
                    "argv",
                    ["build_public_registry.py", "--check", "--output", str(output)],
                ),
            ):
                self.assertEqual(1, registry_builder.main())


if __name__ == "__main__":
    unittest.main()
