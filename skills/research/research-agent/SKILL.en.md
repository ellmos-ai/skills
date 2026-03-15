---
name: research-agent
version: 0.1.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: >
  Research pipeline for PubMed and arXiv. Quick search and structured
  literature reviews using pure Python standard library.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true

category: research
tags: [pubmed, arxiv, literature-review, research, science]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "MODULAR_AGENTS/ResearchAgent"
  origin_version: "0.1.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Research Agent

Modular research pipeline for scientific literature search.
Uses exclusively Python standard library (urllib, xml, json).

## Architecture

```
ResearchAgent (Orchestrator)
  sources/          Data sources (PubMed, arXiv)
    base.py         Article/SearchResult dataclasses, Source ABC
    pubmed.py       NCBI E-utilities (esearch + efetch)
    arxiv.py        arXiv Atom API
  workflows/        Research workflows
    quick_search.py Quick search across multiple sources
    literature_review.py  4-phase literature review
```

## Usage as Python Library

```python
from scripts.agent import ResearchAgent

agent = ResearchAgent()

# Quick search
result = agent.search("machine learning diagnostics", max_results=10)
print(result)

# Structured literature review
plan = agent.create_review_plan("transformer architectures", years=3)
print(plan.total_articles, "articles found")

# Save result
agent.save_result(result, "research_ml.md", fmt="markdown")
```

## Usage as CLI

```bash
cd scripts
python -m ResearchAgent search "quantum computing" --max 20
python -m ResearchAgent review "CRISPR gene editing" --years 5
```

## Data Sources

| Source | API | Rate Limit | Access |
|--------|-----|------------|--------|
| PubMed | NCBI E-utilities | 3/s (without key), 10/s (with key) | Free |
| arXiv | Atom REST API | None documented | Free |

Extensible: New sources implement the `Source` ABC from `sources/base.py`.

## Extension

```python
from scripts.sources.base import Source, SearchResult

class MySource(Source):
    @property
    def name(self) -> str:
        return "my-source"

    def search(self, query, max_results=10, **kwargs):
        # Implement API query
        ...

    def get_article(self, article_id):
        ...

    def is_available(self) -> bool:
        return True
```

## BACH Notes

> Only relevant when used within BACH.

```python
from scripts.agent import ResearchAgent
agent = ResearchAgent(use_bach=True)  # Optional BACH integration
```

## Changelog

### 0.1.0 (2026-03-12)
- Migration from MODULAR_AGENTS/ResearchAgent to skill library
- PubMed + arXiv sources
- QuickSearch + LiteratureReview workflows
