#!/usr/bin/env python3
"""Prüft README-Skilllinks (Sprachpassung) UND relative Links in SKILL*.md.

README-Teil: verhindert, dass lokalisierte Übersichtsseiten versehentlich
die deutsche Primärdatei statt einer vorhandenen Übersetzung verlinken. Fehlt
eine Übersetzung, gilt die deutsche SKILL.md als dokumentierter Rückfall.

SKILL*.md-Teil (T-20260927-518399776, PR #48 Review): PR #48 verlinkte in
`wayfinding-routing` per `../likelihood-routing/SKILL.md` auf einen Skill,
der als `visibility: private-only` markiert und nicht in diesem Repo
getrackt ist -- ein toter Link auf einen privaten Skill in einem
öffentlichen Repo, unentdeckt weil der README-Teil nur README-Dateien
prüft, nicht den Fließtext von SKILL*.md-Dateien. Dieser zweite Teil
prüft deshalb jeden relativen Markdown-Link (`[text](pfad)`) und jede
`<img src="pfad">` in jeder getrackten SKILL*.md gegen `git ls-files`.

Beide Teile prüfen gegen GIT-GETRACKTE Dateien, nicht gegen die Festplatte:
Lokal liegen ungetrackte private Skills (z. B. `trampelpfadanalyse`,
`likelihood-routing`), fuer die ein Link lokal gruen waere, auf GitHub
aber tot ist -- `git ls-files` ist deshalb die einzige Quelle, die mit dem
oeffentlichen Repo uebereinstimmt. Eine `visibility: private-only`-Markierung
in der Bibliothek aendert daran nichts: entweder die Datei ist getrackt
(dann zaehlt sie), oder sie ist es nicht (dann zaehlt sie als fehlend) --
unabhaengig vom Frontmatter-Feld.
"""
from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
from pathlib import Path, PurePosixPath

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


# Markdown-Link `[text](ziel)` -- Fragment/Query am Ende wird beim Aufloesen
# abgeschnitten, zaehlt aber nicht zur Existenzpruefung.
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
# <img src="ziel"> (einfache oder doppelte Anfuehrungszeichen).
IMG_SRC = re.compile(r'<img\b[^>]*\bsrc=["\']([^"\']+)["\']', re.I)

SKILL_MD_NAME = re.compile(r"^SKILL(\.[a-z]{2})?\.md$")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "file:", "#")


def _is_external_or_anchor(target: str) -> bool:
    return target.startswith(EXTERNAL_PREFIXES) or target.startswith("//")


SKILL_LINK_BASELINE = Path(__file__).with_name("skill_link_baseline.json")


def _load_skill_link_baseline() -> frozenset[tuple[str, str]]:
    """(datei, aufgeloestes-ziel)-Paare, die bewusst (noch) nicht gefixt sind.

    T-20260927-518399776 (PR #48 Folgeticket): der erste Lauf dieses Checks
    gegen den echten Baum fand 434 Verstoesse, uebersaettigt von EINEM
    systemischen Vorbestand -- Sprach-Unterordner-Kopien (`EN/SKILL.md` etc.),
    deren relative Links (`banner.png`, `../anderer-skill/SKILL.en.md`) nicht
    an die zusaetzliche Verzeichnistiefe angepasst wurden. Das ist zu viel
    fuer diese PR und braucht ein eigenes Ticket -- aber ein hartes Blockieren
    aller 434 Alt-Funde haette das Gate direkt nach Einfuehrung wieder
    stillgelegt (die uebliche Reaktion darauf: `--no-verify` oder Revert).
    Diese Baseline haelt die ALT-Funde fest (mit Fundstelle, damit sie nicht
    "verschwinden"), waehrend jeder NEUE Fund -- wie der likelihood-routing-
    Link, der dieses Gate ausgeloest hat -- weiterhin hart blockiert.
    """
    if not SKILL_LINK_BASELINE.is_file():
        return frozenset()
    daten = json.loads(SKILL_LINK_BASELINE.read_text(encoding="utf-8"))
    return frozenset((e["datei"], e["ziel"]) for e in daten.get("ausnahmen", []))


def scan_skill_bodies(repo_root: Path) -> tuple[list[str], int, int]:
    """Prueft jeden relativen Link/img-src in jeder getrackten SKILL*.md.

    Liefert (Verletzungen, Anzahl gepruefter Links, Anzahl per Baseline
    ausgenommener Alt-Funde).
    """
    violations: list[str] = []
    checked_links = 0
    baselined = 0
    tracked = tracked_files(repo_root)
    baseline = _load_skill_link_baseline()

    skill_md_paths = sorted(
        p for p in tracked
        if SKILL_MD_NAME.match(PurePosixPath(p).name)
        and PurePosixPath(p).parts[0] == "skills"
    )

    for rel_path in skill_md_paths:
        md_file = repo_root / rel_path
        base_dir = PurePosixPath(rel_path).parent
        text = md_file.read_text(encoding="utf-8", errors="replace")

        for line_number, line in enumerate(text.splitlines(), start=1):
            # Strip inline code spans first: a line documenting this very
            # gate's own target syntax (e.g. "`[text](url)`" as a worked
            # example of what a Markdown link looks like) is not a real,
            # navigable link -- Markdown renders code spans literally, and
            # placeholders like "url" were never meant to resolve.
            scan_line = re.sub(r"`[^`]*`", "", line)
            targets = [m.group(1) for m in MD_LINK.finditer(scan_line)]
            targets += [m.group(1) for m in IMG_SRC.finditer(scan_line)]
            for raw_target in targets:
                target = raw_target.strip()
                if not target or _is_external_or_anchor(target):
                    continue
                # Fragment/Query abschneiden (z.B. SKILL.md#abschnitt), das
                # Linkziel selbst ist die Datei davor.
                path_part = re.split(r"[#?]", target, maxsplit=1)[0]
                if not path_part:
                    continue
                checked_links += 1
                # normpath aufloest "..": PurePosixPath allein tut das nicht,
                # posixpath.normpath schon (funktioniert fuer posix-Segmente
                # unabhaengig vom Host-Betriebssystem).
                resolved = posixpath.normpath(str(PurePosixPath(base_dir, path_part)))
                if resolved not in tracked:
                    if (rel_path, resolved) in baseline:
                        baselined += 1
                        continue
                    violations.append(
                        f"{rel_path}:{line_number}: Link auf '{path_part}' -> "
                        f"'{resolved}' ist nicht git-getrackt (privat oder nicht "
                        "vorhanden)"
                    )

    return violations, checked_links, baselined


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository-Wurzel (Standard: Wurzel dieses Skripts).",
    )
    args = parser.parse_args(argv)
    repo_root = args.repo.resolve()

    readme_violations, readme_checked = scan_readmes(repo_root)
    skill_violations, skill_checked, baselined = scan_skill_bodies(repo_root)
    violations = readme_violations + skill_violations

    if violations:
        print(f"README/SKILL link gate failed: {len(violations)} violation(s).")
        for violation in violations:
            print(f"- {violation}")
        if baselined:
            print(f"\n({baselined} additional known pre-existing finding(s) "
                  f"exempted via {SKILL_LINK_BASELINE.name}.)")
        return 1

    print(
        "README/SKILL link gate passed: "
        f"{readme_checked} skill links across {len(README_LANGUAGES)} READMEs, "
        f"{skill_checked} relative links across tracked SKILL*.md files validated "
        f"({baselined} pre-existing exempted via {SKILL_LINK_BASELINE.name})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
