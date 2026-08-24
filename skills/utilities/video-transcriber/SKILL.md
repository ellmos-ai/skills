---
name: video-transcriber
version: 1.2.0
type: tool
author: Lukas Geiger
created: 2026-04-04
updated: 2026-08-24
description: Fetch video transcripts (subtitles) and metadata from online video sources and output them as Markdown, JSON, or plain text. Currently supported: YouTube. Prefers manually created subtitles, falls back to auto-generated ones.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [video, transcript, subtitles, metadata, research, youtube]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['youtube-transcript-api', 'yt-dlp']}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/youtube_extractor.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-04-04', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="video-transcriber banner">

# Video-Transkriber

Holt Transkripte (Untertitel) und Metadaten (Titel, Kanal, Datum, Views,
Beschreibung) von Online-Videos. Bevorzugt manuell erstellte Untertitel,
Fallback auf automatisch generierte. Ausgabe als Markdown, JSON oder Plaintext.

Liefert der Primärweg (`youtube-transcript-api`) nichts, greift automatisch ein
zweiter Weg über die yt-dlp-Metadaten. Er liest ausschließlich die
Untertitelspur, die die Plattform ohnehin zur Wiedergabe ausliefert — **kein
Video- oder Audio-Download**. Welcher Weg gegriffen hat, steht im Feld `source`
der JSON-Ausgabe und auf stderr.

Für jede gewünschte Sprache priorisiert der Fallback manuelle exakte und
Basis-Spuren vor automatischen exakten und Basis-Spuren; beliebige Spuren folgen
erst danach. Eine nicht lesbare JSON3-Spur beendet den Abruf nicht, solange noch
eine weitere Kandidatin verfügbar ist.

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
| `--allow-empty-transcript` | Leeres Transkript als Erfolg werten (Exit 0 statt 3) |

### Exit-Codes

Ein leeres Transkript ist **kein** Erfolg. Vor 1.2.0 endete dieser Fall mit
Exit 0: die Ausgabedatei wurde geschrieben, das Segment-Array war leer, und
jeder aufrufende Automat hielt das für gelungen. Dieser stille Fehlschlag ist
der eigentliche Defekt, den 1.2.0 beseitigt.

| Code | Bedeutung |
|------|-----------|
| `0` | Erfolg — Transkript vorhanden, oder `--meta-only`, oder `--allow-empty-transcript` |
| `1` | Keine gültige Video-URL/-ID |
| `2` | Aufruffehler (von argparse vergeben, z. B. unbekannte Option) |
| `3` | Kein Transkript erhalten — beide Wege leer |

`2` bleibt argparse vorbehalten, damit ein Tippfehler im Aufruf vom Video ohne
Untertitel unterscheidbar bleibt.

```bash
# In Skripten
PYTHONIOENCODING=utf-8 python video_transcriber.py URL -o out.md || {
  code=$?
  [ "$code" -eq 3 ] && echo "Video hat keine Untertitel" || echo "Fehler: $code"
}
```

### Als Python-Library

```python
from video_transcriber import extract_video_id, fetch_metadata, fetch_transcript, format_markdown

video_id = extract_video_id("https://www.youtube.com/watch?v=VIDEO_ID")
meta = fetch_metadata(video_id)
transcript = fetch_transcript(video_id, languages=["de", "en"])
output = format_markdown(meta, transcript)

# Immer pruefen -- fetch_transcript wirft nicht, es meldet:
if not transcript["segments"]:
    raise RuntimeError(transcript["error"])
print(transcript["source"])  # "youtube_transcript_api" oder "yt-dlp"
```

Beide Wege sind einzeln aufrufbar: `fetch_transcript_primary()` (nur
`youtube-transcript-api`) und `fetch_transcript_ytdlp()` (nur der Ersatzweg).
`fetch_transcript()` verkettet sie und garantiert die Felder `segments`,
`language`, `is_generated`, `full_text`, `source` und im Fehlerfall `error`.

## Typische Einsatzfälle

- Recherche: Videoinhalte zitierfähig als Text erschließen
- Quellenanalyse: Argumentation/Metaphern in Vorträgen untersuchen
- Zusammenfassungen: Transkript als verlässliche Grundlage statt Halluzination

## Grenzen

- Funktioniert nur, wenn das Video Untertitel hat (manuell oder automatisch)
- Automatische Untertitel können Erkennungsfehler enthalten
- Kein Audio-Download, keine eigene Spracherkennung — auch der Ersatzweg lädt
  nur die Untertitelspur, nie Video oder Audio
- Der Ersatzweg braucht eine JSON3-Spur; liefert die Plattform nur andere
  Formate, endet der Lauf mit Exit 3 statt mit einer Teilausgabe

## Changelog

### 1.2.0 (2026-08-24)
- **Exit-Semantik:** Leeres Transkript endet mit Exit `3` statt stillschweigend
  mit `0`. Ungültige URL nun `1` als benannte Konstante. `--meta-only` bleibt
  erfolgreich, weil dort kein Transkript erwartet wird.
- **Neue Option `--allow-empty-transcript`:** wertet ein leeres Transkript
  bewusst als Erfolg — für Aufrufer, die Untertitel als optional behandeln.
- **yt-dlp-Untertitel-Fallback:** greift, sobald der Primärweg keine Segmente
  liefert (nicht erst bei einer Ausnahme). Nutzt `extract_info(download=False)`
  und liest nur die Untertitel-URL — kein Video, kein Audio, kein Umgehen von
  Zugangsbeschränkungen.
- **Sprachwahl gehärtet:** `de-orig`/`de-DE` werden für `--lang de` gefunden
  (Basissprachen-Abgleich). Manuelle Untertitel weiterhin vor automatischen.
- **Feld `source`** im Ergebnis: `youtube_transcript_api` oder `yt-dlp`.
- Regressionstests: 29 Tests mit gemockten Antworten (UTF-8, alle drei
  Ausgabeformate, Exit-Codes, Sprachwahl, JSON3-Parsing).

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
