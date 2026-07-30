---
name: ai-portable-setup
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Crea un espacio de trabajo de IA portable en una unidad USB o cualquier disco. Pipeline RAG con modelos LLM locales (Ollama), base de datos vectorial (ChromaDB) y prompts preconfigurados.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: infrastructure
tags: [portable, rag, ollama, usb-drive, offline, local-llm]
language: es
status: active
dependencies: {'tools': [], 'services': ['ollama'], 'protocols': [], 'python': ['chromadb', 'ollama']}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/AI-Portable', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **Español** — Versión oficial en español de `ai-portable-setup`.


# AI Portable Setup (Español)

Crea un espacio de trabajo de IA portable con un pipeline RAG local.
Diseñado para unidades USB o discos externos — funciona sin conexión a internet
con Ollama y modelos de embedding locales.

## Inicio rápido

```bash
# Create structure on USB drive (Deutsch)
python setup_portable.py E:\AI-Portable

# Then on the target system: (Deutsch)
cd E:\AI-Portable
python -m venv venv
venv\Scripts\activate          # Windows
pip install chromadb ollama

# Index documents (Deutsch)
python rag/ingest.py

# Query (Deutsch)
python rag/query.py "My question..."
python rag/query.py --mode icf "Observations about the client"
```

## Estructura de directorios generada

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

## Pipeline RAG

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

## Modos de consulta

| Modo | Prompt | Uso |
|------|--------|-----|
| `default` | Asistente general | Consultas estándar |
| `icf` | Estructuración CIF | Clasificar observaciones según la CIF |
| `coding` | Asistente de programación | Escribir y explicar código |
| `rpg` | Director de juego | Juego de rol de mesa |

## Requisitos en el sistema destino

- Python 3.10+
- Ollama (con `mistral:instruct` y `nomic-embed-text`)
- ~8 GB de RAM para Mistral

## Historial de cambios

### 1.0.0 (2026-03-12)
- Consolidación desde MODULAR_AGENTS/AI-Portable
- Script de instalación como skill de un solo archivo
- 4 prompts preconfigurados (coding, icf, rpg, default)
- Pipeline RAG (ingest, query, pipeline)