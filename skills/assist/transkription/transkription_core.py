#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""
transkription_core.py — Headless Audio-Transkription via Whisper oder Vosk.

Portiert aus: Eigenentwurf (kein direkter BACH-Origin)
Inspiration:  BACH hub/_services/voice/voice_stt.py (Backend-Muster, read-only)
Store:        SQLite — assist/transkription/store.db (eigener Store, kein bach.db)
Abhaengigkeit: Python-Stdlib + sqlite3. Whisper/Vosk optional (Presence-Check).

Verwendung (CLI):
  python transkription_core.py check                       # Backend-Check
  python transkription_core.py transcribe audio.wav        # Transkribieren
  python transkription_core.py transcribe audio.mp3 --lang de
  python transkription_core.py transcribe audio.wav --dry-run
  python transkription_core.py list [--limit 20]           # Letzte Transkripte
  python transkription_core.py search "Begriff"            # Volltextsuche
  python transkription_core.py export <id> [--out out.txt] # Exportieren
  python transkription_core.py --store /tmp/t.db transcribe x.wav --dry-run
"""

from __future__ import annotations

import os
import sqlite3
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Pfade (userneutral, relativ zum Skill)
# ---------------------------------------------------------------------------

_SKILL_DIR = Path(__file__).resolve().parent
_DEFAULT_STORE = _SKILL_DIR / "store.db"

# Env-Override: TRANSKRIPTION_STORE
_ENV_STORE = os.environ.get("TRANSKRIPTION_STORE")


def _store_path(cli_override: Optional[str] = None) -> Path:
    if cli_override:
        return Path(cli_override)
    if _ENV_STORE:
        return Path(_ENV_STORE)
    return _DEFAULT_STORE


def _prefs_file() -> Optional[Path]:
    p = _SKILL_DIR.parent / "prefs.json"
    return p if p.exists() else None


def _read_pref(key: str) -> Optional[str]:
    pf = _prefs_file()
    if not pf:
        return None
    try:
        import json
        return json.loads(pf.read_text(encoding="utf-8")).get(key)
    except Exception:  # noqa: BLE001
        return None


# ---------------------------------------------------------------------------
# Store (SQLite)
# ---------------------------------------------------------------------------

_SCHEMA = """
CREATE TABLE IF NOT EXISTS transcripts (
    id          TEXT PRIMARY KEY,
    file_path   TEXT NOT NULL,
    file_name   TEXT NOT NULL,
    text        TEXT NOT NULL,
    language    TEXT,
    backend     TEXT,
    duration_s  REAL,
    created_at  TEXT NOT NULL,
    tags        TEXT
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


def save_transcript(store: Path, file_path: str, text: str, language: str = "de",
                    backend: str = "dry-run", duration_s: Optional[float] = None,
                    tags: Optional[str] = None) -> str:
    """Speichert ein Transkript; gibt die ID zurueck."""
    record_id = _short_id()
    conn = _open_store(store)
    conn.execute(
        """INSERT INTO transcripts
           (id, file_path, file_name, text, language, backend, duration_s, created_at, tags)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            record_id,
            file_path,
            Path(file_path).name,
            text,
            language,
            backend,
            duration_s,
            datetime.now().isoformat(),
            tags,
        ),
    )
    conn.commit()
    conn.close()
    return record_id


def list_transcripts(store: Path, limit: int = 20) -> list[dict]:
    if not store.exists():
        return []
    conn = _open_store(store)
    rows = conn.execute(
        "SELECT * FROM transcripts ORDER BY created_at DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def search_transcripts(store: Path, term: str) -> list[dict]:
    if not store.exists():
        return []
    conn = _open_store(store)
    rows = conn.execute(
        "SELECT * FROM transcripts WHERE LOWER(text) LIKE ? OR LOWER(file_name) LIKE ?"
        " ORDER BY created_at DESC",
        (f"%{term.lower()}%", f"%{term.lower()}%"),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_transcript(store: Path, record_id: str) -> Optional[dict]:
    if not store.exists():
        return None
    conn = _open_store(store)
    row = conn.execute("SELECT * FROM transcripts WHERE id = ?", (record_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# ---------------------------------------------------------------------------
# Backend-Erkennung (optionale Imports, nie hart)
# ---------------------------------------------------------------------------

def _detect_backend(preferred: Optional[str] = None) -> str:
    """Gibt 'whisper', 'vosk' oder 'none' zurueck."""
    order = ["whisper", "vosk"]
    if preferred and preferred in order:
        order = [preferred] + [x for x in order if x != preferred]

    for backend in order:
        try:
            if backend == "whisper":
                import whisper  # type: ignore  # noqa: F401
                return "whisper"
            elif backend == "vosk":
                import vosk  # type: ignore  # noqa: F401
                return "vosk"
        except ImportError:
            continue
    return "none"


def _transcribe_whisper(file_path: str, language: str = "de") -> tuple[str, Optional[float]]:
    """Transkribiert mit Whisper (lokal). Gibt (text, duration_s) zurueck."""
    import whisper  # type: ignore
    model_name = "base"  # konservativ; konfigurierbar via prefs
    model = whisper.load_model(model_name)
    result = model.transcribe(file_path, language=language)
    text = result.get("text", "").strip()
    # Whisper liefert keine Gesamtdauer direkt; aus Segmenten schaetzen
    segs = result.get("segments", [])
    duration = segs[-1]["end"] if segs else None
    return text, duration


def _transcribe_vosk(file_path: str, language: str = "de") -> tuple[str, Optional[float]]:
    """Transkribiert mit Vosk (offline). Gibt (text, None) zurueck."""
    import json as _json
    import wave
    from vosk import Model, KaldiRecognizer  # type: ignore

    # Vosk-Modell: im prefs.json konfigurierbar via 'vosk_model_path'
    model_path = _read_pref("vosk_model_path")
    if not model_path or not Path(model_path).exists():
        raise RuntimeError(
            "Vosk-Modell nicht gefunden. Bitte 'vosk_model_path' in assist/prefs.json setzen."
        )
    model = Model(model_path)
    wf = wave.open(file_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    parts = []
    while True:
        data = wf.readframes(4000)
        if not data:
            break
        if rec.AcceptWaveform(data):
            parts.append(_json.loads(rec.Result()).get("text", ""))
    parts.append(_json.loads(rec.FinalResult()).get("text", ""))
    wf.close()
    return " ".join(p for p in parts if p).strip(), None


# ---------------------------------------------------------------------------
# Hauptfunktion: Transkription
# ---------------------------------------------------------------------------

def transcribe(file_path: str, store: Path, language: str = "de",
               dry_run: bool = False, preferred_backend: Optional[str] = None) -> dict:
    """
    Transkribiert eine Audio-/Video-Datei.
    Gibt {'id', 'text', 'backend', 'duration_s'} zurueck.
    """
    if dry_run:
        text = f"[DRY-RUN] Platzhalter-Transkript fuer: {Path(file_path).name}"
        record_id = save_transcript(store, file_path, text, language, "dry-run")
        return {"id": record_id, "text": text, "backend": "dry-run", "duration_s": None}

    if not Path(file_path).exists():
        return {"error": f"Datei nicht gefunden: {file_path}"}

    backend = _detect_backend(preferred_backend)
    if backend == "none":
        return {
            "error": (
                "Kein Transkriptions-Backend verfuegbar. "
                "Bitte 'pip install openai-whisper' oder 'pip install vosk' ausfuehren, "
                "oder --dry-run fuer Demo-Modus nutzen."
            )
        }

    try:
        if backend == "whisper":
            text, duration = _transcribe_whisper(file_path, language)
        else:
            text, duration = _transcribe_vosk(file_path, language)
    except Exception as exc:  # noqa: BLE001
        return {"error": f"Transkriptions-Fehler ({backend}): {exc}"}

    record_id = save_transcript(store, file_path, text, language, backend, duration)
    return {"id": record_id, "text": text, "backend": backend, "duration_s": duration}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _resolve_store_from_args(args: list[str]) -> tuple[Path, list[str]]:
    """Extrahiert --store <pfad> aus args. Gibt (store_path, remaining_args) zurueck."""
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
    cmd = argv[0].lower() if argv else ""

    # --- check ---
    if cmd == "check":
        pref = _read_pref("transkription_backend")
        backend = _detect_backend(pref)
        if backend == "none":
            print("[transkription] Kein Backend gefunden.")
            print("  Whisper: pip install openai-whisper")
            print("  Vosk:    pip install vosk")
        else:
            print(f"[transkription] Backend verfuegbar: {backend}")
            if pref:
                print(f"  Bevorzugtes Backend (prefs.json): {pref}")
        return 0

    # --- transcribe ---
    if cmd == "transcribe":
        args = argv[1:]
        dry_run = "--dry-run" in args
        args = [a for a in args if a != "--dry-run"]
        lang = "de"
        if "--lang" in args:
            idx = args.index("--lang")
            if idx + 1 < len(args):
                lang = args[idx + 1]
                args = args[:idx] + args[idx + 2:]
        if not args:
            print("Verwendung: transkription_core.py transcribe <datei> [--lang de] [--dry-run]")
            return 1
        file_path = args[0]
        pref = _read_pref("transkription_backend") if not dry_run else None
        result = transcribe(file_path, store, language=lang, dry_run=dry_run,
                            preferred_backend=pref)
        if "error" in result:
            print(f"[FEHLER] {result['error']}")
            return 1
        print(f"[transkription] ID: {result['id']} | Backend: {result['backend']}")
        if result.get("duration_s"):
            print(f"  Dauer: {result['duration_s']:.1f}s")
        print(f"\n{result['text']}")
        return 0

    # --- list ---
    if cmd == "list":
        args = argv[1:]
        limit = 20
        if "--limit" in args:
            idx = args.index("--limit")
            if idx + 1 < len(args):
                try:
                    limit = int(args[idx + 1])
                except ValueError:
                    pass
        rows = list_transcripts(store, limit)
        if not rows:
            print("[transkription] Keine Transkripte gespeichert.")
            return 0
        print(f"=== Transkripte (letzte {len(rows)}) ===")
        for r in rows:
            print(f"  [{r['id']}] {r['created_at'][:19]} | {r['file_name']} | {r['backend']}")
        return 0

    # --- search ---
    if cmd == "search":
        if len(argv) < 2:
            print("Verwendung: transkription_core.py search <Begriff>")
            return 1
        term = " ".join(argv[1:])
        rows = search_transcripts(store, term)
        if not rows:
            print(f"[transkription] Keine Treffer fuer: {term!r}")
            return 0
        print(f"=== Suche: {term!r} ({len(rows)} Treffer) ===")
        for r in rows:
            snippet = r["text"][:80].replace("\n", " ")
            print(f"  [{r['id']}] {r['file_name']} — {snippet}…")
        return 0

    # --- export ---
    if cmd == "export":
        if len(argv) < 2:
            print("Verwendung: transkription_core.py export <id> [--out datei.txt]")
            return 1
        record_id = argv[1]
        out_path = None
        args = argv[2:]
        if "--out" in args:
            idx = args.index("--out")
            if idx + 1 < len(args):
                out_path = args[idx + 1]
        row = get_transcript(store, record_id)
        if not row:
            print(f"[transkription] Transkript nicht gefunden: {record_id!r}")
            return 1
        if out_path:
            Path(out_path).write_text(row["text"], encoding="utf-8")
            print(f"[transkription] Exportiert: {out_path}")
        else:
            print(row["text"])
        return 0

    print(f"Unbekannter Befehl: {cmd!r}")
    print("Verfuegbar: check, transcribe, list, search, export")
    return 1


if __name__ == "__main__":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.exit(main())
