---
name: ai-portable-setup
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "একটি USB স্টিক বা যেকোনো ড্রাইভে একটি পোর্টেবল AI কর্মক্ষেত্র তৈরি করে। স্থানীয় LLM মডেল (Ollama), ভেক্টর ডেটাবেস (ChromaDB) এবং পূর্বনির্ধারিত প্রম্পট সহ RAG পাইপলাইন।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: infrastructure
tags: [portable, rag, ollama, usb-stick, offline, local-llm]
language: bn
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
translated_at: "2026-10-15T11:49:47.133819+00:00"
---
<img src="banner.png" width="100%" alt="ai-portable-setup banner">

# AI Portable Setup

স্থানীয় RAG পাইপলাইন সহ একটি পোর্টেবল AI কার্যপরিবেশ তৈরি করে।
USB স্টিক বা বাহ্যিক ড্রাইভের জন্য উদ্দেশ্যে তৈরি -- Ollama এবং স্থানীয়
এমবেডিং মডেলের সাথে অফলাইনে কাজ করে।

## দ্রুত শুরু

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

## তৈরি হওয়া ডিরেক্টরি কাঠামো

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

## RAG পাইপলাইন

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

## কোয়েরি মোড

| মোড | প্রম্পট | ব্যবহার |
|-------|--------|------------|
| `default` | সাধারণ সহকারী | সাধারণ কোয়েরি |
| `icf` | ICF-কাঠামোবদ্ধকরণ | পর্যবেক্ষণগুলোকে ICF অনুযায়ী শ্রেণিবদ্ধ করা |
| `coding` | কোডিং সহকারী | কোড লেখা ও ব্যাখ্যা করা |
| `rpg` | গেম মাস্টার | Pen-and-Paper রোলপ্লেইং গেম |

## লক্ষ্য সিস্টেমের প্রয়োজনীয়তা

- Python 3.10+
- Ollama (`mistral:instruct` এবং `nomic-embed-text` সহ)
- Mistral-এর জন্য ~8 GB RAM

## পরিবর্তন লগ

### 1.0.0 (2026-03-12)
- MODULAR_AGENTS/AI-Portable থেকে একীভূতকরণ
- একক-ফাইল Skill হিসেবে সেটআপ স্ক্রিপ্ট
- 4টি পূর্বনির্ধারিত প্রম্পট (coding, icf, rpg, default)
- RAG পাইপলাইন (ingest, query, pipeline)
