---
name: research-agent
version: 0.1.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: Pipeline de investigación para PubMed y arXiv. Búsqueda rápida y revisiones de literatura estructuradas usando solo la biblioteca estándar de Python.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: research
tags: [pubmed, arxiv, literature-review, research, science]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/ResearchAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="research-agent banner">

> **Español** — Versión oficial en español de `research-agent`.


# Research Agent (Español)

Pipeline de investigación modular para búsqueda de literatura científica.
Utiliza exclusivamente la biblioteca estándar de Python (urllib, xml, json).

## Arquitectura

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

## Uso como biblioteca de Python

```python
from scripts.agent import ResearchAgent

agent = ResearchAgent()

# Quick search (Deutsch)
result = agent.search("machine learning diagnostics", max_results=10)
print(result)

# Structured literature review (Deutsch)
plan = agent.create_review_plan("transformer architectures", years=3)
print(plan.total_articles, "articles found")

# Save result (Deutsch)
agent.save_result(result, "research_ml.md", fmt="markdown")
```

## Uso como CLI

```bash
cd scripts
python -m ResearchAgent search "quantum computing" --max 20
python -m ResearchAgent review "CRISPR gene editing" --years 5
```

## Fuentes de datos

| Fuente | API | Límite de velocidad | Acceso |
|--------|-----|----------------------|--------|
| PubMed | NCBI E-utilities | 3/s (sin clave), 10/s (con clave) | Gratuito |
| arXiv | Atom REST API | Ninguno documentado | Gratuito |

Extensible: Las nuevas fuentes implementan la ABC `Source` de `sources/base.py`.

## Extensión

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

## Notas de BACH

> Solo relevante cuando se utiliza dentro de BACH.

```python
from scripts.agent import ResearchAgent
agent = ResearchAgent(use_bach=True)  # Optional BACH integration
```

## Historial de cambios

### 0.1.0 (2026-03-12)
- Migración de MODULAR_AGENTS/ResearchAgent a la biblioteca de habilidades
- Fuentes de PubMed + arXiv
- Flujos de trabajo QuickSearch + LiteratureReview