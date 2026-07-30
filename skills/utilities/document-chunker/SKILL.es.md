---
name: document-chunker
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Divide documentos en fragmentos de tokens superpuestos para canalizaciones RAG y ventanas de contexto de LLM. Sin dependencias.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [chunking, rag, tokens, nlp, text-processing, embedding]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/document_chunker.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **Español** — Versión oficial en español de `document-chunker`.


# Document Chunker (Español)

Divide documentos en fragmentos (chunks) de tokens superpuestos. Optimizado para canalizaciones RAG y ventanas de contexto de LLM. Sin dependencias externas — solo la biblioteca estándar de Python + `re`.

## Uso

### Como Biblioteca
```python
from document_chunker import DocumentChunker

chunker = DocumentChunker(chunk_size=400, overlap=80)
chunks = chunker.chunk_text("Long text...")

for chunk in chunks:
    print(f"Chunk {chunk['chunk_id']}: {chunk['tokens']} tokens")
```

### Fragmentar un Archivo
```python
chunks = chunker.chunk_document("document.md", source="My Project")
```

### Fragmentar un Directorio Completo
```python
from document_chunker import chunk_corpus

chunks = chunk_corpus(["doc1.md", "doc2.txt"], source="Corpus")
```

### Línea de Comandos (CLI)
```bash
python document_chunker.py document.md    # Single file
python document_chunker.py ./docs/        # Entire directory
```

## Parámetros

| Parámetro | Valor por defecto | Descripción |
|-----------|---------|-------------|
| chunk_size | 400 | Máximo de tokens por fragmento |
| overlap | 80 | Tokens superpuestos entre fragmentos |

## Tipos de Archivos Compatibles

`.txt`, `.md`, `.py`, `.sh`

## Registro de Cambios

### 1.0.0 (2026-03-12)
- Portado desde BACH system/tools/document_chunker.py