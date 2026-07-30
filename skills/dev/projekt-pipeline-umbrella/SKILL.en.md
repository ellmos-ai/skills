---
name: projekt-pipeline-umbrella
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-07-30
description: >
  Meta/Umbrella skill for the "Project/Pipeline Construction & Restructuring" family. Knows all skills
  for creating, onboarding, restructuring, and analyzing projects and pipelines, and routes to the appropriate one.
  Use this skill when it is unclear whether something should be newly created (greenfield) or restructured
  (existing), or whether it involves a single project or an entire pipeline. Also trigger on "create new project/pipeline",
  "restructure existing", "onboard project", "renovate directory structure", "which bootstrapper fits".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [projekt, pipeline, bootstrap, umbau, umbrella, meta, routing]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: [project-bootstrapper, pipeline-bootstrapper, project-onboarding, pipeline-optimizer, docs-analysis, dev-cycle]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/projekt-pipeline-umbrella/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="projekt-pipeline-umbrella banner">

# Project/Pipeline Setup & Restructuring — Umbrella

## Purpose

Entry point for the "Project/Pipeline Setup & Restructuring" family. Members are organized along two axes: **Greenfield vs. Existing** and **Project Level vs. Pipeline Level**. This umbrella prevents common confusion between "bootstrap" vs. "optimize" vs. "onboard".

## Members & Routing

| Skill | What it's for | When to use this instead of others |
|-------|-------|-------------------------------|
| `/project-bootstrapper` | Create a NEW project **in** an existing pipeline | Greenfield, Project Level |
| `/pipeline-bootstrapper` | Create a COMPLETELY NEW top-level pipeline | Greenfield, Pipeline Level (rare) |
| `/project-onboarding` | Onboard/capture an existing project | Existing, Project Level |
| `/pipeline-optimizer` | Renovate existing pipeline/structure (6-step procedure) | Existing, Restructuring |
| `/docs-analysis` | Check requirement/concept docs against current code | Existing, Analysis (no restructuring) |
| `/dev-cycle` | 8-phase development framework for actual building | Cross-cutting: HOW to develop |

> Routing Rule: **new + project** → `/project-bootstrapper` · **new + pipeline** → `/pipeline-bootstrapper` · **onboard existing** → `/project-onboarding` · **restructure existing** → `/pipeline-optimizer` · **check only** → `/docs-analysis` · **build** → `/dev-cycle`.

## Well-Coupled Combinations

- `/project-onboarding` (first: capture existing) → `/pipeline-optimizer` (afterwards: targeted restructuring) — understand first, then renovate (covers the 6-step principle "read first, then write").
- `/docs-analysis` (find gaps) → `/dev-cycle` (close gaps).
- `/project-bootstrapper` (scaffold) → `/dev-cycle` (develop content).

## Common Conventions

- Always read existing pipeline conventions (Registry, Templates, CLAUDE.md) first — do not create parallel standards.
- Greenfield skills create, existing skills renovate — do not mix them.
- Read live files of individual skills before applying.

## Changelog

### 0.1.0 (2026-06-17)
- Initial version. Created by audit mode (3c1) for the project/pipeline family.
