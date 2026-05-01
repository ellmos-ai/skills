# yt-transcriber

YouTube Video Transkript + Metadaten Extraktor.

## Features

- Transkript (Untertitel) von YouTube-Videos abrufen
- Metadaten (Titel, Kanal, Datum, Views, Beschreibung)
- Bevorzugt manuell erstellte Untertitel, Fallback auf automatisch generierte
- Ausgabe als Markdown, JSON oder Plaintext
- Zeitstempel optional

## Abhängigkeiten

```bash
pip install youtube-transcript-api  # Transkripte
pip install yt-dlp                  # Metadaten (optional, Fallback auf noembed)
```

## Usage

```bash
# Standard: Markdown mit Timestamps
python yt_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Bestimmte Sprachen bevorzugen
python yt_transcriber.py URL --lang de en fr

# JSON-Output
python yt_transcriber.py URL --format json

# In Datei speichern
python yt_transcriber.py URL -o transcript.md

# Nur Metadaten (kein Transkript)
python yt_transcriber.py URL --meta-only

# Ohne Zeitstempel
python yt_transcriber.py URL --no-timestamps

# Schneller (ohne yt-dlp Metadaten)
python yt_transcriber.py URL --no-meta
```

## Python-API

```python
from yt_transcriber import extract_video_id, fetch_metadata, fetch_transcript, format_markdown

video_id = extract_video_id("https://www.youtube.com/watch?v=VNq-PfnzVUM")
meta = fetch_metadata(video_id)
transcript = fetch_transcript(video_id, languages=["de", "en"])
output = format_markdown(meta, transcript)
```

## Integration

- **Um:bruch:** Recherche-Tool für KI-Reviews und Leitartikel
- **BACH:** Ergänzt den Transkriptions-Service (Audio→Text) um YouTube→Text
- **.RESEARCH:** Quellenerschließung für Metaphern- und Argumentationsanalysen
