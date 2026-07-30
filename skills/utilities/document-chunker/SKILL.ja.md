---
name: document-chunker
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: RAGパイプラインやLLMのコンテキストウィンドウ向けに、ドキュメントをオーバーラップするトークンチャンクに分割します。依存関係ゼロ。

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

### 1.0.0 (2026-03-12)
- BACH system/tools/document_chunker.py より移植