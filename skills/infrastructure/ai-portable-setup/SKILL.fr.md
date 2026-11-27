---
name: ai-portable-setup
version: 1.0.1
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-11-22
description: "À utiliser pour configurer un espace de travail IA portable et local sur une clé USB ou un disque externe (ex. 'installation IA portable', 'IA sur clé USB', 'pipeline RAG local hors ligne', /ai-portable-setup). Configure les modèles locaux (Ollama), la base vectorielle (ChromaDB) et les prompts modulaires pour un usage autonome hors ligne. Ne PAS utiliser pour l'onboarding complet d'un poste de travail (utiliser system-onboarding)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: infrastructure
tags: [portable, rag, ollama, usb-stick, offline, local-llm]
language: fr
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
---


<img src="banner.png" width="100%" alt="ai-portable-setup banner">

> **Français** — Version française officielle de la compétence `ai-portable-setup`.

# AI Portable Setup — Espace IA portable

Crée un environnement de travail IA portable équipé d'un pipeline RAG local.
Conçu pour des clés USB ou des disques externes — fonctionne hors ligne
avec Ollama et des modèles d'embeddings locaux.

## Démarrage rapide

```bash
# Créer la structure sur la clé USB
python setup_portable.py E:\AI-Portable

# Ensuite sur le système cible :
cd E:\AI-Portable
python -m venv venv
venv\Scripts\activate          # Windows
pip install chromadb ollama

# Indexer les documents
python rag/ingest.py

# Interroger
python rag/query.py "Ma question..."
python rag/query.py --mode icf "Observations sur le client"
```

## Arborescence générée

```
AI-Portable/
  models/
    llm/                  Modèles LLM locaux (Mistral, Llama, etc.)
    embeddings/           Modèles d'embeddings (nomic-embed-text, bge-small)
    tts/                  Optionnel : synthèse vocale (Piper, Coqui)
  db/
    chroma/               Base de données vectorielle ChromaDB
    sqlite/               Base de métadonnées
  documents/
    code/                 Extraits de code, projets
    general/              Documents généraux
  rag/
    ingest.py             Lire et indexer les fichiers
    query.py              Requêtes RAG avec sélection de mode
    pipeline.py           Pipeline RAG principal (Embed + Query + LLM)
  prompts/
    coding.txt            Prompt assistant de codage
    icf.txt               Prompt structuration ICF
    rpg.txt               Prompt maître de jeu jeu de rôle papier
  templates/              Modèles Word/PDF
  venv/                   Environnement Python portable
```

## Pipeline RAG

```
Documents -> Découpage (Chunking) -> Embedding (nomic-embed-text)
                                           |
                                           v
                                     ChromaDB (local)
                                           |
Question -> Embedding -> Recherche de similarité -> Top-K Chunks
                                                       |
                                                       v
                                             Contexte + Prompt -> Ollama (Mistral)
                                                       |
                                                       v
                                                   Réponse
```

## Modes d'interrogation

| Mode | Prompt | Utilisation |
|------|--------|-------------|
| `default` | Assistant général | Requêtes standard |
| `icf` | Structuration ICF | Classifier des observations selon la CIF (ICF) |
| `coding` | Assistant de codage | Écrire et expliquer du code |
| `rpg` | Maître de jeu | Jeu de rôle sur table |

## Prérequis sur le système cible

- Python 3.10+
- Ollama (avec `mistral:instruct` et `nomic-embed-text`)
- ~8 Go de RAM pour Mistral

## Journal des modifications

### 1.0.1 (2026-11-22)
- Mention linguistique corrigée.

### 1.0.0 (2026-03-12)
- Consolidation depuis `MODULAR_AGENTS/AI-Portable`
- Script d'installation en tant que compétence autonome en un seul fichier
- 4 prompts préconfigurés (`coding`, `icf`, `rpg`, `default`)
- Pipeline RAG (`ingest`, `query`, `pipeline`)
