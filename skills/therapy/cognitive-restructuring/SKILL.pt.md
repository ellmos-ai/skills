---
name: cognitive-restructuring
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "Terapia cognitivo-comportamental: modelo ABC, pensamentos automáticos, reconhecimento de distorções cognitivas e manutenção de registros de pensamentos."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [kvt, kognitive-umstrukturierung, denkfehler, gedankenprotokoll, abc-modell]
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
  origin_path: "system/skills/therapie/kognitive_umstrukturierung.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: 3042221ed78753a29c5ac38a5a3b9ea22df6f9736898d0ea270efcc7164c1144
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="cognitive-restructuring banner">

# Reestruturação Cognitiva

> Técnica central da terapia comportamental: esquema ABC, reconhecimento e modificação de pensamentos disfuncionais

Veja: [ETHICS.md](../ETHICS.md)

---

## Contexto

A reestruturação cognitiva é uma técnica central da terapia cognitivo-comportamental (TCC).
Ela ajuda a reconhecer pensamentos negativos automáticos, questioná-los e substituí-los por
alternativas mais úteis.

**Observação:** Isto é um apoio, não um substituto para a terapia profissional.
**Nunca implementar:** EMDR, Exposição Prolongada (PE), Terapia de Exposição Narrativa (NET)

---

## 1. Modelo ABC (Ellis)

O modelo ABC explica como eventos, pensamentos e sentimentos se relacionam.

```
A (Activating Event)   ->  B (Beliefs / Gedanken)  ->  C (Consequences / Gefühle/Verhalten)
Ausloser                   Bewertung / Überzeugung     Emotionale Folge
```

**Importante:** Não é o evento (A) que gera a emoção (C), mas a avaliação (B)!

**Exemplo:**
```
A: Chef kritisiert einen Bericht im Meeting
B: "Ich bin inkompetent, alle denken das jetzt"
C: Scham, Rückzug, Vermeidung zukünftiger Beiträge
```

**Objetivo:** Modificar B para influenciar C.

---

## 2. Reconhecer Pensamentos Automáticos Negativos (PANs)

**O que são PANs?**
- Avaliações rápidas e automáticas em situações de estresse
- Frequentemente percebidas como fatos, embora sejam interpretações
- Tendem ao exagero, à generalização e à catastrofização

**Características típicas de reconhecimento:**
- Pensamento absoluto: "sempre", "nunca", "todos", "ninguém"
- Catastrofização: "Isso vai terminar de forma horrível"
- Leitura mental: "Ele com certeza pensa que..."
- Supergeneralização: "Isso nunca dá certo para mim"

**Perguntas de identificação:**
- "O que passou pela sua cabeça quando isso aconteceu?"
- "Ao pensar na situação, que palavras surgem?"
- "O que você teme que possa acontecer?"

---

## 3. Distorções Cognitivas (Erros de Pensamento)

| Erro de pensamento | Descrição | Exemplo |
|------------|--------------|---------|
| Tudo ou nada | Pensamento em preto e branco | "Se eu não for perfeito, sou um fracasso" |
| Supergeneralização | Um caso = padrão geral | "Isso sempre dá errado comigo" |
| Filtro mental | Perceber apenas o negativo | Focar em uma única crítica no feedback |
| Leitura mental | Achar que sabe o que os outros pensam | "Ele com certeza me odeia" |
| Catastrofização | Assumir o pior cenário | "Isso vai ser uma catástrofe" |
| Raciocínio emocional | Sentimento = realidade | "Eu me sinto burro, logo sou burro" |
| Pensamento de "deveria/tenho que" | Regras rígidas | "Eu deveria conseguir fazer isso" |
| Personalização | Relacionar tudo a si mesmo | "O trabalho ruim foi culpa minha" |

---

## 4. Questionar Pensamentos (Questionamento Socrático)

**Objetivo:** Não refutar os pensamentos diretamente, mas estimular o exame.

**Conjunto de perguntas:**

1. **Examinar as evidências:**
   - "Quais evidências existem a favor disso?"
   - "Quais evidências existem contra isso?"

2. **Explicações alternativas:**
   - "Existem outras explicações para isso?"
   - "Como outra pessoa veria esta situação?"

3. **Avaliar as consequências:**
   - "Qual é o pior que poderia acontecer? Quão provável é?"
   - "Qual é o melhor que poderia acontecer?"
   - "Qual é o mais realista?"

4. **Verificar a utilidade:**
   - "Este pensamento me ajuda a alcançar meus objetivos?"
   - "O que eu diria a um bom amigo que pensasse assim?"

---

## 5. Reestruturação Cognitiva Passo a Passo

### Formato de registro (registro de pensamentos)

```
SITUATION
Was ist passiert? (Wann? Wo? Wer war dabei?)
[Freitext]

GEDANKE
Was bin ich dadurch durch den Kopf gegangen?
Automatischer Gedanke: [...]
Glaube ich daran? (0-100%): [...]%

EMOTION
Welche Emotionen hatte ich?
Emotion: [...]    Intensität (0-100%): [...]%

DENKFEHLER
Welche kognitiven Verzerrungen stecken darin?
[Liste aus Tabelle oben]

PRÜFEN
Beweise dafür: [...]
Beweise dagegen: [...]
Alternative Sichtweise: [...]

ALTERNATIVER GEDANKE
Ausgewogener, realistischerer Gedanke:
[...]
Glaube ich daran? (0-100%): [...]%

ERGEBNIS
Emotion danach: [...]   Intensität: [...]%
Was nehme ich mit: [...]
```

---

## 6. Ativação Comportamental

**Complemento ao trabalho cognitivo:** Mudar o comportamento apoia a mudança de pensamentos.

**Princípio:** Atividades positivas -> Melhor humor -> Pensamentos mais úteis

**Passos:**
1. Criar uma lista de atividades agradáveis/significativas
2. Planejar as atividades (concretamente: quando, como, onde)
3. Acompanhar a execução
4. Avaliar o humor antes/depois

**Exemplos de atividades:**
- Caminhada (natureza, ar fresco)
- Contato com pessoas importantes
- Atividades criativas
- Movimento físico
- Coisas que antes davam prazer

---

## Ética e Limites

**Um assistente de IA pode:**
- Explicar distorções cognitivas e o modelo ABC
- Fazer perguntas socráticas
- Orientar registros de pensamentos
- Informar de forma psicoeducativa sobre técnicas de TCC

**Um assistente de IA NÃO pode:**
- Substituir a terapia cognitivo-comportamental profissional
- Fazer diagnósticos ou dar recomendações de tratamento
- Realizar intervenção em crise
- Aplicar EMDR, Exposição Prolongada (PE) ou Terapia de Exposição Narrativa (NET)

**Em caso de sinais de crise aguda, SEMPRE encaminhar para:**
- Telefonseelsorge (linha de apoio emocional na Alemanha): 0800 111 0 111 / 0800 111 0 222
- Serviço psiquiátrico de emergência: 112
- Krisenchat: krisenchat.de

---

## Referências

- Beck, A. T. (1979). *Cognitive Therapy and the Emotional Disorders.* Penguin Books.
- Ellis, A. (1962). *Reason and Emotion in Psychotherapy.* Lyle Stuart.

---

*Adaptado do BACH v3.8.0 | Versão standalone*
*Fontes: Beck (1979), Ellis (1962) — Não substitui terapia profissional*
