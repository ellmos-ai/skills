---
name: document-chunker
version: 1.1.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-11-06
description: "Use when text has to be cut into pieces that fit a limit: preparing documents for RAG, embeddings or a vector store, or text that overflows a model's context window or token limit: 'split this into chunks', 'chunk the docs for RAG', 'my embedding model only accepts 512 tokens', 'the context overflows', 'overlapping chunks', 'each piece needs a chunk_id and a source', /document-chunker. Splits .txt, .md, .py and .sh files or whole folders into overlapping token chunks with chunk number and source label, so nothing is lost at the boundaries (Python standard library only, no dependencies). Do NOT use to summarise a document (no skill needed), to clean AI leftovers from a text (llm-text-hygiene), to convert PDFs or scans to text, or to build a CV (bewerbungsexperte)."

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [chunking, rag, tokens, nlp, text-processing, embedding]
language: en
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/document_chunker.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="document-chunker banner">

> **English** — Offizielle English-Version / Documento Oficial en English.


# Document Chunker (English)

Splits documents into overlapping token chunks. Optimized for RAG pipelines
and LLM context windows. Zero dependencies — Python stdlib + re only.

## Usage

### As Library
```python
from document_chunker import DocumentChunker

chunker = DocumentChunker(chunk_size=400, overlap=80)
chunks = chunker.chunk_text("Long text...")

for chunk in chunks:
    print(f"Chunk {chunk['chunk_id']}: {chunk['tokens']} tokens")
```

### Chunking a File
```python
chunks = chunker.chunk_document("document.md", source="My Project")
```

### Chunking an Entire Directory
```python
from document_chunker import chunk_corpus

chunks = chunk_corpus(["doc1.md", "doc2.txt"], source="Corpus")
```

### CLI
```bash
python document_chunker.py document.md    # Single file
python document_chunker.py ./docs/        # Entire directory
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| chunk_size | 400 | Max tokens per chunk |
| overlap | 80 | Overlapping tokens between chunks |

## Supported File Types

`.txt`, `.md`, `.py`, `.sh`

## Changelog

### 1.1.0 (2026-11-06)
- Description rewritten with a clear trigger and delimitation (rule from docs/CONVENTIONS.md): situation of use, typical user phrases and the slash command first, neighbouring skills named in a Do NOT clause.

### 1.0.0 (2026-03-12)
- Ported from BACH system/tools/document_chunker.py