---
name: psychoeducation
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Psychoeducation on depression, anxiety disorders, PTSD, bipolar disorder, schizophrenia, ADHD, and borderline. Knowledge sharing without diagnosis.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: therapy
tags: [psychoeducation, depression, anxiety, ptsd, adhd, borderline, knowledge]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/psychoedukation.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Psychoeducation

> Knowledge sharing about mental disorders, symptoms, and treatment approaches

See: [ETHICS.md](../ETHICS.md)

---

## Context

Psychoeducation refers to the systematic sharing of knowledge about mental disorders with affected individuals and their families. The goal is to foster understanding of the disorder, strengthen self-management, and reduce stigmatization.

Evidence: Psychoeducation is recommended as a component in all treatment guidelines (DGPPN, NICE, APA) and demonstrably reduces relapse rates (Xia et al. 2011, Cochrane Review).

**Note:** This is support, not a substitute for professional therapy.
**Never implement:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. What is Psychoeducation?

### Definition
Structured communication of knowledge about mental disorders with the goal of making affected individuals "experts of their own condition."

### Goals
- Understanding the illness: What do I have? Why?
- Recognizing early warning signs
- Knowing treatment options
- Fostering self-efficacy
- Reducing stigma
- Improving adherence (treatment compliance)

### Evidence
- Relapse prevention in schizophrenia: NNT = 9 (Xia et al. 2011)
- Depression: Improvement of treatment adherence by 30-50% (Donker et al. 2009)
- Anxiety disorders: Psychoeducation alone already mildly effective (Donker et al. 2009)

---

## 2. Mental Disorders Overview

### 2.1 Depression (Major Depressive Disorder)

**What is it?** Persistent low mood, loss of interest, and lack of drive for at least 2 weeks, going beyond normal sadness.

**Core symptoms (ICD-11):**
- Depressed mood (most of the day, nearly every day)
- Loss of interest / inability to feel pleasure (anhedonia)
- Reduced drive / increased fatigue

**Additional symptoms:** Concentration difficulties, feelings of guilt, sleep problems, appetite changes, suicidal thoughts, psychomotor retardation/agitation

**Treatment:** CBT, medication (SSRIs, SNRIs), exercise, light therapy (seasonal)
**Self-help:** Daily structure, activity scheduling, social contacts, exercise, sleep hygiene

### 2.2 Anxiety Disorders

**What is it?** Excessive, uncontrollable anxiety or fear that impairs everyday life.

**Types:**
- Generalized Anxiety Disorder (GAD): Chronic worrying
- Panic Disorder: Sudden anxiety attacks with physical symptoms
- Social Anxiety Disorder: Fear of evaluation in social situations
- Specific Phobias: Fear of specific objects/situations
- Agoraphobia: Fear of places/situations without escape

**Treatment:** CBT (exposure, cognitive restructuring), SSRIs, relaxation
**Self-help:** Anxiety diary, breathing exercises, gradual confrontation

### 2.3 Post-Traumatic Stress Disorder (PTSD)

**What is it?** Persistent reaction to a traumatic experience (threat, violence, accident, disaster) with re-experiencing, avoidance, and hyperarousal.

**Core symptoms:**
- Intrusions (flashbacks, nightmares)
- Avoidance behavior
- Emotional numbing or hyperarousal
- Negative changes in thoughts and mood

**Treatment:** Trauma-focused CBT, EMDR, Narrative Exposure Therapy
**Self-help:** Stabilization techniques, grounding, safe place — NO self-exposure

### 2.4 Bipolar Disorder

**What is it?** Alternation between depressive and (hypo)manic episodes. Chronic condition with high relapse risk.

**Manic episode:** Elevated mood, decreased need for sleep, grandiose ideas, increased activity, risk-taking behavior, pressured speech

**Treatment:** Mood stabilizers (lithium, valproate), atypical antipsychotics
**Self-help:** Mood diary, regular sleep schedule, knowing early warning signs

### 2.5 Schizophrenia

**What is it?** Severe mental disorder with disturbances of thought, perception, and experience. Affects approximately 1% of the population.

**Positive symptoms:** Hallucinations, delusions, disorganized thinking
**Negative symptoms:** Lack of drive, social withdrawal, flat affect
**Cognitive symptoms:** Attention, memory, executive functions

**Treatment:** Antipsychotics, CBT for psychosis, social therapy, family interventions
**Self-help:** Medication adherence, stress avoidance, early warning signs, daily structure

### 2.6 ADHD (Attention Deficit Hyperactivity Disorder)

**What is it?** Neurobiological developmental disorder with inattention, impulsivity, and/or hyperactivity. Begins in childhood, persists into adulthood in approximately 50% of cases.

**Treatment:** Multimodal (medication, psychoeducation, coaching, CBT)
**Self-help:** External structural aids, timers, lists, routines, exercise

### 2.7 Borderline Personality Disorder (BPD)

**What is it?** Pattern of instability in relationships, self-image, and affect with pronounced impulsivity. High emotional vulnerability.

**Core symptoms:** Unstable relationships, identity disturbance, impulsivity, affective instability, self-harm, chronic emptiness, dissociation

**Treatment:** DBT (Linehan), Schema Therapy, MBT, TFP
**Self-help:** Skills kit, emergency plan, distress tolerance skills

---

## 3. Stigma Reduction

### Common Myths and Facts

| Myth | Fact |
|------|------|
| "Mentally ill people are dangerous" | Affected individuals are more often victims than perpetrators |
| "Depression is weakness of will" | Depression is a neurobiological disorder |
| "Therapy is just talking" | Evidence-based therapy demonstrably changes brain structures |
| "It will pass on its own" | Many conditions become chronic without treatment |
| "Medications cause addiction" | Antidepressants do not cause dependence |

### Language and Stigma
- "Person with schizophrenia" instead of "schizophrenic"
- "Person with depression" instead of "depressive person"
- Person-first language demonstrably reduces stigma (Granello & Gibbs, 2016)

---

## 4. Family Perspective

- Mental disorders affect the entire social environment
- Families need their own psychoeducation and relief
- Expressed Emotion (EE): High criticism/overinvolvement increases relapse risk
- Recommendation: Family support groups, family psychoeducation

---

## Ethics and Boundaries

**An AI assistant may:**
- Provide factual information about mental disorders
- Answer common questions
- Refer to further resources

**An AI assistant must NOT:**
- Make or confirm diagnoses
- Give individual treatment recommendations
- Replace professional psychoeducation in group format

**In case of acute crisis, ALWAYS refer to:**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- Emergency services: 911 (US) / 112 (EU)

---

*Ported from BACH v3.8.0 | Standalone Version*
*Sources: ICD-11, DGPPN Guidelines, Xia et al. (2011), Donker et al. (2009), Cochrane Reviews — Not professional therapy*
