---
name: research-agent
version: 0.1.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: >
  Forschungspipeline fuer PubMed und arXiv. Schnellrecherche und
  strukturierte Literatur-Reviews mit reiner Python-Standardbibliothek.

# Kompatibilitaet
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true

# Kategorisierung
category: research
tags: [pubmed, arxiv, literature-review, research, science]
language: de
status: active

# Abhaengigkeiten
dependencies:
  tools: []
  services: []
  protocols: []
  python: []

# Provenance
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

Modulare Forschungspipeline fuer wissenschaftliche Literaturrecherche.
Nutzt ausschliesslich Python-Standardbibliothek (urllib, xml, json).

## Architektur

```
ResearchAgent (Orchestrator)
  sources/          Datenquellen (PubMed, arXiv)
    base.py         Article/SearchResult Dataclasses, Source ABC
    pubmed.py       NCBI E-utilities (esearch + efetch)
    arxiv.py        arXiv Atom API
  workflows/        Recherche-Ablauefe
    quick_search.py Schnellrecherche ueber mehrere Quellen
    literature_review.py  4-Phasen Literatur-Review
```

## Nutzung als Python-Library

```python
from scripts.agent import ResearchAgent

agent = ResearchAgent()

# Schnellrecherche
result = agent.search("machine learning diagnostics", max_results=10)
print(result)

# Strukturierter Literatur-Review
plan = agent.create_review_plan("transformer architectures", years=3)
print(plan.total_articles, "Artikel gefunden")

# Ergebnis speichern
agent.save_result(result, "recherche_ml.md", fmt="markdown")
```

## Nutzung als CLI

```bash
cd scripts
python -m ResearchAgent search "quantum computing" --max 20
python -m ResearchAgent review "CRISPR gene editing" --years 5
```

## Datenquellen

| Quelle | API | Rate-Limit | Zugang |
|--------|-----|------------|--------|
| PubMed | NCBI E-utilities | 3/s (ohne Key), 10/s (mit Key) | Frei |
| arXiv | Atom REST API | Keine dokumentiert | Frei |

Erweiterbar: Neue Quellen implementieren `Source` ABC aus `sources/base.py`.

## Erweiterung

```python
from scripts.sources.base import Source, SearchResult

class MySource(Source):
    @property
    def name(self) -> str:
        return "my-source"

    def search(self, query, max_results=10, **kwargs):
        # API-Abfrage implementieren
        ...

    def get_article(self, article_id):
        ...

    def is_available(self) -> bool:
        return True
```

## BACH-Hinweise

> Nur relevant bei Nutzung innerhalb von BACH.

```python
from scripts.agent import ResearchAgent
agent = ResearchAgent(use_bach=True)  # Optionale BACH-Integration
```

## Changelog

### 0.1.0 (2026-03-12)
- Migration aus MODULAR_AGENTS/ResearchAgent in Skillbibliothek
- PubMed + arXiv Quellen
- QuickSearch + LiteratureReview Workflows
