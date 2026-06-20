---
name: {{workflow-name}}
version: 0.1.0
type: protocol
author: {{author}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
description: >
  {{Kurzbeschreibung: Was orchestriert dieser Workflow? Welche Schritte?}}

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

# Abhaengigkeiten
dependencies:
  tools: []
  services: []
  protocols: []
  skills: []

# Provenance
provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# {{Workflow-Name}}

## Zweck

{{Was ist der uebergeordnete Zweck dieses Workflows? Wann wird er ausgefuehrt?}}

## Eingaben

- **{{Parameter 1}}**: {{Beschreibung und Typ}}
- **{{Parameter 2}}**: {{Beschreibung und Typ}}

## Schritte

### Schritt 1: {{Name}}

{{Beschreibung was in diesem Schritt passiert.}}

**Aktion:** {{Konkreter Aufruf oder Anweisung}}
**Ausgabe:** {{Was liefert dieser Schritt?}}

### Schritt 2: {{Name}}

{{Beschreibung was in diesem Schritt passiert.}}

**Aktion:** {{Konkreter Aufruf oder Anweisung}}
**Ausgabe:** {{Was liefert dieser Schritt?}}

## Fehlerfaelle

| Fehler | Ursache | Loesung |
|--------|---------|---------|
| {{Fehler}} | {{Ursache}} | {{Loesung}} |

## Ausgabe

{{Was liefert der erfolgreiche Abschluss des Workflows?}}

## Hinweise

- {{Wichtige Einschraenkung}}
- {{Verweis auf verwandte Workflows oder Skills}}
