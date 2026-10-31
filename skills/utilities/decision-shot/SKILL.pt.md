---
name: decision-shot
version: 1.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-24
updated: 2026-09-18
description: "Formato de saída extremamente curto e substancial para UMA decisão ou um grupo de decisões, quando a análise subjacente já existe (criada no chat, a partir de `decide`, a partir de `decision-briefing`, de um ticket ou documento): contexto em 2-3 linhas, prós/contras por opção como tópicos no estilo reduzido paveman/caveman, pontos de conversa, uma recomendação fundamentada e um caminho/link para a análise completa para leitura integral. Use esta skill com \"me dê isso resumido com prós, contras e recomendação\", \"resumo executivo da decisão\", \"contexto curto sobre <Thema>\", \"resuma a decisão X em forma curta\", /decision-shot, ou quando um resultado precisar ser repassado a alguém que só precisa da essência, não da derivação completa. NÃO use para COLETAR várias decisões em aberto e consultá-las por letra — isso é feito por decision-briefing; NÃO use para ANALISAR uma decisão primeiro — isso é feito por decide. decision-shot pressupõe uma análise pronta e apenas comprime a sua apresentação."
visibility: public
language: pt
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: utilities
tags: [entscheidung, executive-summary, kurzform, pro-contra, talking-points, empfehlung]
status: active

dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, knappform, paveman]

provenance:
  origin: "custom"
  decision_ref: "T-20260824-673115956 (Ticket-Master, User-Auftrag 2026-08-24)"
translated_from_sha256: 26ff135e844d526543d9f5df212d36e408a427a71cc13a9e744a55abdb5ed991
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.477287+00:00"
---
<img src="banner.png" width="100%" alt="decision-shot banner">

# decision-shot

> A análise está feita. O que agora é necessário não é uma segunda derivação,
> mas a essência mais o caminho de volta para o conteúdo completo.

## Quando usar

- Uma decisão (ou um grupo estreitamente relacionado, p. ex. várias subperguntas
  do mesmo tema) já foi pensada — no chat, em um ticket, por meio do framework
  `decide` ou na fase 2 do `decision-briefing` — e precisa agora ser
  disponibilizada em segundos a alguém (ao usuário, a outro agente, a um
  documento de passagem).
- Palavras-gatilho: "resumido com prós e contras", "resumo executivo",
  "contexto curto", "pontos de conversa sobre isso", "me dê isso comprimido com
  recomendação", `/decision-shot`.
- **Não** para várias questões ainda em aberto e não decididas, que o usuário
  deve responder em sequência/em lote por letra — isso é o
  [decision-briefing](../decision-briefing/SKILL.md). **Não** para elaborar uma decisão
  primeiro — isso é o [decide](../decide/SKILL.md). decision-shot é apenas a
  APRESENTAÇÃO de uma análise já existente.

## Delimitação (versão resumida)

| Skill | Faz o quê | Quando está pronta |
|---|---|---|
| `decide` | Elabora UMA decisão com um framework (matriz prós/contras, pontuação ponderada, árvore de decisão, ...) | A análise ainda está pendente |
| `decision-briefing` | Coleta VÁRIAS decisões em aberto de um tema, apresenta-as como lote A/B/C/D e recebe respostas por letra | Vários pontos ainda não foram decididos |
| `decision-shot` | Condensa UMA análise pronta (seja de onde for) em uma forma executiva curta com link para a versão completa | A análise já existe, falta apenas a apresentação |
| `knappform` | Modificador geral do estilo de resposta para TODA resposta da sessão | Em toda a sessão, independentemente do tema |
| `paveman` | Encurta ARQUIVOS DE PROSA existentes (arquivos de regras/memória) de forma determinística | Encurta um arquivo, não a saída do chat |

`decision-shot` não concorre com nenhuma das quatro — é o FORMATO que entra
depois do `decide` ou ao lado do `decision-briefing`, assim que a essência
precisar ser repassada. O estilo de linguagem reduzido segue o `knappform`/`paveman`
(ver lá a lista completa de supressões), mas aqui é aplicado de forma consistente
em um formato fixo de cinco partes.

## Formato (obrigatório, cinco partes)

```
## <Entscheidungstitel>

**Kontext:** <2-3 Zeilen -- worum es geht, warum jetzt, was auf dem Spiel steht>

**<Option A>**
+ <staerkstes Pro-Argument>
+ <zweites Pro-Argument, nur falls es traegt>
- <staerkstes Contra-Argument>

**<Option B>**
+ <Pro>
- <Contra>
- <Contra>

**Talking Points:**
- <Punkt, der im Gespraech/in einer Mail sofort zieht>
- <Punkt, der einen typischen Einwand vorwegnimmt>

**Empfehlung:** <Option> -- <ein Satz Begruendung, keine Wiederholung der Pro-Liste>

**Vollanalyse:** <Pfad oder Link -- Ticket-Datei, Dokument, Chat-Referenz>
```

## Regras

- **Textos para o usuário sem números/siglas técnicos (forma em primeira pessoa, linguagem cotidiana):**
  No texto visível para a pessoa (título, contexto, opções, pontos de conversa, recomendação) **não** aparecem siglas internas, números de ticket (`T-...`), identificadores D ou caminhos relativos de arquivo.
  O contexto descreve a situação e a ação planejada em primeira pessoa („Eu proponho...“).
  Referências técnicas (ID do ticket, caminho exato do arquivo) aparecem exclusivamente na linha final `**Vollanalyse:**` ou em uma tabela de referências.
- **As linhas são um orçamento, não uma meta.** 2-3 linhas de contexto, 2-4 tópicos por opção,
  2-3 pontos de conversa, 1 frase de recomendação — o excedente é cortado, não
  encurtado-e-mantido. Se uma opção não cabe em 4 tópicos, ela não pertence a
  esta skill, e sim à análise completa.
- **Estilo reduzido como no `knappform`/`paveman`:** sem palavras de preenchimento, sem
  fórmulas vazias, sem evasivas. Negações (`nicht`, `nie`, `kein`, `nur`,
  `außer`) permanecem intactas — suprimi-las inverte a afirmação.
- **Prós/contras são tópicos, não frases.** `+`/`-` como prefixo, um
  pensamento por linha, sem oração complementar.
- **Pontos de conversa são comunicativos, não analíticos.** Eles respondem a
  "o que eu digo se alguém me perguntar" — não a "o que está na análise".
  Duplicatas da lista de prós/contras indicam que ainda não houve condensação.
- **A recomendação se justifica em uma frase.** Sem repetir a lista de prós,
  sem "ver acima" — a frase precisa se sustentar mesmo sem o restante do bloco.
- **O link/caminho para a análise completa é obrigatório, não opcional.** O
  decision-shot não substitui a análise, ele a torna rapidamente localizável.
  Se não houver fonte tangível (surgido apenas oralmente no chat, sem
  documento), indique a referência ao chat/sessão da forma mais concreta
  possível (p. ex. "esta sessão, resposta sobre F4") em vez de deixar o campo
  vazio.
- **Várias decisões relacionadas** (grupo, p. ex. várias subperguntas de um
  tema): um bloco por decisão, separados por `---`; contexto comum apenas
  uma vez no início, somente se realmente valer para todas.

### Carimbo de proveniência da sessão em decision-shots salvos

Quando o decision-shot for salvo como artefato novo, importante e duradouro, o arquivo termina com:

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

O ID da sessão vem primeiro de uma indicação explícita de runtime/CLI, depois de um
ambiente autoritativo do provedor ou de um hook; se ambos faltarem, usa-se `unbekannt`. Nunca
adivinhe valores. Subagentes usam a sessão-mãe. Chat de rotina, fontes, políticas, `CLAUDE.md`,
READMEs e arquivos antigos não recebem carimbo genérico nem carimbo retroativo.

## Exemplo

```
## Wo laeuft der naechtliche Backup-Job?

**Kontext:** Ich beobachte wiederholte Ausfälle auf dem Laptop, weil das Gerät nachts
schläft. Ich schlage vor, den Job auf den Mac Studio umzuziehen, der rund um die Uhr läuft.

**Laptop (Status quo)**
+ Keine Netzwerkabhaengigkeit
- Job faellt regelmaessig aus, wenn das Geraet schlaeft
- Kein zentraler Log-Ueberblick

**Mac Studio**
+ Laeuft 24/7, keine Ausfaelle durch Schlafmodus
+ Zentrale Logs an einem Ort
- Braucht funktionierendes Tailscale/SSH als Voraussetzung

**Talking Points:**
- "Der Ausfall ist kein Bug im Skript, sondern eine Standortfrage."
- "Tailscale laeuft schon fuer andere Jobs stabil -- kein neues Risiko."

**Empfehlung:** Mac Studio -- einzige Option ohne den bekannten Schlafmodus-
Ausfall, und die Abhaengigkeit (Tailscale) ist bereits im Betrieb bewaehrt.

**Vollanalyse:** `.SYNC/MAC_STUDIO_COMPUTE_HANDOFF.md`, Abschnitt "Backup-Jobs" (Ticket T-20260620-42)
```

## Changelog

### 1.2.0 (2026-09-18)
- Regra de estilo para textos de decisão compreensíveis incorporada (T-20260913-883789445, instrução do usuário de 2026-09-13):
  - Sem números de ticket, identificadores D ou caminhos internos no texto visível (título, contexto, pontos de conversa).
  - Contexto e recomendação em linguagem cotidiana natural, em primeira pessoa.
  - Referências técnicas de ticket e caminho estritamente limitadas à linha final da análise completa.

### 1.1.0 (2026-09-09)
- P-018 acrescenta o carimbo de sessão para decision-shots novos e importantes salvos, com
  prioridade de fonte restrita e exclusões.

### 1.0.0 (2026-08-24)
- Versão inicial.
