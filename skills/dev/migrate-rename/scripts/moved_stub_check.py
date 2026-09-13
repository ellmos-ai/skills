#!/usr/bin/env python3
"""Prueft MOVED-Stubs (Umzugs-Pointer) unter einem Wurzelverzeichnis.

Listet jede *.MOVED.md / *.MIGRATED.md-Datei, meldet fehlende Pflichtfelder
(moved_to, moved_on, ticket, reason, moved_by, remove_when) und markiert Stubs,
die nach Alter rueckbau-faellig sind (remove_when-Tageszahl, Default 90).

Prueft NICHT "0 lebende Referenzen" -- das braucht eine Volltextsuche ueber den
gesamten Baum, die dieses Skript bewusst nicht mitbringt (siehe SKILL.md,
Abschnitt "Ordner-/Datei-Umzug mit MOVED-Stub").

Usage:
    python moved_stub_check.py <wurzelverzeichnis>
"""
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

REQUIRED_FIELDS = ["moved_to", "moved_on", "ticket", "reason", "moved_by", "remove_when"]
DEFAULT_REMOVE_AFTER_DAYS = 90
FIELD_RE = re.compile(r"^([a-z_]+):\s*(.*)$")
DAYS_RE = re.compile(r"(\d+)\s*Tage")


def parse_stub(path: Path) -> dict[str, str]:
    """Liest fuehrende key: value-Zeilen bis zur ersten Leerzeile/unbekannten Zeile."""
    fields: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            break
        m = FIELD_RE.match(line)
        if not m:
            break
        fields[m.group(1)] = m.group(2).strip()
    return fields


def check_stub(path: Path) -> dict:
    fields = parse_stub(path)
    missing = [f for f in REQUIRED_FIELDS if f not in fields or not fields[f]]

    due_for_removal = False
    age_days = None
    moved_on = fields.get("moved_on", "")
    try:
        moved_date = date.fromisoformat(moved_on)
        age_days = (date.today() - moved_date).days
        m = DAYS_RE.search(fields.get("remove_when", ""))
        threshold = int(m.group(1)) if m else DEFAULT_REMOVE_AFTER_DAYS
        due_for_removal = age_days >= threshold
    except ValueError:
        pass

    return {
        "path": str(path),
        "missing_fields": missing,
        "age_days": age_days,
        "due_for_removal": due_for_removal,
    }


def find_stubs(root: Path):
    yield from root.rglob("*.MOVED.md")
    yield from root.rglob("*.MIGRATED.md")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 1
    root = Path(argv[1])
    if not root.is_dir():
        print(f"Kein Verzeichnis: {root}")
        return 1

    results = [check_stub(p) for p in sorted(find_stubs(root))]
    if not results:
        print(f"Keine *.MOVED.md/*.MIGRATED.md-Stubs unter {root}")
        return 0

    for r in results:
        status = []
        if r["missing_fields"]:
            status.append(f"FEHLENDE FELDER: {', '.join(r['missing_fields'])}")
        if r["due_for_removal"]:
            status.append(f"RUECKBAU-FAELLIG (Alter {r['age_days']} Tage)")
        if not status:
            status.append(f"ok (Alter {r['age_days']} Tage)" if r["age_days"] is not None else "ok")
        print(f"{r['path']}: {' | '.join(status)}")

    print(
        f"\n{len(results)} Stub(s) geprueft. "
        "'RUECKBAU-FAELLIG' prueft nur das Alter -- 'remove_when' braucht zusaetzlich "
        "0 lebende Referenzen (manuelle/Tool-Suche, hier nicht automatisiert)."
    )
    return 0


def demo() -> None:
    """Kleiner Selbsttest ueber temporaere Stub-Dateien (kein Framework, siehe Ponytail-Regel)."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        ok_stub = root / "ok.MOVED.md"
        ok_stub.write_text(
            "moved_to: <HOME>/x\n"
            "moved_on: 2026-09-06\n"
            "ticket: T-20260906-1\n"
            "reason: Test\n"
            "moved_by: test@host\n"
            "remove_when: 90 Tage UND 0 lebende Referenzen\n",
            encoding="utf-8",
        )
        broken_stub = root / "broken.MOVED.md"
        broken_stub.write_text("moved_to: <HOME>/y\nmoved_on: 2026-01-01\n", encoding="utf-8")
        old_stub = root / "old.MIGRATED.md"
        old_stub.write_text(
            "moved_to: <HOME>/z\n"
            "moved_on: 2020-01-01\n"
            "ticket: T-1\n"
            "reason: Test\n"
            "moved_by: test@host\n"
            "remove_when: 90 Tage UND 0 lebende Referenzen\n",
            encoding="utf-8",
        )

        ok_result = check_stub(ok_stub)
        assert not ok_result["missing_fields"], ok_result
        assert not ok_result["due_for_removal"], ok_result

        broken_result = check_stub(broken_stub)
        assert set(broken_result["missing_fields"]) == {"ticket", "reason", "moved_by", "remove_when"}, broken_result

        old_result = check_stub(old_stub)
        assert old_result["due_for_removal"], old_result

        stubs_found = set(find_stubs(root))
        assert stubs_found == {ok_stub, broken_stub, old_stub}, stubs_found

    print("demo(): alle Selbsttests gruen.")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--demo":
        demo()
        sys.exit(0)
    sys.exit(main(sys.argv))
