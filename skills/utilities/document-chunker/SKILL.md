---
name: document-chunker
version: 1.1.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-11-06
description: "Verwenden, wenn Text in Stücke zerlegt werden muss, die in eine Grenze passen: Dokumente für RAG, Embeddings oder einen Vektorspeicher vorbereiten, oder Text, der das Kontextfenster bzw. das Token-Limit eines Modells sprengt: 'teil das in Chunks', 'bereite die Docs für RAG auf', 'mein Embedding-Modell nimmt nur 512 Tokens', 'der Kontext läuft über', 'überlappende Stücke', 'jedes Stück braucht chunk_id und Quelle', /document-chunker. Zerlegt .txt-, .md-, .py- und .sh-Dateien oder ganze Ordner in überlappende Token-Chunks mit Nummer und Quellenangabe, sodass an den Schnittstellen nichts verloren geht (nur Python-Standardbibliothek, keine Abhängigkeiten). NICHT verwenden, um ein Dokument zusammenzufassen (kein Skill nötig), KI-Reste aus einem Text zu entfernen (llm-text-hygiene), PDFs oder Scans in Text umzuwandeln oder einen Lebenslauf zu erstellen (bewerbungsexperte)."

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [chunking, rag, tokens, nlp, text-processing, embedding]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/document_chunker.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="document-chunker banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.


# Document Chunker (Deutsch)

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

## Änderungsprotokoll

### 1.1.0 (2026-11-06)
- Beschreibung mit klarem Auslöser und Abgrenzung neu gefasst (Regel aus docs/CONVENTIONS.md): Einsatzsituation, typische Nutzerformulierungen und Slash-Befehl vorn, Nachbar-Skills in einer NICHT-verwenden-Klausel.

### 1.0.0 (2026-03-12)
- Ported from BACH system/tools/document_chunker.py