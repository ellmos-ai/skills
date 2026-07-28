# Core-set functions

## Contents

1. Compact and full topology
2. Functions and evidence
3. Hypothesis catalogue
4. Four safeguards
5. Rollout order

## Compact and full topology

The compact topology uses five scheduled tasks:

| Task | Functions |
|---|---|
| `automation-care.hygiene` | definition integrity, bindings, permissions and runtime health |
| `automation-care.prompt-quality` | prompt outcome review and reversible text improvement |
| `automation-care.scheduler-tuning` | frequency, activation and load distribution |
| `automation-care.resources` | usage, capacity, prediction and temporary throttling |
| `automation-care.cross-system` | inventory exchange, coverage, deduplication and handback |

The full topology preserves nine focused responsibilities from the original task
family:

| Task | Responsibility |
|---|---|
| `automation-care.hygiene` | registry/definition completeness, paths and stale tasks |
| `automation-care.prompt-quality` | sample outcomes and improve misleading prompts |
| `automation-care.frequency` | raise/lower cadence and test one reactivation |
| `automation-care.load` | distribute work over day/week and avoid collisions |
| `automation-care.resources` | usage history, prediction, model/cadence throttling |
| `automation-care.cross-system` | exchange tasks, status, coverage and changes |
| `automation-care.bindings` | verify project/workspace/task bindings |
| `automation-care.permissions` | review least-required permissions from run evidence |
| `automation-care.runtime` | app health, archives and maintenance prerequisites |

Use compact by default when the platform has few tasks or expensive runs. Use full
when each function has enough evidence and a distinct native control surface.

## Functions and evidence

### Hygiene

Check both directions: registered task without definition and definition without
registration. Check missing schedule, dead target, foreign-host path, missing
workspace permission and overdue run only after comparing creation time, time zone
and first due time.

### Prompt quality

Sample one task per run. Compare its declared outcome with actual artifacts and
receipts. Keep the prompt unchanged when evidence is good. Preserve the old text
before a small correction and define the next run that will test it.

### Frequency and activation

Use observed workload, user priority and successful outcomes. Do not disable a task
merely because one run found no work. Test at most one previously disabled task per
run and decide its state only after the follow-up evidence.

### Load distribution

Inventory every relevant scheduler before moving times. Separate deliberate
independent reviews from accidental duplicate mutation. Preserve required ordering
between producer and reviewer tasks.

### Resources

Track measurements over time and attribute consumption only when evidence supports
it. Prefer cheaper models or lower cadence before disabling important work. Restore
the exact previous settings when capacity recovers. Never disable the recovery
core itself.

### Cross-system coordination

Use stable task, deployment, actor and run identities. Import new tasks as disabled
proposals unless activation was approved. Respect deletion/suppression logs.
Duplicate coverage is valid for high-priority work, read-only review and failover;
it is not permission for duplicate writes.

### Bindings, permissions and runtime

Validate project/workspace association and accessible roots. Derive permissions
from actual task needs, never from a blanket unrestricted default. Treat app
lifecycle, scheduler liveness, task execution and successful outcome as separate
facts.

## Hypothesis catalogue

Classify a failure before changing anything:

| ID | Hypothesis | Allowed response |
|---|---|---|
| h1 | model does not fit task difficulty | propose or apply a supported model change |
| h2 | prompt is stale, misleading or poorly scoped | make one reversible prompt correction |
| h3 | required skill, tool or permission is missing | add the narrow capability or report the gap |
| h4 | required policy or local orientation is missing | add a verified boot pointer, not copied policy sprawl |
| h5 | binding, path or scheduler registration is broken | repair only through the native surface with readback |
| h6 | guidance level does not fit the model | adjust structure and degree of freedom |
| h7 | a new evidenced cause exists | add it to the local catalogue with evidence |
| h8 | cause remains unknown | observe, narrow permissions or pause; do not guess |

## Four safeguards

1. Self-protection: care tasks cannot disable the recovery core.
2. Deletion protection: deleted tasks remain suppressed until the user reverses
   the decision.
3. Effect check and rollback: every change has a before-state and follow-up.
4. One change per run: preserve causal attribution.

Locks, publication gates, privacy boundaries and explicit user decisions remain
stronger than every tuning recommendation.

## Rollout order

1. Hygiene, read-only.
2. Resource observation and recovery floor.
3. Prompt-quality loop.
4. Frequency and load tuning after sufficient run history.
5. Cross-system coordination after the local fleet is stable.

Collect several real scheduled outcomes before enabling automatic tuning. The exact
observation period depends on cadence and task risk; do not invent a calendar
duration unsupported by local evidence.
