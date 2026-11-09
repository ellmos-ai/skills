---
name: notizblock
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-11-09
description: "Use when capturing, structuring, or synthesizing spontaneous notes, thoughts, and text snippets app-agnostically (e.g. 'quick note', 'organize thoughts', 'summarize scratch notes', /notizblock). Captures and condenses freeform notes without dependency on specific proprietary note apps. Do NOT use for deep research briefings (use assist/dossier-briefing) or incident logs (use infrastructure/incident-notes)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [notes, capture, summarize, organize]
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


<img src="banner.png" width="100%" alt="notizblock banner">

# Note Assistant

## Purpose

Turn loose thoughts into discoverable topics, tasks, and decisions.

**Result:** Structured note with tags, tasks, and open items.

## Workflow

1. Clarify the goal, context, and requested output format.
2. Use only information supplied in the current request.
3. Produce a structured and traceable result.
4. Label assumptions and obtain confirmation before external changes.

## Example

**Input:** Organize these meeting notes by topic and next action.

**Result:** Structured note with tags, tasks, and open items.

## Public core and private extensions

This public skill contains only the transferable method. App-specific adapters, accounts, local paths, databases, and personal defaults belong in a private supplemental profile or private fork and must not be committed to this repository.

Without a private profile, the skill uses only information explicitly supplied in the current request.

## Limits and data protection

- Data is not persisted by default.
- No source, file, or interface is opened or changed without explicit permission.

## Changelog

### 2.0.0 (2026-07-30)

- User-neutral public core; private integrations and personal profiles removed.
