---
name: {{skill-name}}
version: 1.0.0
type: {{skill | agent | expert | service | protocol | tool}}
author: {{author}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
description: >
  {{Beschreibung}}

# Kompatibilitaet
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true

# Kategorisierung
category: {{kategorie}}
tags: []
language: de
status: active

# Abhaengigkeiten (nur standalone-faehige!)
dependencies:
  tools: []
  services: []
  protocols: []
  python: []

# BACH-Integration (optional, fuer Rueck-Import)
bach_integration:
  handler: null
  db_tables: []
  hooks: []
  bach_origin_path: "system/{{pfad}}/"

# Provenance
provenance:
  origin: "bach"
  origin_path: "system/{{pfad}}/"
  origin_version: "{{bach-version}}"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "{{YYYY-MM-DD}}"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# {{Skill-Name}}

> Exportiert aus BACH v{{version}} am {{datum}}.
> Original: `{{bach-pfad}}`

## Zweck

{{Beschreibung}}

## Anweisungen

{{Standalone-faehige Anweisungen -- KEINE bach_api oder bach CLI Referenzen}}

## BACH-Hinweise

> Dieser Abschnitt ist nur relevant wenn der Skill innerhalb von BACH genutzt wird.
> Fuer standalone-Nutzung kann er ignoriert werden.

{{BACH-spezifische Zusatzinfos, CLI-Befehle, Handler-Referenzen}}

## Changelog

### 1.0.0 ({{YYYY-MM-DD}})
- Export aus BACH v{{version}}
