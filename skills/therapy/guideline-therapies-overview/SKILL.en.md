---
name: guideline-therapies-overview
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: >
  Comparison of the four guideline-approved psychotherapy approaches in Germany: Cognitive Behavioral Therapy, Psychodynamic Therapy, Psychoanalysis, Systemic Therapy — Orientation guide.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [guideline-therapies, cbt, psychodynamic, psychoanalysis, systemic-therapy, orientation]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/richtlinienverfahren_ueberblick.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-15"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Guideline Therapies Overview

> Comparison of the four approved guideline psychotherapy approaches in Germany: CBT, Psychodynamic Therapy, Psychoanalysis, Systemic Therapy — Orientation guide

See: [ETHICS.md](../ETHICS.md)

---

## Context

In Germany, there are four recognized guideline psychotherapy approaches whose costs are covered by statutory health insurance. Many people don't know which approach might be suitable for them. This skill provides a psychoeducational overview for orientation.

Legal basis: Guideline therapies are approved by the Federal Joint Committee (G-BA) based on scientific evidence.
- Cognitive Behavioral Therapy (CBT): Guideline therapy since 1987
- Psychodynamic Psychotherapy (PDT): since 1967
- Psychoanalytic Psychotherapy (AP): since 1967
- Systemic Therapy (ST): since 2019 (adults) / 2024 (children & adolescents)

**Note:** This is an orientation guide, not a therapy recommendation.
**Never implement:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. The Four Guideline Therapies at a Glance

| Feature | CBT | PDT | AP | ST |
|---------|-----|-----|----|----|
| **Core idea** | Change behavior and thought patterns | Understand unconscious conflicts | Deep personality change | Change relationships and systems |
| **Time focus** | Present and future | Past and present | Past (childhood) | Present and relationships |
| **Sessions** | 12-80 hrs | 12-100 hrs | 80-300 hrs | 12-48 hrs |
| **Frequency** | 1x/week | 1x/week | 2-3x/week | 1x/week or less |
| **Setting** | Mostly individual | Mostly individual | Individual (couch) | Individual, couple, family |

---

## 2. Cognitive Behavioral Therapy (CBT)

### Core Assumptions
- Behavior is learned and can be unlearned
- Thought patterns influence feelings and behavior (cognitive revolution, Beck)
- Change happens through active practice and new experiences

### When particularly suitable?
- Anxiety disorders, phobias, panic attacks
- Depression
- OCD, PTSD, eating disorders

---

## 3. Psychodynamic Psychotherapy (PDT)

### Core Assumptions
- Unconscious conflicts influence our experience and behavior
- Earlier relationship experiences shape current patterns
- Insight into unconscious connections promotes change

### When particularly suitable?
- Depression (especially chronic)
- Relationship problems with recurring patterns
- Personality disorders, psychosomatic complaints

---

## 4. Psychoanalytic Psychotherapy (Psychoanalysis, AP)

### Core Assumptions
- Deeply rooted unconscious conflicts from early childhood influence all experience
- Comprehensive personality change is possible through deep understanding

### When particularly suitable?
- Deep-seated personality problems
- Chronic, recurring problems
- When shorter approaches haven't been sufficient

---

## 5. Systemic Therapy (ST)

### Core Assumptions
- Problems arise and persist in relationship systems
- Change in one member changes the entire system
- Every person has resources and solution competencies

### When particularly suitable?
- Family and couple conflicts
- Child and adolescent problems (within the family system)
- When shorter therapy is desired

---

## 6. Practical Orientation

### Decision Aid (NOT a recommendation, only orientation)

| I want to... | Potentially suitable approach |
|--------------|------------------------------|
| Get concrete tools against anxiety | CBT |
| Understand why I keep falling into the same patterns | PDT |
| Fundamentally get to know myself better | AP |
| Understand relationship problems in their systemic context | ST |
| Get quick practical help | CBT or ST |

### Therapeutic Relationship

Research consistently shows: The most important therapeutic factor is the therapeutic relationship (Wampold 2015). The "right" approach is less important than the "right" therapist.

---

## 7. Practical Information

### Finding a Therapist
- In the US: Psychology Today therapist finder, insurance provider directories
- In the UK: NHS psychological therapies, BACP therapist directory
- In Germany: Appointment service: 116 117, Association of Statutory Health Insurance Physicians

---

## Ethics and Boundaries

**An AI assistant may:**
- Present and compare the four guideline therapies objectively
- Provide orientation (not recommendations)
- Give practical information about finding a therapist
- Ask reflection questions for self-clarification

**An AI assistant must NOT:**
- Recommend a specific approach
- Advise against an approach
- Make diagnoses or derive indications
- Evaluate or recommend therapists
- Comment on or question ongoing therapies

**In case of acute crisis, ALWAYS refer to:**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- Emergency services: 911 (US) / 112 (EU)

---

## References

- Wampold, B. E. (2015). *The Great Psychotherapy Debate.* Routledge.
- Leichsenring, F. & Rabung, S. (2011). Long-term psychodynamic psychotherapy in complex mental disorders. *British Journal of Psychiatry*, 199(1), 15-22.
- von Sydow, K. et al. (2010). *Die Wirksamkeit der Systemischen Therapie/Familientherapie.* Hogrefe.
- G-BA Psychotherapy Guideline

---

*Ported from BACH v3.8.0 | Standalone Version*
*Sources: G-BA Guidelines, Wampold (2015), Leichsenring & Rabung (2011), von Sydow et al. (2010) — Not professional therapy*
