---
name: research-agent
version: 0.1.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: Исследовательский пайплайн для PubMed и arXiv. Быстрый поиск и структурированные обзоры литературы с использованием только стандартной библиотеки Python.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: research
tags: [pubmed, arxiv, literature-review, research, science]
language: ru
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/ResearchAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="research-agent banner">

> **Русский** — Официальная русская версия `research-agent`.


# Research Agent (Русский)

Модульный исследовательский пайплайн для поиска научной литературы.
Использует исключительно стандартную библиотеку Python (urllib, xml, json).

## Архитектура

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

## Использование в качестве библиотеки Python

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

## Использование в качестве CLI

```bash
cd scripts
python -m ResearchAgent search "quantum computing" --max 20
python -m ResearchAgent review "CRISPR gene editing" --years 5
```

## Источники данных

| Источник | API | Ограничение запросов | Доступ |
|----------|-----|----------------------|--------|
| PubMed | NCBI E-utilities | 3/с (без ключа), 10/с (с ключом) | Бесплатно |
| arXiv | Atom REST API | Не задокументировано | Бесплатно |

Расширяемость: Новые источники реализуют абстрактный базовый класс `Source` из `sources/base.py`.

## Расширение

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

## Примечания BACH

> Актуально только при использовании внутри BACH.

```python
from scripts.agent import ResearchAgent
agent = ResearchAgent(use_bach=True)  # Optional BACH integration
```

## Журнал изменений

### 0.1.0 (2026-03-12)
- Миграция из MODULAR_AGENTS/ResearchAgent в библиотеку навыков
- Источники PubMed + arXiv
- Рабочие процессы QuickSearch + LiteratureReview