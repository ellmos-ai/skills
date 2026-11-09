---
name: mediabrain-reader
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-11-09
description: "Use when parsing and cataloging media lists, reading logs, movie watchlists, or media metadata (e.g. 'analyze media collection', 'catalog books and films', 'structure watchlist', /mediabrain-reader). Analyzes media catalogs and metadata app-agnostically. Do NOT use for fetching video subtitle transcripts (use utilities/video-transcriber)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [media, catalog, metadata, export]
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


<img src="banner.png" width="100%" alt="mediabrain-reader banner">

# Media Catalog Reader

## Purpose

Evaluate media collections by type, status, topic, or duplicates.

**Result:** Catalog overview, quality issues, and concrete search or cleanup suggestions.

## Workflow

1. Clarify the goal, context, and requested output format.
2. Use only information supplied in the current request.
3. Produce a structured and traceable result.
4. Label assumptions and obtain confirmation before external changes.

## Example

**Input:** Summarize this JSON media export by type and status.

**Result:** Catalog overview, quality issues, and concrete search or cleanup suggestions.

## Public core and private extensions

This public skill contains only the transferable method. App-specific adapters, accounts, local paths, databases, and personal defaults belong in a private supplemental profile or private fork and must not be committed to this repository.

Without a private profile, the skill uses only information explicitly supplied in the current request.

## Limits and data protection

- Data is not persisted by default.
- No source, file, or interface is opened or changed without explicit permission.

## Changelog

### 2.0.0 (2026-07-30)

- User-neutral public core; private integrations and personal profiles removed.
