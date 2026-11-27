#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
kalender_core.py — Lokaler Multi-Silo-Kalender & Berichtsgenerator (v0.3.0).

Eigenschaften:
  - Lokaler SQLite-Store (`store.db`, überschreibbar per `--store` oder `KALENDER_STORE`)
  - Externe Konfiguration via `kalender-config.json` (+ Selbstheilung mit `.corrupt.<ts>.bak`)
  - Austauschbare Vorlagen unter `templates/` (`.template.html`, `.template.md`, `.template.txt`)
  - 100 % Python-Stdlib (`sqlite3`, `calendar`, `datetime`, `html`, `json`, ...)
  - Getrennte Kalender-Silos/Profile (`user`, `tickets`, `finanzen`, `gesundheit`,
    `geburtstage_privat`, `geburtstage_beruflich`, `terminpilot`, `routinen` + eigene)
  - Verlustfreie additive Migration bestehender v0.1-Datenbanken
  - Silo-Operationen (`mirror`, `sync-mirrors`, `transfer`, `clone`)
  - Idempotenter RFC-5545-ICS-Import (`import-ics`, ideal für TerminPilot) & -Export
  - Grafisches Kalenderblatt & Berichtsgenerator (`html`, `pdf`, `md`, `txt`, `ics`)

Flag 3 — Backend-Wahl (in `assist/prefs.json` via `kalender_backend`):
  local             -> Dieser Core (Standard/Default)
  google            -> Google-Calendar-MCP (LLM-Pfad; dieser Core bleibt lokal)
  routinika/uptoday -> zukünftiger module-installer-Pfad
  nicht gesetzt     -> LLM fragt Nutzer interaktiv
"""

from __future__ import annotations

import calendar as pycalendar
import copy
import html
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import uuid
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping, Optional

__version__ = "0.3.0"

# ---------------------------------------------------------------------------
# Pfade, Konfiguration (Selbstheilung) & Präferenzen
# ---------------------------------------------------------------------------

_SKILL_DIR = Path(__file__).resolve().parent
_DEFAULT_STORE = _SKILL_DIR / "store.db"
_BASE_CONFIG_NAME = "kalender-config.json"

DEFAULT_CALENDARS: tuple[tuple[str, str, str, str, str, int], ...] = (
    ("user", "Nutzerkalender", "personal", "#2563eb", "Persönlicher Standardkalender", 1),
    ("tickets", "Ticket-Kalender", "tasks", "#7c3aed", "Eingeplante Tickets und Arbeitsblöcke", 0),
    ("finanzen", "Finanzkalender / Zahlungstermine", "finance", "#059669", "Zahlungstermine, Fristen und Buchungen", 0),
    ("gesundheit", "Arzttermine & Gesundheit", "health", "#dc2626", "Arztbesuche, Vorsorge und Gesundheit", 0),
    ("geburtstage_privat", "Geburtstage (privat)", "birthdays", "#db2777", "Private Geburtstage und Jahrestage", 0),
    ("geburtstage_beruflich", "Geburtstage (beruflich)", "birthdays", "#d97706", "Berufliche Geburtstage und Jubiläen", 0),
    ("terminpilot", "TerminPilot / Terminabstimmung", "coordination", "#0891b2", "Terminabstimmungen und TerminPilot-Importe", 0),
    ("routinen", "Routinen", "routines", "#4b5563", "Wiederkehrende Routinen", 0),
)

_DEFAULT_KALENDER_CONFIG: dict[str, Any] = {
    "schema": "ocean.skill-config.v2",
    "skill": "kalender",
    "version": "0.3.0",
    "self_healing": {
        "enabled": True,
        "backup_suffix": ".corrupt.<ts>.bak",
        "atomic_writes": True,
    },
    "defaults": {
        "calendar": "user",
        "import_calendar": "terminpilot",
        "date_format": "%Y-%m-%d",
        "time_format": "%H:%M",
        "first_weekday": 0,
        "default_list_limit": 50,
        "default_color": "#3b82f6",
    },
    "silos": [
        {
            "id": cid,
            "name": cname,
            "category": ccat,
            "color": ccol,
            "description": cdesc,
            "is_default": is_def,
        }
        for cid, cname, ccat, ccol, cdesc, is_def in DEFAULT_CALENDARS
    ],
    "output": {
        "default_format": "html",
        "default_view": "month",
        "supported_formats": ["html", "pdf", "md", "txt", "ics"],
        "max_chips_per_day_md": 4,
        "output_dir": "./output",
    },
    "templates": {
        "dir": "./templates",
        "month_html": "month-sheet.template.html",
        "week_html": "week-sheet.template.html",
        "report_html": "agenda-report.template.html",
        "report_md": "agenda-report.template.md",
        "report_txt": "agenda-report.template.txt",
        "custom_dir": None,
    },
    "delivery": {
        "enabled": False,
        "dry_run": True,
        "mode": "draft",
    },
}


def _deep_merge(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = copy.deepcopy(dict(base))
    for key, val in override.items():
        if key in ("_hinweis", "_comment") and key in merged:
            continue
        if isinstance(merged.get(key), dict) and isinstance(val, dict):
            merged[key] = _deep_merge(merged[key], val)
        else:
            merged[key] = copy.deepcopy(val)
    return merged


def _atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(dict(payload), ensure_ascii=False, indent=2) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(serialized)
        os.replace(tmp_name, str(path))
    except Exception:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
        raise


def load_kalender_config(
    *,
    skill_root: Path = _SKILL_DIR,
    repair: bool = False,
) -> dict[str, Any]:
    """Lädt kalender-config.json -> config.json mit Selbstheilung (.corrupt.<ts>.bak)."""
    warnings: list[str] = []
    healed: list[dict[str, str]] = []
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    effective = copy.deepcopy(_DEFAULT_KALENDER_CONFIG)

    for idx, filename in enumerate((_BASE_CONFIG_NAME, "config.json")):
        candidate = skill_root / filename
        if not candidate.is_file():
            continue
        try:
            raw = json.loads(candidate.read_text(encoding="utf-8-sig"))
            if not isinstance(raw, dict):
                raise ValueError("JSON root must be object")
            effective = _deep_merge(effective, raw)
        except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
            warnings.append(f"{candidate.name}: corrupt config ({exc}); fell back to defaults")
            if repair:
                bak = candidate.with_name(f"{candidate.name}.corrupt.{ts}.bak")
                shutil.copy2(str(candidate), str(bak))
                _atomic_write_json(candidate, _DEFAULT_KALENDER_CONFIG if idx == 0 else {})
                healed.append({"path": str(candidate), "backup_path": str(bak)})

    pref_def_cal = _read_pref("kalender_default_calendar", None)
    if isinstance(pref_def_cal, str) and pref_def_cal.strip():
        effective["defaults"]["calendar"] = pref_def_cal.strip().lower()
    pref_def_fmt = _read_pref("kalender_default_format", None)
    if isinstance(pref_def_fmt, str) and pref_def_fmt.strip().lower() in VALID_REPORT_FORMATS:
        effective["output"]["default_format"] = pref_def_fmt.strip().lower()

    return {"config": effective, "warnings": warnings, "healed": healed}


def _silo_rows_from_config(cfg: Mapping[str, Any] | None) -> tuple[tuple[str, str, str, str, str, int], ...]:
    raw_silos = (cfg or {}).get("silos")
    if not isinstance(raw_silos, list) or not raw_silos:
        return DEFAULT_CALENDARS
    rows: list[tuple[str, str, str, str, str, int]] = []
    for entry in raw_silos:
        if not isinstance(entry, dict):
            continue
        cid = str(entry.get("id") or "").strip().lower()
        cname = str(entry.get("name") or cid).strip()
        if not cid or not cname:
            continue
        ccat = str(entry.get("category") or "personal").strip().lower()
        ccol = str(entry.get("color") or "#3b82f6").strip()
        cdesc = str(entry.get("description") or "").strip()
        is_def = 1 if entry.get("is_default") else 0
        rows.append((cid, cname, ccat, ccol, cdesc, is_def))
    return tuple(rows) if rows else DEFAULT_CALENDARS


def _resolve_template_path(
    template_key: str,
    *,
    cfg: Mapping[str, Any],
    skill_root: Path = _SKILL_DIR,
) -> Path:
    tpl_cfg = cfg.get("templates") if isinstance(cfg.get("templates"), dict) else {}
    default_tpls = _DEFAULT_KALENDER_CONFIG["templates"]
    filename = str(tpl_cfg.get(template_key) or default_tpls.get(template_key) or template_key)
    search_dirs: list[Path] = []
    custom_dir = tpl_cfg.get("custom_dir")
    if isinstance(custom_dir, str) and custom_dir.strip():
        cpath = Path(custom_dir)
        search_dirs.append(cpath if cpath.is_absolute() else (skill_root / cpath))
    rel_dir = str(tpl_cfg.get("dir") or "./templates")
    dpath = Path(rel_dir)
    search_dirs.append(dpath if dpath.is_absolute() else (skill_root / dpath))
    search_dirs.append(_SKILL_DIR / "templates")
    for folder in search_dirs:
        candidate = folder / filename
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f"Template {filename!r} not found in {search_dirs}")


def _store_path(cli_override: Optional[str] = None) -> Path:
    """Löst den Pfad zur SQLite-Datei auf (`--store` > `KALENDER_STORE` > Default)."""
    if cli_override:
        return Path(cli_override)
    env_store = os.environ.get("KALENDER_STORE")
    if env_store:
        return Path(env_store)
    return _DEFAULT_STORE


def _prefs_file() -> Optional[Path]:
    p = _SKILL_DIR.parent / "prefs.json"
    return p if p.exists() else None


def _read_pref(key: str, default: Any = None) -> Any:
    pf = _prefs_file()
    if not pf:
        return default
    try:
        return json.loads(pf.read_text(encoding="utf-8")).get(key, default)
    except Exception:  # noqa: BLE001
        return default


def _write_pref(key: str, value: Any) -> None:
    p = _SKILL_DIR.parent / "prefs.json"
    data: dict[str, Any] = {}
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            data = {}
    data[key] = value
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Standard-Kalender-Silos & additives SQLite-Schema (v0.1 -> v0.3)
# ---------------------------------------------------------------------------

_CALENDAR_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
_COLOR_HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_MONTH_RE = re.compile(r"^\d{4}-(?:0[1-9]|1[0-2])$")
_YEAR_RE = re.compile(r"^\d{4}$")
_HHMM_RE = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")

VALID_LINK_MODES = (None, "mirror", "transfer", "clone")
VALID_REPORT_VIEWS = ("day", "week", "month", "year", "range")
VALID_REPORT_FORMATS = ("html", "md", "txt", "ics", "pdf")

WEEKDAYS_SHORT_DE = ("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So")
MONTHS_DE = (
    "",
    "Januar",
    "Februar",
    "März",
    "April",
    "Mai",
    "Juni",
    "Juli",
    "August",
    "September",
    "Oktober",
    "November",
    "Dezember",
)

_BASE_SCHEMA = """
CREATE TABLE IF NOT EXISTS calendars (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    category    TEXT,
    color       TEXT,
    description TEXT,
    is_default  INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id                 TEXT PRIMARY KEY,
    title              TEXT NOT NULL,
    date               TEXT NOT NULL,
    time               TEXT,
    duration_min       INTEGER,
    location           TEXT,
    description        TEXT,
    recurrence         TEXT,
    ics_uid            TEXT UNIQUE,
    created_at         TEXT NOT NULL,
    updated_at         TEXT NOT NULL,
    calendar_id        TEXT NOT NULL DEFAULT 'user',
    category           TEXT,
    source_calendar_id TEXT,
    source_event_id    TEXT,
    link_mode          TEXT,
    external_id        TEXT,
    end_time           TEXT,
    status             TEXT NOT NULL DEFAULT 'planned'
);
"""

_ADDITIVE_EVENT_COLUMNS: tuple[tuple[str, str], ...] = (
    ("calendar_id", "TEXT NOT NULL DEFAULT 'user'"),
    ("category", "TEXT"),
    ("source_calendar_id", "TEXT"),
    ("source_event_id", "TEXT"),
    ("link_mode", "TEXT"),
    ("external_id", "TEXT"),
    ("end_time", "TEXT"),
    ("status", "TEXT NOT NULL DEFAULT 'planned'"),
)


def _short_id() -> str:
    return uuid.uuid4().hex[:8]


def _now() -> str:
    return datetime.now().isoformat()


def _ics_uid() -> str:
    return f"{uuid.uuid4()}@ellmos-kalender"


def _migrate_and_seed(conn: sqlite3.Connection, *, cfg: Mapping[str, Any] | None = None) -> None:
    """Führt additive Schema-Migrationen durch und legt die Standard-Silos an."""
    conn.executescript(_BASE_SCHEMA)

    existing_cols = {
        str(row[1]) for row in conn.execute("PRAGMA table_info(events)").fetchall()
    }
    for col_name, col_ddl in _ADDITIVE_EVENT_COLUMNS:
        if col_name not in existing_cols:
            conn.execute(f"ALTER TABLE events ADD COLUMN {col_name} {col_ddl}")

    conn.execute(
        "UPDATE events SET calendar_id = 'user' WHERE calendar_id IS NULL OR TRIM(calendar_id) = ''"
    )
    conn.execute(
        "UPDATE events SET status = 'planned' WHERE status IS NULL OR TRIM(status) = ''"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_events_date ON events(date, time)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_events_calendar_date ON events(calendar_id, date)"
    )

    active_cfg = cfg if cfg is not None else load_kalender_config()["config"]
    silo_rows = _silo_rows_from_config(active_cfg)
    now_str = _now()
    for cal_id, name, cat, color, desc, is_def in silo_rows:
        conn.execute(
            """INSERT OR IGNORE INTO calendars
               (id, name, category, color, description, is_default, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (cal_id, name, cat, color, desc, is_def, now_str),
        )
    conn.commit()


def _open_store(store: Path, *, cfg: Mapping[str, Any] | None = None) -> sqlite3.Connection:
    """Öffnet den SQLite-Store und stellt Tabellen & Standard-Silos sicher."""
    store.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(store))
    conn.row_factory = sqlite3.Row
    _migrate_and_seed(conn, cfg=cfg)
    return conn


# ---------------------------------------------------------------------------
# Validierungs- & Filter-Helfer
# ---------------------------------------------------------------------------

def _validate_date(value: str) -> str:
    clean = str(value or "").strip()
    if not _DATE_RE.fullmatch(clean):
        raise ValueError(f"Ungültiges Datum {value!r} (erwartet YYYY-MM-DD)")
    date.fromisoformat(clean)
    return clean


def _validate_time(value: Optional[str], field: str = "time") -> Optional[str]:
    if value is None or str(value).strip() == "":
        return None
    clean = str(value).strip()
    if len(clean) >= 5 and _HHMM_RE.fullmatch(clean[:5]):
        return clean[:5]
    raise ValueError(f"Ungültige Uhrzeit für {field}: {value!r} (erwartet HH:MM)")


def _compute_end_time(start_time: Optional[str], duration_min: Optional[int]) -> Optional[str]:
    if not start_time or not duration_min or duration_min <= 0:
        return None
    t_val = time(int(start_time[:2]), int(start_time[3:5]))
    dt = datetime.combine(date(2026, 1, 1), t_val) + timedelta(minutes=int(duration_min))
    return dt.strftime("%H:%M")


def parse_calendar_filter(raw: Optional[str]) -> Optional[list[str]]:
    """Parst `--calendar`: `None`/`'all'`/`'*'` -> `None` (alle Silos), sonst Liste."""
    if raw is None:
        return None
    clean = str(raw).strip()
    if not clean or clean.lower() in {"all", "*"}:
        return None
    items = [part.strip().lower() for part in clean.split(",") if part.strip()]
    return items or None


def _ensure_calendar_exists(conn: sqlite3.Connection, calendar_id: str) -> sqlite3.Row:
    row = conn.execute("SELECT * FROM calendars WHERE id = ?", (calendar_id,)).fetchone()
    if row is None:
        raise ValueError(
            f"Unbekannter Kalender {calendar_id!r}. Verfügbare Kalender mit 'calendar list' prüfen "
            f"oder mit 'calendar add {calendar_id} --name \"...\"' anlegen."
        )
    return row


def _enrich_event_row(row: sqlite3.Row | dict[str, Any]) -> dict[str, Any]:
    d = dict(row)
    cal_id = d.get("calendar_id") or "user"
    d["calendar_id"] = cal_id
    d.setdefault("calendar_name", cal_id)
    d.setdefault("calendar_color", "#4b5563")
    d.setdefault("calendar_category", None)
    if not d.get("end_time") and d.get("time") and d.get("duration_min"):
        d["end_time"] = _compute_end_time(d["time"], d["duration_min"])
    d["effective_category"] = d.get("category") or d.get("calendar_category")
    return d


# ---------------------------------------------------------------------------
# Kalender-Profile / Silo-Verwaltung
# ---------------------------------------------------------------------------

def list_calendars(store: Path) -> list[dict[str, Any]]:
    """Gibt alle konfigurierten Kalender-Profile samt Terminanzahl zurück."""
    conn = _open_store(store)
    try:
        rows = conn.execute(
            """SELECT c.*, COUNT(e.id) AS event_count
               FROM calendars c
               LEFT JOIN events e ON e.calendar_id = c.id
               GROUP BY c.id
               ORDER BY c.is_default DESC, c.id ASC"""
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def add_calendar(
    store: Path,
    calendar_id: str,
    name: str,
    *,
    category: Optional[str] = None,
    color: Optional[str] = None,
    description: Optional[str] = None,
) -> dict[str, Any]:
    """Legt ein neues Kalender-Silo an oder gibt Fehler bei ungültiger ID/Duplikat."""
    cal_id = str(calendar_id or "").strip().lower()
    if not _CALENDAR_ID_RE.fullmatch(cal_id):
        raise ValueError(
            f"Ungültige Kalender-ID {calendar_id!r} (erlaubt: [a-z0-9][a-z0-9_-]{{0,63}})"
        )
    if cal_id == "all":
        raise ValueError("Kalender-ID 'all' ist für den gemergten Gesamtkalender reserviert.")
    clean_name = str(name or "").strip()
    if not clean_name:
        raise ValueError("Kalendername (--name) darf nicht leer sein.")
    cfg = load_kalender_config()["config"]
    default_col = str((cfg.get("defaults") or {}).get("default_color") or "#3b82f6")
    clean_color = str(color).strip() if color else default_col
    if not _COLOR_HEX_RE.fullmatch(clean_color):
        raise ValueError(f"Ungültiger Hex-Farbwert {clean_color!r} (erwartet z. B. '#2563eb').")
    clean_cat = str(category).strip().lower() if category and str(category).strip() else None
    clean_desc = str(description).strip() if description else ""

    conn = _open_store(store)
    try:
        if conn.execute("SELECT 1 FROM calendars WHERE id = ?", (cal_id,)).fetchone():
            raise ValueError(f"Kalender {cal_id!r} existiert bereits.")
        created_at = _now()
        conn.execute(
            """INSERT INTO calendars (id, name, category, color, description, is_default, created_at)
               VALUES (?, ?, ?, ?, ?, 0, ?)""",
            (cal_id, clean_name, clean_cat, clean_color, clean_desc, created_at),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM calendars WHERE id = ?", (cal_id,)).fetchone()
        return dict(row)
    finally:
        conn.close()


def delete_calendar(store: Path, calendar_id: str) -> bool:
    """Löscht ein benutzerdefiniertes Kalender-Silo (schützt `user` / `is_default=1`)."""
    cal_id = str(calendar_id or "").strip().lower()
    if cal_id == "user":
        raise ValueError("Der Standardkalender 'user' ist geschützt und kann nicht gelöscht werden.")
    if not store.exists():
        return False
    conn = _open_store(store)
    try:
        row = conn.execute("SELECT * FROM calendars WHERE id = ?", (cal_id,)).fetchone()
        if row is None:
            return False
        if int(row["is_default"] or 0) == 1:
            raise ValueError(f"Standardkalender {cal_id!r} kann nicht gelöscht werden.")
        conn.execute("DELETE FROM calendars WHERE id = ?", (cal_id,))
        conn.commit()
        return True
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Termin-CRUD & Abfragen
# ---------------------------------------------------------------------------

def add_event(
    store: Path,
    title: str,
    event_date: str,
    time: Optional[str] = None,
    duration_min: Optional[int] = None,
    location: Optional[str] = None,
    description: Optional[str] = None,
    recurrence: Optional[str] = None,
    *,
    calendar_id: str = "user",
    category: Optional[str] = None,
    end_time: Optional[str] = None,
    external_id: Optional[str] = None,
    status: str = "planned",
    ics_uid: Optional[str] = None,
) -> str:
    """Legt einen Termin im gewählten Silo an (Default: `user`) und gibt die ID zurück."""
    clean_title = str(title or "").strip()
    if not clean_title:
        raise ValueError("Termin-Titel darf nicht leer sein.")
    clean_date = _validate_date(event_date)
    clean_time = _validate_time(time, "time")
    clean_end = _validate_time(end_time, "end_time")
    cal_id = str(calendar_id or "user").strip().lower()
    dur_val = int(duration_min) if duration_min is not None else None
    if clean_end is None and clean_time and dur_val:
        clean_end = _compute_end_time(clean_time, dur_val)

    conn = _open_store(store)
    try:
        cal_row = _ensure_calendar_exists(conn, cal_id)
        eff_cat = (
            str(category).strip().lower()
            if category and str(category).strip()
            else cal_row["category"]
        )
        record_id = _short_id()
        while conn.execute("SELECT 1 FROM events WHERE id = ?", (record_id,)).fetchone():
            record_id = _short_id()
        now_str = _now()
        uid_val = ics_uid or _ics_uid()
        conn.execute(
            """INSERT INTO events
               (id, title, date, time, duration_min, location, description,
                recurrence, ics_uid, created_at, updated_at, calendar_id,
                category, end_time, external_id, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                record_id,
                clean_title,
                clean_date,
                clean_time,
                dur_val,
                location,
                description,
                recurrence,
                uid_val,
                now_str,
                now_str,
                cal_id,
                eff_cat,
                clean_end,
                external_id,
                status or "planned",
            ),
        )
        conn.commit()
        return record_id
    finally:
        conn.close()


def _query_events(
    store: Path,
    *,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    calendar: Optional[str] = "all",
    category: Optional[str] = None,
    search: Optional[str] = None,
    limit: Optional[int] = None,
    record_id: Optional[str] = None,
) -> list[dict[str, Any]]:
    if not store.exists():
        return []
    conn = _open_store(store)
    try:
        clauses: list[str] = []
        params: list[Any] = []

        if record_id is not None:
            clauses.append("e.id = ?")
            params.append(record_id)
        if from_date is not None and to_date is not None:
            clauses.append("e.date BETWEEN ? AND ?")
            params.extend([from_date, to_date])
        elif from_date is not None:
            clauses.append("e.date >= ?")
            params.append(from_date)
        elif to_date is not None:
            clauses.append("e.date <= ?")
            params.append(to_date)

        cal_ids = parse_calendar_filter(calendar)
        if cal_ids:
            placeholders = ", ".join("?" for _ in cal_ids)
            clauses.append(f"LOWER(e.calendar_id) IN ({placeholders})")
            params.extend(cal_ids)

        if category and str(category).strip():
            cat_norm = str(category).strip().lower()
            clauses.append("LOWER(COALESCE(e.category, c.category, '')) = ?")
            params.append(cat_norm)

        if search and str(search).strip():
            needle = f"%{str(search).strip().lower()}%"
            clauses.append(
                "(LOWER(e.title) LIKE ? OR LOWER(COALESCE(e.description, '')) LIKE ? "
                "OR LOWER(COALESCE(e.location, '')) LIKE ?)"
            )
            params.extend([needle, needle, needle])

        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        limit_sql = "LIMIT ?" if limit is not None else ""
        if limit is not None:
            params.append(int(limit))

        sql = f"""
            SELECT e.*,
                   COALESCE(c.name, e.calendar_id) AS calendar_name,
                   COALESCE(c.color, '#4b5563') AS calendar_color,
                   c.category AS calendar_category
            FROM events e
            LEFT JOIN calendars c ON c.id = e.calendar_id
            {where_sql}
            ORDER BY e.date ASC, COALESCE(e.time, '') ASC, e.id ASC
            {limit_sql}
        """
        rows = conn.execute(sql, params).fetchall()
        return [_enrich_event_row(r) for r in rows]
    finally:
        conn.close()


def get_events_by_date_range(
    store: Path,
    from_date: str,
    to_date: str,
    *,
    calendar: Optional[str] = "all",
    category: Optional[str] = None,
    search: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Gibt alle Termine im Datumsbereich `[from_date, to_date]` zurück."""
    return _query_events(
        store,
        from_date=_validate_date(from_date),
        to_date=_validate_date(to_date),
        calendar=calendar,
        category=category,
        search=search,
    )


def list_events(
    store: Path,
    search: Optional[str] = None,
    limit: int = 50,
    *,
    calendar: Optional[str] = "all",
    category: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Listet Termine gefiltert nach Silo, Kategorie, Zeitraum und Suchbegriff."""
    return _query_events(
        store,
        from_date=_validate_date(from_date) if from_date else None,
        to_date=_validate_date(to_date) if to_date else None,
        calendar=calendar,
        category=category,
        search=search,
        limit=limit,
    )


def delete_event(store: Path, record_id: str) -> bool:
    """Löscht einen Termin anhand seiner ID."""
    if not store.exists():
        return False
    conn = _open_store(store)
    try:
        cursor = conn.execute("DELETE FROM events WHERE id = ?", (record_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Silo-Operationen: mirror, sync-mirrors, transfer, clone
# ---------------------------------------------------------------------------

def mirror_event(store: Path, event_id: str, target_calendar_id: str) -> dict[str, Any]:
    """Spiegelt einen Termin idempotent in ein Ziel-Silo (`link_mode='mirror'`)."""
    target_cal = str(target_calendar_id or "").strip().lower()
    conn = _open_store(store)
    try:
        _ensure_calendar_exists(conn, target_cal)
        src = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
        if src is None:
            raise ValueError(f"Quelltermin {event_id!r} nicht gefunden.")
        root_id = str(src["source_event_id"] or src["id"]) if src["link_mode"] == "mirror" else str(src["id"])
        root_cal = str(src["source_calendar_id"] or src["calendar_id"]) if src["link_mode"] == "mirror" else str(src["calendar_id"])
        if root_cal == target_cal or str(src["calendar_id"]) == target_cal:
            raise ValueError(f"Termin liegt bereits im Ziel-Kalender {target_cal!r}.")

        existing = conn.execute(
            """SELECT id FROM events
               WHERE calendar_id = ? AND source_event_id = ? AND link_mode = 'mirror'""",
            (target_cal, root_id),
        ).fetchone()
        now_str = _now()

        if existing is not None:
            mirror_id = str(existing["id"])
            conn.execute(
                """UPDATE events
                   SET title = ?, date = ?, time = ?, end_time = ?, duration_min = ?,
                       location = ?, description = ?, recurrence = ?, category = ?,
                       status = ?, source_calendar_id = ?, updated_at = ?
                   WHERE id = ?""",
                (
                    src["title"],
                    src["date"],
                    src["time"],
                    src["end_time"],
                    src["duration_min"],
                    src["location"],
                    src["description"],
                    src["recurrence"],
                    src["category"],
                    src["status"],
                    root_cal,
                    now_str,
                    mirror_id,
                ),
            )
            conn.commit()
            return {
                "action": "updated",
                "id": mirror_id,
                "source_event_id": root_id,
                "source_calendar_id": root_cal,
                "target_calendar_id": target_cal,
            }

        mirror_id = _short_id()
        while conn.execute("SELECT 1 FROM events WHERE id = ?", (mirror_id,)).fetchone():
            mirror_id = _short_id()
        conn.execute(
            """INSERT INTO events
               (id, title, date, time, end_time, duration_min, location, description,
                recurrence, ics_uid, created_at, updated_at, calendar_id, category,
                source_calendar_id, source_event_id, link_mode, external_id, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'mirror', ?, ?)""",
            (
                mirror_id,
                src["title"],
                src["date"],
                src["time"],
                src["end_time"],
                src["duration_min"],
                src["location"],
                src["description"],
                src["recurrence"],
                _ics_uid(),
                now_str,
                now_str,
                target_cal,
                src["category"],
                root_cal,
                root_id,
                src["external_id"],
                src["status"],
            ),
        )
        conn.commit()
        return {
            "action": "created",
            "id": mirror_id,
            "source_event_id": root_id,
            "source_calendar_id": root_cal,
            "target_calendar_id": target_cal,
        }
    finally:
        conn.close()


def sync_mirrors(store: Path) -> dict[str, Any]:
    """Synchronisiert alle aktiven Spiegelungen (`link_mode='mirror'`) aus ihren Quellterminen."""
    if not store.exists():
        return {
            "updated": 0,
            "unchanged": 0,
            "orphaned": 0,
            "updated_ids": [],
            "unchanged_ids": [],
            "orphaned_ids": [],
        }
    conn = _open_store(store)
    try:
        mirrors = conn.execute(
            "SELECT * FROM events WHERE link_mode = 'mirror' ORDER BY id ASC"
        ).fetchall()
        updated_ids: list[str] = []
        unchanged_ids: list[str] = []
        orphaned_ids: list[str] = []
        sync_fields = (
            "title",
            "date",
            "time",
            "end_time",
            "duration_min",
            "location",
            "description",
            "recurrence",
            "category",
            "status",
        )
        now_str = _now()
        for m_row in mirrors:
            m_id = str(m_row["id"])
            src_id = m_row["source_event_id"]
            if not src_id:
                orphaned_ids.append(m_id)
                continue
            src = conn.execute("SELECT * FROM events WHERE id = ?", (src_id,)).fetchone()
            if src is None:
                orphaned_ids.append(m_id)
                continue
            changed = any(m_row[f] != src[f] for f in sync_fields)
            if not changed:
                unchanged_ids.append(m_id)
                continue
            conn.execute(
                """UPDATE events
                   SET title = ?, date = ?, time = ?, end_time = ?, duration_min = ?,
                       location = ?, description = ?, recurrence = ?, category = ?,
                       status = ?, source_calendar_id = ?, updated_at = ?
                   WHERE id = ?""",
                (
                    src["title"],
                    src["date"],
                    src["time"],
                    src["end_time"],
                    src["duration_min"],
                    src["location"],
                    src["description"],
                    src["recurrence"],
                    src["category"],
                    src["status"],
                    src["calendar_id"],
                    now_str,
                    m_id,
                ),
            )
            updated_ids.append(m_id)
        conn.commit()
        return {
            "updated": len(updated_ids),
            "unchanged": len(unchanged_ids),
            "orphaned": len(orphaned_ids),
            "updated_ids": updated_ids,
            "unchanged_ids": unchanged_ids,
            "orphaned_ids": orphaned_ids,
        }
    finally:
        conn.close()


def transfer_event(store: Path, event_id: str, target_calendar_id: str) -> dict[str, Any]:
    """Verschiebt einen Termin in ein anderes Silo (`link_mode='transfer'`)."""
    target_cal = str(target_calendar_id or "").strip().lower()
    conn = _open_store(store)
    try:
        _ensure_calendar_exists(conn, target_cal)
        src = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
        if src is None:
            raise ValueError(f"Termin {event_id!r} nicht gefunden.")
        old_cal = str(src["calendar_id"])
        origin_cal = str(src["source_calendar_id"] or old_cal)
        conn.execute(
            """UPDATE events
               SET calendar_id = ?, source_calendar_id = ?, link_mode = 'transfer', updated_at = ?
               WHERE id = ?""",
            (target_cal, origin_cal, _now(), event_id),
        )
        conn.commit()
        return {
            "action": "transferred",
            "id": event_id,
            "from_calendar_id": old_cal,
            "to_calendar_id": target_cal,
            "source_calendar_id": origin_cal,
        }
    finally:
        conn.close()


def clone_event(store: Path, event_id: str, target_calendar_id: str) -> dict[str, Any]:
    """Erstellt eine unabhängige Kopie eines Termins im Ziel-Silo (`link_mode='clone'`)."""
    target_cal = str(target_calendar_id or "").strip().lower()
    conn = _open_store(store)
    try:
        _ensure_calendar_exists(conn, target_cal)
        src = conn.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
        if src is None:
            raise ValueError(f"Quelltermin {event_id!r} nicht gefunden.")
        clone_id = _short_id()
        while conn.execute("SELECT 1 FROM events WHERE id = ?", (clone_id,)).fetchone():
            clone_id = _short_id()
        now_str = _now()
        conn.execute(
            """INSERT INTO events
               (id, title, date, time, end_time, duration_min, location, description,
                recurrence, ics_uid, created_at, updated_at, calendar_id, category,
                source_calendar_id, source_event_id, link_mode, external_id, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'clone', ?, ?)""",
            (
                clone_id,
                src["title"],
                src["date"],
                src["time"],
                src["end_time"],
                src["duration_min"],
                src["location"],
                src["description"],
                src["recurrence"],
                _ics_uid(),
                now_str,
                now_str,
                target_cal,
                src["category"],
                str(src["calendar_id"]),
                str(src["id"]),
                None,
                src["status"],
            ),
        )
        conn.commit()
        return {
            "action": "cloned",
            "id": clone_id,
            "source_event_id": str(src["id"]),
            "source_calendar_id": str(src["calendar_id"]),
            "target_calendar_id": target_cal,
        }
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# ICS-Import & -Export (RFC 5545 Subset, TerminPilot-kompatibel)
# ---------------------------------------------------------------------------

def _escape_ics(text: str) -> str:
    """Escaped ICS-Sonderzeichen (Komma, Semikolon, Backslash, Newline)."""
    return (
        (text or "")
        .replace("\\", "\\\\")
        .replace(",", "\\,")
        .replace(";", "\\;")
        .replace("\n", "\\n")
    )


def _unescape_ics(text: str) -> str:
    """Unescaped RFC-5545-Textwerte (`\\n`, `\\,`, `\\;`, `\\\\`)."""
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] == "\\" and i + 1 < n:
            nxt = text[i + 1]
            if nxt in ("n", "N"):
                out.append("\n")
            elif nxt in (",", ";", "\\"):
                out.append(nxt)
            else:
                out.append(nxt)
            i += 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def _parse_ics_datetime(raw_val: str, params_upper: str) -> tuple[str, Optional[str], Optional[datetime]]:
    """Parst `DTSTART`/`DTEND` in `(YYYY-MM-DD, HH:MM | None, naive_datetime | None)`."""
    val = raw_val.strip()
    if "VALUE=DATE" in params_upper or re.fullmatch(r"\d{8}", val):
        d_str = f"{val[0:4]}-{val[4:6]}-{val[6:8]}"
        date.fromisoformat(d_str)
        return d_str, None, None
    m = re.match(r"^(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})?(Z)?$", val)
    if not m:
        raise ValueError(f"Nicht unterstütztes ICS-Datumsformat: {raw_val!r}")
    y, mo, da, hh, mm, ss, _z = m.groups()
    d_obj = date(int(y), int(mo), int(da))
    t_obj = time(int(hh), int(mm), int(ss or 0))
    dt_obj = datetime.combine(d_obj, t_obj)
    return d_obj.isoformat(), f"{int(hh):02d}:{int(mm):02d}", dt_obj


def _parse_ics_duration(raw_dur: str) -> Optional[int]:
    """Parst RFC-5545 `DURATION` (z. B. `PT1H30M`, `PT45M`, `P1D`) in Minuten."""
    m = re.fullmatch(
        r"P(?:(\d+)W)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?",
        raw_dur.strip().upper(),
    )
    if not m:
        return None
    weeks, days, hours, minutes, seconds = (int(x or 0) for x in m.groups())
    total = weeks * 7 * 1440 + days * 1440 + hours * 60 + minutes + (1 if seconds >= 30 else 0)
    return total if total > 0 else None


def parse_ics_events(ics_text: str) -> list[dict[str, Any]]:
    """Extrahiert `VEVENT`-Einträge aus einem RFC-5545-ICS-Text (inkl. Line-Unfolding)."""
    normalized = re.sub(r"\r+\n", "\n", ics_text).replace("\r", "\n")
    unfolded = re.sub(r"\n[ \t]", "", normalized)
    lines = unfolded.splitlines()
    events: list[dict[str, Any]] = []
    in_event = False
    props: dict[str, tuple[str, str]] = {}

    for line in lines:
        stripped = line.strip()
        if stripped.upper() == "BEGIN:VEVENT":
            in_event = True
            props = {}
            continue
        if stripped.upper() == "END:VEVENT":
            if in_event and "DTSTART" in props:
                dtstart_val, dtstart_params = props["DTSTART"]
                ev_date, ev_time, dt_start = _parse_ics_datetime(dtstart_val, dtstart_params)
                end_time: Optional[str] = None
                duration_min: Optional[int] = None

                if "DURATION" in props:
                    duration_min = _parse_ics_duration(props["DURATION"][0])
                if "DTEND" in props:
                    _end_d, end_t, dt_end = _parse_ics_datetime(*props["DTEND"])
                    end_time = end_t
                    if duration_min is None and dt_start is not None and dt_end is not None and dt_end > dt_start:
                        duration_min = int((dt_end - dt_start).total_seconds() // 60)

                if end_time is None and ev_time and duration_min:
                    end_time = _compute_end_time(ev_time, duration_min)

                summary = _unescape_ics(props.get("SUMMARY", ("Unbenannter Termin", ""))[0]).strip() or "Unbenannter Termin"
                location = _unescape_ics(props["LOCATION"][0]) if "LOCATION" in props else None
                description = _unescape_ics(props["DESCRIPTION"][0]) if "DESCRIPTION" in props else None
                uid = _unescape_ics(props["UID"][0]).strip() if "UID" in props else None
                rrule = props["RRULE"][0].strip() if "RRULE" in props else None
                cats_raw = _unescape_ics(props["CATEGORIES"][0]).strip() if "CATEGORIES" in props else ""
                first_cat = cats_raw.split(",")[0].strip().lower() if cats_raw else None
                raw_status = props["STATUS"][0].strip().lower() if "STATUS" in props else "planned"
                status_map = {"confirmed": "planned", "tentative": "tentative", "cancelled": "cancelled"}

                events.append({
                    "title": summary,
                    "date": ev_date,
                    "time": ev_time,
                    "end_time": end_time,
                    "duration_min": duration_min,
                    "location": location,
                    "description": description,
                    "recurrence": rrule,
                    "uid": uid,
                    "category": first_cat,
                    "status": status_map.get(raw_status, raw_status or "planned"),
                })
            in_event = False
            props = {}
            continue

        if not in_event or ":" not in line:
            continue
        left, val = line.split(":", 1)
        name_and_params = left.split(";", 1)
        prop_name = name_and_params[0].strip().upper()
        prop_params = name_and_params[1].strip().upper() if len(name_and_params) > 1 else ""
        props[prop_name] = (val, prop_params)

    return events


def import_ics(
    store: Path,
    ics_source: Path | str,
    *,
    calendar_id: str = "terminpilot",
    raw_text: bool = False,
) -> dict[str, Any]:
    """Importiert `.ics`-Termine idempotent in das gewählte Silo (Default: `terminpilot`)."""
    cal_id = str(calendar_id or "terminpilot").strip().lower()
    if raw_text:
        ics_text = str(ics_source)
    else:
        ics_path = Path(ics_source)
        if not ics_path.is_file():
            raise FileNotFoundError(f"ICS-Datei nicht gefunden: {ics_path}")
        ics_text = ics_path.read_bytes().decode("utf-8-sig", errors="replace")

    parsed_events = parse_ics_events(ics_text)
    conn = _open_store(store)
    try:
        cal_row = _ensure_calendar_exists(conn, cal_id)
        imported = 0
        updated = 0
        unchanged = 0
        event_ids: list[str] = []
        now_str = _now()

        for item in parsed_events:
            ext_uid = item["uid"]
            eff_cat = item["category"] or cal_row["category"]
            existing = None
            if ext_uid:
                existing = conn.execute(
                    """SELECT * FROM events
                       WHERE calendar_id = ? AND (external_id = ? OR ics_uid = ?)""",
                    (cal_id, ext_uid, ext_uid),
                ).fetchone()

            if existing is not None:
                rec_id = str(existing["id"])
                event_ids.append(rec_id)
                same = (
                    existing["title"] == item["title"]
                    and existing["date"] == item["date"]
                    and existing["time"] == item["time"]
                    and existing["end_time"] == item["end_time"]
                    and existing["duration_min"] == item["duration_min"]
                    and existing["location"] == item["location"]
                    and existing["description"] == item["description"]
                    and existing["recurrence"] == item["recurrence"]
                    and existing["status"] == item["status"]
                )
                if same:
                    unchanged += 1
                    continue
                conn.execute(
                    """UPDATE events
                       SET title = ?, date = ?, time = ?, end_time = ?, duration_min = ?,
                           location = ?, description = ?, recurrence = ?, category = ?,
                           status = ?, external_id = ?, updated_at = ?
                       WHERE id = ?""",
                    (
                        item["title"],
                        item["date"],
                        item["time"],
                        item["end_time"],
                        item["duration_min"],
                        item["location"],
                        item["description"],
                        item["recurrence"],
                        eff_cat,
                        item["status"],
                        ext_uid,
                        now_str,
                        rec_id,
                    ),
                )
                updated += 1
                continue

            rec_id = _short_id()
            while conn.execute("SELECT 1 FROM events WHERE id = ?", (rec_id,)).fetchone():
                rec_id = _short_id()

            candidate_uid = ext_uid or _ics_uid()
            if conn.execute("SELECT 1 FROM events WHERE ics_uid = ?", (candidate_uid,)).fetchone():
                candidate_uid = f"{cal_id}:{candidate_uid}"
                if conn.execute("SELECT 1 FROM events WHERE ics_uid = ?", (candidate_uid,)).fetchone():
                    candidate_uid = _ics_uid()

            conn.execute(
                """INSERT INTO events
                   (id, title, date, time, end_time, duration_min, location, description,
                    recurrence, ics_uid, created_at, updated_at, calendar_id, category,
                    external_id, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    rec_id,
                    item["title"],
                    item["date"],
                    item["time"],
                    item["end_time"],
                    item["duration_min"],
                    item["location"],
                    item["description"],
                    item["recurrence"],
                    candidate_uid,
                    now_str,
                    now_str,
                    cal_id,
                    eff_cat,
                    ext_uid,
                    item["status"],
                ),
            )
            imported += 1
            event_ids.append(rec_id)

        conn.commit()
        return {
            "calendar_id": cal_id,
            "total_vevents": len(parsed_events),
            "imported": imported,
            "updated": updated,
            "unchanged": unchanged,
            "event_ids": event_ids,
        }
    finally:
        conn.close()


def _ics_date(event_date: str, event_time: Optional[str] = None, prop: str = "DTSTART") -> str:
    if event_time:
        dt_str = f"{event_date.replace('-', '')}T{event_time.replace(':', '')}00"
        return f"{prop}:{dt_str}"
    return f"{prop};VALUE=DATE:{event_date.replace('-', '')}"


def _events_to_ics(events: list[dict[str, Any]]) -> str:
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//ellmos-assist//kalender//DE",
        "CALSCALE:GREGORIAN",
    ]
    dtstamp = datetime.now().strftime("%Y%m%dT%H%M%SZ")
    for ev in events:
        uid = ev.get("ics_uid") or _ics_uid()
        cal_id = ev.get("calendar_id") or "user"
        cats = [cal_id]
        eff_cat = ev.get("effective_category") or ev.get("category")
        if eff_cat and eff_cat != cal_id:
            cats.append(str(eff_cat))
        lines.extend([
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"SUMMARY:{_escape_ics(ev['title'])}",
            _ics_date(ev["date"], ev.get("time"), "DTSTART"),
        ])
        if ev.get("end_time") and ev.get("time"):
            lines.append(_ics_date(ev["date"], ev["end_time"], "DTEND"))
        elif ev.get("duration_min"):
            h, m = divmod(int(ev["duration_min"]), 60)
            lines.append(f"DURATION:PT{h}H{m}M")
        lines.append(f"CATEGORIES:{','.join(_escape_ics(c) for c in cats)}")
        if ev.get("location"):
            lines.append(f"LOCATION:{_escape_ics(str(ev['location']))}")
        if ev.get("description"):
            lines.append(f"DESCRIPTION:{_escape_ics(str(ev['description']))}")
        if ev.get("recurrence"):
            lines.append(f"RRULE:{ev['recurrence']}")
        lines.append(f"DTSTAMP:{dtstamp}")
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


def export_ics(
    store: Path,
    record_id: Optional[str] = None,
    *,
    calendar: Optional[str] = "all",
    category: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    search: Optional[str] = None,
) -> str:
    """Erzeugt einen RFC-5545-ICS-String für einen einzelnen oder gefilterte Termine."""
    if record_id:
        events = _query_events(store, record_id=record_id)
        if not events:
            return ""
    else:
        events = _query_events(
            store,
            from_date=_validate_date(from_date) if from_date else None,
            to_date=_validate_date(to_date) if to_date else None,
            calendar=calendar,
            category=category,
            search=search,
            limit=10000,
        )
    return _events_to_ics(events)


# ---------------------------------------------------------------------------
# Zeitraum-Auflösung & Berichtsgenerator (HTML / PDF / MD / TXT / ICS)
# ---------------------------------------------------------------------------

def resolve_view_window(
    view: str,
    *,
    day_str: Optional[str] = None,
    week_from: Optional[str] = None,
    month_str: Optional[str] = None,
    year_str: Optional[str] = None,
    range_from: Optional[str] = None,
    range_to: Optional[str] = None,
) -> tuple[date, date, str]:
    """Berechnet `(start_date, end_date, default_title)` für eine Berichtsansicht."""
    v = view.strip().lower()
    if v not in VALID_REPORT_VIEWS:
        raise ValueError(f"Unbekannte Ansicht {view!r} (erlaubt: {', '.join(VALID_REPORT_VIEWS)})")

    today = date.today()
    if v == "day":
        d = date.fromisoformat(_validate_date(day_str)) if day_str else today
        wd = WEEKDAYS_SHORT_DE[d.weekday()]
        return d, d, f"Tagesübersicht {wd}, {d.isoformat()}"

    if v == "week":
        base_str = week_from or range_from
        if base_str:
            start_d = date.fromisoformat(_validate_date(base_str))
        else:
            start_d = today - timedelta(days=today.weekday())
        end_d = start_d + timedelta(days=6)
        return start_d, end_d, f"Wochenübersicht {start_d.isoformat()} bis {end_d.isoformat()}"

    if v == "month":
        m_val = (month_str or today.strftime("%Y-%m")).strip()
        if not _MONTH_RE.fullmatch(m_val):
            raise ValueError(f"Ungültiger Monat {m_val!r} (erwartet YYYY-MM)")
        year_i, month_i = int(m_val[:4]), int(m_val[5:7])
        last_day = pycalendar.monthrange(year_i, month_i)[1]
        return (
            date(year_i, month_i, 1),
            date(year_i, month_i, last_day),
            f"Monatskalender {MONTHS_DE[month_i]} {year_i}",
        )

    if v == "year":
        y_val = (year_str or str(today.year)).strip()
        if not _YEAR_RE.fullmatch(y_val):
            raise ValueError(f"Ungültiges Jahr {y_val!r} (erwartet YYYY)")
        year_i = int(y_val)
        return date(year_i, 1, 1), date(year_i, 12, 31), f"Jahresübersicht {year_i}"

    # range
    if not range_from or not range_to:
        raise ValueError("Ansicht 'range' erfordert --from YYYY-MM-DD und --to YYYY-MM-DD.")
    s_d = date.fromisoformat(_validate_date(range_from))
    e_d = date.fromisoformat(_validate_date(range_to))
    if s_d > e_d:
        raise ValueError(f"--from ({s_d}) darf nicht nach --to ({e_d}) liegen.")
    return s_d, e_d, f"Terminauszug {s_d.isoformat()} bis {e_d.isoformat()}"


def _silo_summary(
    events: list[dict[str, Any]],
    calendars_map: dict[str, dict[str, Any]],
    selected_cals: Optional[list[str]],
) -> list[dict[str, Any]]:
    counts: dict[str, int] = {}
    for ev in events:
        cid = ev["calendar_id"]
        counts[cid] = counts.get(cid, 0) + 1

    keys = selected_cals if selected_cals else sorted(counts.keys() or ["user"])
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for cid in list(keys) + sorted(counts.keys()):
        if cid in seen:
            continue
        seen.add(cid)
        cinfo = calendars_map.get(cid, {})
        out.append({
            "id": cid,
            "name": cinfo.get("name") or cid,
            "color": cinfo.get("color") or "#4b5563",
            "category": cinfo.get("category"),
            "count": counts.get(cid, 0),
        })
    return out


def _fmt_time_span(ev: dict[str, Any]) -> str:
    t_start = ev.get("time") or ""
    t_end = ev.get("end_time") or ""
    if t_start and t_end:
        return f"{t_start}–{t_end}"
    if t_start and ev.get("duration_min"):
        return f"{t_start} ({ev['duration_min']}m)"
    if t_start:
        return t_start
    return "ganztägig"


def _render_ascii_month_grid(
    year: int,
    month: int,
    events_by_day: dict[str, list[dict[str, Any]]],
    *,
    first_weekday: int = 0,
) -> str:
    cal = pycalendar.Calendar(firstweekday=first_weekday)
    weeks = cal.monthdatescalendar(year, month)
    wd_headers = [WEEKDAYS_SHORT_DE[(first_weekday + i) % 7] for i in range(7)]
    header_bar = "  |" + "|".join(f"  {w}  " for w in wd_headers) + "|"
    lines = [
        f"  {MONTHS_DE[month]} {year}",
        "  +------+------+------+------+------+------+------+",
        header_bar,
        "  +------+------+------+------+------+------+------+",
    ]
    for week in weeks:
        cells: list[str] = []
        for d in week:
            if d.month != month:
                cells.append("      ")
            else:
                cnt = len(events_by_day.get(d.isoformat(), []))
                marker = f"*{cnt}" if cnt > 0 else "  "
                cells.append(f" {d.day:2d}{marker:<2s} ")
        lines.append("  |" + "|".join(cells) + "|")
    lines.append("  +------+------+------+------+------+------+------+")
    return "\n".join(lines)


def _render_markdown(
    view: str,
    title: str,
    start_d: date,
    end_d: date,
    events: list[dict[str, Any]],
    legend: list[dict[str, Any]],
    *,
    cfg: Mapping[str, Any] | None = None,
    skill_root: Path = _SKILL_DIR,
) -> str:
    eff = cfg or load_kalender_config(skill_root=skill_root)["config"]
    first_wd = int((eff.get("defaults") or {}).get("first_weekday", 0))
    max_chips = max(1, int((eff.get("output") or {}).get("max_chips_per_day_md", 4)))
    tpl = _resolve_template_path("report_md", cfg=eff, skill_root=skill_root).read_text(encoding="utf-8")

    legend_md = (
        ", ".join(f"`{s['id']}` ({s['name']}: {s['count']})" for s in legend)
        if legend
        else "_keine_"
    )
    body_lines: list[str] = []

    events_by_day: dict[str, list[dict[str, Any]]] = {}
    for ev in events:
        events_by_day.setdefault(ev["date"], []).append(ev)

    if view == "month":
        cal = pycalendar.Calendar(firstweekday=first_wd)
        weeks = cal.monthdatescalendar(start_d.year, start_d.month)
        wd_headers = [WEEKDAYS_SHORT_DE[(first_wd + i) % 7] for i in range(7)]
        body_lines.extend([
            f"## Monatsgitter ({wd_headers[0]}–{wd_headers[-1]})",
            "",
            "| " + " | ".join(wd_headers) + " |",
            "|---|---|---|---|---|---|---|",
        ])
        for week in weeks:
            row_cells: list[str] = []
            for d in week:
                if d.month != start_d.month:
                    row_cells.append(" ")
                else:
                    day_evs = events_by_day.get(d.isoformat(), [])
                    if not day_evs:
                        row_cells.append(f"**{d.day}**")
                    else:
                        chips = "<br>".join(
                            f"`{ev.get('time') or '--:--'}` [{ev['calendar_id']}] "
                            f"{ev['title'].replace('|', '/')}"
                            for ev in day_evs[:max_chips]
                        )
                        if len(day_evs) > max_chips:
                            chips += f"<br>_(+{len(day_evs) - max_chips} weitere)_"
                        row_cells.append(f"**{d.day}**<br>{chips}")
            body_lines.append("| " + " | ".join(row_cells) + " |")
        body_lines.append("")

    body_lines.append("## Terminliste")
    body_lines.append("")
    if not events:
        body_lines.append("_Keine Termine im gewählten Zeitraum._")
    elif view in {"year", "range"}:
        by_month: dict[str, list[dict[str, Any]]] = {}
        for ev in events:
            by_month.setdefault(ev["date"][:7], []).append(ev)
        for ym in sorted(by_month.keys()):
            y_i, m_i = int(ym[:4]), int(ym[5:7])
            m_evs = by_month[ym]
            body_lines.extend([
                f"### {MONTHS_DE[m_i]} {y_i} ({len(m_evs)})",
                "",
                "| Datum | Zeit | Kalender | Titel | Ort | Notiz |",
                "|---|---|---|---|---|---|",
            ])
            for ev in m_evs:
                body_lines.append(
                    f"| {ev['date']} | {_fmt_time_span(ev)} | `{ev['calendar_id']}` | "
                    f"{ev['title'].replace('|', '/')} | {(ev.get('location') or '-').replace('|', '/')} | "
                    f"{(ev.get('description') or '-').replace('|', '/').replace(chr(10), ' ')} |"
                )
            body_lines.append("")
    else:
        body_lines.extend([
            "| Datum | Zeit | Kalender | Titel | Ort | Notiz |",
            "|---|---|---|---|---|---|",
        ])
        for ev in events:
            body_lines.append(
                f"| {ev['date']} | {_fmt_time_span(ev)} | `{ev['calendar_id']}` | "
                f"{ev['title'].replace('|', '/')} | {(ev.get('location') or '-').replace('|', '/')} | "
                f"{(ev.get('description') or '-').replace('|', '/').replace(chr(10), ' ')} |"
            )

    rendered = (
        tpl.replace("{{title}}", title)
        .replace("{{start_date}}", start_d.isoformat())
        .replace("{{end_date}}", end_d.isoformat())
        .replace("{{event_count}}", str(len(events)))
        .replace("{{legend_md}}", legend_md)
        .replace("{{body_md}}", "\n".join(body_lines).rstrip("\n"))
    )
    return rendered.rstrip("\n") + "\n"


def _render_text(
    view: str,
    title: str,
    start_d: date,
    end_d: date,
    events: list[dict[str, Any]],
    legend: list[dict[str, Any]],
    *,
    cfg: Mapping[str, Any] | None = None,
    skill_root: Path = _SKILL_DIR,
) -> str:
    eff = cfg or load_kalender_config(skill_root=skill_root)["config"]
    first_wd = int((eff.get("defaults") or {}).get("first_weekday", 0))
    tpl = _resolve_template_path("report_txt", cfg=eff, skill_root=skill_root).read_text(encoding="utf-8")

    sep = "=" * max(64, len(title) + 6)
    legend_txt = ", ".join(f"{s['id']} ({s['count']})" for s in legend) if legend else "-"
    events_by_day: dict[str, list[dict[str, Any]]] = {}
    for ev in events:
        events_by_day.setdefault(ev["date"], []).append(ev)

    body_lines: list[str] = []
    if view == "month":
        body_lines.append("")
        body_lines.append(
            _render_ascii_month_grid(start_d.year, start_d.month, events_by_day, first_weekday=first_wd)
        )

    body_lines.append("")
    if not events:
        body_lines.append("  Keine Termine im gewählten Zeitraum.")
    else:
        current_group = ""
        for ev in events:
            grp = ev["date"][:7] if view in {"year", "range"} else ev["date"]
            if grp != current_group:
                current_group = grp
                if view in {"year", "range"}:
                    y_i, m_i = int(grp[:4]), int(grp[5:7])
                    body_lines.append(f"\n--- {MONTHS_DE[m_i]} {y_i} ---")
                else:
                    d_obj = date.fromisoformat(grp)
                    body_lines.append(f"\n--- {WEEKDAYS_SHORT_DE[d_obj.weekday()]}, {grp} ---")
            loc = f" @ {ev['location']}" if ev.get("location") else ""
            desc = f" — {ev['description']}" if ev.get("description") else ""
            body_lines.append(
                f"  [{ev['id']}] {ev['date']} {_fmt_time_span(ev):<13s} "
                f"[{ev['calendar_id']}] {ev['title']}{loc}{desc}"
            )

    rendered = (
        tpl.replace("{{sep}}", sep)
        .replace("{{title}}", title)
        .replace("{{start_date}}", start_d.isoformat())
        .replace("{{end_date}}", end_d.isoformat())
        .replace("{{event_count}}", str(len(events)))
        .replace("{{legend_txt}}", legend_txt)
        .replace("{{body_txt}}", "\n".join(body_lines))
    )
    return rendered.rstrip("\n") + "\n"


def _render_html(
    view: str,
    title: str,
    start_d: date,
    end_d: date,
    events: list[dict[str, Any]],
    legend: list[dict[str, Any]],
    *,
    cfg: Mapping[str, Any] | None = None,
    skill_root: Path = _SKILL_DIR,
) -> str:
    eff = cfg or load_kalender_config(skill_root=skill_root)["config"]
    first_wd = int((eff.get("defaults") or {}).get("first_weekday", 0))
    esc = html.escape
    page_orient = "landscape" if view in {"month", "week"} else "portrait"
    tpl_key = "month_html" if view == "month" else ("week_html" if view == "week" else "report_html")
    tpl = _resolve_template_path(tpl_key, cfg=eff, skill_root=skill_root).read_text(encoding="utf-8")

    events_by_day: dict[str, list[dict[str, Any]]] = {}
    for ev in events:
        events_by_day.setdefault(ev["date"], []).append(ev)

    legend_html = "".join(
        f'<span class="legend-pill" style="--silo:{esc(s["color"])}">'
        f'<span class="dot"></span><strong>{esc(s["name"])}</strong> '
        f'<code>{esc(s["id"])}</code> ({s["count"]})</span>'
        for s in legend
    )

    body_parts: list[str] = []

    if view == "month":
        cal = pycalendar.Calendar(firstweekday=first_wd)
        weeks = cal.monthdatescalendar(start_d.year, start_d.month)
        body_parts.append('<table class="cal-grid"><thead><tr>')
        for i in range(7):
            wd = WEEKDAYS_SHORT_DE[(first_wd + i) % 7]
            body_parts.append(f"<th>{wd}</th>")
        body_parts.append("</tr></thead><tbody>")
        for week in weeks:
            body_parts.append("<tr>")
            for d in week:
                in_month = d.month == start_d.month
                cls = "day-cell" if in_month else "day-cell outside"
                if d.weekday() >= 5:
                    cls += " weekend"
                body_parts.append(f'<td class="{cls}">')
                body_parts.append(f'<div class="day-num">{d.day}</div>')
                for ev in events_by_day.get(d.isoformat(), []):
                    color = esc(ev.get("calendar_color") or "#2563eb")
                    loc = f' · <span class="loc">{esc(str(ev["location"]))}</span>' if ev.get("location") else ""
                    body_parts.append(
                        f'<div class="ev-chip" style="border-left-color:{color}">'
                        f'<span class="ev-time">{esc(_fmt_time_span(ev))}</span> '
                        f'<span class="ev-badge" style="background:{color}">{esc(ev["calendar_id"])}</span> '
                        f'<span class="ev-title">{esc(ev["title"])}</span>{loc}</div>'
                    )
                body_parts.append("</td>")
            body_parts.append("</tr>")
        body_parts.append("</tbody></table>")

    elif view == "week":
        days = [start_d + timedelta(days=i) for i in range(7)]
        body_parts.append('<table class="cal-grid week-grid"><thead><tr>')
        for d in days:
            wd = WEEKDAYS_SHORT_DE[d.weekday()]
            body_parts.append(f"<th>{wd}<br><small>{d.isoformat()}</small></th>")
        body_parts.append("</tr></thead><tbody><tr>")
        for d in days:
            cls = "day-cell weekend" if d.weekday() >= 5 else "day-cell"
            body_parts.append(f'<td class="{cls}">')
            day_evs = events_by_day.get(d.isoformat(), [])
            if not day_evs:
                body_parts.append('<div class="empty-slot">—</div>')
            for ev in day_evs:
                color = esc(ev.get("calendar_color") or "#2563eb")
                loc = f'<div class="ev-meta">{esc(str(ev["location"]))}</div>' if ev.get("location") else ""
                body_parts.append(
                    f'<div class="ev-chip" style="border-left-color:{color}">'
                    f'<div class="ev-head"><span class="ev-time">{esc(_fmt_time_span(ev))}</span> '
                    f'<span class="ev-badge" style="background:{color}">{esc(ev["calendar_id"])}</span></div>'
                    f'<div class="ev-title">{esc(ev["title"])}</div>{loc}</div>'
                )
            body_parts.append("</td>")
        body_parts.append("</tr></tbody></table>")

    elif view == "day":
        body_parts.append('<div class="agenda-list">')
        if not events:
            body_parts.append('<p class="empty-msg">Keine Termine an diesem Tag.</p>')
        for ev in events:
            color = esc(ev.get("calendar_color") or "#2563eb")
            loc = f'<span>Ort: {esc(str(ev["location"]))}</span>' if ev.get("location") else ""
            desc = f'<p class="ev-desc">{esc(str(ev["description"]))}</p>' if ev.get("description") else ""
            body_parts.append(
                f'<div class="day-card" style="border-left-color:{color}">'
                f'<div class="day-card-top"><strong>{esc(_fmt_time_span(ev))}</strong> '
                f'<span class="ev-badge" style="background:{color}">{esc(ev["calendar_name"])}</span> '
                f'{loc}</div>'
                f'<div class="day-card-title">{esc(ev["title"])}</div>{desc}</div>'
            )
        body_parts.append("</div>")

    else:
        if not events:
            body_parts.append('<p class="empty-msg">Keine Termine im gewählten Zeitraum.</p>')
        by_month: dict[str, list[dict[str, Any]]] = {}
        for ev in events:
            by_month.setdefault(ev["date"][:7], []).append(ev)
        for ym in sorted(by_month.keys()):
            y_i, m_i = int(ym[:4]), int(ym[5:7])
            m_evs = by_month[ym]
            body_parts.append(
                f'<section class="month-section"><h2>{esc(MONTHS_DE[m_i])} {y_i} '
                f'<small>({len(m_evs)} Termine)</small></h2>'
                '<table class="list-table"><thead><tr>'
                "<th>Datum</th><th>Zeit</th><th>Kalender</th><th>Titel</th><th>Ort</th><th>Notiz</th>"
                "</tr></thead><tbody>"
            )
            for ev in m_evs:
                color = esc(ev.get("calendar_color") or "#2563eb")
                d_obj = date.fromisoformat(ev["date"])
                wd = WEEKDAYS_SHORT_DE[d_obj.weekday()]
                body_parts.append(
                    f"<tr><td>{wd}, {esc(ev['date'])}</td>"
                    f"<td>{esc(_fmt_time_span(ev))}</td>"
                    f'<td><span class="ev-badge" style="background:{color}">{esc(ev["calendar_id"])}</span></td>'
                    f"<td><strong>{esc(ev['title'])}</strong></td>"
                    f"<td>{esc(str(ev.get('location') or ''))}</td>"
                    f"<td>{esc(str(ev.get('description') or ''))}</td></tr>"
                )
            body_parts.append("</tbody></table></section>")

    content_html = "\n".join(body_parts)
    subtitle = f"{esc(start_d.isoformat())} – {esc(end_d.isoformat())} · {len(events)} Termine"
    return (
        tpl.replace("{{page_orient}}", page_orient)
        .replace("{{title}}", esc(title))
        .replace("{{subtitle}}", subtitle)
        .replace("{{legend_html}}", legend_html)
        .replace("{{content_html}}", content_html)
    )


# ---------------------------------------------------------------------------
# Stdlib-only PDF-1.4-Generator (WinAnsi-Umlaute + Vektor-Kalenderblatt)
# ---------------------------------------------------------------------------

_WINANSI_EXTRA: dict[str, int] = {
    "€": 0x80, "‚": 0x82, "„": 0x84, "…": 0x85, "–": 0x96, "—": 0x97,
    "‘": 0x91, "’": 0x92, "“": 0x93, "”": 0x94, "•": 0x95, "™": 0x99,
}


def _pdf_encode_str(text: str) -> str:
    """Kodiert Unicode-Text deterministisch als WinAnsi-kompatiblen PDF-Literal-String."""
    buf: list[str] = []
    for ch in text:
        code = ord(ch)
        if ch == "\\":
            buf.append("\\\\")
        elif ch == "(":
            buf.append("\\(")
        elif ch == ")":
            buf.append("\\)")
        elif ch in ("\r", "\n", "\t"):
            buf.append(" ")
        elif 32 <= code <= 126:
            buf.append(ch)
        elif ch in _WINANSI_EXTRA:
            buf.append(f"\\{_WINANSI_EXTRA[ch]:03o}")
        elif 160 <= code <= 255:
            # deckt alle deutschen Umlaute äöüÄÖÜß, §, ·, Akzente usw. exakt ab
            buf.append(f"\\{code:03o}")
        else:
            buf.append("?")
    return "(" + "".join(buf) + ")"


def _hex_to_rgb01(hex_color: str) -> tuple[float, float, float]:
    clean = (hex_color or "#2563eb").lstrip("#")
    if len(clean) == 3:
        clean = "".join(c * 2 for c in clean)
    if len(clean) != 6:
        return (0.15, 0.39, 0.92)
    try:
        r = int(clean[0:2], 16) / 255.0
        g = int(clean[2:4], 16) / 255.0
        b = int(clean[4:6], 16) / 255.0
        return (round(r, 3), round(g, 3), round(b, 3))
    except ValueError:
        return (0.15, 0.39, 0.92)


def _assemble_pdf_document(pages_ops: list[str], page_width: float, page_height: float) -> bytes:
    """Baut ein valides `%PDF-1.4`-Dokument mit exakter `xref`-Tabelle."""
    # Objekte:
    # 1: Catalog, 2: Pages, 3: Font Regular (Helvetica), 4: Font Bold (Helvetica-Bold),
    # danach pro Seite 2 Objekte: Page + Contents-Stream
    num_pages = max(1, len(pages_ops))
    if not pages_ops:
        pages_ops = [""]

    objects: dict[int, bytes] = {}
    objects[3] = (
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
    )
    objects[4] = (
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"
    )

    kids_refs: list[str] = []
    next_id = 5
    for content_str in pages_ops:
        page_id = next_id
        stream_id = next_id + 1
        next_id += 2
        kids_refs.append(f"{page_id} 0 R")
        stream_bytes = content_str.encode("latin-1", errors="replace")
        objects[stream_id] = (
            f"<< /Length {len(stream_bytes)} >>\nstream\n".encode("ascii")
            + stream_bytes
            + b"\nendstream"
        )
        objects[page_id] = (
            f"<< /Type /Page /Parent 2 0 R "
            f"/MediaBox [0 0 {page_width:.2f} {page_height:.2f}] "
            f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> "
            f"/Contents {stream_id} 0 R >>"
        ).encode("ascii")

    objects[2] = (
        f"<< /Type /Pages /Kids [{' '.join(kids_refs)}] /Count {num_pages} >>"
    ).encode("ascii")
    objects[1] = b"<< /Type /Catalog /Pages 2 0 R >>"

    total_objs = next_id - 1
    chunks: list[bytes] = [b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"]
    offsets: dict[int, int] = {}
    cursor = len(chunks[0])

    for obj_id in range(1, total_objs + 1):
        offsets[obj_id] = cursor
        block = f"{obj_id} 0 obj\n".encode("ascii") + objects[obj_id] + b"\nendobj\n"
        chunks.append(block)
        cursor += len(block)

    xref_offset = cursor
    xref_lines = [f"xref\n0 {total_objs + 1}\n", "0000000000 65535 f \n"]
    for obj_id in range(1, total_objs + 1):
        xref_lines.append(f"{offsets[obj_id]:010d} 00000 n \n")
    trailer = (
        "".join(xref_lines)
        + f"trailer\n<< /Size {total_objs + 1} /Root 1 0 R >>\n"
        + f"startxref\n{xref_offset}\n%%EOF\n"
    ).encode("ascii")
    chunks.append(trailer)
    return b"".join(chunks)


def generate_pdf_bytes(
    view: str,
    title: str,
    start_d: date,
    end_d: date,
    events: list[dict[str, Any]],
    legend: list[dict[str, Any]],
) -> bytes:
    """Erzeugt ein druckreifes `%PDF-1.4` (Monats-Vektorgitter + strukturierte Seiten)."""
    is_month = view == "month"
    pw, ph = (841.89, 595.28) if is_month else (595.28, 841.89)
    margin = 34.0
    pages: list[str] = []

    def _header_ops(page_title: str, sub: str) -> list[str]:
        ops = [
            "0.06 0.09 0.16 rg",
            f"{margin:.1f} {ph - margin - 28:.1f} {pw - 2 * margin:.1f} 28 re f",
            "1 1 1 rg",
            f"BT /F2 13 Tf {margin + 10:.1f} {ph - margin - 19:.1f} Td {_pdf_encode_str(page_title)} Tj ET",
            f"BT /F1 8.5 Tf {pw - margin - 230:.1f} {ph - margin - 18:.1f} Td {_pdf_encode_str(sub)} Tj ET",
        ]
        # Silo legend row
        lx = margin
        ly = ph - margin - 44
        for s in legend[:8]:
            r, g, b = _hex_to_rgb01(s["color"])
            label = f"{s['id']} ({s['count']})"
            ops.append(f"{r} {g} {b} rg {lx:.1f} {ly:.1f} 8 8 re f")
            ops.append(
                f"0.2 0.25 0.33 rg BT /F1 7.5 Tf {lx + 11:.1f} {ly + 1:.1f} Td {_pdf_encode_str(label)} Tj ET"
            )
            lx += max(68.0, len(label) * 4.4 + 18.0)
            if lx > pw - margin - 70:
                break
        return ops

    sub_line = f"{start_d.isoformat()} bis {end_d.isoformat()} | {len(events)} Termine"

    if is_month:
        events_by_day: dict[str, list[dict[str, Any]]] = {}
        for ev in events:
            events_by_day.setdefault(ev["date"], []).append(ev)

        cal = pycalendar.Calendar(firstweekday=0)
        weeks = cal.monthdatescalendar(start_d.year, start_d.month)
        ops = _header_ops(title, sub_line)

        grid_top = ph - margin - 56.0
        header_h = 18.0
        grid_h = grid_top - margin - header_h
        col_w = (pw - 2 * margin) / 7.0
        row_h = grid_h / max(4, len(weeks))

        # Weekday header bar
        ops.append(f"0.12 0.16 0.23 rg {margin:.1f} {grid_top - header_h:.1f} {pw - 2 * margin:.1f} {header_h:.1f} re f")
        for col_idx, wd in enumerate(WEEKDAYS_SHORT_DE):
            cx = margin + col_idx * col_w + col_w * 0.42
            ops.append(f"1 1 1 rg BT /F2 8.5 Tf {cx:.1f} {grid_top - 12.5:.1f} Td ({wd}) Tj ET")

        max_lines_per_cell = max(2, int((row_h - 18) // 10))
        for r_idx, week in enumerate(weeks):
            cell_top = grid_top - header_h - r_idx * row_h
            cell_bottom = cell_top - row_h
            for c_idx, d in enumerate(week):
                cell_x = margin + c_idx * col_w
                if d.month != start_d.month:
                    ops.append(f"0.95 0.96 0.98 rg {cell_x:.1f} {cell_bottom:.1f} {col_w:.1f} {row_h:.1f} re f")
                elif d.weekday() >= 5:
                    ops.append(f"0.98 0.98 0.99 rg {cell_x:.1f} {cell_bottom:.1f} {col_w:.1f} {row_h:.1f} re f")
                ops.append(f"0.78 0.82 0.88 RG 0.6 w {cell_x:.1f} {cell_bottom:.1f} {col_w:.1f} {row_h:.1f} re S")

                num_color = "0.2 0.25 0.33" if d.month == start_d.month else "0.62 0.66 0.72"
                ops.append(
                    f"{num_color} rg BT /F2 8 Tf {cell_x + 4:.1f} {cell_top - 11:.1f} Td ({d.day}) Tj ET"
                )
                if d.month != start_d.month:
                    continue
                day_evs = events_by_day.get(d.isoformat(), [])
                for ev_i, ev in enumerate(day_evs[:max_lines_per_cell]):
                    ey = cell_top - 22.0 - ev_i * 10.0
                    r, g, b = _hex_to_rgb01(ev.get("calendar_color") or "#2563eb")
                    ops.append(f"{r} {g} {b} rg {cell_x + 3:.1f} {ey - 1:.1f} 2.5 7.5 re f")
                    t_prefix = f"{ev['time']} " if ev.get("time") else ""
                    snippet = f"{t_prefix}{ev['title']}"[:22]
                    ops.append(
                        f"0.08 0.1 0.15 rg BT /F1 6.7 Tf {cell_x + 8:.1f} {ey:.1f} Td {_pdf_encode_str(snippet)} Tj ET"
                    )
                if len(day_evs) > max_lines_per_cell:
                    extra = f"+{len(day_evs) - max_lines_per_cell} weitere"
                    ey = cell_bottom + 4.0
                    ops.append(
                        f"0.35 0.4 0.48 rg BT /F1 6.3 Tf {cell_x + 8:.1f} {ey:.1f} Td {_pdf_encode_str(extra)} Tj ET"
                    )
        pages.append("\n".join(ops))

    # Detail-/Listen-Seiten (für day/week/year/range immer; für month ab >0 Terminen zusätzlich als Detailblatt)
    if not is_month or events:
        detail_title = f"{title} — Terminliste" if is_month else title
        cur_ops = _header_ops(detail_title, sub_line)
        y_cursor = ph - margin - 64.0
        bottom_limit = margin + 24.0

        if not events:
            cur_ops.append(
                f"0.4 0.45 0.52 rg BT /F1 10 Tf {margin:.1f} {y_cursor:.1f} Td "
                f"{_pdf_encode_str('Keine Termine im gewählten Zeitraum.')} Tj ET"
            )
            pages.append("\n".join(cur_ops))
        else:
            current_grp = ""
            for ev in events:
                grp = ev["date"][:7] if view in {"year", "range"} else ev["date"]
                needed = 30.0 if grp != current_grp else 15.0
                if y_cursor - needed < bottom_limit:
                    pages.append("\n".join(cur_ops))
                    cur_ops = _header_ops(detail_title, sub_line)
                    y_cursor = ph - margin - 64.0
                    current_grp = ""

                if grp != current_grp:
                    current_grp = grp
                    y_cursor -= 6.0
                    if view in {"year", "range"}:
                        y_i, m_i = int(grp[:4]), int(grp[5:7])
                        grp_heading = f"{MONTHS_DE[m_i]} {y_i}"
                    else:
                        d_obj = date.fromisoformat(grp)
                        grp_heading = f"{WEEKDAYS_SHORT_DE[d_obj.weekday()]}, {grp}"
                    cur_ops.append(
                        f"0.12 0.18 0.28 rg BT /F2 9.5 Tf {margin:.1f} {y_cursor:.1f} Td "
                        f"{_pdf_encode_str(grp_heading)} Tj ET"
                    )
                    y_cursor -= 14.0

                r, g, b = _hex_to_rgb01(ev.get("calendar_color") or "#2563eb")
                cur_ops.append(f"{r} {g} {b} rg {margin + 2:.1f} {y_cursor - 1:.1f} 3.5 8.5 re f")
                loc_part = f" @ {ev['location']}" if ev.get("location") else ""
                line_str = (
                    f"{ev['date']}  {_fmt_time_span(ev):<13s}  [{ev['calendar_id']}]  "
                    f"{ev['title']}{loc_part}"
                )[:115]
                cur_ops.append(
                    f"0.08 0.1 0.15 rg BT /F1 8.5 Tf {margin + 10:.1f} {y_cursor:.1f} Td "
                    f"{_pdf_encode_str(line_str)} Tj ET"
                )
                y_cursor -= 13.5

            pages.append("\n".join(cur_ops))

    total_p = len(pages)
    numbered_pages: list[str] = []
    for idx, p_ops in enumerate(pages, start=1):
        footer = (
            f"\n0.45 0.5 0.58 rg BT /F1 7.5 Tf {pw - margin - 65:.1f} {margin - 16:.1f} Td "
            f"(Seite {idx} / {total_p}) Tj ET"
        )
        numbered_pages.append(p_ops + footer)

    return _assemble_pdf_document(numbered_pages, pw, ph)


def render_report(
    store: Path,
    *,
    view: str = "month",
    fmt: str = "html",
    day_str: Optional[str] = None,
    week_from: Optional[str] = None,
    month_str: Optional[str] = None,
    year_str: Optional[str] = None,
    range_from: Optional[str] = None,
    range_to: Optional[str] = None,
    calendar: Optional[str] = "all",
    category: Optional[str] = None,
    search: Optional[str] = None,
    title: Optional[str] = None,
    out_path: Optional[Path | str] = None,
    skill_root: Path = _SKILL_DIR,
    repair: bool = False,
) -> dict[str, Any]:
    """Erzeugt einen Kalenderbericht in `html`, `md`, `txt`, `ics` oder `pdf`."""
    cfg = load_kalender_config(skill_root=skill_root, repair=repair)["config"]
    fmt_norm = str(fmt or (cfg.get("output") or {}).get("default_format") or "html").strip().lower()
    if fmt_norm not in VALID_REPORT_FORMATS:
        raise ValueError(
            f"Unbekanntes Format {fmt!r} (erlaubt: {', '.join(VALID_REPORT_FORMATS)})"
        )

    start_d, end_d, auto_title = resolve_view_window(
        view,
        day_str=day_str,
        week_from=week_from,
        month_str=month_str,
        year_str=year_str,
        range_from=range_from,
        range_to=range_to,
    )
    final_title = str(title).strip() if title and str(title).strip() else auto_title

    cals_list = list_calendars(store) if store.exists() else [
        {
            "id": cid,
            "name": cname,
            "category": ccat,
            "color": ccol,
            "description": cdesc,
            "is_default": cdef,
        }
        for cid, cname, ccat, ccol, cdesc, cdef in _silo_rows_from_config(cfg)
    ]
    cals_map = {c["id"]: c for c in cals_list}
    events = _query_events(
        store,
        from_date=start_d.isoformat(),
        to_date=end_d.isoformat(),
        calendar=calendar,
        category=category,
        search=search,
    )
    selected_cals = parse_calendar_filter(calendar)
    legend = _silo_summary(events, cals_map, selected_cals)

    text_output: Optional[str] = None
    binary_output: Optional[bytes] = None

    if fmt_norm == "html":
        text_output = _render_html(view, final_title, start_d, end_d, events, legend, cfg=cfg, skill_root=skill_root)
    elif fmt_norm == "md":
        text_output = _render_markdown(view, final_title, start_d, end_d, events, legend, cfg=cfg, skill_root=skill_root)
    elif fmt_norm == "txt":
        text_output = _render_text(view, final_title, start_d, end_d, events, legend, cfg=cfg, skill_root=skill_root)
    elif fmt_norm == "ics":
        text_output = _events_to_ics(events)
    else:
        binary_output = generate_pdf_bytes(view, final_title, start_d, end_d, events, legend)

    written_path: Optional[str] = None
    byte_count = 0
    if out_path is not None:
        dest = Path(out_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if binary_output is not None:
            dest.write_bytes(binary_output)
            byte_count = len(binary_output)
        else:
            assert text_output is not None
            dest.write_text(text_output, encoding="utf-8", newline="" if fmt_norm == "ics" else None)
            byte_count = len(text_output.encode("utf-8"))
        written_path = str(dest)
    else:
        byte_count = len(binary_output) if binary_output is not None else len((text_output or "").encode("utf-8"))

    return {
        "view": view,
        "format": fmt_norm,
        "title": final_title,
        "from_date": start_d.isoformat(),
        "to_date": end_d.isoformat(),
        "calendar_filter": selected_cals or "all",
        "category_filter": category,
        "search_filter": search,
        "events_count": len(events),
        "silos": legend,
        "output_path": written_path,
        "bytes": byte_count,
        "content": text_output,
        "pdf_bytes": binary_output,
    }


# ---------------------------------------------------------------------------
# Dry-Run-Beispieldaten & Text-Formatierung
# ---------------------------------------------------------------------------

_DRY_EVENTS: list[dict[str, Any]] = [
    {
        "id": "evt-1",
        "title": "Zahnarzt",
        "date": date.today().isoformat(),
        "time": "10:00",
        "end_time": "11:00",
        "duration_min": 60,
        "location": "Praxis Dr. Muster",
        "description": "",
        "calendar_id": "gesundheit",
    },
    {
        "id": "evt-2",
        "title": "Team-Abstimmung",
        "date": date.today().isoformat(),
        "time": "14:00",
        "end_time": "15:30",
        "duration_min": 90,
        "location": "",
        "description": "Wöchentlich",
        "calendar_id": "terminpilot",
    },
    {
        "id": "evt-3",
        "title": "Sport",
        "date": (date.today() + timedelta(days=2)).isoformat(),
        "time": "08:00",
        "end_time": "09:00",
        "duration_min": 60,
        "location": "Fitnessstudio",
        "description": "",
        "calendar_id": "routinen",
    },
]


def _fmt_event(ev: dict[str, Any]) -> str:
    cal_id = ev.get("calendar_id") or "user"
    t = f" {ev['time']}" if ev.get("time") else ""
    dur = f" ({ev['duration_min']} min)" if ev.get("duration_min") else ""
    loc = f" @ {ev['location']}" if ev.get("location") else ""
    desc = f" — {ev['description']}" if ev.get("description") else ""
    return f"  [{ev['id']}] {ev['date']}{t}{dur} [{cal_id}] | {ev['title']}{loc}{desc}"


# ---------------------------------------------------------------------------
# Backend-Check & CLI
# ---------------------------------------------------------------------------

def cmd_check_backend(*, as_json: bool = False) -> int:
    backend = _read_pref("kalender_backend")
    if as_json:
        print(json.dumps({"backend": backend or "unset", "core_version": __version__}, ensure_ascii=False, indent=2))
        return 0
    if not backend:
        print("[kalender] Kein Backend in prefs.json konfiguriert.")
        print("  Das LLM wird den Nutzer interaktiv nach dem bevorzugten Backend fragen.")
        print("  Optionen: local | google | routinika | uptoday")
        print('  Setzen via: prefs.json -> kalender_backend: "local"')
    elif backend == "local":
        print("[kalender] Backend: lokal (SQLite-Store, dieser Core)")
    elif backend == "google":
        print("[kalender] Backend: Google Calendar MCP (LLM-gesteuert, dieser Core inaktiv)")
    else:
        print(f"[kalender] Backend: {backend!r} (via module-installer)")
    return 0


def cmd_check_config(*, as_json: bool = False, repair: bool = False) -> int:
    loaded = load_kalender_config(repair=repair)
    payload = {
        "core_version": __version__,
        "config": loaded["config"],
        "warnings": loaded["warnings"],
        "healed": loaded["healed"],
    }
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        cfg = loaded["config"]
        print(
            f"[kalender] Config v{cfg.get('version')} | Default-Silo: {cfg['defaults']['calendar']} | "
            f"Format: {cfg['output']['default_format']} | Silos: {len(cfg.get('silos', []))}"
        )
        for warn in loaded["warnings"]:
            print(f"  [WARN] {warn}")
        for heal in loaded["healed"]:
            print(f"  [HEALED] {heal['path']} -> Backup: {heal['backup_path']}")
    return 0


def _extract_flag(args: list[str], flag: str) -> tuple[Optional[str], list[str]]:
    if flag in args:
        idx = args.index(flag)
        if idx + 1 >= len(args):
            raise ValueError(f"Option {flag} benötigt einen Wert.")
        val = args[idx + 1]
        return val, args[:idx] + args[idx + 2:]
    return None, args


def _emit_events_result(
    heading: str,
    empty_msg: str,
    events: list[dict[str, Any]],
    *,
    as_json: bool,
    grouped_by_day: bool = False,
) -> int:
    if as_json:
        print(json.dumps({"count": len(events), "events": events}, ensure_ascii=False, indent=2))
        return 0
    print(heading)
    if not events:
        print(f"  {empty_msg}")
        return 0
    cur_day = ""
    for ev in events:
        if grouped_by_day and ev["date"] != cur_day:
            print(f"\n  {ev['date']}")
            cur_day = ev["date"]
        print(_fmt_event(ev))
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """Haupteinstiegspunkt der CLI (`kalender_core.py`)."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if argv is None:
        argv = list(sys.argv[1:])
    if not argv or argv[0] in {"-h", "--help", "help"}:
        print(__doc__.strip())
        return 0

    try:
        store_override, argv = _extract_flag(list(argv), "--store")
        store = _store_path(store_override)

        dry_run = "--dry-run" in argv
        argv = [a for a in argv if a != "--dry-run"]
        as_json = "--json" in argv
        argv = [a for a in argv if a != "--json"]
        repair_cfg = "--repair" in argv
        argv = [a for a in argv if a != "--repair"]

        if not argv:
            print(__doc__.strip())
            return 0

        cfg = load_kalender_config(repair=repair_cfg)["config"]
        cfg_defaults = cfg.get("defaults") or {}
        cfg_output = cfg.get("output") or {}

        cmd = argv[0].lower()
        rest = argv[1:]

        # --- check-backend / check-config ---
        if cmd == "check-backend":
            return cmd_check_backend(as_json=as_json)
        if cmd == "check-config":
            return cmd_check_config(as_json=as_json, repair=repair_cfg)

        # --- calendar list | add | delete ---
        if cmd == "calendar":
            if not rest:
                raise ValueError("Verwendung: kalender_core.py calendar <list|add|delete> ...")
            sub = rest[0].lower()
            sub_args = rest[1:]
            if sub == "list":
                cals = list_calendars(store)
                if as_json:
                    print(json.dumps({"count": len(cals), "calendars": cals}, ensure_ascii=False, indent=2))
                else:
                    print(f"=== Kalender-Profile ({len(cals)}) ===")
                    for c in cals:
                        d_tag = " [Default]" if c.get("is_default") else ""
                        cat_tag = f" ({c['category']})" if c.get("category") else ""
                        print(
                            f"  {c['id']:<22s} | {c['name']}{cat_tag}{d_tag} | "
                            f"{c.get('color') or '-'} | Termine: {c.get('event_count', 0)}"
                        )
                return 0
            if sub == "add":
                name, sub_args = _extract_flag(sub_args, "--name")
                category, sub_args = _extract_flag(sub_args, "--category")
                color, sub_args = _extract_flag(sub_args, "--color")
                description, sub_args = _extract_flag(sub_args, "--description")
                if not sub_args or not name:
                    raise ValueError(
                        'Verwendung: kalender_core.py calendar add <id> --name "..." '
                        '[--category ...] [--color "#2563eb"] [--description "..."]'
                    )
                cal_id = sub_args[0]
                created = add_calendar(
                    store,
                    cal_id,
                    name,
                    category=category,
                    color=color,
                    description=description,
                )
                if as_json:
                    print(json.dumps(created, ensure_ascii=False, indent=2))
                else:
                    print(f"[kalender] Kalender angelegt: {created['id']} ({created['name']})")
                return 0
            if sub == "delete":
                if not sub_args:
                    raise ValueError("Verwendung: kalender_core.py calendar delete <id>")
                cal_id = sub_args[0]
                ok = delete_calendar(store, cal_id)
                if as_json:
                    print(json.dumps({"deleted": ok, "id": cal_id}, ensure_ascii=False, indent=2))
                elif ok:
                    print(f"[kalender] Kalender {cal_id!r} gelöscht.")
                else:
                    print(f"[kalender] Kalender {cal_id!r} nicht gefunden.")
                return 0 if ok else 1
            raise ValueError(f"Unbekannter calendar-Unterbefehl: {sub!r} (erlaubt: list, add, delete)")

        # --- add ---
        if cmd == "add":
            event_date, rest = _extract_flag(rest, "--date")
            time_, rest = _extract_flag(rest, "--time")
            end_time, rest = _extract_flag(rest, "--end-time")
            dur_s, rest = _extract_flag(rest, "--duration")
            location, rest = _extract_flag(rest, "--location")
            description, rest = _extract_flag(rest, "--note")
            cal_id, rest = _extract_flag(rest, "--calendar")
            category, rest = _extract_flag(rest, "--category")
            recurrence, rest = _extract_flag(rest, "--recurrence")
            status_val, rest = _extract_flag(rest, "--status")

            if not rest:
                print(
                    'Verwendung: kalender_core.py add "Titel" --date YYYY-MM-DD '
                    '[--time HH:MM] [--end-time HH:MM] [--duration min] '
                    '[--calendar user] [--category ...] [--location "..."] [--note "..."]'
                )
                return 1
            title = rest[0]
            if not event_date:
                print("[kalender] --date YYYY-MM-DD ist Pflicht.")
                return 1
            duration_min = int(dur_s) if dur_s else None
            target_cal = cal_id or str(cfg_defaults.get("calendar") or "user")

            if dry_run:
                payload = {
                    "dry_run": True,
                    "title": title,
                    "date": event_date,
                    "time": time_,
                    "calendar_id": target_cal,
                }
                if as_json:
                    print(json.dumps(payload, ensure_ascii=False, indent=2))
                else:
                    print(f"[DRY-RUN] Würde Termin anlegen: {title!r} am {event_date} {time_ or ''} [{target_cal}]")
                return 0

            record_id = add_event(
                store,
                title,
                event_date,
                time_,
                duration_min,
                location,
                description,
                recurrence,
                calendar_id=target_cal,
                category=category,
                end_time=end_time,
                status=status_val or "planned",
            )
            if as_json:
                ev = _query_events(store, record_id=record_id)
                print(json.dumps(ev[0] if ev else {"id": record_id}, ensure_ascii=False, indent=2))
            else:
                print(f"[kalender] Termin gespeichert: {title!r} am {event_date} [{record_id}] (Silo: {target_cal})")
            return 0

        # --- Gemeinsame Abfragefilter für Zeitraum-/Listenbefehle ---
        if cmd in {"today", "day", "week", "month", "year", "range", "list"}:
            cal_filter, rest = _extract_flag(rest, "--calendar")
            cat_filter, rest = _extract_flag(rest, "--category")
            search_filter, rest = _extract_flag(rest, "--search")

            if cmd in {"today", "day"}:
                day_arg, rest = _extract_flag(rest, "--date")
                target_day = _validate_date(day_arg) if day_arg else date.today().isoformat()
                evs = (
                    [e for e in _DRY_EVENTS if e["date"] == target_day]
                    if dry_run
                    else get_events_by_date_range(
                        store,
                        target_day,
                        target_day,
                        calendar=cal_filter or "all",
                        category=cat_filter,
                        search=search_filter,
                    )
                )
                return _emit_events_result(
                    f"=== Tag ({target_day}) ===",
                    "Keine Termine an diesem Tag.",
                    evs,
                    as_json=as_json,
                )

            if cmd == "week":
                from_arg, rest = _extract_flag(rest, "--from")
                from_str = _validate_date(from_arg) if from_arg else date.today().isoformat()
                to_str = (date.fromisoformat(from_str) + timedelta(days=6)).isoformat()
                evs = (
                    list(_DRY_EVENTS)
                    if dry_run
                    else get_events_by_date_range(
                        store,
                        from_str,
                        to_str,
                        calendar=cal_filter or "all",
                        category=cat_filter,
                        search=search_filter,
                    )
                )
                return _emit_events_result(
                    f"=== Woche ({from_str} – {to_str}) ===",
                    "Keine Termine diese Woche.",
                    evs,
                    as_json=as_json,
                    grouped_by_day=True,
                )

            if cmd == "month":
                m_arg, rest = _extract_flag(rest, "--month")
                m_str = m_arg or date.today().strftime("%Y-%m")
                start_d, end_d, _ = resolve_view_window("month", month_str=m_str)
                evs = (
                    list(_DRY_EVENTS)
                    if dry_run
                    else get_events_by_date_range(
                        store,
                        start_d.isoformat(),
                        end_d.isoformat(),
                        calendar=cal_filter or "all",
                        category=cat_filter,
                        search=search_filter,
                    )
                )
                return _emit_events_result(
                    f"=== Monat {m_str} ({start_d.isoformat()} – {end_d.isoformat()}) ===",
                    "Keine Termine in diesem Monat.",
                    evs,
                    as_json=as_json,
                )

            if cmd == "year":
                y_arg, rest = _extract_flag(rest, "--year")
                y_str = y_arg or str(date.today().year)
                start_d, end_d, _ = resolve_view_window("year", year_str=y_str)
                evs = (
                    list(_DRY_EVENTS)
                    if dry_run
                    else get_events_by_date_range(
                        store,
                        start_d.isoformat(),
                        end_d.isoformat(),
                        calendar=cal_filter or "all",
                        category=cat_filter,
                        search=search_filter,
                    )
                )
                return _emit_events_result(
                    f"=== Jahr {y_str} ({len(evs)} Termine) ===",
                    "Keine Termine in diesem Jahr.",
                    evs,
                    as_json=as_json,
                    grouped_by_day=True,
                )

            if cmd == "range":
                f_arg, rest = _extract_flag(rest, "--from")
                t_arg, rest = _extract_flag(rest, "--to")
                start_d, end_d, _ = resolve_view_window("range", range_from=f_arg, range_to=t_arg)
                evs = (
                    list(_DRY_EVENTS)
                    if dry_run
                    else get_events_by_date_range(
                        store,
                        start_d.isoformat(),
                        end_d.isoformat(),
                        calendar=cal_filter or "all",
                        category=cat_filter,
                        search=search_filter,
                    )
                )
                return _emit_events_result(
                    f"=== Zeitraum ({start_d.isoformat()} – {end_d.isoformat()}) ===",
                    "Keine Termine in diesem Zeitraum.",
                    evs,
                    as_json=as_json,
                    grouped_by_day=True,
                )

            # list
            lim_arg, rest = _extract_flag(rest, "--limit")
            from_arg, rest = _extract_flag(rest, "--from")
            to_arg, rest = _extract_flag(rest, "--to")
            limit = int(lim_arg) if lim_arg else int(cfg_defaults.get("default_list_limit") or 50)
            evs = (
                list(_DRY_EVENTS)
                if dry_run
                else list_events(
                    store,
                    search_filter,
                    limit,
                    calendar=cal_filter or "all",
                    category=cat_filter,
                    from_date=from_arg,
                    to_date=to_arg,
                )
            )
            label = f"(Suche: {search_filter!r}) " if search_filter else ""
            return _emit_events_result(
                f"=== Termine {label}({len(evs)}) ===",
                "Keine Termine gefunden.",
                evs,
                as_json=as_json,
            )

        # --- delete ---
        if cmd == "delete":
            if not rest:
                print("Verwendung: kalender_core.py delete <id>")
                return 1
            record_id = rest[0]
            if dry_run:
                print(f"[DRY-RUN] Würde Termin {record_id!r} löschen.")
                return 0
            ok = delete_event(store, record_id)
            if as_json:
                print(json.dumps({"deleted": ok, "id": record_id}, ensure_ascii=False, indent=2))
            elif ok:
                print(f"[kalender] Termin {record_id!r} gelöscht.")
            else:
                print(f"[kalender] Termin {record_id!r} nicht gefunden.")
            return 0 if ok else 1

        # --- Silo-Operationen: mirror / sync-mirrors / transfer / clone ---
        if cmd in {"mirror", "transfer", "clone"}:
            target_cal, rest = _extract_flag(rest, "--to")
            if not rest or not target_cal:
                raise ValueError(f"Verwendung: kalender_core.py {cmd} <event_id> --to <target_calendar_id>")
            ev_id = rest[0]
            if cmd == "mirror":
                res = mirror_event(store, ev_id, target_cal)
            elif cmd == "transfer":
                res = transfer_event(store, ev_id, target_cal)
            else:
                res = clone_event(store, ev_id, target_cal)
            if as_json:
                print(json.dumps(res, ensure_ascii=False, indent=2))
            else:
                print(f"[kalender] {res['action']}: {ev_id} -> {target_cal} (ID: {res['id']})")
            return 0

        if cmd == "sync-mirrors":
            res = sync_mirrors(store)
            if as_json:
                print(json.dumps(res, ensure_ascii=False, indent=2))
            else:
                print(
                    f"[kalender] Spiegel-Sync: aktualisiert={res['updated']}, "
                    f"unverändert={res['unchanged']}, verwaist={res['orphaned']}"
                )
            return 0

        # --- import-ics ---
        if cmd == "import-ics":
            cal_id, rest = _extract_flag(rest, "--calendar")
            if not rest:
                raise ValueError("Verwendung: kalender_core.py import-ics <pfad.ics> [--calendar terminpilot]")
            default_imp = str(cfg_defaults.get("import_calendar") or "terminpilot")
            res = import_ics(store, Path(rest[0]), calendar_id=cal_id or default_imp)
            if as_json:
                print(json.dumps(res, ensure_ascii=False, indent=2))
            else:
                print(
                    f"[kalender] ICS-Import in {res['calendar_id']!r}: "
                    f"neu={res['imported']}, aktualisiert={res['updated']}, unverändert={res['unchanged']}"
                )
            return 0

        # --- export ---
        if cmd == "export":
            record_id, rest = _extract_flag(rest, "--id")
            cal_filter, rest = _extract_flag(rest, "--calendar")
            cat_filter, rest = _extract_flag(rest, "--category")
            from_arg, rest = _extract_flag(rest, "--from")
            to_arg, rest = _extract_flag(rest, "--to")
            search_arg, rest = _extract_flag(rest, "--search")
            out_path, rest = _extract_flag(rest, "--out")

            if dry_run:
                print("[DRY-RUN] ICS-Export übersprungen.")
                return 0
            ics_content = export_ics(
                store,
                record_id,
                calendar=cal_filter or "all",
                category=cat_filter,
                from_date=from_arg,
                to_date=to_arg,
                search=search_arg,
            )
            if not ics_content.strip():
                print("[kalender] Keine Termine zum Exportieren.")
                return 0
            if out_path:
                Path(out_path).parent.mkdir(parents=True, exist_ok=True)
                Path(out_path).write_text(ics_content, encoding="utf-8", newline="")
                if as_json:
                    print(json.dumps({"output_path": out_path, "bytes": len(ics_content.encode("utf-8"))}, ensure_ascii=False, indent=2))
                else:
                    print(f"[kalender] ICS exportiert: {out_path}")
            else:
                print(ics_content)
            return 0

        # --- report / render ---
        if cmd in {"report", "render"}:
            view_arg, rest = _extract_flag(rest, "--view")
            fmt_arg, rest = _extract_flag(rest, "--format")
            day_arg, rest = _extract_flag(rest, "--date")
            month_arg, rest = _extract_flag(rest, "--month")
            year_arg, rest = _extract_flag(rest, "--year")
            from_arg, rest = _extract_flag(rest, "--from")
            to_arg, rest = _extract_flag(rest, "--to")
            cal_arg, rest = _extract_flag(rest, "--calendar")
            cat_arg, rest = _extract_flag(rest, "--category")
            search_arg, rest = _extract_flag(rest, "--search")
            title_arg, rest = _extract_flag(rest, "--title")
            out_arg, rest = _extract_flag(rest, "--out")

            if not view_arg:
                if year_arg:
                    view_arg = "year"
                elif month_arg:
                    view_arg = "month"
                elif day_arg:
                    view_arg = "day"
                elif from_arg and to_arg:
                    view_arg = "range"
                elif from_arg:
                    view_arg = "week"
                else:
                    view_arg = str(cfg_output.get("default_view") or "month")

            fmt_norm = (fmt_arg or str(cfg_output.get("default_format") or "html")).strip().lower()
            if fmt_norm == "pdf" and not out_arg:
                raise ValueError("--format pdf erfordert --out <pfad.pdf>.")

            rep = render_report(
                store,
                view=view_arg,
                fmt=fmt_norm,
                day_str=day_arg,
                week_from=from_arg if view_arg == "week" else None,
                month_str=month_arg,
                year_str=year_arg,
                range_from=from_arg,
                range_to=to_arg,
                calendar=cal_arg or "all",
                category=cat_arg,
                search=search_arg,
                title=title_arg,
                out_path=out_arg,
            )

            meta = {k: v for k, v in rep.items() if k not in {"content", "pdf_bytes"}}
            if as_json:
                if not out_arg and rep["content"] is not None:
                    meta["content"] = rep["content"]
                print(json.dumps(meta, ensure_ascii=False, indent=2))
                return 0
            if out_arg:
                print(
                    f"[kalender] Bericht erstellt ({rep['format'].upper()}, {rep['view']}): "
                    f"{rep['output_path']} ({rep['bytes']} Bytes, {rep['events_count']} Termine)"
                )
                return 0
            print(rep["content"] or "")
            return 0

        print(f"Unbekannter Befehl: {cmd!r}")
        print(
            "Verfügbar: add, today, day, week, month, year, range, list, delete, "
            "calendar, mirror, sync-mirrors, transfer, clone, import-ics, export, report, render, check-backend"
        )
        return 1
    except (ValueError, FileNotFoundError, sqlite3.Error) as exc:
        if "--json" in (argv or []):
            print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        else:
            print(f"[kalender] Fehler: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.exit(main())
