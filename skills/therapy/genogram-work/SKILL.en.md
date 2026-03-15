---
name: genogram-work
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: >
  Genogram work: Recognizing and reflecting on family relationship patterns. Multigenerational perspective, genogram symbols, pattern recognition, and resources in family history.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [genogram, systemic-therapy, family-therapy, multigenerational, relationship-patterns]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/genogramm_arbeit.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-15"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Genogram Work

> Recognizing and reflecting on family relationship patterns: Multigenerational perspective, genogram symbols, pattern recognition, and resources in family history

See: [ETHICS.md](../ETHICS.md)

---

## Context

The genogram is a tool from systemic therapy and family therapy. It was significantly shaped by Murray Bowen (multigenerational approach) and Monica McGoldrick (genogram standardization). It graphically represents family relationships across multiple generations and makes patterns, roles, and dynamics visible.

Evidence: Genogram work is a component of all systemic therapy training programs and is established in clinical practice as a diagnostic and reflective tool (McGoldrick, Gerson & Petry 2020, von Schlippe & Schweitzer 2012).

**Note:** This is a reflection tool, not a substitute for professional therapy.
**Never implement:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. What Is a Genogram?

### Definition
A genogram is an extended graphical representation of a family tree that captures not only biological descent but also relationship qualities, emotional patterns, conflicts, illnesses, and important life events — typically across three generations.

### Difference from a Family Tree

| Family Tree | Genogram |
|-------------|----------|
| Who is related to whom? | How do people relate to each other? |
| Biological descent | Emotional relationship quality |
| Static facts | Dynamic patterns |
| Historically oriented | Pattern-oriented |

---

## 2. Genogram Symbols (Standard after McGoldrick)

### Persons

```
Male:         [ ]     (Square)
Female:       ( )     (Circle)
Non-binary:   < >     (Diamond)
Deceased:     [X]     (Symbol with X)
Index person: [=]     (Double border)
```

### Relationships

```
Marriage/Partnership:   ———————      (solid line)
Separation:            ——/——        (line with one slash)
Divorce:               ——//——       (line with two slashes)
Close relationship:    ═══════      (double line)
Enmeshed relationship: ≡≡≡≡≡≡≡      (triple line)
Conflict:              /\/\/\/\     (zigzag line)
Distance:              · · · · ·   (dotted line)
Cutoff:                ——||——      (line with double bar)
```

---

## 3. How Do I Create a Genogram?

### Step-by-Step Guide

**Step 1: Gather Data**
For each person (at least 3 generations):
- Name, birth year, death year if applicable
- Occupation, place of residence
- Special life events (migration, illness, losses)
- Relationship status

**Step 2: Draw Basic Structure**
- Grandparents at top, children at bottom
- Partners side by side
- Children from left to right (oldest first)

**Step 3: Add Relationship Qualities**
- Which relationships are close, which are distant?
- Where are conflicts?
- Where are enmeshments or cutoffs?

**Step 4: Mark Patterns**
- Color-code recurring themes
- E.g.: Addiction (red), mental illness (blue), separation (orange)

---

## 4. Recognizing Patterns — Multigenerational Perspective

### Typical Multigenerational Patterns

**Repetition patterns:**
- Divorces across multiple generations
- Addictive behavior (alcohol, work, ...)
- Early parenthood
- Career choices / role distribution

**Relationship patterns:**
- Enmeshment (too-close relationship, no boundaries)
- Cutoff (contact break, exclusion)
- Triangulation (child drawn into parental conflict)
- Parentification (child takes on parental role)

**Roles and mandates:**
- "The strong one" / "The caretaker"
- "The black sheep"
- "The peacemaker"
- Unspoken family mandates ("You should have it better")

### Reflection Questions on Patterns
- "What themes appear in your family across generations?"
- "What role have you taken on in your family?"
- "Are there family rules that were never spoken aloud?"
- "Who in the family do you resemble most — and in what way?"
- "Which relationship patterns of your parents do you recognize in yourself?"

---

## 5. Resources in the Genogram

### Not Just Problems — Also Strengths

The genogram shows not only burdens but also resources:
- Who has mastered difficult times?
- What strengths exist in the family?
- Who was a positive role model?
- What values were passed on that are helpful?

### Reflection Questions on Resources
- "Who in your family admires you? For what?"
- "From whom did you inherit or learn a strength?"
- "Which family member handled a crisis particularly well?"
- "Which positive family traditions would you like to continue?"
- "What has held your family together?"

---

## 6. Exercises

### Exercise 1: My Genogram
Draw your own genogram (3 generations). Use the symbols from section 2. Note 2-3 keywords for each person.

### Exercise 2: Relationship Qualities
Add relationship qualities to your genogram:
- Where are the closest relationships?
- Where are conflicts?
- Where is distance or cutoff?

### Exercise 3: Pattern Search
Look at your finished genogram and answer:
1. What themes repeat?
2. What roles do you recognize?
3. Which patterns do you want to continue — and which not?

### Exercise 4: Resource Genogram
Mark all positive resources in your genogram: Strengths, talents, mastered crises, positive values.

---

## Ethics and Boundaries

**An AI assistant may:**
- Explain genogram concepts and symbols
- Support creating a simple genogram
- Ask reflection questions about family patterns
- Point out resources in family history

**An AI assistant must NOT:**
- Make family diagnoses
- Process family secrets or traumas
- Conduct family constellations
- Promote blame toward family members
- Perform family therapeutic interventions

**In case of acute crisis, ALWAYS refer to:**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- Emergency services: 911 (US) / 112 (EU)

---

## References

- McGoldrick, M., Gerson, R. & Petry, S. (2020). *Genograms: Assessment and Treatment.* Norton.
- Bowen, M. (1978). *Family Therapy in Clinical Practice.* Jason Aronson.
- von Schlippe, A. & Schweitzer, J. (2012). *Lehrbuch der systemischen Therapie und Beratung.* Vandenhoeck & Ruprecht.

---

*Ported from BACH v3.8.0 | Standalone Version*
*Sources: McGoldrick et al. (2020), Bowen (1978), von Schlippe & Schweitzer (2012) — Not professional therapy*
