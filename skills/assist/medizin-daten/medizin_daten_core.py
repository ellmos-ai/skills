#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
medizin_daten_core.py — Headless lokale Medizindaten-Erfassung.

Portiert aus: Eigenentwurf (kein BACH-Origin)
Store:        SQLite — assist/medizin-daten/store.db (eigener Store, kein bach.db)
Abhaengigkeit: nur Python-Stdlib + sqlite3

DATENSCHUTZ-HINWEIS: Diese Datei verarbeitet besonders schützenswerte
Gesundheitsdaten. store.db NIEMALS in Git committen oder in Cloud-Ordner
ablegen. Kein Netzwerkzugriff in diesem Modul.

Verwendung (CLI):
  python medizin_daten_core.py add-diagnosis "Hypertonie" [--icd I10] [--note "..."]
  python medizin_daten_core.py diagnoses [--dry-run]
  python medizin_daten_core.py add-symptom "Kopfschmerzen" [--severity 7] [--date YYYY-MM-DD]
  python medizin_daten_core.py symptom-history "Kopfschmerzen" [--limit 30]
  python medizin_daten_core.py add-exam "Blutbild" [--date YYYY-MM-DD] [--note "nuechtern"]
  python medizin_daten_core.py exams [--upcoming]
  python medizin_daten_core.py --store /tmp/med_test.db diagnoses --dry-run

  # Arzttermine (UC: Arzttermine verwalten)
  python medizin_daten_core.py add-appointment "Kardiologie" [--date YYYY-MM-DD] [--doctor "Dr. Muster"] [--note "..."]
  python medizin_daten_core.py appointments [--upcoming]

  # Dokumentenverzeichnis (UC: Med-Dokumentenverzeichnis aktualisieren)
  python medizin_daten_core.py add-document "Arztbrief Kardiologie" --path /pfad/zu/datei.pdf [--category brief] [--date YYYY-MM-DD]
  python medizin_daten_core.py documents [--category brief]
"""

from __future__ import annotations

import os
import sqlite3
import sys
import uuid
from datetime import datetime, date
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Pfade (userneutral, relativ zum Skill)
# ---------------------------------------------------------------------------

_SKILL_DIR = Path(__file__).resolve().parent
_DEFAULT_STORE = _SKILL_DIR / "store.db"
_ENV_STORE = os.environ.get("MEDIZIN_STORE")

# Sync-Ordner-Warnung: medizinische Daten nicht in Cloud-Sync-Pfaden ablegen
_SYNC_INDICATORS = ["OneDrive", "Dropbox", "iCloud", "Google Drive", "Nextcloud"]


def _store_path(cli_override: Optional[str] = None) -> Path:
    if cli_override:
        return Path(cli_override)
    if _ENV_STORE:
        return Path(_ENV_STORE)
    return _DEFAULT_STORE


def _warn_if_cloud(store: Path) -> None:
    """Gibt eine Warnung aus wenn der Store-Pfad in einem Cloud-Sync-Ordner liegt."""
    p = str(store.resolve())
    for indicator in _SYNC_INDICATORS:
        if indicator.lower() in p.lower():
            print(
                f"[WARNUNG] Medizin-Store liegt in einem Cloud-Sync-Ordner ({indicator})!\n"
                f"  Pfad: {p}\n"
                f"  Empfehlung: Store in einen lokalen (nicht-synced) Ordner verlegen.\n"
                f"  Override via: MEDIZIN_STORE=/lokaler/pfad/store.db",
                file=sys.stderr,
            )
            break


# ---------------------------------------------------------------------------
# Store (SQLite)
# ---------------------------------------------------------------------------

_SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS diagnoses (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    icd_code    TEXT,
    onset_date  TEXT,
    status      TEXT DEFAULT 'aktiv',
    note        TEXT,
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS symptoms (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),
    name         TEXT NOT NULL,
    severity     INTEGER,
    recorded_at  TEXT NOT NULL,
    note         TEXT
);

CREATE TABLE IF NOT EXISTS examination_plans (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),
    exam_name    TEXT NOT NULL,
    planned_date TEXT,
    done_date    TEXT,
    note         TEXT,
    created_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS appointments (
    id           TEXT PRIMARY KEY,
    title        TEXT NOT NULL,
    appointment_date TEXT,
    doctor       TEXT,
    location     TEXT,
    status       TEXT DEFAULT 'geplant',
    note         TEXT,
    created_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS documents (
    id           TEXT PRIMARY KEY,
    title        TEXT NOT NULL,
    file_path    TEXT,
    category     TEXT DEFAULT 'sonstiges',
    document_date TEXT,
    note         TEXT,
    created_at   TEXT NOT NULL
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


# ---------------------------------------------------------------------------
# Diagnosen
# ---------------------------------------------------------------------------

def add_diagnosis(store: Path, name: str, icd_code: Optional[str] = None,
                  onset_date: Optional[str] = None, note: Optional[str] = None) -> str:
    """Legt eine neue Diagnose an; gibt die ID zurueck."""
    record_id = _short_id()
    now = _now()
    conn = _open_store(store)
    conn.execute(
        """INSERT INTO diagnoses (id, name, icd_code, onset_date, note, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (record_id, name, icd_code, onset_date, note, now, now),
    )
    conn.commit()
    conn.close()
    return record_id


def list_diagnoses(store: Path, only_active: bool = False) -> list[dict]:
    if not store.exists():
        return []
    conn = _open_store(store)
    query = "SELECT * FROM diagnoses"
    if only_active:
        query += " WHERE status = 'aktiv'"
    query += " ORDER BY created_at DESC"
    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_diagnosis_status(store: Path, record_id: str, status: str) -> bool:
    """Aktualisiert den Status einer Diagnose (aktiv/remission/abgeschlossen)."""
    if not store.exists():
        return False
    conn = _open_store(store)
    cursor = conn.execute(
        "UPDATE diagnoses SET status = ?, updated_at = ? WHERE id = ?",
        (status, _now(), record_id),
    )
    conn.commit()
    changed = cursor.rowcount > 0
    conn.close()
    return changed


# ---------------------------------------------------------------------------
# Symptome
# ---------------------------------------------------------------------------

def add_symptom(store: Path, name: str, severity: Optional[int] = None,
                recorded_at: Optional[str] = None, note: Optional[str] = None,
                diagnosis_id: Optional[str] = None) -> str:
    """Erfasst ein Symptom; gibt die ID zurueck."""
    if severity is not None:
        severity = max(1, min(10, severity))  # Clamp 1–10
    record_id = _short_id()
    ts = recorded_at or _now()
    conn = _open_store(store)
    conn.execute(
        """INSERT INTO symptoms (id, diagnosis_id, name, severity, recorded_at, note)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (record_id, diagnosis_id, name, severity, ts, note),
    )
    conn.commit()
    conn.close()
    return record_id


def symptom_history(store: Path, name: str, limit: int = 30) -> list[dict]:
    """Verlauf eines Symptoms nach Bezeichnung (Teilstring)."""
    if not store.exists():
        return []
    conn = _open_store(store)
    rows = conn.execute(
        """SELECT * FROM symptoms
           WHERE LOWER(name) LIKE ?
           ORDER BY recorded_at DESC LIMIT ?""",
        (f"%{name.lower()}%", limit),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def list_symptoms(store: Path, limit: int = 50) -> list[dict]:
    if not store.exists():
        return []
    conn = _open_store(store)
    rows = conn.execute(
        "SELECT * FROM symptoms ORDER BY recorded_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Untersuchungspläne
# ---------------------------------------------------------------------------

def add_exam(store: Path, exam_name: str, planned_date: Optional[str] = None,
             note: Optional[str] = None, diagnosis_id: Optional[str] = None) -> str:
    """Plant eine Untersuchung; gibt die ID zurueck."""
    record_id = _short_id()
    conn = _open_store(store)
    conn.execute(
        """INSERT INTO examination_plans
           (id, diagnosis_id, exam_name, planned_date, note, created_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (record_id, diagnosis_id, exam_name, planned_date, note, _now()),
    )
    conn.commit()
    conn.close()
    return record_id


def mark_exam_done(store: Path, record_id: str,
                   done_date: Optional[str] = None) -> bool:
    """Markiert eine Untersuchung als durchgefuehrt."""
    if not store.exists():
        return False
    conn = _open_store(store)
    cursor = conn.execute(
        "UPDATE examination_plans SET done_date = ? WHERE id = ?",
        (done_date or _now(), record_id),
    )
    conn.commit()
    changed = cursor.rowcount > 0
    conn.close()
    return changed


def list_exams(store: Path, upcoming_only: bool = False) -> list[dict]:
    if not store.exists():
        return []
    conn = _open_store(store)
    query = "SELECT * FROM examination_plans"
    if upcoming_only:
        query += " WHERE done_date IS NULL"
    query += " ORDER BY planned_date ASC, created_at DESC"
    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Arzttermine (UC: Arzttermine verwalten)
# ---------------------------------------------------------------------------

def add_appointment(store: Path, title: str,
                    appointment_date: Optional[str] = None,
                    doctor: Optional[str] = None,
                    location: Optional[str] = None,
                    note: Optional[str] = None) -> str:
    """Legt einen neuen Arzttermin an; gibt die ID zurueck."""
    record_id = _short_id()
    conn = _open_store(store)
    conn.execute(
        """INSERT INTO appointments
           (id, title, appointment_date, doctor, location, note, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (record_id, title, appointment_date, doctor, location, note, _now()),
    )
    conn.commit()
    conn.close()
    return record_id


def list_appointments(store: Path, upcoming_only: bool = False) -> list[dict]:
    """Gibt Arzttermine zurueck; optional nur zukuenftige."""
    if not store.exists():
        return []
    conn = _open_store(store)
    query = "SELECT * FROM appointments"
    if upcoming_only:
        today = date.today().isoformat()
        query += f" WHERE (appointment_date IS NULL OR appointment_date >= '{today}') AND status != 'erledigt'"
    query += " ORDER BY appointment_date ASC, created_at DESC"
    rows = conn.execute(query).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_appointment_done(store: Path, record_id: str) -> bool:
    """Markiert einen Termin als erledigt."""
    if not store.exists():
        return False
    conn = _open_store(store)
    cursor = conn.execute(
        "UPDATE appointments SET status = 'erledigt' WHERE id = ?",
        (record_id,),
    )
    conn.commit()
    changed = cursor.rowcount > 0
    conn.close()
    return changed


# ---------------------------------------------------------------------------
# Dokumentenverzeichnis (UC: Med-Dokumentenverzeichnis aktualisieren)
# ---------------------------------------------------------------------------

def add_document(store: Path, title: str, file_path: Optional[str] = None,
                 category: str = "sonstiges",
                 document_date: Optional[str] = None,
                 note: Optional[str] = None) -> str:
    """Registriert ein medizinisches Dokument im Verzeichnis; gibt die ID zurueck.

    Speichert nur den Pfad (Index), liest/verschiebt die Datei NICHT.
    """
    record_id = _short_id()
    conn = _open_store(store)
    conn.execute(
        """INSERT INTO documents
           (id, title, file_path, category, document_date, note, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (record_id, title, file_path, category, document_date, note, _now()),
    )
    conn.commit()
    conn.close()
    return record_id


def list_documents(store: Path, category: Optional[str] = None) -> list[dict]:
    """Listet registrierte Dokumente; optional nach Kategorie gefiltert."""
    if not store.exists():
        return []
    conn = _open_store(store)
    query = "SELECT * FROM documents"
    params: list = []
    if category:
        query += " WHERE category = ?"
        params.append(category)
    query += " ORDER BY document_date DESC, created_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Dry-Run-Beispieldaten
# ---------------------------------------------------------------------------

_DRY_DIAGNOSES = [
    {"id": "diag-1", "name": "Hypertonie", "icd_code": "I10",
     "onset_date": "2025-01-15", "status": "aktiv", "note": "Beispiel-Diagnose"},
    {"id": "diag-2", "name": "Saisonale Allergie", "icd_code": "J30.1",
     "onset_date": None, "status": "aktiv", "note": ""},
]

_DRY_SYMPTOMS = [
    {"id": "sym-1", "name": "Kopfschmerzen", "severity": 5,
     "recorded_at": date.today().isoformat(), "note": ""},
    {"id": "sym-2", "name": "Schwindel", "severity": 3,
     "recorded_at": date.today().isoformat(), "note": ""},
]

_DRY_EXAMS = [
    {"id": "ex-1", "exam_name": "Blutbild", "planned_date": "2026-07-01",
     "done_date": None, "note": "nuechtern erscheinen"},
    {"id": "ex-2", "exam_name": "EKG", "planned_date": "2026-07-15",
     "done_date": None, "note": ""},
]

_DRY_APPOINTMENTS = [
    {"id": "ap-1", "title": "Hausarzt Kontrolle", "appointment_date": "2026-07-10",
     "doctor": "Dr. Muster", "location": "Praxis Musterstraße", "status": "geplant", "note": ""},
    {"id": "ap-2", "title": "Facharzt Dermatologie", "appointment_date": "2026-08-05",
     "doctor": None, "location": None, "status": "geplant", "note": ""},
]

_DRY_DOCUMENTS = [
    {"id": "doc-1", "title": "Arztbrief Kardiologie 2026", "file_path": "/lokal/arztbrief_kardio.pdf",
     "category": "brief", "document_date": "2026-04-15", "note": ""},
    {"id": "doc-2", "title": "Blutbild-Ergebnis April 2026", "file_path": None,
     "category": "laborwert", "document_date": "2026-04-20", "note": ""},
]


# ---------------------------------------------------------------------------
# Formatierung
# ---------------------------------------------------------------------------

def _fmt_diagnosis(d: dict) -> str:
    icd = f" [{d['icd_code']}]" if d.get("icd_code") else ""
    note = f" — {d['note']}" if d.get("note") else ""
    return f"  [{d['id']}] {d['name']}{icd} | {d['status']}{note}"


def _fmt_symptom(s: dict) -> str:
    sev = f" | Schwere: {s['severity']}/10" if s.get("severity") else ""
    ts = s.get("recorded_at", "")[:19]
    note = f" — {s['note']}" if s.get("note") else ""
    return f"  [{s['id']}] {ts} | {s['name']}{sev}{note}"


def _fmt_exam(e: dict) -> str:
    status = f"erledigt am {e['done_date'][:10]}" if e.get("done_date") else "ausstehend"
    planned = f" | geplant: {e['planned_date']}" if e.get("planned_date") else ""
    note = f" — {e['note']}" if e.get("note") else ""
    return f"  [{e['id']}] {e['exam_name']}{planned} | {status}{note}"


def _fmt_appointment(a: dict) -> str:
    dt = f" | {a['appointment_date']}" if a.get("appointment_date") else ""
    doctor = f" | {a['doctor']}" if a.get("doctor") else ""
    loc = f" @ {a['location']}" if a.get("location") else ""
    note = f" — {a['note']}" if a.get("note") else ""
    status = a.get("status", "geplant")
    return f"  [{a['id']}] {a['title']}{dt}{doctor}{loc} | {status}{note}"


def _fmt_document(d: dict) -> str:
    cat = f" [{d['category']}]" if d.get("category") else ""
    dt = f" | {d['document_date'][:10]}" if d.get("document_date") else ""
    path = f" → {d['file_path']}" if d.get("file_path") else ""
    note = f" — {d['note']}" if d.get("note") else ""
    return f"  [{d['id']}] {d['title']}{cat}{dt}{path}{note}"


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

    # Privacy-Gate: Warnung bei Cloud-Pfad (nur wenn echter Store)
    if not dry_run:
        _warn_if_cloud(store)

    if not argv:
        print(__doc__)
        return 0

    cmd = argv[0].lower()

    # --- add-diagnosis ---
    if cmd == "add-diagnosis":
        if len(argv) < 2:
            print("Verwendung: medizin_daten_core.py add-diagnosis <Name> [--icd CODE] [--note TEXT] [--date YYYY-MM-DD]")
            return 1
        args = argv[1:]
        name = args[0]
        icd = None
        onset = None
        note = None
        if "--icd" in args:
            idx = args.index("--icd")
            if idx + 1 < len(args):
                icd = args[idx + 1]
        if "--date" in args:
            idx = args.index("--date")
            if idx + 1 < len(args):
                onset = args[idx + 1]
        if "--note" in args:
            idx = args.index("--note")
            if idx + 1 < len(args):
                note = args[idx + 1]
        if dry_run:
            print(f"[DRY-RUN] Wuerde Diagnose anlegen: {name!r} (ICD: {icd}, Datum: {onset})")
            return 0
        record_id = add_diagnosis(store, name, icd, onset, note)
        print(f"[medizin] Diagnose gespeichert: {name!r} [{record_id}]")
        return 0

    # --- diagnoses ---
    if cmd == "diagnoses":
        if dry_run:
            rows = _DRY_DIAGNOSES
            print("[DRY-RUN] Beispiel-Diagnosen:")
        else:
            rows = list_diagnoses(store)
        if not rows:
            print("[medizin] Keine Diagnosen gespeichert.")
            return 0
        print(f"=== Diagnosen ({len(rows)}) ===")
        for d in rows:
            print(_fmt_diagnosis(d))
        return 0

    # --- add-symptom ---
    if cmd == "add-symptom":
        if len(argv) < 2:
            print("Verwendung: medizin_daten_core.py add-symptom <Name> [--severity 1-10] [--date YYYY-MM-DD] [--note TEXT]")
            return 1
        args = argv[1:]
        name = args[0]
        severity = None
        recorded_at = None
        note = None
        if "--severity" in args:
            idx = args.index("--severity")
            if idx + 1 < len(args):
                try:
                    severity = int(args[idx + 1])
                except ValueError:
                    pass
        if "--date" in args:
            idx = args.index("--date")
            if idx + 1 < len(args):
                recorded_at = args[idx + 1]
        if "--note" in args:
            idx = args.index("--note")
            if idx + 1 < len(args):
                note = args[idx + 1]
        if dry_run:
            print(f"[DRY-RUN] Wuerde Symptom erfassen: {name!r} (Schwere: {severity})")
            return 0
        record_id = add_symptom(store, name, severity, recorded_at, note)
        print(f"[medizin] Symptom gespeichert: {name!r} [{record_id}]")
        return 0

    # --- symptom-history ---
    if cmd == "symptom-history":
        if len(argv) < 2:
            print("Verwendung: medizin_daten_core.py symptom-history <Name> [--limit 30]")
            return 1
        name = argv[1]
        limit = 30
        if "--limit" in argv:
            idx = argv.index("--limit")
            if idx + 1 < len(argv):
                try:
                    limit = int(argv[idx + 1])
                except ValueError:
                    pass
        if dry_run:
            rows = [s for s in _DRY_SYMPTOMS if name.lower() in s["name"].lower()]
            print(f"[DRY-RUN] Symptomverlauf fuer {name!r}:")
        else:
            rows = symptom_history(store, name, limit)
        if not rows:
            print(f"[medizin] Keine Eintraege fuer Symptom: {name!r}")
            return 0
        print(f"=== Verlauf: {name!r} ({len(rows)} Eintraege) ===")
        for s in rows:
            print(_fmt_symptom(s))
        return 0

    # --- add-exam ---
    if cmd == "add-exam":
        if len(argv) < 2:
            print("Verwendung: medizin_daten_core.py add-exam <Name> [--date YYYY-MM-DD] [--note TEXT]")
            return 1
        args = argv[1:]
        exam_name = args[0]
        planned_date = None
        note = None
        if "--date" in args:
            idx = args.index("--date")
            if idx + 1 < len(args):
                planned_date = args[idx + 1]
        if "--note" in args:
            idx = args.index("--note")
            if idx + 1 < len(args):
                note = args[idx + 1]
        if dry_run:
            print(f"[DRY-RUN] Wuerde Untersuchung planen: {exam_name!r} am {planned_date}")
            return 0
        record_id = add_exam(store, exam_name, planned_date, note)
        print(f"[medizin] Untersuchung geplant: {exam_name!r} [{record_id}]")
        return 0

    # --- exams ---
    if cmd == "exams":
        upcoming = "--upcoming" in argv
        if dry_run:
            rows = _DRY_EXAMS
            print("[DRY-RUN] Beispiel-Untersuchungen:")
        else:
            rows = list_exams(store, upcoming_only=upcoming)
        if not rows:
            label = "ausstehende" if upcoming else "geplante"
            print(f"[medizin] Keine {label} Untersuchungen.")
            return 0
        label = "Ausstehende" if upcoming else "Alle"
        print(f"=== {label} Untersuchungen ({len(rows)}) ===")
        for e in rows:
            print(_fmt_exam(e))
        return 0

    # --- exam-done ---
    if cmd == "exam-done":
        if len(argv) < 2:
            print("Verwendung: medizin_daten_core.py exam-done <id> [--date YYYY-MM-DD]")
            return 1
        record_id = argv[1]
        done_date = None
        if "--date" in argv:
            idx = argv.index("--date")
            if idx + 1 < len(argv):
                done_date = argv[idx + 1]
        if dry_run:
            print(f"[DRY-RUN] Wuerde Untersuchung {record_id!r} als erledigt markieren.")
            return 0
        ok = mark_exam_done(store, record_id, done_date)
        if ok:
            print(f"[medizin] Untersuchung {record_id!r} als erledigt markiert.")
        else:
            print(f"[medizin] Untersuchung {record_id!r} nicht gefunden.")
        return 0 if ok else 1

    # --- add-appointment ---
    if cmd == "add-appointment":
        if len(argv) < 2:
            print("Verwendung: medizin_daten_core.py add-appointment <Titel> [--date YYYY-MM-DD] [--doctor NAME] [--location ORT] [--note TEXT]")
            return 1
        args = argv[1:]
        title = args[0]
        appointment_date = None
        doctor = None
        location = None
        note = None
        if "--date" in args:
            idx = args.index("--date")
            if idx + 1 < len(args):
                appointment_date = args[idx + 1]
        if "--doctor" in args:
            idx = args.index("--doctor")
            if idx + 1 < len(args):
                doctor = args[idx + 1]
        if "--location" in args:
            idx = args.index("--location")
            if idx + 1 < len(args):
                location = args[idx + 1]
        if "--note" in args:
            idx = args.index("--note")
            if idx + 1 < len(args):
                note = args[idx + 1]
        if dry_run:
            print(f"[DRY-RUN] Wuerde Termin anlegen: {title!r} am {appointment_date}")
            return 0
        record_id = add_appointment(store, title, appointment_date, doctor, location, note)
        print(f"[medizin] Termin gespeichert: {title!r} [{record_id}]")
        return 0

    # --- appointments ---
    if cmd == "appointments":
        upcoming = "--upcoming" in argv
        if dry_run:
            rows = _DRY_APPOINTMENTS
            print("[DRY-RUN] Beispiel-Termine:")
        else:
            rows = list_appointments(store, upcoming_only=upcoming)
        if not rows:
            label = "bevorstehende" if upcoming else "gespeicherte"
            print(f"[medizin] Keine {label} Termine.")
            return 0
        label = "Bevorstehende" if upcoming else "Alle"
        print(f"=== {label} Arzttermine ({len(rows)}) ===")
        for a in rows:
            print(_fmt_appointment(a))
        return 0

    # --- add-document ---
    if cmd == "add-document":
        if len(argv) < 2:
            print("Verwendung: medizin_daten_core.py add-document <Titel> [--path /pfad/datei] [--category KAT] [--date YYYY-MM-DD] [--note TEXT]")
            return 1
        args = argv[1:]
        title = args[0]
        file_path = None
        category = "sonstiges"
        document_date = None
        note = None
        if "--path" in args:
            idx = args.index("--path")
            if idx + 1 < len(args):
                file_path = args[idx + 1]
        if "--category" in args:
            idx = args.index("--category")
            if idx + 1 < len(args):
                category = args[idx + 1]
        if "--date" in args:
            idx = args.index("--date")
            if idx + 1 < len(args):
                document_date = args[idx + 1]
        if "--note" in args:
            idx = args.index("--note")
            if idx + 1 < len(args):
                note = args[idx + 1]
        if dry_run:
            print(f"[DRY-RUN] Wuerde Dokument registrieren: {title!r} [{category}] @ {file_path}")
            return 0
        record_id = add_document(store, title, file_path, category, document_date, note)
        print(f"[medizin] Dokument registriert: {title!r} [{record_id}]")
        return 0

    # --- documents ---
    if cmd == "documents":
        category = None
        if "--category" in argv:
            idx = argv.index("--category")
            if idx + 1 < len(argv):
                category = argv[idx + 1]
        if dry_run:
            rows = _DRY_DOCUMENTS
            print("[DRY-RUN] Beispiel-Dokumente:")
        else:
            rows = list_documents(store, category)
        if not rows:
            print("[medizin] Keine Dokumente registriert.")
            return 0
        label = f" (Kategorie: {category})" if category else ""
        print(f"=== Dokumente{label} ({len(rows)}) ===")
        for d in rows:
            print(_fmt_document(d))
        return 0

    print(f"Unbekannter Befehl: {cmd!r}")
    print("Verfuegbar: add-diagnosis, diagnoses, add-symptom, symptom-history, "
          "add-exam, exams, exam-done, "
          "add-appointment, appointments, add-document, documents")
    return 1


if __name__ == "__main__":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.exit(main())
