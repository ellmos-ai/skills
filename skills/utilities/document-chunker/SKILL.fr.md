---
name: document-chunker
version: 1.1.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-11-06
description: "À utiliser lorsqu'un texte doit être découpé en morceaux tenant dans une limite : préparer des documents pour le RAG, les embeddings ou une base vectorielle, ou texte qui dépasse la fenêtre de contexte ou la limite de tokens d'un modèle : 'découpe ça en chunks', 'prépare la doc pour le RAG', 'mon modèle d'embedding n'accepte que 512 tokens', 'le contexte déborde', 'morceaux qui se chevauchent', 'chaque morceau doit avoir un chunk_id et une source', /document-chunker. Découpe des fichiers .txt, .md, .py et .sh ou des dossiers entiers en chunks de tokens avec chevauchement, numéro et étiquette de source, afin que rien ne se perde aux jonctions (bibliothèque standard Python uniquement, sans dépendances). NE PAS utiliser pour résumer un document (aucun skill requis), nettoyer les résidus d'IA d'un texte (llm-text-hygiene), convertir des PDF ou scans en texte ni créer un CV (bewerbungsexperte)."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [chunking, rag, tokens, nlp, text-processing, embedding]
language: fr
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/document_chunker.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="document-chunker banner">

> **Français** — Documentation officielle complète traduite en français pour la compétence `document-chunker`.



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

## Journal des Modifications

### 1.1.0 (2026-11-06)
- Description réécrite avec un déclencheur clair et une délimitation (règle de docs/CONVENTIONS.md) : situation d'usage, formulations typiques et commande slash en tête, skills voisins cités dans une clause NE PAS utiliser.

### 1.0.0 (2026-03-12)
- Ported from BACH system/tools/document_chunker.py