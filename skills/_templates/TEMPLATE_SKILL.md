---
name: {{skill-name}}
version: 0.1.0
type: skill
author: {{author}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
description: >
  {{Beschreibung der Faehigkeit}}

# Kompatibilitaet
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: {{kategorie}}
tags: []
language: de
status: draft
# Wie weit darf der Skill nach aussen? public | public potential | private profile | private-only
# Bewusst auf 'private-only' vorbelegt: Eine Vorlage veroeffentlicht nichts von allein.
# Erst wenn der Skill nutzerneutral ist und geprueft wurde, auf 'public' stellen --
# und dann muss er auch im oeffentlichen Repo getrackt sein (testing/privacy_gate.py
# blockiert Abweichungen). Siehe docs/CONVENTIONS.md.
visibility: private-only

# Abhaengigkeiten
dependencies:
  tools: []
  services: []
  protocols: []
  python: []

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# {{Skill-Name}}

## Zweck

{{Was macht dieser Skill? Wann wird er eingesetzt?}}

## Anweisungen

{{Detaillierte Anweisungen fuer die KI / den Nutzer}}

## Beispiele

```
{{Beispiel-Nutzung}}
```

## Changelog

### 0.1.0 ({{YYYY-MM-DD}})
- Initiale Version
