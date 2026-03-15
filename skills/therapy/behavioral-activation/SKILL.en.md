---
name: behavioral-activation
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Behavioral activation for depression: Breaking the vicious cycle, activity monitoring, weekly planning, and values-based activities.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [behavioral-activation, depression, activity, weekly-plan, values]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/verhaltensaktivierung.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Behavioral Activation

> Activity planning, mood-activity diary, and values-based activity selection: Counteracting the vicious cycle of inactivity and low mood

See: [ETHICS.md](../ETHICS.md)

---

## Context

Behavioral Activation (BA) is an evidence-based intervention from behavioral therapy for treating depression. It is based on the insight that depression leads to withdrawal and inactivity, which further worsens mood (vicious cycle). Through targeted building of positive activities, this cycle is broken.

Evidence: Behavioral activation is effective as a standalone therapy and is equivalent to cognitive therapy (Dimidjian et al. 2006, Richards et al. 2016 COBRA study). Recommended as first-line intervention for mild to moderate depression (NICE Guidelines).

**Note:** This is support, not a substitute for professional therapy.
For severe depression or suicidal thoughts, ALWAYS recommend professional help.
**Never implement:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. The Behavioral Activation Model of Depression

### The Vicious Cycle

```
Triggering situation (loss, stress, change)
        |
        v
Low mood, lack of energy
        |
        v
Withdrawal, avoidance, inactivity
        |
        v
Fewer positive experiences, isolation
        |
        v
Even deeper low mood
        |
        v
Even more withdrawal ... (downward spiral)
```

### The Counter-Principle

```
Targeted activity (even with low motivation)
        |
        v
Positive experience / sense of accomplishment / connection
        |
        v
Slight mood improvement
        |
        v
Somewhat more energy and motivation
        |
        v
Further activity ... (upward spiral)
```

**Core principle:** Don't wait for motivation to come — action creates motivation.
"Act first, feel second." (Not: "Feel first, then act.")

---

## 2. Mood-Activity Diary

### Goal
Make connections between activities and mood visible. Recognize which activities improve mood and which worsen it.

### Diary Format

```
MOOD-ACTIVITY DIARY

Date: [...]

| Time  | Activity | Mood (0-10) | Enjoyment (0-10) | Importance (0-10) |
|-------|----------|-------------|-------------------|---------------------|
| 07:00 | Got up, had breakfast | 3 | 2 | 5 |
| 08:00 | Work: emails | 4 | 1 | 6 |
| 10:00 | Walk | 6 | 5 | 4 |
| 12:00 | Lunch with colleague | 7 | 6 | 7 |
| 14:00 | Work: project | 5 | 3 | 7 |
| 18:00 | Watching TV (alone) | 3 | 2 | 1 |
| 20:00 | Phone call with friend | 6 | 5 | 8 |

Daily mood average: [...]
Best activity today: [...]
Insight: [...]
```

### Weekly Review

**Guiding questions:**
- Which activities regularly lift my mood?
- Which activities lower my mood?
- Are there times that are particularly difficult?
- How much time do I spend on pleasant vs. unpleasant activities?
- Which activities have I been avoiding?

---

## 3. Activity Planning

### Step 1: Create Activity List

Collect three categories of activities:

**A) Pleasant Activities (joy, enjoyment)**
- Nature: Walk, park, forest
- Social: Meet friends, phone calls, cook together
- Creative: Music, painting, writing, crafting
- Physical: Sports, yoga, dancing, swimming
- Enjoyment: Cook favorite meal, read a book, listen to music
- Relaxation: Take a bath, meditation, breathing exercise

**B) Necessary Activities (structure, self-care)**
- Household: Tidying up, cooking, shopping
- Personal care: Showering, getting dressed, brushing teeth
- Administration: Bills, appointments, paperwork
- Health: Doctor's appointments, medication, nutrition

**C) Values-Based Activities (meaning, significance)**
- See section 4 below

### Step 2: Create Weekly Plan

```
WEEKLY PLAN

| Day | Morning | Midday | Afternoon | Evening |
|-----|---------|--------|-----------|---------|
| Mon | [...]   | [...]  | [...]     | [...]   |
| Tue | [...]   | [...]  | [...]     | [...]   |
| Wed | [...]   | [...]  | [...]     | [...]   |
| Thu | [...]   | [...]  | [...]     | [...]   |
| Fri | [...]   | [...]  | [...]     | [...]   |
| Sat | [...]   | [...]  | [...]     | [...]   |
| Sun | [...]   | [...]  | [...]     | [...]   |
```

### Planning Rules
1. **Start small:** Don't plan the whole day, but 1-2 activities per day
2. **Mix:** Pleasant + necessary + values-based
3. **Specific:** "Tuesday 3:00 PM walk in the park" instead of "Move more"
4. **Realistic:** Achievable even with low energy
5. **Flexible:** Plan is guidance, not obligation
6. **Graduated:** For very low energy: mini-steps (5 minutes is enough)

### Dealing with Obstacles

| Obstacle | Strategy |
|----------|----------|
| "I have no energy" | Reduce activity to 5 minutes |
| "I don't feel like it" | Reminder: motivation comes through action |
| "It won't help anyway" | Experiment: try it and measure mood afterward |
| "I can't do it alone" | Involve someone (appointment = commitment) |
| "I don't have time" | Build in small activities (take stairs, 5 min break outside) |

---

## 4. Values-Based Activity Selection

### Principle
Activities that align with personal values create sustainable well-being — as opposed to mere pleasure, which fades quickly.

### Life Domains and Values

```
VALUES COMPASS

Relationships:     What kind of partner/friend/family member do I want to be?
Work/Education:    What is important to me about my work?
Leisure:           How do I want to spend my free time?
Health:            How do I want to treat my body?
Community:         What contribution do I want to make?
Personal:          What kind of person do I want to be?
```

### Values-Activity Mapping

**Example:**

| Value | Activity | Frequency |
|-------|----------|-----------|
| Connection | Call a friend | 2x per week |
| Health | 20 min walk | Daily |
| Creativity | Play guitar | 1x per week |
| Helpfulness | Help neighbor with shopping | 1x per week |
| Learning | 15 min reading non-fiction | 3x per week |

### Values vs. Goals
- **Value:** A direction you want to move toward (e.g., "being a loving partner")
- **Goal:** An achievable endpoint (e.g., "plan anniversary celebration")
- Values can never be "checked off" — they provide ongoing orientation

---

## 5. Measuring Progress

### Weekly Review

```
WEEKLY REVIEW

Week: [Date]
Planned activities: [Number]
Completed activities: [Number]
Average mood: [0-10]

What went well: [...]
What was difficult: [...]
Insight of the week: [...]
Plan for next week: [...]
```

### Long-Term Tracking
- Observe mood trends over weeks
- Recognize the connection between activity level and mood
- Make successes visible (even small ones)

---

## Ethics and Boundaries

**An AI assistant may:**
- Guide through the diary and activity planning
- Suggest activities (never prescribe)
- Document mood data and reflect back patterns
- Accompany values reflection
- Acknowledge small progress

**An AI assistant must NOT:**
- Be the sole support for severe depression
- Make medication-related recommendations
- Assess suicidality
- Make diagnoses
- Guarantee that behavioral activation is sufficient

**Important:** For severe depression (persistent lack of drive, suicidal thoughts, inability to manage daily life), professional help is essential. Behavioral activation is a complement, not a substitute.

**In case of acute crisis, ALWAYS refer to:**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- Emergency services: 911 (US) / 112 (EU)

---

*Ported from BACH v3.8.0 | Standalone Version*
*Sources: Martell et al. (2010), Dimidjian et al. (2006), Richards et al. (2016) — Not professional therapy*
