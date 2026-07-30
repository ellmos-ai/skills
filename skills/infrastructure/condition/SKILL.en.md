---
name: condition
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-25
updated: 2026-07-28
description: Flexible condition language for goals, prompts, and tasks. Translates conditions, timestamps, and sequence dependencies into verifiable gates so that a sub-step is executed only after verified release. Always use for /condition, /if, /if-only, /when, /after, /and, or /or as well as phrases such as "only when", "as soon as", "only if", "after", "wait until", "afterwards", or "not before". Also use when multiple sub-goals depend on each other or a goal contains a later release.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [condition, gate, prompt-language, goal, trigger, blocker, timing, dependency, workflow]
language: en
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'condition/SKILL.md', 'origin_version': '1.0.0', 'origin_repo': 'None', 'last_sync_from_origin': '2026-07-28', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="condition banner">

> **English** — Official English version of `condition`.


# condition — Condition Language for Goals and Prompts

## Core Idea

Prose conditions are easy to overlook. Therefore, translate every relevant condition into a named, verifiable gate:

> Generous when reading, unyielding when proving.

The input may be natural language and incomplete. The internal translation, however, must explicitly record:

1. which condition must be met,
2. which sub-step is blocked,
3. which tool query serves as proof,
4. whether non-fulfillment means delay or prohibition.

Block only the affected sub-step. Continue independent work.

## Language Elements

| Expression | Semantics | Example |
| --- | --- | --- |
| `/condition <Condition> -> <Step>` | Canonical gate | `/condition Tests green -> Build release` |
| `/if <Condition> -> <Step>` | Synonym for `/condition` | `/if Review complete -> Merge` |
| `/when <Condition> -> <Step>` | Execute as soon as condition occurs | `/when Export finished -> Verify report` |
| `/if-only <Condition> -> <Step>` | Only if fulfilled; otherwise do not execute at all | `/if-only Backup proven -> Delete legacy data` |
| `/after <Duration> -> <Step>` | Time offset from creation timestamp | `/after 30 minutes -> Check status` |
| `/and` | All linked conditions must hold | `/if Tests green /and Review present -> Merge` |
| `/or` | At least one condition suffices | `/if Approval present /or Emergency rule active -> Start` |

Use numbered conditions such as `/condition 1 ...` and `/condition 2 ...` when a prompt contains multiple gates. When mixing `/and` and `/or`, do not invent implicit operator precedence: use parentheses or numbered sub-conditions. If the meaning remains ambiguous, ask before releasing a risky step.

Treat `/if-only` as a prohibition. If the condition cannot be proven, do not execute the step. In case of unclear phrasing and irreversible consequences, choose the stricter interpretation.

## Workflow

### 1. Normalize Condition

Translate input into a verifiable sentence. Convert relative times upon creation into an absolute timestamp with timezone.

| Input | Normalized Condition | Proof Class |
| --- | --- | --- |
| `time 06:00` | System time is at least 06:00 in the agreed timezone | Clock/Time tool |
| `after 2 hours` | System time is at least creation time plus two hours | Clock/Time tool |
| `wenn Worker A fertig ist` | Acceptance artifact or task status of A shows completion | Task/File tool |
| `wenn Tests grün sind` | Prescribed test run completes successfully | Process/Test tool |
| `nach dem Push` | Target remote contains the expected commit | Version control tool |
| `wenn der User zustimmt` | Explicit approval exists in the conversation | User input |

If no objective proof path is recognizable, state this openly. Never formulate a gate such that it can only be closed through conjecture.

### 2. Record Gate State

If a persistent gate, task, or memory store is available, store at least these fields there:

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

An existing runtime adapter may use different command names. Functionally, it requires: `open`, `list`, `meet`, and `drop` or equivalent operations.

### 3. Reorder Work

An open gate does not block the entire task. Execute all independent steps and re-check the gate state before the next dependent step.

Do not actively poll in short agent loops. For longer waiting times, use a scheduler, background job, or event that reports once upon occurrence. After the wakeup signal, still verify the actual condition again using the designated tool.

### 4. Rigorously Verify and Close

First execute the tool query, then close the gate with concrete evidence. Suitable proofs include, for example:

- Time: measured timestamp with timezone,
- File: path, metadata, or hash of expected artifact,
- Tests: executed command, exit code, and relevant summary,
- Repository: branch, commit ID, and remote comparison,
- Process or Task: stable ID and measured final status,
- Approval: unambiguous user answer in current context.

An estimate, an expected state, or the mere assertion of another worker is not sufficient when an independent proof should be available.

If a gate becomes obsolete due to a task change, mark it as `dropped` with justification. For `/or`, also close or drop the no longer needed alternatives so no zombie gates remain.

### 5. Escalate

When all independent steps are completed:

1. check whether the blocking preliminary work can be actively completed within the task,
2. for pure wait conditions, use a suitable scheduler or background job,
3. for user decisions or external dependencies, hand over with an open gate and clear intermediate status.

Do not derive additional authorization from a condition. A fulfilled gate only changes the sequence; it does not expand the authorized scope of the task.

## Example & Application

### Goal with Time Condition

```text
Ziel: Daten prüfen und Bericht veröffentlichen.
/condition time 16:00 Europe/Berlin -> Veröffentlichung starten
```

Data verification may take place beforehand. Publishing remains blocked until a current time query proves at least 16:00.

### Prompt with Multiple Conditions

```text
/condition 1 Tests erfolgreich
/condition 2 Review freigegeben
/if condition 1 /and condition 2 -> mergen
```

Verify both gates separately. Only merge afterwards.

### Prohibition Instead of Delay

```text
/if-only verifiziertes Backup vorhanden -> alte Dateien löschen
```

Without a proven backup, delete nothing and state the open prohibition in the final report.

## Pitfalls

- Repeating the condition only in prose text instead of tracking it as a state.
- Pausing an entire goal even though only a single sub-step is blocked.
- Saving relative time without creation timestamp and timezone.
- Replacing tool proof with assumption or self-reporting.
- Treating `/if-only` like a mere wait condition.
- Leaving unneeded alternative gates open after `/or`.
- Hardcoding vendor, model, user, or host names into the general mechanics.
- Treating a local runtime path as a requirement for the language itself.

## Changelog

### 1.1.0 (2026-07-28)

- Formulated vendor-, user-, and system-neutral for shared skill runtimes.
- Made usage in goals and prompts explicit.
- Described runtime as an interchangeable adapter; removed fixed local paths and model names.
- Clarified ambiguous `/and`/`/or` links, persistent states, and authorization boundaries.

### 1.0.0 (2026-07-25)

- Initial version with `/condition`, `/if`, `/if-only`, `/when`, `/after`, `/and`, and `/or`.