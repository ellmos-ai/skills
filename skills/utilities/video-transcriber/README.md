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
- Zweiter Abrufweg über yt-dlp, wenn der Primärweg nichts liefert — liest nur
  die Untertitelspur, **kein Video-/Audio-Download**
- Ausgabe als Markdown, JSON oder Plaintext
- Zeitstempel optional
- Aussagekräftige Exit-Codes: leeres Transkript endet mit `3`, nicht mit `0`

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

# Leeres Transkript bewusst als Erfolg werten (Exit 0 statt 3)
python video_transcriber.py URL --allow-empty-transcript
```

## Exit-Codes

| Code | Bedeutung |
|------|-----------|
| `0` | Erfolg — Transkript vorhanden, oder `--meta-only`, oder `--allow-empty-transcript` |
| `1` | Keine gültige Video-URL/-ID |
| `2` | Aufruffehler (argparse) |
| `3` | Kein Transkript erhalten — beide Abrufwege leer |

Ein leeres Transkript ist kein Erfolg: vor v1.2.0 wurde die Ausgabedatei mit
leerem Segment-Array geschrieben und der Lauf endete mit `0` — aufrufende
Skripte hielten das für gelungen.

## Python-API

```python
from video_transcriber import extract_video_id, fetch_metadata, fetch_transcript, format_markdown

video_id = extract_video_id("https://www.youtube.com/watch?v=VNq-PfnzVUM")
meta = fetch_metadata(video_id)
transcript = fetch_transcript(video_id, languages=["de", "en"])
output = format_markdown(meta, transcript)

if not transcript["segments"]:
    raise RuntimeError(transcript["error"])
print(transcript["source"])  # "youtube_transcript_api" oder "yt-dlp"
```

Einzelne Wege: `fetch_transcript_primary()` und `fetch_transcript_ytdlp()`.

## Integration

- **Um:bruch:** Recherche-Tool für KI-Reviews und Leitartikel
- **BACH:** Ergänzt den Transkriptions-Service (Audio→Text) um Video→Text
- **.RESEARCH:** Quellenerschließung für Metaphern- und Argumentationsanalysen
