---
name: structured-thinking
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-05-19
updated: 2026-05-19
description: >
  Meta-skill: Structured thinking as a 3-phase workflow. Combines analysis (think),
  ideation (brainstorm), and decision-making (decide) into one continuous process.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: utilities
tags: [denken, analyse, kreativitaet, entscheidung, workflow, meta-skill]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  merged_from:
    - "utilities/think (v1.0.0)"
    - "utilities/brainstorm (v1.0.0)"
    - "utilities/decide (v1.0.0)"
  local_changes_since_sync: false
---

# Structured Thinking — Analyze, Ideate, Decide

> Meta-workflow for structured thinking: from problem analysis through creative solutions to a well-founded decision

---

## Workflow Overview

```
Problem/Question
     |
     v
Phase 1: ANALYZE (think)
  Divide & Conquer, Root Cause, Constraint Relaxation
     |
     v
Phase 2: IDEATE (brainstorm)
  SCAMPER, Six Hats, Reverse Brainstorming, Rapid Ideation
     |
     v
Phase 3: DECIDE (decide)
  Pro/Con, Weighted Scoring, Scenario Analysis, Eisenhower
     |
     v
Result + Rationale
```

---

## Phase 1: Analyze

Goal: Understand the problem, identify causes, recognize structure.

### Approaches

| Method | When | Procedure |
|--------|------|-----------|
| **Divide & Conquer** | Complex problem | Problem → sub-problems → solve individually → combine |
| **Root Cause (5x Why)** | Symptom visible, cause unclear | Symptom → Why? → Why? → ... → cause → solution |
| **Constraint Relaxation** | Problem appears unsolvable | Relax constraints → solve → re-tighten constraints |
| **Analogy Search** | Novel problem | Find a similar known problem → adapt its solution |

### Analysis Frameworks

| Framework | Application |
|-----------|-------------|
| **SWOT** | Strengths / Weaknesses / Opportunities / Threats |
| **Pareto** | 80/20 — What provides the biggest leverage? |
| **Fishbone** | Systematic cause analysis (Ishikawa) |

### Heuristics under Uncertainty

1. What is the worst-case scenario?
2. Is it reversible?
3. What is the cost of not acting?

### Heuristics under Complexity

1. What is the simplest first step?
2. What would an expert do?
3. What would the 80% solution be?

---

## Phase 2: Ideate

Goal: Generate as many solution approaches as possible. Quantity over quality. NO criticism during this phase.

### Methods

**SCAMPER** — Systematically improve existing solutions:
- **S**ubstitute: What to replace? | **C**ombine: What to combine? | **A**dapt: What to adapt?
- **M**odify: What to change? | **P**ut to other use: What else could it serve? | **E**liminate: What to drop?
- **R**everse: What to invert?

**Six Thinking Hats** (de Bono) — 6 perspectives in sequence:
1. Blue: Process control ("What is the question?")
2. White: Facts ("What do we know?")
3. Red: Emotion ("What feels right?")
4. Black: Criticism ("What could go wrong?")
5. Yellow: Optimism ("What are the opportunities?")
6. Green: Creativity ("What new ideas are there?")

**Reverse Brainstorming** — Invert the problem:
1. "How do we make it WORSE?"
2. Collect bad ideas
3. Invert = good ideas

**Rapid Ideation** — 50+ ideas in 20 minutes:
- Round 1 (5 min): Open ideation
- Round 2 (5 min): Variations
- Round 3 (5 min): Combinations
- Round 4 (5 min): Extreme ideas

### After Ideation

1. Clustering: Group similar ideas
2. Feasibility/Impact matrix: Rate feasibility vs. impact
3. Select top 5-10 for Phase 3

---

## Phase 3: Decide

Goal: Select the best option with a transparent rationale.

### Framework Selection

| Situation | Framework |
|-----------|-----------|
| 2 options, quick decision | **Pro/Con Matrix** |
| 3+ options, multiple criteria | **Weighted Scoring** |
| Sequential if-then decision | **Decision Tree** |
| High uncertainty | **Scenario Analysis** |
| Prioritizing tasks | **Eisenhower Matrix** |

### Weighted Scoring (core method)

1. Collect criteria (3-7, specific and measurable)
2. Set weights (sum = 100%, most important >= 25%)
3. Rate options (1-10 scale)
4. Compute scores (rating x weight)
5. Compare and recommend

### Scenario Analysis

```
Best Case (X%):      Outcome → expected value
Realistic Case (X%): Outcome → expected value
Worst Case (X%):     Outcome → expected value
Total expected value: [sum]
```

### Eisenhower Matrix

```
              URGENT          NOT URGENT
IMPORTANT     1. DO           2. PLAN
NOT IMPORTANT 3. DELEGATE     4. ELIMINATE
```

### Quality Checklist before the Final Recommendation

- [ ] All relevant criteria identified?
- [ ] User values taken into account?
- [ ] Long-term effects considered?
- [ ] Risks identified and assessed?
- [ ] Bias check performed?
- [ ] Reversibility checked?

---

## Context-Sensitive Selection

| Situation | Recommended Phase(s) |
|-----------|----------------------|
| "I have a problem" | Phase 1 (analysis) → possibly Phase 2+3 |
| "I need ideas" | Phase 2 (ideation) |
| "I have to decide" | Phase 3 (decision) |
| "I am stuck" | Phase 2 (reverse brainstorming) |
| "What should I prioritize?" | Phase 3 (Eisenhower) |
| "Understand a complex problem" | Phase 1 (Divide & Conquer + SWOT) |

---

## Changelog

### 1.0.0 (2026-05-19)
- Created as a meta-skill from think, brainstorm, and decide

---

*Meta-skill | Detailed reference: [think](../think/SKILL.md), [brainstorm](../brainstorm/SKILL.md), [decide](../decide/SKILL.md)*
