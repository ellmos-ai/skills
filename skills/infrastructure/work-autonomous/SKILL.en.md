---
name: work-autonomous
version: 1.1.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-08-15
updated: 2026-08-15
description: >
  Termination condition for autonomous loops: keep working independently as
  far as possible AND only end a loop once it is PROVEN that no autonomously
  executable task remains. The mere impression "nothing left to do" is NOT
  enough — it triggers a four-step verification chain (think/decide,
  _DECISIONS, Gardener/USMC, decision-avatar/BYUM) that must first try to WIN
  new tasks before the loop is allowed to end. Use this skill for
  /work-autonomous, /waafap, "keep working autonomously until there is
  nothing left to do", as the goal condition inside a /loop, or whenever it
  needs checking whether autonomous work is truly exhausted before ending a
  loop or session.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [autonomy, loop, goal, workflow, decision, exhaustion-check, guard, ticket-master]
language: en
status: active
aliases: [waafap, work-autonomous-as-far-as-possible]

dependencies:
  tools: []
  services: []
  protocols: [think, decide, decision-avatar]
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

# work-autonomous — Only end the loop once it is proven no autonomous tasks remain

## Purpose

This skill does two things at once:

1. **Keep working autonomously as far as possible** — ordinary session work, nothing special.
2. **Only end a loop once it is PROVEN** that no autonomously executable task remains anymore. The
   suspicion "I can't find anything left to do right now" is **not** a reason to stop — it is the
   **trigger** for a verification chain that first tries to **win** new tasks. Only once that chain
   comes back completely empty does the stop count as proven.

**Deliberately without a built-in `/goal`:** The skill can be used standalone (e.g. invoked
directly as `/work-autonomous` inside a normal session) as well as a condition inside a larger
loop construction: assign `/loop` as usual, then name only this skill as the goal. The goal then
roughly reads: *"End the loop once no autonomous tasks remain — and until then, keep working
autonomously as far as possible."* The skill itself does not call any `/goal` construct; it only
produces the unambiguous stop signal that such a construct can read (see "Termination signal"
below).

## Operating model — two tiers

### Tier 1 — Normal work (every tick)

On every invocation, first look for autonomously executable work the normal way (see the
boundary section below) and do it: open `ACTIONABLE` tickets, unblocked `BLOCKED` tickets, due
`WAITING` tickets, open `TODO.md`/`AUFGABEN.txt` items in projects with no user dependency, due
routine/hygiene checks per local policy, work started but not finished in the previous session
(USMC `working`).

→ **Found & done:** report the outcome briefly, tick ends, the loop keeps running normally. Tier
2 is NOT entered — none of the four expensive verification steps are needed while visible work
exists.

### Tier 2 — Exhaustion check (only on suspicion "nothing left to do")

Only once Tier 1 finds **nothing** autonomous does the suspicion arise. That suspicion alone is
not enough. The following chain now runs **mandatorily** to **win** new tasks:

1. Apply **`/think` + `/decide`** to the question: "Is there really no autonomously executable
   work left, or am I overlooking something?" — structured analysis, not a gut feeling.
2. **Evaluate the system's central decision register** — wherever open and resolved user decisions
   are tracked. **Resolve that location via the role `decisions.ledger`** rather than hard-wiring
   it: `source_resolver.resolve("decisions.ledger")` (module `source-resolver`,
   `.MODULES/.CONTROL/source-resolver`), if installed. If `source-resolver` isn't installed or
   returns `not_found`, fall back to the known default path (on this system:
   `_control-center/_DECISIONS/`, the `TO-DECIDE-USER*.txt` chain, the host's own
   `TO-DECIDE-USER-<HOST>.txt`, `DECIDED-AND-DONE.md`; on other systems, the equivalent decision
   register kept there) — the skill behaves identically with or without the resolver present. Have
   decisions been made recently that now unblock work that was previously blocked or waiting for
   approval? A freshly decided item is almost always a new autonomous task (implementing the
   decision).
3. **Evaluate Gardener and USMC** (`find()`/`recall()` resp. `usmc facts|lessons|working|context`):
   is there open working-memory content, a lesson with an unfinished follow-up task, or facts
   pointing at overlooked but executable work? This is exactly where earlier sessions leave
   unfinished items (`RESUME:` field, open `note` entries).
4. **Apply `decision-avatar`** (on systems with a local profile: `tom-lm` +
   `build-your-users-mind`/BYUM): is there a documented pattern showing that the user would want a
   specific action carried out autonomously here? Only count this as a new task at sufficient
   confidence (🟢/🟡) — 🔴 does not count as a won task; it becomes an item for the "user-only
   remainder" case below.

**Only once all four steps come back empty** does "no autonomous tasks remain" count as
**proven**. Only then is the loop actually over.

If any step finds new work → go back to Tier 1, do the work, set the guard state (see below) to
"found" instead of "exhausted".

### Special case: only user-bound remainders left

If the chain finds **no autonomous** task anymore, but `USER/*` tickets or undecided
`_DECISIONS` items remain open, that is still a **stop for autonomy** — but not "nothing to do",
rather "nothing *autonomous* to do". Per the ticket-master autonomy-loop rule, these items are
presented **bundled** (one combined ask, not individual pings). The termination signal explicitly
distinguishes this case from a genuinely empty backlog.

## Boundary — what counts as "autonomously executable"?

Reference: `ticket-master` categories (`.AI/.MODULES/.CONTROL/ticket-master/docs/CATEGORIES.en.md`).

| Case | Autonomous? | Reasoning |
|---|---|---|
| `ACTIONABLE` ticket | **Yes** | No blocker, no user dependency — by definition. |
| `BLOCKED/*` (host-receipt, foreign-state, lock, quota, dependency) | No, unless the blocker has **empirically** lapsed | A periodic re-check is allowed (autonomy loop); "present" alone is not sufficient proof — evidence is required. |
| `WAITING/*` (scheduled, review-due, marker) before its date/marker | No | Time-bound. |
| `WAITING/*` after the date/marker hits | **Yes** | Condition met → moves to `ACTIONABLE`. |
| `USER/*` (decision, data, freigabe, hardware, session) | **Never autonomous** | Strictly requires a user decision/data/approval/hardware/session. Present bundled, see above. |
| `PARKED/*` (skip, backlog, until-trigger) | No, unless an explicit order/trigger exists | Deliberately deferred, no auto re-check. |
| Open `TODO.md`/`AUFGABEN.txt` items without an approval/decision note | **Yes** | Project register, ordinary work. |
| Due routine/hygiene checks (cooldown elapsed, no lock) | **Yes** | Regular maintenance per local policy. |
| Areas locked by `LOCK.user.*` | **Never** | User lock — only the user removes it, see LOCK-SYSTEM. |
| Irreversible or externally-effective steps without policy approval (Zenodo upload, pushing to judged/protected branches, server-spend decisions beyond the laptop threshold, permanent deletion without preview) | **No** | Requires approval/decision even when technically executable. |
| A session only startable via GUI/login (e.g. a Claude Desktop task, interactive login, a physical hardware action) | **Never** | "A session only the user can start" — no loop can take that over. |

Rule of thumb: something is autonomous if it can be brought to completion **without** a user
decision, approval, data, hardware, or session, AND does not require an irreversible or
externally-effective action lacking documented policy approval.

## Guard against infinite loops (mandatory)

**Problem:** without a brake, the four-step chain would run in full on every re-check, even though
nothing has changed since the last empty run — expensive and pointless, especially if the skill
is invoked repeatedly (a loop, a scheduled task, or a manual re-invocation shortly after).

**State is persisted in USMC** (process state belongs there on this system, not in markdown
files):

```bash
# Read the state (filter by tag work-autonomous-guard)
usmc --agent <agent> working --limit 20

# Write the state after a chain run
usmc --agent <agent> note "work-autonomous-guard: result=<exhausted|found> fingerprint=<FP> at=<ISO-time>" \
  --type context --priority 3 --tags "work-autonomous-guard,<project-slug>"
```

**Fingerprint** = a coarse but checkable figure built from: count/IDs of open `ACTIONABLE`
tickets, mtime of the `_DECISIONS` chain (`TO-DECIDE-USER*.txt`, `DECIDED-AND-DONE.md`), and the
number of new USMC `working` entries since the last chain run. If any of these values changes, the
situation has changed — the guard must not keep blindly assuming "exhausted".

**Procedure before every chain run:**

```
guard = read the latest "work-autonomous-guard" entry from USMC
if guard exists
   and guard.result == "exhausted"
   and (now - guard.timestamp) < GUARD_INTERVAL   (default: 15 minutes)
   and fingerprint(now) == guard.fingerprint:
       → do NOT run the chain again.
       → report: "Still no autonomous work — unchanged since {guard.timestamp}.
                  No new trigger. STOP (guard active)."
else:
       → run the chain in full (all four steps).
       → write a new guard state (timestamp=now, fingerprint=fingerprint(now),
         result=exhausted|found).
       → exhausted → STOP (proven). found → back to Tier 1, do the work.
```

A single fully empty chain run is enough proof of "no autonomous tasks remain" (per the ticket's
requirement: "only once ALL steps of a run come back empty"). The guard does not prevent the
finding itself, only the **repeated, unchanged re-finding** of it on closely spaced re-invocations.

`GUARD_INTERVAL` is configurable (default 15 minutes) — pick it longer in a very slow-moving
environment (rare new tickets/decisions), shorter in a very active one.

## Termination signal

Every run ends with **one** unambiguous, grep-able line so a surrounding `/loop` or a future
`/goal` construct can read whether to continue:

```
WORK-AUTONOMOUS: CONTINUE                        — Tier 1 did work, the loop keeps running.
WORK-AUTONOMOUS: STOP (exhausted)                — chain steps 1–4 came back fully empty, proven no work left.
WORK-AUTONOMOUS: STOP (guard, unchanged since …) — guard active, no new trigger since the timestamp.
WORK-AUTONOMOUS: STOP (user-only)                — only USER/* remainders open, presented bundled.
```

`CONTINUE` is the only signal on which a surrounding loop should trigger another tick. Every
`STOP` variant is the proven termination — including which of the three stop cases applies.

## Relationship to other skills

- **`think`/`decide`** — provide the structured analysis/decision for chain step 1. Called here as
  a building block, not reinvented.
- **`decision-avatar`** (this skill, user-neutral) — provides chain step 4. On systems with a
  concrete, authorized profile this corresponds to `tom-lm` + `build-your-users-mind`.
- **`orchestrator`** — governs HOW work is delegated to subagents and how their completion claims
  are verified. `work-autonomous` governs WHEN to stop looking for work at all; the two combine
  freely (the orchestrator can be part of the work done in Tier 1).
- **`bugsweep`** — an example of a different, self-limiting search protocol (doubling escalation
  instead of a four-step chain). `work-autonomous` is more generic: it checks not only code for
  bugs but any source of autonomous work.
- **Ticket categories (`ticket-master`)** — supply the vocabulary for "autonomously executable"
  (see boundary table) and the template for the autonomy loop (BLOCKED re-check, USER bundling,
  WAITING date pulling, PARKED standstill).

## Example run

```
Tick 1: found ACTIONABLE ticket T-... → done. WORK-AUTONOMOUS: CONTINUE
Tick 2: no ACTIONABLE ticket left, no open TODO item.
        → Tier 2: chain 1–4 runs.
        → Step 2 (_DECISIONS): DECIDED-AND-DONE.md got a new entry 10 minutes ago.
          → yields a new autonomous task.
        → Guard: result=found written. Task done. WORK-AUTONOMOUS: CONTINUE
Tick 3: nothing visible again.
        → Tier 2: chain 1–4 runs, all four steps come back empty.
        → Guard: result=exhausted, fingerprint=FP1, timestamp=T1 written.
        → WORK-AUTONOMOUS: STOP (exhausted)
Tick 4 (2 minutes later, e.g. triggered by another loop re-invocation):
        → Guard: result=exhausted, fingerprint(now)==FP1, (now-T1) < 15 min.
        → Chain NOT run again.
        → WORK-AUTONOMOUS: STOP (guard, unchanged since T1)
```

## Changelog

### 1.1.0 (2026-08-15)
- Reference retrofit from ticket T-20260815-385400870: step 2 (decision register) now resolves
  its location via the `decisions.ledger` role (`source_resolver.resolve(...)`, module
  `source-resolver`) instead of hard-wiring it — with a documented fallback to the previous path
  if the resolver isn't installed. Functional behavior unchanged.

### 1.0.0 (2026-08-15)
- First version from ticket T-20260815-522639345: two-tier operating model, four-step
  verification chain, boundary table following `ticket-master` categories, USMC-backed guard
  against infinite loops, unambiguous termination signal for `/loop`/`/goal` constructs.
