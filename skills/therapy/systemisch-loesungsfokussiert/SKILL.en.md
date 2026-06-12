---
name: systemisch-loesungsfokussiert
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-05-19
updated: 2026-06-13
description: >
  Systemic and solution-focused methods: miracle question, scaling, exception
  exploration, circular questions, hypothetical questions, worsening questions,
  coping questions. Merged from solution-focused-therapy and systemic-questioning.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [sfbt, systemic, solution-focused, miracle-question, scaling, circular, questioning-techniques, de-shazer]
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
    - "therapy/solution-focused-therapy (v1.0.0, BACH skills/therapie/loesungsfokussierte_therapie.md)"
    - "therapy/systemic-questioning (v1.0.0, BACH skills/therapie/systemische_fragetechniken.md)"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-05-19"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Systemic & Solution-Focused Methods

> Miracle question, scaling, exceptions, circular questions, hypothetical questions — one integrated skill

See: [ETHICS.md](../ETHICS.md)

---

## Foundations

### Solution-Focused Brief Therapy (SFBT)

Developed by Steve de Shazer and Insoo Kim Berg at the Brief Family Therapy Center (Milwaukee).
Core idea: instead of analyzing problems, work directly on solutions.
"Problem talk creates problems, solution talk creates solutions" (de Shazer).

**The three basic rules:**
1. **"If it ain't broke, don't fix it"** — do not change what works
2. **"If it works, do more of it"** — reinforce what succeeds
3. **"If it doesn't work, do something different"** — change what does not help

### Systemic perspective

Problems do not arise within persons but in relationships and patterns between persons.
Questions aim to broaden perspectives, make patterns visible, and open up new possibilities.

**Note:** This is psychoeducation, not a substitute for professional therapy.
**Never implement:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. The miracle question

### Basic form

```
"Imagine that tonight, while you are asleep, a miracle happens.
The problem that has been troubling you is solved.
But you don't know it, because you were asleep.

What would be the first thing tomorrow morning that tells you the miracle has happened?"
```

### Deepening follow-ups

**Sensory level:**
- "What exactly would you do differently tomorrow morning?"
- "How would you get up? What would you do first?"
- "What would you feel when you open your eyes?"

**Relationship level:**
- "How would your partner notice the miracle?"
- "What would he/she see differently about you?"
- "Who in your environment would notice it first?"

**Fractions of the miracle:**
- "Which part of this miracle is perhaps already happening a little bit?"
- "On a scale from 0 to 10 — how far are you already toward the miracle?"

### Shortened variants

- "If the problem were gone tomorrow — what would be different?"
- "What would your ideal everyday life look like?"
- "If everything were the way you wish — what would you be doing?"

---

## 2. Scaling techniques

### Basic structure

"On a scale from 0 to 10, where 0 is [pole A] and 10 is [pole B] — where are you right now?"

### Variants

| Type | Example question |
|------|------------------|
| **State scaling** | "How burdened do you feel right now?" |
| **Coping scaling** | "How well do you manage your everyday life despite the problem?" |
| **Confidence scaling** | "How confident are you that you can make progress?" |
| **Progress scaling** | "Where were you a week / a month ago?" |
| **Relationship scaling** | "Where on the scale would your partner rate your relationship?" |

### The "one point higher" trick

Always ask only about the next point — never about the end goal.

```
"What would be different at a 6 compared to the current 5?"
"What could you do TOMORROW that moves you toward a 6?"
```

### Follow-up questions (essential!)

- "What has kept you from being at 0?" (resource activation)
- "What would have to happen for you to move one point higher?" (small-step solution orientation)
- "How would you notice that you are at [target value]?" (concretization)

---

## 3. Exception exploration

### Principle

Exceptions are moments in which the problem does not occur or occurs less.
They already contain working solution elements.

### Systematic search

**Phase 1 — Find:**
- "When was it recently a bit better — even minimally?"
- "Are there days when the problem is less intense?"

**Phase 2 — Describe in detail:**
- "Describe that moment as precisely as possible"
- "What was different about that day?"

**Phase 3 — Recognize one's own contribution:**
- "What did YOU contribute to it being better?"
- "What decision did you make?"

**Phase 4 — Reinforce:**
- "How could you deliberately repeat that?"
- "What would be a first small step in that direction?"

### Types of exceptions

| Type | Description | Follow-up |
|------|-------------|-----------|
| Deliberate | The client consciously did something differently | "Do more of it!" |
| Random | Something was different without conscious action | "What was different about the circumstances?" |
| External | Others did something | "What could you do to make that more likely?" |

---

## 4. Circular questions

### Principle

Encourage perspective shifts — the person is invited to put themselves in others' positions and to recognize relationship patterns.

### Basic structure

"What do you think — how does [person X] see/feel/judge this?"

### Variants

**Relationship questions:**
- "What do you think your partner thinks when you withdraw?"
- "How would your best friend describe your relationship?"
- "If I asked your brother what the biggest problem in the family is — what would he say?"

**Difference questions:**
- "Who in the family suffers most from the situation?"
- "Who notices the change first?"

**Agreement questions:**
- "Would your partner agree with that?"
- "Who in your environment sees it similarly to you?"

**Classification questions:**
- "If you ranked your family members by who handles conflict best — what would the order be?"

---

## 5. Hypothetical questions

Open new thinking spaces, loosen rigid convictions, rehearse options for action.

- "Suppose you just tried it — what could happen in the best case?"
- "What would happen if you did the opposite of what you normally do?"
- "If you were to give advice to someone in the same situation — what would you say?"
- "If fear played no role — what would you do?"
- "If you looked back at today from 5 years in the future — what would you advise yourself?"

---

## 6. Worsening questions (paradoxical intervention)

Strengthen the sense of control: whoever can describe how to make the problem worse has influence — and can therefore also improve it.

- "What could you do to make it guaranteed worse?"
- "How could you make sure the argument escalates?"
- "What would have to happen for everything to go completely wrong?"

**Important:** NOT suitable in acute crisis, suicidality, or severe depression.

---

## 7. Coping questions & resource comments

- "How do you still manage to get up every day?"
- "What keeps you going?"
- "I am impressed that you are here despite the difficulties."

---

## Context-sensitive selection

| Situation | Recommended technique | Rationale |
|---|---|---|
| Person is stuck in the problem | Miracle question | Releases from the problem trance |
| Progress not visible | Scaling questions | Makes small steps measurable |
| Relationship conflicts | Circular questions | Enables perspective shifts |
| "It is ALWAYS like this" | Exception questions | Breaks generalization |
| Fear of change | Hypothetical questions | Risk-free trial thinking |
| Helplessness / loss of control | Worsening questions | Shows one's own influence |
| Unclear goals | Miracle question + scaling | Clarifies direction and starting point |

---

## Combination patterns

### Scaling + exception + small step

1. "On a scale of 0-10, where are you right now?" → e.g. "4"
2. "What has kept you from being at 0?" (resources!)
3. "Were there moments when you were at 5 or higher?" (exceptions!)
4. "What was different then?" (recognize patterns!)
5. "What would be the smallest step to get from 4 to 5?" (action!)

### Miracle question + circular + scaling

1. Ask the miracle question (create a target image)
2. "Who would notice it first?" (circular — relationship context)
3. "How far along are you already on the way to the miracle?" (scaling — progress)

### Circular + hypothetical

1. "What do you think — how does your boss see the situation?"
2. "Suppose he said exactly that — what could you do then?"

---

## Reflection questions for self-application

- "What works well in my life — and how do I do that?"
- "What is a small exception I could build on?"
- "If the problem were gone tomorrow — what would I do first?"
- "What have I managed before, even though it was hard?"

---

## Dos and Don'ts

### Dos
- **Ask openly** — no leading questions
- **Stay curious** — the answer is more valuable than the question
- **Allow pauses** — good questions need time
- **Build on answers** — follow-up matters more than the next technique
- **Phrase appreciatively** — "What did you succeed at?" instead of "What did you do wrong?"

### Don'ts
- **Do not interrogate** — max. 2-3 questions in a row, then reflect
- **Not in acute crisis** — stabilize first, then explore
- **Not as manipulation** — questions must be authentically curious
- **Never use worsening questions with suicidality** — never

---

## Ethics and limits

**An AI assistant may:**
- Explain and contextualize SFBT and systemic concepts
- Guide the miracle question, exception exploration, and scaling
- Ask circular and hypothetical questions
- Ask reflection questions and point out resources

**An AI assistant may NOT:**
- Conduct or replace therapy
- Trivialize persistent problems ("just think positive")
- Brush over acute crises with solution orientation
- Give relationship counseling that replaces professional therapy
- Use worsening questions in fragile states

**At signs of an acute crisis, ALWAYS refer to local emergency services and crisis hotlines** (in Germany e.g.: Telefonseelsorge 0800 111 0 111 / 0800 111 0 222, psychiatric emergency service 112, krisenchat.de).

---

## References

- de Shazer, S. (1985). *Keys to Solution in Brief Therapy.* Norton.
- de Shazer, S. (1988). *Clues: Investigating Solutions in Brief Therapy.* Norton.
- Berg, I. K. & Miller, S. D. (1992). *Working with the Problem Drinker.* Norton.
- Berg, I. K. & Dolan, Y. (2001). *Tales of Solutions.* Norton.
- Selvini Palazzoli, M. et al. (1981). *Hypothesizing — Circularity — Neutrality.*
- Schlippe, A. von & Schweitzer, J. (2012). *Lehrbuch der systemischen Therapie und Beratung.*
- Gingerich, W. J. & Peterson, L. T. (2013). Effectiveness of Solution-Focused Brief Therapy. *Research on Social Work Practice*, 23(3), 266-283.
- Kim, J. S. et al. (2019). Solution-Focused Brief Therapy: A Meta-Analysis. *Journal of Marital and Family Therapy*, 45(2), 271-286.

---

## Changelog

### 1.0.0 (2026-05-19)
- Merged from `solution-focused-therapy` (v1.0.0) and `systemic-questioning` (v1.0.0)
- All unique content of both sources integrated

---

*Merged from BACH v3.8.0 exports | Standalone version*
*Not professional therapy — psychoeducation and reflection*
