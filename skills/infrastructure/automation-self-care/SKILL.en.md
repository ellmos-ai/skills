---
name: automation-self-care
version: 1.3.1
type: skill
author: Lukas Geiger + OpenAI + Google Gemini
created: 2026-07-28
updated: 2026-09-09
description: >
  Builds and operates a provider-neutral self-care core set for scheduled LLM
  tasks and desktop-app automations. Adds deterministic policy linting, lock
  and model governance, semantic prompt review, consistent multi-surface
  updates, mini-checks, and rule-file hygiene. Use when an agent should
  discover its native scheduler or continuously improve an automation fleet
  with rollback, readback, and deletion protection. Triggers on automation
  self care, scheduler task care, desktop app automation maintenance,
  automation fleet audit, self-healing schedules, core-set-textautomations,
  basic-text-automations, textbased-automation-core,
  textbased-automation-drivers, textbased-governance-automations, or
  textbased-desktopapp-automations.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, scheduler, desktop-apps, self-care, maintenance, rollback, cross-system, governance, token-governance, mini-check, policy-linter]
language: en
status: active
visibility: public
aliases: [textbased-governance-automations-seed, tgas, textbasierte-governance-automationen-seed, textbased-governance-automations, textbasierte-governance-automationen, textbased-governance-automatisations-seed, core-set-textautomations, basic-text-automations, textbased-automation-core, textbased-automation-drivers, textbased-desktopapp-automations]
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
  local_changes_since_sync: true
---

<img src="banner.png" width="100%" alt="automation-self-care banner">

# Automation Self-Care

Create a native, provider-specific maintenance fleet from one provider-neutral
control loop. Preserve the original intent of the ANTIGRAVITY task family while
requiring evidence, reversible changes and native readback.

## Non-negotiable boundaries

- Treat discovery, planning, approval, mutation and readback as separate phases.
- Use the target app's supported automation API, command or UI. Never assume that
  editing a storage file changes live app state.
- Read local rules, locks, deletion/suppression logs and existing schedules before
  proposing a task.
- Do not invent scheduler support. If create/update/readback cannot be proven,
  produce a manual installation plan and stop before mutation.
- Make at most one independently testable tuning change per care run.
- Protect the care tasks from disabling themselves or reducing their own cadence
  below the configured recovery floor. Only an explicit user decision, a
  security gate or an evidenced emergency may authorize a controlled pause.
- Keep stable machine task IDs independent from visible titles. Treat an app
  prefix as an additional recognition safeguard, never as identity or as a
  replacement for recovery, suppression, rollback and readback controls.
- Preserve the previous prompt, schedule, model, permissions and enabled state so
  every mutation can be rolled back.
- Count success only after outcome evidence, not merely scheduler start or exit 0.
- Never copy secrets, private prompts or personal data into a shared registry.
- Before any mutation, run the deterministic policy linter named by the
  provider profile. Resolve project paths, checks, and policies through adapter
  fields or neutral placeholders; never put host, account, or private directory
  paths into the public skill.
- Check the target system's authoritative lock mechanism before file,
  scheduler, commit, or push actions. If lock authority is unknown,
  unavailable, or contradictory, fail closed and remain read-only.
- Do not change models from hard-coded product versions or unsupported quality
  assumptions. Resolve allowed models and minimum standards from the current
  provider surface and valid local policy. Upgrades and downgrades require the
  authority defined there; if unclear, preserve the current model.
- Do not derive prompt tuning from run logs alone. Before mutation, compare the
  proposal semantically with the target project's policies and preserve all
  safety, research, and release boundaries.
- Treat multiple authoritative state surfaces as one transaction: capture the
  before-state, update every declared target, read back every target, and roll
  back completely after partial success. Never assume a universal mirror count
  or local directory layout.
- Store run reports only in dedicated local evidence and status stores, never
  in agent rule files. Their names and locations come from the provider profile.
- Heavy maintenance may be paired with tightly bounded mini-checks. The
  provider profile must declare the runtime limit, scope, parent task, and
  escalation path; a mini-check must not perform deep repair.

## Workflow

### 1. Discover the native automation surface

Inventory the current actor, provider, non-sensitive `app_display_name`, app
class, scheduler surface, supported operations, state files, run history, usage
telemetry and readback method. Record capabilities using the profile contract in
[provider-adapter-contract.md](references/provider-adapter-contract.md).

Distinguish native desktop-app schedules, CLI/headless execution, OS scheduler or
service starter, general scheduler service, workflow engine, and unsupported or
UI-only automation. Do not equate the existence of a config file with a supported
mutation path.

### 2. Inventory the fleet

For each task capture a stable local identifier, semantic role, visible title,
purpose, prompt fingerprint, schedule, enabled state, model, reasoning,
permissions, target paths, last scheduler event, last successful outcome and
current owner. Keep prompt content local.

Match existing tasks semantically before proposing creation. Prefer stable task
ID, then provider-native ID, semantic role and known legacy title. A different
visible title is not evidence that a new task is needed. Ambiguous matches block
the plan instead of creating a duplicate.

Check the authoritative live surface twice before mutation when the app can rewrite
state from memory.

### 3. Design the core set

Read [core-set.md](references/core-set.md). Select either:

- `compact`: five care tasks combining frequency with load distribution; or
- `full`: nine focused tasks corresponding to the original maintenance family.

Generate a provider-neutral plan:

```bash
python scripts/build_core_set.py provider-profile.json \
  --topology compact --out automation-care-plan.json
python scripts/build_core_set.py --lint-plan automation-care-plan.json
```

The generator never installs tasks. Review every `blocked` capability and choose
collision-free local times before applying the plan. New provider profiles set
`app_display_name` explicitly; CI can enforce that with `--strict-profile`.
Generated visible titles use `<APP_DISPLAY_NAME> — <CARE_TITLE>` while
`automation-care.*` task IDs remain unchanged. A Codex profile uses `CODEX`.

### 4. Stage installation

Install through the native provider adapter:

1. Start with hygiene in read-only mode.
2. Add resource protection.
3. Add prompt-quality tuning with rollback.
4. Add frequency and load tuning only after enough run evidence exists.
5. Add cross-system coordination last.

For a title-only migration, update the semantically matched task in place through
the supported native surface. Read back the stable ID and all non-title fields;
any unexpected operational delta requires rollback. A second plan/apply cycle
must report no change and must not create another task.

Create new or imported tasks disabled unless the user explicitly approved active
installation. For an unattended pilot, require a deletion log, before-state
snapshot, run receipt and rollback path first.

### 5. Run the care loop

Every care task follows:

```text
follow-up previous change
  -> collect current evidence
  -> classify one cause
  -> choose zero or one change
  -> mutate through native surface
  -> read back
  -> write receipt and next-check condition
```

Use the hypothesis catalogue and evidence rules in
[core-set.md](references/core-set.md). Unknown cause means observe, narrow
permissions or pause safely; never guess a repair.

### 6. Coordinate across actors

Keep local app state authoritative. Share only task contracts, coverage, status,
receipts and sanitized fingerprints. Redundant read-only reviews are allowed;
single-writer mutations require a claim or an equivalent native lock.

### 7. Systems Without Native Event Hooks (Letter-Hooker Extension)


Treat token or subscription limitation as capacity state, not a broken actor.
Return delegated coverage after the original actor produces a successful receipt.

## Required outputs

For each setup or care run report:

- discovered native surface and unsupported capabilities;
- selected topology and tasks created, proposed or skipped;
- exact mutation and before/after readback;
- evidence of outcome or open observation window;
- rollback location and return condition;
- shared coverage update, if a coordination registry exists.

## Example

User: "Set up self-maintaining schedules in this desktop app."

Discover whether the app can list, create, update and verify scheduled tasks.
Generate the compact plan, present unsupported capabilities, then install only the
approved tasks through the native surface. A folder containing a task prompt
without a live scheduler registration is not a completed setup.

## Changelog

### 1.3.1 (2026-09-09)

- Consolidated the explicitly requested 1.2 and 1.3 self-care hardening into a
  provider-neutral contract.
- Removed host, account, and private project paths from the public guidance and
  replaced them with adapter fields or neutral placeholders.
- Bound model changes to current provider capabilities, local policy, and
  evidenced authority; removed fixed version rankings and unsupported quality
  claims.
- Defined portable contracts for policy linting, semantic prompt review, lock
  gates, transactional multi-surface updates, rule-file hygiene, and mini-checks.

### 1.3.0 (2026-09-09)

- Added deterministic policy linting and semantic policy review.
- Hardened multi-surface parity and reconciliation of contradictory states.

### 1.2.0 (2026-09-06)

- Added lock governance, model anti-regression, rule-file hygiene, and the
  mini-check architecture.

### 1.1.0 (2026-08-30)

- Added provider-neutral `app_display_name` and the visible title format
  `<APP_DISPLAY_NAME> — <CARE_TITLE>`, including `CODEX — ...` through the
  Codex adapter profile.
- Added plan linting, stable-ID/semantic reconciliation and duplicate guards.
- Clarified that naming is additive to the recovery floor and that title-only
  migrations must preserve every non-title fingerprint.

### 1.0.1 (2026-07-30)

- Added provider-neutral text-automation and desktop-app automation aliases.

### 1.0.0 (2026-07-28)

- Consolidated the original ANTIGRAVITY maintenance family, the F1-F6 control
  loop and later provider-specific adaptations into a neutral core-set skill.
