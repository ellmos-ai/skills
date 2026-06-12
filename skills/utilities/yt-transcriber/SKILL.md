---
name: yt-transcriber
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-04-04
updated: 2026-06-12
description: >
  YouTube-Transkripte (Untertitel) und Video-Metadaten abrufen und als
  Markdown, JSON oder Plaintext ausgeben. Bevorzugt manuelle Untertitel,
  Fallback auf automatisch generierte.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true

category: utilities
tags: [youtube, transkript, untertitel, metadaten, recherche, video]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: [youtube-transcript-api, yt-dlp]

provenance:
  origin: "bach"
  origin_path: "system/tools/youtube_extractor.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-04-04"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# YouTube-Transkriber

Holt Transkripte (Untertitel) und Metadaten (Titel, Kanal, Datum, Views,
Beschreibung) von YouTube-Videos. Bevorzugt manuell erstellte Untertitel,
Fallback auf automatisch generierte. Ausgabe als Markdown, JSON oder Plaintext.

Bei YouTube-Videos dieses Tool nutzen statt Inhalte manuell zusammenzufassen —
das Transkript ist die verlässliche Quelle.

## Abhängigkeiten

```bash
pip install youtube-transcript-api   # Transkripte (Pflicht)
pip install yt-dlp                   # Metadaten (optional, Fallback: noembed)
```

## Nutzung

> **Windows-Hinweis:** Immer `PYTHONIOENCODING=utf-8` setzen, sonst brechen
> Umlaute und Sonderzeichen in der Ausgabe (cp1252-Encoding).

```bash
# Standard: Markdown mit Timestamps
PYTHONIOENCODING=utf-8 python yt_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Ausgabeformat waehlen
PYTHONIOENCODING=utf-8 python yt_transcriber.py URL --format markdown|json|plain

# In Datei speichern
PYTHONIOENCODING=utf-8 python yt_transcriber.py URL -o transcript.md

# Sprachen bevorzugen (Default: de en)
PYTHONIOENCODING=utf-8 python yt_transcriber.py URL --lang de en fr
```

### Optionen

| Option | Wirkung |
|--------|---------|
| `--format markdown\|json\|plain` | Ausgabeformat (Default: markdown) |
| `--output, -o <datei>` | In Datei schreiben statt stdout |
| `--lang <codes...>` | Bevorzugte Untertitel-Sprachen (Default: de en) |
| `--meta-only` | Nur Metadaten, kein Transkript |
| `--transcript-only` | Nur Transkript, keine Metadaten |
| `--no-timestamps` | Transkript ohne Zeitstempel |
| `--no-meta` | Schneller: yt-dlp-Metadaten überspringen |

### Als Python-Library

```python
from yt_transcriber import extract_video_id, fetch_metadata, fetch_transcript, format_markdown

video_id = extract_video_id("https://www.youtube.com/watch?v=VIDEO_ID")
meta = fetch_metadata(video_id)
transcript = fetch_transcript(video_id, languages=["de", "en"])
output = format_markdown(meta, transcript)
```

## Typische Einsatzfälle

- Recherche: Videoinhalte zitierfähig als Text erschließen
- Quellenanalyse: Argumentation/Metaphern in Vorträgen untersuchen
- Zusammenfassungen: Transkript als verlässliche Grundlage statt Halluzination

## Grenzen

- Funktioniert nur, wenn das Video Untertitel hat (manuell oder automatisch)
- Automatische Untertitel können Erkennungsfehler enthalten
- Kein Audio-Download, keine eigene Spracherkennung

## Changelog

### 1.0.0 (2026-06-12)
- SKILL.md ergänzt (Tool existierte bereits als Script + README)
- Script v1.0.0: Transkript + Metadaten, 3 Ausgabeformate, Sprachpräferenzen
