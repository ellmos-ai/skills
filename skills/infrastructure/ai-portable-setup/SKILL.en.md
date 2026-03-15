---
name: ai-portable-setup
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Creates a portable AI workspace on a USB drive or any drive.
  RAG pipeline with local LLM models (Ollama), vector database
  (ChromaDB), and preconfigured prompts.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: infrastructure
tags: [portable, rag, ollama, usb-drive, offline, local-llm]
language: en
status: active

dependencies:
  tools: []
  services: [ollama]
  protocols: []
  python: [chromadb, ollama]

provenance:
  origin: "bach"
  origin_path: "MODULAR_AGENTS/AI-Portable"
  origin_version: "0.1.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# AI Portable Setup

Creates a portable AI workspace with a local RAG pipeline.
Designed for USB drives or external drives — works offline
with Ollama and local embedding models.

## Quick Start

```bash
# Create structure on USB drive
python setup_portable.py E:\AI-Portable

# Then on the target system:
cd E:\AI-Portable
python -m venv venv
venv\Scripts\activate          # Windows
pip install chromadb ollama

# Index documents
python rag/ingest.py

# Query
python rag/query.py "My question..."
python rag/query.py --mode icf "Observations about the client"
```

## Generated Directory Structure

```
AI-Portable/
  models/
    llm/                  Local LLM models (Mistral, Llama, etc.)
    embeddings/           Embedding models (nomic-embed-text, bge-small)
    tts/                  Optional: Text-to-Speech (Piper, Coqui)
  db/
    chroma/               ChromaDB vector database
    sqlite/               Metadata DB
  documents/
    code/                 Code snippets, projects
    general/              General documents
  rag/
    ingest.py             Ingest and index files
    query.py              RAG queries with mode selection
    pipeline.py           Main RAG pipeline (embed + query + LLM)
  prompts/
    coding.txt            Coding assistant prompt
    icf.txt               ICF structuring prompt
    rpg.txt               Pen-and-paper game master prompt
  templates/              Word/PDF templates
  venv/                   Portable Python environment
```

## RAG Pipeline

```
Documents -> Chunking -> Embedding (nomic-embed-text)
                              |
                              v
                         ChromaDB (local)
                              |
Query -> Embedding -> Similarity Search -> Top-K Chunks
                                              |
                                              v
                                    Context + Prompt -> Ollama (Mistral)
                                              |
                                              v
                                          Response
```

## Query Modes

| Mode | Prompt | Usage |
|------|--------|-------|
| `default` | General assistant | Standard queries |
| `icf` | ICF structuring | Classify observations according to ICF |
| `coding` | Coding assistant | Write and explain code |
| `rpg` | Game master | Pen-and-paper role-playing |

## Requirements on Target System

- Python 3.10+
- Ollama (with `mistral:instruct` and `nomic-embed-text`)
- ~8 GB RAM for Mistral

## Changelog

### 1.0.0 (2026-03-12)
- Consolidation from MODULAR_AGENTS/AI-Portable
- Setup script as single-file skill
- 4 preconfigured prompts (coding, icf, rpg, default)
- RAG pipeline (ingest, query, pipeline)
