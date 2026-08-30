---
name: tidy-up
version: 1.1.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-08-19
updated: 2026-08-19
description: >
  One-time Tasksolver+Writer+Maintainer pass for the project folder the
  session has been working in anyway (including subfolders) — not a
  system-wide sweep. Resolves open trivial/autonomous register points,
  updates documentation to the measured current state (in the project AND
  in the root of the pipeline the project lives in) and clears out
  strays/temp files following the trash-can principle. Use this skill for
  /tidy-up, "tidy up the project", "clean up here before we continue", at
  the end of a work session on a project, or as a due autonomous task
  inside /work-autonomous + /goal.

# Compatibility
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Categorization
category: dev
tags: [hygiene, maintenance, cleanup, documentation, tasksolver, writer, maintainer, autonomy, goal, work-autonomous, ticket-master]
language: en
status: active
visibility: public

# Dependencies
dependencies:
  tools: []
  services: []
  protocols: [work-autonomous, bilingual-doc-sync]
  python: []

# Provenance
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Tidy Up — Tasksolver+Writer+Maintainer pass for the active project folder

## Purpose

At the end of a work session on a project, small loose ends typically
remain: a finished TODO point that was never checked off; a README that
shows the old rather than the measured state; a handful of test files
nobody needs anymore. `tidy-up` is a **one-time, self-limiting pass** that
follows up on exactly that for **one** project folder — the one the
session has been working in anyway. No permanent loop, no system-wide
sweep.

The pass consists of three roles that the model takes on itself, one after
another:

1. **TASKSOLVER** — resolve or correctly file open, trivial/autonomous
   points of the project register.
2. **WRITER** — update documentation to the measured current state, in the
   project AND in the root of the pipeline the project lives in.
3. **MAINTAINER** — hygiene: collect strays/temp files (trash-can
   principle), register/catalogue maintenance, file away remaining open
   points instead of only mentioning them in chat.

**Measured before building this skill:** as of 2026-08-19, this library
has **no** standalone skills or roles named `tasksolver`/`writer`/
`maintainer` — neither as a skill name nor as a documented role in another
skill (full-text search over `skills/**/SKILL.md`, no hits except an
unrelated name `privat-mail-writer`). The three roles are therefore
defined directly below as sections, not orchestrated externally. Should
standalone `tasksolver`/`writer`/`maintainer` skills emerge later,
`tidy-up` adopts them by reference instead of continuing to duplicate the
logic (a check duty on every further development of this skill).

## Scope — what counts as "the active project folder"?

- The project folder the session has worked on in this context,
  **including all subfolders**. No jump into neighboring projects, no
  sweep over an entire pipeline or even `.TOPICS/` as a whole.
- **One** targeted exception: documentation/register updates may
  additionally touch the **root level of the pipeline** the project lives
  in (e.g. a status line for this one project in a pipeline-wide overview
  table) — but only the line/section concerning this project, not
  reordering the whole pipeline root.
- If it's unclear what "the active project folder" is (e.g. the session
  has worked in several folders), take the nearest common project root
  (where the project's README/TODO/CLAUDE.md live) — when in doubt, scope
  it narrower rather than wider.

## Role 1 — TASKSOLVER

Goal: bring the project register (`TODO.md`/`AUFGABEN.txt`/comparable
local convention) to a correct, current state.

1. Locate the project register (the local convention takes precedence
   over a new file — see the rule "leftover tasks belong filed, not just
   mentioned" in the global rule set).
2. Assess each open point individually:
   - **Already done** (e.g. by the session that just ended) → mark as done
     / move to `DONE.md` or the local done convention.
   - **Trivial and autonomously solvable** (no user decision/approval/
     data/hardware/session needed, see the boundary table in
     `work-autonomous`) → solve it now, then file it as done.
   - **Not trivial or not autonomous** → do NOT touch it, but leave it
     correctly filed (don't leave it uncommented if a better filing spot
     exists — e.g. a point that has long deserved a `USER/*` ticket
     category).
3. Don't invent new tasks — `tidy-up` resolves existing leftovers, it does
   not create a new agenda.

## Role 2 — WRITER

Goal: documentation shows the **measured**, not the remembered or hoped-for
state.

1. In the project: check README/CHANGELOG/status lines against the actual
   code/folder state (e.g. named files still exist, the named version
   number is correct, an "in progress" marker isn't long since done).
2. In the pipeline root: if a register/status table exists there that
   lists this one project (e.g. `.TOPICS/<pipeline>/ROADMAP.md`,
   `STATUS.md`, a project table in the pipeline README) — update its
   line/section for EXACTLY this project.
3. **Never replace curated content, only measure+update.** Tables,
   changelogs or carefully worded sections keep their form and tone —
   only facts (numbers, status, filenames, versions) are corrected. When
   unsure whether a section is curated: rather add a note than overwrite
   an existing wording.
4. No rewriting from scratch when an update is enough.
5. **Translation follow-up** (addition 2026-08-19, live user order): if a
   language version required by its tier under **policy P-006**
   (`.SYNC/_policies/library/P-006_sprachstufen.md`) is missing for the
   project, or an existing version is noticeably outdated — the WRITER
   step follows up on that. P-006 in short: **the core set (DE+EN) is
   mandatory** for every published repo/catalogued object (repo:
   `README.md` EN + `README_de.md`; skill: `SKILL.md` DE + `SKILL.en.md`);
   the full/world set (ES/ZH/JA/RU resp. +FR/HI/AR/BN/PT) is the target
   picture but is followed up **gradually**, not in a campaign through
   `tidy-up`. **Tool: the existing skill `bilingual-doc-sync` is
   orchestrated (invoked), its logic is NOT duplicated** — it already
   covers exactly "follow up on a missing version" + section parity check
   + divergence resolution. `tidy-up` only gives it the trigger (which
   object, which mandatory language is missing per P-006) for the active
   project folder; translation quality, structural parity and the
   lead-language rule remain `bilingual-doc-sync`'s responsibility.
   **Same boundaries as P-006:** translate only up to the measured current
   state, don't invent content, respect real diacritics/umlauts, the repo
   cooldown (<24h since the last commit) and active locks — then leave
   this point untranslated and file it as an open point (role 3) instead
   of forcing it.

## Role 3 — MAINTAINER

Goal: hygiene, without anything getting lost.

1. **Collect strays/temp files** (script leftovers, `*.tmp`, duplicate
   copies, forgotten debug output) — trash-can principle: move into a
   local `_archive/` folder (create it + add it to `.gitignore` if not
   already there), **never delete directly**. For finds whose origin/
   purpose is unclear: actively determine the purpose (read the file), not
   clear it away unread — see the convention "certify foreign changes".
2. **Register/catalogue maintenance:** if the project is part of a larger
   catalogue/registry (skill registry, module manifest, pipeline
   overview), check whether the entry for this project is still correct —
   don't rebuild the whole registry, only this one entry.
3. **File open leftovers instead of just mentioning them in chat:**
   whatever remains at the end of this pass (points that aren't
   autonomously solvable, discovered but unfixed defects, deliberately
   postponed items) gets filed following the rule "leftover tasks belong
   filed, not just mentioned" — primarily locally at the source (the
   project's TODO.md/AUFGABEN.txt convention), otherwise centrally
   (`ticket-master`/`TASKPLAN`), each with context (what, why open, next
   step).
4. **Respect locks:** before every change, check whether an active
   `LOCK.txt`/`LOCK.<scope>.txt`/`LOCK.user.*` sits in the project folder.
   A `LOCK.user.*` stops `tidy-up` completely for the affected area — no
   bypassing, no partial tidy-up on the locked area.
5. **Commit+push only per the respective project's repo convention** —
   for separate planning and development surfaces, make changes in the
   authorized local project clone, not in a planning or projection copy.
   Own changes are handled per the global convention "commit + push your
   own work immediately", where the project provides for that.

## Self-limitation

`tidy-up` is **one pass, not a loop**. After role 3, the skill ends with a
short summary (what was solved, what was updated, what was cleaned up,
what was filed as open) and returns to the calling session. Calling
`/tidy-up` again on the same project shortly afterward is allowed, but not
automatically sensible — see the due-criterion below.

## Relationship to work-autonomous

`tidy-up` runs **count as an autonomously executable task in the sense of
`work-autonomous` level 1** (normal, visible work — no reason to switch
into the expensive level-2 exhaustion check as long as a due `tidy-up` run
exists). In practice this means: when `/work-autonomous` is used together
with `/tidy-up` inside a `/goal`, the goal only counts as complete once
due `tidy-up` points are also handled — as far as they're autonomously
executable (see the boundary table in `work-autonomous`; a `tidy-up` point
that needs a user decision counts just as little as autonomous as any
other `USER/*`-bound task).

**Due criterion** (when is a `tidy-up` run "due"?):

1. The session has already worked on a concrete project folder in this
   session context (not: pure research/reading without changes — then
   there's nothing to tidy up).
2. The cooldown since the last logged `tidy-up` run for EXACTLY this
   project has expired (default: 1× per session close-out on this
   project — no repeat run **within** the same session without new
   changes since the last run).
3. No active `LOCK.user.*` blocks the project folder (see role 3, point
   4).

Logging the last run (analogous to the guard pattern in
`work-autonomous`, but deliberately leaner — `tidy-up` doesn't need a
four-step chain, just a timestamp per project):

```bash
usmc --agent <agent> note "tidy-up: project=<project-path-or-slug> at=<ISO-time> result=<done|nothing-to-do>" \
  --type context --priority 2 --tags "tidy-up-log,<project-slug>"
```

Before a new run, read the same day (`usmc --agent <agent> working
--limit 20` filtered by `tidy-up-log,<project-slug>`) to check criterion
2.

A `/goal` construct (if one exists or is being built — `work-autonomous`
itself doesn't call `/goal`, see its section "deliberately without a
built-in `/goal`") reads this due criterion just like it reads
`work-autonomous`'s own abort signal: if a `tidy-up` run is due AND
autonomously executable, the goal isn't done yet — regardless of whether
`work-autonomous`'s own four-step chain already reports "exhausted".

The matching, minimally invasive counter-entry in the `work-autonomous`
skill itself (level 1, new source "due tidy-up runs of the active
project") is part of this extension — see its changelog entry.

## Related skills

- **`work-autonomous`** — see above; `tidy-up` is one of the sources that
  `work-autonomous`'s level 1 works through, not a replacement for its
  exhaustion check.
- **`bilingual-doc-sync`** — orchestrated by role 2 (WRITER) for the
  translation follow-up (see there), not duplicated. `tidy-up` only
  decides WHAT is missing per P-006, `bilingual-doc-sync` decides HOW it
  gets translated/synced.
- **`bugsweep`** — systematic bug search with doubling escalation.
  Different purpose (finding defects, not maintaining a register/docs/
  hygiene) — on overlap (a bugsweep find lands in the register), `tidy-up`
  only takes over register maintenance, not the bug search itself.
- **`dev-cycle`** — 8-phase framework for new feature development.
  `tidy-up` is not a development framework, but a wrap-up/hygiene pass
  after work already done.
- **`folder-flattening`** — restructures nested folder hierarchies.
  `tidy-up` tidies files within the existing structure, it doesn't change
  the structure itself.

## Examples

```
User: "/tidy-up"
(the session has just worked on the authorized local checkout of
`example-project`)

→ TASKSOLVER: read TODO.md — 2 points already done by the session (moved
  to DONE.md), 1 trivial point ("README typo on line 12") solved
  autonomously, 1 point needs a user decision (left unchanged).
→ WRITER: the README version was 1.2.0, actually 1.3.0 (package.json) —
  corrected. Pipeline root status table: the line for "example-project"
  set from "in progress" to "active".
→ MAINTAINER: found 3 debug scripts in the project root, moved to
  _archive/ (purpose checked: one-off test scripts, no longer
  referenced). Checked the skill registry entry: correct. Left 1 open
  point (user decision) in AUFGABEN.txt, already correctly filed there.
→ USMC log written: tidy-up: project=example-project at=2026-08-19T14:30
  result=done
→ Summary to the user: 3 solved, 2 doc spots updated, 3 files archived,
  1 point open (needs a user decision).
```

```
Combined with /goal + /work-autonomous:

/goal "finish project X" with /work-autonomous + /tidy-up as conditions
→ work-autonomous level 1 finds: an ACTIONABLE ticket done, then no
  further ticket, BUT the tidy-up due criterion is met (the session has
  worked on project X, no logged run since session start, no LOCK.user
  active) → tidy-up pass executed.
→ Only AFTER tidy-up reports "done" AND work-autonomous level 2 reports
  "exhausted" does the goal count as complete.
```

## Changelog

### 1.1.0 (2026-08-19)
- Addition from a live follow-up to T-20260819-461890468 (user, verbatim:
  "following up on a translation that doesn't exist yet should also
  belong to the skill"): role 2 (WRITER) gets a fifth point, translation
  follow-up per **policy P-006** (language tiers: core set DE+EN
  mandatory, full/world gradually). The tool is the already-existing
  skill `bilingual-doc-sync` — orchestrated, not duplicated. Added a
  frontmatter dependency + a "related skills" entry.

### 1.0.0 (2026-08-19)
- Initial version from ticket T-20260819-461890468. Three roles
  (Tasksolver/Writer/Maintainer) defined as sections in the skill, after a
  full-text search across the library confirmed that no standalone
  `tasksolver`/`writer`/`maintainer` skills exist (otherwise they would
  have been orchestrated instead of duplicated). Scope limited to the
  active project folder + a pipeline-root status line. Goal integration:
  `tidy-up` runs count as a `work-autonomous` level-1 source, with its own,
  lean USMC due-log (no four-step guard like `work-autonomous` itself —
  `tidy-up` is too simply structured for that). Added the matching,
  minimally invasive counter-entry in `work-autonomous` 1.3.0 (see its
  changelog).
