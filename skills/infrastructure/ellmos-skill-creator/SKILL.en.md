---
name: ellmos-skill-creator
version: 0.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-24
updated: 2026-08-24
description: >
  Creates or reworks a skill FOR THIS ECOSYSTEM: delegates the generic
  interview/design/eval loop to the official skill-creator plugin
  (Anthropic, Apache-2.0), but additionally enforces the ellmos
  requirements the official plugin doesn't know about — house frontmatter
  (9 fields), category/visibility rules, provider-/user-/ellmos-neutral but
  ellmos-sensitive detection via grounding-seed, a bundled config.json
  (incl. a learning contract) + connections.json, provider/vendor
  awareness (proposing state-of-the-art alternatives including our own
  ellmos components), a self-update section AND a reusable learning/
  coverage file set (user-usecases.json, usecase-gaps.json,
  known-providers-and-abilities.json, gap-closing-analysis.json — modeled
  on skill-creator's evals.json and A2A/AgentSkill, not a parallel
  standard). ALWAYS use it when a NEW skill for this system should be
  created or an existing one retrofitted for ellmos conformance — also for
  "create a skill", "build me a skill for X", "use skill-creator", "create
  a new skill", "make this skill ellmos-conformant", "create a learning
  contract/code of conduct for a skill", "check a skill's usecase
  coverage". For pure skill FINDING/ROUTING use skill-finder instead, for a
  landscape audit use skill-explorer.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skill-authoring, meta, grounding-seed, provenance, vendor-awareness]
language: en
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: [grounding-seed (optional, recommended)]
  skills: ["skill-creator:skill-creator (plugin, Apache-2.0)"]

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# ellmos-skill-creator

## Origin and decision (fork vs. building it ourselves)

**Decision: build it ourselves, no fork.** Reasoning, so it doesn't get
lost:

- `skill-creator` (Anthropic, marketplace `claude-plugins-official`) is
  **Apache-2.0** licensed (LICENSE text read and verified in the clone,
  2026-08-24) — a fork would be legally clean and is already the
  established pattern elsewhere in the repo (`skills/third-party/grill-me`,
  `skills/third-party/grilling`).
- A fork, however, would have dragged along the original's entire
  eval/benchmark machinery (`agents/{analyzer,comparator,grader}.md`,
  `eval-viewer/`, 7 scripts, a 485-line SKILL.md) — a capability that
  already exists and is directly invocable (`Skill:
  skill-creator:skill-creator`). Per `.PLUGINS/CLAUDE.md` rule 4 ("check
  capabilities before rebuilding") and pattern P10 ("two switches nobody
  compares"), that would be a duplicate, not an extension.
- The actual gap is **purely ellmos-specific** and fundamentally unknown to
  the original: house frontmatter (`templates/SKILL.md`),
  `docs/CONVENTIONS.md`, provider/user/ellmos neutrality with
  ellmos-sensitivity, `grounding-seed` docking, vendor awareness,
  self-update.
- This skill contains **no Anthropic text** (own wording throughout) — so
  it doesn't trigger any Apache-2.0 attribution obligation for
  modifications either. It **composes** the original instead of copying
  it: that's both the legally cleanest and the lowest-maintenance path.

## When to activate

- "create a skill for X", "build a new skill", "use skill-creator"
- "make this skill ellmos-conformant", "retrofit a skill to house
  standard"
- Whenever the **target location** is a skill in `.AI/.SKILLS/skills/…`
  (or its canonical Plan-D clone) — not for general, ecosystem-unrelated
  requests ("create me some Claude skill with no connection here").

## Procedure

### Step 1 — delegate interview/design/eval

Call the official `Skill: skill-creator:skill-creator` for: intent
clarification, designing the SKILL.md structure, test cases, the eval
loop, description optimization (`scripts/improve_description.py`).
**Don't reinvent it** — this part is generic and already well solved in
the original.

### Step 2 — set up the ellmos house scaffold (mandatory, additive to the original format)

Extend the SKILL.md produced by the original with the nine house fields
from `.SKILLS/templates/SKILL.md` (resp. `AGENT.md`/`WORKFLOW.md`/
`PROMPT.md` depending on the type), first reading
`.SKILLS/docs/CONVENTIONS.md` for the category folder, the flat rule
(<5 files flat), the version convention (SemVer: MAJOR/MINOR/PATCH) and
the multilingual sets (core: DE+EN mandatory). **`visibility` always
starts at `private-only`** — publication is a later, reviewed user
decision (`.AI/VISIBILITY-POLICY.md`), never the default. These fields are
purely **additive** to the Anthropic format (extra YAML keys alongside
`name`/`description`) — every skill created this way stays fully
`anthropic_compatible: true`.

### Step 3 — enforce the principles: provider-neutral, user-neutral, ellmos-neutral-but-ellmos-sensitive

Full text + code patterns: `references/ELLMOS-PRINCIPLES.md`. Short
version: the skill produced must be **runnable on its own** (bringing
everything it needs) and **at the same time** use ellmos components as
soon as they're present — it decides that itself at runtime, never hard-
wired. That is exactly the pattern `grounding-seed` already provides
(README: "cultivated landscape, not wildflower" / "viable alone, more
productive together") — **no second detection mechanism is invented**,
this skill consistently points produced skills at
`grounding_seed.detect_ecosystem()`.

### Step 4 — ship config.json + connections.json

`grounding-seed` is already importable as a Python package (verified
2026-08-24: `import grounding_seed` resolves successfully to the locally
cloned `grounding-seed` source tree, Plan-D clone) — it is the
**canonical docking point**, don't invent a new file. For every produced
skill with an external need (programs, services, providers):

- **`config.json`** — the skill's own settings (template:
  `templates/skill-config.template.json`).
  `grounding_seed.store.LocalStore(root)` uses this filename by default
  for its role storage — a produced skill can therefore either use its
  `config.json` itself as the `LocalStore` backend OR keep it separate,
  if it needs pure behavior settings alongside roles (then a second
  `LocalStore(root, filename="connections.json")` instance).
- **`connections.json`** — the actually **resolved** external docking
  points (which program/which service was found, since when, with which
  provenance) — template: `templates/skill-connections.template.json`,
  schema `ellmos.source-resolver.user-config.v1` (identical to
  `source-resolver`, deliberately chosen that way per the grounding-seed
  README so a later migration into the real `source-resolver` is
  lossless — see `migration.py` there).

Details, CLI and code example: `references/ELLMOS-PRINCIPLES.md`, section
"Docking".

### Step 5 — build in provider/vendor awareness

Full text: `references/VENDOR-AWARENESS.md`. Short version: the produced
skill gets a "Providers & alternatives" section that (a) names the
state-of-the-art provider(s) for the topic (e.g. ElevenLabs for TTS), (b)
at least one alternative provider, (c) **explicitly lists ellmos' own
components as an equally ranked candidate** when they cover the topic
(e.g. `ellmos-voice-io` instead of/alongside ElevenLabs) — and **proposes**
installation/switching on a matching user request, instead of silently
assuming it. Basis for "what's present on the system":
`grounding_seed.scan.scan_resources([...])` (checks `shutil.which`) plus
`.AI/.MCP/MCP-PROFILE-MANAGEMENT.md` for ellmos candidates.

### Step 6 — set up self-update

Full text: `references/SELF-UPDATE.md`. Short version: every produced
skill gets a "Self-update" section that (a) periodically proposes a short
web search to stay state-of-the-art, (b) knows related skills/workflows
and names new alternatives that might fit better, (c) carries a small
learning JSON along (template:
`templates/skill-connections.template.json`, field `notizen`/`gelernt`),
which can be offloaded to an existing ellmos memory component
(USMC/Gardener) instead of growing locally — here too: detect instead of
hard-wire (`grounding_seed.detect_ecosystem()`).

### Step 6b — set up a learning contract + usecase coverage (reusable pattern)

Full text: `references/LEARNING-CONTRACT-AND-COVERAGE.md`. Short version:
not only this skill itself, but **every skill it produces** gets a small,
reusable learning/coverage file set — checked against established
standards, not a parallel standard:

- `evals/evals.json` — **reuse**, don't duplicate: this is already the
  skill-creator standard for test cases designed by the author.
- `user-usecases.json` — use cases actually raised by the user, same
  shape as `evals.json` (template:
  `templates/user-usecases.template.json`).
- `usecase-gaps.json` — comparison: which user usecases are untested/
  uncovered (template: `templates/usecase-gaps.template.json`).
- `known-providers-and-abilities.json` — the candidate space of known
  providers per role, fields modeled on A2A/`AgentSkill`
  (id/name/description/tags), not invented (template:
  `templates/known-providers-and-abilities.template.json`).
- `gap-closing-analysis.json` — structural ways to close each gap (ellmos
  module, ellmos bundle, third-party module, new build) — not a
  duplicate of `grading.json.eval_feedback` (template:
  `templates/gap-closing-analysis.template.json`).
- `config.json` field `lernvertrag` — code of conduct (choose the best
  option, **the user is king**, never install anything autonomously,
  update interval) — deliberately as an extension of `config.json`, not a
  seventh file.

Schemas: `.SKILLS/schemas/{user-usecases,usecase-gaps,known-providers,
gap-closing-analysis}-v1.schema.json` — the same house convention as
`skill-v1.schema.json`. `grounding-seed` was checked for this file set and
deliberately **not** extended (reasoning in
`LEARNING-CONTRACT-AND-COVERAGE.md`) — only `connections.json` remains its
part.

### Step 7 — register, test, commit

- Choose the category folder per `.SKILLS/CLAUDE.md`/`SKILLS-MAP.md`; when
  in doubt, ask `skill-finder` or `controlcenter_find_skill` whether a
  family already exists.
- Run `testing/` (privacy gate + metadata tests) before committing.
- **Don't hand-edit** the registry files (`registry/components.json`,
  `SKILLS-MAP.md`, `llms.txt`) — they get generated
  (`build_public_registry.py`, `build_skills_map.py`, `catalog.py`). If a
  foreign, uncommitted session is currently running in the canonical
  clone, do NOT regenerate globally (that mixes foreign and own changes
  into one file) — instead commit the new skill folder in isolation and
  leave the registry regeneration to the next clean run
  (`skill-register-care`).
- `git commit -- skills/<category>/<name>/` — only your own, new paths.

## Compatibility with the Anthropic format

All additional fields are pure YAML extensions alongside
`name`/`description` — a standard Claude Code instance without this
ecosystem keeps reading only `name`/`description` and ignores the rest.
`config.json`/`connections.json` are optional bundled resources (as
provided for in `docs/CONVENTIONS.md`), not a mandatory dependency — a
skill without them works unchanged.

## Related skills

- `skill-creator:skill-creator` — the generic interview/eval loop
  (delegated to, step 1).
- `skill-finder` — router for existing own skills (check BEFORE building:
  does this already exist?).
- `skill-explorer` — landscape audit + web research for new skills/plugins
  (meta level: our skill *inventory*; this skill here instead makes every
  *individual produced* skill itself provider-aware).
- `skill-family-care`, `skill-register-care` — maintenance after building.
- `grounding-seed` (module, `.AI/.MODULES/.CONTROL/grounding-seed`) — the
  actual docking/self-provisioning logic, only referenced here, not
  duplicated.

## Changelog

### 0.2.0 (2026-08-24)
- Follow-up (ticket T-20260824-218233618, scope addition): added a
  reusable learning/coverage pattern per produced skill —
  `user-usecases.json`, `usecase-gaps.json`,
  `known-providers-and-abilities.json`, `gap-closing-analysis.json` (new
  house schemas in `.SKILLS/schemas/`) plus a learning-contract field in
  `config.json`. `evals/evals.json` (skill-creator) deliberately reused
  instead of duplicated. `grounding-seed` checked — no extension needed
  (reasoning in `references/LEARNING-CONTRACT-AND-COVERAGE.md`), so no
  follow-up ticket. Field names for provider catalogues modeled on the A2A
  protocol (`AgentSkill`) instead of an own vocabulary.

### 0.1.0 (2026-08-24)
- Initial version. Decided and justified building it ourselves instead of
  forking (ticket T-20260824-218233618). Delegates generic skill creation
  to `skill-creator:skill-creator`, adds the house scaffold, ellmos
  principles, `grounding-seed` docking (config.json/connections.json),
  vendor awareness and self-update.
