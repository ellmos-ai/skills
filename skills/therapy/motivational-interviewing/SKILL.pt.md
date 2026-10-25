---
name: motivational-interviewing
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "Entrevista Motivacional (MI) segundo Miller e Rollnick: técnicas OARS, Change Talk e promoção da prontidão para a mudança."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [motivational-interviewing, oars, change-talk, ambivalenz, miller-rollnick]
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
  origin_path: "system/skills/therapie/motivational_interviewing.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: 01de6c62c2cec0733b415e304542ee71c54dfcf03f9873fbfddab29c8125c1f7
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:40:39.337351+00:00"
---
<img src="banner.png" width="100%" alt="motivational-interviewing banner">

# Entrevista Motivacional (Motivational Interviewing)

> Técnicas OARS, estágios de prontidão para a mudança e Change Talk: promover a motivação para a mudança sem pressão ou manipulação

Veja: [ETHICS.md](../ETHICS.md)

---

## Contexto

A Entrevista Motivacional (Motivational Interviewing, MI) foi desenvolvida por William R. Miller e Stephen Rollnick.
É uma abordagem de aconselhamento centrada no cliente e diretiva, voltada à promoção da
motivação intrínseca para a mudança. A MI é aplicada com base em evidências no tratamento de
dependências, em comportamentos de saúde, na adesão a terapias e na mudança de comportamento.

Evidência: Mais de 200 ensaios clínicos randomizados (RCTs) comprovam a eficácia da MI, especialmente em
comportamentos de dependência (Lundahl et al. 2010, Cochrane Review), comportamentos de saúde
e adesão ao tratamento.

**Nota:** Isto é apoio, não substitui a terapia profissional.
**Nunca implementar:** EMDR, Prolonged Exposure (PE), Narrative Exposure Therapy (NET)

---

## 1. Atitude fundamental da MI

### Os quatro princípios básicos

1. **Parceria:** Colaboração de igual para igual, não especialização
2. **Aceitação:** Respeitar a autonomia, reconhecer os pontos fortes, valor absoluto da pessoa
3. **Compaixão:** O bem-estar da pessoa está em primeiro plano
4. **Evocação:** A motivação já está na pessoa — ela é trazida à tona, não implantada

### O espírito da MI
A MI não é uma coleção de técnicas, mas uma atitude. As técnicas funcionam
apenas no contexto dessa atitude. Sem ela, a MI se torna manipulação.

---

## 2. Técnicas OARS

OARS são as quatro competências centrais da entrevista motivacional.

### O — Open Questions (Perguntas abertas)

**Princípio:** Fazer perguntas que convidem a refletir e a narrar, que não possam ser
respondidas com sim/não.

**Exemplos:**
- "O que você gostaria que mudasse?"
- "Como seria a sua vida se você tivesse conseguido essa mudança?"
- "O que levou você a pensar nisso?"
- "O que é importante para você em relação à sua saúde?"
- "O que você ganharia se mudasse isso?"

**Evitar:**
- Perguntas fechadas: "Você quer parar de fumar?"
- Perguntas sugestivas: "Você sabe que isso faz mal?"
- Perguntas com "por quê": "Por que você fez isso?" (soa acusatório)

---

### A — Affirming (Valorizar / Encorajar)

**Princípio:** Reconhecer os pontos fortes, os esforços e os passos positivos do interlocutor.
Não elogiar de forma genérica ("Você é ótimo"), mas nomear concretamente o que foi observado.

**Exemplos:**
- "É preciso coragem para falar sobre isso abertamente."
- "Você conseguiu aguentar três dias — isso mostra que você está levando a sério."
- "Apesar da situação difícil, você veio hoje — isso mostra comprometimento."
- "Você obviamente refletiu bastante sobre isso."

**Quando usar:**
- Quando a pessoa descreve passos em direção à mudança
- Quando ela não desiste apesar de contratempos
- Para fortalecer a autoeficácia

---

### R — Reflecting (Refletir / Espelhar)

**Princípio:** Devolver o que foi dito com as próprias palavras — para demonstrar compreensão
e estimular a pessoa a continuar pensando.

**Tipos de reflexão:**

| Tipo | Descrição | Exemplo |
|-----|-------------|---------|
| Simples | Repetir/parafrasear o conteúdo | "Você diz que está sendo difícil." |
| Aprofundada | Retomar o que está implícito | "Parece que você está dividido(a)." |
| Bilateral | Espelhar os dois lados da ambivalência | "Por um lado você quer parar, por outro isso lhe traz algo." |
| Exagerada | Levemente exagerar (com cuidado!) | "Então não há absolutamente nenhum motivo para mudar algo?" |

**Reflexão bilateral (ambivalência):**
```
"Einerseits sagst du, dass du gerne weniger Alkohol trinken würdest.
Andererseits ist dir der soziale Aspekt beim Feierabendbier wichtig.
Beides macht Sinn."
```

---

### S — Summarizing (Resumir)

**Princípio:** Reunir a conversa — destacando especialmente o Change Talk.

**Tipos:**
- **Agregador:** Reunir vários pontos
- **Conectivo:** Ligar o que foi dito antes com o momento atual
- **De transição:** No final da conversa, introduz os próximos passos

**Exemplo:**
```
"Lass mich zusammenfassen, was ich bisher gehört habe:
Du hast bemerkt, dass dein Schlaf sich verschlechtert hat und das
deine Arbeit beeinflusst. Du hast schon mal versucht, weniger Koffein
zu trinken, und das hat teilweise geholfen. Dir ist wichtig, fit und
leistungsfähig zu sein. Gleichzeitig ist dir der Kaffee-Genuss am Morgen
wichtig. Stimmt das so? Was möchtest du ergänzen?"
```

---

## 3. Estágios de prontidão para a mudança (Modelo Transteórico)

### Os estágios (Prochaska & DiClemente)

| Estágio | Descrição | Estratégia de MI |
|---------|-------------|-------------|
| Pré-contemplação | Sem consciência do problema, sem intenção de mudar | Informar, despertar curiosidade, não pressionar |
| Contemplação | Ambivalência: "Talvez eu devesse..." | Explorar a ambivalência, promover o Change Talk |
| Preparação | Decisão tomada, plano sendo elaborado | Apoiar o planejamento, fortalecer a confiança |
| Ação | Implementação ativa da mudança | Encorajar, trabalhar os obstáculos |
| Manutenção | Estabilizar a mudança | Prevenção de recaídas, valorizar conquistas |
| Recaída | Retorno ao comportamento anterior | Normalizar, motivar novamente, aprender com a experiência |

**Importante:** A recaída não é um fracasso, mas parte do processo de mudança.

### Reconhecer o estágio

**Perguntas orientadoras:**
- "Você já pensou em mudar algo?" (Pré-contemplação vs. Contemplação)
- "O que fala a favor, o que fala contra?" (explorar a ambivalência)
- "Você já tem ideias concretas de como faria isso?" (Preparação)
- "O que você já tentou?" (experiência de ação)

---

## 4. Reconhecer e fortalecer o Change Talk

### O que é Change Talk?

Change Talk são as falas da pessoa que apontam na direção da mudança.
A MI visa aumentar o Change Talk e não reforçar o Sustain Talk (manter
o status quo).

### Estrutura DARN-CAT

**Change Talk preparatório (DARN):**
- **D**esire (Desejo): "Eu gostaria de..."
- **A**bility (Capacidade): "Eu poderia..."
- **R**easons (Razões): "Seria melhor porque..."
- **N**eed (Necessidade): "Eu preciso mudar algo..."

**Change Talk mobilizador (CAT):**
- **C**ommitment (Compromisso): "Eu vou..."
- **A**ctivation (Ativação): "Estou pronto(a)..."
- **T**aking Steps (Passos): "Eu já..."

### Promover o Change Talk

**Estratégias:**
1. **Fazer perguntas abertas:**
   - "O que você ganharia se algo mudasse?"
   - "O que lhe dá confiança de que você conseguiria?"

2. **Escala de importância e confiança:**
   - "Em uma escala de 0 a 10, quão importante é para você essa mudança?"
   - "Quão confiante você está de que conseguiria?"
   - "Por que um 5 e não um 2?" (fortalece a motivação já existente)

3. **Explorar os extremos:**
   - "O que poderia acontecer no pior caso se nada mudasse?"
   - "Qual seria o melhor que poderia acontecer se você mudasse?"

4. **Olhar para trás e para frente:**
   - "Como era antes, quando esse tema ainda não existia?"
   - "Onde você se vê daqui a cinco anos, se tudo continuar como está?"

---

## 5. Lidar com a resistência

### A resistência como sinal

Na MI, a "resistência" é interpretada como um sinal de que o conselheiro está avançando rápido demais
ou não está respeitando suficientemente a autonomia da pessoa.

### Estratégias

| Situação | Reação |
|-----------|----------|
| "Eu não tenho problema" | Aceitar, não argumentar, demonstrar curiosidade |
| "Vocês não me entendem" | Refletir: "É importante para você ser compreendido" |
| "Isso não funciona de qualquer forma" | Explorar sucessos anteriores, fortalecer a confiança |
| A pessoa fica irritada | Reduzir o ritmo, enfatizar a autonomia, espelhar com empatia |

**Regra de ouro:** Nunca argumentar contra a resistência. Acompanhar a resistência
(Rolling with Resistance), não ir contra ela.

---

## Ética e limites

**Um assistente de IA pode:**
- Aplicar técnicas OARS para estimular a reflexão
- Reconhecer o Change Talk e devolvê-lo de forma espelhada
- Fornecer informações sobre processos de mudança
- Explorar a ambivalência com respeito

**Um assistente de IA NÃO pode:**
- Forçar ou manipular a mudança
- Tomar decisões pela pessoa
- Conduzir tratamento de dependência ou acompanhamento de desintoxicação
- Usar ameaças ou apelos ao medo
- Minar a autonomia da pessoa

**Princípio central:** A pessoa decide. Um assistente de IA apoia o processo de reflexão.

**Em caso de sinais de crise aguda, SEMPRE encaminhar para:**
- Telefonseelsorge (serviço de apoio telefónico): 0800 111 0 111 / 0800 111 0 222
- Serviço psiquiátrico de emergência: 112
- Krisenchat: krisenchat.de

---

*Portado do BACH v3.8.0 | Versão standalone*
*Fontes: Miller & Rollnick (2013), Prochaska & DiClemente (1983), Lundahl et al. (2010) — Não é terapia profissional*
