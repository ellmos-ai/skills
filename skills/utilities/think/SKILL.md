---
name: think
version: 1.1.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-11-06
description: "Verwenden, wenn ein Problem außerhalb des Codes verstanden werden muss, bevor entschieden oder geändert wird: Ablauf, Organisation, Produkt, Strategie, Kennzahl oder Systemverhalten auf Geschäftsebene mit mehreren möglichen Ursachen, ein Knäuel, das in Teile zerlegt werden soll, oder eine Lage, die eine SWOT- oder 80/20-Sicht braucht: 'warum passiert ... immer wieder', 'finde die Ursache', 'fünf Warum', 'zerleg das in Teilprobleme', 'wo fange ich an', 'mach kurz eine SWOT', /think. Wendet Divide & Conquer, Ursachenanalyse, Analogiesuche, SWOT, Pareto und Fishbone an und endet mit der gefundenen Ursache bzw. Struktur und dem ersten Prüfpunkt. NICHT verwenden bei Software-Defekten (Fehlermeldungen, fehlschlagende Builds, Tests oder Deploys, Regressionen: bugfix-protocol), um viele Ideen zu erzeugen (brainstorm), zwischen vorliegenden Optionen zu wählen (decide), Ideen gegen die Projekthistorie zu schürfen (idea-mining) oder für die ganze Kette Analyse-Ideen-Entscheidung (structured-thinking)."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [thinking, problem-solving, analysis, swot, root-cause, heuristics]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/think.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---
<img src="banner.png" width="100%" alt="think banner">

# Think — Problemloesung & Analyse

> Strukturierte Denkprozesse fuer komplexe Probleme

---

## Problemloesungs-Ansaetze

### 1. Divide & Conquer

```
Problem -> Teilprobleme -> Loese einzeln -> Kombiniere
```

### 2. Root Cause Analysis

```
Symptom -> Warum? -> Warum? -> Warum? -> Ursache -> Loesung
```

### 3. Constraint Relaxation

```
Unloesbares Problem -> Constraints lockern -> Loesen -> Constraints wieder anziehen
```

### 4. Analogie-Suche

```
Neues Problem -> Aehnliches bekanntes Problem -> Loesung adaptieren
```

---

## Analyse-Methoden

| Methode | Anwendung |
|---------|-----------|
| **SWOT** | Staerken/Schwaechen/Chancen/Risiken |
| **Pro/Contra** | Entscheidungsfindung |
| **Pareto** | 80/20 Priorisierung |
| **Fishbone** | Ursachenanalyse |

---

## Entscheidungs-Heuristiken

### Bei Unsicherheit

```
1. Was ist das Worst-Case-Szenario?
2. Ist es reversibel?
3. Was kostet Nicht-Handeln?
```

### Bei Komplexitaet

```
1. Was ist der einfachste erste Schritt?
2. Was wuerde ein Experte tun?
3. Was waere die 80%-Loesung?
```

---

## Changelog

### 1.1.0 (2026-11-06)
- Beschreibung mit klarem Auslöser und Abgrenzung neu gefasst (Regel aus docs/CONVENTIONS.md): Einsatzsituation, typische Nutzerformulierungen und Slash-Befehl vorn, Nachbar-Skills in einer NICHT-verwenden-Klausel.

### 1.0.0 (2026-03-15)
- Portiert aus BACH v3.8.0

---

*Portiert aus BACH v3.8.0 | Standalone-Version*

**Siehe auch:** [brainstorm](../brainstorm/SKILL.md) (Kreativmethoden, Ideenfindung) | [decide](../decide/SKILL.md) (Entscheidungs-Frameworks)
