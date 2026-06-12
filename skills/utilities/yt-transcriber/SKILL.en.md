---
name: yt-transcriber
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-04-04
updated: 2026-06-13
description: >
  Fetch YouTube transcripts (subtitles) and video metadata and output them as
  Markdown, JSON, or plain text. Prefers manually created subtitles, falls back
  to auto-generated ones.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true

category: utilities
tags: [youtube, transcript, subtitles, metadata, research, video]
language: en
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

# YouTube Transcriber

Fetches transcripts (subtitles) and metadata (title, channel, date, views,
description) of YouTube videos. Prefers manually created subtitles, falls back
to auto-generated ones. Output as Markdown, JSON, or plain text.

For YouTube videos, use this tool instead of summarizing content manually —
the transcript is the reliable source.

## Dependencies

```bash
pip install youtube-transcript-api   # transcripts (required)
pip install yt-dlp                   # metadata (optional, fallback: noembed)
```

## Usage

> **Windows note:** Always set `PYTHONIOENCODING=utf-8`, otherwise umlauts and
> special characters break in the output (cp1252 encoding).

```bash
# Default: Markdown with timestamps
PYTHONIOENCODING=utf-8 python yt_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Choose output format
PYTHONIOENCODING=utf-8 python yt_transcriber.py URL --format markdown|json|plain

# Save to file
PYTHONIOENCODING=utf-8 python yt_transcriber.py URL -o transcript.md

# Prefer languages (default: de en)
PYTHONIOENCODING=utf-8 python yt_transcriber.py URL --lang de en fr
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

### As a Python library

```python
from yt_transcriber import extract_video_id, fetch_metadata, fetch_transcript, format_markdown

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
- No audio download, no built-in speech recognition

## Changelog

### 1.0.0 (2026-06-12)
- SKILL.md added (the tool already existed as a script + README)
- Script v1.0.0: transcript + metadata, 3 output formats, language preferences
