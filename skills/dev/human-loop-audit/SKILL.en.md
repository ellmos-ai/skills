---
name: human-loop-audit
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-18
updated: 2026-08-18
description: >
  Interactive zip-merge-style audit procedure for a series of apps/review
  objects: the user tests live and gives short feedback in the chat, while
  the agent already starts the next object AND evaluates the previous
  feedback in parallel (capture it in a structured way, delegate repair
  orders to workers immediately) — instead of waiting sequentially. Use
  this skill for "human-loop-audit", "let's zip-test the apps", "I test,
  you evaluate and repair", or whenever a series of GUIs/products should be
  tested together with the user and findings should turn into repairs
  immediately. Completion is a structured finding list per object
  (Works/Broken/Wish) plus the list of repairs already started.

# Compatibility
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Categorization
category: dev
tags: [audit, usertest, human-in-the-loop, gui-test, reissverschluss, delegation, feedback]
language: en
status: active
visibility: public

# Dependencies
dependencies:
  tools: []
  services: []
  protocols: []
  python: []

# Provenance
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Human-Loop-Audit

> **Not to be confused with `reissverschluss-merge`:** the name shares the
> "zipper" image, but `reissverschluss-merge` is a **Git merge procedure**
> (interleaving two code branches section by section). `human-loop-audit`
> here has nothing to do with Git — it is a **test/audit workflow with the
> user**. Both skills only share the zipper image as the same underlying
> idea (interleaving two strands tooth by tooth, instead of one strand
> after the other).

## Purpose & division of roles

The user's time is the **serial bottleneck**: only they can actually operate
an app live and say within seconds whether it feels right. Everything
else — opening objects, capturing feedback in a structured way, kicking off
repairs — is handled by the agent, and specifically **while** the user is
already on the next object, not afterward. The agent is cockpit operator
and evaluator at the same time.

**The core is the overlap, not the ordering itself:** a purely sequential
"open app → wait → evaluate → open next app" wastes exactly the waiting
time during which the user is testing. Human-Loop-Audit uses precisely
that window.

## Procedure

1. **"start"** from the user → the agent opens the **first** review object.
   Starting the process is enough (e.g. `Start-Process <exe>` or the
   object's matching start command) — **no desktop takeover needed**, the
   user operates it themselves. Briefly confirm that it is open.
2. **The user tests and writes feedback into the chat** — short bullet
   points are enough, nothing gets reworded in a way that changes the
   meaning.
3. **As soon as the feedback arrives, two things run in parallel, not one
   after the other:**
   - The agent **immediately opens the next review object**, so the user
     can keep testing without waiting.
   - **At the same time**, the agent evaluates the feedback that came in:
     recording the finding per object in a structured way (**Works** /
     **Broken** / **Wish**, with a short description), and on a defect or
     clear wish **immediately delegating a repair order to a worker** (not
     collecting it and ordering it "later" — the repair should run while
     the user keeps testing).
4. **Repeat** until all objects are done (back to step 2/3 for each further
   object).
5. **Completion:** present the user with the finding list (per object
   Works/Broken/Wish) plus the list of repairs started (worker/order/
   status).

## Finding structure (per review object)

| Object | Status | Finding | Repair delegated to |
|---|---|---|---|
| `<app/object name>` | Works / Broken / Wish | short bullet, unchanged from the user's wording | worker name/session, if delegated |

An object can get several lines (several findings). Nothing is silently
summarized — completion is read from this table, not from memory.

## Boundary against related skills

- **`reissverschluss-merge`** (see note above) — a pure Git merge procedure,
  no overlap in substance despite the shared name image.
- Related but narrower wave/store-submission test cycles with hard-wired
  extra phases (asset review, submission sheets, ID write-back) and
  **sequential** implementation ("implementing the points runs separately")
  exist as project-local procedures. `human-loop-audit` is deliberately the
  **generic** procedure for **any** series of apps/GUIs and delegates
  repairs **immediately and in parallel**, not as a separate later step.
- **`bugsweep` / `bugfix-protocol`** — the actual repair work that
  `human-loop-audit` delegates to; this skill itself does not repair
  anything.

## Pitfalls

- **Don't wait for the evaluation before opening the next object** — a
  purely sequential "wait, then evaluate, then open the next one" gives
  away exactly the overlap that makes this skill what it is.
- **Capture feedback in a structured way immediately**, don't just collect
  it in the chat history — otherwise it would be gone on a session abort.
- **Don't start objects blindly** when an object is known to be unstable —
  briefly check startability before the user sits in front of it live.
- **Delegate immediately, not collected at the end** — otherwise the repair
  only starts once the user has long finished testing, and the procedure's
  time advantage is lost.

## Trigger examples

- "human-loop-audit"
- "Let's zip-test the apps."
- "I test, you evaluate and repair."
- "start" (after a human-loop audit has already been announced, as the
  start signal for step 1)

## Changelog

### 1.0.0 (2026-08-18)
- Initial version. Procedure adopted from a user definition dated
  2026-08-18: zip-merge-style audit with parallel evaluation + immediate
  repair delegation, delimited from `reissverschluss-merge` (Git merge,
  same name image, no relation) and from narrower, project-local wave test
  cycles (sequential implementation instead of parallel).
