---
name: webseiten-lesen
version: 1.0.0
type: protocol
author: BACH Team
created: 2026-03-12
updated: 2026-03-12
description: >
  Strukturiertes Vorgehen zum Lesen und Extrahieren von Webinhalten.
  Entscheidungsbaum fuer Content-Extraktion vs. Struktur-Analyse.

# Kompatibilitaet
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true

# Kategorisierung
category: web
tags: [web-scraping, content-extraction, research]
language: de
status: active

# Abhaengigkeiten
dependencies:
  tools: []
  services: []
  protocols: []
  python: [requests, beautifulsoup4]

# Provenance
provenance:
  origin: "bach"
  origin_path: "system/skills/workflows/webseiten-lesen.md"
  origin_version: "3.8.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false

# BACH-Integration (nur relevant bei Nutzung in BACH)
bach_integration:
  handler: "web-parse, web-scrape"
  db_tables: []
  hooks: []
  bach_origin_path: "system/skills/workflows/"
---

# Webseiten lesen

## Zweck

Strukturiertes Protokoll zum Abrufen und Verarbeiten von Webinhalten.
Unterscheidet zwischen **Content-Extraktion** (Haupttext) und
**Struktur-Analyse** (Links, Formulare, Metadaten).

## Entscheidungsbaum

```
Webseite lesen?
  |
  +-- Hauptinhalt (Artikel, Text) gesucht?
  |     -> Content-Extraktion (trafilatura/html2text)
  |     -> Ergebnis: Sauberer Markdown-Text
  |
  +-- Struktur (Links, Forms, Headers) gesucht?
  |     -> Struktur-Analyse (requests + Parsing)
  |     -> Ergebnis: Listen von Links, Formularen, etc.
  |
  +-- Beides?
        -> Erst Content, dann Struktur bei Bedarf
```

## Standalone-Nutzung

```python
import requests
from bs4 import BeautifulSoup

def extract_content(url: str) -> str:
    """Einfache Content-Extraktion ohne externe Abhaengigkeiten."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Stoer-Elemente entfernen
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()

    return soup.get_text(separator="\n", strip=True)
```

## BACH-Hinweise

> Dieser Abschnitt ist nur relevant bei Nutzung innerhalb von BACH.

```bash
# Content-Extraktion (Hauptinhalt als Markdown)
bach web-parse clean <url>

# Struktur-Analyse (Links, Formulare, Headers)
bach web-scrape get <url>
bach web-scrape links <url>
bach web-scrape forms <url>
```

## Changelog

### 1.0.0 (2026-03-12)
- Export aus BACH v3.8.0 Workflow `webseiten-lesen.md`
