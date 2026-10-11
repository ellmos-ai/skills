---
name: model-strategy
version: 3.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-10-03
description: Role-based multi-model strategy. The model catalog lives in a local configuration file instead of the skill text -- roles (thinker/decision-maker, long-running worker, draft generator, reviewer/acceptance, escalation), reasoning effort as an independent axis, mandatory review for draft models, provider switching for independent reviews, budgets, and delegation flow.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [model-switching, orchestration, multi-model, cost-optimization, routing, cross-agent, advisor, roles]
language: en
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/ing-strategie.md', 'origin_version': '2.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="model-strategy banner">

> **English** — Official English version of `model-strategy`.

# Model-Switching Strategy (English)

> Role-based multi-model strategy: configuration instead of a hardcoded catalog, roles instead
> of a rigid score table, mandatory review for drafts, provider switching for independent
> reviews.

---

## 0. Configuration

**Models do not belong in this text.** Which concrete models, providers, and invocation paths
exist right now changes faster than a skill can sensibly be maintained — and differs per user.
This skill therefore describes only **roles and principles**; the actual catalog lives in a
configuration file inside the skill folder.

### Load order

1. **Local file** in the skill folder: `models.local.json` or `models.private.json` (both naming
   patterns are already covered by this library's `.gitignore`, `skills/**/*.local.*` and
   `skills/**/*.private.*` — never publish, never commit). If present, this is the authoritative
   catalog.
2. **Example file** `models.example.json` in the same folder — a neutral placeholder template
   that shows the schema. It is only a template for creating your own local file, never a
   catalog for real runs.
3. **Live discovery**, when both files are missing or incomplete: which models does the current
   runtime actually offer (e.g. a native subagent tool's `model` enum, `codex debug models
   --bundled`, an app's own model list)? A guessed model is worse than a briefly measured one.

**On conflict, the live measurement wins.** A configuration file can be stale (a model was
retired, renamed, or replaced); a fresh measurement against the runtime itself outranks any text
source, including your own local configuration. Name the conflict briefly and update the
configuration file afterward instead of silently overriding it.

**`deprecated: true` means: never use.** A catalog entry marked `deprecated` stays in place for
recognition/history reasons (so an agent can make sense of an old mention), but is never chosen
for a new task — not even as a fallback.

### Schema (see `models.example.json`)

Every catalog entry carries: `id`, `provider`, `invoke` (invocation pattern, no real paths in the
example), `effort_levels`, `roles` (see Section 1), `strengths`, `weaknesses`, `guardrails`
(reliability constraints such as "draft only", "must not write to the filesystem itself", "tight
review" — see Section 3), `budget_hint` (pointer to the `budgetierung` skill), and `deprecated`.

---

## 1. Roles instead of a rigid model hierarchy

A model choice first answers **which role** a task needs, only then which concrete model
currently fills that role best/cheapest. Roles are more stable than model names — a model gets
swapped out, the role stays.

| Role | Question | Typical trait |
|---|---|---|
| **Thinker/decision-maker** | architecture, strategy, ambiguous requirements, weighing alternatives | expensive, used selectively rather than continuously |
| **Long-running worker** | ongoing implementation across many steps: implementation, debugging, standard tasks | cheap enough to run continuously |
| **Draft generator** | fast first pass (design, text, code, structure, translation) | fast but subject to mandatory review (Section 3) |
| **Reviewer/acceptance** | checks results of other models | strongest when the provider differs from the author's (Section 4) |
| **Escalation** | brought in only for the single hardest step | never for the whole run, always briefly justified |

A model can carry several roles (e.g. being both a long-running worker and an occasional
reviewer). Which models currently fill which roles lives in the configuration (Section 0), not
here.

### Rough difficulty orientation (not a fixed table)

A score calculated over fixed dimensions (clarity, complexity, creativity, context, criticality)
can serve as a **rough orientation** to distinguish between a long-running worker and a
thinker/escalation — it is not a binding mechanism that automatically determines a model:

```
SCORE = (10 - CLARITY) + COMPLEXITY + CREATIVITY + CONTEXT + CRITICALITY   (each dimension 0-10)
```

Low score → a long-running worker, or even a cheap/token-free local model, suffices. High score
(persistently contradictory requirements, mathematical proof, statistics with far-reaching
consequences) → thinker/escalation, usually followed by review. The broad normal case of the
long-running worker sits in between. The exact threshold for escalating depends on the current
catalog (some users have only two role-fillings, others six) and therefore does not belong in a
fixed table in this text.

---

## 2. Reasoning effort as an independent axis

Reasoning effort (e.g. `low`/`medium`/`high`/`xhigh`/`max`, or a finer/different staggering per
provider) is an axis **independent of model/role choice**: first pick a fit-for-purpose, live
available model for the role, then stagger its thinking depth to match the difficulty.

- Low levels for routine and well-defined subtasks.
- High levels for science, proof construction, architecture decisions with real consequences.
- A breadth route (parallel, clearly separated subtasks instead of more depth in one strand)
  only when the current runtime offers a dedicated mode for it and the already-applicable
  confirmation/cost rule for larger or hard-to-estimate fan-outs is satisfied.

**No effort level expands write, cost, approval, or publication rights.** Delegations stay within
the existing authority (see Section 5). If a level is unavailable in the current runtime, that is
named and a level that is actually available is used instead — not silently reported as the
success of the planned strategy at a cheaper behavior.

Long-running or compute-intensive individual steps belong — independent of the effort level — on
the designated compute host, not on the local interactive machine; the threshold for that is an
environment rule, not a model-strategy rule.

---

## 3. Mandatory review for draft models

Models in the **draft generator** role deliver a draft by design, never a finished delivery —
regardless of how good the first impression is. This is not a blanket judgment of one specific
model; it is a property of the role: fast first passes are valuable because they are fast, and
exactly for that reason more error-prone.

Three fixed rules follow from this, independent of the concrete model:

1. **Every draft is checked before adoption** — by a worker or reviewer model, never by mere
   trust in the apparent quality of the draft.
2. **A draft model preferably does not write to the target system itself** (target filesystem,
   production database, published location). It returns the result; a vetted model applies it.
   This guardrail is stated concretely in the relevant catalog entry (`guardrails`), because it
   is implemented differently per tool.
3. **Tightly scoped domains** (e.g. LaTeX, legal or numeric text, security-relevant code) get
   **tighter** review than general text, even when the draft model performs well there by
   experience.

---

## 4. Provider switching for independent reviews

A review carries the most weight when author and reviewer **do not share a provider and do not
share a model** — otherwise they may share the same blind spots.

- **Review patterns:**

  | Pattern | How it works | When to use |
  |---|---|---|
  | **Session advisor** | the user sets a reviewer in the running session, the agent calls it deliberately | standard for proof/architecture |
  | **Orchestrator-as-reviewer** | the stronger/coordinating model reviews a worker subagent's output | the orchestrator is already more capable than the worker |
  | **Counter-agent / provider switch** | model A (provider 1) works, model B (provider 2) reviews adversarially | independent verification, two perspectives, highest evidentiary weight |
  | **Recommendation instead of self-execution** | the agent explicitly recommends: "handle this with the escalation role plus review" | the current session is too weak for the step |

- **When to use review:** mathematical proof construction, architecture decisions with long-term
  consequences, statistical methodology/study design, complex bugs after several unsuccessful
  debugging cycles, every draft from Section 3.
- **When review is not needed:** routine code, content, formatting; well-defined, uncritical
  tasks within an already-vetted approach.
- **Documented weaknesses belong in the configuration, not here** — e.g. "model X is unsuitable
  for mathematical reviews" belongs as a `weaknesses` entry in the catalog, because it changes
  with the model, not with the skill.

---

## 5. Permissions attach to the task, not the model

There is deliberately **no permission matrix keyed by model name** (which model may delete,
which may run system commands). Such a matrix suggests permissions are a property of the model —
they are a property of the **task and the granted authority**:

- What an agent may read, write, delete, or execute follows from the current runtime sandbox, the
  scope of the task, and any user approval — not from whether an expensive or a cheap model
  happens to be answering.
- Guardrails in the catalog (`guardrails` field) are **reliability notes**, not a grant or
  restriction of rights: "draft only" says how much to trust the result, not what is technically
  permitted.
- A delegation (to a subagent, an external agent, another model) stays within the authority of
  the delegating run. It expands nothing.

### Escalation and de-escalation (patterns, not model names)

- **Upward (role shifts to thinker/escalation):** an architecture decision is required, several
  systems must be integrated, requirements are contradictory/unclear, strategic planning is
  needed, a critical bug persists after several unsuccessful cycles.
- **Lateral (different role, same level):** out-of-domain research, independent review, a
  specialist tool from another provider.
- **Downward (de-escalation):** the concept is defined → the long-running worker takes over
  implementation; the task is trivial/repetitive → a cheaper model takes over; a pure text task
  with no tool access → a local/token-free model takes over, if actually in inventory and
  verified (`verified: true` in the catalog).

### Transparency rule on model switching

**A silent model switch against the configured roster must be reported.** If a runtime, on its
own initiative (quota, availability, an internal default), picks a different model than the one
set in `models.local.json`/`models.private.json`, that is not an error, but it must be named
transparently — not silently reported as the success of the planned strategy. This applies
regardless of which two specific models are involved; earlier versions of this skill named a
specific model pair as the precedent case — the rule has since been deliberately kept neutral so
it does not hinge on a single model swap.

---

## 6. Budgets, flow, and role assignment — pointers instead of duplicate upkeep

This skill answers **which role** and **with what rigor (effort, review)**. Two neighboring
questions are deliberately not answered here, to avoid duplicate upkeep:

- **"How often may I use an expensive/scarce model?"** → skill `budgetierung`: negotiating quotas
  per time window, a running account, a puzzle-piece pre-check before escalation. `budget_hint`
  in the catalog points exactly here.
- **"How do I break down the task, delegate work packages, and accept results?"** → skill
  `orchestrator` (protocol for decomposing, assigning, accepting) or skill
  `choose-your-orchestrator` (when the right orchestration form itself still needs to be
  negotiated — a session contract for model slots, parallelism, spawn depth, write boundaries,
  acceptance, escalation).

---

## Changelog

### 3.0.0 (2026-10-03) — Breaking: model catalog externalized
- Removed the model catalog from the skill text and moved it to `models.example.json` (tracked,
  neutral) plus a local, unpublished configuration file (`models.local.json` /
  `models.private.json`, already covered by `.gitignore` as private)
- Documented the load order: local file → example file → live discovery; on conflict, the live
  measurement wins; `deprecated: true` is never used
- Replaced the rigid Level-1-through-4 model hierarchy and fixed score→model table with five
  roles (thinker/decision-maker, long-running worker, draft generator, reviewer/acceptance,
  escalation); score remains only a rough orientation
- Added mandatory review for draft models as its own section (review obligation, no direct write
  rights to the target system, tighter review in tightly scoped domains)
- Provider switching for independent reviews as a principle instead of a fixed model-pair
  recommendation
- Removed the permission matrix keyed by model name — permissions attach to the task/authority,
  not the model; guardrails are reliability notes, not a permission clause
- Removed the concrete companion-1.0.4 invocation path, the fixed Ollama/Haiku escalation chain,
  and the Fable/Opus-4.8 precedent rule, folding the latter into a neutral "a silent model switch
  must be reported" rule
- Pointed budgets to the `budgetierung` skill and delegation flow/role assignment to
  `orchestrator`/`choose-your-orchestrator` instead of duplicating them

### 2.2.0 (2026-09-02)
- Added reasoning effort as an axis orthogonal to model choice (`xhigh`, deliberate `max`,
  breadth-oriented `ultracode`)
- Clarified local compute threshold plus runtime, cost, and authority boundaries

### 2.1.0 (2026-07-02)
- PRECEDENT RULE: a specific model replaced another in all Level-4/reviewer/proof
  recommendations (user decision; neutralized with 3.0.0)
- Added silent-model-switch warning

### 2.0.0 (2026-06-12)
- Cross-agent delegation: external agents and a local model as routing targets
- Advisor pairing: 4 patterns (session advisor, orchestrator-as-reviewer, counter-agent,
  user recommendation)
- Reachability matrix: subagent-startable vs. user-only documented
- Lateral escalation to external agents (research, review)
- Extended score thresholds

### 1.0.0 (2026-03-15)
- Ported from BACH v3.8.0 (ing-strategie v2.0.0)

---

*Ported from BACH v3.8.0 | Role-based since 3.0.0*
