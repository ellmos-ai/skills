from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

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


from build_public_registry import (
    canonical_core_language_errors,
    list_public_skill_files,
    read_frontmatter,
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


if __name__ == "__main__":
    unittest.main()
