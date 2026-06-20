---
name: {{prompt-name}}
version: 0.1.0
type: prompt
author: {{author}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
description: >
  {{Kurzbeschreibung: Wozu dient dieses Prompt-Template?}}

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

# {{Prompt-Name}}

## Zweck

{{Wozu wird dieses Prompt eingesetzt? Welches Problem loest es?}}

## Prompt-Template

```
{{Eigentliches Prompt hier einfuegen. Platzhalter in doppelten geschweiften Klammern markieren: {{VARIABLE}}}}
```

## Variablen

| Variable | Beschreibung | Beispiel |
|----------|-------------|---------|
| `{{VARIABLE}}` | {{Beschreibung}} | {{Beispielwert}} |

## Verwendungsbeispiel

```
{{Ausgefuelltes Beispiel mit echten Werten}}
```

## Hinweise

- {{Wichtige Einschraenkung oder Besonderheit}}
- {{Empfohlenes Modell oder minimale Modell-Anforderungen}}
