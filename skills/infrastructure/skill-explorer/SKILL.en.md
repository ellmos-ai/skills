---
name: skill-explorer
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: >
  Manages your own skill landscape: surveys and compares existing skills (Audit mode),
  researches the web for new skills/plugins (Explore mode), and is at the same time the installer that
  generates lean subskills (Skill-Finder, family umbrella, maintenance skills) instead of loading a
  monolith. Use this skill for "compare/audit skills", "which skills are duplicated",
  "form skill families", "clean up/consolidate skills", "maintain the skill register", "find skills/plugins
  for topic X", "install new skills", "browse the skill marketplace", or for
  `/skill-explorer`. Delivers a sub-report per family and a globally numbered
  decision list; installs/uninstalls only after a security check and explicit approval.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, audit, cluster, recherche, install, security, installer, meta, workflow, branch, fork]
language: en
status: active

dependencies:
  tools: [git]
  services: [websearch]
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-explorer/"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Skill-Explorer — Manage the Skill Landscape (Audit · Explore · Installer)

## Purpose

As the skill inventory grows, duplicates, unused resources, and unclear "which skill instead of which"
situations arise — and there are constantly new skills/plugins out there. `skill-explorer`
bundles three roles into one tool:

| Role | What it does | Detail |
| --- | --- | --- |
| **Audit mode** (inward) | survey all skills, cluster them into families, gather capabilities/dependencies/resources, produce a sub-report + numbered recommendations per family | `references/audit-mode.md` |
| **Explore mode** (outward) | research the web (web/GitHub/Reddit, bilingual) for new skills/plugins on a topic, compare, install gated | `references/explore-mode.md` |
| **Installer** | *generate* lean subskills instead of a monolith — Skill-Finder, family umbrella, maintenance skills | below + `references/family-care.md` |

Invocation: `/skill-explorer` (Audit as default) or "… find for topic X" (Explore). Both modes share
a taxonomy (`references/clustering.md`), a report format (`references/report-format.md`), and the
numbering scheme, so the user can respond with a single numbered list.

## Installer Principle & Persistence

Instead of growing monolithically itself, `skill-explorer` *generates* lean, individually
loadable subskills on demand — so an overlong single skill never has to be loaded:

- **Skill-Finder** ([F]) — an active finder/router analogous to a "using-superpowers" doorman that reads
  the register before every task and routes to the matching family (`references/skill-finder.md`,
  template `assets/skill-finder-template.md`).
- **Family umbrella** (c1) — a meta-skill that knows an entire family (`assets/family-umbrella-template.md`).
- **Maintenance skills** ([P1] families, [P2] register) — keep families/register up to date (`references/family-care.md`).

Decisions are persisted in `~/.claude/skills/skill-explorer/config.json`
(`references/config.md`, template `assets/config.example.json`): read at startup (known
families/routers/generated subskills), update after execution — so a re-run never creates anything twice.

## Branch Mechanism (Customizing Third-Party Skills)

A read-only skill (plugin, imported third-party) can be customized without modifying the original:
the original directory is copied in full (**branch**); only the copy is then edited. The branch
carries four mandatory fields: a reference to the original, the branch date, the author, and the
reason. Once the branch supersedes the original, the original is deregistered from the runtime
(`SKILL.md` → `CONTENT.md`) or the family router is pointed to the branch, so two nearly identical
skills do not collide. Third-party branches stay **private** — they do not go into the public
`.AI/.SKILLS` library. Details: `references/skill-branching.md`.

## Workflow

1. **Choose mode:** survey/clean up the inventory → Audit mode. Search/install from outside →
   Explore mode. (Explore can build on a previous audit/`config.json`.)
2. **Audit mode** (`references/audit-mode.md`): inventory (script) → family clusters → sub-reports →
   **one globally numbered decision list** (a/b/c1/c2/c3, plus R/F/P1/P2).
3. **Explore mode** (`references/explore-mode.md`): bilingual multi-source research → 3 categories
   per candidate → impact simulation → numbered install/remove recommendations.
4. **Execute** only after the user's numeric confirmation; register skill creation/changes and
   update `config.json`.

## Iron Rules

- **Survey ≠ mutation:** cluster everything, but only edit **user-owned** skills; plugin/third-party
  skills are read-only (never modify the header/delete). To customize a third-party skill, create a
  **branch** (fork copy) instead — the original remains untouched, all changes are made exclusively
  on the copy (→ `references/skill-branching.md`).
- **Extend the register, do not duplicate:** if a skill register exists (index + family map +
  index skill), extend it instead of creating a fourth one.
- **Security primarily manual:** before every installation, the model reads the skill itself and judges;
  `scripts/scan_skill_security.py` is only supporting triage with known limits. Never auto-install.
- **Registration by origin:** user-authored → Library; third-party → external path, **not** Library.

## Orchestration (model-neutral)

Family sub-reports or sources/languages are independent work paths. If the platform offers
cheaper subagents than the orchestrator itself, assign one subagent per family/source
and, as orchestrator, only consolidate/verify (specialist swarm). Otherwise sequentially yourself.

## Resources

- **Modes:** `references/audit-mode.md`, `references/explore-mode.md`
- **Shared:** `references/clustering.md`, `references/report-format.md`, `references/config.md`
- **Audit:** `references/family-care.md`, `references/skill-finder.md`
- **Explore:** `references/research-method.md`, `references/integration-sim.md`, `references/install-uninstall.md`
- **Branch:** `references/skill-branching.md`
- **Scripts:** `scripts/inventory_skills.py` (inventory), `scripts/inject_family_header.py` (header router),
  `scripts/scan_skill_security.py` (security triage)
- **Templates:** `assets/family-umbrella-template.md`, `assets/skill-finder-template.md`,
  `assets/skill-register-template.md`, `assets/config.example.json`, `assets/branch-header.example.md`

## Changelog

### 1.1.0 (2026-06-17)
- Added branch mechanism: third-party/read-only skills can be customized via a fork copy (branch)
  — with a reference to the original, date, author, and reason; the original remains untouched.
  Iron rule "Survey ≠ mutation" extended with branch escape hatch. New section
  `## Branch Mechanism`. New files: `references/skill-branching.md`, `assets/branch-header.example.md`.

### 1.0.0 (2026-06-17)
- Initial version. Unites inventory audit (family clustering, numbered decisions) and
  web research (gated install with security triage) in one installer that generates lean subskills.
