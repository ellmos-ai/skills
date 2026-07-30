---
name: skill-family-care
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-07-30
description: >
  Maintenance skill that keeps skill families up to date without running a full skill-explorer audit.
  Use this skill when assigning a new skill to the correct family, updating a family header router
  after a family change, or removing an orphaned router. Also trigger on "maintain families", "assign
  new skill to a family", "update router", "set/remove family header".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, familien, pflege, routing, meta]
language: en
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
# Skill Family Care

## Purpose

Keeps skill **families** up to date — without running the full audit cycle of `skill-explorer`. Formed according to the installer principle (lean sub-skill instead of a monolith). References scripts from `skill-explorer` without copying them.

## Sources (Do Not Duplicate)

- **Family list:** `<USER_HOME>\OneDrive\.USR\SKILL-MAP.md` (canonical family / routing map).
- **Inventory (current state):** `skill-explorer/scripts/inventory_skills.py`.
- **Set/Remove router:** `skill-explorer/scripts/inject_family_header.py`.
- **Config (which families are linked):** `~/.claude/skills/skill-explorer/config.json`.

## Tasks

### A — Assigning a New Skill to a Family
1. Gather inventory anew:
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
2. Select matching family from `SKILL-MAP.md` (Axes: Phase/Breadth/Rigidity/Impact/Raw Material).
3. Record skill as member in `config.json` (`families[<fam>].members`) and in `SKILL-MAP.md`.

### B — Updating Header Router After Family Change
```bash
PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inject_family_header.py \
    --family <Familie> --skills s1,s2,s3 --router "<Wegweiser>" --inventory ~/.skill-inventory.json
```
- Idempotent: an existing block of the same family is replaced.
- Only `editable`/`source=user` skills are modified (gate inside script).

### C — Removing Orphaned Router
Same script with `--remove` (no `--router` required).

## Strict Rules

- **Survey ≠ Mutation:** only user-owned skills receive headers. Never touch plugin/external skills.
- After every change, update `config.json` (`families[*].linked`, `updated`).
- Do not copy contents from the family map into individual skills — only inject the signpost block.

## Changelog

### 0.1.0 (2026-06-17)
- Initial version. Created by audit mode (P1).
