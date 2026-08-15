---
name: condition
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-25
updated: 2026-07-30
description: >
  Flexible condition language for goals, prompts, and tasks. Translates conditions,
timestamps, and sequence dependencies into verifiable gates so that a sub-step is only
executed after proven approval. Always use for /condition, /if, /if-only,
/when, /after, /and, or /or as well as for phrases like "only when", "as soon as",
"only if", "after", "wait until", "then", or "not before". Also use when multiple sub-goals
depend on each other or a goal contains a later release step.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [condition, gate, prompt-language, goal, trigger, blocker, timing, dependency, workflow]
language: en
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: "condition/SKILL.md"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-07-28"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

<img src="banner.png" width="100%" alt="condition banner">

# condition — Condition Language for Goals and Prompts

## Core Concept

Continuous text conditions are easily overlooked. Therefore, translate every relevant condition into a named, verifiable gate:

> Generous in reading, relentless in proving.

The input may be natural language and incomplete. The internal translation, however, must explicitly specify:

1. which condition must be met,
2. which sub-step is blocked,
3. which tool query serves as proof,
4. whether non-fulfillment means delay or prohibition.

Lock only the affected sub-step. Continue independent work.

## Language Building Blocks

| Expression | Semantics | Example |
| --- | --- | --- |
| `/condition <Condition> -> <Step>` | Canonical gate | `/condition Tests green -> Build release` |
| `/if <Condition> -> <Step>` | Synonym for `/condition` | `/if Review completed -> merge` |
| `/when <Condition> -> <Step>` | Execute as soon as condition occurs | `/when Export done -> Check report` |
| `/if-only <Condition> -> <Step>` | Only when fulfilled; otherwise do not execute at all | `/if-only Backup proven -> Delete legacy data` |
| `/after <Duration> -> <Step>` | Time offset from set time | `/after 30 minutes -> Check status` |
| `/and` | All linked conditions must apply | `/if Tests green /and Review present -> merge` |
| `/or` | At least one condition suffices | `/if Approval present /or Emergency rule active -> start` |

Use numbered conditions like `/condition 1 ...` and `/condition 2 ...` when a prompt contains multiple gates. When mixing `/and` and `/or`, do not invent implicit operator precedence: use parentheses or numbered sub-conditions. If the meaning remains ambiguous, ask for clarification before releasing a risky step.

Treat `/if-only` as a prohibition. If the condition cannot be proven, do not execute the step. In case of unclear wording and irreversible consequences, choose the stricter interpretation.

## Process

### 1. Normalize Condition

Translate input into a verifiable statement. When setting relative times, convert them to an absolute timestamp with timezone.

| Input | Normalized Condition | Proof Class |
| --- | --- | --- |
| `time 06:00` | System time is at least 06:00 in agreed timezone | Clock/Time tool |
| `after 2 hours` | System time is at least set time plus two hours | Clock/Time tool |
| `when Worker A is finished` | Acceptance artifact or task status of A shows completion | Task/File tool |
| `when tests are green` | Prescribed test run ends successfully | Process/Test tool |
| `after the push` | Target remote contains intended commit | Version control tool |
| `when user agrees` | Explicit agreement is present in conversation | User input |

If no objective proof method is discernible, state this openly. Never formulate a gate such that it can only be closed by assumption.

### 2. Record Gate State

If a persistent gate, task, or memory store is available, save at least these fields:

```text
id
condition
blocks
mode = wait | only
proof_method
status = open | met | dropped
created_at
evidence
```

If no persistent store exists, keep the state visibly in the current goal, task plan, or handover document. Only claim that a gate survives sessions if the storage used is actually persistent.

An existing runtime adapter may use different command names. Functionally it needs: `open`, `list`, `meet`, and `drop` or equivalent operations.

### 3. Reorder Work

An open gate does not block the entire order. Execute all independent steps and recheck the gate state before the next dependent step.

Do not poll actively in short agent loops. For longer wait times, use a scheduler, background job, or event that reports once upon occurrence. After the wakeup signal, re-verify the actual condition using the designated tool.

### 4. Strictly Verify and Close

First execute tool query, then close gate with concrete evidence. Suitable proof includes:

- Time: measured timestamp with timezone,
- File: path, metadata, or hash of expected artifact,
- Tests: executed command, exit code, and relevant summary,
- Repository: branch, commit ID, and remote check,
- Process or Task: stable ID and measured final status,
- Agreement: unambiguous user response in current context.

An estimate, expected state, or mere assertion by another worker is insufficient when independent proof should be available.

If a gate becomes obsolete due to order changes, mark it as `dropped` with justification. For `/or`, close or drop unneeded alternatives as well to prevent zombie gates.

### 5. Escalate

When all independent steps are completed:

1. check whether blocking prerequisite work can be actively performed within the task,
2. for pure wait conditions, use a suitable scheduler or background job,
3. for user decisions or external dependencies, hand over with an open gate and clear intermediate status.

Do not derive additional authorization from a condition. A fulfilled gate only changes sequence; it does not expand authorized scope.

## Examples

### Goal with Time Condition

```text
Ziel: Daten prüfen und Bericht veröffentlichen.
/condition time 16:00 Europe/Berlin -> Veröffentlichung starten
```

Data verification may take place beforehand. Publication remains locked until a current time query proves at least 16:00.

### Prompt with Multiple Conditions

```text
/condition 1 Tests erfolgreich
/condition 2 Review freigegeben
/if condition 1 /and condition 2 -> mergen
```

Prove both gates separately. Merge only afterwards.

### Prohibition Instead of Delay

```text
/if-only verifiziertes Backup vorhanden -> alte Dateien löschen
```

Without proven backup, delete nothing and state the open prohibition in the final report.

## Pitfalls

- Repeating condition only in continuous text instead of maintaining it as state.
- Pausing an entire goal even though only a sub-step is blocked.
- Saving relative time without set timestamp and timezone.
- Replacing tool proof with assumption or self-assessment.
- Treating `/if-only` as mere waiting.
- Leaving unneeded alternative gates open after `/or`.
- Hardcoding provider, model, user, or host names into general mechanics.
- Treating a local runtime path as a requirement for the language itself.

## Changelog

### 1.1.0 (2026-07-28)

- Formulated provider-, user-, and system-neutral for shared skill runtimes.
- Made usage in goals and prompts explicit.
- Described runtime as an interchangeable adapter; removed fixed local paths and model names.
- Clarified ambiguous `/and`/`/or` links, persistent states, and authorization limits.

### 1.0.0 (2026-07-25)

- Initial version with `/condition`, `/if`, `/if-only`, `/when`, `/after`, `/and`, and `/or`.
