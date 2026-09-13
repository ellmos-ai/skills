---
name: rotation-check
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-07-30
description: >
  Standard framework for rotating pipeline checks: Select exactly one target per run from a set
  (projects, folders, repos) — preferably the one unchecked for the longest time —, perform the check,
  record the result in a check registry and a history log. Use this skill when a recurring check needs
  to be distributed across many projects ("regularly check all X for Y"), when automation must avoid
  duplicate checks, when creating or using a check registry / CHECKS-LOG structure, or when a periodic
  quality round (source check, style check, health check, audit) should be fairly distributed across a pipeline.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [automation, check, rotation, registry, pipeline, log, audit, wartung]
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

<img src="banner.png" width="100%" alt="rotation-check banner">
# Rotation Check — One Target Per Run, Fair Coverage, Memory

## Purpose

Anyone wanting to periodically audit a pipeline containing many projects (sources, style, health, security, translations, …) faces a distribution problem: checking all projects per run is too expensive; without memory, every run randomly checks the same project. The rotation pattern solves both: **exactly one target per run, selection based on "unchecked for the longest time", registry as memory.** Thus even a low frequency (daily/weekly) covers the entire pipeline over weeks — provably and without duplicated work.

Proven as the backbone of a mature collection of production automations across multiple project pipelines.

## Building Blocks

### 1. Two Files per Pipeline (Created Once)

| File | Content | Character |
| --- | --- | --- |
| `CHECKED-REGISTRY.md` | One compact line per check: target, date, check type, result, next step | State summary — read BEFORE every target selection |
| `CHECKS-LOG.txt` | Short history entry per run with details/evidence | Journal — append-only |

Both reside in the pipeline root (not in individual project folders) so a run can inspect them with a single read. Registry line format:

```text
| <ziel> | <YYYY-MM-DD> | <checktyp> | <ok|befund|übersprungen> | <nächster schritt> |
```

### 2. Selection Rule

1. Read registry and log (Mandatory, BEFORE selection — otherwise duplicate check occurs).
2. Candidates: Targets that have never been checked for THIS check type or haven't been checked for the longest time.
3. Fallback/Bypass when the target was recently touched by a **closely related** check (e.g., citation check right after source check yields no value) or is currently locked/under active edit (respect locks).
   **Sibling Cooldown:** When multiple related checks run over the same target set (e.g., development, bug hunt, and review of the same pipeline), agree on a cooldown period (rule of thumb: ~24 h) during which a target modified by a sibling check is not re-selected — prevents collisions and conflicting parallel changes.
4. Prioritize out of order only with a good reason (e.g., major overhaul since last check) — state the reason in the log.

### 3. Perform Check — With Read-Only Exit

Apply the actual check (freely definable: source check, style check, security audit, …) to the ONE selected target. Two valid outcomes:

- **Finding:** Fix what fits into the scope; record larger follow-up work in the project-local TODO/task file (the check does not need to solve everything itself).
- **Nothing to do:** Document briefly and terminate. An idle run is a result, not a failure — under no circumstances expand the scope just to "have found something".

### 4. Documenting

- Supplement registry line (compact), write log entry (details/evidence).
- **Log Hygiene:** If registry/log become cluttered (rule of thumb: several hundred lines), move old state to `_archiv/`, create a fresh file, reference the predecessor in the header (path + date).
- **Path Drift:** If an expected path points to nowhere (target moved/renamed), DO NOT create it anew — correct via the authoritative status file / registry of the pipeline and record the invalid path in a failure log.

### 5. Cadence

Couple frequency to the rate of change of the audited items: Rotation checks over stable repositories run well on a weekly cadence (one target per run ≈ entire pipeline per quarter for ~12 targets); fast-moving checks (e.g., on active work) run daily. Practical experience: initial hourly checks were almost all reduced to daily/weekly — coverage remained, costs dropped.

## Prompt Template (For Scheduler / Automation)

```text
VORBEREITUNG: Lies <PIPELINE_ROOT>/<POLICY-DOKUMENTE> sowie <REGISTRY> und <LOG>.

AUFGABE: Wähle genau ein Ziel aus <ZIELMENGE>. Bevorzuge Ziele, die für den Check
"<CHECKTYP>" noch nie oder am längsten nicht geprüft wurden. Wurde ein Ziel kürzlich
von diesem oder einem eng verwandten Check geprüft oder ist es gesperrt: ausweichen
oder read-only mit Logeintrag enden.

CHECK: <konkrete Prüf-/Pflegeaufgabe und was bei Befund zu tun ist; Folgearbeiten in
die projektlokale TODO-Datei>.

Wenn keine Arbeit anfällt: kurz dokumentieren, Lauf beenden.

DOKUMENTATION: Registry-Zeile in <REGISTRY> (Ziel, Datum, Checktyp, Ergebnis, nächster
Schritt) + Verlaufseintrag in <LOG>. Bei Überlänge: alten Stand nach _archiv/ und
frische Datei mit Verweis.

ABSCHLUSS: Kurzbericht (Ziel | getan | Ergebnis | Folgeaufgaben).
```

## Red Flags

| Thought | Reality |
| --- | --- |
| "I'll just pick an interesting project" | Selection strictly via registry — otherwise favorite-project bias and blind spots occur. |
| "I'll read the registry after the check" | Read it before. It is the selection criterion, not just the log. |
| "Multiple targets per run achieve more" | One target keeps runs short, idempotent, and cancelable; volume comes via rotation. |
| "The idle run was wasted effort" | A documented idle run updates the memory — that is half the value of the system. |

## Related Skills

- `workflow-extract` — builds automations from sessions / external automations; uses this framework as a standard component.
- `pipeline-optimizer` — for structural rebuilding of a pipeline (Rotation-Check maintains, Optimizer renovates).

## Changelog

### 1.1.0 (2026-07-03)
- Added sibling cooldown as selection rule (anti-collision between related checks over the same target set; finding from full classification of automation stock).

### 1.0.0 (2026-07-03)
- Initial version. Abstracted from Codex automation stock (rotation pattern in ~40 of 77 automations: research/software/roblox checks with CHECKED-REGISTRY/CHECKS-LOG).
