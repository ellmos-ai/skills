---
name: document-chunker
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 将文档切分为重叠的 token 块，适用于 RAG 流水线和 LLM 上下文窗口。零依赖。

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [chunking, rag, tokens, nlp, text-processing, embedding]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/document_chunker.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **中文** — `document-chunker` 官方中文版本。


# Document Chunker (中文)

将文档切分为具有重叠区域的 token 块 (chunks)。针对 RAG 流水线和大语言模型 (LLM) 上下文窗口进行了优化。零外部依赖——仅基于 Python 标准库 + `re` 模块。

## 使用方法

### 作为 Python 库使用
```python
from document_chunker import DocumentChunker

chunker = DocumentChunker(chunk_size=400, overlap=80)
chunks = chunker.chunk_text("Long text...")

for chunk in chunks:
    print(f"Chunk {chunk['chunk_id']}: {chunk['tokens']} tokens")
```

### 切分单个文件
```python
chunks = chunker.chunk_document("document.md", source="My Project")
```

### 切分整个目录
```python
from document_chunker import chunk_corpus

chunks = chunk_corpus(["doc1.md", "doc2.txt"], source="Corpus")
```

### 命令行界面 (CLI)
```bash
python document_chunker.py document.md    # Single file
python document_chunker.py ./docs/        # Entire directory
```

## 参数说明

| 参数 | 默认值 | 描述 |
|-----------|---------|-------------|
| chunk_size | 400 | 每个块的最大 token 数 |
| overlap | 80 | 块之间的重叠 token 数 |

## 支持的文件类型

`.txt`, `.md`, `.py`, `.sh`

## 更新日志

### 1.0.0 (2026-03-12)
- 从 BACH system/tools/document_chunker.py 移植