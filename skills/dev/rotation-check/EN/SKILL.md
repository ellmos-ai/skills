---
language: en
---

> **English** — Official English version of `rotation-check`.

# Rotation-Check — One Target per Run, Fair Coverage, Memory

## Overview & Purpose

Anyone who wants to periodically check a pipeline containing many projects (sources, style, health, security, translations, …) faces a distribution problem: checking all projects in every run is too expensive; without memory, every run randomly checks the same things. The rotation pattern solves both: **exactly one target per run, selection by "longest unchecked", registry as memory.** This way, even a sparse schedule (daily/weekly) covers the entire pipeline over weeks — provably and without duplicated effort.

Proven as the backbone of a mature inventory of production automations across multiple project pipelines.

## Components

### 1. Two Files per Pipeline (Created Once)

| File | Contents | Character |
| --- | --- | --- |
| `CHECKED-REGISTRY.md` | One compact line per check: target, date, check type, result, next step | State overview — read BEFORE any target selection |
| `CHECKS-LOG.txt` | Short history entry per run with details/evidence | Journal — append-only |

Both reside in the pipeline root (not in individual projects) so a run can capture them with a single read. Registry line format:

```text
| <ziel> | <YYYY-MM-DD> | <checktyp> | <ok|befund|übersprungen> | <nächster schritt> |
```

### 2. Selection Rule

1. Read registry and log (mandatory, BEFORE selection — otherwise duplicate check).
2. Candidates: Targets that have never been checked or were checked longest ago for THIS check type.
3. Fall back / skip if the target was recently touched by a **closely related** check (e.g., citation check right after source check yields no value) or is currently locked/under active work (respect locks).
   **Sibling Cooldown:** If multiple related checks run over the same target set (e.g., development, bug hunt, and review of the same pipeline), agree on a grace period (empirical value: ~24 h) during which a target processed by a sibling check is not selected again — prevents collisions and conflicting parallel changes.
4. Prioritize out of turn only with good reason (e.g., major overhaul since last check) — state the reason in the log.

### 3. Perform Check — with Read-only Exit

Apply the actual check (freely definable: source check, style check, security audit, …) to the ONE chosen target. Two valid outcomes:

- **Finding:** Fix what fits into the scope; record larger tasks as follow-up items in the project-local TODO/AUFGABEN file (the check does not have to solve everything itself).
- **Nothing to do:** Document briefly and end. An idle run is a result, not a failure — under no circumstances expand the scope just to "have found something".

### 4. Documenting

- Supplement registry line (compact), write log entry (details/evidence).
- **Log Hygiene:** If registry/log become cluttered (empirical value: several hundred lines), move old state to `_archiv/`, create a fresh file, reference the predecessor in the header (path + date).
- **Path Drift:** If an expected path points to nowhere (target moved/renamed), do NOT recreate — correct via the authoritative status file/registry of the pipeline and record the invalid path in a failure log.

### 5. Cadence

Couple frequency to the rate of change of the checked assets: rotation checks over stable inventories work well weekly (one target per run ≈ entire pipeline per quarter for ~12 targets); fast-moving checks (e.g., for active work) daily. Practical experience: initially hourly checks were almost all reduced to daily/weekly — coverage remained, costs dropped.

## Prompt Template (for Scheduler/Automation)

```text
VORBEREITUNG: Lies <PIPELINE_ROOT>/<POLICY-DOKUMENTE> sowie <REGISTRY> und <LOG>.

AUFGABE: Wähle genau ein Ziel aus <ZIELMENGE>. Bevorzuge Ziele, die für den Check
"<CHECKTYP>" noch nie oder am längsten nicht geprüft wurden. Wurde ein Ziel kürzlich
von diesem oder einem eng verwandten Check geprüft oder ist es gesperrt: ausweichen
oder read-only mit Logeintrag enden.

CHECK: <konkrete Prüf-/Pflegeaufgabe und what bei Befund zu tun ist; Folgearbeiten in
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
| "I'll just pick an interesting project" | Selection only via registry — otherwise favorite-project bias and blind spots. |
| "I'll read the registry after the check" | Before. It is the selection criterion, not just the log. |
| "Multiple targets per run achieve more" | One target keeps runs short, idempotent, and abortable; volume comes through rotation. |
| "The idle run was wasted" | A documented idle run updates memory — that's half the system's value. |

## Related Skills

- `workflow-extract` — builds automations from sessions/third-party automations; uses this framework as a standard component.
- `pipeline-optimizer` — for structural overhaul of a pipeline (rotation-check maintains, optimizer renovates).

## Changelog

### 1.1.0 (2026-07-03)
- Added sibling cooldown as selection rule (anti-collision between related checks across the same target set; finding from full classification of automation inventory).

### 1.0.0 (2026-07-03)
- Initial version. Abstracted from Codex automation inventory (rotation pattern in ~40 out of 77 automations: research/software/Roblox checks with CHECKED-REGISTRY/CHECKS-LOG).
