---
name: ai-portable-setup
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "يُنشئ مساحة عمل ذكاء اصطناعي محمولة على محرك USB أو أي قرص آخر. خط أنابيب RAG مع نماذج LLM محلية (Ollama) وقاعدة بيانات متجهية (ChromaDB) ومطالبات مُهيّأة مسبقًا."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: infrastructure
tags: [portable, rag, ollama, usb-stick, offline, local-llm]
language: ar
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
translated_at: "2026-10-15T11:49:44.476760+00:00"
---
<img src="banner.png" width="100%" alt="ai-portable-setup banner">

# إعداد الذكاء الاصطناعي المحمول

ينشئ بيئة عمل محمولة للذكاء الاصطناعي مع خط أنابيب RAG محلي.
مصممة لمحركات USB أو الأقراص الخارجية، وتعمل دون اتصال بالإنترنت
باستخدام Ollama ونماذج التضمين المحلية.

## البدء السريع

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

## بنية الدلائل الناتجة

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

## خط أنابيب RAG

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

## أوضاع الاستعلام

| الوضع | المطالبة | الاستخدام |
|-------|----------|-----------|
| `default` | مساعد عام | الاستعلامات القياسية |
| `icf` | تنظيم ICF | تصنيف الملاحظات وفق ICF |
| `coding` | مساعد البرمجة | كتابة الشيفرة وشرحها |
| `rpg` | قائد اللعبة | لعب الأدوار بالقلم والورق |

## المتطلبات على النظام المستهدف

- Python 3.10 أو أحدث
- Ollama (مع `mistral:instruct` و`nomic-embed-text`)
- نحو 8 GB من الذاكرة RAM لنموذج Mistral

## سجل التغييرات

### 1.0.0 (2026-03-12)
- توحيد من MODULAR_AGENTS/AI-Portable
- سكربت الإعداد كمهارة بملف واحد
- 4 مطالبات مُهيّأة مسبقًا (coding، icf، rpg، default)
- خط أنابيب RAG (ingest، query، pipeline)
