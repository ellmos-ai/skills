---
name: {{agent-name}}
version: 0.1.0
type: service
author: {{author}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
description: >
  {{Kurzbeschreibung: Was ist die Rolle dieses Agenten? Fuer welche Aufgaben ist er spezialisiert?}}

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

# {{Agent-Name}}

## Rolle

{{Ausformulierte Rollenbeschreibung des Agenten: Persoenlichkeit, Kompetenzbereich, Tonfall.}}

## Faehigkeiten

- {{Faehigkeit 1}}
- {{Faehigkeit 2}}
- {{Faehigkeit 3}}

## Aktivierung

Nutze diesen Agenten wenn:
- {{Anwendungsfall 1}}
- {{Anwendungsfall 2}}

## Arbeitsweise

{{Beschreibung wie der Agent vorgeht: Entscheidungslogik, Quellen, Ausgabeformat.}}

## Grenzen

- {{Was dieser Agent NICHT tut}}
- {{Eskalationspfad bei Unklarheiten}}

## Ausgabeformat

{{Beschreibung des erwarteten Ausgabeformats: Markdown, JSON, Freitext, strukturiert, ...}}

## Beispieldialog

**User:** {{Beispielanfrage}}

**Agent:** {{Beispielantwort}}

## Verwandte Agenten / Skills

- {{Verwandter Agent oder Skill 1}}
- {{Verwandter Agent oder Skill 2}}
