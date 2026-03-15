---
name: pmr-autogenic-training
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Progressive Muscle Relaxation (PMR) according to Jacobson and Autogenic Training according to Schultz. Short forms and full versions.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [pmr, autogenic-training, relaxation, jacobson, schultz, muscle-relaxation]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/pmr_autogenes_training.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Progressive Muscle Relaxation & Autogenic Training

> Body-based relaxation techniques according to Jacobson and Schultz

See: [ETHICS.md](../ETHICS.md)

---

## Context

Progressive Muscle Relaxation (PMR, Jacobson 1929) and Autogenic Training (AT, Schultz 1932) are the two most extensively researched relaxation techniques. Both work through conscious influence on the autonomic nervous system and can be learned as self-help methods without therapeutic supervision.

**Note:** This is support, not a substitute for professional therapy.
**Never implement:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Progressive Muscle Relaxation (PMR) according to Jacobson

### Basic Principle

Systematic tensing and releasing of muscle groups. Through the contrast between tension and release, the body learns deeper relaxation than possible in its normal state.

**Mechanism:** Muscle tension -> conscious release -> parasympathetic activation -> reduction of heart rate, blood pressure, muscle tone

### 1.1 Long Form: 16 Muscle Groups

| No | Muscle Group | Tension |
|----|-------------|---------|
| 1 | Right hand/forearm | Clench fist |
| 2 | Right upper arm | Tense biceps |
| 3 | Left hand/forearm | Clench fist |
| 4 | Left upper arm | Tense biceps |
| 5 | Forehead | Raise eyebrows |
| 6 | Mid-face | Squeeze eyes shut, wrinkle nose |
| 7 | Lower face | Clench teeth, pull corners of mouth wide |
| 8 | Neck | Press chin toward chest (counter-pressure) |
| 9 | Chest/shoulders | Raise shoulders, inhale deeply |
| 10 | Abdomen | Tense abdominal muscles |
| 11 | Lower back | Slight arch |
| 12 | Right thigh | Slightly lift leg |
| 13 | Right lower leg | Pull foot toward shin |
| 14 | Right foot | Curl toes |
| 15 | Left thigh | Slightly lift leg |
| 16 | Left lower leg/foot | Pull foot up, curl toes |

**Procedure per muscle group:**
1. Direct attention to the muscle group
2. Tense: 5-7 seconds (approximately 70% of maximum strength)
3. Release: Let go abruptly
4. Notice: 20-30 seconds, perceive the relaxation
5. Next muscle group

### 1.2 Short Form: 7 Muscle Groups

For experienced practitioners or when time is limited:

| No | Combination | Tension |
|----|------------|---------|
| 1 | Both arms | Clench fists, bend arms |
| 2 | Entire face | Grimace: furrow brow, close eyes, mouth wide |
| 3 | Neck/shoulders | Pull shoulders up to ears |
| 4 | Chest/abdomen | Inhale, tense abdomen |
| 5 | Back | Shoulder blades together, slight arch |
| 6 | Both thighs | Slightly lift legs |
| 7 | Both lower legs/feet | Pull feet up |

### 1.3 Recall Technique (Advanced)

After several weeks of practice: Relaxation of muscle groups ONLY through imagination (without actual tensing). The body has conditioned the relaxation response.

---

## 2. Autogenic Training (AT) according to Schultz

### Basic Principle

Concentrative self-relaxation through formulaic autosuggestion. The practitioner induces a state of deep relaxation through repeated guiding phrases (autonomic switching).

**Mechanism:** Concentration on formulas -> ideomotor response -> actual physical changes (blood flow, warmth, calm)

### 2.1 The 6 Basic Exercises (Lower Level)

| Exercise | Formula | Goal |
|----------|---------|------|
| 1. Heaviness | "My right arm is very heavy" | Muscle relaxation |
| 2. Warmth | "My right arm is very warm" | Vasodilation, blood flow |
| 3. Heart | "My heart beats calmly and steadily" | Heart regulation |
| 4. Breathing | "My breathing is calm and steady" | Breath regulation |
| 5. Solar plexus | "My solar plexus is streaming warm" | Abdominal organ relaxation |
| 6. Forehead | "My forehead is pleasantly cool" | Mental clarity |

**Progression:** Gradual over 6-8 weeks. Add one new exercise each week.

### 2.2 Session Procedure

```
1. Basic posture: Coachman's posture, armchair position, or lying down
2. Opening: Close eyes, "I am completely calm"
3. Internally repeat formulas (6x each, slowly):
   - "My right arm is very heavy" (6x)
   - "My right arm is very warm" (6x)
   - [additional formulas depending on practice level]
4. Rest formula in between: "I am completely calm"
5. Recall: Firmly tense arms, inhale deeply, open eyes
   IMPORTANT: Never skip the recall (except before falling asleep)
```

### 2.3 Learning Plan

| Week | Exercise | Duration |
|------|----------|----------|
| 1-2 | Heaviness exercise | 5 min |
| 3-4 | Heaviness + Warmth | 8 min |
| 5-6 | Heaviness + Warmth + Heart + Breathing | 12 min |
| 7-8 | All 6 basic exercises | 15 min |

---

## 3. PMR vs. AT: Decision Guide

| Criterion | PMR | AT |
|-----------|-----|-----|
| Learnability | Easy, immediately effective | Requires practice (4-8 weeks) |
| Physical activity | Yes (tensing) | No (imagination only) |
| For muscle tension | Very suitable | Moderately suitable |
| For inner restlessness | Good | Very good |
| For sleep problems | Good | Very good |
| Usable anywhere | Limited (movement needed) | Yes (inconspicuous) |
| For children | From approx. age 8 | From approx. age 10 |

---

## 4. Contraindications

**PMR:**
- Acute muscle injuries or inflammation
- Severe spasticity
- Epilepsy (tensing may trigger seizures — rare)

**AT:**
- Acute psychosis
- Severe depression (risk of excessive introspection)
- Cardiac arrhythmia (omit heart exercise)
- Dissociative disorders
- Severe hypotension (circulatory problems possible)

**Both methods:**
- Stop immediately if trauma flashbacks occur
- Not a substitute for medical/psychotherapeutic treatment

---

## Progress Tracking

- Tension level before/after exercise (0-10 scale)
- Which muscle groups were particularly tense?
- AT: Which formulas are already effective, which not yet?
- Regularity: Goal 1x daily, at least 4x/week

**In case of acute crisis, ALWAYS refer to:**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- Emergency services: 911 (US) / 112 (EU)

---

*Ported from BACH v3.8.0 | Standalone Version*
*Sources: Jacobson (1929), Schultz (1932) — Not professional therapy*
