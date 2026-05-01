#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yt_transcriber.py — YouTube Video Transkript + Metadaten Extraktor

Holt Transkripte (Untertitel) und Metadaten von YouTube-Videos.
Nutzt youtube_transcript_api für Transkripte und yt-dlp für Metadaten.

Usage:
    python yt_transcriber.py <url>
    python yt_transcriber.py <url> --lang de en
    python yt_transcriber.py <url> --format markdown
    python yt_transcriber.py <url> --format json
    python yt_transcriber.py <url> --output transcript.md
    python yt_transcriber.py <url> --meta-only
    python yt_transcriber.py <url> --no-timestamps

Abhängigkeiten:
    - youtube_transcript_api (pip install youtube-transcript-api)
    - yt-dlp (pip install yt-dlp) — optional, für Metadaten

Version: 1.0.0
Autor: Claude (für BACH/Um:bruch)
"""

__version__ = "1.0.0"

import sys
import os
import re
import json
import argparse
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Encoding fix für Windows
os.environ.setdefault("PYTHONIOENCODING", "utf-8")


# --- Video-ID Extraktion (aus BACH youtube_extractor.py) ---

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

    if parsed.netloc in ("youtu.be", "www.youtu.be"):
        vid = parsed.path.lstrip("/").split("/")[0].split("?")[0]
        return vid if re.fullmatch(r"[A-Za-z0-9_-]{11}", vid) else ""

    if parsed.netloc.endswith("youtube.com") or parsed.netloc.endswith("youtube-nocookie.com"):
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

def fetch_transcript(video_id: str, languages: list = None) -> dict:
    """
    Holt Transkript eines YouTube-Videos.

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
                    "full_text": "", "error": "Kein Transkript verfügbar"}

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
        }

    except Exception as e:
        return {"segments": [], "language": "", "is_generated": False,
                "full_text": "", "error": str(e)}


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
        lines.append(f"## Transkript")
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
        description="YouTube Transkript + Metadaten Extraktor",
        epilog="Beispiel: python yt_transcriber.py https://www.youtube.com/watch?v=dQw4w9WgXcQ"
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

    args = parser.parse_args()

    # Video-ID extrahieren
    video_id = extract_video_id(args.url)
    if not video_id:
        sys.stderr.write(f"[FEHLER] Keine gültige YouTube-URL: {args.url}\n")
        sys.exit(1)

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
        if transcript.get("error"):
            sys.stderr.write(f"[WARNUNG] {transcript['error']}\n")
        else:
            n = len(transcript.get("segments", []))
            sys.stderr.write(f"[INFO] {n} Segmente geladen\n")

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


if __name__ == "__main__":
    main()
