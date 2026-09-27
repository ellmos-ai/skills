#!/usr/bin/env python3
"""Prüft SKILL*.md-Frontmatter auf die zwei bekannten YAML-Bruchmuster + Pflichtfelder.

WARUM ES DIESES GATE GIBT
--------------------------
Am 2026-09-27 wurde entdeckt, dass 279 `SKILL*.md`-Dateien ein Frontmatter
hatten, das ein YAML-Parser nicht lesen konnte -- meist eine unquotierte
`description:` mit einem ": " im Fliesstext (YAML liest das als neue
Mapping-Zeile) oder ein `description: >`-Faltblock, dessen Fortsetzungszeilen
die Einrueckung verloren hatten (vermutlich durch einen Batch-Uebersetzer/
Zeilenumbruch-Skript). 11 der betroffenen Skills waren bereits deployt und
warfen in Claude Code den Laufzeitfehler
`Error in user YAML: mapping values are not allowed in this context`.
Weder `language_gate.py` (prueft die SPRACHE des Bodys) noch `skill_tester.py`
(prueft PFLICHTFELDER ueber eine tolerante Regex, nicht ueber einen echten
Parse) haben einen kaputten Parse jemals VOR der Laufzeit erkannt.

KEIN YAML-PARSER, ABSICHTLICH
------------------------------
Dieses Repo ist bewusst zero-dependency (kein Eintrag in pyproject.toml,
mehrere Skills werben aktiv damit) -- ein erster Entwurf importierte PyYAML
und brach die CI, weil `pip install ruff pytest` in tests.yml kein PyYAML
mitbringt. Statt einer Fremdabhaengigkeit prueft dieses Skript stdlib-only
gezielt genau die Struktur, die alle ~1060 echten Frontmatter-Bloecke dieses
Repos tatsaechlich brauchen (flache `schluessel: wert`-Paare, gequotete oder
blanke Skalare, `>`/`|`-Faltbloecke, `[...]`/`{...}`-Inline-Collections) und
die zwei oben beschriebenen Bruchmuster. Es ist keine vollstaendige
YAML-Engine und erkennt keine beliebige Fehlform -- fuer diesen Zweck reicht
das nicht, war aber auch nie das Ziel.

Dieses Skript ist bewusst wiederverwendbar an drei Stellen gedacht (Ticket
T-20260927-518399776, Nutzerwunsch): (1) als CI-/Pre-Commit-Gate in diesem
Repo, (2) als Vorabpruefung in `skill_sync.py deploy` (OneDrive-Mirror,
bricht das Deployment eines kaputten Skills ab statt ihn live zu schalten),
(3) als Pruefschritt im Skill `repo-publish-check`.

Aufruf:
    PYTHONIOENCODING=utf-8 python testing/skill_frontmatter_gate.py
        Nur pruefen. Exit 0 = jede SKILL*.md-Frontmatter ist frei von den
        beiden bekannten Bruchmustern und hat die Pflichtfelder `name` und
        `description`.
    PYTHONIOENCODING=utf-8 python testing/skill_frontmatter_gate.py --fix
        Quotet zusaetzlich mechanisch (json.dumps) jede unquotierte
        description mit einem problematischen Wert und fasst kaputte
        `description: >`-Bloecke zu einer Zeile zusammen -- die einzigen
        beiden bekannten Fehlerbilder. Validiert jede geaenderte Datei danach
        erneut; eine Datei, die auch nach dem Fix nicht sauber ist, wird als
        Fehler gemeldet statt still "repariert".
    ... --repo <pfad>
        Andere Wurzel als dieses Skript pruefen (z. B. der OneDrive-Mirror).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_ROOT_NAME = "skills"

# Vorlagen-Assets wie skill-explorer/assets/skill-finder-template.md heissen
# zufaellig "skill*.md" (Windows-Dateisystem ist case-insensitiv, ein reines
# Glob wuerde sie mittreffen) und enthalten bewusst {{platzhalter}} statt
# echter Werte -- kein zu ladendes Skill-Frontmatter.
SKILL_FILE = re.compile(r"^SKILL(\.[a-z]{2})?\.md$")
IGNORIERTE_TEILE = {"_archive", "__pycache__"}

REQUIRED_FIELDS = ("name", "description")
BLOCK_SCALAR_VALUES = (">", "|", ">-", "|-", ">+", "|+")

TOP_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(.*)$")
DESC_LINE = re.compile(r"^description:(.*)$")
BLOCK_SCALAR_HEAD = re.compile(r"^description:\s*[>|][+-]?\s*$")
NEXT_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*:")


def gefundene_skill_dateien(repo: Path) -> list[Path]:
    skills_root = repo / SKILLS_ROOT_NAME
    if not skills_root.is_dir():
        return []
    return sorted(
        p for p in skills_root.rglob("*.md")
        if SKILL_FILE.match(p.name)
        and not (set(p.relative_to(repo).parts) & IGNORIERTE_TEILE)
    )


def split_frontmatter(text: str) -> tuple[str, str] | None:
    """Gibt (frontmatter, rest) zurueck, oder None wenn keins vorliegt."""
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    return parts[1], parts[2]


def _frontmatter_findings(fm: str) -> list[str]:
    """Stdlib-only Strukturpruefung fuer die zwei bekannten Bruchmuster.

    Lauft zeilenweise ueber die Frontmatter-Rohtexte. Jede nicht eingerueckte,
    nicht-leere Zeile muss `schluessel: wert` sein; alles direkt darauf
    folgende Eingerueckte/Leere gilt als Koerper dieses Schluessels (Faltblock
    ODER verschachteltes Mapping -- Letzteres wird hier nicht tiefer geprueft,
    das ist nicht der bekannte Fehlerfall). Zwei gezielte Zusatzchecks:
    ein `>`/`|`-Header, dessen naechste Nichtleer-Zeile NICHT eingerueckt ist
    (Bruchmuster 2), und ein blanker Ein-Zeilen-Wert mit einem ": " darin
    (Bruchmuster 1 -- genau das, was YAML als neue Mapping-Zeile lesen wuerde).
    """
    lines = fm.splitlines()
    n = len(lines)
    findings: list[str] = []
    i = 0
    saw_any_key = False
    while i < n:
        line = lines[i]
        stripped_line = line.strip()
        if not stripped_line or stripped_line.startswith("#"):
            i += 1  # leer oder ein voller YAML-Kommentar (z.B. Abschnittsueberschrift)
            continue
        if line[0] in " \t":
            findings.append(
                f"Zeile {i + 1}: eingerueckte Zeile ohne vorausgehenden "
                f"Schluessel: {line.strip()[:60]!r}"
            )
            i += 1
            continue
        m = TOP_KEY.match(line)
        if not m:
            findings.append(f"Zeile {i + 1}: keine gueltige 'schluessel: wert'-Zeile: {line[:60]!r}")
            i += 1
            continue
        saw_any_key = True
        key, value = m.group(1), m.group(2).strip()

        scan = i + 1
        while scan < n and lines[scan].strip() == "":
            scan += 1
        if value in BLOCK_SCALAR_VALUES and scan < n and lines[scan][0] not in " \t":
            findings.append(
                f"Zeile {scan + 1}: Faltblock von '{key}:' (Zeile {i + 1}) verlor "
                "die Einrueckung -- wird als eigene Mapping-Zeile gelesen"
            )
            i = scan
            continue

        if value and value not in BLOCK_SCALAR_VALUES and not value.startswith(('"', "'", "[", "{")):
            if ": " in value or value.endswith(":"):
                findings.append(
                    f"Zeile {i + 1}: unquotierter Wert von '{key}:' enthaelt ': ' "
                    f"-- wird als neue Mapping-Zeile gelesen: {value[:60]!r}"
                )

        j = i + 1
        while j < n and (lines[j].strip() == "" or lines[j][0] in " \t"):
            j += 1
        i = j

    if not saw_any_key:
        findings.append("keine einzige gueltige 'schluessel: wert'-Zeile gefunden")
    return findings


def _top_level_field_presence(fm: str) -> dict[str, bool]:
    """Schluessel -> traegt er einen nicht-leeren Wert (Einzeiler oder Koerper)?"""
    lines = fm.splitlines()
    n = len(lines)
    presence: dict[str, bool] = {}
    i = 0
    while i < n:
        line = lines[i]
        if not line.strip() or line[0] in " \t":
            i += 1
            continue
        m = TOP_KEY.match(line)
        if not m:
            i += 1
            continue
        key, value = m.group(1), m.group(2).strip()
        has_content = bool(value) and value not in BLOCK_SCALAR_VALUES
        j = i + 1
        while j < n and (lines[j].strip() == "" or lines[j][0] in " \t"):
            if lines[j].strip():
                has_content = True
            j += 1
        presence[key] = has_content
        i = j
    return presence


def pruefe(md: Path) -> list[str]:
    """Gibt alle Befunde zurueck; leere Liste = Datei ist in Ordnung."""
    text = md.read_text(encoding="utf-8", errors="replace")
    split = split_frontmatter(text)
    if split is None:
        return ["keine Frontmatter-Markierung '---' am Dateianfang bzw. "
                "Frontmatter-Block nicht mit zweitem '---' geschlossen"]
    fm, _ = split

    struktur_befunde = _frontmatter_findings(fm)
    if struktur_befunde:
        return struktur_befunde

    presence = _top_level_field_presence(fm)

    # Uebersetzungs-/Marker-Stubs (z.B. skills/assist/dev/SKILL.fr.md: nur
    # `language: fr`, Inhalt bleibt die englische Primaerfassung mit
    # Sprachbanner) tragen bewusst KEIN eigenes `name` -- sie erben es von der
    # Primaerfassung, wie `inherits_visibility()` in skill_tester.py es fuer
    # `visibility` bereits vormacht. 73 solcher Dateien wurden beim Entwurf
    # dieses Gates gemessen; kein einziger echter Primaer-Skill hat `language`
    # ohne `name`. Pflichtfelder gelten deshalb nur, wenn die Datei ueberhaupt
    # einen eigenen `name`-Schluessel deklariert.
    if "name" not in presence and "language" in presence:
        return []

    befunde = []
    for feld in REQUIRED_FIELDS:
        if not presence.get(feld):
            befunde.append(f"Pflichtfeld fehlt oder ist leer: {feld}")
    return befunde


def _fix_unquoted_description(fm: str) -> str | None:
    """Fehlerbild 1: einzeilige description mit problematischem Wert quoten."""
    lines = fm.splitlines(keepends=True)
    for i, line in enumerate(lines):
        stripped = line.rstrip("\r\n")
        eol = line[len(stripped):]
        m = DESC_LINE.match(stripped)
        if not m:
            continue
        raw_value = m.group(1)
        if raw_value.startswith(" "):
            raw_value = raw_value[1:]
        value = raw_value.strip()
        if value.startswith(('"', "'", ">", "|")):
            return None  # schon quotiert oder ein Block-Skalar
        lines[i] = "description: " + json.dumps(value, ensure_ascii=False) + eol
        return "".join(lines)
    return None


def _fix_broken_block_scalar(fm: str) -> str | None:
    """Fehlerbild 2: description: > -Block mit verlorener Einrueckung."""
    lines = fm.splitlines()
    desc_i = None
    for i, line in enumerate(lines):
        if BLOCK_SCALAR_HEAD.match(line):
            desc_i = i
            break
    if desc_i is None:
        return None

    j = desc_i + 1
    block_lines = []
    while j < len(lines) and not NEXT_KEY.match(lines[j]):
        block_lines.append(lines[j].strip())
        j += 1
    value = " ".join(zeile for zeile in block_lines if zeile)

    new_lines = (
        lines[:desc_i]
        + ["description: " + json.dumps(value, ensure_ascii=False)]
        + lines[j:]
    )
    return "\n".join(new_lines) + ("\n" if fm.endswith("\n") else "")


def fixe(md: Path) -> str | None:
    """Versucht die zwei bekannten Fehlerbilder mechanisch zu reparieren.

    Gibt eine kurze Statuszeile zurueck wenn etwas geaendert wurde, sonst
    None. Aendert nie den Wortlaut -- nur Quotierung/Zeilenfaltung.
    """
    text = md.read_text(encoding="utf-8", errors="replace")
    split = split_frontmatter(text)
    if split is None:
        return None
    fm, body = split

    if not _frontmatter_findings(fm):
        return None  # schon sauber, nichts zu tun

    neu = _fix_unquoted_description(fm) or _fix_broken_block_scalar(fm)
    if neu is None:
        return None

    reststoerungen = _frontmatter_findings(neu)
    if reststoerungen:
        return f"FIX FEHLGESCHLAGEN (unveraendert gelassen): {reststoerungen[0]}"

    md.write_text("---" + neu + "---" + body, encoding="utf-8")
    return "requotiert"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", type=Path, default=REPO,
                         help="Repository-Wurzel (Standard: Wurzel dieses Skripts).")
    parser.add_argument("--fix", action="store_true",
                         help="Mechanisch requotieren, dann neu validieren.")
    args = parser.parse_args(argv)
    repo = args.repo.resolve()

    dateien = gefundene_skill_dateien(repo)
    if args.fix:
        fixe_anzahl = 0
        fix_fehlschlaege = []
        for md in dateien:
            ergebnis = fixe(md)
            if ergebnis is None:
                continue
            if ergebnis.startswith("FIX FEHLGESCHLAGEN"):
                fix_fehlschlaege.append((md, ergebnis))
            else:
                fixe_anzahl += 1
        if fixe_anzahl:
            print(f"{fixe_anzahl} Datei(en) requotiert.")
        if fix_fehlschlaege:
            print(f"{len(fix_fehlschlaege)} Datei(en) konnten NICHT automatisch "
                  "repariert werden:")
            for md, ergebnis in fix_fehlschlaege:
                print(f"  {md.relative_to(repo)}: {ergebnis}")

    befunde = []
    for md in dateien:
        for fehler in pruefe(md):
            befunde.append((str(md.relative_to(repo)).replace("\\", "/"), fehler))

    if befunde:
        print(f"FEHLER: {len(befunde)} Befund(e) in SKILL*.md-Frontmatter "
              f"({len(dateien)} Dateien geprueft)\n")
        for pfad, fehler in befunde:
            print(f"  {pfad}: {fehler}")
        if not args.fix:
            print("\nMit --fix koennen bekannte Quotierungsfehler mechanisch "
                  "behoben werden.")
        return 1

    print(f"Skill-Frontmatter-Gate bestanden: {len(dateien)} SKILL*.md-Dateien geprueft.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
