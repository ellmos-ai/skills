---
name: schema-therapy
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: >
  Schema Therapy according to Jeffrey Young: Schemas, modes, inner child concept, and coping styles — psychoeducationally presented.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [schema-therapy, modes, inner-child, coping-styles, personality]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/schematherapie.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-15"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Schema Therapy

> Fundamentals of Schema Therapy according to Jeffrey Young: Schemas, modes, inner child concept, and coping styles — psychoeducationally presented

See: [ETHICS.md](../ETHICS.md)

---

## Context

Schema Therapy was developed by Jeffrey E. Young from the 1990s onward as an extension of cognitive behavioral therapy. It integrates elements from CBT, attachment theory, Gestalt therapy, and psychodynamic approaches.

Evidence: Schema Therapy is well supported empirically, particularly for personality disorders (Giesen-Bloo et al. 2006, Masley et al. 2012). In Germany, it is recognized as a method within behavioral therapy.

**Note:** This is psychoeducation, not a substitute for professional therapy.
**Never implement:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Early Maladaptive Schemas

### Principle
Schemas are deeply rooted emotional and cognitive patterns that develop in childhood through unmet core needs. They influence how we perceive the world, ourselves, and others.

### The Five Core Needs (according to Young)

| Core Need | When Unmet, May Lead To |
|-----------|------------------------|
| Secure attachment | Abandonment, mistrust |
| Autonomy & competence | Dependence, fear of failure |
| Realistic limits | Entitlement, insufficient self-control |
| Freedom to express needs | Subjugation, self-sacrifice |
| Spontaneity & play | Unrelenting standards, punitiveness |

### The 18 Schemas — Overview (5 Domains)

**Domain 1: Disconnection and Rejection**
- Abandonment / Instability
- Mistrust / Abuse
- Emotional Deprivation
- Defectiveness / Shame
- Social Isolation

**Domain 2: Impaired Autonomy and Performance**
- Dependence / Incompetence
- Vulnerability to Harm
- Enmeshment / Undeveloped Self
- Failure

**Domain 3: Impaired Limits**
- Entitlement / Grandiosity
- Insufficient Self-Control

**Domain 4: Other-Directedness**
- Subjugation
- Self-Sacrifice
- Approval-Seeking

**Domain 5: Overvigilance and Inhibition**
- Negativity / Pessimism
- Emotional Inhibition
- Unrelenting Standards
- Punitiveness

### Reflection Questions for Schema Recognition
- "What beliefs about yourself keep coming up again and again?"
- "In which situations do you react particularly strongly emotionally?"
- "Do you notice patterns that repeat across different relationships?"
- "Which needs may have been insufficiently met in your childhood?"

---

## 2. The Mode Model

### Principle
Modes are momentary emotional states activated by schemas. The mode model helps understand and categorize different "inner parts."

### The Four Mode Categories

**Child Modes:**
- *Vulnerable Child:* Feels sad, lonely, anxious, overwhelmed
- *Angry Child:* Angry about unmet needs
- *Impulsive Child:* Acts without thinking, wants immediate gratification
- *Happy Child:* Feels safe, loved, spontaneous

**Maladaptive Parent Modes:**
- *Punitive Parent:* Inner voice that criticizes, punishes, devalues
- *Demanding Parent:* Inner voice that demands perfection and achievement

**Maladaptive Coping Modes:**
- *Compliant Surrender:* Gives in, adapts excessively
- *Detached Protector:* Numbs feelings, withdraws, distracts
- *Overcompensation:* Dominates, controls, attacks

**Healthy Adult:**
- Can perceive needs and meet them appropriately
- Sets healthy boundaries
- Comforts and soothes the vulnerable child
- Limits excessive parent modes

### Exercise: Recognizing Modes in Daily Life

```
Situation: ______________
Which mode am I feeling right now?
  [ ] Vulnerable Child — "I feel small and helpless"
  [ ] Angry Child — "That's unfair!"
  [ ] Punitive Parent — "You're not good enough"
  [ ] Demanding Parent — "You must do more"
  [ ] Detached Protector — "I don't want to think about it"
  [ ] Overcompensator — "I'll show them"
  [ ] Healthy Adult — "What do I really need right now?"
```

---

## 3. Inner Child Work (Psychoeducational)

### Principle
Inner child work in Schema Therapy aims to develop a caring inner attitude toward one's own vulnerable parts.

**CAUTION:** Deep inner child work belongs in professional therapeutic supervision.

### Reflection Exercise: Letter to the Inner Child

```
Write a brief letter to your younger self:
1. What would you have needed back then?
2. What would you say to that child today?
3. What comfort would you offer?
```

### Reflection Questions
- "When you think about that situation — how old do you feel inside?"
- "What would a caring adult have said to you back then?"
- "Which needs of the child within you are currently going unmet?"

---

## 4. Understanding Coping Styles

### The Three Basic Patterns

| Coping Style | Strategy | Example |
|-------------|----------|---------|
| Surrender | Accept the schema, submit | "That's just how I am, I can't change it" |
| Avoidance | Not wanting to feel the schema | Distraction, substance use, overwork |
| Overcompensation | Living the opposite of the schema | Perfectionism instead of feeling like a failure |

### Reflection Questions
- "When you're under pressure — do you tend to submit, flee, or fight?"
- "Which of your habits might be avoidance strategies?"
- "Are there areas where you do the opposite of what you actually feel?"

---

## Ethics and Boundaries

**An AI assistant may:**
- Explain schemas and modes as concepts
- Ask reflection questions for self-exploration
- Present coping styles as psychoeducation
- Guide simple, written inner child reflection exercises

**An AI assistant must NOT:**
- Diagnose or attribute schemas
- Conduct chair work or experiential exercises
- Offer reparenting (limited reparenting)
- Process traumatic childhood experiences
- Replace schema mode therapy

**In case of acute crisis, ALWAYS refer to:**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- Emergency services: 911 (US) / 112 (EU)

---

## References

- Young, J. E., Klosko, J. S. & Weishaar, M. E. (2003). *Schema Therapy: A Practitioner's Guide.* Guilford Press.
- Giesen-Bloo, J. et al. (2006). Outpatient Psychotherapy for Borderline Personality Disorder. *Archives of General Psychiatry*, 63(6), 649-658.
- Roediger, E. (2011). *Praxis der Schematherapie.* Schattauer.

---

*Ported from BACH v3.8.0 | Standalone Version*
*Sources: Young et al. (2003), Giesen-Bloo et al. (2006), Roediger (2011) — Not professional therapy*
