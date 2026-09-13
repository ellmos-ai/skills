# Core-set functions & Topology Reference

## Contents

1. Compact (5-Task) and Full (10-Task) Governance Topology
2. Functions and Evidence Rules
3. 4-Tier Model Allocation & Dynamic Throttling Rules
4. 3-Line Prompt Header Standard
5. Hypothesis Catalogue
6. Five Safeguards
7. Visible Naming and Stable Identity

---

## 1. Compact and Full Topology

### The compact topology (5 scheduled tasks):

| Task | Functions |
|---|---|
| `automation-care.hygiene` | definition integrity, bindings, permissions and runtime health |
| `automation-care.prompt-quality` | prompt outcome review and reversible text improvement (3-line header standard) |
| `automation-care.scheduler-tuning` | frequency, probe-activation and load distribution |
| `automation-care.resources` | usage, capacity, prediction, dynamic 3-stage throttling |
| `automation-care.cross-system` | inventory exchange, coverage, deduplication and handback |

### The full topology (10 specialized tasks):

| Task Identifier | Default Cadence | Model Tier | Core Responsibility |
|---|---|---|---|
| `antigravity-maintainer` | `35 1,13 * * *` | Tier 1 (3.6 Flash) | Definition completeness, DB vacuuming, orphaned file cleanup. |
| `antigravity-token-watcher` | `18 * * * *` | Tier 1 (3.6 Flash) | Live telemetry, SQLite sync, 7d/30d predictions, dynamic throttling. |
| `antigravity-permissioner` | `37 19 * * *` | Tier 1 (3.6 Flash) | Review least-required permissions, lock enforcement, path bounds. |
| `antigravity-sheduler-state-controller` | `26 5,17 * * *` | Tier 1 (3.6 Flash) | State control, probe-activations, defective task detection. |
| `antigravity-sheduled-task-sentiziser` | `27 2,14 * * *` | Tier 1 (3.6 Flash) | Workload-based cron cadence regulation (raise/lower frequency). |
| `antigravity-task-sheduler-burden-divisor` | `40 20 * * *` | Tier 1 (3.6 Flash) | Load distribution, peak staggering, collision avoidance. |
| `antigravity-sheduler-text-improver` | `30 6 * * *` | Tier 2 (3.7 Flash) | Prompt quality audits, misleading guidance correction (3-line header). |
| `antigravity-task-sync` | `50 10,22 * * *` | Tier 1 (3.6 Flash) | Bidirectional mirroring between active sidecars and reference catalog. |
| `antigravity-file-bond-corrector` | `57 23 * * *` | Tier 1 (3.6 Flash) | Path bindings, naming conventions (`NAMING-SYSTEM.md`), broken link repair. |
| `antigravity-kontext-and-workflow-loader-and-divider` | `2 * * * *` | Tier 1 (3.6 Flash) | Keyword index updates (`STICHWORTLISTE.json`), context & Letter-Hook loading. |

---

## 2. Functions and evidence

### Hygiene & Bindings
Check both directions: registered task without definition and definition without registration. Check missing schedule, dead target, foreign-host path, missing workspace permission and overdue run.

### Prompt quality & 3-Line Header
Sample tasks per run. Verify prompt adherence to the 3-line format (`[TITEL]`, `ZWECK:`, `AUFGABE:`). Compare declared outcome with actual artifacts and receipts.

### Frequency, Activation & Probe-Testing
Use observed workload, user priority and successful outcomes. Never disable warden/standby tasks merely because one run found no work. Test previously disabled tasks with high user priority **one at a time** (probe-activation) and decide state based on follow-up evidence.

### Load distribution & Staggering
Inventory every relevant scheduler before moving times. Avoid peak minute collisions (e.g. staggering across `:18`, `:26`, `:27`, `:30`, `:35`, `:37`, `:40`, `:50`, `:57`). Preserve required ordering between producer and reviewer tasks.

### Token Governance & Dynamic Throttling
Track measurements over time (`token_tracker.sqlite`).
- `Credit > 50%`: Full operation; restore any previously paused tasks and original models.
- `Credit < 20%`: Pause `LOW` priority automations (`LOW_CREDIT_THROTTLING_ACTIVE`).
- `Credit < 10%`: Critical throttling; leave only `HIGH` priority active and downgrade models to Flash (`CRITICAL_THROTTLING_ACTIVE`).
- `ANTIGRAVITY` core tasks are immune to deactivation.

---

## 3. Four-Tier Model Allocation

| Tier | Model | Profile & Purpose |
|---|---|---|
| **Tier 1** | `Gemini 3.6 Flash (High)` | Fast wardens, token tracking, hygiene, sync, umlaut checks. |
| **Tier 2** | `Gemini 3.7 Flash (High)` | Software dev, GitHubBot marketing, Roblox Lua, LaTeX design, prompt improvement. |
| **Tier 3** | `Gemini 3.1 Pro (High)` / Claude | Deep science, mathematical model analysis, peer reviews, technical style audits. |
| **Tier 4** | `Codex (GPT-5.4)` / Claude Code | Multi-file refactorings and architecture migrations. |

---

## 4. Hypothesis catalogue

Classify a failure before changing anything:

| ID | Hypothesis | Allowed response |
|---|---|---|
| h1 | model does not fit task difficulty | propose or apply a supported model tier change |
| h2 | prompt is stale, misleading or lacks 3-line header | make one reversible prompt correction |
| h3 | required skill, tool or permission is missing | add the narrow capability or report the gap |
| h4 | required policy or local orientation is missing | add a verified boot pointer (`AUTOMATION_POLICY.md`), not copied policy sprawl |
| h5 | binding, path or scheduler registration is broken | repair only through the native surface with readback |
| h6 | guidance level does not fit the model | adjust structure and degree of freedom |
| h7 | a new evidenced cause exists | add it to the local catalogue with evidence |
| h8 | cause remains unknown | observe, narrow permissions or pause; do not guess |

---

## 5. Five safeguards

1. **Self-protection & Immunity**: Care tasks with `ANTIGRAVITY` in their name cannot disable themselves or each other, and cannot reduce their own cadence below `recovery_floor.minimum_core_runs_per_day`. A controlled pause remains possible only after an explicit user decision, a security gate or an evidenced emergency.
2. **Deletion protection**: Deleted tasks remain suppressed until the user reverses the decision.
3. **Effect check and rollback**: Every change has a before-state and follow-up.
4. **One change per run**: Preserve causal attribution.
5. **Fail-Closed on Locks**: Active user locks (e.g. `LOCK.user.buildweek-no-push.txt`) override all autonomous write operations.

---

## 7. Visible naming and stable identity

Each adapter profile supplies a non-sensitive `app_display_name`. The generated
visible title is always:

```text
<APP_DISPLAY_NAME> — <CARE_TITLE>
```

A Codex adapter therefore emits `CODEX — ...`; other providers use their own app
label. The stable IDs (`automation-care.*` in the generator, `antigravity-*` in
the native full topology above) do not change. Adapters reconcile by stable ID
and semantic role before considering legacy unprefixed titles, update one
matched task in place and block ambiguous matches. They never create a
replacement merely because the visible title differs.

The prefix helps humans recognize protected core tasks but does not confer
permissions and does not replace the recovery floor, deletion/suppression log,
rollback or native readback.
