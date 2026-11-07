---
name: think
version: 1.1.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-11-06
description: "Use when a problem outside the code has to be understood before anything is decided or changed: a process, organisation, product, strategy, metric or business-level system behaviour with several possible causes, a tangle to break into parts, or a situation that needs a SWOT or 80/20 view: 'why does ... keep happening', 'find the root cause', 'five whys', 'split this into sub-problems', 'where do I start', 'quick SWOT', 'what is really going on', /think. Applies Divide & Conquer, Root Cause Analysis, Constraint Relaxation, Analogy Search, SWOT, Pareto and Fishbone, and ends with the cause or structure found and the first thing to check. Do NOT use for software defects (error messages, failing builds, tests or deploys, regressions: bugfix-protocol), to generate many ideas (brainstorm), to choose between given options (decide), to mine ideas against project history (idea-mining) or for the full analyse-ideate-decide chain (structured-thinking)."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [thinking, problem-solving, analysis, swot, root-cause, heuristics]
language: en
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/think.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="think banner">

> **English** — Offizielle English-Version / Documento Oficial en English.


# Think — Problem Solving & Analysis (English)

> Structured thinking processes for complex problems

---

## Problem-Solving Approaches

### 1. Divide & Conquer

```
Problem -> Sub-problems -> Solve individually -> Combine
```

### 2. Root Cause Analysis

```
Symptom -> Why? -> Why? -> Why? -> Root cause -> Solution
```

### 3. Constraint Relaxation

```
Unsolvable problem -> Relax constraints -> Solve -> Re-apply constraints
```

### 4. Analogy Search

```
New problem -> Similar known problem -> Adapt solution
```

---

## Analysis Methods

| Method | Application |
|--------|-------------|
| **SWOT** | Strengths/Weaknesses/Opportunities/Threats |
| **Pro/Con** | Decision making |
| **Pareto** | 80/20 prioritization |
| **Fishbone** | Root cause analysis |

---

## Decision Heuristics

### Under Uncertainty

```
1. What is the worst-case scenario?
2. Is it reversible?
3. What is the cost of inaction?
```

### Under Complexity

```
1. What is the simplest first step?
2. What would an expert do?
3. What would the 80% solution be?
```

---

## Changelog

### 1.1.0 (2026-11-06)
- Description rewritten with a clear trigger and delimitation (rule from docs/CONVENTIONS.md): situation of use, typical user phrases and the slash command first, neighbouring skills named in a Do NOT clause.

### 1.0.0 (2026-03-15)
- Ported from BACH v3.8.0

---

*Ported from BACH v3.8.0 | Standalone Version*