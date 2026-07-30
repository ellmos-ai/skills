---
name: skill-family-care
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: >
  Pflege-Skill, der die Skill-Familien aktuell hält, ohne den vollen skill-explorer-Audit zu fahren.
  Nutze diesen Skill, wenn ein neuer Skill der richtigen Familie zugeordnet, ein Familien-Header-Router
  nach einer Familienänderung nachgezogen oder ein verwaister Router entfernt werden soll. Auch
  auslösen bei „Familien pflegen", „neuen Skill einer Familie zuordnen", „Router aktualisieren",
  „Familien-Header setzen/entfernen".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, familien, pflege, routing, meta]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: [skill-explorer, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-family-care/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="skill-family-care banner">
# Skill-Family-Care

## Zweck

Hält die Skill-**Familien** aktuell — ohne den vollen Audit-Lauf von `skill-explorer`. Ausgegründet
nach dem Installer-Prinzip (schlanker Subskill statt Monolith). Referenziert die Skripte von
`skill-explorer`, kopiert sie nicht.

## Quellen (nicht duplizieren)

- **Familienliste:** `<USER_HOME>\OneDrive\.USR\SKILL-MAP.md` (kanonische Family-/Routing-Map).
- **Inventar (Ist-Stand):** `skill-explorer/scripts/inventory_skills.py`.
- **Router setzen/entfernen:** `skill-explorer/scripts/inject_family_header.py`.
- **Config (welche Familien verlinkt):** `~/.claude/skills/skill-explorer/config.json`.

## Aufgaben

### A — Neuen Skill einer Familie zuordnen
1. Inventar neu erheben:
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
2. Passende Familie aus `SKILL-MAP.md` wählen (Achsen: Phase/Breite/Rigidität/Wirkung/Rohstoff).
3. Skill als Mitglied in `config.json` (`families[<fam>].members`) und in `SKILL-MAP.md` eintragen.

### B — Header-Router nach Familienänderung nachziehen
```bash
PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inject_family_header.py \
    --family <Familie> --skills s1,s2,s3 --router "<Wegweiser>" --inventory ~/.skill-inventory.json
```
- Idempotent: ein vorhandener Block derselben Familie wird ersetzt.
- Nur `editable`/`source=user`-Skills werden verändert (Gate im Skript).

### C — Verwaisten Router entfernen
Gleiches Skript mit `--remove` (kein `--router` nötig).

## Eiserne Regeln

- **Survey ≠ Mutation:** nur user-eigene Skills bekommen Header. Plugin/extern nie anfassen.
- Nach jeder Änderung `config.json` (`families[*].linked`, `updated`) aktualisieren.
- Keine Inhalte aus der Family-Map in die Einzelskills kopieren — nur Wegweiser-Block.

## Changelog

### 0.1.0 (2026-06-17)
- Initiale Version. Erzeugt vom Audit-Modus (P1).
