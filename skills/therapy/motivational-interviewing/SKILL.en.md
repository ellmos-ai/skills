---
name: motivational-interviewing
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Motivational Interviewing (MI) according to Miller and Rollnick: OARS techniques, change talk, fostering readiness for change.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [motivational-interviewing, oars, change-talk, ambivalence, miller-rollnick]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/motivational_interviewing.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Motivational Interviewing

> OARS techniques, stages of change, and change talk: Fostering intrinsic motivation for change without pressure or manipulation

See: [ETHICS.md](../ETHICS.md)

---

## Context

Motivational Interviewing (MI) was developed by William R. Miller and Stephen Rollnick. It is a client-centered, directive counseling approach for fostering intrinsic motivation for change. MI is used evidence-based in addiction treatment, health behavior, therapy adherence, and behavior change.

Evidence: Over 200 RCTs support the effectiveness of MI, particularly for addictive behaviors (Lundahl et al. 2010, Cochrane Review), health behaviors, and treatment adherence.

**Note:** This is support, not a substitute for professional therapy.
**Never implement:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. MI Spirit and Principles

### The Four Principles

1. **Partnership:** Collaboration on equal footing, not expert authority
2. **Acceptance:** Respecting autonomy, acknowledging strengths, absolute worth of the person
3. **Compassion:** The well-being of the person comes first
4. **Evocation:** Motivation already resides within the person — it is elicited, not implanted

### The Spirit of MI
MI is not a collection of techniques, but an attitude. The techniques only work within the context of this foundational spirit. Without it, MI becomes manipulation.

---

## 2. OARS Techniques

OARS are the four core competencies of motivational interviewing.

### O — Open Questions

**Principle:** Ask questions that invite reflection and storytelling, that cannot be answered with yes/no.

**Examples:**
- "What would you like to see change?"
- "How would your life look if you had made this change?"
- "What brought you to think about this?"
- "What is important to you about your health?"
- "What would you gain if you made this change?"

**Avoid:**
- Closed questions: "Do you want to quit smoking?"
- Leading questions: "You know that's harmful, right?"
- Why-questions: "Why did you do that?" (sounds accusatory)

---

### A — Affirming

**Principle:** Acknowledge strengths, efforts, and positive steps of the other person. Not praising ("You're great"), but specifically naming what was observed.

**Examples:**
- "It takes courage to speak openly about this."
- "You managed to hold on for three days — that shows you're serious."
- "Despite the difficult situation, you came today — that shows commitment."
- "You've clearly given this a lot of thought."

**When to use:**
- When the person describes steps toward change
- When they persist despite setbacks
- To strengthen self-efficacy

---

### R — Reflecting

**Principle:** Give back what was said in your own words — to show understanding and encourage further thinking.

**Types of reflections:**

| Type | Description | Example |
|------|-------------|---------|
| Simple | Repeat/paraphrase content | "You're saying it's hard for you." |
| Deepening | Pick up on what's beneath the surface | "It sounds like you're torn." |
| Double-sided | Mirror both sides of ambivalence | "On one hand you want to stop, on the other it gives you something." |
| Amplified | Slightly overstate (carefully!) | "So there's absolutely no reason to change anything?" |

**Double-sided reflection (ambivalence):**
```
"On one hand, you say you'd like to drink less alcohol.
On the other hand, the social aspect of after-work drinks is important to you.
Both make sense."
```

---

### S — Summarizing

**Principle:** Bundle the conversation — especially highlighting change talk.

**Types:**
- **Collecting:** Summarize multiple points
- **Linking:** Connect earlier statements with current ones
- **Transitional:** At the end of a conversation, leading to next steps

**Example:**
```
"Let me summarize what I've heard so far:
You've noticed that your sleep has gotten worse and it's
affecting your work. You've tried reducing caffeine before,
and that partly helped. Being fit and productive is important
to you. At the same time, your morning coffee enjoyment matters.
Does that sound right? What would you like to add?"
```

---

## 3. Stages of Change (Transtheoretical Model)

### The Stages (Prochaska & DiClemente)

| Stage | Description | MI Strategy |
|-------|-------------|-------------|
| Precontemplation | No problem awareness, no intention to change | Inform, spark curiosity, don't push |
| Contemplation | Ambivalence: "Maybe I should..." | Explore ambivalence, foster change talk |
| Preparation | Decision made, making plans | Support planning, strengthen confidence |
| Action | Actively implementing change | Affirm, work through obstacles |
| Maintenance | Stabilizing the change | Relapse prevention, acknowledge successes |
| Relapse | Return to old behavior | Normalize, re-motivate, learn from experience |

**Important:** Relapse is not failure, but part of the change process.

### Recognizing the Stage

**Guide questions:**
- "Have you thought about changing something?" (Precontemplation vs. Contemplation)
- "What speaks for it, what against it?" (Exploring ambivalence)
- "Do you have concrete ideas about how you'd approach it?" (Preparation)
- "What have you already tried?" (Action experience)

---

## 4. Recognizing and Strengthening Change Talk

### What is Change Talk?

Change talk consists of statements by the person that point toward change. MI aims to increase change talk and not reinforce sustain talk (maintaining the status quo).

### DARN-CAT Framework

**Preparatory Change Talk (DARN):**
- **D**esire: "I would like to..."
- **A**bility: "I could..."
- **R**easons: "It would be better because..."
- **N**eed: "I need to change something..."

**Mobilizing Change Talk (CAT):**
- **C**ommitment: "I will..."
- **A**ctivation: "I'm ready to..."
- **T**aking Steps: "I've already..."

### Fostering Change Talk

**Strategies:**
1. **Ask open questions:**
   - "What would you gain if something changed?"
   - "What gives you confidence that you could do this?"

2. **Importance and confidence scaling:**
   - "How important is this change to you on a scale of 0 to 10?"
   - "How confident are you that you could manage it?"
   - "Why a 5 and not a 2?" (strengthens existing motivation)

3. **Exploring extremes:**
   - "What could happen in the worst case if nothing changes?"
   - "What would be the best thing that could happen if you changed it?"

4. **Looking back and looking forward:**
   - "What was it like before this issue came up?"
   - "Where do you see yourself in five years if everything stays the same?"

---

## 5. Dealing with Resistance

### Resistance as a Signal

In MI, "resistance" is interpreted as a sign that the counselor is moving too fast or not adequately respecting the person's autonomy.

### Strategies

| Situation | Response |
|-----------|----------|
| "I don't have a problem" | Accept, don't argue, show curiosity |
| "You don't understand me" | Reflect: "Being understood is important to you" |
| "That won't work anyway" | Explore past successes, strengthen confidence |
| Person becomes angry | Slow down, emphasize autonomy, reflect empathically |

**Golden rule:** Never argue against resistance. Roll with the resistance, don't push against it.

---

## Ethics and Boundaries

**An AI assistant may:**
- Use OARS techniques to foster reflection
- Recognize and reflect back change talk
- Provide information about change processes
- Respectfully explore ambivalence

**An AI assistant must NOT:**
- Force or manipulate change
- Make decisions for the person
- Conduct addiction therapy or withdrawal support
- Use threats or fear appeals
- Undermine the person's autonomy

**Core principle:** The person decides. An AI assistant supports the reflection process.

**In case of acute crisis, ALWAYS refer to:**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- Emergency services: 911 (US) / 112 (EU)

---

*Ported from BACH v3.8.0 | Standalone Version*
*Sources: Miller & Rollnick (2013), Prochaska & DiClemente (1983), Lundahl et al. (2010) — Not professional therapy*
