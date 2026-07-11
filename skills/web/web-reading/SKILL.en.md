---
name: web-reading
version: 1.1.0
type: protocol
author: BACH Team
created: 2026-03-12
updated: 2026-07-05
description: >
  Router and protocol for reading and extracting web content.
  Decides first WHAT is needed (main text vs. structure vs. screenshot) and then
  WHICH tool available on the system delivers it. If nothing suitable is present,
  it recommends installing the web-scraper module.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true

category: web
tags: [web-scraping, content-extraction, research, router]
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
  local_changes_since_sync: true

bach_integration:
  handler: "web-parse, web-scrape"
  db_tables: []
  hooks: []
  bach_origin_path: "system/skills/workflows/"
---

# Web Reading (Router)

## Purpose

Fetch and process web content — but don't pick a tool blindly. This skill
routes: **purpose first, then the best available tool.** The actual
implementation lives in the **`web-scraper` module**; this skill only shows
what is currently present and how to use it.

## Step 1 — What is needed?

```
Process a web page?
  |
  +-- Main text (article / prose)   → "Content"     → Step 2A
  +-- Links / forms / headers       → "Structure"   → Step 2B
  +-- Rendered image of the page    → "Screenshot"  → Step 2C
```

## Step 2 — Which tool? (Router)

Use the **first available** tool in each list. "Available" means the
tool/skill/module is actually present in this session.

### 2A — Content (main text, clean markdown)

| Priority | Tool | Available when … | Usage |
|---|---|---|---|
| 1 | **`defuddle`** skill | skill `defuddle` listed | clean markdown from normal web pages |
| 2 | Built-in **`WebFetch`** | agent has the WebFetch tool | quick read/summary of a URL |
| 3 | **`fc_web_fetch`** (MCP) | FileCommander MCP loaded | `mode: "extract"` |
| 4 | **`web-scraper`** module | module installed/importable | `web-scraper extract <url>` / `extract(url)` |

> Note: `.md` URLs are already markdown → use `WebFetch` directly, no extractor.

### 2B — Structure (links, forms, headers)

`WebFetch`/`defuddle` are **not** suitable here (they return processed text, not
raw structure). Use instead:

| Priority | Tool | Available when … | Usage |
|---|---|---|---|
| 1 | **`fc_web_fetch`** (MCP) | FileCommander MCP loaded | `mode: "links" \| "forms" \| "headers"` |
| 2 | **`web-scraper`** module | module installed/importable | `web-scraper links\|forms\|headers <url>` |

### 2C — Screenshot

| Priority | Tool | Available when … | Usage |
|---|---|---|---|
| 1 | **`web-scraper`** module | module with `[screenshot]` extra | `web-scraper screenshot <url> --out img.png` |
| 2 | Browser automation tool | e.g. Playwright/Computer-Use present | page-dependent |

## Step 3 — Fallback: nothing suitable found?

If **no** tool is available for the purpose, recommend installing the
**`web-scraper` module** (full: get/links/forms/headers/extract/screenshot):

```bash
# from the local module folder (.MODULES/.TOOLS/web-scraper)
pip install ".[http,extract]"          # + [screenshot] for screenshots

# then:
web-scraper extract <url>
```

As a library:

```python
from web_scraper import WebScraper, extract
print(extract("https://example.com")["content"])
```

## Last resort — standalone snippet (no dependencies beyond requests/bs4)

```python
import requests
from bs4 import BeautifulSoup

def extract_content(url: str) -> str:
    """Simple content extraction."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)
```

## Changelog

### 1.1.0 (2026-07-05)
- Reworked from a plain protocol into a **router**: detects available web
  capabilities (`defuddle`, `WebFetch`, `fc_web_fetch`, `web-scraper` module)
  and routes by purpose (content/structure/screenshot); otherwise recommends the
  `web-scraper` module.
- Unified name to `web-reading` (was `webseiten-lesen` in the DE version).
- Removed BACH CLI examples from the body (standalone-compliant; origin stays
  documented in the `bach_integration` frontmatter).

### 1.0.0 (2026-03-12)
- Export from BACH v3.8.0 workflow `webseiten-lesen.md`
