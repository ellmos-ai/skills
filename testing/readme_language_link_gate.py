#!/usr/bin/env python3
"""Prüft, ob README-Skilllinks zur Sprache der jeweiligen README passen.

Diese Schranke verhindert, dass lokalisierte Übersichtsseiten versehentlich
die deutsche Primärdatei statt einer vorhandenen Übersetzung verlinken. Fehlt
eine Übersetzung, gilt die deutsche SKILL.md als dokumentierter Rückfall.

Prüft gegen GIT-GETRACKTE Dateien, nicht gegen die Festplatte: Lokal liegen
ungetrackte private Skills (z. B. `trampelpfadanalyse`), fuer die ein Link
lokal gruen waere, auf GitHub aber tot ist -- `git ls-files` ist deshalb die
einzige Quelle, die mit dem oeffentlichen Repo uebereinstimmt.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPOSITORY_ROOT))
from testing.repo_privacy_gate import git_lines  # noqa: E402


def tracked_files(repo_root: Path) -> frozenset[str]:
    """Alle von git getrackten Pfade, relativ zur Repo-Wurzel, POSIX-Slashes."""
    return frozenset(git_lines(repo_root, "ls-files"))


README_LANGUAGES = {
    "README.md": "en",
    "README_de.md": "de",
    "README_es.md": "es",
    "README_ja.md": "ja",
    "README_ru.md": "ru",
    "README_zh.md": "zh",
}

# Erfasst relative Skilldatei-Ziele mit den zwei Verzeichnisebenen des Katalogs.
SKILL_LINK = re.compile(
    r"(?P<target>skills/[^/\s)<>]+/[^/\s)<>]+/SKILL[^/\s)<>]*?\.md)"
    r"(?:#[^\s)<>]*)?"
)


def _expected_target(
    tracked: frozenset[str], skill_dir: Path, language: str
) -> tuple[Path, str]:
    """Gibt den bevorzugten Link und den Grund für einen Rückfall zurück."""
    primary = skill_dir / "SKILL.md"
    if language == "de":
        return primary, "deutsche Primärdatei"

    translated = skill_dir / f"SKILL.{language}.md"
    if translated.as_posix() in tracked:
        return translated, f"vorhandene Übersetzung {language}"
    return primary, f"deutscher Rückfall, da SKILL.{language}.md fehlt"


def scan_readmes(repo_root: Path) -> tuple[list[str], int]:
    """Liefert alle Linkverletzungen und die Zahl der geprüften Skilllinks."""
    violations: list[str] = []
    checked_links = 0
    tracked = tracked_files(repo_root)

    for readme_name, language in README_LANGUAGES.items():
        readme_path = repo_root / readme_name
        if readme_name not in tracked:
            violations.append(f"{readme_name}: README-Datei ist nicht git-getrackt.")
            continue

        for line_number, line in enumerate(
            readme_path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            for match in SKILL_LINK.finditer(line):
                checked_links += 1
                target = match.group("target")
                skill_dir = Path(*target.split("/")[:3])
                expected_path, reason = _expected_target(tracked, skill_dir, language)
                actual_target = Path(*target.split("/")).as_posix()
                expected_target = expected_path.as_posix()
                actual_tracked = actual_target in tracked
                problems: list[str] = []

                if not actual_tracked:
                    problems.append("Zieldatei ist nicht git-getrackt")
                if actual_target != expected_target:
                    problems.append(f"falsche Sprachdatei; erwartet {expected_target} ({reason})")

                if problems:
                    violations.append(
                        f"{readme_name}:{line_number}: {target} -> "
                        f"erwartet {expected_target}, tatsächlich {actual_target} "
                        f"({'getrackt' if actual_tracked else 'nicht getrackt'}); "
                        f"{' ; '.join(problems)}"
                    )

    return violations, checked_links


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository-Wurzel (Standard: Wurzel dieses Skripts).",
    )
    args = parser.parse_args(argv)

    violations, checked_links = scan_readmes(args.repo.resolve())
    if violations:
        print(f"README language link gate failed: {len(violations)} violation(s).")
        for violation in violations:
            print(f"- {violation}")
        return 1

    print(
        "README language link gate passed: "
        f"{checked_links} skill links across {len(README_LANGUAGES)} READMEs validated."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
