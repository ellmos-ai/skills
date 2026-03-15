---
name: model-strategy
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: >
  Multi-model orchestration and model-switching strategy. Score-based model selection, escalation triggers, permission matrix, and cost-efficiency optimization.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: dev
tags: [model-switching, orchestration, multi-model, cost-optimization, routing]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/workflows/ing-strategie.md"
  origin_version: "2.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-15"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Model-Switching Strategy

> Multi-model orchestration: Score-based model selection, escalation triggers, and cost-efficiency optimization

---

## 1. Model Hierarchy

```
Level 3 (Strategist):  Opus     — Architecture, concepts
Level 2 (Workhorse):   Sonnet   — Implementation, debugging
Level 1 (Fast):        Haiku    — Boilerplate, simple tasks
Level 0 (Local/Free):  Ollama   — Prompts, text, token-free
```

---

## 2. Score Calculation

```
Dimensions (0-10):
  CLARITY       : How unambiguous is the task?
  COMPLEXITY    : How many components?
  CREATIVITY    : New solutions needed?
  CONTEXT       : How much prior knowledge?
  CRITICALITY   : How important is perfection?

SCORE = (10 - CLARITY) + COMPLEXITY + CREATIVITY + CONTEXT + CRITICALITY
```

### Score Thresholds

| Score | Model | Examples |
|-------|-------|---------|
| 0-8 | Ollama | Generate prompts, summaries |
| 9-12 | Haiku | __init__.py, formatting |
| 13-28 | Sonnet | Implementation, bug fixes |
| 29-50 | Opus | Architecture, strategy |

---

## 3. Escalation Triggers

### Ollama -> Haiku
- File access needed
- Code analysis required

### Haiku -> Sonnet
- More than 2 files affected
- Decision between alternatives needed
- Unexpected error occurred
- Delete operation requested

### Sonnet -> Opus
- Architecture decision required
- 3+ systems must be integrated
- Requirements contradictory/unclear
- Strategic planning needed

### De-escalation
- Concept defined -> Sonnet takes over implementation
- Task trivial/repetitive -> Haiku takes over

---

## 4. Permission Matrix

| Operation | Ollama | Haiku | Sonnet | Opus |
|-----------|--------|-------|--------|------|
| Read files | - | Yes | Yes | Yes |
| Write files | - | Yes | Yes | Yes |
| Delete files | - | - | Yes* | Yes |
| System commands | - | - | Yes* | Yes |
| Architecture decisions | - | - | - | Yes |

*with user confirmation

---

## 5. Cost Efficiency

### Token Savings Through Routing

| Task Type | Without Routing | With Routing | Savings |
|-----------|----------------|-------------|---------|
| Trivial (Haiku) | Opus tokens | Haiku tokens | ~80% |
| Standard (Sonnet) | Opus tokens | Sonnet tokens | ~50% |
| Ollama-suitable | Haiku tokens | 0 tokens | 100% |

---

## 6. Golden Rule

> "Opus thinks, Sonnet builds, Haiku executes, Ollama saves."

---

## Changelog

### 1.0.0 (2026-03-15)
- Ported from BACH v3.8.0 (ing-strategie v2.0.0)

---

*Ported from BACH v3.8.0 | Standalone Version*
