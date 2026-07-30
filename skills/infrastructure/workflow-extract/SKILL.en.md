---
language: en
---

> **English** — Official English version of `workflow-extract`.

<img src="banner.png" width="100%" alt="workflow-extract banner">

# Workflow-Extract — Building Automations from Chat Histories and External Automations

## Overview & Purpose

Some workflows do not belong in an on-demand skill loaded as needed, but rather in an **automation that runs on its own**: nightly checks, rotating project audits, periodic maintenance runs. This skill extracts such workflows from two types of sources — chat histories (where a workflow was interactively developed and should henceforth run unattended) and existing automation prompts from other systems (e.g., Codex-Automations, Scheduled Tasks, n8n flows) — and transforms them into user-neutral, robust automation prompts or skills.

The key difference from an interactive workflow: An automation has **no user present to make corrections**. Everything that the user caught during an interactive session must be caught by the automation itself. This is precisely what the building blocks in `automation-bausteine.md` are designed for.

## Workflow

### 1. Clarify Source and Target Form

| Source | Typical Case |
| --- | --- |
| Current Session / Transcript | Workflow was interactively developed and should continue running periodically |
| External Automation (Prompt file, Cron task, n8n flow) | Porting/abstraction to another system or into the library |

Target forms (one or more):

- **Automation Prompt:** Self-contained, user-neutral prompt text usable in any scheduler (Codex-Automations, Claude `/schedule`/Cron, Scheduled Task, n8n).
- **Workflow Skill:** A library skill describing the workflow, which is then called/parameterized by the automation prompt (preferred when the same workflow applies to multiple pipelines/systems — single source of truth).
- **Command:** A thin slash command for manual trigger of the same workflow.

### 2. Extract Workflow Core

Extract from the source:

- **Core Task:** What is being checked/maintained/generated? (one sentence)
- **Selection Logic:** What is the task applied to — a fixed target or rotation across a set (one project per run)?
- **Preconditions:** What must be read/checked prior to work (root documents, registries, locks)?
- **Documentation Duties:** Where are results, logs, and follow-up tasks written?
- **Abort Paths:** When does the run end read-only ("nothing to do" is a valid result)?

For chat histories, additionally evaluate correction loops (see `../skill-extractor/transcript-quellen.md`): Every user correction is a candidate for a guard that the automation will need on its own in the future.

### 3. Neutralize

Follow the rules in `../skill-extractor/neutralisierung.md`: Separate mechanics from configuration, move paths/hosts/project names into a configuration block. Automation prompts need a configuration block especially urgently because they are copied verbatim into schedulers — concrete values belong in ONE place at the start of the prompt.

### 4. Add Automation Building Blocks

Hold the extracted core against the checklist in `automation-bausteine.md` and add missing building blocks — especially rotation selection with check registry, idempotency, log hygiene, lock respect, read-only exit, and summary report. A workflow without these building blocks works in testing but degrades during continuous operation (duplicate checks, growing logs, collisions with parallel agents).

### 5. Set Cadence and Budget

- **Couple frequency to rate of change:** A check does not need to run more often than its target changes. Rule of thumb from mature automation fleets: Many initially hourly checks were reduced to daily/weekly — with rotation selection, even a low cadence covers the entire pipeline.
- **Nightly window for heavy tasks**, short read-only checks may run more frequently.
- **Cost awareness:** Every run costs tokens/compute; a run that mostly ends read-only should determine this early (read registry BEFORE expensive analysis).

### 6. Test and Deploy

1. **Dry Run:** Execute the finished prompt once interactively (as if acting as the scheduler) and verify: Does it exit cleanly? Does it write registry/log correctly? Does it stay in scope?
2. **Edge Case Test:** Simulate a run where there is nothing to do — it must end read-only with a short log entry, rather than "inventing work".
3. **Deploy:** Enter into target scheduler; if in skill form, also place in library and deploy.
4. **Monitor Error Paths:** Check log/registry after the first 2–3 actual runs — automations most frequently fail due to path drift (target was moved) and growing log files.

## Fleet Audit Mode: Auditing a Running Automation Fleet

For "audit my automations": do not extract, but help operate the EXISTING inventory. Systematically inspect via the target system's automation source (prompt/config files, schedules, run logs/memories):

1. **Silent-Failure / No-op Detection:** Is the automation running but no longer doing anything? (Read run memories/logs of recent runs: only idle runs, errors, dead paths?)
2. **Redundancy + Return:** Do automations overlap in scope? Is the return (output, resolved findings) still proportional to consumption (tokens, runs)?
3. **Drift:** Do prompt paths, conventions, and schedules still match reality? (Targets moved, policies changed, cadence too high for rate of change.)
4. **Catalog Alignment:** Is an automation missing that should exist (gaps in pattern grid)? Suggestions must be approval-gated (Building Block 12), never armed automatically.
5. **Findings Report:** One line per automation (keep | adapt | pause | merge | delete) + rationale; perform changes only after approval.

## Bulk Mode: Reviewing Automation Fleets or Multiple Transcripts

For "review all automations of System X for abstractable workflows" or "extract automation candidates from old chat histories":

1. **Data reduction as in `skill-extractor`** (Map-Reduce via subagents, `swarm-operations` pattern): One subagent per bundle reporting per source: Core task | Pattern (e.g. rotation check, health check, idea mining) | Unique elements | User-neutral abstractable? | Covered by existing skill?
2. **Patterns over one-offs:** When many sources share the same skeleton (e.g., 40 rotation checks), the SKELETON becomes a skill and individual cases become parameterizations — not 40 separate skills.
3. **Deduplication against existing skill/command landscape**, then present numbered candidate list to user before mass creation.

## Example & Application

```text
User: "We tested the citation check for a paper today — from now on this should run weekly across all papers."

1. Target form: Automation prompt for the scheduler + reference to rotation-check.
2. Core: Check citations of a paper against original sources (web/database), apply corrections, in case of changes record follow-up task "Re-upload" in TODO.md.
3. Neutralize: Pipeline root, registry/log paths → configuration block.
4. Add building blocks: Rotation selection (one paper per run), read registry BEFORE selection, read-only exit ("all sources ok"), log hygiene, summary report.
5. Cadence: Weekly is sufficient (papers change slowly); dry run + idle test, then into the scheduler.
```

## Red Flags

| Thought | Reality |
| --- | --- |
| "The workflow ran in the session, so it will run as an automation" | Without a user, all correctives are missing — building blocks checklist is mandatory. |
| "Hourly doesn't hurt" | Yes it does: tokens, log growth, collision risk. Couple cadence to rate of change. |
| "I'll build a separate automation for each variant" | Shared skeleton as a skill, variants as parameters. |
| "Nothing found — guess I'll look for other work" | Read-only exit with log entry is the correct result of an idle run. |

## Related Skills

- `skill-extractor` — Same extraction, target is a callable skill; shares neutralization and transcript sources (documented there).
- `rotation-check` — Standard skeleton for rotating pipeline checks (most common automation type); reference as a building block instead of reinventing.
- `swarm-operations` — Swarm pattern for bulk reviewing.

## Changelog

### 1.1.0 (2026-07-03)
- Fleet Audit Mode (auditing running automation fleet: silent failures, redundancy, drift, gaps) — integrated instead of separate skill (deduplication decision).
- Three new building blocks in `automation-bausteine.md`: Approval gate via sentinel files (12), Staged escalation with handoff artifact (13), Reporting discipline for monitors (14).

### 1.0.0 (2026-07-03)
- Initial version. Derived from abstracting the Codex-Automations inventory (77 automations, dominant rotation check pattern) into user-neutral building blocks.