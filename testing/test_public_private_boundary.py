"""Regression tests for the neutral public cores created on 2026-07-30."""

from __future__ import annotations

import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
LANGUAGES = {
    "SKILL.md": "de",
    "SKILL.en.md": "en",
    "SKILL.es.md": "es",
    "SKILL.fr.md": "fr",
    "SKILL.ja.md": "ja",
    "SKILL.ru.md": "ru",
    "SKILL.zh.md": "zh",
}
SUPPORTED_LANGUAGES = {
    **LANGUAGES,
    "SKILL.ar.md": "ar",
    "SKILL.bn.md": "bn",
    "SKILL.hi.md": "hi",
    "SKILL.pt.md": "pt",
}
PUBLIC_CORES = [
    "skills/assist/buero",
    "skills/assist/finanz-versicherung",
    "skills/assist/formbuilder-reader",
    "skills/assist/gesundheit",
    "skills/assist/haushalt-manager",
    "skills/assist/hauslagerist-reader",
    "skills/assist/kontaktbuch",
    "skills/assist/mediabrain-reader",
    "skills/assist/notizblock",
    "skills/assist/rpg",
    "skills/assist/voice",
    "skills/education/foerderplaner",
]
PRIVATE_BINDINGS = re.compile(
    r"OfficeHub|VersicherungsManager|FormConstructor|Routinika|"
    r"HausLagerist|MediaBrain|llm-note|RPX|SOVEREIGN|module-installer|"
    r"OneDrive|C:[\\/]Users[\\/]|bericht_template|\.WISSEN",
    re.IGNORECASE,
)


def frontmatter_value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.+)$", text)
    return match.group(1).strip() if match else None


class PublicPrivateBoundaryTests(unittest.TestCase):
    def test_every_public_core_has_complete_language_set(self) -> None:
        for relative in PUBLIC_CORES:
            skill_dir = REPOSITORY_ROOT / relative
            with self.subTest(skill=relative):
                actual = {path.name for path in skill_dir.glob("SKILL*.md")}
                self.assertLessEqual(set(LANGUAGES), actual, "Required core language missing")
                self.assertLessEqual(actual, set(SUPPORTED_LANGUAGES), "Unknown skill language filename")

    def test_language_frontmatter_matches_filename(self) -> None:
        for relative in PUBLIC_CORES:
            for path in (REPOSITORY_ROOT / relative).glob("SKILL*.md"):
                with self.subTest(path=path):
                    self.assertIn(path.name, SUPPORTED_LANGUAGES)
                    text = path.read_text(encoding="utf-8")
                    self.assertEqual(SUPPORTED_LANGUAGES[path.name], frontmatter_value(text, "language"))
                    self.assertEqual("2.0.0", frontmatter_value(text, "version"))
                    self.assertEqual("true", frontmatter_value(text, "standalone"))

    def test_private_bindings_are_absent_from_public_bodies(self) -> None:
        for relative in PUBLIC_CORES:
            for path in (REPOSITORY_ROOT / relative).glob("SKILL*.md"):
                body = re.sub(
                    r"^---\s*\n.*?\n---\s*\n",
                    "",
                    path.read_text(encoding="utf-8"),
                    count=1,
                    flags=re.DOTALL,
                )
                body = re.sub(
                    r'(?m)^\s*<img src="banner\.png"[^>]*>\s*$',
                    "",
                    body,
                )
                with self.subTest(path=path):
                    self.assertIsNone(PRIVATE_BINDINGS.search(body))

    def test_foerderplaner_is_planning_only(self) -> None:
        path = REPOSITORY_ROOT / "skills/education/foerderplaner/SKILL.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("Unterrichts- und Förderplaner", text)
        self.assertIn("report-forge", text)
        self.assertNotIn("report-generator", text)
        self.assertNotIn("anonymizer", text)


class LanguageBoundaryCountercases(unittest.TestCase):
    def setUp(self) -> None:
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.skill = self.root / "fixture"
        self.skill.mkdir()
        for filename, language in LANGUAGES.items():
            self.write_skill(filename, language)

    def write_skill(self, filename: str, language: str, body: str = "Neutral public guidance.") -> None:
        (self.skill / filename).write_text(
            f"---\nlanguage: {language}\nversion: 2.0.0\nstandalone: true\n---\n{body}\n",
            encoding="utf-8",
        )

    def run_gate(self, method: str) -> unittest.TestResult:
        result = unittest.TestResult()
        with patch.dict(globals(), {"REPOSITORY_ROOT": self.root, "PUBLIC_CORES": ["fixture"]}):
            PublicPrivateBoundaryTests(method).run(result)
        return result

    def test_known_additional_languages_are_accepted(self) -> None:
        for language in ("ar", "bn", "hi", "pt"):
            with self.subTest(language=language):
                self.write_skill(f"SKILL.{language}.md", language)
                result = self.run_gate("test_every_public_core_has_complete_language_set")
                self.assertTrue(result.wasSuccessful(), result.failures + result.errors)

    def test_required_language_cannot_disappear(self) -> None:
        (self.skill / "SKILL.en.md").unlink()
        self.assertFalse(self.run_gate("test_every_public_core_has_complete_language_set").wasSuccessful())

    def test_unknown_language_filename_is_rejected(self) -> None:
        self.write_skill("SKILL.unknown.md", "unknown")
        self.assertFalse(self.run_gate("test_every_public_core_has_complete_language_set").wasSuccessful())

    def test_additional_language_frontmatter_is_checked(self) -> None:
        self.write_skill("SKILL.ar.md", "en")
        self.assertFalse(self.run_gate("test_language_frontmatter_matches_filename").wasSuccessful())

    def test_additional_language_private_binding_is_rejected(self) -> None:
        self.write_skill("SKILL.ar.md", "ar", PRIVATE_BINDINGS.pattern.split("|")[0])
        self.assertFalse(self.run_gate("test_private_bindings_are_absent_from_public_bodies").wasSuccessful())


if __name__ == "__main__":
    unittest.main()
