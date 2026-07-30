---
name: ai-portable-setup
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Создает портативное рабочее пространство ИИ на USB-накопителе или любом другом диске. RAG-пайплайн с локальными моделями LLM (Ollama), векторной базой данных (ChromaDB) и предустановленными промптами.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: infrastructure
tags: [portable, rag, ollama, usb-drive, offline, local-llm]
language: ru
status: active
dependencies: {'tools': [], 'services': ['ollama'], 'protocols': [], 'python': ['chromadb', 'ollama']}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/AI-Portable', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **Русский** — Официальная русская версия `ai-portable-setup`.


# AI Portable Setup (Русский)

Создает портативное рабочее пространство ИИ с локальным RAG-пайплайном.
Разработано для USB-накопителей или внешних дисков — работает в автономном режиме (офлайн)
с Ollama и локальными моделями эмбеддингов.

## Быстрый старт

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

## Создаваемая структура каталогов

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

## RAG-пайплайн

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

## Режимы запросов

| Режим | Промпт | Использование |
|-------|--------|---------------|
| `default` | Общий ассистент | Стандартные запросы |
| `icf` | Структурирование МКФ | Классификация наблюдений по МКФ |
| `coding` | Ассистент по кодингу | Написание и объяснение кода |
| `rpg` | Гейммастер | Настольные ролевые игры |

## Требования к целевой системе

- Python 3.10+
- Ollama (с `mistral:instruct` и `nomic-embed-text`)
- ~8 ГБ ОЗУ для Mistral

## История изменений

### 1.0.0 (2026-03-12)
- Консолидация из MODULAR_AGENTS/AI-Portable
- Скрипт настройки в виде однофайлового skill
- 4 предустановленных промпта (coding, icf, rpg, default)
- RAG-пайплайн (ingest, query, pipeline)