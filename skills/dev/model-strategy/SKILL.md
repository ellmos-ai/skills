---
name: model-strategy
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: >
  Multi-Modell Orchestrierung und Model-Switching Strategie. Score-basierte Modellauswahl, Eskalations-Trigger, Berechtigungsmatrix und Kosten-Effizienz-Optimierung.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: dev
tags: [model-switching, orchestrierung, multi-modell, kosten-optimierung, routing]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/workflows/ing-strategie.md"
  origin_version: "2.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-15"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Model-Switching Strategie

> Multi-Modell Orchestrierung: Score-basierte Modellauswahl, Eskalations-Trigger und Kosten-Effizienz-Optimierung

---

## 1. Modell-Hierarchie

```
Level 3 (Stratege):    Opus     — Architektur, Konzepte
Level 2 (Arbeitstier): Sonnet   — Implementation, Debugging
Level 1 (Schnell):     Haiku    — Boilerplate, einfache Tasks
Level 0 (Lokal/Frei):  Ollama   — Prompts, Texte, Token-frei
```

---

## 2. Score-Berechnung

```
Dimensionen (0-10):
  KLARHEIT      : Wie eindeutig ist die Aufgabe?
  KOMPLEXITAET  : Wie viele Komponenten?
  KREATIVITAET  : Neue Loesungen noetig?
  KONTEXT       : Wie viel Vorwissen?
  KRITIKALITAET : Wie wichtig ist Perfektion?

SCORE = (10 - KLARHEIT) + KOMPLEXITAET + KREATIVITAET + KONTEXT + KRITIKALITAET
```

### Score-Schwellwerte

| Score | Modell | Beispiele |
|-------|--------|-----------|
| 0-8 | Ollama | Prompt generieren, Summaries |
| 9-12 | Haiku | __init__.py, Formatierung |
| 13-28 | Sonnet | Implementation, Bug-Fixes |
| 29-50 | Opus | Architektur, Strategie |

---

## 3. Eskalations-Trigger

### Ollama -> Haiku
- Dateizugriff benoetigt
- Analyse von Code noetig

### Haiku -> Sonnet
- Mehr als 2 Dateien betroffen
- Entscheidung zwischen Alternativen noetig
- Unerwarteter Fehler aufgetreten
- Loesch-Operation angefordert

### Sonnet -> Opus
- Architektur-Entscheidung gefordert
- 3+ Systeme muessen integriert werden
- Anforderungen widerspruechlich/unklar
- Strategische Planung noetig

### De-Eskalation
- Konzept definiert -> Sonnet uebernimmt Implementation
- Aufgabe trivial/repetitiv -> Haiku uebernimmt

---

## 4. Berechtigungsmatrix

| Operation | Ollama | Haiku | Sonnet | Opus |
|-----------|--------|-------|--------|------|
| Dateien lesen | - | Ja | Ja | Ja |
| Dateien schreiben | - | Ja | Ja | Ja |
| Dateien loeschen | - | - | Ja* | Ja |
| System-Befehle | - | - | Ja* | Ja |
| Architektur-Entscheidung | - | - | - | Ja |

*mit User-Bestaetigung

---

## 5. Kosten-Effizienz

### Token-Ersparnis durch Routing

| Aufgaben-Typ | Ohne Routing | Mit Routing | Ersparnis |
|--------------|--------------|-------------|-----------|
| Trivial (Haiku) | Opus-Tokens | Haiku-Tokens | ~80% |
| Standard (Sonnet) | Opus-Tokens | Sonnet-Tokens | ~50% |
| Ollama-geeignet | Haiku-Tokens | 0 Tokens | 100% |

---

## 6. Goldene Regel

> "Opus denkt, Sonnet baut, Haiku fuehrt aus, Ollama spart."

---

## Changelog

### 1.0.0 (2026-03-15)
- Portiert aus BACH v3.8.0 (ing-strategie v2.0.0)

---

*Portiert aus BACH v3.8.0 | Standalone-Version*
