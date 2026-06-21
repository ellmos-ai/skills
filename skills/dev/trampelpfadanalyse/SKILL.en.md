---
name: trampelpfadanalyse
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-06-21
updated: 2026-06-21
description: >
  Error analysis for pipeline and control-file workflows: check whether a convention
  or procedure is actually visible and discoverable to an LLM. Empirical baseline →
  intervention → retest comparison using naive subagents (isolated sandbox copies,
  identical test case, quantitative success measurement). Use this skill when agents
  repeatedly ignore a rule/README/convention or navigate incorrectly, and you want to
  measure whether a documentation change actually changes the behavior. Triggers on
  "is the convention even seen", "why does no agent follow the rule", "make a doc
  signpost measurably effective", "desire-path analysis", "trampelpfadanalyse".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: dev
tags: [workflow, error-analysis, llm-ux, doc-audit, baseline-retest, naive-subagent, empirical, pipeline, control-file]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/workflows/system/trampelpfadanalyse.md"
  origin_version: "2.0"
  origin_repo: "github.com/ellmos-ai/swarm-ai"
  last_sync_from_origin: "2026-06-21"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Desire-Path Analysis — Making Conventions Empirically Visible to LLMs

A method for uncovering errors in pipeline and control-file workflows that do not come
from broken code, but from a **convention being invisible to an LLM**. Instead of
guessing whether a README or rule is "clear enough", you measure it empirically: naive
subagents with no prior knowledge are turned loose on the workflow, their behavior
becomes the **baseline**, a targeted documentation change (a "signpost") is the
**intervention**, and fresh naive subagents provide the **retest**. The diff against the
baseline is the success measurement.

The name comes from the *desire path* (German: *Trampelpfad*): where people actually walk
instead of on the paved route is where a path belongs. By analogy, the paths of naive
LLMs show where documentation/guardrails are actually needed — not where we assume them.

## When to use this skill

- Agents repeatedly ignore a rule/convention even though it is documented.
- You want to know whether a procedure is **visible/discoverable** to an LLM before
  writing more docs ("is anyone here talking to a wall?").
- After a restructuring (new directories, renames): can agents still find the entry points?
- You made a documentation change and want to **prove** it works — not just hope so.
- Onboarding test before integrating new LLM partners into a pipeline.

Not for: pure code bugs (→ systematic debugging), or selecting swarm coordination patterns
for a production task (→ see `swarm-operations`). This skill uses a swarm of naive agents
exclusively as a **measuring instrument**.

## Core idea in one sentence

Treat documentation like UX: what counts is not what you wrote, but what an unbiased user
(here: a naive agent) actually does with it — and you measure that, change it, and measure
again.

---

## The process: 5 steps

```
1. BASELINE       naive subagents → measure current behavior (quantitative)
2. PATH ANALYSIS  where exactly does it fail? which doc location misleads?
3. INTERVENTION   put up a "signpost" (README/convention made more prominent)
4. RETEST         FRESH naive subagents, identical test case
5. DIFF           retest vs. baseline → success measurement + honest assessment
```

### Step 1 — Baseline: measure current behavior naively

First phrase the problem as a **testable question**, e.g. "Does an agent create a log at
the convention-mandated location?" or "Does an agent find the pipeline's entry point?".

Then turn naive subagents loose:

- **Naive means:** no project memory, no skills, no prior hints — the agent only knows the
  entry path and the task. This measures **pure discoverability via the existing docs**,
  not the agent's prior knowledge.
- **Isolated sandbox copies:** each probe agent works on its own copy of the affected
  folder/workflow, so probes do not influence each other and the real state stays untouched.
- **Same test case, multiple repetitions:** variability is real. One probe is an anecdote;
  n repetitions (e.g. 3, or more if needed) yield a rate.
- **A cheap, "naive" model** is sufficient and realistic — it should not guess cleverly,
  but show where the docs lead an average agent.

Minimal probe prompt (adjust placeholders):

```
You are exploring <SYSTEM>. It is located at: <PATH>.
TASK: <specific task>.
RULES:
1. You only know the path above, nothing else.
2. Explore to complete the task. Max. <N> steps.
3. Report at the end: VISITED_DIRECTORIES, READ_FILES,
   TASK_COMPLETED (yes/no), MOST_HELPFUL_FILE.
```

**Record as baseline metrics** (always quantitative, never "feels better"):

| Metric | Meaning |
|---|---|
| Success rate | how often the task was completed per convention (e.g. 0/3) |
| Wrong behavior | how often the wrong location/method (e.g. 3/3 collective log instead of per-entry) |
| Paths to goal | how many steps/detours to reach the goal |
| Blind spots | which relevant file/location nobody opens |

### Step 2 — Path analysis: where does it really fail?

Evaluate the probe reports together (a "heatmap" of visited locations is enough):

- Which file is read **often** (HOT)? If orientation is missing there, that is the most
  effective place for a signpost.
- Which relevant location is **never** opened (COLD / blind spot)? It is effectively
  invisible — no matter how good its content is.
- Where does an agent loop or bypass the convention (dead end, circumvention)? That marks
  the concrete documentation gap.

Findings table:

| Finding | Meaning | Action (→ Step 3) |
|---|---|---|
| HOT + no orientation | high traffic, no signpost | place the signpost right there |
| WARM + errors | agents arrive, stumble | add example/clarification |
| COLD | location is never found | link to it from a HOT file |
| Circumvention | convention is bypassed | hint at the point of circumvention |

Outcome of Step 2: **one concrete, localized hypothesis** — "Agents read X, but X does not
mention the convention; that is why they end up at Y."

### Step 3 — Intervention: put up a signpost

Put up **exactly one** signpost (one variable per pass, otherwise the diff is not
interpretable). Typical signposts:

- Place the convention **prominently where the HOT path already passes** (e.g. a short,
  explicit hint at the very top of the most-read README/control file).
- A **quick-navigation table** at the start of the central architecture/overview file that
  points to former blind spots.
- A **signpost/cross-reference** from a HOT file to a COLD location.
- Optionally a **guardrail** (e.g. a PreToolUse hint) for dangerous or convention-violating
  actions.

Keep the signpost short and unmissable — agents skim, they rarely read at length.

### Step 4 — Retest with FRESH naive subagents

Repeat Step 1 **identically** — same task, same number of repetitions, same model, same
naive condition — but on sandbox copies **with** the new signpost. Important:

- **Fresh** agents with no memory of the baseline run (otherwise you measure learning, not
  discoverability).
- **Only the signpost** differs from the baseline setup.

### Step 5 — Diff against baseline + honest success measurement

Put retest and baseline directly side by side:

| Metric | Baseline | After signpost | Δ |
|---|---|---|---|
| Success rate | e.g. 0/3 | e.g. 3/3 | +3 |
| Wrong behavior | e.g. 3/3 | e.g. 0/3 | −3 |
| Blind spots | e.g. 1 | e.g. 0 | −1 |

Assessment — and do not sugarcoat here:

- **Works** (wrong behavior measurably drops): keep the signpost, document it.
- **Does not work** (little Δ): the signpost was in the wrong place or too subtle → back to
  Step 2/3, different signpost, measure again.
- **State limits openly:** small n are indicators, not proofs; a naive agent models "average
  uninformed", not every real user; explicitly check for false positives/negatives in the
  success scoring (what exactly counted as "completed"?).

---

## Mini case study (real, with actual numbers)

Problem: A ticket pipeline mandated that trivial completions each get **one** dedicated
per-ticket log — but agents instead put everything into **one collective log**.

- **Step 1 (baseline):** 3 naive subagents, same task → **3/3 used the collective log**
  (convention not followed).
- **Step 2 (path analysis):** the most-read README did not mention the per-ticket rule at a
  visible spot → the naive path led to the collective log.
- **Step 3 (intervention):** a short, explicit "signpost" about the logging convention
  placed prominently in the README.
- **Step 4 (retest):** 3 fresh naive subagents, identical task.
- **Step 5 (diff):** **3/3 wrong → 0/3 wrong**, all three created a correct per-ticket log.
  (Documented in ticket T-20260621-44.)

Lesson: The convention was not "worded too weakly" — it was **invisible** on the path that
was actually read. The signpost in the right place, empirically verified, solved the problem.

---

## Source and related methods

This method comes from Desire-Path Analysis v2.0 (swarm as an empirical measuring instrument
for LLM behavior). The original reference results of a large run (100 naive probes) are
documented as evidence from the source: the biggest blind spot was a help directory that
**0/100** agents visited (despite many help files), and the task "create a new skill"
succeeded **0%** because nobody found the templates directory — both classic visibility, not
content, problems.

## See also

- `swarm-operations` (dev) — catalog of swarm **coordination patterns** for production
  tasks; it carries desire-path analysis only as a conceptual section. This skill is the
  applicable **process** variant with a baseline→retest loop.
- `pipeline-optimizer` (dev) — 6-step pipeline renovation; its retest with fresh subagents
  corresponds to Steps 4–5 here.
- `bugfix-protocol` / systematic debugging — for real code bugs rather than visibility
  problems.

## Changelog

### 0.1.0 (2026-06-21)
- Initial port from Desire-Path Analysis v2.0 (source: swarm-ai/BACH).
- Focused on the applicable 5-step process (baseline → path analysis → intervention →
  retest → diff); swarm coordination patterns deliberately omitted (they stay in
  `swarm-operations`). User-neutral with placeholders; real mini case study.
