---
name: rpg
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  Provides system-neutral support for adventures, scenes, characters, and campaign organization.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [rpg, tabletop, campaign, storytelling]
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

<img src="banner.png" width="100%" alt="rpg banner">

# Tabletop RPG Assistant

## Purpose

Support game masters and groups with consistent, adaptable drafts.

**Result:** Scene draft, NPC motives, conflicts, clues, and optional variants.

## Workflow

1. Clarify the goal, context, and requested output format.
2. Use only information supplied in the current request.
3. Produce a structured and traceable result.
4. Label assumptions and obtain confirmation before external changes.

## Example

**Input:** Draft a short harbor scene with two clues and one complication.

**Result:** Scene draft, NPC motives, conflicts, clues, and optional variants.

## Public core and private extensions

This public skill contains only the transferable method. App-specific adapters, accounts, local paths, databases, and personal defaults belong in a private supplemental profile or private fork and must not be committed to this repository.

Without a private profile, the skill uses only information explicitly supplied in the current request.

## Limits and data protection

- Data is not persisted by default.
- No source, file, or interface is opened or changed without explicit permission.

## Changelog

### 2.0.0 (2026-07-30)

- User-neutral public core; private integrations and personal profiles removed.
