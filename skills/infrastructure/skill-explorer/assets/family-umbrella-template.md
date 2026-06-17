---
name: {{familie}}-umbrella
version: 0.1.0
type: skill
author: {{author}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
description: >
  Meta-/Umbrella-Skill für die Familie „{{Familie}}". Kennt alle Skills der Familie und leitet zum
  passenden weiter. Nutze diesen Skill, wenn unklar ist, welcher {{Familie}}-Skill passt, oder wenn
  ein Überblick/Routing über die Familie gebraucht wird. Auch auslösen bei {{trigger-phrasen}}.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: {{kategorie}}
tags: [{{familie}}, umbrella, meta, routing]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: [{{skill1}}, {{skill2}}, {{skill3}}]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/{{familie}}-umbrella/"
  origin_version: "0.1.0"
---

# {{Familie}} — Umbrella

## Zweck

Einstiegspunkt für die Familie „{{Familie}}". Bündelt das übergreifende Wissen und leitet für
Spezialfälle an den passenden Skill weiter.

## Mitglieder & Routing

| Skill | Wofür | Wann diesen statt der anderen |
|-------|-------|-------------------------------|
| `/{{skill1}}` | {{kurz}} | {{vorzugsregel}} |
| `/{{skill2}}` | {{kurz}} | {{vorzugsregel}} |
| `/{{skill3}}` | {{kurz}} | {{vorzugsregel}} |

> Routing-Regel: {{eine-zeile-routing, z. B. "neue Ideen -> /brainstorm; Analyse -> /think; Auswahl -> /decide"}}.

## Gut gekoppelte Kombinationen

- {{Skill A (vor) → Skill B (nach): warum sie sich verstärken}}

## Gemeinsame Konventionen

- {{geteilte Prinzipien/Begriffe der Familie}}

## Changelog

### 0.1.0 ({{YYYY-MM-DD}})
- Initiale Version. Erzeugt von den Audit-Modus (c1) für die Familie {{Familie}}.
