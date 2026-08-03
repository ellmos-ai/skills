from __future__ import annotations

import json
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


from build_public_registry import read_frontmatter


class PublicRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_registry_matches_public_skill_tree(self) -> None:
        public_paths = set()
        for path in (REPOSITORY_ROOT / "skills").glob("*/*/SKILL.md"):
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


if __name__ == "__main__":
    unittest.main()
