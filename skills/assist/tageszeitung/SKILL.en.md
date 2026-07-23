---
name: tageszeitung
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: >
  Creates a personalised daily newspaper from RSS feeds and web sources.
  Ported from the BACH news system (news.py + newspaper_generator.py).
  Own SQLite store (no Origin-DB). feedparser optional — XML fallback
  via stdlib. PDF export via Edge Headless (msedge.exe).
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags:
  - zeitung
  - news
  - rss
  - feed
  - pdf
  - tageszeitung
language: en
status: stable

dependencies:
  tools:
    - name: msedge.exe
      optional: true
      purpose: "HTML → PDF (Edge Headless); without Edge: HTML output only"
  services: []
  protocols: []
  python:
    - name: feedparser
      optional: true
      install: "pip install feedparser"
      purpose: "RSS parsing (main backend). Fallback: defusedxml → regex"
    - name: defusedxml
      optional: true
      install: "pip install defusedxml"
      purpose: "XXE-safe XML parser as fallback when feedparser is missing. Without defusedxml a regex fallback is used (no ET.fromstring on network data)."

provenance:
  origin: bach-port
  origin_path: "BACH/system/hub/news.py + hub/_services/newspaper/newspaper_generator.py"
  origin_version: "news.py v1.x, newspaper_generator.py v1.x"
  origin_repo: "ellmos-ai/bach (privat)"
  origin_license: MIT
  last_sync_from_origin: "2026-06-22"
  notes: >
    Schema (news_sources + news_items) 1:1 aus BACH news.py portiert.
    BaseHandler-Abhängigkeit entfernt. Origin-DB-Pfad entfernt. DB-Pfad
    konfigurierbar. newspaper_generator.py-Logik (HTML-Render + Edge-PDF)
    userneutral übernommen.
---

## Purpose

Fetch articles from configured RSS feeds and web sources, sort them by category
and render them as an HTML/PDF daily newspaper. Articles are stored locally in
`tageszeitung/store.db` and marked as read.

---

## Triggers

| Phrase | Action |
|---|---|
| "Create my daily newspaper" | Fetch articles + render PDF |
| "Daily newspaper for today" | Render today's newspaper |
| "Add feed [URL]" | Register RSS source |
| "Show my sources" | Output source list |
| "Fetch news" | Fetch all sources (no render) |

---

## Workflow

1. **Check sources**: Read all active sources from `news_sources`.
2. **Fetch**: RSS via feedparser (or xml.etree fallback), web via urllib.
3. **Deduplication**: UNIQUE(source_id, url) prevents duplicates.
4. **Render**: Group unread articles by category → HTML → PDF.
5. **Deliver**: Place HTML/PDF in output folder (configurable path).

---

## CLI Entry Point

```bash
# Add source
python tageszeitung_core.py add-source "Heise" rss https://www.heise.de/rss/heise-atom.xml --category tech

# Fetch all sources
python tageszeitung_core.py fetch

# Render daily newspaper (HTML + PDF if Edge available)
python tageszeitung_core.py render [--date 2026-06-22] [--out /path/]

# List sources
python tageszeitung_core.py sources

# Unread articles
python tageszeitung_core.py items [--limit 50] [--category tech]

# Mark article as read
python tageszeitung_core.py read <item_id>

# Alternative store (e.g. for tests)
python tageszeitung_core.py --store /tmp/t.db sources --dry-run
```

---

## Store

| Property | Value |
|---|---|
| Type | SQLite |
| Path (default) | `skills/assist/tageszeitung/store.db` |
| Override | `--store <path>` or env `TAGESZEITUNG_STORE` |
| Tables | `news_sources`, `news_items` |

### Schema (ported from BACH news.py)

```sql
CREATE TABLE IF NOT EXISTS news_sources (
    id           TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    type         TEXT NOT NULL DEFAULT 'rss',  -- rss | web
    url          TEXT NOT NULL UNIQUE,
    category     TEXT DEFAULT 'Allgemein',
    schedule     TEXT DEFAULT 'daily',
    is_active    INTEGER DEFAULT 1,
    last_fetched TEXT,
    fetch_count  INTEGER DEFAULT 0,
    error_count  INTEGER DEFAULT 0,
    last_error   TEXT,
    created_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS news_items (
    id           TEXT PRIMARY KEY,
    source_id    TEXT NOT NULL REFERENCES news_sources(id),
    title        TEXT NOT NULL,
    content      TEXT,
    summary      TEXT,
    url          TEXT,
    author       TEXT,
    published_at TEXT,
    fetched_at   TEXT NOT NULL,
    is_read      INTEGER DEFAULT 0,
    category     TEXT,
    UNIQUE(source_id, url)
);
```

---

## Attitude

- feedparser is preferred; without feedparser an xml.etree fallback handles simple RSS 2.0 feeds.
- PDF generation requires `msedge.exe` in the system PATH or `MSEDGE_PATH` env. Without Edge only HTML is rendered.
- Maximum articles per category: configurable via `assist/prefs.json` (`tageszeitung_max_per_category`, default: 5).

---

## Privacy

- Article contents stay local in `store.db`.
- No external analysis services — only the configured RSS/web sources are called.

---

## Related Resources

- BACH `hub/news.py` — origin (read-only)
- BACH `hub/_services/newspaper/newspaper_generator.py` — origin (read-only)

---

## Changelog

| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-06-22 | Initial creation — BACH schema ported, own store, feedparser optional |
