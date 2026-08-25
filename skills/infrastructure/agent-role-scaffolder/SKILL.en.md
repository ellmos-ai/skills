---
name: agent-role-scaffolder
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-25
updated: 2026-08-25
description: >
  Builds and verifies new agent roles inside the ellmos ecosystem: native
  Claude Code subagents (durable role definitions) and Companion Workers
  (SendMessage-reused instances for a ticket/task series). Formalizes
  previously informal, hands-on knowledge from building agent roles
  (ati-agent, bueroassistent, versicherungs-agent, etc.) into a reusable
  scaffold-plus-verify workflow. Use this skill when a new role needs to be
  created ("build a new agent role", "set up a subagent", "start a companion
  worker") or an existing one needs to be checked against house conventions
  ("is this agent set up correctly?").
visibility: public
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
---

# agent-role-scaffolder

<!-- FAMILY-ROUTER:Agent Orchestration START -->
> **Family Agent Orchestration — signpost:** choose/staff a model ->
> `model-strategy`; pick an orchestration pattern -> `choose-your-orchestrator`;
> swarm operations (5 base patterns + 2 modes) -> `swarm-operations`;
> decompose/delegate/accept a task -> `orchestrator`; cross-provider
> messaging/presence/locks -> `agents-bridge`; **build or verify a new role
> -> this skill (agent-role-scaffolder)**.
<!-- FAMILY-ROUTER:Agent Orchestration END -->

## Purpose

This ecosystem already has a mature family of orchestration skills
(`model-strategy`, `swarm-operations`, `orchestrator`, `choose-your-orchestrator`,
`agents-bridge`) — but none of them answers "how does a new role come into
being correctly." That is the gap `agent-role-scaffolder` fills. It does not
duplicate those skills; it **routes to them** once staffing, orchestration
patterns, or cross-provider messaging are needed.

**Origin:** user decision M5 from ticket `T-20260825-935905816` (marketplace
full survey): verdict (b) — own agent-building knowledge already existed but
was unformalized. The official Claude Code plugin `agent-sdk-dev`
(claude-plugins-official, Apache-2.0) served as the **structural model**: a
scaffolding command file plus two topic-specific verifier subagents with a
checklist and a PASS/PASS-WITH-WARNINGS/FAIL report format. What was adopted
is the **shape** (scaffold question catalogue → build → verification
checklist with a structured report), not the text and not the subject
matter — that plugin builds raw Claude Agent SDK apps (Python/TypeScript),
this skill builds **ellmos-own agent roles** (subagent definitions and
Companion Workers). The original is NOT installed; it sits read-only in the
local marketplace cache and was only read (`.PLUGINS/CLAUDE.md` rule 5: ideas
are free, wording is not). Register entry:
`.AI/.PLUGINS/PLUGIN-REGISTER.md`, status `zitiert`.

## Two build paths — both belong here

New roles in the ellmos ecosystem come into being along two structurally
different paths that must not be conflated (analogous to the model plugin's
TS/Python split — but here following the actual system boundary):

| | **Native subagent** | **Companion Worker** |
|---|---|---|
| What is created | a durable role definition (`~/.claude/agents/<name>.md`, launchable via the `Agent` tool) | an ad-hoc named, `SendMessage`-reused instance for ONE task series |
| Lifespan | durable, reusable across sessions | for the duration of a ticket/topic series, discarded afterward |
| Examples in the existing set | `ati-agent`, `bueroassistent`, `versicherungs-agent`, `gesundheitsassistent`, `persoenlicher-assistent`, `production`, `research-agent`, `reflection-agent`, `test-agent`, `entwickler-agent` | this session's own worker model (e.g. `skillcreator-bau`, `policyreg-decisions`, `workflowhooker-ausbau` — named workers inside the ticket system) |
| Lifecycle layer | Claude Code's own agent registry | **COMA** (`.MODULES/.ORCHESTRATION/coma`) — if spawned across processes, not merely tool-internal |
| Build guide here | `references/subagent-role-scaffold.md` | `references/companion-worker-scaffold.md` |

**Rule of thumb:** does the capability need its own name, reusable across
many sessions, with a fixed trigger description (e.g. "whenever it's about
tax receipts") → native subagent. Is it a bounded but coherent series of
tasks a coordinator is delegating right now (ticket chain, topic switch) →
Companion Worker.

## Workflow

1. **Choose the build path** (table above) — ask the user when in doubt,
   don't guess.
2. **Work through the scaffold questions** (see the matching
   `references/*.md`) — one at a time, mirroring the model plugin: purpose/
   trigger, tool needs (`Tools:`), model choice (→ **step 3**), coordination
   need (boss agent with experts, or a single role?).
3. **Do NOT decide the model here — delegate to `model-strategy`.**
   Score-based selection, cross-agent delegation, advisor pairing, and
   escalation triggers are already solved there; this skill only points to
   it. Established rule of thumb from the existing memory: subagents do
   **not** inherit the main model by default (see memory fact
   `feedback_subagenten_modellstaffelung`).
4. **Check the orchestration pattern** if the new role has to work with
   several others — `choose-your-orchestrator` picks the pattern,
   `swarm-operations` supplies the 5 base patterns + 2 modes, `orchestrator`
   the decompose/delegate/accept protocol.
5. **Follow team/messaging conventions**
   (`references/model-staffing-and-messaging.md`): `SendMessage` for
   cross-agent communication, claim-by-filename for ticket delegation,
   "reference instead of repeating" when assigning work (don't re-narrate
   house-wide rules in the prompt — only the task-specific parts).
6. **Verify** — work through the matching checklist in the chosen
   `references/*.md`, produce a report in the
   `PASS / PASS WITH WARNINGS / FAIL` format (structure below).
7. **Catalogue if needed** — a durable new role belongs in the appropriate
   register (`~/.claude/agents/`, possibly plugin bundling); a Companion
   Worker needs no register entry, just a clear first task handoff.

## Verification report format (for both build paths)

Structure deliberately adopted from the model plugin (shape, not wording) —
four sections, kept short:

- **Status:** PASS | PASS WITH WARNINGS | FAIL
- **Critical issues:** what makes the role unusable (no concrete trigger
  description, `Tools:` too broad/too narrow, model choice not grounded via
  `model-strategy`, no check against an existing overlapping role)
- **Warnings:** functional but suboptimal (e.g. inherited the main model
  instead of staffing it, no rotation criterion for a long-lived Companion
  Worker)
- **Passed checks + recommendations:** what fits, what to do next

## Related skills

- `model-strategy` — model choice/staffing (step 3, referenced here only).
- `swarm-operations` — swarm patterns for multi-role collaboration.
- `choose-your-orchestrator` — picks the matching orchestration pattern.
- `orchestrator` — decompose/delegate/accept protocol.
- `agents-bridge` — cross-provider messaging/presence/locks, if the new role
  must talk to Codex/Gemini/Kimi beyond Claude Code.
- `skill-explorer` — checks whether a capability already exists BEFORE a new
  role is built (duplicate avoidance).

## Changelog

### 1.0.0 (2026-08-25)
- Initial version. Built following user decision M5 (`T-20260825-935905816`)
  via `ellmos-skill-creator`. Formalizes the Companion-Worker pattern
  (primary source: `_control-center/_TICKETS/README.md`, section "Leitprinzip
  (Kontext-Ökonomie)"), the COMA lifecycle (primary source:
  `.MODULES/.ORCHESTRATION/coma/README.md`), and the observed "boss agent
  coordinates experts" pattern of existing roles. Deliberately routes to
  `model-strategy`/`swarm-operations`/`orchestrator`/`choose-your-orchestrator`/
  `agents-bridge` instead of duplicating them. Model `agent-sdk-dev`
  (claude-plugins-official) NOT installed, only read and structurally cited
  (`.PLUGINS/CLAUDE.md` rule 5).
