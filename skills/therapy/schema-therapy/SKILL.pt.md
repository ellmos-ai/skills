---
name: schema-therapy
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: "Fundamentos da Terapia do Esquema segundo Jeffrey Young: esquemas, modos, conceito da criança interior e estilos de enfrentamento — transmitidos de forma psicoeducativa."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [schematherapie, modi, inneres-kind, bewältigungsstile, persönlichkeit]
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
  origin_path: "system/skills/therapie/schematherapie.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-15"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: fdd13417d876b6ecd6aac707e41f07142711c4905c71ec15874455b2e27387c8
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="schema-therapy banner">

# Terapia do Esquema

> Fundamentos da Terapia do Esquema segundo Jeffrey Young: esquemas, modos, conceito da criança interior e estilos de enfrentamento — transmitidos de forma psicoeducativa

Ver: [ETHICS.md](../ETHICS.md)

---

## Contexto

A Terapia do Esquema foi desenvolvida por Jeffrey E. Young a partir da década de 1990 como uma extensão
da terapia cognitivo-comportamental. Ela integra elementos da TCC,
da teoria do apego, da terapia Gestalt e de abordagens psicodinâmicas.

Evidência: A Terapia do Esquema é bem fundamentada empiricamente, sobretudo
para transtornos de personalidade (Giesen-Bloo et al. 2006, Masley et al. 2012).
Na Alemanha, é reconhecida como método dentro da terapia comportamental.

**Nota:** Isto é psicoeducação, não um substituto para a terapia profissional.
**Nunca implementar:** EMDR, Exposição Prolongada (PE), Terapia de Exposição Narrativa (NET)

---

## 1. Esquemas maladaptativos precoces

### Princípio
Os esquemas são padrões emocionais e cognitivos profundamente enraizados que surgem na infância
a partir de necessidades básicas não atendidas. Eles influenciam como percebemos o mundo,
a nós mesmos e aos outros.

### As cinco necessidades básicas (segundo Young)

| Necessidade básica | Quando não atendida, surgem, por exemplo |
|--------------------|------------------------------------------|
| Apego seguro | Abandono, desconfiança |
| Autonomia e competência | Dependência, medo de fracasso |
| Limites realistas | Atitude de exigência, falta de autocontrole |
| Expressão livre de necessidades | Submissão, abnegação |
| Espontaneidade e brincadeira | Padrões exagerados, tendência à punição |

### Os 18 esquemas — visão geral (5 domínios)

**Domínio 1: Desconexão e rejeição**
- Abandono / Instabilidade
- Desconfiança / Abuso
- Privação emocional
- Defectividade / Vergonha
- Isolamento social

**Domínio 2: Autonomia prejudicada**
- Dependência / Incompetência
- Vulnerabilidade
- Emaranhamento / Self subdesenvolvido
- Fracasso

**Domínio 3: Limites prejudicados**
- Merecimento / Grandiosidade
- Autocontrole insuficiente

**Domínio 4: Heterodirecionamento**
- Subjugação
- Abnegação
- Busca por aprovação

**Domínio 5: Vigilância excessiva**
- Negativismo / Pessimismo
- Inibição emocional
- Padrões exagerados
- Tendência à punição

### Perguntas de reflexão para identificar esquemas
- "Quais crenças sobre você mesmo continuam aparecendo?"
- "Em quais situações você reage com especial intensidade emocional?"
- "Você percebe padrões que se repetem em diferentes relacionamentos?"
- "Quais necessidades possivelmente ficaram em segundo plano na sua infância?"

---

## 2. O modelo dos modos

### Princípio
Os modos são estados emocionais momentâneos ativados por esquemas.
O modelo dos modos ajuda a compreender e classificar diferentes "partes internas".

### As quatro categorias de modos

**Modos da criança:**
- *Criança vulnerável:* Sente-se triste, sozinha, ansiosa, sobrecarregada
- *Criança zangada:* Irritada por necessidades não atendidas
- *Criança impulsiva:* Age sem pensar, quer satisfação imediata
- *Criança feliz:* Sente-se segura, amada, espontânea

**Modos parentais maladaptativos:**
- *Modo parental punitivo:* Voz interna que critica, pune, deprecia
- *Modo parental exigente:* Voz interna que exige perfeição e desempenho

**Modos de enfrentamento maladaptativos:**
- *Submissão / Resignação:* Cede, adapta-se de forma exagerada
- *Evitação:* Anestesia sentimentos, retrai-se, distrai-se
- *Supercompensação:* Domina, controla, ataca

**Adulto saudável:**
- Consegue perceber necessidades e atendê-las de forma adequada
- Estabelece limites saudáveis
- Consola e acalma a criança vulnerável
- Limita os modos parentais exagerados

### Exercício: reconhecer os modos no cotidiano

```
Situation: ______________
Welchen Modus spüre ich gerade?
  [ ] Verletztes Kind — "Ich fühle mich klein und hilflos"
  [ ] Ärgerliches Kind — "Das ist unfair!"
  [ ] Strafender Elternmodus — "Du bist nicht gut genug"
  [ ] Fordernder Elternmodus — "Du musst mehr leisten"
  [ ] Vermeidung — "Ich will nicht darüber nachdenken"
  [ ] Überkompensation — "Ich zeig's denen"
  [ ] Gesunder Erwachsener — "Was brauche ich jetzt wirklich?"
```

---

## 3. Trabalho com a criança interior (psicoeducativo)

### Princípio
O trabalho com a criança interior na Terapia do Esquema visa desenvolver uma atitude interna de cuidado
em relação às próprias partes feridas.

**ATENÇÃO:** O trabalho aprofundado com a criança interior pertence ao acompanhamento terapêutico profissional.

### Exercício reflexivo: carta para a criança interior

```
Schreibe einen kurzen Brief an dein jüngeres Ich:
1. Was hättest du damals gebraucht?
2. Was würdest du dem Kind heute sagen?
3. Welchen Trost würdest du anbieten?
```

### Perguntas de reflexão
- "Quando você pensa nessa situação, quantos anos você sente ter por dentro?"
- "O que um adulto cuidadoso teria dito a você naquela época?"
- "Quais necessidades da criança dentro de você estão sendo deixadas de lado agora?"

---

## 4. Compreendendo os estilos de enfrentamento

### Os três padrões básicos

| Estilo de enfrentamento | Estratégia | Exemplo |
|-------------------------|------------|---------|
| Resignação | Aceitar o esquema, submeter-se | "Eu sou assim mesmo, não posso mudar nada" |
| Evitação | Não querer sentir o esquema | Distração, consumo de substâncias, excesso de trabalho |
| Supercompensação | Viver o oposto do esquema | Perfeccionismo no lugar da sensação de fracasso |

### Perguntas de reflexão
- "Quando você está sob pressão, tende mais a ceder, fugir ou lutar?"
- "Quais dos seus hábitos poderiam ser estratégias de evitação?"
- "Há áreas em que você faz o oposto do que realmente sente?"

---

## Ética e limites

**Um assistente de IA pode:**
- Explicar esquemas e modos como conceitos
- Fazer perguntas de reflexão para autoexploração
- Apresentar estilos de enfrentamento como psicoeducação
- Orientar exercícios reflexivos simples, por escrito, com a criança interior

**Um assistente de IA NÃO pode:**
- Diagnosticar ou atribuir esquemas
- Realizar trabalho de cadeira ou exercícios de ativação experiencial
- Oferecer reparentalização
- Trabalhar experiências traumáticas da infância
- Substituir a terapia do esquema-modos

**Em caso de sinais de crise aguda, SEMPRE encaminhar para:**
- Telefonseelsorge: 0800 111 0 111 / 0800 111 0 222
- Serviço psiquiátrico de emergência: 112
- Krisenchat: krisenchat.de

---

## Referências

- Young, J. E., Klosko, J. S. & Weishaar, M. E. (2003). *Schema Therapy: A Practitioner's Guide.* Guilford Press.
- Giesen-Bloo, J. et al. (2006). Outpatient Psychotherapy for Borderline Personality Disorder. *Archives of General Psychiatry*, 63(6), 649-658.
- Roediger, E. (2011). *Praxis der Schematherapie.* Schattauer.

---

*Portado de BACH v3.8.0 | Versão standalone*
*Fontes: Young et al. (2003), Giesen-Bloo et al. (2006), Roediger (2011) — Não é terapia profissional*
