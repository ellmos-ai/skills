---
name: skill-finder
version: 0.7.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-08-20
description: >
  Active finder/router for own local skills (analogue to using-superpowers). ALWAYS use at the start
  of a non-trivial task to check whether a user skill fits, and route to the correct skill. Activates on
  "which skill fits", "is there a skill for this", "find skill", or generally before tasks that a local
  skill can solve better than ad-hoc work.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, finder, routing, discovery, meta]
language: en
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

<img src="banner.png" width="100%" alt="skill-finder banner">
# Skill Finder

## The Rule

Before starting any non-trivial task, first check if a local skill handles it better. Even with minor suspicion, load the appropriate skill and **follow its live instructions** (read file, do not work from memory). If no skill applies, proceed as normal.

## Family Routing

<!-- Generated/updated from SKILL-MAP.md + inventory_skills.py. Topic -> Family -> Skill.
     Maintenance: Sub-skill skill-family-care or new skill-explorer audit run. As of: 2026-06-17 -->

| Topic / Intent | Family | Skill(s) |
|-----------------|---------|----------|
| Think through / analyze a problem | Thinking Tools | `/structured-thinking` (guides `/think` → `/brainstorm` → `/decide`) |
| New ideas / creativity | Thinking Tools | `/brainstorm` (vs `/think` analysis, `/decide` selection) |
| Decision stack | Thinking Tools | `/decision-briefing` |
| Build or use an authorized user preference model | Multi-Agent | `build-your-users-mind` (build) · `decision-avatar` (runtime) |
| Bug / test failure | Coding & Debugging | `/bugfix-protocol` (1 bug), `/bugsweep` (many, before release) |
| New/existing project or pipeline | Project/Pipeline | `/projekt-pipeline-umbrella` (→ bootstrapper/onboarding/optimizer) |
| Roblox game | Game Dev | `/roblox-dev` (→ `/rojo`, `/roblox-studio`, `/game-design`) |
| Therapy / counseling / crisis | Therapy | `/therapie-umbrella` (→ stabilization/guideline/counseling) |
| Presentation / slides | Office | `/academic-pptx` (content) + `/pptx` (file) |
| Bound orchestration together before complex multi-agent work | Multi-Agent | `choose-your-orchestrator` (`/choose-your-orchestrator`) |
| Execute confirmed multi-agent coordination | Multi-Agent | `orchestrator`, `/swarm-operations`, `/model-strategy` |
| Application / self-management | Personal | `/bewerbungsexperte`, `/selbstmanagement` |
| Compare/clean up/find skills | System/Meta | `skill-explorer` (audit/explore), `code-skill-index` (list) |
| Set up system / sync MCP / connect agents | System/Meta | `/system-onboarding`, `/mcp-config-sync`, `/agents-bridge` |
| File utilities | Utilities | `/document-chunker`, `/migrate-rename`, `/plugin-system` |
| Chat history → preserve as skill | System/Meta | `skill-extractor` (`/skill-extract`) |
| Chat history/external automation → automation | System/Meta | `workflow-extract` (`/automations-extract`) |
| Recurring check across many projects | Coding & Debugging | `rotation-check` (registry/log structure) |
| Stuck problem, mine ideas | Thinking Tools | `idea-mining` (vs `/brainstorm` = free/broad) |
| Keep DE/EN document versions in sync | Utilities | `bilingual-doc-sync` |
| AI traces/chat remnants in text, AI disclosure | Utilities | `llm-text-hygiene` |
| Condition/timing/order in request ("only when", "from 6 am", "as soon as X done") | Process | `condition` (`/if` · `/when` · `/if-only` · `/after` · `/and` · `/or`) |

Full list: Skill `code-skill-index`.

## Red Flags (Rationalizations that mean STOP)

| Thought | Reality |
|---------|----------|
| "This is just a quick question." | Questions are tasks — check skills first. |
| "I know the concept." | Knowing concept ≠ using skill. Read live file. |
| "The skill is overkill." | Simple things get complex — use it. |
| "I'll explore on my own first." | Skills tell HOW to explore. Check first. |

## Maintenance

Update routing table when families change (sub-skill `skill-family-care` or new `inventory_skills.py` run from `skill-explorer`).

## Changelog

### 0.7.0 (2026-08-20)
- Added `choose-your-orchestrator` as the recommendation and contract dialogue before
  complex multi-agent work; separated it from execution routing to `orchestrator`,
  `swarm-operations`, and `model-strategy`.

### 0.2.0 (2026-07-03)
- Added routing lines for new skills: skill-extractor, workflow-extract, rotation-check, idea-mining, bilingual-doc-sync (Codex automations extraction).

### 0.1.0 (2026-06-17)
- Initial version. Created by audit mode ([F]) as an analogue to using-superpowers. Routing table from audit dated 2026-06-17 (10 user families).
