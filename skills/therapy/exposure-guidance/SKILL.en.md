---
name: exposure-guidance
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Graded exposure for anxiety disorders: Fear hierarchy, SUDs scale, exposure planning and guidance. Psychoeducation only, not implementation.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [exposure, anxiety, phobia, suds, graded, behavioral-therapy]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/exposition_begleitung.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Exposure Guidance

> Fear hierarchy, SUDs scale, graded exposure and habituation: Planning and guidance — actual exposure only with a therapist

See: [ETHICS.md](../ETHICS.md)

---

## Context

Exposure (confrontation therapy) is one of the most effective methods in behavioral therapy for anxiety disorders, phobias, OCD, and PTSD. It is based on the principles of habituation and extinction: When one repeatedly faces an anxiety-provoking situation, the anxiety response decreases over time.

Evidence: Exposure therapy is the gold-standard treatment for specific phobias, social anxiety, panic disorder, and agoraphobia (NICE Guidelines, Bandelow et al. 2014, S3 Guideline Anxiety Disorders). Effect sizes are among the highest in psychotherapy research.

**IMPORTANT:** This skill supports PLANNING of exposure exercises and conveys understanding of the mechanisms. The IMPLEMENTATION of exposure must be conducted under the guidance of a qualified therapist.
**Never implement:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Understanding the Mechanisms

### Habituation

```
HABITUATION: Adaptation through repeated confrontation

Anxiety level
100 |  *
    | * *
 80 |*   *
    |     *
 60 |      *
    |       *
 40 |        *
    |         *  *
 20 |          **  * *
    |                  * * * * * *
  0 |________________________________
    Time (during exposure)

Anxiety initially rises, reaches a peak,
and then drops on its own WITHOUT flight or avoidance.

Key experience: "The anxiety passes, even when
I stay in the situation."
```

### Extinction (New Learning)

```
EXTINCTION: New experiences overwrite old fear associations

Old experience: Dog -> Danger -> Fear -> Flight
New experience: Dog -> No danger -> Fear decreases -> I am safe

The old association is not erased but overlaid by new
experiences. Therefore, fear can return in certain
contexts (renewal, reinstatement) — which is NORMAL.
```

### Why Avoidance Maintains the Problem

```
THE AVOIDANCE CYCLE:

Anxiety-provoking situation
        |
        v
Anxiety rises (unpleasant)
        |
        v
Avoidance/flight
        |
        v
Short-term relief (anxiety drops immediately)
        |
        v
Long-term reinforcement of anxiety
("The situation IS dangerous, good that I fled")
        |
        v
Next time: Even more anxiety, even more avoidance
```

---

## 2. The SUDs Scale

### Subjective Units of Distress (0-100)

```
SUDs SCALE (Subjective Units of Distress)

  0  Completely relaxed, no anxiety
 10  Minimal tension, barely noticeable
 20  Slight unease, easily tolerable
 30  Noticeably unpleasant, but controllable
 40  Noticeable anxiety, still able to function
 50  Moderate anxiety, strenuous but manageable
 60  Strong anxiety, clear urge to avoid
 70  Very strong anxiety, hard to endure
 80  Intense anxiety, at the edge of tolerance
 90  Extreme anxiety, feeling of panic
100  Maximum anxiety, worst imaginable distress
```

### Using the SUDs Scale

**Before exposure:**
- Estimated anxiety in the planned situation (expected value)

**During exposure:**
- Assess current SUDs value every 5 minutes
- Document the progression (rising, falling, fluctuating)

**After exposure:**
- Highest SUDs value? Final value? How quickly did anxiety decrease?
- Was it as bad as expected?

---

## 3. Creating a Fear Hierarchy

### Principle

A fear hierarchy ranks anxiety-provoking situations from lowest to highest anxiety level. Exposure begins with easy situations and increases step by step.

### Example: Fear of Dogs

```
FEAR HIERARCHY: Dog Phobia

SUDs | Situation
-----|--------------------------------------------------
 10  | Look at a picture of a dog
 15  | Watch a video of playing dogs
 25  | Talk about own experiences with dogs
 30  | Watch a small dog from 10 meters away
 40  | Watch a small dog from 5 meters away
 50  | Stand next to a leashed small dog (2 meters)
 55  | Touch a small leashed dog (owner holding)
 60  | Watch a medium dog from 5 meters
 65  | Sit next to a leashed medium dog
 70  | Pet a medium dog
 75  | Walk past an unleashed dog (park)
 80  | Be alone in a room with a calm dog
 85  | Pet a large dog
 90  | Be in a park with multiple unleashed dogs
 95  | Feed a dog
100  | Let an unfamiliar dog run toward you
```

### Template for Completion

```
MY FEAR HIERARCHY

Anxiety topic: [...]

SUDs | Situation
-----|--------------------------------------------------
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
```

---

## 4. Types of Exposure

### Graded Exposure (In Vivo)

**Principle:** Step-by-step confrontation with real situations, starting at low SUDs values.

### Flooding

**Principle:** Direct confrontation with highly anxiety-provoking situations for extended periods. Only under therapeutic guidance. NOT to be guided by an AI assistant — only explained.

### Exposure in Sensu (Imaginal)

**Principle:** Experiencing anxiety-provoking situations in imagination. Helpful as preparation for real exposure.

### Interoceptive Exposure

**Principle:** Deliberately inducing physical anxiety symptoms (e.g., rapid heartbeat through exercise, dizziness through spinning). ONLY under therapeutic guidance.

---

## 5. Guided Exposure Planning

### Preparation Protocol

```
EXPOSURE PLANNING PROTOCOL

Date: [...]
Therapist informed: [ ] Yes  [ ] No (MANDATORY!)

Anxiety topic: [...]
Chosen situation: [...]
Expected SUDs value: [...]
Level in hierarchy: [...]

What exactly will I do: [...]
Where: [...]
When: [...]
How long: [...]
Alone or accompanied: [...]

My greatest fear: [...]
What will realistically happen: [...]

Emergency plan (if SUDs > 90 or dissociation):
1. Grounding (5-4-3-2-1)
2. Breathing exercise (box breathing)
3. [Call trusted person]: Tel. [...]
4. Leave situation in an orderly manner (no panicked fleeing)
```

### Post-Session Protocol

```
EXPOSURE DEBRIEFING

Date: [...]
Situation: [...]

SUDs before (expectation): [...]
SUDs highest value during: [...]
SUDs at the end: [...]

How long stayed in situation: [...]
Habituation occurred: [ ] Yes  [ ] Partial  [ ] No

What I learned: [...]
Was it as bad as feared: [ ] Worse  [ ] As expected  [ ] Less bad

What I want to do differently next time: [...]
Next level: [...]
```

---

## 6. Safety Notes and Abort Criteria

### Prerequisites for Exposure

```
CHECKLIST BEFORE STARTING EXPOSURE:

[ ] Qualified therapist is involved
[ ] Sufficient stabilization is present
[ ] Fear hierarchy is created and discussed
[ ] Emergency plan is prepared
[ ] Person understands the mechanism (habituation)
[ ] No acute suicidality
[ ] No uncontrolled psychotic symptoms
[ ] No severe dissociative disorder (without therapeutic support)
[ ] No acute substance intoxication
[ ] Person has voluntarily consented (no forced exposure!)
```

### Abort Criteria

```
ABORT EXPOSURE IF:

- Dissociation occurs (person is "gone," unresponsive)
- Panic attack with loss of control
- Person explicitly wants to stop (respect autonomy!)
- Physical symptoms: chest pain, shortness of breath, fainting
- Suicidal thoughts during exposure
- The situation becomes objectively unsafe

ON ABORT:
1. Grounding and stabilization (5-4-3-2-1, breathing exercise)
2. Ensure person is oriented and stable
3. Discuss experience (what happened, what was learned)
4. No blame ("You should have stayed")
5. Plan next step with therapist
```

---

## Ethics and Boundaries

**An AI assistant may:**
- Explain exposure principles (psychoeducation)
- Create fear hierarchies together
- Explain and use the SUDs scale
- Support exposure planning (fill out protocols)
- Document debriefing
- Provide safety information
- Motivate and normalize ("Anxiety during exposure is desired and normal")

**An AI assistant must NOT:**
- Independently conduct or guide exposure
- Guide flooding (ONLY therapist)
- Guide interoceptive exposure (ONLY therapist)
- Conduct prolonged exposure for PTSD
- Accompany exposure in severe dissociation
- Pressure toward exposure ("You must face this")
- Guarantee results
- Make diagnoses or create treatment plans
- Make medication-related recommendations

**PARTICULARLY STRICT BOUNDARY:** An AI assistant plans and explains. Actual exposure takes place under the guidance of a qualified therapist. For any request regarding implementation: refer to professional. Exposure without professional support can re-traumatize or intensify anxiety.

**In case of acute crisis, ALWAYS refer to:**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- Emergency services: 911 (US) / 112 (EU)

---

*Ported from BACH v3.8.0 | Standalone Version*
*Sources: Foa & Kozak (1986), Craske et al. (2014), Bandelow et al. (2014), S3 Guideline Anxiety Disorders (2014) — Not professional therapy*
