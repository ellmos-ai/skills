---
name: document-chunker
version: 1.1.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-11-06
description: "テキストを上限に収まる断片に分割する必要があるときに使います。RAG、埋め込み、ベクトルストア向けにドキュメントを準備する場合や、モデルのコンテキストウィンドウ／トークン上限を超えるテキスト: 'チャンクに分割して'、'RAG 用にドキュメントを準備して'、'埋め込みモデルが512トークンしか受け付けない'、'コンテキストがあふれる'、'重なりのある断片'、'各断片に chunk_id と出典が必要'、/document-chunker。.txt、.md、.py、.sh のファイルやフォルダ全体を、番号と出典ラベル付きのオーバーラップするトークンチャンクに分割し、境界で情報が失われないようにします（Python 標準ライブラリのみ、依存関係なし）。次の用途には使わないでください: ドキュメントの要約（スキル不要）、テキストからの AI 痕跡の除去（llm-text-hygiene）、PDF やスキャンのテキスト化、履歴書の作成（bewerbungsexperte）。"

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [chunking, rag, tokens, nlp, text-processing, embedding]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/document_chunker.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="document-chunker banner">

> **日本語** — `document-chunker` の公式日本語版。


# Document Chunker (日本語)

ドキュメントをオーバーラップするトークンチャンクに分割します。RAGパイプラインおよびLLMコンテキストウィンドウ用に最適化されています。サードパーティ依存関係ゼロ — Python標準ライブラリ + `re` のみ。

## 使い方

### ライブラリとして使用
```python
from document_chunker import DocumentChunker

chunker = DocumentChunker(chunk_size=400, overlap=80)
chunks = chunker.chunk_text("Long text...")

for chunk in chunks:
    print(f"Chunk {chunk['chunk_id']}: {chunk['tokens']} tokens")
```

### ファイルのチャンク化
```python
chunks = chunker.chunk_document("document.md", source="My Project")
```

### ディレクトリ全体のチャンク化
```python
from document_chunker import chunk_corpus

chunks = chunk_corpus(["doc1.md", "doc2.txt"], source="Corpus")
```

### CLI
```bash
python document_chunker.py document.md    # Single file
python document_chunker.py ./docs/        # Entire directory
```

## パラメータ

| パラメータ | デフォルト値 | 説明 |
|-----------|---------|-------------|
| chunk_size | 400 | チャンクあたりの最大トークン数 |
| overlap | 80 | チャンク間のオーバーラップトークン数 |

## サポートするファイル形式

`.txt`, `.md`, `.py`, `.sh`

## 変更履歴

### 1.1.0 (2026-11-06)
- 説明文を明確なトリガーと境界づけで書き直し（docs/CONVENTIONS.md の規則）: 使用場面、典型的なユーザーの言い回し、スラッシュコマンドを先頭に置き、隣接スキルを「使わない場合」の節で明示。

### 1.0.0 (2026-03-12)
- BACH system/tools/document_chunker.py より移植