---
name: skill-register-care
version: 0.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-09-20
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
  origin_version: "0.2.0"
---

<img src="banner.png" width="100%" alt="skill-register-care banner">
# Skill Register Care

## Purpose

Keeps the **register** drift-free. The register consists of three interconnected artifacts — never create a fourth, always expand these three:

| Artifact | Role | Upkeep |
|---|---|---|
| `~/.claude/skills/code-skill-index/references/catalog-*.md` | category catalogs | curated, by hand |
| `<USER_HOME>/OneDrive/.SYNC/CLAUDE-CODE-SKILLS.md` | cross-system index (the only skill view Claude Desktop has) | **automated**, see below |
| `<USER_HOME>/OneDrive/.USR/SKILL-MAP.md` | family / routing map | curated, by hand |

## Automated: the cross-system index

The index is no longer updated by hand — that is what let it sit still for three months
(state 2026-06-21 against 152 real skills on 2026-09-20; 81 were missing). Instead:

```bash
PYTHONIOENCODING=utf-8 python "<USER_HOME>/OneDrive/.SYNC/scripts/skill_index_care.py" --check
PYTHONIOENCODING=utf-8 python "<USER_HOME>/OneDrive/.SYNC/scripts/skill_index_care.py" --apply
```

It already runs as **step 2b of the daily `/sync`**; run it manually only when skills were just
built or deployed and the index has to be right immediately. The run is additive and
idempotent: curated short descriptions stay, missing skills are filed by library category, and
entries without an active `SKILL.md` are **marked rather than deleted**.

## Drift Check Procedure (the two curated registers)

1. **Gather current state:**
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
   Only `source=user` skills are register-relevant (plugin/external remain excluded).
2. **Read target state:** the three register artifacts.
3. **Form difference:**
   - **Missing** (in inventory, not in register) → add.
   - **Orphaned** (in register, no longer in inventory) → **look before you judge.**
     A skill folder whose `SKILL.md` was renamed to `CONTENT.md` is *deregistered*: deliberately
     no longer loaded as a skill, yet still present and findable via `code-skill-index`. The
     inventory does not count it, but it must not be deleted — mark it. Remove an entry only
     when the folder itself is gone.
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
- Do **not** hand-edit the cross-system index; run `skill_index_care.py`. Manual lines there are
  the seed of the next silent drift.

## Changelog

### 0.2.0 (2026-09-20)
- Cross-system index `CLAUDE-CODE-SKILLS.md` moved onto `.SYNC/scripts/skill_index_care.py`
  (additive, marking, idempotent) and wired into the daily `/sync` as step 2b. Reason: the index
  had been stale since 2026-06-21 — 81 local skills missing, 15 entries silently pointing at
  deregistered procedures, one at a folder without `SKILL.md`.
- Sharpened "orphaned": deregistered skills (`CONTENT.md` instead of `SKILL.md`) get marked, not
  removed — otherwise the catch-up run would have deleted 15 curated entries.

### 0.1.0 (2026-06-17)
- Initial version. Created by audit mode (P2). Reason: during audit 2026-06-17 ~10 user skills were missing in SKILL-MAP (swarm-operations, model-strategy, agents-bridge, mcp-config-sync, system-onboarding, update-cli-docs, migrate-rename, plugin-system + therapy and game dev family).
