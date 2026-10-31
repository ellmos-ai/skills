---
name: structured-thinking
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-05-19
updated: 2026-05-19
description: "Meta-skill: Pensamento estruturado como um fluxo de trabalho em 3 fases. Combina análise (think), geração de ideias (brainstorm) e tomada de decisão (decide) em um único processo contínuo."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [denken, analyse, kreativitaet, entscheidung, workflow, meta-skill]
language: pt
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'merged_from': ['utilities/think (v1.0.0)', 'utilities/brainstorm (v1.0.0)', 'utilities/decide (v1.0.0)'], 'local_changes_since_sync': False}
translated_from_sha256: e82ba03e100146dcafad229ee0d37103ce41774ddbb87ec965cabebcf2c88fef
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:47.188265+00:00"
---
<img src="banner.png" width="100%" alt="structured-thinking banner">

# Pensamento Estruturado — Analisar, Encontrar Ideias, Decidir

> Meta-fluxo de trabalho para pensamento estruturado: da análise do problema às soluções criativas até a decisão fundamentada

---

## Visão Geral do Fluxo de Trabalho

```
Problem/Frage
     |
     v
Phase 1: ANALYSIEREN (think)
  Divide & Conquer, Root Cause, Constraint Relaxation
     |
     v
Phase 2: IDEENFINDEN (brainstorm)
  SCAMPER, Six Hats, Reverse Brainstorming, Rapid Ideation
     |
     v
Phase 3: ENTSCHEIDEN (decide)
  Pro/Con, Weighted Scoring, Scenario Analysis, Eisenhower
     |
     v
Ergebnis + Begruendung
```

---

## Fase 1: Analisar

Objetivo: Compreender o problema, identificar as causas e reconhecer a estrutura.

### Abordagens

| Método | Quando | Procedimento |
|--------|--------|--------------|
| **Dividir e Conquistar** | Problema complexo | Problema → Subproblemas → Resolver individualmente → Combinar |
| **Causa Raiz (5 Porquês)** | Sintoma visível, causa incerta | Sintoma → Por quê? → Por quê? → ... → Causa → Solução |
| **Relaxamento de Restrições** | O problema parece insolúvel | Afrouxar restrições → Resolver → Reapertar as restrições |
| **Busca por Analogia** | Problema inédito | Encontrar um problema conhecido semelhante → Adaptar a solução |

### Frameworks de Análise

| Framework | Aplicação |
|-----------|-----------|
| **SWOT** | Forças / Fraquezas / Oportunidades / Ameaças |
| **Pareto** | 80/20 — O que traz a maior alavancagem? |
| **Espinha de Peixe** | Análise sistemática de causas (Ishikawa) |

### Heurísticas em caso de incerteza

1. Qual é o cenário de pior caso?
2. Ele é reversível?
3. Quanto custa não agir?

### Heurísticas em caso de complexidade

1. Qual é o primeiro passo mais simples?
2. O que um especialista faria?
3. Qual seria a solução de 80%?

---

## Fase 2: Encontrar Ideias

Objetivo: Gerar o máximo possível de abordagens para a solução. Quantidade antes de qualidade. NENHUMA crítica durante esta fase.

### Métodos

**SCAMPER** — Melhorar sistematicamente soluções existentes:
- **S**ubstituir: O que substituir? | **C**ombinar: O que combinar? | **A**daptar: O que adaptar?
- **M**odificar: O que alterar? | **P**ut to other use (Outro uso): Para que mais? | **E**liminar: O que omitir?
- **R**everter: O que inverter?

**Six Thinking Hats** (de Bono) — 6 perspectivas em sequência:
1. Azul: Controle do processo ("Qual é a questão?")
2. Branco: Fatos ("O que sabemos?")
3. Vermelho: Emoção ("O que parece certo?")
4. Preto: Crítica ("O que poderia dar errado?")
5. Amarelo: Otimismo ("Quais são as oportunidades?")
6. Verde: Criatividade ("Quais novas ideias existem?")

**Brainstorming Reverso** — Inverter o problema:
1. "Como tornamos isso PIOR?"
2. Coletar más ideias
3. Inverter = Boas ideias

**Ideação Rápida** — 50+ ideias em 20 min:
- Rodada 1 (5 min): Ideação aberta
- Rodada 2 (5 min): Variações
- Rodada 3 (5 min): Combinações
- Rodada 4 (5 min): Ideias extremas

### Após a ideação

1. Agrupamento: Reunir ideias semelhantes
2. Matriz de Viabilidade/Impacto: Avaliar viabilidade versus efeito
3. Seleção das 5-10 melhores para a Fase 3

---

## Fase 3: Decidir

Objetivo: Escolher a melhor opção com uma justificativa transparente.

### Seleção de Framework

| Situação | Framework |
|----------|-----------|
| 2 opções, decisão rápida | **Matriz de Prós e Contras** |
| 3+ opções, vários critérios | **Pontuação Ponderada** |
| Decisão sequencial se-então | **Árvore de Decisão** |
| Alta incerteza | **Análise de Cenários** |
| Priorizar tarefas | **Matriz de Eisenhower** |

### Pontuação Ponderada (método central)

1. Reunir critérios (3-7, específicos e mensuráveis)
2. Definir pesos (soma = 100%, o mais importante ≥ 25%)
3. Avaliar as opções (escala de 1 a 10)
4. Calcular as pontuações (avaliação x peso)
5. Comparar e recomendar

### Análise de Cenários

```
Best Case (X%):      Ergebnis → Erwartungswert
Realistic Case (X%): Ergebnis → Erwartungswert
Worst Case (X%):     Ergebnis → Erwartungswert
Gesamt-Erwartungswert: [Summe]
```

### Matriz de Eisenhower

```
              DRINGEND        NICHT DRINGEND
WICHTIG       1. TUN          2. PLANEN
NICHT WICHTIG 3. DELEGIEREN   4. ELIMINIEREN
```

### Checklist de Qualidade antes da recomendação final

- [ ] Todos os critérios relevantes foram identificados?
- [ ] Os valores do usuário foram considerados?
- [ ] Os efeitos de longo prazo foram ponderados?
- [ ] Os riscos foram identificados e avaliados?
- [ ] A verificação de viés foi realizada?
- [ ] A reversibilidade foi verificada?

---

## Seleção Sensível ao Contexto

| Situação | Fase(s) recomendada(s) |
|----------|------------------------|
| "Tenho um problema" | Fase 1 (Análise) → eventualmente Fases 2+3 |
| "Preciso de ideias" | Fase 2 (Busca de Ideias) |
| "Tenho que tomar uma decisão" | Fase 3 (Decisão) |
| "Estou travado" | Fase 2 (Brainstorming Reverso) |
| "O que devo priorizar?" | Fase 3 (Eisenhower) |
| "Entender um problema complexo" | Fase 1 (Dividir e Conquistar + SWOT) |

---

## Changelog

### 1.0.0 (2026-05-19)
- Criado como meta-skill a partir de think, brainstorm e decide

---

*Meta-skill | Referência detalhada: [think](../think/SKILL.md), [brainstorm](../brainstorm/SKILL.md), [decide](../decide/SKILL.md)*
