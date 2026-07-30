---
name: skill-register-care
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-07-30
description: >
  Maintenance skill that keeps the three-part skill register consistent (code-skill-index catalogs,
  skill index, SKILL-MAP family/routing map). Use this skill for a drift check between the real skill
  inventory and the documented register: report missing or surplus entries, correct counts, set updated date.
  Also trigger on "maintain skill register", "update index", "check register drift", "which skills are missing in the map".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, register, index, drift, pflege, meta]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: [skill-explorer, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-register-care/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="skill-register-care banner">
# Skill Register Care

## Purpose

Keeps the **register** drift-free. The register consists of three interconnected artifacts — never create a fourth, always expand these three:

- `~/.claude/skills/code-skill-index/references/catalog-*.md` (category catalogs)
- the Skill Index (master list)
- `<USER_HOME>\OneDrive\.USR\SKILL-MAP.md` (family / routing map)

## Drift Check Procedure

1. **Gather current state:**
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
   Only `source=user` skills are register-relevant (plugin/external remain excluded).
2. **Read target state:** the three register artifacts.
3. **Form difference:**
   - **Missing** (in inventory, not in register) → add.
   - **Orphaned** (in register, no longer in inventory) → mark/remove.
   - **Count discrepancy** (e.g., "18 skills" no longer correct) → correct count.
4. **Update entries:** for each new skill, add a line in the matching `catalog-<kategorie>.md`, a line in the Skill Index (+ header date), and — if new/modified family — a section in `SKILL-MAP.md`.
5. **Set updated date** in all touched files to the current date.

## Helper Snippet (List missing user skills)

```bash
PYTHONIOENCODING=utf-8 python -c "
import json
inv=json.load(open('<USER_HOME>/.skill-inventory.json',encoding='utf-8'))
print('\n'.join(s['dir'] for s in inv['skills'] if s['source']=='user'))
"
```
Cross-check the output against the register artifacts (manually or via grep).

## Strict Rules

- **No fourth register** — only expand these three.
- Only user-authored skills belong in the register; third-party skills follow the external path.
- Do not guess dates — set the current date.

## Changelog

### 0.1.0 (2026-06-17)
- Initial version. Created by audit mode (P2). Reason: during audit 2026-06-17 ~10 user skills were missing in SKILL-MAP (swarm-operations, model-strategy, agents-bridge, mcp-config-sync, system-onboarding, update-cli-docs, migrate-rename, plugin-system + therapy and game dev family).
