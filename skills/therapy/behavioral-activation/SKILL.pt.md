---
name: behavioral-activation
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "Ativação comportamental na depressão: quebrar o círculo vicioso, registro de atividades, planejamento semanal e atividades baseadas em valores."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [verhaltensaktivierung, depression, aktivität, wochenplan, werte]
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
  origin_path: "system/skills/therapie/verhaltensaktivierung.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: 0b1a46a9999f052cf5049fc127f440df9fa6aa26a15195c7250d91f9ec4c4c47
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.906820+00:00"
---
<img src="banner.png" width="100%" alt="behavioral-activation banner">

# Ativação Comportamental

> Planejamento de atividades, diário de humor-atividade e seleção de atividades baseadas em valores: contrapor-se ao círculo vicioso de inatividade e desânimo

Veja: [ETHICS.md](../ETHICS.md)

---

## Contexto

A ativação comportamental (Behavioral Activation, BA) é uma intervenção baseada em evidências
da terapia comportamental para o tratamento da depressão. Ela se baseia na constatação de que
a depressão leva ao retraimento e à inatividade, o que piora ainda mais o humor
(círculo vicioso). Por meio da construção direcionada de atividades positivas, esse ciclo é
interrompido.

Evidência: A ativação comportamental é eficaz como forma de terapia independente e equivalente
à terapia cognitiva (Dimidjian et al. 2006, estudo COBRA de Richards et al. 2016).
Recomendada como intervenção inicial em casos de depressão leve a moderada (Diretrizes NICE).

**Observação:** Isto é apoio, não substituto de terapia profissional.
Em casos de depressão grave ou pensamentos suicidas, recomendar SEMPRE ajuda profissional.
**Nunca implementar:** EMDR, Exposição Prolongada (PE), Terapia de Exposição Narrativa (NET)

---

## 1. O Modelo de Depressão da Ativação Comportamental

### O Círculo Vicioso

```
Auslösende Situation (Verlust, Stress, Veränderung)
        |
        v
Niedergeschlagenheit, Energielosigkeit
        |
        v
Rückzug, Vermeidung, Inaktivität
        |
        v
Weniger positive Erfahrungen, Isolation
        |
        v
Noch tiefere Niedergeschlagenheit
        |
        v
Noch mehr Rückzug ... (Spirale)
```

### O Princípio Contrário

```
Gezielte Aktivität (auch bei geringer Motivation)
        |
        v
Positive Erfahrung / Erfolgserlebnis / Kontakt
        |
        v
Leichte Stimmungsverbesserung
        |
        v
Etwas mehr Energie und Motivation
        |
        v
Weitere Aktivität ... (Aufwärtsspirale)
```

**Princípio central:** Não esperar até que a motivação chegue — agir gera motivação.
"Act first, feel second." (Não: "Primeiro sentir, depois agir.")

---

## 2. Diário de Humor-Atividade

### Objetivo
Tornar visíveis as relações entre atividades e humor.
Identificar quais atividades melhoram o humor e quais o pioram.

### Formato do Diário

```
STIMMUNGS-AKTIVITÄTS-TAGEBUCH

Datum: [...]

| Uhrzeit | Aktivität | Stimmung (0-10) | Freude (0-10) | Wichtigkeit (0-10) |
|---------|-----------|-----------------|---------------|---------------------|
| 07:00   | Aufgestanden, gefrühstückt | 3 | 2 | 5 |
| 08:00   | Arbeit: E-Mails | 4 | 1 | 6 |
| 10:00   | Spaziergang | 6 | 5 | 4 |
| 12:00   | Mittagessen mit Kollegin | 7 | 6 | 7 |
| 14:00   | Arbeit: Projekt | 5 | 3 | 7 |
| 18:00   | Fernsehen (allein) | 3 | 2 | 1 |
| 20:00   | Telefonat mit Freund | 6 | 5 | 8 |

Tagesdurchschnitt Stimmung: [...]
Beste Aktivität heute: [...]
Erkenntnis: [...]
```

### Avaliação após uma semana

**Perguntas orientadoras:**
- Quais atividades elevam o humor regularmente?
- Quais atividades derrubam o humor?
- Há momentos especialmente difíceis?
- Quanto tempo passo com atividades agradáveis versus desagradáveis?
- Quais atividades tenho evitado?

---

## 3. Planejamento de Atividades

### Passo 1: Criar a lista de atividades

Reunir três categorias de atividades:

**A) Atividades agradáveis (alegria, prazer)**
- Natureza: caminhada, parque, floresta
- Social: encontrar amigos, telefonar, cozinhar juntos
- Criativa: música, pintura, escrita, artesanato
- Corporal: esporte, ioga, dança, natação
- Prazer: cozinhar o prato favorito, ler um livro, ouvir música
- Relaxamento: banho, meditação, exercício de respiração

**B) Atividades necessárias (estrutura, autocuidado)**
- Casa: arrumar, cozinhar, fazer compras
- Higiene pessoal: tomar banho, vestir-se, escovar os dentes
- Administração: contas, compromissos, papelada
- Saúde: consultas médicas, medicamentos, alimentação

**C) Atividades baseadas em valores (sentido, significado)**
- Veja a seção 4 abaixo

### Passo 2: Criar o plano semanal

```
WOCHENPLAN

| Tag | Morgens | Mittags | Nachmittags | Abends |
|-----|---------|---------|-------------|--------|
| Mo  | [...]   | [...]   | [...]       | [...]  |
| Di  | [...]   | [...]   | [...]       | [...]  |
| Mi  | [...]   | [...]   | [...]       | [...]  |
| Do  | [...]   | [...]   | [...]       | [...]  |
| Fr  | [...]   | [...]   | [...]       | [...]  |
| Sa  | [...]   | [...]   | [...]       | [...]  |
| So  | [...]   | [...]   | [...]       | [...]  |
```

### Regras de planejamento
1. **Começar pequeno:** Não planejar o dia inteiro, mas 1-2 atividades por dia
2. **Mistura:** Agradável + necessário + baseado em valores
3. **Concreto:** "Terça-feira às 15h caminhada no parque" em vez de "Me movimentar mais"
4. **Realista:** Factível mesmo com pouca energia
5. **Flexível:** O plano é uma orientação, não uma obrigação
6. **Graduado:** Com energia muito baixa: pequenos passos (5 minutos bastam)

### Lidar com obstáculos

| Obstáculo | Estratégia |
|-----------|-----------|
| "Não tenho energia" | Reduzir a atividade a 5 minutos |
| "Não tenho vontade" | Lembrar: a motivação vem com a ação |
| "Não adianta de qualquer forma" | Experimento: testar e medir o humor depois |
| "Não consigo sozinho" | Envolver alguém (um compromisso = obrigação) |
| "Não tenho tempo" | Incluir pequenas atividades (subir escadas, 5 min de pausa ao ar livre) |

---

## 4. Seleção de Atividades Baseadas em Valores

### Princípio
Atividades que se alinham com valores pessoais geram bem-estar duradouro — em contraste com o
prazer puro, que passa rapidamente.

### Áreas da vida e valores

```
WERTE-KOMPASS

Beziehungen:     Was für ein Partner/Freund/Familienmitglied möchte ich sein?
Arbeit/Bildung:  Was ist mir bei meiner Arbeit wichtig?
Freizeit:        Wie möchte ich meine freie Zeit verbringen?
Gesundheit:      Wie möchte ich mit meinem Körper umgehen?
Gemeinschaft:    Welchen Beitrag möchte ich leisten?
Persönliches:   Welcher Mensch möchte ich sein?
```

### Mapeamento valores-atividades

**Exemplo:**

| Valor | Atividade | Frequência |
|------|-----------|-------------|
| Vínculo | Ligar para um amigo | 2x por semana |
| Saúde | Caminhar 20 min | Diariamente |
| Criatividade | Tocar violão | 1x por semana |
| Solidariedade | Ajudar a vizinha nas compras | 1x por semana |
| Aprendizado | Ler um livro técnico por 15 min | 3x por semana |

### Valores versus metas
- **Valor:** Uma direção em que se quer seguir (ex.: "ser um parceiro amoroso")
- **Meta:** Um ponto final alcançável (ex.: "planejar o aniversário de casamento")
- Valores nunca podem ser "riscados da lista" — eles oferecem orientação permanente

---

## 5. Medir o Progresso

### Revisão semanal

```
WOCHEN-REVIEW

Woche: [Datum]
Geplante Aktivitäten: [Anzahl]
Umgesetzte Aktivitäten: [Anzahl]
Durchschnittliche Stimmung: [0-10]

Was lief gut: [...]
Was war schwierig: [...]
Erkenntnis der Woche: [...]
Plan für nächste Woche: [...]
```

### Acompanhamento de longo prazo
- Observar a evolução do humor ao longo das semanas
- Reconhecer a relação entre o nível de atividade e o humor
- Tornar visíveis as conquistas (mesmo as pequenas)

---

## Ética e Limites

**Um assistente de IA pode:**
- Orientar pelo diário e pelo planejamento de atividades
- Fazer sugestões de atividades (nunca prescrever)
- Documentar dados de humor e devolver padrões observados
- Acompanhar a reflexão sobre valores
- Reconhecer pequenos progressos

**Um assistente de IA NÃO pode:**
- Ser o único apoio em casos de depressão grave
- Dar recomendações relacionadas a medicamentos
- Avaliar risco de suicídio
- Fazer diagnósticos
- Garantir que a ativação comportamental seja suficiente

**Importante:** Em casos de depressão grave (falta persistente de energia, pensamentos suicidas,
incapacidade de lidar com o cotidiano), a ajuda profissional é indispensável.
A ativação comportamental é complemento, não substituto.

**Em sinais de crise aguda, SEMPRE encaminhar para:**
- Telefonseelsorge (apoio emocional por telefone): 0800 111 0 111 / 0800 111 0 222
- Serviço psiquiátrico de emergência: 112
- Krisenchat: krisenchat.de

---

*Adaptado de BACH v3.8.0 | Versão standalone*
*Fontes: Martell et al. (2010), Dimidjian et al. (2006), Richards et al. (2016) — Não é terapia profissional*
