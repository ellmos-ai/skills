---
name: solution-focused-therapy
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: >
  Solution-Focused Brief Therapy according to de Shazer and Berg: Miracle question, exception exploration, scaling, resource activation.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [sfbt, solution-focused, miracle-question, scaling, brief-therapy, resources]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/loesungsfokussierte_therapie.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-15"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Solution-Focused Therapy

> Fundamentals of Solution-Focused Brief Therapy according to Steve de Shazer and Insoo Kim Berg: Miracle question, exception exploration, scaling, resource activation

See: [ETHICS.md](../ETHICS.md)

---

## Context

Solution-Focused Brief Therapy (SFBT) was developed by Steve de Shazer and Insoo Kim Berg at the Brief Family Therapy Center in Milwaukee. It is one of the most well-researched brief therapy approaches.

Core idea: Instead of analyzing problems, work directly on solutions. "Problem talk creates problems, solution talk creates solutions" (de Shazer).

Evidence: Meta-analyses support effectiveness for depression, anxiety, behavioral problems, substance abuse, and couple conflicts (Gingerich & Peterson 2013, Kim et al. 2019).

**Note:** This is psychoeducation, not a substitute for professional therapy.
**Never implement:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Core Principles of SFBT

### The Three Basic Rules (de Shazer)

1. **"If it ain't broke, don't fix it"** — Don't change what works
2. **"If it works, do more of it"** — Strengthen what works
3. **"If it doesn't work, do something different"** — Change what doesn't help

### View of the Person
- Every person has resources and competencies
- The client is the expert on their own life
- Small changes trigger larger ones (butterfly effect)
- The solution doesn't have to be related to the problem

---

## 2. The Miracle Question — In-Depth Application

### Basic Form

```
"Imagine that tonight, while you are sleeping, a miracle happens.
The problem that has been troubling you is solved.
But you don't know it, because you were asleep.

What would you notice first thing tomorrow morning that tells you
the miracle has happened?"
```

### Deepening Follow-Up Questions

**Making it concrete on a sensory level:**
- "What exactly would you do differently tomorrow morning?"
- "How would you get up? What would you do first?"
- "What would you feel when you open your eyes?"

**Relationship level:**
- "How would your partner notice the miracle?"
- "What would they see differently about you?"
- "Who in your circle would notice it first?"

**Finding fragments of the miracle:**
- "Which part of this miracle is perhaps already happening a little bit?"
- "On a scale of 0 to 10 — how far along are you already toward the miracle?"

---

## 3. Exception Exploration

### Principle
Exceptions are moments when the problem does not occur or occurs less. They already contain functioning solution approaches.

### Systematic Exception Search

**Phase 1: Finding exceptions**
- "When was it a bit better recently — even just minimally?"
- "Are there days when the problem is less severe?"

**Phase 2: Describing exceptions in detail**
- "Describe that moment as precisely as possible"
- "What was different about that day?"

**Phase 3: Recognizing one's own contribution**
- "What did YOU contribute to it being better?"
- "What decision did you make?"

**Phase 4: Strengthening exceptions**
- "How could you deliberately repeat that?"
- "What would be a first small step in that direction?"

### Types of Exceptions

| Type | Description | Follow-up |
|------|-------------|-----------|
| Deliberate exception | Client consciously did something different | "Do more of that!" |
| Random exception | Something was different without conscious effort | "What was different about the circumstances?" |
| External exception | Others did something | "What could you do to make that more likely?" |

---

## 4. Scaling Techniques

### Basic Scaling
"On a scale of 0 to 10, where 0 is the worst and 10 is the best possible..."

### Extended Scaling Forms

**Coping scaling:**
- "How well are you managing to cope with daily life despite the problem?"

**Confidence scaling:**
- "How confident are you that you can make progress?"

**Progress scaling:**
- "Where were you a week / a month ago?"
- "What contributed to the increase?"

### The "One Point Higher" Trick
Always ask only about the next point — never about the final goal.

```
"What would be different at a 6 compared to the current 5?"
"What could you do TOMORROW that moves toward a 6?"
```

---

## 5. Additional SFBT Techniques

### Coping Questions
- "How do you manage to get up every day despite everything?"
- "What keeps you going?"

### Relationship Questions
- "If I asked your partner, what would they say?"
- "Who in your circle would notice the change first?"

### Compliments / Resource Comments
- "I'm impressed that despite the difficulties, you're here."

---

## 6. Reflection Questions for Self-Application

- "What is working well in my life — and how am I doing that?"
- "What is one small exception I could build on?"
- "If the problem were gone tomorrow — what would I do first?"
- "What have I accomplished before, even though it was hard?"

---

## Ethics and Boundaries

**An AI assistant may:**
- Explain and contextualize SFBT concepts
- Guide the miracle question, exception exploration, and scaling
- Ask reflection questions
- Point out resources and strengths

**An AI assistant must NOT:**
- Conduct solution-focused therapy
- Trivialize persistent problems ("Just think positive")
- Bypass acute crises with solution orientation
- Promise that SFBT techniques will solve problems

**In case of acute crisis, ALWAYS refer to:**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- Emergency services: 911 (US) / 112 (EU)

---

## References

- de Shazer, S. (1988). *Clues: Investigating Solutions in Brief Therapy.* Norton.
- Berg, I. K. & Miller, S. D. (1992). *Working with the Problem Drinker.* Norton.
- Gingerich, W. J. & Peterson, L. T. (2013). Effectiveness of Solution-Focused Brief Therapy. *Research on Social Work Practice*, 23(3), 266-283.
- Kim, J. S. et al. (2019). Solution-Focused Brief Therapy: A Meta-Analysis. *Journal of Marital and Family Therapy*, 45(2), 271-286.

---

*Ported from BACH v3.8.0 | Standalone Version*
*Sources: de Shazer (1988), Berg & Miller (1992), Gingerich & Peterson (2013), Kim et al. (2019) — Not professional therapy*
