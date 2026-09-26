"""Tests for the README skill-link language gate."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("readme_language_link_gate.py")
SPEC = importlib.util.spec_from_file_location("readme_language_link_gate", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)

REPO_ROOT = Path(__file__).resolve().parents[1]


def _create_readmes(root: Path) -> None:
    for readme_name in gate.README_LANGUAGES:
        (root / readme_name).write_text("", encoding="utf-8")


class ReadmeLanguageLinkGateTests(unittest.TestCase):
    def test_repository_readmes_match_their_skill_languages(self) -> None:
        violations, checked_links = gate.scan_readmes(REPO_ROOT)
        self.assertEqual([], violations, "\n".join(violations))
        self.assertGreater(checked_links, 0)

    def test_accepts_localized_skill_and_german_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _create_readmes(root)
            translated = root / "skills/dev/translated"
            translated.mkdir(parents=True)
            (translated / "SKILL.md").touch()
            (translated / "SKILL.en.md").touch()
            german_only = root / "skills/utilities/german-only"
            german_only.mkdir(parents=True)
            (german_only / "SKILL.md").touch()

            (root / "README.md").write_text(
                "[Translated](skills/dev/translated/SKILL.en.md)\n", encoding="utf-8"
            )
            (root / "README_de.md").write_text(
                "[Primary](skills/dev/translated/SKILL.md)\n", encoding="utf-8"
            )
            (root / "README_es.md").write_text(
                "[Fallback](skills/utilities/german-only/SKILL.md)\n", encoding="utf-8"
            )

            violations, checked_links = gate.scan_readmes(root)

        self.assertEqual([], violations, "\n".join(violations))
        self.assertEqual(3, checked_links)

    def test_reports_wrong_language_and_missing_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _create_readmes(root)
            translated = root / "skills/dev/translated"
            translated.mkdir(parents=True)
            (translated / "SKILL.md").touch()
            (translated / "SKILL.en.md").touch()
            german_only = root / "skills/utilities/german-only"
            german_only.mkdir(parents=True)
            (german_only / "SKILL.md").touch()

            (root / "README.md").write_text(
                "[Wrong](skills/dev/translated/SKILL.md)\n", encoding="utf-8"
            )
            (root / "README_ja.md").write_text(
                "[Missing](skills/utilities/german-only/SKILL.ja.md)\n", encoding="utf-8"
            )

            violations, _ = gate.scan_readmes(root)

        self.assertEqual(2, len(violations), "\n".join(violations))
        self.assertIn("README.md:1", violations[0])
        self.assertIn("SKILL.en.md", violations[0])
        self.assertIn("README_ja.md:1", violations[1])
        self.assertIn("Zieldatei fehlt", violations[1])


if __name__ == "__main__":
    unittest.main()
