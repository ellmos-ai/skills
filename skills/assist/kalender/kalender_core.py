#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
kalender_core.py — Headless lokaler Kalender (SQLite, local-Backend).

Portiert aus: Eigenentwurf (kein BACH-Origin, kein Kalender-Service in BACH/system/ gefunden)
Store:        SQLite — assist/kalender/store.db (eigener Store, kein bach.db)
Abhaengigkeit: nur Python-Stdlib + sqlite3

Flag 3 — Backend-Wahl (in assist/prefs.json via 'kalender_backend'):
  local    → Dieser Core (Standard/Default)
  google   → Google-Calendar-MCP (LLM-Pfad; dieser Core wird nicht genutzt)
  routinika/uptoday → zukunftiger module-installer-Pfad (v0.2)
  nicht gesetzt → LLM fragt Nutzer interaktiv

Dieser Core implementiert ausschliesslich das 'local'-Backend.

Verwendung (CLI):
  python kalender_core.py add "Titel" --date YYYY-MM-DD [--time HH:MM] [--duration 60]
  python kalender_core.py today [--dry-run]
  python kalender_core.py week [--from YYYY-MM-DD] [--dry-run]
  python kalender_core.py month [--month YYYY-MM] [--dry-run]
  python kalender_core.py list [--search Begriff] [--limit 50] [--dry-run]
  python kalender_core.py delete <id>
  python kalender_core.py export [--id <id>] [--out kalender.ics]
  python kalender_core.py check-backend
  python kalender_core.py --store /tmp/kal.db today --dry-run
"""

from __future__ import annotations

import os
import sqlite3
import sys
import uuid
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Pfade (userneutral, relativ zum Skill)
# ---------------------------------------------------------------------------

_SKILL_DIR = Path(__file__).resolve().parent
_DEFAULT_STORE = _SKILL_DIR / "store.db"
_ENV_STORE = os.environ.get("KALENDER_STORE")


def _store_path(cli_override: Optional[str] = None) -> Path:
    if cli_override:
        return Path(cli_override)
    if _ENV_STORE:
        return Path(_ENV_STORE)
    return _DEFAULT_STORE


def _prefs_file() -> Optional[Path]:
    p = _SKILL_DIR.parent / "prefs.json"
    return p if p.exists() else None


def _read_pref(key: str, default=None):
    pf = _prefs_file()
    if not pf:
        return default
    try:
        import json
        return json.loads(pf.read_text(encoding="utf-8")).get(key, default)
    except Exception:  # noqa: BLE001
        return default


def _write_pref(key: str, value) -> None:
    import json
    p = _SKILL_DIR.parent / "prefs.json"
    data = {}
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            data = {}
    data[key] = value
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Store (SQLite)
# ---------------------------------------------------------------------------

_SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id           TEXT PRIMARY KEY,
    title        TEXT NOT NULL,
    date         TEXT NOT NULL,
    time         TEXT,
    duration_min INTEGER,
    location     TEXT,
    description  TEXT,
    recurrence   TEXT,
    ics_uid      TEXT UNIQUE,
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);
"""


def _open_store(store: Path) -> sqlite3.Connection:
    store.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(store))
    conn.row_factory = sqlite3.Row
    conn.executescript(_SCHEMA)
    conn.commit()
    return conn


def _short_id() -> str:
    return uuid.uuid4().hex[:8]


def _now() -> str:
    return datetime.now().isoformat()


def _ics_uid() -> str:
    return f"{uuid.uuid4()}@ellmos-kalender"


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

def add_event(store: Path, title: str, event_date: str,
              time: Optional[str] = None, duration_min: Optional[int] = None,
              location: Optional[str] = None, description: Optional[str] = None,
              recurrence: Optional[str] = None) -> str:
    """Legt einen Termin an; gibt die ID zurueck."""
    record_id = _short_id()
    now = _now()
    conn = _open_store(store)
    conn.execute(
        """INSERT INTO events
           (id, title, date, time, duration_min, location, description,
            recurrence, ics_uid, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            record_id, title, event_date, time, duration_min,
            location, description, recurrence, _ics_uid(), now, now,
        ),
    )
    conn.commit()
    conn.close()
    return record_id


def get_events_by_date_range(store: Path, from_date: str,
                              to_date: str) -> list[dict]:
    if not store.exists():
        return []
    conn = _open_store(store)
    rows = conn.execute(
        """SELECT * FROM events
           WHERE date BETWEEN ? AND ?
           ORDER BY date ASC, time ASC""",
        (from_date, to_date),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def list_events(store: Path, search: Optional[str] = None,
                limit: int = 50) -> list[dict]:
    if not store.exists():
        return []
    conn = _open_store(store)
    if search:
        rows = conn.execute(
            """SELECT * FROM events
               WHERE LOWER(title) LIKE ? OR LOWER(description) LIKE ?
               ORDER BY date ASC, time ASC LIMIT ?""",
            (f"%{search.lower()}%", f"%{search.lower()}%", limit),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM events ORDER BY date ASC, time ASC LIMIT ?",
            (limit,),
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_event(store: Path, record_id: str) -> bool:
    if not store.exists():
        return False
    conn = _open_store(store)
    cursor = conn.execute("DELETE FROM events WHERE id = ?", (record_id,))
    conn.commit()
    changed = cursor.rowcount > 0
    conn.close()
    return changed


# ---------------------------------------------------------------------------
# ICS-Export (RFC 5545 Subset — kein externer Parser noetig)
# ---------------------------------------------------------------------------

def _escape_ics(text: str) -> str:
    """Escaped ICS-Sonderzeichen (Komma, Semikolon, Backslash, Newline)."""
    return (text or "").replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")


def _ics_date(event_date: str, event_time: Optional[str] = None) -> str:
    """Gibt DTSTART-Wert im ICS-Format zurueck."""
    if event_time:
        dt_str = f"{event_date.replace('-', '')}T{event_time.replace(':', '')}00"
        return f"DTSTART:{dt_str}"
    return f"DTSTART;VALUE=DATE:{event_date.replace('-', '')}"


def export_ics(store: Path, record_id: Optional[str] = None) -> str:
    """Erzeugt einen ICS-String (VCALENDAR) fuer einen oder alle Termine."""
    if record_id:
        if not store.exists():
            return ""
        conn = _open_store(store)
        row = conn.execute("SELECT * FROM events WHERE id = ?", (record_id,)).fetchone()
        conn.close()
        events = [dict(row)] if row else []
    else:
        events = list_events(store, limit=10000)

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//ellmos-assist//kalender//DE",
        "CALSCALE:GREGORIAN",
    ]
    for ev in events:
        uid = ev.get("ics_uid") or _ics_uid()
        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"SUMMARY:{_escape_ics(ev['title'])}",
            _ics_date(ev["date"], ev.get("time")),
        ]
        if ev.get("duration_min"):
            h, m = divmod(int(ev["duration_min"]), 60)
            lines.append(f"DURATION:PT{h}H{m}M")
        if ev.get("location"):
            lines.append(f"LOCATION:{_escape_ics(ev['location'])}")
        if ev.get("description"):
            lines.append(f"DESCRIPTION:{_escape_ics(ev['description'])}")
        if ev.get("recurrence"):
            lines.append(f"RRULE:{ev['recurrence']}")
        dtstamp = datetime.now().strftime("%Y%m%dT%H%M%SZ")
        lines.append(f"DTSTAMP:{dtstamp}")
        lines.append("END:VEVENT")

    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


# ---------------------------------------------------------------------------
# Dry-Run-Beispieldaten
# ---------------------------------------------------------------------------

_DRY_EVENTS = [
    {"id": "evt-1", "title": "Zahnarzt", "date": date.today().isoformat(),
     "time": "10:00", "duration_min": 60, "location": "Praxis Dr. Muster", "description": ""},
    {"id": "evt-2", "title": "Team-Meeting", "date": date.today().isoformat(),
     "time": "14:00", "duration_min": 90, "location": "", "description": "Wochentlich"},
    {"id": "evt-3", "title": "Sport", "date": (date.today() + timedelta(days=2)).isoformat(),
     "time": "08:00", "duration_min": 60, "location": "Fitnessstudio", "description": ""},
]


# ---------------------------------------------------------------------------
# Formatierung
# ---------------------------------------------------------------------------

def _fmt_event(ev: dict) -> str:
    t = f" {ev['time']}" if ev.get("time") else ""
    dur = f" ({ev['duration_min']} min)" if ev.get("duration_min") else ""
    loc = f" @ {ev['location']}" if ev.get("location") else ""
    desc = f" — {ev['description']}" if ev.get("description") else ""
    return f"  [{ev['id']}] {ev['date']}{t}{dur} | {ev['title']}{loc}{desc}"


# ---------------------------------------------------------------------------
# Backend-Check
# ---------------------------------------------------------------------------

def cmd_check_backend() -> int:
    backend = _read_pref("kalender_backend")
    if not backend:
        print("[kalender] Kein Backend in prefs.json konfiguriert.")
        print("  Das LLM wird den Nutzer interaktiv nach dem bevorzugten Backend fragen.")
        print("  Optionen: local | google | routinika | uptoday")
        print("  Setzen via: prefs.json -> kalender_backend: \"local\"")
    elif backend == "local":
        print("[kalender] Backend: lokal (SQLite-Store, dieser Core)")
    elif backend == "google":
        print("[kalender] Backend: Google Calendar MCP (LLM-gesteuert, dieser Core inaktiv)")
    else:
        print(f"[kalender] Backend: {backend!r} (via module-installer, ab v0.2)")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _resolve_store_from_args(args: list[str]) -> tuple[Path, list[str]]:
    if "--store" in args:
        idx = args.index("--store")
        if idx + 1 < len(args):
            store = Path(args[idx + 1])
            remaining = args[:idx] + args[idx + 2:]
            return store, remaining
    return _store_path(), args


def main(argv: Optional[list] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 0

    store, argv = _resolve_store_from_args(argv)
    dry_run = "--dry-run" in argv
    argv = [a for a in argv if a != "--dry-run"]

    if not argv:
        print(__doc__)
        return 0

    cmd = argv[0].lower()

    # --- check-backend ---
    if cmd == "check-backend":
        return cmd_check_backend()

    # --- add ---
    if cmd == "add":
        if len(argv) < 2:
            print('Verwendung: kalender_core.py add "Titel" --date YYYY-MM-DD [--time HH:MM] [--duration min] [--location "..."] [--note "..."]')
            return 1
        args = argv[1:]
        title = args[0]
        event_date = None
        time_ = None
        duration_min = None
        location = None
        description = None

        def _get_arg(flag: str) -> Optional[str]:
            if flag in args:
                idx = args.index(flag)
                return args[idx + 1] if idx + 1 < len(args) else None
            return None

        event_date = _get_arg("--date")
        time_ = _get_arg("--time")
        location = _get_arg("--location")
        description = _get_arg("--note")
        dur_s = _get_arg("--duration")
        if dur_s:
            try:
                duration_min = int(dur_s)
            except ValueError:
                pass

        if not event_date:
            print("[kalender] --date YYYY-MM-DD ist Pflicht.")
            return 1

        if dry_run:
            print(f"[DRY-RUN] Wuerde Termin anlegen: {title!r} am {event_date} {time_ or ''}")
            return 0
        record_id = add_event(store, title, event_date, time_, duration_min,
                               location, description)
        print(f"[kalender] Termin gespeichert: {title!r} am {event_date} [{record_id}]")
        return 0

    # --- today ---
    if cmd == "today":
        today_str = date.today().isoformat()
        print(f"=== Heute ({today_str}) ===")
        if dry_run:
            events = [e for e in _DRY_EVENTS if e["date"] == today_str]
            print("[DRY-RUN] Beispiel-Termine:")
        else:
            events = get_events_by_date_range(store, today_str, today_str)
        if not events:
            print("  Keine Termine heute.")
        else:
            for ev in events:
                print(_fmt_event(ev))
        return 0

    # --- week ---
    if cmd == "week":
        from_str = date.today().isoformat()
        if "--from" in argv:
            idx = argv.index("--from")
            if idx + 1 < len(argv):
                from_str = argv[idx + 1]
        from_d = date.fromisoformat(from_str)
        to_str = (from_d + timedelta(days=6)).isoformat()
        print(f"=== Woche ({from_str} – {to_str}) ===")
        if dry_run:
            events = _DRY_EVENTS
            print("[DRY-RUN] Beispiel-Termine:")
        else:
            events = get_events_by_date_range(store, from_str, to_str)
        if not events:
            print("  Keine Termine diese Woche.")
            return 0
        cur_day = ""
        for ev in events:
            if ev["date"] != cur_day:
                print(f"\n  {ev['date']}")
                cur_day = ev["date"]
            print(_fmt_event(ev))
        return 0

    # --- month ---
    if cmd == "month":
        month_str = date.today().strftime("%Y-%m")
        if "--month" in argv:
            idx = argv.index("--month")
            if idx + 1 < len(argv):
                month_str = argv[idx + 1]
        from_str = f"{month_str}-01"
        # Letzten Tag des Monats berechnen (stdlib-only)
        y, m = int(month_str[:4]), int(month_str[5:7])
        next_m_y, next_m = (y + 1, 1) if m == 12 else (y, m + 1)
        to_str = (date(next_m_y, next_m, 1) - timedelta(days=1)).isoformat()
        print(f"=== Monat {month_str} ({from_str} – {to_str}) ===")
        if dry_run:
            events = _DRY_EVENTS
            print("[DRY-RUN] Beispiel-Termine:")
        else:
            events = get_events_by_date_range(store, from_str, to_str)
        if not events:
            print("  Keine Termine in diesem Monat.")
            return 0
        for ev in events:
            print(_fmt_event(ev))
        return 0

    # --- list ---
    if cmd == "list":
        args = argv[1:]
        search = None
        limit = 50
        if "--search" in args:
            idx = args.index("--search")
            if idx + 1 < len(args):
                search = args[idx + 1]
        if "--limit" in args:
            idx = args.index("--limit")
            if idx + 1 < len(args):
                try:
                    limit = int(args[idx + 1])
                except ValueError:
                    pass
        if dry_run:
            events = _DRY_EVENTS
            print("[DRY-RUN] Beispiel-Termine:")
        else:
            events = list_events(store, search, limit)
        label = f"(Suche: {search!r})" if search else ""
        print(f"=== Termine {label} ({len(events)}) ===")
        if not events:
            print("  Keine Termine gefunden.")
        else:
            for ev in events:
                print(_fmt_event(ev))
        return 0

    # --- delete ---
    if cmd == "delete":
        if len(argv) < 2:
            print("Verwendung: kalender_core.py delete <id>")
            return 1
        record_id = argv[1]
        if dry_run:
            print(f"[DRY-RUN] Wuerde Termin {record_id!r} loeschen.")
            return 0
        ok = delete_event(store, record_id)
        if ok:
            print(f"[kalender] Termin {record_id!r} geloescht.")
        else:
            print(f"[kalender] Termin {record_id!r} nicht gefunden.")
        return 0 if ok else 1

    # --- export ---
    if cmd == "export":
        args = argv[1:]
        record_id = None
        out_path = None
        if "--id" in args:
            idx = args.index("--id")
            if idx + 1 < len(args):
                record_id = args[idx + 1]
        if "--out" in args:
            idx = args.index("--out")
            if idx + 1 < len(args):
                out_path = args[idx + 1]
        if dry_run:
            print("[DRY-RUN] ICS-Export uebersprungen.")
            return 0
        ics_content = export_ics(store, record_id)
        if not ics_content.strip():
            print("[kalender] Keine Termine zum Exportieren.")
            return 0
        if out_path:
            Path(out_path).write_text(ics_content, encoding="utf-8")
            print(f"[kalender] ICS exportiert: {out_path}")
        else:
            print(ics_content)
        return 0

    print(f"Unbekannter Befehl: {cmd!r}")
    print("Verfuegbar: add, today, week, month, list, delete, export, check-backend")
    return 1


if __name__ == "__main__":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.exit(main())
