---
language: en
description: Mine ideas, filter against history, explore one to completion. A 5-phase workflow (A-E) for complex problem solving.
---

> **English** — Official English version of `idea-mining`.

<img src="banner.png" width="100%" alt="idea-mining banner">

# Idea-Mining — Mine ideas, filter, execute one

## Overview & Purpose

When facing complex problems, ideation rarely fails due to a lack of ideas, but rather due to three things: ideas are not **recorded**, they are not checked against **what has already been tried** (leading to repeating the same dead ends), and none is consistently **pursued to completion**. This workflow strictly separates the three phases: first, mine redundantly/divergently (without evaluation), then filter (against the project documentation), and finally explore ONE idea substantially.

Origin: distilled from a productive research-automation run on open mathematical problems; works equally well for architecture, design, and conceptual blockages.

## Phase A — Fill the Idea Storage (Divergent, Without Evaluation)

Write all findings into a file `IDEENSPEICHER.md` in the project folder (keywords + 2–3 sentences, note source/trigger). Go through the eight techniques sequentially — they target different association spaces, so for truly stuck problems, do not skip any (for minor blockages or tight time, a justified subset is sufficient, but at least one soft technique from 3–5 plus research):

1. **Recognition:** Does this look familiar? Have I seen this structure before in a different context?
2. **Distant Discipline:** Is there a similar problem/formula in a distant discipline (Physics↔Economics, Biology↔Computer Science, …)? Where exactly lies the connection?
3. **Everyday Allegory:** Tell the problem in a nature-inspired allegory (waves, sand, current, growth …). Effective: have an **unbiased subagent** invent the allegory and then see where it leads — your own view is already deformed by the problem.
4. **Discomfort / Frog→Prince:** What bothers me about the current state, what do I find ugly? What would need to change for me to suddenly find it beautiful? Aesthetic discomfort often points to a poorly chosen representation.
5. **Fairy Tale Reframing:** Tell the problem as a fairy tale: Who is the hero, who are the villains, what dangers lurk, what could help the hero? Assigning roles forces a causal structure that remains invisible in formalism.
6. **Research:** Search web, domain databases, preprint servers, forums (Reddit/ResearchGate/GitHub) for new publications, scripts, approaches. Load relevant sources into a `_sources/` folder and read for innovations — remain critical of preprints.
7. **Sibling Projects:** Check related personal/internal projects for back-transferable solution ideas (sub-problems solved there, tools built there).
8. **Inventory Cross-Run:** Review your entire project inventory (pipeline) for approaches that could fit THIS problem.

## Phase B — Filter (Against What Has Been Tried)

Cross-check the idea storage against the project documentation: proof notes, decision logs, TODO/DONE, previous idea storages. **Eliminate what is documented as already tried and completed** — not what merely "sounds unlikely" (evaluation by attractiveness happens only in Phase C). Save surviving ideas to `IDEENSPEICHER_FILTERED.md`.

A prerequisite is well-maintained experiment documentation — if none exists, the first step is to create it (otherwise every future run will produce duplicate efforts).

## Phase C — Choose and Execute

1. Briefly explore one to three ideas from the filtrate (one paragraph each: what would be the first concrete step, what would be the sign of success?).
2. Choose **one** — the one with the strongest attraction. Attraction is a legitimate criterion here: for hard problems, only an idea you *want* to pursue will carry you through.
3. Carry the choice through to the end or at least substantially forward — do not jump to the next idea at the first obstacle (that would be Phase A behavior during Phase C).

## Phase D — Document

- Enter findings into project documentation (proof note, decision log, ADR) — **including failures**, as they form the filter for the next run.
- Put open follow-up ideas back into `IDEENSPEICHER.md` or TODO.
- Short report: mined (count) | filtered (surviving) | explored | result | next step.

## Phase E — Seeding (Optional Outbound Transfer)

Technique 7 brings ideas IN from sibling projects — Phase E reverses the direction: If exploration yields something transferable (method, tool, solution pattern), briefly review your project inventory: Who would this help?

- **Seed selectively, do not scatter:** At most ~3 recipient projects directly provided with a concrete TODO entry (what to adopt, where it is located, why it fits); note further candidates only as a prioritized list in your own project.
- Reason for the limit: Broad scattering creates vague tasks in many projects that no one picks up — three precise seeds beat ten diffuse ones.

## As a Periodic Run

The workflow is well suited as a recurring automation for a fixed project (innovation round). For this, combine it with the rotation scaffolding (`rotation-check` skill): the registry prevents the same ideas from being "rediscovered" multiple times — the idea storage and experiment documentation act as the memory here.

## Example & Application

```text
Problem: A convergence proof has been stuck on an estimate for weeks.

A) Mining → IDEENSPEICHER.md: e.g., (2) similar structure in queueing
   theory?; (3) Subagent allegory "sand trickles through finer and finer sieves" →
   idea: estimate step-by-step instead of globally; (6) 2026 preprint with new
   lemma, downloaded to _sources/; (7) neighboring project has a numerical
   check script that can be transferred back.
B) Filter against BEWEISNOTIZ.md: "tighten global estimate" was tried twice
   and documented as discarded → removed. 3 ideas survive → IDEENSPEICHER_FILTERED.md.
C) Prime Choice: the sieve idea (strongest attraction) — carried through to a partial result.
D) BEWEISNOTIZ.md updated (including failure of idea 2), short report.
```

## Red Flags

| Thought | Reality |
| --- | --- |
| "Techniques 3–5 are just playfulness" | The soft techniques provide the ideas that research cannot deliver — they address different association spaces. |
| "I evaluate while collecting" | Evaluation in Phase A kills divergent yield. Save first, filter later. |
| "The filter takes too long, I already remember" | Memory smooths over failed attempts — only documentation counts. |
| "The idea is stuck, I'll take the next one" | In Phase C you carry through; jumping back to Phase A only with a documented reason. |

## Related Skills

- `brainstorm` — broad creative methods (SCAMPER, Six Hats) without filter/exploration pipeline.
- `think` / `decide` — analysis and selection decision, usable within Phase C.
- `rotation-check` — scaffolding for periodic deployment.
- `swarm-operations` — unbiased subagents for technique 3 and parallel exploration.

## Changelog

### 1.1.0 (2026-07-03)
- Phase E "Seeding": optional outbound transfer of transferable results to
  sibling projects (max. ~3 direct recipients) — integrated instead of a separate
  cross-project-transfer skill (deduplication decision).

### 1.0.0 (2026-07-03)
- Initial version. Abstracted from the Codex automation "ultra-deep-idea-search-single-project"
  (idea storage → filter → prime choice → exploration) and generalized to be user-neutral.
