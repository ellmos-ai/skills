---
name: gesundheit
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-11-09
description: "Use when organizing personal health notes, symptom chronologies, or preparing consultations with doctors (e.g. 'prepare doctor visit', 'structure symptom notes', 'organize health questions', /gesundheit). Formats voluntary health information neutrally and drafts targeted questions for healthcare professionals. Do NOT use for medical diagnosis, treatment prescribing, or medical emergencies."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [health, organization, questions, safety]
language: en
status: stable
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: public-neutral
  origin_license: MIT
  notes: Public core only; adapters and private profiles are excluded.
---


<img src="banner.png" width="100%" alt="gesundheit banner">

# Health Information Organizer

## Purpose

Summarize symptoms, timelines, medication, and open questions factually.

**Result:** Timeline, structured observations, safety flags, and questions for medical professionals.

## Workflow

1. Clarify the goal, context, and requested output format.
2. Use only information supplied in the current request.
3. Produce a structured and traceable result.
4. Label assumptions and obtain confirmation before external changes.

## Example

**Input:** Turn these symptom notes into a short timeline for a medical appointment.

**Result:** Timeline, structured observations, safety flags, and questions for medical professionals.

## Public core and private extensions

This public skill contains only the transferable method. App-specific adapters, accounts, local paths, databases, and personal defaults belong in a private supplemental profile or private fork and must not be committed to this repository.

Without a private profile, the skill uses only information explicitly supplied in the current request.

## Limits and data protection

- Data is not persisted by default.
- No source, file, or interface is opened or changed without explicit permission.
- The skill does not diagnose or replace medical care. Acute danger requires local emergency services.

## Changelog

### 2.0.0 (2026-07-30)

- User-neutral public core; private integrations and personal profiles removed.
