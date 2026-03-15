---
name: web-reading
version: 1.0.0
type: protocol
author: BACH Team
created: 2026-03-12
updated: 2026-03-12
description: >
  Structured approach to reading and extracting web content.
  Decision tree for content extraction vs. structure analysis.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true

category: web
tags: [web-scraping, content-extraction, research]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: [requests, beautifulsoup4]

provenance:
  origin: "bach"
  origin_path: "system/skills/workflows/webseiten-lesen.md"
  origin_version: "3.8.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false

bach_integration:
  handler: "web-parse, web-scrape"
  db_tables: []
  hooks: []
  bach_origin_path: "system/skills/workflows/"
---

# Web Reading

## Purpose

Structured protocol for fetching and processing web content.
Distinguishes between **content extraction** (main text) and
**structure analysis** (links, forms, metadata).

## Decision Tree

```
Read webpage?
  |
  +-- Main content (article, text) sought?
  |     -> Content extraction (trafilatura/html2text)
  |     -> Result: Clean markdown text
  |
  +-- Structure (links, forms, headers) sought?
  |     -> Structure analysis (requests + parsing)
  |     -> Result: Lists of links, forms, etc.
  |
  +-- Both?
        -> Content first, then structure if needed
```

## Standalone Usage

```python
import requests
from bs4 import BeautifulSoup

def extract_content(url: str) -> str:
    """Simple content extraction without external dependencies."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove interfering elements
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()

    return soup.get_text(separator="\n", strip=True)
```

## BACH Notes

> This section is only relevant when used within BACH.

```bash
# Content extraction (main content as markdown)
bach web-parse clean <url>

# Structure analysis (links, forms, headers)
bach web-scrape get <url>
bach web-scrape links <url>
bach web-scrape forms <url>
```

## Changelog

### 1.0.0 (2026-03-12)
- Export from BACH v3.8.0 workflow `webseiten-lesen.md`
