"""Lint: Sprachhinweise (Banner) in SKILL*.md muessen zur Dateisprache und zum Text passen.

Hintergrund und Regeln: fix_language_banners.py (T-20261122-838934534).
"""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "fix_language_banners", REPO_ROOT / "fix_language_banners.py"
)
assert SPEC is not None and SPEC.loader is not None
tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tool)

EN_BODY = ("# Title\n\n" + "The skill will check the files and the results for each run when needed. " * 6)
DE_BODY = ("# Titel\n\n" + "Der Skill wird die Dateien und die Ergebnisse nicht ohne Prüfung ändern und auch nicht löschen. " * 6)


def _write(root: Path, name: str, banner: str, body: str) -> Path:
    skill = root / "skills" / "x" / "demo"
    skill.mkdir(parents=True, exist_ok=True)
    path = skill / name
    path.write_text(f"---\nname: demo\n---\n\n{banner}\n\n{body}\n", encoding="utf-8")
    return path


class LanguageBannerTests(unittest.TestCase):
    def test_repository_has_no_broken_banners(self) -> None:
        broken = []
        for path in tool.tracked_skill_files():
            _, problems = tool.analyze(path)
            if problems:
                broken.append(f"{path.relative_to(REPO_ROOT).as_posix()}: {', '.join(problems)}")
        self.assertEqual(
            broken, [], "run `python fix_language_banners.py --apply` and review the diff"
        )

    def test_garbled_template_is_detected_and_fixed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            banner = "> **English** — Offizielle English-Version / Documento Oficial en English."
            path = _write(Path(tmp), "SKILL.en.md", banner, EN_BODY)
            new, problems = tool.analyze(path)
            self.assertIn("Mischvorlage", problems)
            self.assertIn("> **English** — Official English version of `demo`.", new)
            self.assertNotIn("Documento Oficial", new)

    def test_wrong_language_text_gets_honest_notice(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            banner = "> **Français** — Version française officielle de la compétence `demo`."
            path = _write(Path(tmp), "SKILL.fr.md", banner, DE_BODY)
            new, problems = tool.analyze(path)
            self.assertTrue(problems)
            self.assertIn("Traduction en attente", new)
            self.assertIn("allemand", new)

    def test_clean_files_and_missing_banner_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ok = "> **English** — Official English version of `demo`."
            self.assertEqual(tool.analyze(_write(Path(tmp), "SKILL.en.md", ok, EN_BODY)), (None, []))
            pending = "> **Français** — Traduction en attente : le contenu est actuellement en allemand."
            self.assertEqual(tool.analyze(_write(Path(tmp), "SKILL.fr.md", pending, DE_BODY)), (None, []))

    def test_stale_pending_notice_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            stale = "> **English** — Translation pending: content is currently German."
            _, problems = tool.analyze(_write(Path(tmp), "SKILL.en.md", stale, EN_BODY))
            self.assertIn("veralteter Uebersetzungs-Hinweis", problems)


if __name__ == "__main__":
    unittest.main()
