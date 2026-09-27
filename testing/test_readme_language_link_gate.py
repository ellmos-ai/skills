"""Tests for the README skill-link language gate."""

from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("readme_language_link_gate.py")
SPEC = importlib.util.spec_from_file_location("readme_language_link_gate", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)

REPO_ROOT = Path(__file__).resolve().parents[1]


def _init_git_repo(root: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    # A local identity avoids failures on CI runners with no global git config.
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)


def _git_add(root: Path, *relative_paths: str) -> None:
    subprocess.run(["git", "add", *relative_paths], cwd=root, check=True)


def _create_readmes(root: Path, tracked: bool = True) -> None:
    names = list(gate.README_LANGUAGES)
    for readme_name in names:
        (root / readme_name).write_text("", encoding="utf-8")
    if tracked:
        _git_add(root, *names)


class ReadmeLanguageLinkGateTests(unittest.TestCase):
    def test_repository_readmes_match_their_skill_languages(self) -> None:
        violations, checked_links = gate.scan_readmes(REPO_ROOT)
        self.assertEqual([], violations, "\n".join(violations))
        self.assertGreater(checked_links, 0)

    def test_accepts_localized_skill_and_german_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _init_git_repo(root)
            _create_readmes(root)
            translated = root / "skills/dev/translated"
            translated.mkdir(parents=True)
            (translated / "SKILL.md").touch()
            (translated / "SKILL.en.md").touch()
            german_only = root / "skills/utilities/german-only"
            german_only.mkdir(parents=True)
            (german_only / "SKILL.md").touch()
            _git_add(
                root,
                "skills/dev/translated/SKILL.md",
                "skills/dev/translated/SKILL.en.md",
                "skills/utilities/german-only/SKILL.md",
            )

            (root / "README.md").write_text(
                "[Translated](skills/dev/translated/SKILL.en.md)\n", encoding="utf-8"
            )
            (root / "README_de.md").write_text(
                "[Primary](skills/dev/translated/SKILL.md)\n", encoding="utf-8"
            )
            (root / "README_es.md").write_text(
                "[Fallback](skills/utilities/german-only/SKILL.md)\n", encoding="utf-8"
            )
            _git_add(root, "README.md", "README_de.md", "README_es.md")

            violations, checked_links = gate.scan_readmes(root)

        self.assertEqual([], violations, "\n".join(violations))
        self.assertEqual(3, checked_links)

    def test_reports_wrong_language_and_missing_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _init_git_repo(root)
            _create_readmes(root)
            translated = root / "skills/dev/translated"
            translated.mkdir(parents=True)
            (translated / "SKILL.md").touch()
            (translated / "SKILL.en.md").touch()
            german_only = root / "skills/utilities/german-only"
            german_only.mkdir(parents=True)
            (german_only / "SKILL.md").touch()
            _git_add(
                root,
                "skills/dev/translated/SKILL.md",
                "skills/dev/translated/SKILL.en.md",
                "skills/utilities/german-only/SKILL.md",
            )

            (root / "README.md").write_text(
                "[Wrong](skills/dev/translated/SKILL.md)\n", encoding="utf-8"
            )
            (root / "README_ja.md").write_text(
                "[Missing](skills/utilities/german-only/SKILL.ja.md)\n", encoding="utf-8"
            )
            _git_add(root, "README.md", "README_ja.md")

            violations, _ = gate.scan_readmes(root)

        self.assertEqual(2, len(violations), "\n".join(violations))
        self.assertIn("README.md:1", violations[0])
        self.assertIn("SKILL.en.md", violations[0])
        self.assertIn("README_ja.md:1", violations[1])
        self.assertIn("nicht git-getrackt", violations[1])

    def test_untracked_link_target_is_a_violation_even_if_present_on_disk(self) -> None:
        """A file that exists locally but was never `git add`-ed is invisible on
        GitHub -- e.g. a private local-only skill. The gate must fail on it
        exactly like a missing file, not pass because Path.is_file() is true.
        """
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            _init_git_repo(root)
            _create_readmes(root)
            local_only = root / "skills/dev/local-only-private-skill"
            local_only.mkdir(parents=True)
            (local_only / "SKILL.en.md").touch()  # present on disk, NEVER git-added

            (root / "README.md").write_text(
                "[LocalOnly](skills/dev/local-only-private-skill/SKILL.en.md)\n",
                encoding="utf-8",
            )
            _git_add(root, "README.md")

            violations, checked_links = gate.scan_readmes(root)

        self.assertEqual(1, checked_links)
        self.assertEqual(1, len(violations), "\n".join(violations))
        self.assertIn("nicht git-getrackt", violations[0])


if __name__ == "__main__":
    unittest.main()
