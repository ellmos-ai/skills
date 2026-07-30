---
name: ai-portable-setup
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: USBドライブやその他のドライブ上にポータブルAIワークスペースを作成します。ローカルLLMモデル (Ollama)、ベクトルデータベース (ChromaDB)、事前設定されたプロンプトを備えたRAGパイプライン。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: infrastructure
tags: [portable, rag, ollama, usb-drive, offline, local-llm]
language: ja
status: active
dependencies: {'tools': [], 'services': ['ollama'], 'protocols': [], 'python': ['chromadb', 'ollama']}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/AI-Portable', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="ai-portable-setup banner">

> **日本語** — `ai-portable-setup` の公式日本語版。


# AI Portable Setup (日本語)

ローカルRAGパイプラインを備えたポータブルAIワークスペースを作成します。
USBドライブや外付けドライブ向けに設計されており、Ollamaおよびローカル埋め込みモデルによりオフラインで動作します。

## クイックスタート

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

## 生成されるディレクトリ構造

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

## RAG パイプライン

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

## クエリモード

| モード | プロンプト | 用途 |
|------|--------|------|
| `default` | 汎用アシスタント | 標準的なクエリ |
| `icf` | ICF 構造化 | ICF に基づく観察結果の分類 |
| `coding` | コーディングアシスタント | コードの記述および説明 |
| `rpg` | ゲームマスター | TRPG (テーブルトークRPG) |

## ターゲットシステムの要件

- Python 3.10+
- Ollama (`mistral:instruct` および `nomic-embed-text` を含む)
- Mistral用メモリ: 約8 GB RAM

## 変更履歴

### 1.0.0 (2026-03-12)
- MODULAR_AGENTS/AI-Portable からの統合
- 単一ファイル skill としてのセットアップスクリプト
- 4つの事前設定済みプロンプト (coding, icf, rpg, default)
- RAG パイプライン (ingest, query, pipeline)