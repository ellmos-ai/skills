---
name: document-chunker
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "Divide documentos em blocos de tokens sobrepostos para pipelines RAG e janelas de contexto de LLM. Sem dependências (apenas a biblioteca padrão do Python e re)."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [chunking, rag, tokens, nlp, text-processing, embedding]
language: pt
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/document_chunker.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: a2795563043bfc5a0bd47e5f92600df6263f1daa31449313183c0cacc0323c50
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T15:41:56.704466+00:00"
---
<img src="banner.png" width="100%" alt="document-chunker banner">

> **Português** — Versão oficial em português / Documento Oficial em Português.

# Document Chunker (Português)

Divide documentos em blocos de tokens sobrepostos. Otimizado para pipelines RAG
e janelas de contexto de LLM. Sem dependências — apenas a biblioteca padrão do Python e re.

## Uso

### Como Biblioteca
```python
from document_chunker import DocumentChunker

chunker = DocumentChunker(chunk_size=400, overlap=80)
chunks = chunker.chunk_text("Long text...")

for chunk in chunks:
    print(f"Chunk {chunk['chunk_id']}: {chunk['tokens']} tokens")
```

### Dividindo um Arquivo
```python
chunks = chunker.chunk_document("document.md", source="My Project")
```

### Dividindo um Diretório Inteiro
```python
from document_chunker import chunk_corpus

chunks = chunk_corpus(["doc1.md", "doc2.txt"], source="Corpus")
```

### CLI
```bash
python document_chunker.py document.md    # Single file
python document_chunker.py ./docs/        # Entire directory
```


## Parâmetros

| Parâmetro | Padrão | Descrição |
|-----------|---------|-----------|
| chunk_size | 400 | Máximo de tokens por bloco |
| overlap | 80 | Tokens sobrepostos entre blocos |

## Tipos de Arquivo Suportados

`.txt`, `.md`, `.py`, `.sh`

## Registro de Alterações

### 1.0.0 (2026-03-12)
- Portado de BACH system/tools/document_chunker.py
