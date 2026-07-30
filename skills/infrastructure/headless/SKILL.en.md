---
language: en
---

> **English** — Official English version of `headless`.


# Headless (English)

## Overview & Purpose

Use this skill when the requesting person explicitly desires a longer, autonomous run without continuous inquiries. This mode increases stamina, not authorization.

A single non-executable item must not unnecessarily halt independent, safe remaining work.

## Prerequisites

Record prior to start:

- concrete goal and success criterion,
- in-scope and out-of-scope items (positive and negative scope),
- available time or cost budgets,
- permissible side effects,
- project rules, locks, and external changes,
- path or mechanism for checkpoints,
- optionally, a permissible local decision profile.

If a decision profile is missing, only explicit rules and safe default assumptions are used. The runtime must not impersonate any person.

## Decision Levels

| Level | Basis | Behavior |
|---|---|---|
| high | explicit rule or repeatedly confirmed pattern | decide; execute only if authority is present |
| medium | plausible, reversible default decision | decide, mark assumption, safely continue |
| low | novel, contradictory, or lacking a resilient framework | do not guess; defer or escalate |

Confidence in the decision and authority for execution are separate axes.

## Execution Protocol

1. **Load context.** Verify rules, state, locks, and goal.
2. **Decompose work.** Mark independent packages, decision points, and approval points. If at least two independent workers are deployed, apply the task and evidence protocol of `orchestrator` if available.
3. **Execute safe work.** Continue reversible, authorized steps.
4. **Handle decisions.**
   - With permissible profile: use the procedure of `decision-avatar`.
   - Without profile: derive strictly from explicit project or task rules.
5. **Park non-executable items.** Record decision or recommendation without anticipating execution.
6. **Continue independent work.** A parked item blocks only its actual dependencies.
7. **Write checkpoint.** Save goal, completed steps, evidence, assumptions, parked items, and next step.
8. **Verify completion.** Self-verify results and bundle open decisions into a compact list.

## Decision Log

Record for every non-trivial assumption:

```text
ID:
Entscheidung:
Grundlage:
Konfidenz:
Ausgeführt: ja/nein
Evidenz:
Rücknahme oder Korrektur:
```

Agent decisions must not later be treated as statements of the requesting person.

## Package-Local Stops

Stop and park an individual package if it requires new authority, an irreversible external action, unclear rules, or involves a conflict. Subsequently check which other packages truly depend on it.

## Overall Run Stop Conditions

The overall run stops only if:

- no safe, independent work is possible anymore,
- a necessary decision has low confidence,
- all remaining work packages require new external or irreversible authority,
- a lock, conflict, or security risk affects the entire remaining scope,
- the agreed budget has been reached,
- the current state can no longer be reliably saved.

## Final Report Format

```text
Erreicht:
Verifiziert durch:
Annahmen:
Zurückgestellte Entscheidungen:
Nicht ausgeführte Seiteneffekte:
Nächster sinnvoller Schritt:
```

## Changelog

### 1.1.0 (2026-07-28)
- Removed personal avatar, path, command, and provider bindings.
- Separated confidence and execution authority.
- Clarified continuation of independent work and bundled escalation.
- Explicitly separated package-local blockers from overall run stops.

### 1.0.0 (2026-06-17)
- Initial local version.