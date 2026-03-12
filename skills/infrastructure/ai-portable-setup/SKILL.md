---
name: ai-portable-setup
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Erstellt eine portable KI-Arbeitsumgebung auf einem USB-Stick oder
  beliebigem Laufwerk. RAG-Pipeline mit lokalen LLM-Modellen (Ollama),
  Vektordatenbank (ChromaDB) und vorkonfigurierten Prompts.

# Kompatibilitaet
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

# Kategorisierung
category: infrastructure
tags: [portable, rag, ollama, usb-stick, offline, local-llm]
language: de
status: active

# Abhaengigkeiten
dependencies:
  tools: []
  services: [ollama]
  protocols: []
  python: [chromadb, ollama]

# Provenance
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

Erstellt eine portable KI-Arbeitsumgebung mit lokaler RAG-Pipeline.
Gedacht fuer USB-Sticks oder externe Laufwerke -- funktioniert offline
mit Ollama und lokalen Embedding-Modellen.

## Schnellstart

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

## Erzeugte Verzeichnisstruktur

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

## RAG-Pipeline

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

## Abfrage-Modi

| Modus | Prompt | Verwendung |
|-------|--------|------------|
| `default` | Allgemeiner Assistent | Standardabfragen |
| `icf` | ICF-Strukturierung | Beobachtungen nach ICF klassifizieren |
| `coding` | Coding-Assistent | Code schreiben und erklaeren |
| `rpg` | Spielleiter | Pen-and-Paper Rollenspiel |

## Voraussetzungen auf dem Zielsystem

- Python 3.10+
- Ollama (mit `mistral:instruct` und `nomic-embed-text`)
- ~8 GB RAM fuer Mistral

## Changelog

### 1.0.0 (2026-03-12)
- Konsolidierung aus MODULAR_AGENTS/AI-Portable
- Setup-Script als Einzeldatei-Skill
- 4 vorkonfigurierte Prompts (coding, icf, rpg, default)
- RAG-Pipeline (ingest, query, pipeline)
