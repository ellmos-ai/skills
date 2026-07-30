---
name: research-agent
version: 0.1.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: PubMed および arXiv 向け研究パイプライン。Python 標準ライブラリのみを使用した迅速な検索および構造化文献レビュー。

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: research
tags: [pubmed, arxiv, literature-review, research, science]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/ResearchAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **日本語** — `research-agent` の公式日本語版。


# Research Agent (日本語)

科学文献検索のためのモジュール式研究パイプライン。
Python 標準ライブラリ（urllib, xml, json）のみを使用。

## アーキテクチャ

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

## Python ライブラリとしての使用

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

## CLI としての使用

```bash
cd scripts
python -m ResearchAgent search "quantum computing" --max 20
python -m ResearchAgent review "CRISPR gene editing" --years 5
```

## データソース

| データソース | API | レート制限 | アクセス |
|--------------|-----|------------|----------|
| PubMed | NCBI E-utilities | 3回/秒（キーなし）、10回/秒（キーあり） | 無料 |
| arXiv | Atom REST API | ドキュメント記載なし | 無料 |

拡張可能: 新しいデータソースは `sources/base.py` の `Source` ABC を実装します。

## 拡張

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

## BACH に関する注記

> BACH 内で使用する場合にのみ関連します。

```python
from scripts.agent import ResearchAgent
agent = ResearchAgent(use_bach=True)  # Optional BACH integration
```

## 変更履歴

### 0.1.0 (2026-03-12)
- MODULAR_AGENTS/ResearchAgent からスキルライブラリへの移行
- PubMed + arXiv データソース
- QuickSearch + LiteratureReview ワークフロー