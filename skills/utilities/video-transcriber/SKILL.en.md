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
language: en
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['youtube-transcript-api', 'yt-dlp']}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/youtube_extractor.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-04-04', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="video-transcriber banner">

> **English** — Official English version of `video-transcriber`.


# Video Transcriber (English)

Fetches transcripts (subtitles) and metadata (title, channel, date, views,
description) of online videos. Prefers manually created subtitles, falls back
to auto-generated ones. Output as Markdown, JSON, or plain text.

For every requested language, the fallback tries manual exact and base-language
tracks before automatic exact and base-language tracks; arbitrary tracks follow
only afterwards. An unreadable JSON3 track does not stop the fallback while
another candidate remains available.

Currently supported source: **YouTube** (youtube.com, youtu.be, youtube-nocookie.com).

For videos, use this tool instead of summarizing content manually —
the transcript is the reliable source.

> **Notice:** This tool is not affiliated with, endorsed by, or sponsored by
> YouTube or Google. Use is at the user's own responsibility. Users are solely
> responsible for complying with the terms of service of the respective platform
> and applicable copyright law. No circumvention of DRM, paywalls, or access
> restrictions. No mass scraping. No redistribution of copyrighted transcripts
> without the rights holder's consent.

## Dependencies and licenses

```bash
pip install youtube-transcript-api   # transcripts (required) — MIT license
pip install yt-dlp                   # metadata (optional, fallback: noembed) — Unlicense (Public Domain)
```

## Usage

> **Windows note:** Always set `PYTHONIOENCODING=utf-8`, otherwise umlauts and
> special characters break in the output (cp1252 encoding).

```bash
# Default: Markdown with timestamps (English)
PYTHONIOENCODING=utf-8 python video_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Choose output format (English)
PYTHONIOENCODING=utf-8 python video_transcriber.py URL --format markdown|json|plain

# Save to file (English)
PYTHONIOENCODING=utf-8 python video_transcriber.py URL -o transcript.md

# Prefer languages (default: de en) (English)
PYTHONIOENCODING=utf-8 python video_transcriber.py URL --lang de en fr
```

### Options

| Option | Effect |
|--------|--------|
| `--format markdown\|json\|plain` | Output format (default: markdown) |
| `--output, -o <file>` | Write to file instead of stdout |
| `--lang <codes...>` | Preferred subtitle languages (default: de en) |
| `--meta-only` | Metadata only, no transcript |
| `--transcript-only` | Transcript only, no metadata |
| `--no-timestamps` | Transcript without timestamps |
| `--no-meta` | Faster: skip yt-dlp metadata |
| `--allow-empty-transcript` | Treat an empty transcript as success (exit 0 instead of 3) |

### Exit codes

An empty transcript is **not** a success. Before 1.2.0 this case exited with 0:
the output file was written, the segment array was empty, and every calling
script treated it as done. That silent failure is the defect 1.2.0 removes.

| Code | Meaning |
|------|---------|
| `0` | Success -- transcript present, or `--meta-only`, or `--allow-empty-transcript` |
| `1` | Not a valid video URL/ID |
| `2` | Usage error (assigned by argparse, e.g. unknown option) |
| `3` | No transcript retrieved -- both paths came back empty |

`2` stays reserved for argparse so that a typo in the invocation remains
distinguishable from a video that simply has no subtitles.

### As a Python library

```python
from video_transcriber import extract_video_id, fetch_metadata, fetch_transcript, format_markdown

video_id = extract_video_id("https://www.youtube.com/watch?v=VIDEO_ID")
meta = fetch_metadata(video_id)
transcript = fetch_transcript(video_id, languages=["de", "en"])
output = format_markdown(meta, transcript)
```

## Typical use cases

- Research: make video content citable as text
- Source analysis: examine argumentation/metaphors in talks
- Summaries: transcript as a reliable basis instead of hallucination

## Limits

- Only works if the video has subtitles (manual or automatic)
- Automatic subtitles can contain recognition errors
- No audio download, no built-in speech recognition -- the fallback path also
  fetches the subtitle track only, never video or audio
- The fallback path needs a JSON3 track; if the platform serves other formats
  only, the run ends with exit 3 rather than partial output

## Changelog

### 1.2.0 (2026-08-24)
- **Exit semantics:** an empty transcript now exits `3` instead of silently `0`.
  An invalid URL exits `1` as a named constant. `--meta-only` still succeeds,
  because no transcript is expected there.
- **New option `--allow-empty-transcript`:** deliberately treats an empty
  transcript as success, for callers that regard subtitles as optional.
- **yt-dlp subtitle fallback:** engages as soon as the primary path returns no
  segments (not only on an exception). Uses `extract_info(download=False)` and
  reads the subtitle URL only -- no video, no audio, no circumvention of access
  restrictions.
- **Hardened language selection:** `de-orig`/`de-DE` are now found for
  `--lang de` (base-language match). Per requested language, manual exact/base
  tracks precede automatic exact/base tracks, and unreadable candidates do not
  stop later fallback attempts.
- **`source` field** in the result: `youtube_transcript_api` or `yt-dlp`.
- Regression tests: 29 tests with mocked responses (UTF-8, all three output
  formats, exit codes, language selection, JSON3 parsing).

### 1.1.0 (2026-06-20)
- Renamed from `yt-transcriber` → `video-transcriber` (YouTube branding policy:
  "yt" is an explicitly forbidden abbreviation; see RECHTSCHECK_2026-06-20.md)
- Script: `yt_transcriber.py` → `video_transcriber.py`
- Disclaimer and dependency licenses added (user responsibility, ToS, no endorsement)
- YouTube mentioned descriptively as a source only, not as a name/brand component
- Backward-compat wrapper `yt_transcriber.py` retained at the old path

### 1.0.0 (2026-06-12)
- SKILL.md added (the tool already existed as a script + README)
- Script v1.0.0: transcript + metadata, 3 output formats, language preferences
