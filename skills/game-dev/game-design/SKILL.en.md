---
name: game-design
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: >
  How game development works as a process — roles, subtasks, workflows and role
  descriptions, especially (but not only) for Roblox. Use this skill when it's about the
  ORGANIZATION of game dev rather than concrete code: Which roles exist (Creative Director,
  Engineer, Artist, Polish/Audio, Business, QA-Tester, Game Critic)? Who does which subtask?
  What does a development chain (concept → backend → frontend → polish → test) look like? How do you write
  a Game Design Document / KONZEPT.md? How do several (AI) agents divide up a game?
  Also trigger on "plan a new game", "create Game Design Document", "which roles do I need
  for my game", "development workflow for a game", "who tests the game", "structure a game idea",
  "Roblox genre/monetization".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: game-dev
tags: [game-design, roblox, rollen, workflow, gdd, konzept, monetarisierung, qa, gamedev]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/game-design/"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Game Design — Roles, Subtasks & Workflows

## Purpose

Game development is teamwork made of clearly separated disciplines — even when a single person
or one AI agent takes on several of them. This skill provides the **organizational model**:
which roles exist, which subtasks belong to them, in what order they interact
and how to capture a game as a concept (GDD). For the *technical* how, see `/rojo` (sync),
`/rbx-studio` (editor/assets) and the meta-skill `/rbx-dev` (architecture).

Use this skill when planning a new game, when dividing up the work (also across
several AI agents) and when writing/reviewing a Game Design Document.

## The Roles (5 development + 2 test)

A proven, compact role distribution. Full descriptions with all subtasks:
[`references/roles-and-workflows.md`](references/roles-and-workflows.md).

| Role | Focus | Core subtasks |
| --- | --- | --- |
| **Creative Director** | WHAT & WHY & for WHOM | GDD/KONZEPT, design & balance mechanics, prioritization/sprints, story, UX flow |
| **Engineer** | HOW (technical) | Server/client/shared code, game loop, networking/remotes, DevOps (Rojo, build), bugfixing |
| **Artist** | how the world looks | World/level building, lighting & atmosphere, particles, asset sourcing (incl. malware check) |
| **Polish / Audio** | how it feels & sounds | SFX/music/ambient, animations, UI/UX fine-tuning, "juice" (screen shake, hit-stop), feedback |
| **Business** | outward-facing | Store page, icon/thumbnail, monetization (gamepass/products/pass), analytics, community |
| **QA-Tester** | technically correct? | Bug scans in code, playtests + check console, reproducible reports, regression, performance |
| **Game Critic** | is it fun? | First/long impression from the player's view, honest assessment (fun, clarity, fairness), suggestions |

**Basic rule:** Development and testing are **separate** roles — ideally separate people
or agents. Whoever writes code does not test it objectively. The Game Critic may be tough.

## Workflows (development chains)

Work flows as a chain from role to role. The most important patterns:

**Standard feature chain:**
```
Creative Director (plans feature) → Engineer (backend) → Artist (frontend/assets)
→ Polish/Audio (sound + fine-tuning) → QA-Tester (technical test)
→ Game Critic (player perspective) → Creative Director (feedback → next iteration)
```

**Quick-fix chain:** QA-Tester (bug) → Engineer (fix) → QA-Tester (verifies).

**Asset chain:** Artist (store search) → Artist (malware scan) → Artist (integrate) → QA (visual).

**Polish chain:** Game Critic (weakness) → Polish/Audio → Artist → Game Critic (re-check).

**Human-in-the-loop:** [agent chain] → human tester → Creative Director (feedback) → [chain].

Each iteration should leave a short changelog. Stop condition: time budget reached
**or** quality goal met.

### Persona-based testing

A game only survives if very different players can cope with it. Therefore test (also
simulated by agents) from several **personas** instead of only from your own perspective — varied
by age, experience, platform (PC/mobile/tablet/console), attention span, language and
accessibility. Examples: a 9-year-old casual kid on a tablet who only wants to press buttons; a
12-year-old core player on PC who looks for the meta; a 60+ beginner who needs big buttons.
Persona tests should run **blind** (the tester does not know the design intent).

## Game Design Document (KONZEPT.md)

Capture every game in a concise GDD — template:
[`assets/KONZEPT_template.md`](assets/KONZEPT_template.md). Minimum structure:

- **Vision** — 1–2 sentences: What is the game?
- **Genre / reference** — classification + reference titles.
- **Core mechanics** — **max. 3–4** (focus forces quality).
- **Gameplay loop** — the player's minute-by-minute loop.
- **Game modes / time formats** — if relevant.
- **Monetization** — gamepasses, developer products, battle pass, shop.
- **Tech** — stack (Rojo/frameworks), rough architecture.
- **Next steps** — implementation checklist.
- **Known bugs / open issues**.

## Multi-agent division of labor

Several AI agents (or human+AI) can divide up a game — two modes:

- **Swarm** — same task, different areas (e.g. three agents each balance one system).
- **Team** — different roles, coordinated with each other (Engineer + Artist + Polish in parallel on
  one feature, coordinated by the Creative Director).

Proven in practice: **never** give development and testing to the same agent; fix role prompts per role
(system prompt = role description); each chain iteration ends with a changelog +
test report; the human remains the quality gate.

## Roblox-specific market context (orientation)

Platform knowledge that grounds the concept work for Roblox (no guarantee, just rules of thumb):

- **Profitable genres:** Simulator, RPG, Tycoon, Horror, Obby — very different scaling
  and effort.
- **Underserved niches (higher risk, less competition):** real strategy/RTS-lite,
  high-quality sports games, cozy/life sim, co-op puzzle/escape, auto-battler.
- **Golden monetization rules:** (1) LiveOps is mandatory (updates every 2–4 weeks),
  (2) monetization should *support* gameplay, not block it, (3) social design (trading,
  co-op) is infrastructure, (4) mobile-first (50%+ play on phones), (5) content-creator
  suitability (YouTube/TikTok) is marketing.

> For current, reliable market figures, research instead of estimating — the points above are
> stable heuristics, not live data.

## Further reading

- Sister skills: `/rojo`, `/rbx-studio`; meta-skill `/rbx-dev` (architecture patterns,
  project structure, Luau lessons).
- Reference pipeline (if available): `<your Roblox project pipeline>` (`AGENT_ROLES.md`, `GUIDE.md`,
  `IDEAS.md`, market analyses).

## Changelog

### 1.0.0 (2026-06-17)
- Initial version. Generic role/workflow framework, distilled from `.ROBLOX/AGENT_ROLES.md`
  & `GUIDE.md`, user-neutral (without project-specific portfolio).
