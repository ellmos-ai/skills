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
    DEFAULT_SOURCE_MANIFEST,
    LANGUAGE_CODES,
    SourceManifestError,
    available_languages,
    build_registry,
    canonical_core_language_errors,
    git_skill_artifacts,
    list_public_skill_files,
    read_frontmatter,
    resolve_source_files,
    serialized_registry,
    serialized_source_manifest,
    unknown_language_variant_errors,
    validate_source_manifest,
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

    def test_versioned_source_manifest_matches_git_authority(self) -> None:
        tracked = git_skill_artifacts()
        self.assertIsNotNone(tracked)
        self.assertEqual(
            serialized_source_manifest(tracked),
            DEFAULT_SOURCE_MANIFEST.read_text(encoding="utf-8"),
        )

    def test_gitless_public_archive_uses_versioned_source_manifest(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as temporary:
            root = Path(temporary)
            canonical = self._write_example_skill(root, "example")
            english = canonical.parent / "SKILL.en.md"
            english.write_text("---\nname: example\nlanguage: en\n---\n", encoding="utf-8")
            files = [
                "skills/dev/example/SKILL.en.md",
                "skills/dev/example/SKILL.md",
            ]
            manifest = root / "registry" / "public-skill-files.json"
            manifest.parent.mkdir()
            manifest.write_text(serialized_source_manifest(files), encoding="utf-8")

            with self._gitless_root(root):
                resolved, authority = resolve_source_files()
                registry = build_registry(resolved)

            self.assertEqual("manifest", authority)
            self.assertEqual(files, resolved)
            self.assertEqual(1, registry["summary"]["component_count"])
            self.assertEqual(["de", "en"], registry["components"][0]["languages"])

    def test_gitless_enriched_projection_ignores_unmanifested_extras(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as temporary:
            root = Path(temporary)
            self._write_example_skill(root, "public-example")
            self._write_example_skill(root, "projection-only")
            files = ["skills/dev/public-example/SKILL.md"]
            manifest = root / "registry" / "public-skill-files.json"
            manifest.parent.mkdir()
            manifest.write_text(serialized_source_manifest(files), encoding="utf-8")

            with self._gitless_root(root):
                resolved, authority = resolve_source_files()
                registry = build_registry(resolved)

            self.assertEqual("manifest", authority)
            self.assertEqual(["public-example"], [item["name"] for item in registry["components"]])

    def test_source_manifest_rejects_missing_manifested_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as temporary:
            root = Path(temporary)
            files = ["skills/dev/missing/SKILL.md"]
            manifest = root / "registry" / "public-skill-files.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(serialized_source_manifest(files), encoding="utf-8")

            with self.assertRaisesRegex(SourceManifestError, "missing manifested file"):
                validate_source_manifest(manifest, repository_root=root)

    def test_source_manifest_rejects_unsafe_path(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as temporary:
            root = Path(temporary)
            manifest = root / "registry" / "public-skill-files.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": "public-skill-files-v1",
                        "generated_by": "build_public_registry.py",
                        "file_count": 1,
                        "files": ["skills/dev/../../private/SKILL.md"],
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(SourceManifestError, "unsafe or irrelevant"):
                validate_source_manifest(manifest, repository_root=root)

    def test_source_manifest_detects_git_authority_drift(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as temporary:
            root = Path(temporary)
            canonical = self._write_example_skill(root, "example")
            files = ["skills/dev/example/SKILL.md"]
            manifest = root / "registry" / "public-skill-files.json"
            manifest.parent.mkdir()
            manifest.write_text(serialized_source_manifest(files), encoding="utf-8")
            self.assertTrue(canonical.is_file())

            with self.assertRaisesRegex(SourceManifestError, "does not match git authority"):
                validate_source_manifest(
                    manifest,
                    repository_root=root,
                    expected_files=files + ["skills/dev/new-public/SKILL.md"],
                )

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

    def test_check_fails_when_git_authority_adds_public_language_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as temporary:
            root = Path(temporary)
            skill_dir = root / "skills" / "dev" / "example"
            skill_dir.mkdir(parents=True)
            canonical = skill_dir / "SKILL.md"
            canonical.write_text(
                "---\nname: example\ntype: skill\nlanguage: de\nvisibility: public\n---\n",
                encoding="utf-8",
            )
            manifest = root / "registry" / "public-skill-files.json"
            manifest.parent.mkdir()
            initial_files = ["skills/dev/example/SKILL.md"]
            manifest.write_text(
                serialized_source_manifest(initial_files),
                encoding="utf-8",
            )
            output = root / "components.json"
            output.write_text(
                serialized_registry(initial_files, repository_root=root),
                encoding="utf-8",
            )
            french = skill_dir / "SKILL.fr.md"
            french.write_text("---\nname: example\nlanguage: fr\n---\n", encoding="utf-8")
            changed_files = initial_files + ["skills/dev/example/SKILL.fr.md"]

            with (
                mock.patch.object(
                    registry_builder,
                    "REPOSITORY_ROOT",
                    root,
                ),
                mock.patch.object(
                    registry_builder,
                    "SKILLS_ROOT",
                    root / "skills",
                ),
                mock.patch.object(
                    registry_builder,
                    "git_skill_artifacts",
                    return_value=changed_files,
                ),
                mock.patch.object(
                    sys,
                    "argv",
                    [
                        "build_public_registry.py",
                        "--check",
                        "--output",
                        str(output),
                        "--source-manifest",
                        str(manifest),
                    ],
                ),
            ):
                self.assertEqual(1, registry_builder.main())

    @staticmethod
    def _write_example_skill(root: Path, name: str) -> Path:
        canonical = root / "skills" / "dev" / name / "SKILL.md"
        canonical.parent.mkdir(parents=True)
        canonical.write_text(
            "---\n"
            f"name: {name}\n"
            "type: skill\n"
            "version: 1.0.0\n"
            "language: de\n"
            "visibility: public\n"
            "description: Example\n"
            "---\n",
            encoding="utf-8",
        )
        return canonical

    @staticmethod
    def _gitless_root(root: Path):
        return _GitlessRoot(root)


class _GitlessRoot:
    def __init__(self, root: Path) -> None:
        self._patches = [
            mock.patch.object(registry_builder, "REPOSITORY_ROOT", root),
            mock.patch.object(registry_builder, "SKILLS_ROOT", root / "skills"),
            mock.patch.object(registry_builder, "git_skill_artifacts", return_value=None),
        ]

    def __enter__(self):
        for patcher in self._patches:
            patcher.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        for patcher in reversed(self._patches):
            patcher.stop()


if __name__ == "__main__":
    unittest.main()
