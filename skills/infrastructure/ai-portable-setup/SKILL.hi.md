---
name: ai-portable-setup
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "एक USB स्टिक या किसी भी ड्राइव पर पोर्टेबल AI वर्कस्पेस बनाता है। स्थानीय LLM मॉडल (Ollama), वेक्टर डेटाबेस (ChromaDB) और पूर्व-कॉन्फ़िगर किए गए प्रॉम्प्ट के साथ RAG पाइपलाइन।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: infrastructure
tags: [portable, rag, ollama, usb-stick, offline, local-llm]
language: hi
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
translated_at: "2026-10-15T11:49:45.040992+00:00"
---
<img src="banner.png" width="100%" alt="ai-portable-setup banner">

# AI पोर्टेबल सेटअप

स्थानीय RAG पाइपलाइन के साथ एक पोर्टेबल AI कार्य वातावरण बनाता है।
USB स्टिक या बाहरी ड्राइव के लिए अभिप्रेत -- Ollama और स्थानीय एम्बेडिंग मॉडल
के साथ ऑफ़लाइन काम करता है।

## त्वरित प्रारंभ

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

## बनाई गई निर्देशिका संरचना

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

## RAG पाइपलाइन

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

## क्वेरी मोड

| मोड | प्रॉम्प्ट | उपयोग |
|-----|-----------|-------|
| `default` | सामान्य सहायक | मानक क्वेरी |
| `icf` | ICF संरचना | अवलोकनों को ICF के अनुसार वर्गीकृत करना |
| `coding` | कोडिंग सहायक | कोड लिखना और समझाना |
| `rpg` | गेम मास्टर | पेन-और-पेपर रोलप्ले |

## लक्ष्य सिस्टम पर आवश्यकताएँ

- Python 3.10+
- Ollama (`mistral:instruct` और `nomic-embed-text` के साथ)
- Mistral के लिए ~8 GB RAM

## चेंजलॉग

### 1.0.0 (2026-03-12)
- MODULAR_AGENTS/AI-Portable से समेकन
- सेटअप स्क्रिप्ट को एकल-फ़ाइल स्किल के रूप में
- 4 पूर्व-कॉन्फ़िगर किए गए प्रॉम्प्ट (coding, icf, rpg, default)
- RAG पाइपलाइन (ingest, query, pipeline)
