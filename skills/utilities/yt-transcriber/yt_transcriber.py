#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yt_transcriber.py — Backward-Compatibility Wrapper

DEPRECATED: Dieses Script wurde umbenannt.
Bitte verwende stattdessen:
    skills/utilities/video-transcriber/video_transcriber.py

Grund: YouTube-Markenrichtlinie — „yt" ist eine explizit verbotene Abkürzung
des Markennamens „YouTube" (YouTube API Services Branding Guidelines).
Empfehlung: RECHTSCHECK_2026-06-20.md

Dieses Wrapper-Script leitet alle Aufrufe transparent an das neue Modul weiter.
"""

import sys
import os
import warnings

# Wrapper-Warnung ausgeben
warnings.warn(
    "yt_transcriber ist veraltet. Bitte nutze stattdessen video_transcriber "
    "aus skills/utilities/video-transcriber/video_transcriber.py",
    DeprecationWarning,
    stacklevel=2,
)
sys.stderr.write(
    "[DEPRECATED] yt_transcriber.py ist ein Compat-Wrapper. "
    "Bitte zu video_transcriber.py wechseln.\n"
)

# Neues Modul auf den Suchpfad legen und alles re-exportieren
_here = os.path.dirname(os.path.abspath(__file__))
_new_dir = os.path.join(os.path.dirname(_here), "video-transcriber")
if _new_dir not in sys.path:
    sys.path.insert(0, _new_dir)

from video_transcriber import (  # noqa: F401, E402
    extract_video_id,
    fetch_metadata,
    fetch_transcript,
    format_markdown,
    format_json,
    format_plain,
    main,
)

if __name__ == "__main__":
    main()
