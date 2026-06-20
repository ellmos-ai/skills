# video-transcriber

Video-Transkript + Metadaten Extraktor (unterstützt YouTube-Quellen).

> Dieses Werkzeug ist nicht mit YouTube oder Google verbunden und wird von diesen
> weder unterstützt noch gebilligt. Die Nutzung erfolgt auf eigene Verantwortung
> gemäß den Nutzungsbedingungen der jeweiligen Plattform und dem geltenden
> Urheberrecht. Kein DRM-/Paywall-Umgehen, kein Massen-Scraping.

## Features

- Transkript (Untertitel) von Videos abrufen — derzeit unterstützt: YouTube
- Metadaten (Titel, Kanal, Datum, Views, Beschreibung)
- Bevorzugt manuell erstellte Untertitel, Fallback auf automatisch generierte
- Ausgabe als Markdown, JSON oder Plaintext
- Zeitstempel optional

## Abhängigkeiten und Lizenzen

```bash
pip install youtube-transcript-api  # Transkripte — MIT-Lizenz
pip install yt-dlp                  # Metadaten (optional, Fallback auf noembed) — Unlicense
```

## Usage

```bash
# Standard: Markdown mit Timestamps
python video_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Bestimmte Sprachen bevorzugen
python video_transcriber.py URL --lang de en fr

# JSON-Output
python video_transcriber.py URL --format json

# In Datei speichern
python video_transcriber.py URL -o transcript.md

# Nur Metadaten (kein Transkript)
python video_transcriber.py URL --meta-only

# Ohne Zeitstempel
python video_transcriber.py URL --no-timestamps

# Schneller (ohne yt-dlp Metadaten)
python video_transcriber.py URL --no-meta
```

## Python-API

```python
from video_transcriber import extract_video_id, fetch_metadata, fetch_transcript, format_markdown

video_id = extract_video_id("https://www.youtube.com/watch?v=VNq-PfnzVUM")
meta = fetch_metadata(video_id)
transcript = fetch_transcript(video_id, languages=["de", "en"])
output = format_markdown(meta, transcript)
```

## Integration

- **Um:bruch:** Recherche-Tool für KI-Reviews und Leitartikel
- **BACH:** Ergänzt den Transkriptions-Service (Audio→Text) um Video→Text
- **.RESEARCH:** Quellenerschließung für Metaphern- und Argumentationsanalysen
