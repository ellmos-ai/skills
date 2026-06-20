---
name: academic-study-test
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-06-20
updated: 2026-06-20
description: >
  Use when exam preparation, self-tests, mock exams or simulations, written
  coursework, or error diagnosis are needed. Provides five modes and a
  rubric-based assessment system with a strict boundary around live exams.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: education
tags: [exams, mock-exam, self-test, simulation, rubric, assessment, feedback, studies]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Academic Study Test

## Overview

Support exam preparation with structured self-tests, realistic simulations,
and diagnostic feedback. The skill is subject- and institution-neutral and
can be used with any study materials.

## Configuration

| Placeholder | Meaning |
|---|---|
| `<MODULE_PREFIX>` | Abbreviation used in module codes (e.g. MM, MF, MO) |
| `<ASSIGNMENT_TYPE>` | Type of submission (e.g. essay, portfolio, seminar paper) |
| `<LMS>` | Learning management system (e.g. ILIAS, Canvas, Stud.IP) |

## Modes

### Mode 1 — Quick Test (5–10 minutes)

- 5 targeted questions on the chosen topic or module.
- Immediate feedback after each answer.
- Recommended for daily revision and progress tracking.

### Mode 2 — Exam Block (60–90 minutes)

- Full exam simulation following the time frame and format of the target exam.
- All questions are answered first, then evaluated together.
- Assessment using the rubric below, total score, and strengths/gaps profile.

### Mode 3 — Oral Examination

- Simulated examination conversation: open questions, follow-up questions, objections.
- Feedback on content, argumentation, and communication style.
- Suitable for Bachelor's/Master's examinations, presentations, and colloquia.

### Mode 4 — `<ASSIGNMENT_TYPE>` Training

- Work through practice tasks in the format of the assignment to be submitted.
- Quality check on content, structure, source references, and formal requirements.
- Feedback with concrete suggestions for improvement.

### Mode 5 — Error Diagnosis

- Analysis of errors from previous tests, corrections, or submissions.
- Identify patterns: conceptual gaps, careless mistakes, misunderstandings.
- Prioritised revision recommendation.

## Assessment Rubric

| Criterion | 0 points | 1 point | 2 points |
|---|---|---|---|
| Factual correctness | Incorrect | Partially correct | Fully correct |
| Completeness | Essential parts missing | Gaps present | Complete |
| Justification | No justification | Hinted at | Clearly justified |
| Technical language | Not used | Partial | Consistently correct |
| Structure | Unclear | Recognisable | Clear and coherent |

Maximum score: 10 points. Scale: 9–10 = excellent, 7–8 = good,
5–6 = satisfactory, 3–4 = pass, 0–2 = fail.

## Material Access

- Use local module folders following the pattern `<MODULE_PREFIX><Number>`.
- For online materials use `<LMS>` or the institutional website.
- Optional: search institutional emails for assignment briefs or corrections
  if a mail connector is available.

## Ethics and Limits

This skill is used exclusively for preparation and practice.

**Absolute prohibitions:**
- No support during live examinations, tests, or `<ASSIGNMENT_TYPE>` submissions
  that are currently in progress.
- No formulating of answers that would be submitted without attribution as the
  student's own work.
- No circumvention of examination regulations or institutional guidelines.

When in doubt: mark the task as "to be clarified" until clarification is obtained.

## Notes

- For source-based learning and consolidation, use the skill `academic-study-learn`.
- For semester planning and deadlines, use the skill `academic-study-control`.
