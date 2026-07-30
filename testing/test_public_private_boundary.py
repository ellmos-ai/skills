"""Regression tests for the neutral public cores created on 2026-07-30."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


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
                self.assertEqual(set(LANGUAGES), {path.name for path in skill_dir.glob("SKILL*.md")})

    def test_language_frontmatter_matches_filename(self) -> None:
        for relative in PUBLIC_CORES:
            for filename, language in LANGUAGES.items():
                path = REPOSITORY_ROOT / relative / filename
                with self.subTest(path=path):
                    text = path.read_text(encoding="utf-8")
                    self.assertEqual(language, frontmatter_value(text, "language"))
                    self.assertEqual("2.0.0", frontmatter_value(text, "version"))
                    self.assertEqual("true", frontmatter_value(text, "standalone"))

    def test_private_bindings_are_absent_from_public_bodies(self) -> None:
        for relative in PUBLIC_CORES:
            for filename in LANGUAGES:
                path = REPOSITORY_ROOT / relative / filename
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


if __name__ == "__main__":
    unittest.main()
