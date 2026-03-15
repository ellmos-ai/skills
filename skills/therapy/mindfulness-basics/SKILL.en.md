---
name: mindfulness-basics
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  MBSR fundamentals, body scan, and breathing exercises. Evidence-based mindfulness techniques according to Jon Kabat-Zinn for everyday life.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [mbsr, mindfulness, meditation, breathing-exercises, bodyscan]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/achtsamkeit_basis.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Mindfulness Basics

> MBSR fundamentals, body scan, and breathing exercises for everyday life

See: [ETHICS.md](../ETHICS.md)

---

## Context

Mindfulness is the intentional, non-judgmental attention to the present moment. MBSR (Mindfulness-Based Stress Reduction, Kabat-Zinn 1979) is the most well-known evidence-based mindfulness program.

**Note:** This is support, not a substitute for professional therapy.
**Never implement:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Core Attitudes of Mindfulness (Kabat-Zinn)

| Attitude | Description | Opposite to Avoid |
|----------|-------------|-------------------|
| Non-Judging | Observing without evaluating | "That is good/bad" |
| Patience | Things unfold in their own time | Rushing, forcing |
| Beginner's Mind | Being open, as if for the first time | Assumptions, expert stance |
| Trust | In one's own experience and intuition | Relying solely on others |
| Non-Striving | Simply being, without having to achieve | Performance orientation |
| Acceptance | Seeing things as they are | Fighting against reality |
| Letting Go | Allowing experiences to pass | Holding on, clinging |

---

## 2. Breathing Exercises

### 2.1 Simple Breath Awareness (5 Minutes)

**Goal:** Anchoring in the present moment, calming the nervous system.

**Instructions:**
1. Assume a comfortable sitting position (chair, floor, cushion)
2. Close your eyes or softly lower your gaze
3. Direct attention to the breath
4. Notice: Where do I feel the breath? (tip of the nose, chest, abdomen)
5. Thoughts arise? -> Kindly notice, return to the breath
6. No goal other than: Being with the breath

**Insight:** Thoughts come and go like clouds — you are the sky behind them.

---

### 2.2 4-7-8 Breathing Technique (Calming)

**Goal:** Activating the parasympathetic nervous system, stress reduction.

**Procedure:**
1. Inhale: 4 seconds
2. Hold: 7 seconds
3. Exhale: 8 seconds (longer than inhaling!)
4. Repeat: 3-4 cycles

**When to use:** Before sleep, during acute stress, before difficult situations.

---

### 2.3 Box Breathing (Square Breathing)

**Goal:** Balance, concentration (also used by Navy SEALs, elite athletes).

**Procedure:**
1. Inhale: 4 seconds
2. Hold: 4 seconds
3. Exhale: 4 seconds
4. Hold: 4 seconds
5. Repeat: 4 cycles

---

## 3. Body Scan

**Goal:** Developing body awareness, recognizing and releasing tension.
**Duration:** 10-30 minutes (shorter version: 5 minutes possible)

**Instructions (Short Form):**

```
1. Lie on your back or sit comfortably
2. Close eyes, take 3 deep breaths
3. Bring attention to the soles of your feet
   - Notice: Temperature, pressure, contact with the ground
   - No changing, just observing
4. Slowly move upward:
   Feet -> Lower legs -> Knees -> Thighs
   -> Pelvis -> Abdomen -> Chest -> Shoulders
   -> Arms -> Hands -> Neck -> Face -> Head
5. At tension: Breathe into the area, release on exhale
6. At the end: Perceive the entire body as a whole
7. Gently return to the room
```

**Documentation afterward:**
- What did I notice?
- Where was there tension?
- How do I feel now compared to before?

---

## 4. STOP Technique (Mini-Mindfulness in Everyday Life)

**S** — **Stop:** Pause whatever you are doing
**T** — **Take a breath:** Take one deep breath
**O** — **Observe:** Observe: thoughts, feelings, body sensations
**P** — **Proceed:** Consciously continue (or decide what to do next)

**Use:** Brief pause at any time, especially during stress or decisions.

---

## 5. Mindfulness in Daily Life (Informal Practice)

No time for formal exercises? Make everyday activities mindful:

| Activity | Mindfulness Focus |
|----------|------------------|
| Eating | Consciously notice taste, texture, smell |
| Walking | Feel each step (ground contact, weight shift) |
| Brushing teeth | Only do that, nothing else on the side |
| Doing dishes | Temperature of the water, sounds, movements |
| Driving | Fully present (no radio, no ruminating) |
| Waiting | Instead of phone: observe surroundings, breathe |

---

## 6. MBSR Program Overview (8 Weeks)

The complete MBSR program as reference:

| Week | Focus |
|------|-------|
| 1 | Autopilot vs. mindfulness |
| 2 | Dealing with obstacles |
| 3 | Mindfulness in the body (yoga) |
| 4 | Recognizing stress reactions |
| 5 | Stressors and reacting vs. responding |
| 6 | Mindful communication |
| 7 | Self-care |
| 8 | Mindfulness in everyday life |

---

## Ethics and Boundaries

**An AI assistant may:**
- Explain and guide mindfulness exercises
- Convey MBSR content (psychoeducation)
- Guide breathing exercises and body scan
- Explain and encourage the STOP technique

**An AI assistant must NOT:**
- Replace formal MBSR courses
- Guide mindfulness for trauma patients without professional supervision
- Therapeutically address dissociation or flashbacks
- Make medication-related recommendations

**Progress tracking:**
- Mood before/after exercise (0-10 scale)
- Track regularity (did I practice today?)
- Observations: Where was attention hard to maintain?

**In case of acute crisis, ALWAYS refer to:**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- Emergency services: 911 (US) / 112 (EU)

---

## References

- Kabat-Zinn, J. (1990). *Full Catastrophe Living: Using the Wisdom of Your Body and Mind to Face Stress, Pain, and Illness.* Delacorte Press.

---

*Ported from BACH v3.8.0 | Standalone Version*
*Sources: Kabat-Zinn (1990), MBSR Program — Not professional therapy*
