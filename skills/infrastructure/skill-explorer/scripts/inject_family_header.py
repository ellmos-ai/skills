#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inject_family_header.py — Familien-Router-Header in user-eigene Skills setzen/entfernen (c2).

Baut in jeden angegebenen, EDITIERBAREN Skill einen Wegweiser-Block ein, der auf die Geschwister
der Familie verweist (z. B. "für ganz neue Ideen lieber /brainstorm statt /think"). Idempotent:
ein vorhandener Block derselben Familie wird ersetzt; mit --remove wird er entfernt.

Sicherheit (Survey != Mutation): Ein Skill wird NUR verändert, wenn er im Inventar als
editable/source=user geführt ist. Plugin- und Drittanbieter-Skills werden übersprungen.

Der Block geht in den BODY (nach der H1-Überschrift), NICHT ins Frontmatter — sonst würde das
Skill-Triggering gestört. Er ist als HTML-Kommentar markiert und damit sauber wieder entfernbar.

Aufruf (Windows: PYTHONIOENCODING=utf-8 setzen):
    python inject_family_header.py --family NAME --skills dir1,dir2,... --router "TEXT" \
        --inventory ~/.skill-inventory.json [--skills-root ~/.claude/skills] [--remove] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

MARK_START = "<!-- FAMILY-ROUTER:{fam} START -->"
MARK_END = "<!-- FAMILY-ROUTER:{fam} END -->"
# erkennt einen vorhandenen Block derselben Familie (zum Ersetzen/Entfernen)
BLOCK_RE = "{start}.*?{end}\n?"


def find_skill_file(skill_dir: Path) -> Path | None:
    if not skill_dir.is_dir():
        return None
    for entry in skill_dir.iterdir():
        if entry.is_file() and entry.name.lower() == "skill.md":
            return entry
    return None


def load_editable(inventory_path: Path) -> dict[str, bool]:
    """dir -> editable-Flag aus dem Inventar (Quelle der Wahrheit für Survey != Mutation)."""
    if not inventory_path or not inventory_path.is_file():
        return {}
    data = json.loads(inventory_path.read_text(encoding="utf-8"))
    return {s["dir"]: bool(s.get("editable")) for s in data.get("skills", [])}


def build_block(fam: str, router: str) -> str:
    start = MARK_START.format(fam=fam)
    end = MARK_END.format(fam=fam)
    return f"{start}\n> **Familie {fam} — Wegweiser:** {router}\n{end}\n"


def strip_block(text: str, fam: str) -> str:
    start = re.escape(MARK_START.format(fam=fam))
    end = re.escape(MARK_END.format(fam=fam))
    pattern = BLOCK_RE.format(start=start, end=end)
    return re.sub(pattern, "", text, flags=re.DOTALL)


def insert_after_h1(text: str, block: str) -> str:
    """Block direkt nach der ersten H1-Überschrift einfügen (sonst am Body-Anfang)."""
    m = re.search(r"^#\s+.+$", text, flags=re.MULTILINE)
    if m:
        idx = m.end()
        return text[:idx] + "\n\n" + block + text[idx:]
    return block + "\n" + text


def read_preserving_eol(skill_file: Path) -> tuple[str, str]:
    """Liest Text und merkt sich den Zeilenend-Stil, damit das Schreiben ihn erhält.

    Ohne das würde write_text unter Windows alle \n in \r\n umwandeln und so die GANZE Datei
    als geändert markieren (verrauschte Diffs), selbst wenn nur der Router-Block dazukommt.
    """
    raw = skill_file.read_bytes().decode("utf-8", errors="replace")
    newline = "\r\n" if "\r\n" in raw else "\n"
    text = raw.replace("\r\n", "\n").replace("\r", "\n")  # für Verarbeitung normalisieren
    return text, newline


def write_preserving_eol(skill_file: Path, text: str, newline: str) -> None:
    if newline == "\r\n":
        text = text.replace("\n", "\r\n")
    skill_file.write_bytes(text.encode("utf-8"))


def process(skill_file: Path, fam: str, router: str, remove: bool) -> tuple[str, str]:
    text, newline = read_preserving_eol(skill_file)
    text = strip_block(text, fam)  # alten Block entfernen (idempotent)
    if not remove:
        text = insert_after_h1(text, build_block(fam, router))
    # doppelte Leerzeilen aufräumen (auf normalisiertem \n)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text, newline


def main() -> int:
    ap = argparse.ArgumentParser(description="Familien-Router-Header setzen/entfernen (nur user-Skills).")
    ap.add_argument("--family", required=True, help="Familienname (Marker-Schlüssel).")
    ap.add_argument("--skills", required=True, help="Komma-Liste der Skill-Verzeichnisnamen.")
    ap.add_argument("--router", default="", help="Wegweiser-Text (bei --remove ignoriert).")
    ap.add_argument("--inventory", default=str(Path.home() / ".skill-inventory.json"),
                    help="Inventar-JSON für die editable-Prüfung.")
    ap.add_argument("--skills-root", default=str(Path.home() / ".claude" / "skills"),
                    help="Wurzel der user-Skills.")
    ap.add_argument("--remove", action="store_true", help="Block entfernen statt setzen.")
    ap.add_argument("--dry-run", action="store_true", help="Nur anzeigen, nichts schreiben.")
    args = ap.parse_args()

    if not args.remove and not args.router.strip():
        print("FEHLER: --router darf beim Setzen nicht leer sein.", file=sys.stderr)
        return 2

    root = Path(os.path.expanduser(args.skills_root))
    editable = load_editable(Path(os.path.expanduser(args.inventory)))
    targets = [s.strip() for s in args.skills.split(",") if s.strip()]

    changed, skipped = 0, 0
    for dirn in targets:
        # Sicherheits-Gate: nur explizit editierbare user-Skills
        if editable and not editable.get(dirn, False):
            print(f"SKIP (read-only/nicht user): {dirn}")
            skipped += 1
            continue
        sf = find_skill_file(root / dirn)
        if not sf:
            print(f"SKIP (kein SKILL.md): {dirn}")
            skipped += 1
            continue
        new_text, newline = process(sf, args.family, args.router, args.remove)
        if args.dry_run:
            action = "WÜRDE ENTFERNEN" if args.remove else "WÜRDE SETZEN"
            print(f"{action}: {sf}")
        else:
            write_preserving_eol(sf, new_text, newline)
            print(f"{'ENTFERNT' if args.remove else 'GESETZT'}: {dirn}")
        changed += 1

    print(f"[router] geändert={changed} übersprungen={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
