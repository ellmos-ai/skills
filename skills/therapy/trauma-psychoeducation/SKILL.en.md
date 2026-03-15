---
name: trauma-psychoeducation
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Trauma psychoeducation: Trauma definition, normal reactions, window of tolerance, trigger management, and self-care.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [trauma, psychoeducation, window-of-tolerance, trigger, self-care, ptsd]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/trauma_psychoedukation.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Trauma Psychoeducation

> Knowledge about trauma, trauma sequelae, and the window of tolerance: Understanding normal reactions to abnormal events — pure psychoeducation, NO trauma processing

See: [ETHICS.md](../ETHICS.md)

---

## Context

Psychoeducation about trauma helps affected individuals understand and contextualize their reactions. The knowledge that symptoms like flashbacks, hyperarousal, or avoidance are NORMAL reactions to ABNORMAL events is already relieving and reduces shame and self-blame.

Evidence: Psychoeducation is a recognized component of trauma therapy (Flatten et al. 2011, S3 Guideline PTSD). As a standalone intervention, it is insufficient, but it can increase therapy motivation and alleviate symptoms.

**IMPORTANT:** This skill exclusively conveys KNOWLEDGE about trauma. It does NOT conduct trauma processing, does NOT explore distressing memories, and does NOT ask for trauma details.
**Never implement:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. What Is Trauma?

### Definition

A trauma is an event that exceeds a person's coping capacity and is accompanied by the experience of helplessness, loss of control, and/or fear of death. It is not the event alone that defines the trauma, but the subjective experience.

### Trauma Types

| Type | Description | Examples |
|------|-------------|----------|
| Type I (Single trauma) | Single, unexpected event | Accident, assault, natural disaster |
| Type II (Complex trauma) | Repeated, prolonged traumatization | Abuse, neglect, war |
| Accidental trauma | Random events | Traffic accident, house fire, workplace accident |
| Interpersonal trauma | Caused by humans | Violence, abuse, torture |
| Secondary trauma | Through co-experiencing/witnessing | Helping professions, family members |

### What Is NOT Trauma (Differentiation)

Not every distressing event is a trauma in the clinical sense:
- Breakup, job loss, arguments — distressing, but usually not trauma
- Bullying — can be traumatizing (especially for children), but is not automatically trauma
- The individual appraisal determines, not the type of event

---

## 2. Normal Reactions to Abnormal Events

### The Three Response Patterns

```
HYPERAROUSAL
- Constant vigilance and tension
- Startle response
- Sleep problems
- Irritability, anger outbursts
- Concentration difficulties

RE-EXPERIENCING (Intrusion)
- Flashbacks (memories that feel real)
- Nightmares
- Distressing memories that arise suddenly
- Physical reactions upon remembering (racing heart, sweating)

AVOIDANCE AND NUMBING (Constriction)
- Avoidance of places, people, situations
- Emotional numbness
- Withdrawal from other people
- Feeling of alienation
- Loss of interest and pleasure
```

### Important Message for Affected Individuals

```
"These reactions are NORMAL reactions to ABNORMAL events.

Your body and mind are trying to protect you.
The vigilance protects you from renewed danger.
The memories are trying to process what happened.
The avoidance protects you from being overwhelmed.

You are not 'crazy.' You are not 'weak.'
Your nervous system is responding the way it is programmed
to respond to extreme threat."
```

### Timeline

```
COURSE AFTER TRAUMATIC EVENT

0-4 weeks:  Acute Stress Reaction (NORMAL)
            - Shock, numbness, restlessness
            - Sleep problems, startle response
            - Flashbacks, nightmares
            - For most people: Spontaneous recovery

4+ weeks:   If symptoms persist: Possible PTSD
            - Professional assessment recommended
            - Early intervention improves prognosis

Months-Years: Chronification possible
            - Therapy is effective even after a long time
            - "It is never too late to seek help"
```

---

## 3. The Window of Tolerance (Dan Siegel)

### The Model

```
            ________________________________________________
           |                                                |
           |   ABOVE THE WINDOW: Hyperarousal               |
           |   Panic, rage, overactivation, flashbacks      |
           |   Racing heart, sweating, trembling            |
           |   "Fight or flight"                            |
           |________________________________________________|
           |                                                |
           |   WINDOW OF TOLERANCE                          |
           |                                                |
           |   Here we can:                                 |
           |   - Think and feel at the same time            |
           |   - Process information                        |
           |   - Maintain relationships                     |
           |   - Solve problems                             |
           |   - Learn and grow                             |
           |________________________________________________|
           |                                                |
           |   BELOW THE WINDOW: Hypoarousal                |
           |   Freeze, numbness, dissociation               |
           |   Lack of energy, emptiness, shutdown           |
           |   "Playing dead reflex"                         |
           |________________________________________________|
```

### What Does This Mean?

- **In the window:** We can regulate stress and function
- **Above the window:** Too much activation — body in alarm mode
- **Below the window:** Too little activation — body shuts down

### Trauma and the Window

```
BEFORE trauma:            AFTER trauma (untreated):

|_______________|         |_____|
|               |         |     |  <- Window has NARROWED
|    WINDOW     |         | W.  |
|   (wide)      |         |     |
|_______________|         |_____|

Even small stimuli can cause falling out of the window
after trauma (triggers).

GOAL of therapy: WIDEN the window again.
```

### Understanding Triggers

```
TRIGGERS are stimuli that remind of the trauma and put
the nervous system into alarm mode — often unconsciously.

Triggers can be:
- Sounds (bang, screaming, certain music)
- Smells (smoke, perfume, alcohol)
- Images (news, movies, places)
- Body sensations (tightness, touch, pain)
- Calendar dates (anniversaries)
- Relationship situations (arguments, loss of control)

Triggers are NOT weakness. They are stored warning signals
of the nervous system. In therapy, one learns to recognize
triggers and regulate the nervous system.
```

---

## 4. Self-Care Strategies

### Ensuring Basic Needs

```
BASIC NEEDS CHECKLIST

[ ] Sleep: Regular bedtimes, at least 7 hours
[ ] Nutrition: Regular meals, sufficient water
[ ] Exercise: At least 20 minutes daily (a walk is enough)
[ ] Social contacts: At least one trusted person
[ ] Safety: Feeling safe in one's own environment
[ ] Structure: Daily routine with fixed anchor points
```

### Self-Care Strategies in Daily Life

**Physical:**
- Regular exercise (lowers stress hormones)
- Breathing exercises
- Sufficient sleep (observe sleep hygiene)
- Reduce caffeine and alcohol (amplify hyperarousal/numbing)

**Social:**
- Have a trusted person (doesn't have to talk about trauma)
- Avoid isolation — even small contacts help
- Learn to set boundaries (being allowed to say "no")
- Accept support

**Emotional:**
- Name feelings (don't judge them)
- Use stabilization techniques (5-4-3-2-1, safe place)
- Keep a journal (optional, don't force it)
- Find creative expression (painting, music, writing)

**Cognitive:**
- Inform yourself (psychoeducation — this skill)
- Challenge self-blame ("It was not my fault")
- Reality-check catastrophizing
- Be patient with yourself (healing takes time)

---

## 5. Finding Professional Help

### When to Seek Professional Help?

```
PROFESSIONAL HELP IS INDICATED WHEN:

- Symptoms persist for more than 4 weeks
- Symptoms worsen instead of improving
- Daily life is no longer manageable (work, relationships)
- Flashbacks or nightmares occur very frequently
- Avoidance behavior severely restricts life
- Substance use as a coping strategy
- Suicidal thoughts or self-harm
- The feeling: "I can't do this alone"
```

### Resources

```
IMMEDIATE HELP:
- 988 Suicide & Crisis Lifeline (US): 988 (24/7, free)
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222 (24/7, free)
- Emergency services: 911 (US) / 112 (EU)

TRAUMA-SPECIFIC:
- Trauma outpatient clinics (at many hospitals, no referral needed)
- Victim support organizations (e.g., RAINN in US: 1-800-656-4673)
- Domestic violence hotline (US): 1-800-799-7233
- National Sexual Assault Hotline (US): 1-800-656-4673

FINDING A THERAPIST:
- Psychology Today therapist directory: psychologytoday.com/us/therapists
- SAMHSA helpline (US): 1-800-662-4357
- Important: Look for therapists specializing in "trauma therapy"
```

---

## 6. Frequently Asked Questions (FAQ)

### "Am I traumatized now?"

Not everyone who experiences a distressing event develops a trauma-related disorder. The majority of people recover spontaneously within weeks. Whether PTSD is present can only be determined by a professional.

### "Do I have to talk about it?"

No. Forcing yourself to talk can be harmful. Some people benefit from talking about it, others don't. There is no "must." In therapy, the right timing is determined together.

### "Why do I react this way even though it was long ago?"

Traumatic memories are stored differently than normal memories. They can be reactivated by triggers and feel as though the event is happening NOW. The brain does not distinguish between "then" and "now." Therapy helps "re-sort" these memories.

### "Am I weak because I can't handle this alone?"

No. Seeking help is a sign of strength. Trauma therapy is effective — most people can improve significantly with professional help.

---

## Ethics and Boundaries

**An AI assistant may:**
- Convey knowledge about trauma and trauma sequelae (psychoeducation)
- Normalize normal reactions and provide relief
- Explain the window of tolerance
- Suggest self-care strategies
- Refer to professional help
- Offer stabilization techniques

**An AI assistant must NOT:**
- Conduct trauma processing (EMDR, exposure, NET, IRRT)
- Ask for or explore trauma details
- Process flashback content (only stabilize)
- Diagnose PTSD or other trauma-related disorders
- Assess suicidality
- Make medication-related recommendations
- Make statements about blame or responsibility
- "Work through" or "process" memories
- Ask suggestive questions ("Could it be that...")

**PARTICULARLY STRICT BOUNDARY:** Trauma processing belongs in the hands of trained trauma therapists. This skill offers exclusively psychoeducation and stabilization. For any form of trauma exploration: STOP and refer to a professional.

**In case of acute crisis, ALWAYS refer to:**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- Emergency services: 911 (US) / 112 (EU)

---

*Ported from BACH v3.8.0 | Standalone Version*
*Sources: Flatten et al. (2011), Siegel (2012), Reddemann (2001), S3 Guideline PTSD (2019) — Not professional therapy*
