---
name: cognitive-restructuring
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Cognitive Behavioral Therapy: ABC model, automatic thoughts, identifying cognitive distortions, and keeping thought records.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [cbt, cognitive-restructuring, cognitive-distortions, thought-record, abc-model]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/kognitive_umstrukturierung.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Cognitive Restructuring

> Core CBT technique: ABC schema, identifying and modifying dysfunctional thoughts

See: [ETHICS.md](../ETHICS.md)

---

## Context

Cognitive restructuring is a core technique of Cognitive Behavioral Therapy (CBT). It helps identify automatic negative thoughts, challenge them, and replace them with more helpful alternatives.

**Note:** This is support, not a substitute for professional therapy.
**Never implement:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. ABC Model (Ellis)

The ABC model explains how events, thoughts, and feelings are connected.

```
A (Activating Event)   ->  B (Beliefs / Thoughts)  ->  C (Consequences / Feelings/Behavior)
Trigger                     Evaluation / Belief           Emotional consequence
```

**Important:** It is not the event (A) that creates the emotion (C), but the evaluation (B)!

**Example:**
```
A: Boss criticizes a report in a meeting
B: "I am incompetent, everyone thinks so now"
C: Shame, withdrawal, avoiding future contributions
```

**Goal:** Change B to influence C.

---

## 2. Identifying Automatic Negative Thoughts (ANTs)

**What are ANTs?**
- Quick, automatic evaluations in stressful situations
- Often perceived as facts, although they are interpretations
- Tend toward exaggeration, generalization, catastrophizing

**Typical recognition features:**
- Absolute thinking: "always," "never," "everyone," "nobody"
- Catastrophizing: "This will end terribly"
- Mind reading: "They must think that..."
- Overgeneralization: "This never works for me"

**Recognition questions:**
- "What went through your mind when that happened?"
- "When you think about the situation, what words come up?"
- "What do you fear might happen?"

---

## 3. Cognitive Distortions (Thinking Errors)

| Distortion | Description | Example |
|------------|-------------|---------|
| All-or-nothing | Black-and-white thinking | "If I'm not perfect, I'm a failure" |
| Overgeneralization | One case = general pattern | "This always goes wrong for me" |
| Mental filter | Only perceiving negatives | Focusing on the single criticism in feedback |
| Mind reading | Believing to know what others think | "They surely hate me" |
| Catastrophizing | Assuming the worst case | "This will be a catastrophe" |
| Emotional reasoning | Feeling = reality | "I feel stupid, so I am stupid" |
| Should/must thinking | Rigid rules | "I should be able to do this" |
| Personalization | Relating everything to oneself | "The bad project was my fault" |

---

## 4. Challenging Thoughts (Socratic Questioning)

**Goal:** Not directly refute thoughts, but encourage examination.

**Question set:**

1. **Examine evidence:**
   - "What evidence is there for this?"
   - "What evidence speaks against it?"

2. **Alternative explanations:**
   - "Are there other explanations for this?"
   - "How would someone else view this situation?"

3. **Assess consequences:**
   - "What is the worst that could happen? How likely is that?"
   - "What is the best that could happen?"
   - "What is the most realistic outcome?"

4. **Check usefulness:**
   - "Does this thought help me achieve my goals?"
   - "What would I say to a good friend who thinks this way?"

---

## 5. Cognitive Restructuring Step by Step

### Record Format (Thought Record)

```
SITUATION
What happened? (When? Where? Who was there?)
[Free text]

THOUGHT
What went through my mind?
Automatic thought: [...]
How much do I believe it? (0-100%): [...]%

EMOTION
What emotions did I have?
Emotion: [...]    Intensity (0-100%): [...]%

COGNITIVE DISTORTION
Which cognitive distortions are involved?
[List from table above]

EXAMINE
Evidence for: [...]
Evidence against: [...]
Alternative perspective: [...]

ALTERNATIVE THOUGHT
More balanced, realistic thought:
[...]
How much do I believe it? (0-100%): [...]%

RESULT
Emotion afterward: [...]   Intensity: [...]%
Takeaway: [...]
```

---

## 6. Behavioral Activation

**Supplement to cognitive work:** Changing behavior supports thought change.

**Principle:** Positive activities -> Better mood -> More helpful thoughts

**Steps:**
1. Create list of pleasant/meaningful activities
2. Plan activities (specifically: when, how, where)
3. Track implementation
4. Rate mood before/after

**Example activities:**
- Walk (nature, fresh air)
- Contact with important people
- Creative activities
- Physical exercise
- Things that used to bring joy

---

## Ethics and Boundaries

**An AI assistant may:**
- Explain cognitive distortions and the ABC model
- Ask Socratic questions
- Guide thought records
- Provide psychoeducation about CBT techniques

**An AI assistant must NOT:**
- Replace professional cognitive behavioral therapy
- Make diagnoses or treatment recommendations
- Conduct crisis intervention
- Apply EMDR, Prolonged Exposure (PE), or Narrative Exposure Therapy (NET)

**In case of acute crisis, ALWAYS refer to:**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- Emergency services: 911 (US) / 112 (EU)

---

## References

- Beck, A. T. (1979). *Cognitive Therapy and the Emotional Disorders.* Penguin Books.
- Ellis, A. (1962). *Reason and Emotion in Psychotherapy.* Lyle Stuart.

---

*Ported from BACH v3.8.0 | Standalone Version*
*Sources: Beck (1979), Ellis (1962) — Not professional therapy*
