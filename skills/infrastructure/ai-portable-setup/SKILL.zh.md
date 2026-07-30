---
name: ai-portable-setup
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 在 USB 驱动器或任何磁盘上创建便携式 AI 工作区。带有本地 LLM 模型 (Ollama)、向量数据库 (ChromaDB) 和预配置 prompt 的 RAG 流水线。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: infrastructure
tags: [portable, rag, ollama, usb-drive, offline, local-llm]
language: zh
status: active
dependencies: {'tools': [], 'services': ['ollama'], 'protocols': [], 'python': ['chromadb', 'ollama']}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/AI-Portable', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **中文** — `ai-portable-setup` 官方中文版本。


# AI Portable Setup (中文)

创建一个带有本地 RAG 流水线的便携式 AI 工作区。
专为 USB 驱动器或外接硬盘设计 — 可与 Ollama 及本地嵌入模型结合离线使用。

## 快速开始

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

## 生成的目录结构

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

## RAG 流水线

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

## 查询模式

| 模式 | Prompt | 用途 |
|------|--------|------|
| `default` | 通用助手 | 标准查询 |
| `icf` | ICF 结构化 | 根据 ICF 分类观察结果 |
| `coding` | 编程助手 | 编写与解释代码 |
| `rpg` | 游戏主持人 (DM/GM) | 跑团/桌面角色扮演游戏 |

## 目标系统要求

- Python 3.10+
- Ollama（包含 `mistral:instruct` 和 `nomic-embed-text`）
- Mistral 运行需约 8 GB 内存

## 变更日志

### 1.0.0 (2026-03-12)
- 从 MODULAR_AGENTS/AI-Portable 整合
- 作为单文件 skill 的安装脚本
- 4 个预配置 prompt（coding、icf、rpg、default）
- RAG 流水线（ingest、query、pipeline）