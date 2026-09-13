---
name: workflow-extract
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-07-30
description: >
  Builds a self-running, user-neutral workflow automation from a chat transcript
  or existing automation prompts (e.g. from another agent system): a recurring prompt
  or automation skill for Cron/Schedule/Loop. Alias: automations-extractor. Use when
  asked: "make an automation out of this", "run this regularly/nightly", "extract workflows
  from these transcripts/automations", "build automation from this session", or at
  `/workflow-extract`. Systematically supplements missing automation building blocks
  (rotation selection, check registry, idempotency, log hygiene, approval gate, escalation handoff,
  monitor reporting discipline). Also includes Fleet Audit mode: audit existing automation fleets
  for silent failures, redundancy, drift, and gaps ("check my automations/scheduled tasks/cron jobs").
  If an on-demand callable skill is needed instead, use sister skill skill-extractor.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [automation, workflow, extraction, cron, schedule, loop, transcript, meta, rotation]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="workflow-extract banner">
# Workflow-Extract — Building Automations from Chat Transcripts and External Automations

## Purpose

Some processes do not belong in an on-demand skill loaded manually, but in an **unattended automation that runs by itself**: nightly checks, rotating project audits, periodic maintenance runs. This skill extracts such workflows from two source types — chat transcripts (a process developed interactively that should run unattended in the future) and existing automation prompts of other systems (e.g. Codex automations, Scheduled Tasks, n8n flows) — turning them into user-neutral, robust automation prompts or skills.

The difference from an interactive workflow: An automation has **no user to correct it**. Everything intercepted by the user in an interactive session must be caught by the automation itself. This is precisely why the building blocks in `automation-bausteine.md` exist.

## Process

### 1. Clarify Source and Target Form

| Source | Typical Case |
| --- | --- |
| Current session / transcript | Process developed interactively, should continue running periodically |
| External automation (prompt file, cron task, n8n flow) | Porting/abstraction to another system or into the library |

Target forms (one or more):

- **Automation Prompt:** standalone, user-neutral prompt text usable in any scheduler (Codex automations, Claude `/schedule`/cron, Scheduled Task, n8n).
- **Workflow Skill:** skill in the library describing the process, which the automation prompt merely calls or parameterizes (preferred when the same process applies across multiple pipelines/systems — single source of truth).
- **Command:** thin slash command for manual trigger of the same process.

### 2. Extract Workflow Core

Extract from the source:

- **Core Task:** What is being checked/maintained/generated? (one sentence)
- **Selection Logic:** What is the task applied to — fixed target or rotation over a set (one project per run)?
- **Prerequisites:** What must be read/checked before work (root documents, registries, locks)?
- **Documentation Duties:** Where are results, logs, and follow-up tasks written?
- **Exit Paths:** When does the run end read-only ("nothing to do" is a valid result)?

For chat transcripts, additionally evaluate correction loops (see `../skill-extractor/transcript-quellen.md`): Every user correction is a candidate for a guard that the automation will need itself in the future.

### 3. Neutralize

Follow the rules in `../skill-extractor/neutralisierung.md`: Separate mechanics from configuration, pull paths/hosts/project names into a configuration block. Automation prompts urgently require this configuration block because they are copied verbatim into schedulers — concrete values belong in ONE place at the prompt header.

### 4. Supplement Automation Building Blocks

Hold the extracted core against the checklist in `automation-bausteine.md` and supplement missing blocks — in particular rotation selection with check registry, idempotency, log hygiene, lock respect, read-only exit, and completion report. A workflow without these blocks works during testing but degenerates in continuous operation (duplicate checks, growing logs, collisions with parallel agents).

### 5. Set Cadence and Budget

- **Link frequency to rate of change:** A check does not need to run more often than its subject changes. Experience from grown automation fleets: Many initially hourly checks were reduced to daily/weekly — with rotation selection, even a sparse cadence covers the entire pipeline.
- **Night window for heavy tasks**, short read-only checks may run more frequently.
- **Cost awareness:** Every run costs tokens/compute; a run that mostly ends read-only should determine that early (read registry BEFORE expensive analysis).

### 6. Test and Deploy

1. **Dry Run:** Execute the finished prompt once interactively (acting as the scheduler) and verify: Does it end cleanly? Does it write registry/log correctly? Does it stay in scope?
2. **Edge Case Test:** Simulate a run where there is nothing to do — it must end read-only with a short log entry, without "inventing work".
3. **Deploy:** Register in the target scheduler; for skill form, store in the library and deploy.
4. **Monitor Failure Path:** Check log/registry after the first 2–3 real runs — automations fail most frequently due to path drift (target moved) and growing log files.

## Fleet Audit Mode: Auditing a Running Automation Fleet

For "check my automations": do not extract, but help operate the EXISTING fleet. Systematically check via the target system's automation source (prompt/config files, schedules, run logs/memories):

1. **Silent Failure / No-Op Detection:** Is the automation running but accomplishing nothing? (Read run memories/logs of recent runs: only idle runs, errors, dead paths?)
2. **Redundancy + Return:** Do automations overlap in scope? Does the return (output, resolved findings) justify the consumption (tokens, runs)?
3. **Drift:** Do prompt paths, conventions, and schedules still match reality? (Targets moved, policies changed, cadence too high for rate of change.)
4. **Catalog Reconciliation:** Is an automation missing that should exist (gaps in pattern grid)? Suggestions must be approval-gated (Block 12), never self-activated.
5. **Findings Report:** one line per automation (keep | adjust | pause | merge | delete) + justification; make changes only after approval.

## Bulk Mode: Reviewing Automation Repositories or Many Transcripts

For "check all automations of System X for abstractable workflows" or "extract automation candidates from old chat transcripts":

1. **Data reduction as in skill-extractor** (Map-Reduce via subagents, `swarm-operations` pattern): One subagent per bundle reporting per source: Core task | Pattern (e.g. rotation check, health check, idea mining) | Unique elements | User-neutral abstractable? | Covered by existing skill?
2. **Pattern over Single Pieces:** When many sources share the same scaffold (e.g. 40 rotation checks), the SCAFFOLD becomes a skill and individual cases become parameterizations — not 40 single skills.
3. **Deduplication against existing skill/command landscape**, then present numbered candidate list to the user before bulk construction.

## Example

```text
User: "We tested the paper citation check today — from now on this should run weekly across all papers."

1. Target form: Automation prompt for scheduler + reference to rotation-check.
2. Core: Check paper citations against original sources (web/database), apply corrections, write follow-up "re-upload" task in TODO.md if modified.
3. Neutralize: Pipeline root, registry/log paths → configuration block.
4. Supplement blocks: Rotation selection (one paper per run), read registry BEFORE selection, read-only exit ("all sources ok"), log hygiene, completion report.
5. Cadence: Weekly suffices (papers change slowly); dry run + idle test, then to scheduler.
```

## Red Flags

| Thought | Reality |
| --- | --- |
| "The process ran in the session, so it will run as an automation" | Without a user, all corrective guards are missing — building blocks checklist is mandatory. |
| "Hourly doesn't hurt" | Yes it does: tokens, log growth, collision risk. Link cadence to rate of change. |
| "I'll build a separate automation for every variant" | Shared scaffold as a skill, variants as parameters. |
| "Nothing found — guess I'll find other work" | Read-only exit with log entry is the correct result of an idle run. |

## Related Skills

- `skill-extractor` — same extraction, target is an on-demand skill; shares neutralization and transcript sources.
- `rotation-check` — standard scaffold for rotating pipeline checks (most frequent automation type); reference as building block instead of reinventing.
- `swarm-operations` — swarm pattern for bulk reviewing.

## Changelog

### 1.1.0 (2026-07-03)
- Fleet Audit Mode (checking running automation fleet: silent failures, redundancy, drift, gaps) — integrated instead of separate skill.
- Three new building blocks in automation-bausteine.md: Approval gate via sentinel files (12), Staggered escalation with handoff artifact (13), Reporting discipline for monitors (14).

### 1.0.0 (2026-07-03)
- Initial version. Created from abstraction of Codex automations inventory (77 automations, dominant rotation check pattern) into user-neutral building blocks.
