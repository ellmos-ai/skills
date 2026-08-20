---
name: choose-your-orchestrator
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-08-20
updated: 2026-08-20
description: >
  Selects a suitable, bounded orchestration together with the user before complex
  multi-agent work and produces a compact session contract. Use for
  /choose-your-orchestrator, when the combination of orchestrator, swarm, model
  routing, or an authorized preference model is unclear, and before agent programs
  that must explicitly define model slots, parallelism, spawn depth, write
  boundaries, acceptance, and escalation.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [orchestration, multi-agent, delegation, routing, budget, matryoshka, session-contract]
aliases: [choose-your-orchestrator]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: [orchestrator, swarm-operations, model-strategy, decision-avatar]
  python: []

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: github.com/ellmos-ai/skills
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Choose Your Orchestrator

## Purpose

Clarify the constraints before complex multi-agent work, recommend the smallest
effective combination of existing skills, and emit a binding session orchestration
contract. Load the selected skills through the current runtime's skill mechanism and
follow their live instructions. Do not copy their procedures into this skill.

Delegation never expands authority. External or irreversible actions such as
publishing, sending, deleting, paying, or production changes remain user-gated unless
the current request explicitly authorizes them.

## Building blocks

| Building block | Job in the contract | Not its job |
|---|---|---|
| `orchestrator` | Work packages, scopes, evidence, and acceptance | Inventing model choices or swarm patterns |
| `swarm-operations` | Swarm patterns, cost gate, and optional matryoshka tiers | Artificially parallelizing a single task |
| `model-strategy` | Capability- and model-based routing from live availability | Prescribing fixed model versions or permissions |
| `clutch` | Optional external routing suggestion | Sole authority for dispatch or scope |
| `decision-avatar` | Optional authorized preference signal for reversible uncertainty | Replacing user approval or expanding authority |

Use `clutch route "<short task description>" --json` only when `clutch` is
actually available. Treat the JSON response as a suggestion and reconcile it with
available runtime slots, budget, project rules, and user boundaries. If `clutch` is
unavailable or its output is unreadable, use `model-strategy` and the runtime's live
capabilities. Do not hardcode current model names or versions into the contract.

## Recommendation dialogue

### 1. Classify the task

Identify the goal, task type, success criteria, negative scopes, current authority,
existing locks, and independent work packages. Start with the smallest suitable route
from the table below.

### 2. Propose the contract

Show a compact draft covering:

1. building blocks and roles,
2. model and budget slots,
3. maximum parallelism and spawn depth,
4. write boundaries and locks,
5. acceptance and evidence,
6. escalation and user questions,
7. the authority boundary.

Recommend concrete values and state the main trade-off in one sentence. Ask only for
decisions that materially change the result. Bundle open questions into no more than
three clearly separated groups and put the recommended option first. Do not ask again
when every dimension is already explicit.

### 3. Confirm or reduce

Do not begin multi-agent dispatch while a material budget, write, or authority question
is unresolved. If only the value of parallelism is unclear, reduce to a single run. An
explicitly authorized request may start with the safe defaults when no material user
decision is missing.

### 4. Emit the contract

Emit the confirmed contract in chat. If a `usmc` command is available, inspect its
help first and add a privacy-neutral session note through a documented note/write
command. Do not invent a subcommand or store raw prompts, secrets, or private content.
Without an available USMC write path, the chat contract is authoritative.

## Routing table

| Task type | Recommendation | Default shape |
|---|---|---|
| Audit / sweep | `orchestrator` + `swarm-operations`; `model-strategy` for different capability classes | independent areas, a small `parallel-chunks` or `specialist` group, central merge |
| Build program | `orchestrator` + `model-strategy`; swarm only for genuinely independent tracks | chief plans and accepts, workers build in disjoint areas |
| Single build | single run; optional `model-strategy` or `clutch` for routing | no swarm or hierarchy overhead |
| Ticket operation | the ticket system remains authoritative; `orchestrator` adds work contracts and evidence | do not replace the existing router/score regime; respect the ticket lifecycle |

## Safe defaults

Use these values unless the user, runtime, or project rules are stricter:

- at most two active workers; start with one and demonstrate the value of the second,
- matryoshka off and maximum spawn depth `0`,
- no worker-created subagents without explicit approval,
- one writer per repository or clearly separated area,
- disjoint file claims and project-standard locks before every write,
- the chief/orchestrator independently checks artifacts, diffs, and tests,
- completion claims count only after evidence acceptance,
- irreversible or external actions remain user-gated,
- bundle uncertainty instead of raising many individual interruptions.

Enable matryoshka only when the user explicitly confirms it and the contract states,
for each tier, the model/capability class, active slot limit, permitted subtasks, and
maximum depth. Count active agents, not merely retained ones. One writer per area still
applies.

## Contract format

```text
SESSION ORCHESTRATION CONTRACT
Goal and type: <outcome; audit/build program/single build/ticket operation>
Building blocks: <loaded skills and optional routers>
Chief: <planning, reasoning, integration, evidence acceptance>
Worker slots: <role/capability class per slot; budget limit>
Parallelism: <maximum active>; spawn depth: <0..N>; matryoshka: <off/on>
Write boundaries: <one writer per area; claims; locks; negative scopes>
Acceptance: <artifacts, tests, diffs, sources; who verifies>
Escalation: <stops; no more than three bundled user questions>
Authority: <permitted actions; external/irreversible actions user-gated>
Persistence: <chat authoritative; USMC note yes/no and privacy-neutral>
```

## Example

```text
Request: Review three independent components and integrate one fix.
Recommendation: orchestrator + swarm-operations; two active read-only reviewers,
then exactly one integration writer. Matryoshka off, depth 0. The chief verifies
findings, diff, and full tests. Push or publication only within explicitly authorized
scope.
Open question: Is the second parallel review lane worth the added consumption?
Recommendation: yes, because the components are independent.
```

## Stop conditions

Stop or reduce the orchestration when scopes overlap, locks are unclear, the runtime
does not offer the recommended slot, the budget is unconfirmed, or acceptance cannot be
independently evidenced. Ask the user instead of guessing a new product, privacy, or
authority decision.

## Changelog

### 1.0.0 (2026-08-20)
- Added the recommendation dialogue, routing table, and compact session contract.
- Established safe defaults for parallelism, matryoshka, write boundaries, evidence,
  and external actions.
- Documented optional `clutch` and an authorized preference model without fixed model binding or
  authority expansion.
