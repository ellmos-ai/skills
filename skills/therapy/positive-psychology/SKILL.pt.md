---
name: positive-psychology
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "Psicologia positiva segundo Seligman: modelo PERMA, forças de caráter (VIA), exercícios de gratidão, teoria do flow e fatores de resiliência."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [positive-psychologie, perma, flow, dankbarkeit, resilienz, seligman]
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
  origin_path: "system/skills/therapie/positive_psychologie.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: aac5dd4c02f72238410afe4f475379557cecf513b2f69cf71e503ae512de8a3b
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.164575+00:00"
---
<img src="banner.png" width="100%" alt="positive-psychology banner">

# Psicologia Positiva

> Foco nas forças, gratidão, flow e PERMA segundo Seligman e Csikszentmihalyi

Ver: [ETHICS.md](../ETHICS.md)

---

## Contexto

A psicologia positiva é o estudo científico do que torna a vida digna de ser vivida (Seligman & Csikszentmihalyi, 2000). Em contraste com a psicologia clínica (o que causa doença?), ela pergunta: o que promove saúde, felicidade e resiliência?

Fundador: Martin Seligman (presidente da APA em 1998) iniciou o movimento.
Outros pioneiros: Mihaly Csikszentmihalyi (flow), Christopher Peterson (forças de caráter),
Barbara Fredrickson (broaden-and-build), Ed Diener (bem-estar subjetivo).

**Nota:** Isto é apoio, não um substituto para a terapia profissional.
**Nunca implementar:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Modelo PERMA (Seligman, 2011)

Cinco pilares do bem-estar segundo Seligman ("Flourish"):

### P — Positive Emotions (Emoções positivas)
- Alegria, gratidão, serenidade, interesse, esperança, orgulho, amor
- Fredrickson: proporção mínima de 3:1 de emoções positivas para negativas
- Exercício: "Three Good Things" (ver abaixo)

### E — Engagement (Engajamento)
- Entregar-se por completo a uma atividade (estado de flow)
- Usar as próprias forças no cotidiano
- Equilíbrio entre desafio e habilidade

### R — Relationships (Relações positivas)
- Conexão social como o preditor mais forte de bem-estar
- Responder de forma ativa e construtiva às boas notícias dos outros
- Pequenas gentilezas (Random Acts of Kindness)

### M — Meaning (Sentido)
- Pertencer a algo maior que si mesmo e servi-lo
- Sentido através do trabalho, da família, da comunidade, da espiritualidade
- Frankl: "Quem tem um porquê suporta quase qualquer como"

### A — Achievement (Realização)
- Vivenciar maestria e competência
- Definir e alcançar metas realistas
- Grit: perseverança + paixão por objetivos de longo prazo (Duckworth, 2016)

---

## 2. Forças de caráter (Classificação VIA)

Peterson e Seligman (2004) identificaram 24 forças de caráter universais
em 6 categorias de virtudes:

| Virtude | Forças |
|--------|---------|
| Sabedoria | Criatividade, curiosidade, discernimento, amor pelo aprendizado, perspectiva |
| Coragem | Bravura, perseverança, honestidade, entusiasmo |
| Humanidade | Amor, gentileza, inteligência social |
| Justiça | Trabalho em equipe, equidade, liderança |
| Moderação | Perdão, humildade, prudência, autorregulação |
| Transcendência | Apreciação da beleza, gratidão, esperança, humor, espiritualidade |

**Forças assinatura:** As 3 a 5 forças que parecem mais autênticas.
Quem usa diariamente suas forças assinatura comprovadamente se sente mais satisfeito e
menos deprimido (Seligman et al. 2005).

**Teste VIA:** Gratuito em viacharacter.org (validado cientificamente)

---

## 3. Exercícios de gratidão

### 3.1 Three Good Things (Seligman et al. 2005)

**Procedimento:**
1. Todas as noites, anotar 3 coisas boas do dia
2. Para cada uma, anotar: por que aconteceu?
3. Duração: pelo menos 1 semana, idealmente de forma permanente

**Evidência:** Bem-estar significativamente aumentado e sintomas depressivos reduzidos
ao longo de 6 meses (Seligman et al. 2005)

### 3.2 Diário de gratidão

Extensão de Three Good Things:
- De manhã: pelo que sou grato hoje? (3 pontos)
- À noite: o que foi bom hoje? O que contribuí?
- Mudança de perspectiva: pessoas, experiências, habilidades, o cotidiano

### 3.3 Carta de gratidão (Gratitude Visit)

**Procedimento:**
1. Identificar uma pessoa a quem nunca agradecemos de fato
2. Escrever uma carta concreta (300 palavras, específica)
3. Visitar a pessoa e ler a carta em voz alta

**Evidência:** Efeito de curto prazo mais forte de todas as intervenções de psicologia positiva
(Seligman et al. 2005). O efeito dura cerca de 1 mês.

---

## 4. Teoria do flow (Csikszentmihalyi, 1990)

### Definição
Flow é um estado de absorção total em uma atividade, no qual a ação
flui sem esforço e o tempo e a autoconsciência passam para segundo plano.

### Condições para o flow

| Condição | Descrição |
|-----------|-------------|
| Equilíbrio | O desafio corresponde às habilidades |
| Metas claras | Sabe-se exatamente o que fazer |
| Feedback direto | Retorno imediato sobre o progresso |
| Concentração | Atenção total na tarefa |
| Controle | Sensação de poder dominar a situação |
| Motivação intrínseca | A atividade é recompensadora em si mesma |

### Canal do flow

```
Herausforderung
     hoch   |  Angst    |  FLOW
            |           |
     niedrig|  Apathie  |  Langeweile
            +-----------|----------
              niedrig      hoch
                    Faehigkeit
```

### Promover o flow
- Eliminar distrações (celular longe, porta fechada)
- Dividir tarefas em unidades administráveis
- Ajustar o nível de dificuldade (nem fácil demais, nem difícil demais)
- Estabelecer horários regulares para a prática

---

## 5. Fatores de resiliência

Resiliência = força psíquica de resistência frente a adversidades.

### Os 7 pilares da resiliência (segundo Reivich & Shatte, 2002)

1. **Regulação emocional:** perceber e conduzir as próprias emoções
2. **Controle de impulsos:** dirigir as ações conscientemente em vez de reagir
3. **Análise causal:** avaliar as causas de forma realista
4. **Autoeficácia:** confiança na própria competência
5. **Empatia:** reconhecer e compreender as emoções dos outros
6. **Otimismo:** expectativa de futuro realista e positiva
7. **Orientação a metas:** definir e perseguir objetivos significativos

### Treinar a resiliência
- Usar conscientemente as próprias forças (forças VIA)
- Cultivar a rede social (as relações como fator de proteção nº 1)
- Autocuidado: sono, movimento, alimentação, descanso
- Flexibilidade cognitiva: buscar perspectivas alternativas
- Encontrar sentido e significado (também em situações difíceis)

---

## Ética e limites

**Um assistente de IA pode:**
- Explicar o modelo PERMA e as forças de caráter (psicoeducação)
- Orientar e acompanhar exercícios de gratidão
- Discutir as condições do flow
- Transmitir fatores de resiliência
- Apoiar a reflexão sobre as forças assinatura

**Um assistente de IA NÃO pode:**
- Tratar sozinho uma depressão clínica com psicologia positiva
- Interpretar clinicamente os resultados do teste VIA
- Recomendar a psicologia positiva como substituto da terapia
- Promover positividade tóxica ("Basta ser grato")

**Medição de progresso:**
- Bem-estar antes/depois do exercício (escala de 0 a 10)
- Sequência de gratidão: quantos dias seguidos?
- Diário de flow: quando e em que vivencio o flow?
- Forças assinatura: com que frequência usadas nesta semana?

---

*Adaptado do BACH v3.8.0 | Versão autônoma*
*Fontes: Seligman (2011), Csikszentmihalyi (1990), Peterson & Seligman (2004) — Não é terapia profissional*
