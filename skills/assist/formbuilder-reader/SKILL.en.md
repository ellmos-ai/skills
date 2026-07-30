---
name: formbuilder-reader
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  Reviews supplied form descriptions for structure, validation, clarity, and accessibility.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [forms, schema, validation, accessibility]
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

<img src="banner.png" width="100%" alt="formbuilder-reader banner">

# Form Structure Reader

## Purpose

Analyze forms from JSON, YAML, CSV, or text independently of any app.

**Result:** Field map, validation risks, accessibility findings, and concrete improvements.

## Workflow

1. Clarify the goal, context, and requested output format.
2. Use only information supplied in the current request.
3. Produce a structured and traceable result.
4. Label assumptions and obtain confirmation before external changes.

## Example

**Input:** Review this JSON form for required fields and clear labels.

**Result:** Field map, validation risks, accessibility findings, and concrete improvements.

## Public core and private extensions

This public skill contains only the transferable method. App-specific adapters, accounts, local paths, databases, and personal defaults belong in a private supplemental profile or private fork and must not be committed to this repository.

Without a private profile, the skill uses only information explicitly supplied in the current request.

## Limits and data protection

- Data is not persisted by default.
- No source, file, or interface is opened or changed without explicit permission.

## Changelog

### 2.0.0 (2026-07-30)

- User-neutral public core; private integrations and personal profiles removed.
