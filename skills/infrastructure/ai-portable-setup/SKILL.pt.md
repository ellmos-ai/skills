---
name: ai-portable-setup
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "Cria um espaço de trabalho portátil de IA em um pen drive USB ou em qualquer unidade. Pipeline RAG com modelos LLM locais (Ollama), banco de dados vetorial (ChromaDB) e prompts pré-configurados."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: infrastructure
tags: [portable, rag, ollama, usb-stick, offline, local-llm]
language: pt
status: active
visibility: public
dependencies:
  tools: []
  services: ['ollama']
  protocols: []
  python: ['chromadb', 'ollama']
provenance:
  origin: "bach"
  origin_path: "MODULAR_AGENTS/AI-Portable"
  origin_version: "0.1.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 30ea4262314dcea06c66b8101eb07430b03ea4949b4cca2878cf35b6974f09ec
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.303696+00:00"
---
<img src="banner.png" width="100%" alt="ai-portable-setup banner">

# AI Portable Setup

Cria um ambiente portátil de IA com pipeline RAG local.
Pensado para pen drives USB ou unidades externas — funciona offline
com Ollama e modelos de embedding locais.

## Início rápido

```bash
# Struktur auf USB-Stick erstellen
python setup_portable.py E:\AI-Portable

# Danach auf dem Zielsystem:
cd E:\AI-Portable
python -m venv venv
venv\Scripts\activate          # Windows
pip install chromadb ollama

# Dokumente indexieren
python rag/ingest.py

# Abfragen
python rag/query.py "Meine Frage..."
python rag/query.py --mode icf "Beobachtungen zum Klienten"
```

## Estrutura de diretórios gerada

```
AI-Portable/
  models/
    llm/                  Lokale LLM-Modelle (Mistral, Llama, etc.)
    embeddings/           Embedding-Modelle (nomic-embed-text, bge-small)
    tts/                  Optional: Text-to-Speech (Piper, Coqui)
  db/
    chroma/               ChromaDB Vektordatenbank
    sqlite/               Metadaten-DB
  documents/
    code/                 Code-Snippets, Projekte
    general/              Allgemeine Dokumente
  rag/
    ingest.py             Dateien einlesen und indexieren
    query.py              RAG-Abfragen mit Modus-Auswahl
    pipeline.py           Haupt-RAG-Pipeline (Embed + Query + LLM)
  prompts/
    coding.txt            Coding-Assistent Prompt
    icf.txt               ICF-Strukturierung Prompt
    rpg.txt               Pen-and-Paper Spielleiter Prompt
  templates/              Word/PDF-Vorlagen
  venv/                   Portable Python-Umgebung
```

## Pipeline RAG

```
Dokumente -> Chunking -> Embedding (nomic-embed-text)
                              |
                              v
                         ChromaDB (lokal)
                              |
Frage -> Embedding -> Similarity Search -> Top-K Chunks
                                              |
                                              v
                                    Kontext + Prompt -> Ollama (Mistral)
                                              |
                                              v
                                          Antwort
```

## Modos de consulta

| Modo | Prompt | Uso |
|------|--------|-----|
| `default` | Assistente geral | Consultas padrão |
| `icf` | Estruturação ICF | Classificar observações segundo a CIF |
| `coding` | Assistente de programação | Escrever e explicar código |
| `rpg` | Mestre de jogo | RPG de mesa (Pen-and-Paper) |

## Pré-requisitos no sistema de destino

- Python 3.10+
- Ollama (com `mistral:instruct` e `nomic-embed-text`)
- ~8 GB de RAM para o Mistral

## Changelog

### 1.0.0 (2026-03-12)
- Consolidação a partir de MODULAR_AGENTS/AI-Portable
- Script de configuração como skill de arquivo único
- 4 prompts pré-configurados (coding, icf, rpg, default)
- Pipeline RAG (ingest, query, pipeline)
