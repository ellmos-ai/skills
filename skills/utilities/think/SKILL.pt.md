---
name: think
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: "Resolução de problemas e análise: Processos de pensamento estruturados para problemas complexos. Divisão e Conquista, Análise de Causa Raiz, SWOT, Pareto e heurísticas de decisão."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [thinking, problem-solving, analysis, swot, root-cause, heuristics]
language: pt
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/think.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: eb79ba4bdf7216c7845cd999ef2c905d4611f252d2c4b8f42404058645b37fc7
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="think banner">

# Think — Resolução de Problemas & Análise

> Processos de pensamento estruturados para problemas complexos

---

## Abordagens de Resolução de Problemas

### 1. Divisão e Conquista (Divide & Conquer)

```
Problem -> Teilprobleme -> Loese einzeln -> Kombiniere
```

### 2. Root Cause Analysis

```
Symptom -> Warum? -> Warum? -> Warum? -> Ursache -> Loesung
```

### 3. Relaxamento de Restrições

```
Unloesbares Problem -> Constraints lockern -> Loesen -> Constraints wieder anziehen
```

### 4. Busca por Analogia

```
Neues Problem -> Aehnliches bekanntes Problem -> Loesung adaptieren
```

---

## Métodos de Análise

| Método | Aplicação |
|--------|-----------|
| **SWOT** | Forças/Fraquezas/Oportunidades/Ameaças |
| **Prós/Contras** | Tomada de decisão |
| **Pareto** | Priorização 80/20 |
| **Fishbone** | Análise de causas |

---

## Heurísticas de Decisão

### Em caso de incerteza

```
1. Was ist das Worst-Case-Szenario?
2. Ist es reversibel?
3. Was kostet Nicht-Handeln?
```

### Em caso de complexidade

```
1. Was ist der einfachste erste Schritt?
2. Was wuerde ein Experte tun?
3. Was waere die 80%-Loesung?
```

---

## Changelog

### 1.0.0 (2026-03-15)
- Portado do BACH v3.8.0

---

*Portado do BACH v3.8.0 | Versão standalone*

**Veja também:** [brainstorm](../brainstorm/SKILL.md) (Métodos criativos, geração de ideias) | [decide](../decide/SKILL.md) (Frameworks de decisão)
