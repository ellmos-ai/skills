---
name: skill-finder
version: 0.1.0
type: skill
author: {{author}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
description: >
  Aktiver Finder/Router für die eigenen lokalen Skills (Analogon zu using-superpowers). IMMER zu Beginn
  einer nicht-trivialen Aufgabe nutzen, um zu prüfen, ob ein user-Skill passt, und zum richtigen Skill
  zu routen. Aktiviert sich bei „welcher Skill passt", „gibt es dafür einen Skill", „skill finden",
  oder generell vor Aufgaben, die ein lokaler Skill besser löst als ad-hoc-Arbeit.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, finder, routing, discovery, meta]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: [code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-finder/"
  origin_version: "0.1.0"
---

# Skill-Finder

## Die Regel

Vor jeder nicht-trivialen Aufgabe zuerst prüfen, ob ein lokaler Skill sie besser löst. Schon bei
geringem Verdacht den passenden Skill laden und **seiner Live-Anleitung folgen** (Datei lesen, nicht
aus dem Gedächtnis arbeiten). Trifft kein Skill zu, normal fortfahren.

## Familien-Routing

<!-- Generiert/aktualisiert aus the family map + inventory_skills.py. Thema -> Familie -> Skill. -->

| Thema / Absicht | Familie | Skill(s) |
|-----------------|---------|----------|
| neue Ideen / Kreativität | Denkwerkzeuge | `/brainstorm` (vs `/think` Analyse, `/decide` Auswahl) |
| Bug / Testfehler | Coding & Debugging | `/bugfix-protocol`, `/bugsweep` |
| Recherche mit Quellen | Wissen/Recherche | `/deep-research`, `/find-docs` |
| Roblox-Spiel | Game-Dev | `/roblox-dev` (→ `/rojo`, `/roblox-studio`, `/game-design`) |
| Skills vergleichen/aufräumen | System/Meta | den Audit-Modus, den Explore-Modus |
| {{weitere aus Register}} | {{Familie}} | {{Skill}} |

Vollständige Liste: Skill `code-skill-index`.

## Red Flags (Rationalisierungen, die STOP bedeuten)

| Gedanke | Realität |
|---------|----------|
| „Das ist nur eine kurze Frage." | Fragen sind Aufgaben — Skill-Check zuerst. |
| „Ich kenne das Konzept." | Konzept kennen ≠ Skill nutzen. Live-Datei lesen. |
| „Der Skill ist Overkill." | Einfaches wird komplex — nutzen. |
| „Ich erkunde erst selbst." | Skills sagen WIE man erkundet. Erst prüfen. |

## Pflege

Routing-Tabelle bei Familienänderung aktualisieren (Subskill `skill-family-care` oder neuer
`inventory_skills.py`-Lauf aus `skill-explorer`).

## Changelog

### 0.1.0 ({{YYYY-MM-DD}})
- Initiale Version. Erzeugt von den Audit-Modus ([F]) als Analogon zu using-superpowers.
