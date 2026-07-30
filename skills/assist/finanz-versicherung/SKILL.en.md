---
name: finanz-versicherung
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  Structures supplied finance and insurance documents into a neutral overview and checklist.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [finance, insurance, documents, checklist]
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

<img src="banner.png" width="100%" alt="finanz-versicherung banner">

# Finance and Insurance Overview

## Purpose

Organize contracts, deadlines, documents, and questions without advice or product recommendations.

**Result:** Factual overview, deadline list, and questions for a qualified adviser.

## Workflow

1. Clarify the goal, context, and requested output format.
2. Use only information supplied in the current request.
3. Produce a structured and traceable result.
4. Label assumptions and obtain confirmation before external changes.

## Example

**Input:** Create a renewal checklist from these anonymized contract details.

**Result:** Factual overview, deadline list, and questions for a qualified adviser.

## Public core and private extensions

This public skill contains only the transferable method. App-specific adapters, accounts, local paths, databases, and personal defaults belong in a private supplemental profile or private fork and must not be committed to this repository.

Without a private profile, the skill uses only information explicitly supplied in the current request.

## Limits and data protection

- Data is not persisted by default.
- No source, file, or interface is opened or changed without explicit permission.
- The skill does not replace financial, tax, legal, or insurance advice.

## Changelog

### 2.0.0 (2026-07-30)

- User-neutral public core; private integrations and personal profiles removed.
