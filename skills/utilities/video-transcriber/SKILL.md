---
name: video-transcriber
version: 1.1.0
type: tool
author: Lukas Geiger
created: 2026-04-04
updated: 2026-06-20
description: >
  Video-Transkripte (Untertitel) und Metadaten von Online-Videos abrufen und als
  Markdown, JSON oder Plaintext ausgeben. Derzeit unterstützte Quellen: YouTube.
  Bevorzugt manuelle Untertitel, Fallback auf automatisch generierte.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true

category: utilities
tags: [video, transkript, untertitel, metadaten, recherche, youtube]
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
  local_changes_since_sync: true
---

# Video-Transkriber

Holt Transkripte (Untertitel) und Metadaten (Titel, Kanal, Datum, Views,
Beschreibung) von Online-Videos. Bevorzugt manuell erstellte Untertitel,
Fallback auf automatisch generierte. Ausgabe als Markdown, JSON oder Plaintext.

Derzeit unterstützte Quelle: **YouTube** (youtube.com, youtu.be, youtube-nocookie.com).

Bei Videos dieses Tool nutzen statt Inhalte manuell zusammenzufassen —
das Transkript ist die verlässliche Quelle.

> **Hinweis:** Dieses Werkzeug ist nicht mit YouTube oder Google verbunden und
> wird von diesen weder unterstützt noch gebilligt. Die Nutzung erfolgt auf
> eigene Verantwortung. Nutzer sind für die Einhaltung der Nutzungsbedingungen
> der jeweiligen Plattform und des geltenden Urheberrechts selbst zuständig.
> Kein Umgehen von DRM, Paywalls oder Zugangsbeschränkungen; keine massenhafte
> Datenerhebung; keine Weiterveröffentlichung geschützter Transkripte ohne
> Zustimmung der Rechteinhaber.

## Abhängigkeiten und Lizenzen

```bash
pip install youtube-transcript-api   # Transkripte (Pflicht) — MIT-Lizenz
pip install yt-dlp                   # Metadaten (optional, Fallback: noembed) — Unlicense (Public Domain)
```

## Nutzung

> **Windows-Hinweis:** Immer `PYTHONIOENCODING=utf-8` setzen, sonst brechen
> Umlaute und Sonderzeichen in der Ausgabe (cp1252-Encoding).

```bash
# Standard: Markdown mit Timestamps
PYTHONIOENCODING=utf-8 python video_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Ausgabeformat waehlen
PYTHONIOENCODING=utf-8 python video_transcriber.py URL --format markdown|json|plain

# In Datei speichern
PYTHONIOENCODING=utf-8 python video_transcriber.py URL -o transcript.md

# Sprachen bevorzugen (Default: de en)
PYTHONIOENCODING=utf-8 python video_transcriber.py URL --lang de en fr
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
from video_transcriber import extract_video_id, fetch_metadata, fetch_transcript, format_markdown

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

### 1.1.0 (2026-06-20)
- Umbenannt von `yt-transcriber` → `video-transcriber` (YouTube-Markenrichtlinie:
  „yt" ist eine explizit verbotene Abkürzung; Empfehlung: RECHTSCHECK_2026-06-20.md)
- Script: `yt_transcriber.py` → `video_transcriber.py`
- Disclaimer + Dependency-Lizenzen ergänzt (Nutzerverantwortung, ToS, kein Endorsement)
- YouTube nur noch als beschreibende Quellangabe, nicht als Namens-/Markenbestandteil
- Backward-Compat-Wrapper `yt_transcriber.py` am alten Pfad belassen

### 1.0.0 (2026-06-12)
- SKILL.md ergänzt (Tool existierte bereits als Script + README)
- Script v1.0.0: Transkript + Metadaten, 3 Ausgabeformate, Sprachpräferenzen
