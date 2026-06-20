---
name: academic-study-learn
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-06-20
updated: 2026-06-20
description: >
  Use when study materials (scripts, books, PDFs, lecture slides) need to
  be worked through systematically, summarised, or consolidated through
  retrieval practice. Guides through a complete learning cycle: learning
  objective, key ideas, glossary, transfer, and self-test.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: education
tags: [learning, objectives, retrieval, glossary, summary, studies, didactics]
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

# Academic Study Learn

## Overview

Support source-based learning with a five-phase learning cycle. The skill is
institution- and subject-neutral: it works with any study material available
as a file, text input, or via web access.

## Configuration

| Placeholder | Meaning |
|---|---|
| `<MODULE_PREFIX>` | Abbreviation used in module codes (e.g. MM, MF, MO) |
| `<LMS>` | Learning management system (e.g. ILIAS, Canvas, Stud.IP) |
| `<INDEX_FILE>` | Local index file of the study folder (e.g. LLM_INDEX.md) |

## Learning Cycle (5 Phases)

### 1. Clarify the Learning Objective

- What should be possible, understood, or applied after this unit?
- State the objective in one sentence and review it at the end of the unit.

### 2. Extract Key Ideas (3–7)

- Identify the most important concepts, theories, or procedures from the material.
- Explain each key idea in 2–4 sentences.
- Name the connections between the key ideas.

### 3. Build a Glossary

- List technical terms with a brief definition and — where available — a source reference.
- Only include terms that are relevant to the learning objective.

### 4. Transfer and Application

- Formulate at least one example or application from your own context.
- Work out the differences between similar concepts.
- Explicitly name open questions and uncertainties.

### 5. Retrieval Practice (5–10 questions)

- Answer questions without looking at the material.
- Compare answers with the source material.
- Note gaps and errors as the basis for the next revision session.

## Sources and Material Access

- Check local module folders following the pattern `<MODULE_PREFIX><Number>`
  (e.g. `<MODULE_PREFIX>1`, `<MODULE_PREFIX>2`).
- For online materials (scripts, assignments, reading lists) use `<LMS>` or the
  official institutional website when a connector or browser access is available.
- Use `<INDEX_FILE>` as the entry point when a local study folder exists.
- Optional: search institutional emails for hints about required reading or
  assignments if a mail connector is available.

## Quality Criteria

- Key ideas are formulated in your own words, not copied verbatim.
- Retrieval questions cover different cognitive levels: recognition,
  understanding, application.
- Open questions and uncertainties are explicitly marked, not omitted.
- Source references are complete (document, chapter, or page number).

## Notes

- The skill is suitable for any subject and any material type (text, table,
  code, diagram).
- For exam preparation and self-tests, use the skill `academic-study-test`.
- For semester planning and deadlines, use the skill `academic-study-control`.
