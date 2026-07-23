---
name: transkription
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: >
  Transcribes audio/video files to text. Uses Whisper (openai-whisper)
  or Vosk (offline) as optional backend — both are detected via presence check.
  Without backend: placeholder mode with dummy output (dry-run).
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags:
  - transkription
  - audio
  - speech-to-text
  - whisper
  - vosk
  - offline
language: en
status: stable

dependencies:
  tools: []
  services: []
  protocols: []
  python:
    - name: openai-whisper
      optional: true
      install: "pip install openai-whisper"
      purpose: "STT backend option 1 (cloud/local model)"
    - name: vosk
      optional: true
      install: "pip install vosk"
      purpose: "STT backend option 2 (fully offline)"

provenance:
  origin: eigenentwurf
  origin_path: ""
  origin_version: ""
  origin_repo: ""
  origin_license: MIT
  last_sync_from_origin: ""
  notes: >
    Kein direkter BACH-Origin vorhanden (transkriptions-service existiert nicht
    als Datei in BACH/system). Skill neu konzipiert. voice_stt.py aus
    BACH/hub/_services/voice/ hat das Backend-Muster inspiriert (optionale
    Imports mit Verfügbarkeits-Flags), wurde aber nicht direkt portiert.
---

## Purpose

Convert audio/video files to text — locally, without mandatory cloud access. The skill
automatically detects whether Whisper or Vosk is installed and selects the best
available backend. Without a backend it runs in dry-run mode and returns a
placeholder text, so the workflow always works.

Transcripts are stored locally in `transkription/store.db` and can be queried.

---

## Triggers

| Phrase | Action |
|---|---|
| "Transcribe this audio" | Transcribe audio file |
| "Transcribe [file]" | Transcribe named file |
| "Show my transcripts" | List latest transcripts |
| "Search transcript [term]" | Full-text search in transcripts |
| "Export transcript [ID]" | Export transcript as TXT |

---

## Workflow

1. **Backend check**: Check whether `whisper` or `vosk` is importable.
2. **File check**: Input file must exist (audio: wav, mp3, m4a, ogg, flac; video: mp4, mkv, webm — extraction via ffmpeg).
3. **Transcription**: Call backend and obtain raw text.
4. **Save**: Store result with metadata (file, duration, language, backend, timestamp) in `store.db`.
5. **Output**: Return text; optionally export as `.txt`.

---

## CLI Entry Point

```bash
# Transcribe file
python transkription_core.py transcribe audio.wav

# With explicit language
python transkription_core.py transcribe audio.mp3 --lang de

# Dry-run (no backend required)
python transkription_core.py transcribe audio.wav --dry-run

# List transcripts
python transkription_core.py list [--limit 20]

# Full-text search
python transkription_core.py search "term"

# Export
python transkription_core.py export <id> [--out file.txt]

# Backend check
python transkription_core.py check

# Alternative store path (e.g. for tests)
python transkription_core.py --store /tmp/test.db transcribe audio.wav --dry-run
```

---

## Store

| Property | Value |
|---|---|
| Type | SQLite |
| Path (default) | `skills/assist/transkription/store.db` |
| Override | `--store <path>` or env `TRANSKRIPTION_STORE` |
| Tables | `transcripts` |

### Schema `transcripts`

```sql
CREATE TABLE IF NOT EXISTS transcripts (
    id          TEXT PRIMARY KEY,  -- UUID (short: 8 hex)
    file_path   TEXT NOT NULL,     -- original path of audio file
    file_name   TEXT NOT NULL,     -- filename (without path, for display)
    text        TEXT NOT NULL,     -- transcribed text
    language    TEXT,              -- language (e.g. "de", "en")
    backend     TEXT,              -- "whisper" | "vosk" | "dry-run"
    duration_s  REAL,              -- duration in seconds (if known)
    created_at  TEXT NOT NULL,     -- ISO-8601 timestamp
    tags        TEXT               -- comma-separated tags (optional)
);
```

---

## Attitude

- Without an installed backend the skill works in dry-run mode (demo text).
- Whisper is preferred over Vosk (better German quality).
- The choice between Whisper and Vosk can be set via `assist/prefs.json` (`transkription_backend: "whisper"|"vosk"|"auto"`).
- ffmpeg for video extraction is needed separately and is not included in the skill.

---

## Privacy

- **All transcripts stay local** — no cloud transfer without Whisper online mode.
- Whisper can be used locally (tiny/base/medium model) or via OpenAI API.
  By default the local model is used.
- `store.db` may contain sensitive conversation content — **do not commit to Git**.
- Recommendation: add `store.db` to `.gitignore`.

---

## Related Resources

- BACH `hub/_services/voice/voice_stt.py` — backend pattern (inspiration, read-only)
- Skill `utilities/yt-transcriber` — YouTube transcription (separate skill, not a duplicate: YT-specific)
- `tools/module-installer/module_installer.py` — registry contains whisper + vosk

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-06-22 | Initial creation — own SQLite store, Whisper/Vosk presence check |
