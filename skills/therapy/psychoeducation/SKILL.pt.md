---
name: psychoeducation
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "Psicoeducação sobre depressão, transtornos de ansiedade, TEPT, transtorno bipolar, esquizofrenia, TDAH e borderline. Transmissão de conhecimento sem diagnóstico."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [psychoedukation, depression, angst, ptbs, adhs, borderline, wissensvermittlung]
language: pt
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/psychoedukation.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: 46d1c6e4a1b2e0d5fd1a6178f283bc0f2a115334ab12e10f7f9e3863d0411c62
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.087092+00:00"
---
<img src="banner.png" width="100%" alt="psychoeducation banner">

# Psicoeducação

> Transmissão de conhecimento sobre doenças mentais, sintomas e abordagens de tratamento

Ver: [ETHICS.md](../ETHICS.md)

---

## Contexto

A psicoeducação designa a transmissão sistemática de conhecimento sobre doenças mentais
a pessoas afetadas e a familiares. O objetivo é promover a compreensão da doença,
fortalecer o autogerenciamento e reduzir o estigma.

Evidência: a psicoeducação é recomendada como componente em todas as diretrizes terapêuticas
(DGPPN, NICE, APA) e comprovadamente reduz as taxas de recaída (Xia et al. 2011,
Cochrane Review).

**Nota:** Trata-se de apoio, não de substituto para a terapia profissional.
**Nunca implementar:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. O que é psicoeducação?

### Definição
Transmissão estruturada de conhecimento sobre doenças mentais com o objetivo de
tornar as pessoas afetadas "especialistas em sua própria doença".

### Objetivos
- Compreensão da doença: O que eu tenho? Por quê?
- Reconhecer sinais precoces de alerta
- Conhecer as possibilidades de tratamento
- Promover a autoeficácia
- Reduzir o estigma
- Melhorar a adesão (adherence) ao tratamento

### Evidência
- Prevenção de recaídas na esquizofrenia: NNT = 9 (Xia et al. 2011)
- Depressão: melhora da adesão ao tratamento em 30–50% (Donker et al. 2009)
- Transtornos de ansiedade: a psicoeducação isoladamente já é levemente eficaz (Donker et al. 2009)

---

## 2. Quadros clínicos em visão geral

### 2.1 Depressão (Depressão Maior)

**O que é?** Tristeza persistente, perda de interesse e falta de energia por pelo menos
2 semanas, que vão além da tristeza normal.

**Sintomas centrais (CID-11):**
- Humor deprimido (quase o dia inteiro, quase todos os dias)
- Perda de interesse / falta de prazer (anedonia)
- Redução da energia / fadiga aumentada

**Sintomas adicionais:** Dificuldades de concentração, sentimentos de culpa, problemas de sono,
alterações do apetite, pensamentos suicidas, inibição/agitação psicomotora

**Tratamento:** TCC, medicamentos (ISRS, IRSN), atividade física, fototerapia (sazonal)
**Autoajuda:** Estrutura diária, construção de atividades, contatos sociais, atividade física, higiene do sono

### 2.2 Transtornos de ansiedade

**O que é?** Medo ou ansiedade excessivos e incontroláveis que prejudicam a vida cotidiana.

**Formas:**
- Transtorno de ansiedade generalizada (TAG): preocupação crônica
- Transtorno de pânico: crises súbitas de ansiedade com sintomas físicos
- Fobia social: medo de avaliação em situações sociais
- Fobias específicas: medo de objetos/situações concretas
- Agorafobia: medo de lugares/situações nos quais não há possibilidade de fuga

**Tratamento:** TCC (exposição, reestruturação cognitiva), ISRS, relaxamento
**Autoajuda:** Diário de ansiedade, exercícios de respiração, confrontação gradual

### 2.3 Transtorno de estresse pós-traumático (TEPT)

**O que é?** Reação persistente a uma experiência traumática (ameaça, violência,
acidente, catástrofe), com reexperiência, evitação e hiperexcitação.

**Sintomas centrais:**
- Intrusões (flashbacks, pesadelos)
- Comportamento de evitação
- Entorpecimento emocional ou hiperexcitação
- Mudanças negativas de pensamentos e humor

**Tratamento:** TCC focada em trauma, EMDR, terapia de exposição narrativa
**Autoajuda:** Técnicas de estabilização, grounding, lugares seguros — SEM autoexposição

### 2.4 Transtorno bipolar

**O que é?** Alternância entre episódios depressivos e episódios (hipo)maníacos.
Doença crônica com alto risco de recaída.

**Episódio maníaco:** Humor elevado, necessidade reduzida de sono,
ideias de grandeza, atividade aumentada, propensão a riscos, fala acelerada

**Tratamento:** Estabilizadores do humor (lítio, valproato), antipsicóticos atípicos
**Autoajuda:** Diário de humor, ritmo de sono regular, conhecer os sinais precoces de alerta

### 2.5 Esquizofrenia

**O que é?** Doença mental grave com perturbações do pensamento,
da percepção e da vivência. Afeta cerca de 1% da população.

**Sintomas positivos:** Alucinações, delírios, pensamento desorganizado
**Sintomas negativos:** Falta de energia, retraimento social, embotamento afetivo
**Sintomas cognitivos:** Atenção, memória, funções executivas

**Tratamento:** Antipsicóticos, TCC para psicoses, socioterapia, intervenções familiares
**Autoajuda:** Adesão à medicação, evitação de estresse, sinais precoces de alerta, estrutura diária

### 2.6 TDAH (Transtorno de Déficit de Atenção/Hiperatividade)

**O que é?** Transtorno do desenvolvimento neurobiológico com desatenção,
impulsividade e/ou hiperatividade. Começa na infância e persiste
em cerca de 50% dos casos na vida adulta.

**Tratamento:** Multimodal (medicação, psicoeducação, coaching, TCC)
**Autoajuda:** Apoios externos de estrutura, alarmes, listas, rotinas, atividade física

### 2.7 Transtorno de personalidade borderline (TPB)

**O que é?** Padrão de instabilidade em relacionamentos, autoimagem e
afetos, com impulsividade acentuada. Alta vulnerabilidade emocional.

**Sintomas centrais:** Relacionamentos instáveis, perturbação da identidade, impulsividade,
instabilidade afetiva, autolesão, vazio crônico, dissociações

**Tratamento:** DBT (Linehan), terapia do esquema, MBT, TFP
**Autoajuda:** Kit de habilidades, plano de emergência, habilidades de tolerância ao estresse

---

## 3. Redução do estigma

### Mitos e fatos frequentes

| Mito | Fato |
|--------|------|
| "Pessoas com doenças mentais são perigosas" | As pessoas afetadas são com mais frequência vítimas do que autoras de violência |
| "Depressão é fraqueza de vontade" | A depressão é uma doença neurobiológica |
| "Terapia é só conversar" | A terapia baseada em evidências comprovadamente altera estruturas cerebrais |
| "Isso passa sozinho" | Muitas doenças se tornam crônicas sem tratamento |
| "Medicamentos criam dependência" | Antidepressivos não produzem dependência |

### Linguagem e estigma
- "Pessoa com esquizofrenia" em vez de "esquizofrênico"
- "Pessoa com depressão" em vez de "depressivo"
- A linguagem centrada na pessoa comprovadamente reduz o estigma (Granello & Gibbs, 2016)

---

## 4. Perspectiva dos familiares

- Doenças mentais afetam todo o entorno social
- Familiares precisam de psicoeducação própria e de alívio
- Emoção expressa (EE): crítica elevada/superenvolvimento aumentam o risco de recaída
- Recomendação: grupos de familiares, psicoeducação familiar

---

## Ética e limites

**Um assistente de IA pode:**
- Fornecer informações objetivas sobre quadros clínicos
- Responder a perguntas frequentes
- Indicar recursos de aprofundamento

**Um assistente de IA NÃO pode:**
- Estabelecer ou confirmar diagnósticos
- Dar recomendações de tratamento individuais
- Substituir a psicoeducação profissional em formato de grupo

---

*Portado a partir do BACH v3.8.0 | Versão standalone*
*Fontes: CID-11, diretrizes da DGPPN, Xia et al. (2011), Donker et al. (2009), Cochrane Reviews — Sem terapia profissional*
