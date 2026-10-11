---
name: orchestrator
version: 1.4.0
type: protocol
author: Claude + Codex
created: 2026-06-17
updated: 2026-10-11
description: Provider-neutral protocol for breaking down complex tasks, commissioning independent workers, and evidence-based verification of their results.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [orchestrierung, multi-agent, delegation, evidenz, checkpoint, workflow]
language: en
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'local-agent-skills/orchestrator/', 'origin_version': '1.0.0', 'origin_repo': 'None', 'last_sync_from_origin': '2026-07-28', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="orchestrator banner">

> **English** — Official English version of `orchestrator`.


# Orchestrator (English)

## Overview & Purpose

Use this skill when a task consists of at least two largely independent work packages and delegation provides a real time, context, or quality advantage. For small, tightly coupled tasks, work directly.

The skill describes a protocol. The actual starting, pausing, and resuming of workers occurs via the capabilities of the respective runtime.

## Authority Limit

Delegation does not expand authorization. Every worker receives at most the scope and modification rights that already apply to the main task. External, irreversible, or otherwise approval-requiring actions remain subject to approval.

## Operator Regime: Think and Delegate, Never Execute Yourself

This regime applies when the user asks for it or the `burst` profile
(`operating_mode: orchestrator`) is active. The operator, i.e. the instance that
breaks down, commissions, and verifies work, then follows these rules:

- **Principle.** The operator is the expensive thinking model. It designs,
  decides, verifies, and integrates; every execution goes to a worker: file
  edits, screenshots, renderings, commits, pushes, research, measurement series,
  creating image or media assets, even mini-edits. The operator itself only
  maintains its own memory and handoff state, makes single-call measurements
  (time, process list, existence of a file), and reopens a file for the user
  when a worker failed at it.
- **Set the model per worker explicitly.** A cheaper model for mechanics
  (building to a clear spec, committing, readback, rework), a stronger one for
  larger build jobs and for second-model reviews. Never spawn without a model
  setting, otherwise the worker inherits the operator's model.
- **The brief contains only what the rule files cannot know:** measured baseline
  values, decisions made in the conversation (quote the user's instructions
  verbatim), scope limits, abort conditions, the name of the lock file for the
  sub-area (never the project-wide lock for partial changes, never touch a
  user lock), review paths, commit trailers, and a cap on the report length
  (e.g. 2 to 6 lines). Pass on the reasons so the worker can hit the intent when
  the letter does not fit.
- **Review before commit for anything the user judges** (graphics, texts,
  layouts): the worker saves the result as a review file (check full paths
  first), opens it in the user's default application, reports, and waits. The
  commit follows only after the approval, which the operator relays verbatim.
  For iterations always use new file names (a, b, c ...), never overwrite.
- **Workers wait actively, not idle.** For serial resources (a tool that allows
  only one run at a time), chain on the predecessor's output file or poll in
  the foreground in bounded calls; never hope for a notification that may not
  arrive. On a collision, end your own run and queue behind.
- **Never discard foreign changes in the working directory:** secure them on a
  rescue branch, read them line by line, then certify or archive them.
  Security-relevant code is not merged by a worker but reported; a model other
  than the author reviews it.
- **Results count only with a readback at the destination,** not at the place
  of creation (e.g. an API response with size or checksum; for animations two
  time-shifted captures with a measurable difference; for private sources a
  parser or API proof instead of a browser picture).
- **The operator collects the leftovers:** file open points with context and
  next step, measure times instead of guessing, secure insights in the memory
  system. Report only decisions and results to the user; do not pass on the
  workers' idle confirmations.
- **Why:** The thinking model is too expensive for execution, and executing
  operators overlook readbacks. An operator that does not have the destination
  checked reports successes that never arrived there.

## Process

### 1. Assess the Situation

1. Record the objective, success criteria, and exclusions of the main task.
2. Check project rules, locks, ongoing changes, and available budgets.
3. Before dispatch, secure the current lock, status, and diff state of the affected areas as a baseline. Only in this way can existing external changes be reliably distinguished from worker changes later.
4. Only parallelize work packages that are sufficiently independent.
5. Separate overlapping write areas or process them sequentially.

### 2. Write Contract

Before each dispatch, create a brief, verifiable contract:

| Field | Required Content |
|---|---|
| ID | stable ID of the work package |
| Objective | exactly one concrete result |
| Inputs | relevant files, data, or context sources |
| Positive scope | what may be read or modified |
| Negative scope | what remains explicitly untouched |
| Success criterion | observable condition for "done" |
| Evidence | expected proof, such as a test, diff, or reference |
| Return format | compact, structured completion message |

A worker receives only the context needed for this contract.

### 3. Execute and Observe

- Keep fan-out small and only increase it when there is independent benefit.
- Track progress via runtime status or a standard project checkpoint.
- In case of conflicts, scope expansion, or lack of authority, stop and escalate.
- A failed worker must not automatically block independent work packages.

### 4. Verify Results

A completion message is initially a claim. The orchestrator verifies itself:

1. Does the claimed artifact or named change exist?
2. Does it belong to the agreed scope?
3. Does the agreed test or proof currently pass?
4. Were external changes, locks, and negative scopes respected?
5. Do results from different workers contradict each other?

Only then is a work package considered complete.

### 5. Integrate and Secure

- Resolve conflicts consciously; do not blindly append results.
- Re-run necessary overall tests after integration.
- Clearly designate open, failed, and deferred packages.
- For longer runs, save objective, status, evidence, and next step in a recoverable checkpoint.

## Minimal Worker Prompt

```text
Auftrag: <Kennung und Ziel>
Eingaben: <Quellen>
Du darfst: <positiver Scope>
Du darfst nicht: <negativer Scope>
Fertig, wenn: <prüfbares Kriterium>
Belege mit: <Test, Diff oder Fundstelle>
Antworte als: <Rückgabeformat>
```

## Stop Conditions

Stop only the affected work package if its scope, authority, or evidence becomes unclear. Independent, safe packages may continue running.

Stop the entire delegation if:

- the subtasks are no longer independent,
- a shared write area cannot be safely separated,
- rules, locks, or authority for the entire remaining scope are unclear,
- the expected costs exceed the discernible benefit,
- the required evidence cannot be generated or verified.

## Changelog

### 1.4.0 (2026-10-11)
- Added the section "Operator Regime: Think and Delegate, Never Execute
  Yourself": the operator thinks, decides, verifies, and integrates; every
  execution (even mini-edits) goes to workers. Covers model choice per worker,
  brief content (only what cannot be looked up), review before commit for
  user-judged results, active waiting on serial resources, handling of foreign
  changes, the readback duty at the destination, and collecting leftovers.
  Applies on the user's request or in the `burst` profile.
- English text brought to this version for that section only; the resource
  profile sections of 1.2.0 and 1.3.x exist only in the German `SKILL.md`.
- No change to process steps 1-5, authority limit, or stop conditions.

### 1.1.0 (2026-07-28)
- Removed user, path, model, and provider bindings.
- Elaborated contract, authority limit, evidence verification, and checkpoints as portable core mechanics.
- Explicitly separated baseline for external changes as well as package-local and global stops.

### 1.0.0 (2026-06-17)
- Initial local version.