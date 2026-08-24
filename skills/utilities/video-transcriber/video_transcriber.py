#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
video_transcriber.py — Video-Transkript + Metadaten Extraktor

Holt Transkripte (Untertitel) und Metadaten von Online-Videos.
Derzeit unterstützt: YouTube (youtube.com, youtu.be, youtube-nocookie.com).
Nutzt youtube_transcript_api für Transkripte und yt-dlp für Metadaten.

Usage:
    python video_transcriber.py <url>
    python video_transcriber.py <url> --lang de en
    python video_transcriber.py <url> --format markdown
    python video_transcriber.py <url> --format json
    python video_transcriber.py <url> --output transcript.md
    python video_transcriber.py <url> --meta-only
    python video_transcriber.py <url> --no-timestamps
    python video_transcriber.py <url> --allow-empty-transcript

Abhängigkeiten:
    - youtube_transcript_api (pip install youtube-transcript-api) — MIT-Lizenz
    - yt-dlp (pip install yt-dlp) — optional, für Metadaten UND als Untertitel-Fallback
      (Unlicense / Public Domain). Der Fallback liest ausschliesslich die
      Untertitelspur aus den Metadaten; es wird kein Video und kein Audio geladen.

Exit-Codes:
    0  Erfolg
    1  Keine gueltige Video-URL
    2  Aufruffehler (von argparse vergeben)
    3  Transkript angefordert, aber keines erhalten
       (mit --allow-empty-transcript stattdessen 0)

DISCLAIMER:
    Dieses Werkzeug ist NICHT mit YouTube oder Google verbunden und wird von diesen
    weder unterstützt noch gebilligt. Die Nutzung erfolgt auf eigene Verantwortung.
    Der Nutzer ist selbst für die Einhaltung der Nutzungsbedingungen der jeweiligen
    Plattform und des geltenden Urheberrechts zuständig. Kein Umgehen von DRM,
    Paywalls oder Zugangsbeschränkungen. Keine massenhafte Datenerhebung (Scraping).
    Keine Weiterveröffentlichung urheberrechtlich geschützter Transkripte ohne
    Zustimmung der Rechteinhaber.

Version: 1.2.0
"""

__version__ = "1.2.0"

import sys
import os
import re
import json
import argparse
import urllib.request
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Exit-Codes. 2 bleibt argparse vorbehalten (Aufruffehler), deshalb 3 fuer den
# fachlichen Fall "kein Transkript" -- sonst waere ein Tippfehler im Aufruf vom
# Video ohne Untertitel nicht unterscheidbar.
EXIT_OK = 0
EXIT_BAD_URL = 1
EXIT_NO_TRANSCRIPT = 3

# Quelle, die das Transkript geliefert hat (landet im JSON-Output).
SOURCE_PRIMARY = "youtube_transcript_api"
SOURCE_YTDLP = "yt-dlp"

# Encoding fix für Windows
os.environ.setdefault("PYTHONIOENCODING", "utf-8")


# --- Video-ID Extraktion (aus BACH youtube_extractor.py) ---

def _host_matches(host: str | None, allowed_domains: set[str]) -> bool:
    if not host:
        return False
    normalized = host.lower().rstrip(".")
    return any(normalized == domain or normalized.endswith(f".{domain}") for domain in allowed_domains)


def extract_video_id(url: str) -> str:
    """Extrahiert YouTube Video-ID aus URL oder direkter ID."""
    if not url:
        return ""
    url = url.strip()

    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url):
        return url

    try:
        parsed = urlparse(url)
    except Exception:
        return ""

    if _host_matches(parsed.hostname, {"youtu.be"}):
        vid = parsed.path.lstrip("/").split("/")[0].split("?")[0]
        return vid if re.fullmatch(r"[A-Za-z0-9_-]{11}", vid) else ""

    if _host_matches(parsed.hostname, {"youtube.com", "youtube-nocookie.com"}):
        if parsed.path == "/watch":
            v = parse_qs(parsed.query).get("v", [""])[0]
            return v if re.fullmatch(r"[A-Za-z0-9_-]{11}", v) else ""
        for prefix in ("/shorts/", "/embed/", "/v/", "/live/"):
            if parsed.path.startswith(prefix):
                vid = parsed.path[len(prefix):].split("/")[0].split("?")[0]
                return vid if re.fullmatch(r"[A-Za-z0-9_-]{11}", vid) else ""

    return ""


# --- Metadaten via yt-dlp ---

def fetch_metadata(video_id: str) -> dict:
    """Holt Video-Metadaten via yt-dlp (kein Download)."""
    try:
        import yt_dlp
    except ImportError:
        return _fetch_metadata_fallback(video_id)

    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title", ""),
                "channel": info.get("channel", info.get("uploader", "")),
                "channel_url": info.get("channel_url", info.get("uploader_url", "")),
                "upload_date": _format_date(info.get("upload_date", "")),
                "duration": info.get("duration", 0),
                "duration_str": _format_duration(info.get("duration", 0)),
                "view_count": info.get("view_count", 0),
                "like_count": info.get("like_count", 0),
                "description": info.get("description", ""),
                "tags": info.get("tags", []),
                "categories": info.get("categories", []),
                "thumbnail": info.get("thumbnail", ""),
                "url": url,
                "video_id": video_id,
            }
    except Exception as e:
        sys.stderr.write(f"[WARNUNG] yt-dlp Fehler: {e}\n")
        return _fetch_metadata_fallback(video_id)


def _fetch_metadata_fallback(video_id: str) -> dict:
    """Fallback: Metadaten via noembed API."""
    try:
        import requests
        url = f"https://noembed.com/embed?url=https://www.youtube.com/watch?v={video_id}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        return {
            "title": data.get("title", ""),
            "channel": data.get("author_name", ""),
            "channel_url": data.get("author_url", ""),
            "upload_date": "",
            "duration": 0,
            "duration_str": "",
            "view_count": 0,
            "like_count": 0,
            "description": "",
            "tags": [],
            "categories": [],
            "thumbnail": data.get("thumbnail_url", ""),
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "video_id": video_id,
        }
    except Exception:
        return {"title": "", "channel": "", "video_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}"}


# --- Transkript via youtube_transcript_api ---

def fetch_transcript_primary(video_id: str, languages: list = None) -> dict:
    """
    Primaerweg: Transkript ueber youtube_transcript_api.

    Kompatibel mit youtube_transcript_api v1.2.x (Instance-API).

    Returns:
        {
            "segments": [{"start": float, "duration": float, "text": str}, ...],
            "language": str,
            "is_generated": bool,
            "full_text": str
        }
    """
    from youtube_transcript_api import YouTubeTranscriptApi

    if languages is None:
        languages = ["de", "en", "de-DE", "en-US"]

    ytt = YouTubeTranscriptApi()

    try:
        # Verfügbare Transkripte auflisten
        transcript_list = ytt.list(video_id)

        # Manuell erstellte Transkripte bevorzugen
        best = None
        for lang in languages:
            for t in transcript_list:
                if t.language_code == lang and not t.is_generated:
                    best = t
                    break
            if best:
                break

        # Fallback: automatisch generiert in bevorzugter Sprache
        if best is None:
            for lang in languages:
                for t in transcript_list:
                    if t.language_code == lang and t.is_generated:
                        best = t
                        break
                if best:
                    break

        # Letzter Fallback: irgendein verfügbares Transkript
        if best is None:
            for t in transcript_list:
                best = t
                break

        if best is None:
            return {"segments": [], "language": "", "is_generated": False,
                    "full_text": "", "error": "Kein Transkript verfügbar", "source": None}

        # Transkript abrufen
        fetched = ytt.fetch(video_id, languages=[best.language_code])

        # Segmente aus FetchedTranscript.snippets extrahieren
        segments = []
        for snippet in fetched.snippets:
            segments.append({
                "start": float(snippet.start),
                "duration": float(snippet.duration),
                "text": snippet.text,
            })

        full_text = " ".join(s["text"] for s in segments)

        return {
            "segments": segments,
            "language": fetched.language_code if hasattr(fetched, "language_code") else best.language_code,
            "is_generated": fetched.is_generated if hasattr(fetched, "is_generated") else best.is_generated,
            "full_text": full_text,
            "source": SOURCE_PRIMARY,
        }

    except Exception as e:
        return {"segments": [], "language": "", "is_generated": False,
                "full_text": "", "error": str(e), "source": None}


# --- Untertitel-Fallback via yt-dlp (kein Video-/Audio-Download) ---

def _base_lang(code: str) -> str:
    """`de-orig`, `de-DE` und `de` haben dieselbe Basissprache `de`."""
    if not code:
        return ""
    return code.split("-")[0].lower()


def _iter_caption_tracks(manual_tracks: dict, automatic_tracks: dict, languages: list):
    """
    Liefert yt-dlp-Untertitelspuren in der gewünschten Priorität.

    Für jede Wunschsprache: manuell exakt/Basis, dann automatisch exakt/Basis.
    Erst danach folgen beliebige Spuren. JSON3 ist erforderlich, weil nur dort
    Zeitmarken und Text strukturiert vorliegen.

    Liefert Tupel aus Sprachcode, Spur und is_generated.
    """
    def json3(eintraege):
        for e in eintraege or []:
            if e.get("ext") == "json3" and e.get("url"):
                return e
        return None

    seen = set()

    def emit(code, spur, generiert):
        if not spur:
            return None
        key = (code, spur["url"], generiert)
        if key in seen:
            return None
        seen.add(key)
        return code, spur, generiert

    for wunsch in languages:
        basis = _base_lang(wunsch)
        for tracks, generiert in ((manual_tracks, False), (automatic_tracks, True)):
            kandidat = emit(wunsch, json3(tracks.get(wunsch)), generiert)
            if kandidat:
                yield kandidat
            for code in sorted(tracks):
                if code != wunsch and _base_lang(code) == basis:
                    kandidat = emit(code, json3(tracks.get(code)), generiert)
                    if kandidat:
                        yield kandidat

    for tracks, generiert in ((manual_tracks, False), (automatic_tracks, True)):
        for code in sorted(tracks):
            kandidat = emit(code, json3(tracks.get(code)), generiert)
            if kandidat:
                yield kandidat


def _pick_caption_track(tracks: dict, languages: list):
    """Waehlt die beste JSON3-Spur aus einer einzelnen Untertitelkarte."""
    for code, spur, _ in _iter_caption_tracks(tracks or {}, {}, languages):
        return code, spur

    return None


def _parse_json3(rohtext: str) -> list:
    """
    Wandelt eine JSON3-Untertitelspur in dieselbe Segmentform wie der Primaerweg.

    Ereignisse ohne `segs` sind Abstandsmarken und werden uebersprungen -- wuerde
    man sie als leere Segmente uebernehmen, entstuende genau der Zustand, den
    dieses Ticket beseitigt: sieht gefuellt aus, ist leer.
    """
    daten = json.loads(rohtext)
    segmente = []
    for ereignis in daten.get("events", []):
        segs = ereignis.get("segs")
        if not segs:
            continue
        text = "".join(s.get("utf8", "") for s in segs).strip()
        if not text:
            continue
        segmente.append({
            "start": float(ereignis.get("tStartMs", 0)) / 1000.0,
            "duration": float(ereignis.get("dDurationMs", 0)) / 1000.0,
            "text": text,
        })
    return segmente


def _http_get_text(url: str) -> str:
    """Laedt eine Untertitel-URL als Text. Stdlib, damit keine neue Abhaengigkeit."""
    anfrage = urllib.request.Request(
        url, headers={"User-Agent": f"video-transcriber/{__version__}"})
    with urllib.request.urlopen(anfrage, timeout=30) as antwort:
        return antwort.read().decode("utf-8", errors="replace")


def fetch_transcript_ytdlp(video_id: str, languages: list = None) -> dict:
    """
    Fallback: Untertitel ueber die yt-dlp-Metadaten.

    Benutzt ausschliesslich `extract_info(download=False)` und liest daraus die
    Untertitel-URL. Bewusst NICHT `writesubtitles`/`writeautomaticsub`: die
    schreiben Dateien und ziehen die Download-Maschinerie mit hinein. Kein Video,
    kein Audio, kein Umgehen von Zugangsbeschraenkungen -- nur die Spur, die die
    Plattform ohnehin zur Wiedergabe ausliefert.
    """
    if languages is None:
        languages = ["de", "en"]

    try:
        import yt_dlp
    except ImportError:
        return {"segments": [], "language": "", "is_generated": False, "full_text": "",
                "error": "yt-dlp nicht installiert (Fallback nicht verfügbar)", "source": None}

    url = f"https://www.youtube.com/watch?v={video_id}"
    opts = {"quiet": True, "no_warnings": True, "skip_download": True}

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as e:
        return {"segments": [], "language": "", "is_generated": False, "full_text": "",
                "error": f"yt-dlp Fehler: {e}", "source": None}

    info = info or {}
    fehlschlaege = []
    for code, spur, generiert in _iter_caption_tracks(
            info.get("subtitles") or {}, info.get("automatic_captions") or {}, languages):
        try:
            segmente = _parse_json3(_http_get_text(spur["url"]))
        except Exception as e:
            fehlschlaege.append(f"{code}: {e}")
            continue
        if not segmente:
            fehlschlaege.append(f"{code}: keine Segmente")
            continue
        return {
            "segments": segmente,
            "language": code,
            "is_generated": generiert,
            "full_text": " ".join(s["text"] for s in segmente),
            "source": SOURCE_YTDLP,
        }

    fehler = "Keine verwertbare Untertitelspur (JSON3) gefunden"
    if fehlschlaege:
        fehler += f": {'; '.join(fehlschlaege)}"
    return {"segments": [], "language": "", "is_generated": False, "full_text": "",
            "error": fehler, "source": None}


def fetch_transcript(video_id: str, languages: list = None) -> dict:
    """
    Holt das Transkript: erst der Primaerweg, bei leerem Ergebnis der yt-dlp-Fallback.

    Der Fallback greift nicht nur bei einer Ausnahme, sondern immer dann, wenn der
    Primaerweg KEINE Segmente liefert. Genau dieser Fall -- Ausnahme gefangen,
    leeres Ergebnis zurueckgegeben -- war der stille Fehlschlag.
    """
    primaer = fetch_transcript_primary(video_id, languages)
    if primaer.get("segments"):
        primaer.setdefault("source", SOURCE_PRIMARY)
        return primaer

    ersatz = fetch_transcript_ytdlp(video_id, languages)
    if ersatz.get("segments"):
        return ersatz

    # Beide leer: beide Befunde behalten, damit die Ursache sichtbar bleibt.
    fehler = " | ".join(f for f in (primaer.get("error"), ersatz.get("error")) if f)
    return {"segments": [], "language": "", "is_generated": False, "full_text": "",
            "error": fehler or "Kein Transkript verfügbar", "source": None}


# --- Formatierung ---

def _format_timestamp(seconds: float) -> str:
    """Sekunden -> HH:MM:SS oder MM:SS."""
    s = int(seconds)
    h, remainder = divmod(s, 3600)
    m, sec = divmod(remainder, 60)
    if h > 0:
        return f"{h}:{m:02d}:{sec:02d}"
    return f"{m}:{sec:02d}"


def _format_date(date_str: str) -> str:
    """YYYYMMDD -> YYYY-MM-DD."""
    if date_str and len(date_str) == 8:
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    return date_str


def _format_duration(seconds: int) -> str:
    """Sekunden -> menschenlesbar."""
    if not seconds:
        return ""
    h, remainder = divmod(seconds, 3600)
    m, s = divmod(remainder, 60)
    parts = []
    if h:
        parts.append(f"{h}h")
    if m:
        parts.append(f"{m}min")
    if s and not h:
        parts.append(f"{s}s")
    return " ".join(parts)


def format_markdown(meta: dict, transcript: dict, timestamps: bool = True) -> str:
    """Formatiert Metadaten + Transkript als Markdown."""
    lines = []

    # Header
    title = meta.get("title", "YouTube Video")
    lines.append(f"# {title}")
    lines.append("")

    # Metadaten
    lines.append("## Metadaten")
    lines.append("")
    if meta.get("channel"):
        ch = meta["channel"]
        if meta.get("channel_url"):
            ch = f"[{ch}]({meta['channel_url']})"
        lines.append(f"- **Kanal:** {ch}")
    if meta.get("upload_date"):
        lines.append(f"- **Veröffentlicht:** {meta['upload_date']}")
    if meta.get("duration_str"):
        lines.append(f"- **Dauer:** {meta['duration_str']}")
    if meta.get("view_count"):
        lines.append(f"- **Aufrufe:** {meta['view_count']:,}".replace(",", "."))
    lines.append(f"- **URL:** {meta.get('url', '')}")

    lang_info = transcript.get("language", "")
    if transcript.get("is_generated"):
        lang_info += " (automatisch generiert)"
    if lang_info:
        lines.append(f"- **Transkript-Sprache:** {lang_info}")
    lines.append("")

    # Beschreibung (gekürzt)
    desc = meta.get("description", "")
    if desc:
        lines.append("## Beschreibung")
        lines.append("")
        # Maximal 500 Zeichen
        if len(desc) > 500:
            lines.append(desc[:500] + "...")
        else:
            lines.append(desc)
        lines.append("")

    # Transkript
    if transcript.get("error"):
        lines.append("## Transkript")
        lines.append("")
        lines.append(f"**Fehler:** {transcript['error']}")
    elif transcript.get("segments"):
        lines.append("## Transkript")
        lines.append("")
        for seg in transcript["segments"]:
            if timestamps:
                ts = _format_timestamp(seg["start"])
                lines.append(f"**[{ts}]** {seg['text']}")
            else:
                lines.append(seg["text"])
        lines.append("")

    return "\n".join(lines)


def format_json(meta: dict, transcript: dict) -> str:
    """Formatiert als JSON."""
    return json.dumps({"metadata": meta, "transcript": transcript},
                      indent=2, ensure_ascii=False)


def format_plain(meta: dict, transcript: dict, timestamps: bool = True) -> str:
    """Formatiert als Plaintext."""
    lines = []
    title = meta.get("title", "")
    if title:
        lines.append(title)
        lines.append("=" * len(title))
        lines.append("")
    if meta.get("channel"):
        lines.append(f"Kanal: {meta['channel']}")
    if meta.get("upload_date"):
        lines.append(f"Datum: {meta['upload_date']}")
    lines.append(f"URL: {meta.get('url', '')}")
    lines.append("")
    lines.append("--- Transkript ---")
    lines.append("")

    if transcript.get("error"):
        lines.append(f"FEHLER: {transcript['error']}")
    elif transcript.get("segments"):
        for seg in transcript["segments"]:
            if timestamps:
                ts = _format_timestamp(seg["start"])
                lines.append(f"[{ts}] {seg['text']}")
            else:
                lines.append(seg["text"])

    return "\n".join(lines)


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(
        description="Video-Transkript + Metadaten Extraktor (unterstützt YouTube-Quellen)",
        epilog="Beispiel: python video_transcriber.py https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )
    parser.add_argument("url", help="YouTube URL oder Video-ID")
    parser.add_argument("--lang", nargs="+", default=["de", "en"],
                        help="Bevorzugte Sprachen (Standard: de en)")
    parser.add_argument("--format", choices=["markdown", "json", "plain"],
                        default="markdown", help="Ausgabeformat (Standard: markdown)")
    parser.add_argument("--output", "-o", help="Ausgabedatei (sonst stdout)")
    parser.add_argument("--meta-only", action="store_true",
                        help="Nur Metadaten, kein Transkript")
    parser.add_argument("--transcript-only", action="store_true",
                        help="Nur Transkript, keine Metadaten")
    parser.add_argument("--no-timestamps", action="store_true",
                        help="Transkript ohne Zeitstempel")
    parser.add_argument("--no-meta", action="store_true",
                        help="Metadaten-Abruf überspringen (schneller)")
    parser.add_argument("--allow-empty-transcript", action="store_true",
                        help="Leeres Transkript als Erfolg werten (Exit 0 statt 3)")

    args = parser.parse_args()

    # Video-ID extrahieren
    video_id = extract_video_id(args.url)
    if not video_id:
        sys.stderr.write(f"[FEHLER] Keine gültige YouTube-URL: {args.url}\n")
        sys.exit(EXIT_BAD_URL)

    sys.stderr.write(f"[INFO] Video-ID: {video_id}\n")

    # Metadaten holen
    meta = {}
    if not args.transcript_only and not args.no_meta:
        sys.stderr.write("[INFO] Hole Metadaten...\n")
        meta = fetch_metadata(video_id)
        if meta.get("title"):
            sys.stderr.write(f"[INFO] Titel: {meta['title']}\n")

    # Transkript holen
    transcript = {"segments": [], "full_text": ""}
    if not args.meta_only:
        sys.stderr.write("[INFO] Hole Transkript...\n")
        transcript = fetch_transcript(video_id, args.lang)
        if transcript.get("segments"):
            n = len(transcript["segments"])
            quelle = transcript.get("source") or "unbekannt"
            sys.stderr.write(f"[INFO] {n} Segmente geladen (Quelle: {quelle})\n")
            if transcript.get("error"):
                sys.stderr.write(f"[HINWEIS] Primaerweg meldete: {transcript['error']}\n")
        else:
            sys.stderr.write(f"[FEHLER] Kein Transkript: {transcript.get('error', 'unbekannt')}\n")

    # Formatieren
    timestamps = not args.no_timestamps
    if args.format == "json":
        output = format_json(meta, transcript)
    elif args.format == "plain":
        output = format_plain(meta, transcript, timestamps)
    else:
        output = format_markdown(meta, transcript, timestamps)

    # Ausgabe
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        sys.stderr.write(f"[OK] Geschrieben: {args.output}\n")
    else:
        print(output)

    # Exit-Semantik: Ein leeres Transkript ist KEIN Erfolg. Vorher lief dieser
    # Fall mit Exit 0 durch -- die Ausgabe wurde geschrieben, das Segmentarray
    # war leer, und jeder aufrufende Automat hielt das fuer gelungen.
    # Wer nur Metadaten wollte, scheitert nicht am fehlenden Transkript.
    transkript_gewuenscht = not args.meta_only
    if transkript_gewuenscht and not transcript.get("segments"):
        if args.allow_empty_transcript:
            sys.stderr.write("[HINWEIS] Leeres Transkript wird auf Wunsch als Erfolg gewertet.\n")
            sys.exit(EXIT_OK)
        sys.stderr.write(
            f"[FEHLER] Kein Transkript erhalten -- Exit {EXIT_NO_TRANSCRIPT}. "
            f"Mit --allow-empty-transcript als Erfolg werten.\n")
        sys.exit(EXIT_NO_TRANSCRIPT)

    sys.exit(EXIT_OK)


if __name__ == "__main__":
    main()
