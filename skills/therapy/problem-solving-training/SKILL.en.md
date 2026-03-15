---
name: problem-solving-training
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Structured problem solving in 6 steps: Problem definition, goals, brainstorming, evaluation, implementation, and review.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [problem-solving, decision, structured, six-steps, coping]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/problemloese_training.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Problem-Solving Training

> Structured problem solving in 6 steps according to D'Zurilla and Goldfried: Approaching problems systematically instead of ruminating in circles

See: [ETHICS.md](../ETHICS.md)

---

## Context

Problem-Solving Training (Social Problem-Solving, SPS) is an evidence-based intervention from cognitive behavioral therapy. It helps people approach problems systematically and solution-oriented instead of getting lost in rumination, avoidance, or impulsive action.

Evidence: Meta-analyses show significant effects for depression (d=0.83), anxiety disorders, and stress (Malouff et al. 2007, Bell & D'Zurilla 2009).

**Note:** This is support, not a substitute for professional therapy.
**Never implement:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Problem-Solving Orientation

Before the actual steps begin, the inner attitude is decisive.

### Helpful Attitude
- "Problems are part of life — they are solvable"
- "I can proceed step by step"
- "There is rarely only one right solution"
- "Not acting is also a decision — usually not a good one"

### Unhelpful Attitude
- "None of this makes any sense"
- "I can't do it anyway"
- "There is no solution"
- Impulsive action without thinking
- Avoidance and procrastination

**First step:** Reflect on your own problem-solving attitude.

---

## 2. The 6-Step Model

### Step 1: Define the Problem

**Goal:** Formulate the problem clearly, concretely, and manageably.

**Guide questions:**
- What exactly is the problem? (Facts, not interpretations)
- Who is involved?
- When and where does it occur?
- Why is it a problem for me?

**Worksheet:**

```
PROBLEM DEFINITION

Situation: [What is happening concretely?]
People involved: [Who is involved?]
Frequency: [How often? When?]
Impact: [What makes it a problem?]

Concrete problem statement:
[...]
```

**Common mistakes:**
- Problem too vague ("Everything is bad")
- Mixing multiple problems together
- Including the solution in the problem statement

---

### Step 2: Set Goals

**Goal:** What should be different after solving the problem?

**SMART Criteria:**
- Specific: What exactly?
- Measurable: How will I recognize success?
- Attractive: Why do I want this?
- Realistic: Is it achievable?
- Time-bound: By when?

**Worksheet:**

```
GOAL SETTING

My goal: [...]
How will I know I've achieved it? [...]
By when? [...]
Realistic (0-10)? [...]
Important to me (0-10)? [...]
```

---

### Step 3: Generate Alternatives (Brainstorming)

**Goal:** Generate as many solution ideas as possible — without immediate evaluation.

**Brainstorming rules:**
1. Quantity over quality — the more ideas, the better
2. No evaluation during collection
3. Creative and unusual thinking is allowed
4. Combine and vary existing ideas

**Worksheet:**

```
BRAINSTORMING

Solution ideas (at least 5-8):
1. [...]
2. [...]
3. [...]
4. [...]
5. [...]
6. [...]
7. [...]
8. [...]
```

**Helper questions:**
- "What would someone do who doesn't have this problem?"
- "What have I done in similar situations before?"
- "What would I advise a friend?"
- "What would be the boldest solution?"
- "What would be the simplest solution?"

---

### Step 4: Evaluate Alternatives

**Goal:** Systematically weigh pros and cons of each alternative.

**Evaluation criteria:**
- Effectiveness: Does it solve the problem?
- Feasibility: Can I implement it?
- Time required: How long will it take?
- Consequences: For me? For others?
- Risks: What could go wrong?

**Worksheet:**

```
EVALUATION MATRIX

| Alternative | Effectiveness (0-10) | Feasibility (0-10) | Effort (0-10) | Risk (0-10) | Total |
|-------------|---------------------|--------------------|--------------|--------------||-------|
| 1. [...]    |                     |                    |              |              |       |
| 2. [...]    |                     |                    |              |              |       |
| 3. [...]    |                     |                    |              |              |       |

Preferred solution: [...]
Reasoning: [...]
```

---

### Step 5: Implement

**Goal:** Concretely plan and carry out the chosen solution.

**Action plan:**

```
ACTION PLAN

Chosen solution: [...]

Concrete steps:
1. [What?] — [When?] — [Where?]
2. [What?] — [When?] — [Where?]
3. [What?] — [When?] — [Where?]

Possible obstacles: [...]
Plan B: [...]
Support I need: [...]
First step (today/tomorrow): [...]
```

---

### Step 6: Evaluate

**Goal:** Review the outcome and adjust if needed.

**Evaluation questions:**
- Was the problem solved? (Fully / partially / not at all)
- Am I satisfied with the result? (0-10)
- What worked well?
- What would I do differently next time?
- Do I need a new attempt with a different alternative?

**Worksheet:**

```
EVALUATION

Result: [Solved / Partially / Not solved]
Satisfaction (0-10): [...]
What worked: [...]
What didn't: [...]
Next step: [Conclude / New attempt / Different approach]
```

---

## 3. Common Problems in Problem Solving

| Problem | Remedy |
|---------|--------|
| "I don't know where to start" | Back to Step 1, formulate problem smaller |
| "No solution is good enough" | Question perfectionism, accept "good enough" |
| "I don't dare" | Identify the smallest possible step |
| "It doesn't work" | Evaluation: What exactly doesn't work? New attempt |
| Problem is too big | Break into sub-problems, one at a time |
| Emotions block | First emotion regulation (breathing, PMR), then problem solving |

---

## Ethics and Boundaries

**An AI assistant may:**
- Guide through the 6 steps and provide worksheet structure
- Ask brainstorming questions
- Support evaluation of alternatives
- Document progress

**An AI assistant must NOT:**
- Prescribe solutions or suggest "the right answer"
- Conduct relationship or life counseling in the therapeutic sense
- Be the sole support for severe psychological distress
- Make diagnoses

**In case of acute crisis, ALWAYS refer to:**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- Emergency services: 911 (US) / 112 (EU)

---

*Ported from BACH v3.8.0 | Standalone Version*
*Sources: D'Zurilla & Goldfried (1971), Nezu et al. (2013), Malouff et al. (2007) — Not professional therapy*
