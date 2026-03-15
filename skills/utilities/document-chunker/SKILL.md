---
name: document-chunker
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Dokumente in ueberlappende Token-Chunks aufteilen fuer RAG-Pipelines
  und LLM-Kontextfenster. Zero Dependencies.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true

category: utilities
tags: [chunking, rag, tokens, nlp, text-processing, embedding]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/tools/document_chunker.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Document Chunker

Zerteilt Dokumente in ueberlappende Token-Chunks. Optimiert fuer RAG-Pipelines
und LLM-Kontextfenster. Zero Dependencies — nur Python stdlib + re.

## Nutzung

### Als Library
```python
from document_chunker import DocumentChunker

chunker = DocumentChunker(chunk_size=400, overlap=80)
chunks = chunker.chunk_text("Langer Text...")

for chunk in chunks:
    print(f"Chunk {chunk['chunk_id']}: {chunk['tokens']} tokens")
```

### Datei chunken
```python
chunks = chunker.chunk_document("dokument.md", source="Mein Projekt")
```

### Ganzen Ordner chunken
```python
from document_chunker import chunk_corpus

chunks = chunk_corpus(["doc1.md", "doc2.txt"], source="Corpus")
```

### CLI
```bash
python document_chunker.py dokument.md    # Einzelne Datei
python document_chunker.py ./docs/        # Ganzes Verzeichnis
```

## Parameter

| Parameter | Default | Beschreibung |
|-----------|---------|-------------|
| chunk_size | 400 | Max. Tokens pro Chunk |
| overlap | 80 | Ueberlappende Tokens zwischen Chunks |

## Unterstuetzte Dateitypen

`.txt`, `.md`, `.py`, `.sh`

## Changelog

### 1.0.0 (2026-03-12)
- Portiert aus BACH system/tools/document_chunker.py
