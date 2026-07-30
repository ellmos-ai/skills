---
name: foerderplaner
version: 2.0.0
type: skill
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  Plans teaching, learning activities, and individual support without a report generator or personal templates.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: education
tags: [education, support, lesson-planning, differentiation]
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

# Teaching and Support Planner

## Purpose

Turn a starting point and learning goal into concrete, reviewable teaching and support steps.

**Result:** Goals, measures, differentiation, observation criteria, and review dates.

## Workflow

1. Clarify the goal, context, and requested output format.
2. Use only information supplied in the current request.
3. Produce a structured and traceable result.
4. Label assumptions and obtain confirmation before external changes.

## Example

**Input:** Plan four weeks of reading-comprehension support for an anonymized learner group.

**Result:** Goals, measures, differentiation, observation criteria, and review dates.

## Public core and private extensions

This public skill contains only the transferable method. App-specific adapters, accounts, local paths, databases, and personal defaults belong in a private supplemental profile or private fork and must not be committed to this repository.

Without a private profile, the skill uses only information explicitly supplied in the current request.

## Limits and data protection

- Data is not persisted by default.
- No source, file, or interface is opened or changed without explicit permission.
- The skill does not create support reports, certificates, or official assessments. General reports can be produced separately with `report-forge`; personal report templates remain private.

## Changelog

### 2.0.0 (2026-07-30)

- User-neutral public core; private integrations and personal profiles removed.
