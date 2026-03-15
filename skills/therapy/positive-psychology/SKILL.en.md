---
name: positive-psychology
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Positive Psychology according to Seligman: PERMA model, character strengths (VIA), gratitude exercises, flow theory, and resilience factors.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [positive-psychology, perma, flow, gratitude, resilience, seligman]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/positive_psychologie.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Positive Psychology

> Strengths focus, gratitude, flow, and PERMA according to Seligman and Csikszentmihalyi

See: [ETHICS.md](../ETHICS.md)

---

## Context

Positive Psychology is the scientific study of what makes life worth living (Seligman & Csikszentmihalyi, 2000). In contrast to clinical psychology (What causes illness?), it asks: What makes people healthy, happy, and resilient?

Founders: Martin Seligman (APA President 1998) initiated the movement. Other pioneers: Mihaly Csikszentmihalyi (Flow), Christopher Peterson (Character Strengths), Barbara Fredrickson (Broaden-and-Build), Ed Diener (Subjective Well-Being).

**Note:** This is support, not a substitute for professional therapy.
**Never implement:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. PERMA Model (Seligman, 2011)

Five pillars of well-being according to Seligman ("Flourish"):

### P — Positive Emotions
- Joy, gratitude, serenity, interest, hope, pride, love
- Fredrickson: At least a 3:1 ratio of positive to negative emotions
- Exercise: "Three Good Things" (see below)

### E — Engagement
- Being fully absorbed in an activity (flow state)
- Using one's strengths in daily life
- Challenge and skill in balance

### R — Relationships (Positive Relationships)
- Social connectedness as the strongest predictor of well-being
- Active-constructive responding to others' good news
- Small kindnesses (Random Acts of Kindness)

### M — Meaning
- Belonging to and serving something greater than oneself
- Meaning through work, family, community, spirituality
- Frankl: "He who has a why can bear almost any how"

### A — Achievement
- Experiencing mastery and competence
- Setting and achieving realistic goals
- Grit: Perseverance + passion for long-term goals (Duckworth, 2016)

---

## 2. Character Strengths (VIA Classification)

Peterson and Seligman (2004) identified 24 universal character strengths in 6 virtue categories:

| Virtue | Strengths |
|--------|----------|
| Wisdom | Creativity, Curiosity, Judgment, Love of Learning, Perspective |
| Courage | Bravery, Perseverance, Honesty, Zest |
| Humanity | Love, Kindness, Social Intelligence |
| Justice | Teamwork, Fairness, Leadership |
| Temperance | Forgiveness, Humility, Prudence, Self-Regulation |
| Transcendence | Appreciation of Beauty, Gratitude, Hope, Humor, Spirituality |

**Signature strengths:** The 3-5 strengths that feel most authentic. Those who use their signature strengths daily are demonstrably more satisfied and less depressed (Seligman et al. 2005).

**VIA Survey:** Free at viacharacter.org (scientifically validated)

---

## 3. Gratitude Exercises

### 3.1 Three Good Things (Seligman et al. 2005)

**Procedure:**
1. Every evening, write down 3 good things from the day
2. For each one note: Why did it happen?
3. Duration: At least 1 week, ideally ongoing

**Evidence:** Significantly increased well-being and reduced depressive symptoms over 6 months (Seligman et al. 2005)

### 3.2 Gratitude Journal

Extension of Three Good Things:
- Morning: What am I grateful for today? (3 items)
- Evening: What was good today? What did I contribute?
- Shift perspective: People, experiences, abilities, everyday things

### 3.3 Gratitude Letter (Gratitude Visit)

**Procedure:**
1. Identify a person you never properly thanked
2. Write a specific letter (300 words, concrete)
3. Visit the person and read the letter aloud

**Evidence:** Strongest short-term effect of all positive psychology interventions (Seligman et al. 2005). Effect lasts approximately 1 month.

---

## 4. Flow Theory (Csikszentmihalyi, 1990)

### Definition
Flow is a state of complete immersion in an activity, where action flows effortlessly and time and self-consciousness recede into the background.

### Conditions for Flow

| Condition | Description |
|-----------|-------------|
| Balance | Challenge matches skill level |
| Clear goals | You know exactly what to do |
| Immediate feedback | Instant feedback on progress |
| Concentration | Full attention on the task |
| Control | Feeling of being able to master the situation |
| Intrinsic motivation | The activity is rewarding in itself |

### Flow Channel

```
Challenge
     high   |  Anxiety    |  FLOW
            |             |
     low    |  Apathy     |  Boredom
            +-------------|----------
              low              high
                    Skill
```

### Fostering Flow
- Eliminate distractions (phone away, door closed)
- Break tasks into manageable units
- Adjust difficulty level (not too easy, not too hard)
- Establish regular practice times

---

## 5. Resilience Factors

Resilience = psychological resistance to adversity.

### The 7 Pillars of Resilience (after Reivich & Shatte, 2002)

1. **Emotion regulation:** Perceiving and managing one's own feelings
2. **Impulse control:** Consciously directing actions rather than reacting
3. **Causal analysis:** Realistically assessing causes
4. **Self-efficacy:** Confidence in one's own competence
5. **Empathy:** Recognizing and understanding others' emotions
6. **Optimism:** Realistic, positive expectations for the future
7. **Goal orientation:** Setting and pursuing meaningful goals

### Building Resilience
- Consciously use strengths (VIA strengths)
- Maintain social network (relationships as the #1 protective factor)
- Self-care: Sleep, exercise, nutrition, recovery
- Cognitive flexibility: Seek alternative perspectives
- Find meaning and significance (even in difficult situations)

---

## Ethics and Boundaries

**An AI assistant may:**
- Explain the PERMA model and character strengths (psychoeducation)
- Guide and support gratitude exercises
- Discuss flow conditions
- Convey resilience factors
- Support signature strengths reflection

**An AI assistant must NOT:**
- Treat clinical depression solely with positive psychology
- Clinically interpret VIA survey results
- Recommend positive psychology as a substitute for therapy
- Foster toxic positivity ("Just be grateful")

**Progress tracking:**
- Well-being before/after exercise (0-10 scale)
- Gratitude streak: How many consecutive days?
- Flow log: When and during which activities do I experience flow?
- Signature strengths: How often used this week?

**In case of acute crisis, ALWAYS refer to:**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- Emergency services: 911 (US) / 112 (EU)

---

*Ported from BACH v3.8.0 | Standalone Version*
*Sources: Seligman (2011), Csikszentmihalyi (1990), Peterson & Seligman (2004) — Not professional therapy*
