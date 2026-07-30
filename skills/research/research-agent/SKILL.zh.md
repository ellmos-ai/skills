---
name: research-agent
version: 0.1.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: 针对 PubMed 和 arXiv 的研究流水线。使用纯 Python 标准库实现快速检索与结构化文献综述。

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: research
tags: [pubmed, arxiv, literature-review, research, science]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/ResearchAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **中文** — `research-agent` 官方中文版本。


# Research Agent (中文)

用于科学文献检索的模块化研究流水线。
完全仅使用 Python 标准库（urllib、xml、json）。

## 架构

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

## 作为 Python 库使用

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

## 作为 CLI 使用

```bash
cd scripts
python -m ResearchAgent search "quantum computing" --max 20
python -m ResearchAgent review "CRISPR gene editing" --years 5
```

## 数据源

| 数据源 | API | 速率限制 | 访问权限 |
|--------|-----|----------|----------|
| PubMed | NCBI E-utilities | 3/s（无 API Key），10/s（有 API Key） | 免费 |
| arXiv | Atom REST API | 未记录 | 免费 |

可扩展：新数据源只需继承 `sources/base.py` 中的 `Source` 抽象基类（ABC）。

## 扩展

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

## BACH 说明

> 仅在 BACH 内部使用时相关。

```python
from scripts.agent import ResearchAgent
agent = ResearchAgent(use_bach=True)  # Optional BACH integration
```

## 变更日志

### 0.1.0 (2026-03-12)
- 从 MODULAR_AGENTS/ResearchAgent 迁移至技能库
- PubMed + arXiv 数据源
- QuickSearch + LiteratureReview 工作流