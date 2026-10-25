---
name: choose-your-orchestrator
version: 1.1.0
type: skill
author: Lukas Geiger + Codex
created: 2026-08-20
updated: 2026-10-03
description: "Escolhe, em conjunto com o usuário, uma orquestração adequada e limitada antes de trabalho complexo com múltiplos agentes, e gera um contrato de sessão compacto. Use a skill em /choose-your-orchestrator, quando a combinação de orquestrador, enxame, roteamento de modelos ou modelo de preferências do usuário não estiver clara, e antes de programas de agentes que precisem definir explicitamente slots de modelo, paralelismo, profundidade de spawn, limites de escrita, aceitação e escalonamento."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [orchestrierung, multi-agent, delegation, routing, budget, matruschka, session-vertrag]
aliases: [choose-your-orchestrator]
language: pt
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [orchestrator, swarm-operations, model-strategy, decision-avatar, budgetierung]
  python: []

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: github.com/ellmos-ai/skills
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 0b3feaa40d5c9d5310977fbc0e9c92572c1504e201baad19e7b73c7b64e4e846
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.615044+00:00"
---
<img src="banner.png" width="100%" alt="choose-your-orchestrator banner">

# Escolha Seu Orquestrador

## Finalidade

Esclareça, antes de trabalho complexo com múltiplos agentes, as condições de contorno, recomende a menor combinação eficaz de skills existentes e emita um contrato vinculante de orquestração da sessão. Carregue as skills selecionadas pelo mecanismo de skills do runtime atual e siga suas instruções ao vivo. Não copie seus procedimentos para esta skill.

Delegação nunca amplia a autoridade. Ações externas ou irreversíveis, como publicar, enviar, excluir, pagar ou fazer alterações em produção, permanecem sujeitas à aprovação do usuário, a menos que a tarefa atual as autorize explicitamente.

## Componentes

| Componente | Função no contrato | Não é sua função |
|---|---|---|
| `orchestrator` | Pacotes de trabalho, escopos, evidências e aceitação | Inventar escolha de modelo ou padrão de enxame |
| `swarm-operations` | Padrão de enxame, portão de custo e escalonamento Matruschka opcional | Paralelizar artificialmente tarefas individuais |
| `model-strategy` | Rota por capacidade e modelo, conforme a disponibilidade ao vivo | Prescrever versões fixas de modelos ou permissões |
| `clutch` | Sugestão externa opcional de roteamento | Autoridade única para despacho ou escopo |
| `decision-avatar` | Sinal opcional de preferência autorizado para incertezas reversíveis | Substituir aprovações do usuário ou ampliar a autoridade |
| `budgetierung` | Cotas negociadas por janela de tempo para modelos/revisores/consultores caros, conta e verificações prévias antes de escalonamentos | Escolher modelos por mérito técnico (isso cabe a `model-strategy`) ou definir cotas por conta própria |

Use `clutch route "<kurze Aufgabenbeschreibung>" --json` somente se `clutch` estiver de fato disponível. Trate a resposta JSON como sugestão e confirme-a contra os slots de runtime disponíveis, o orçamento, as regras do projeto e os limites do usuário. Se `clutch` não estiver disponível ou sua saída for ilegível, use `model-strategy` e as capacidades ao vivo do runtime. Não codifique nomes ou versões atuais de modelos no contrato.

## Diálogo de Recomendação

### 1. Classificar a tarefa

Identifique objetivo, tipo de tarefa, critérios de sucesso, escopos negativos, permissões atuais, bloqueios existentes e pacotes de trabalho independentes. Escolha primeiro a menor rota adequada da tabela abaixo.

### 2. Propor o contrato

Apresente um rascunho compacto com:

1. componentes e funções,
2. slots de modelo/orçamento (para execuções de várias horas ou modelos escassos/caros, negocie via `budgetierung` e mantenha o registro da conta),
3. paralelismo máximo e profundidade de spawn,
4. limites de escrita e bloqueios,
5. aceitação e evidências,
6. escalonamento e perguntas ao usuário,
7. limite de autoridade.

Recomende valores concretos e cite em uma frase o principal trade-off. Pergunte apenas sobre decisões que alterem materialmente o resultado. Agrupe perguntas abertas em no máximo três grupos claramente separados; apresente sempre a opção recomendada em primeiro lugar. Se todas as dimensões já estiverem explicitamente definidas, não pergunte novamente.

### 3. Confirmar ou reduzir

Não inicie despacho com múltiplos agentes enquanto houver uma questão material aberta sobre orçamento, escrita ou autoridade. Se apenas o benefício do paralelismo estiver incerto, reduza para execução individual. Uma tarefa explicitamente autorizada pode começar com os padrões seguros quando não faltar nenhuma decisão material do usuário.

### 4. Emitir o contrato

Apresente o contrato confirmado no chat. Se um comando `usmc` estiver disponível, verifique primeiro sua ajuda e, além disso, grave uma nota de sessão neutra quanto à privacidade por meio de um comando de nota/escrita documentado ali. Não invente subcomandos e não armazene prompts brutos, segredos ou conteúdo privado. Sem um caminho de escrita USMC disponível, o contrato no chat é autoritativo.

## Tabela de Roteamento

| Tipo de tarefa | Recomendação | Recorte padrão |
|---|---|---|
| Auditoria / varredura | `orchestrator` + `swarm-operations`; `model-strategy` para classes de capacidade diferentes | áreas independentes, pequeno grupo `parallel-chunks` ou `specialist`, consolidação central |
| Programa de construção | `orchestrator` + `model-strategy`; enxame apenas para fluxos realmente independentes | o chefe planeja e aceita, os workers constroem em áreas disjuntas |
| Construção individual | Execução individual; opcionalmente `model-strategy` ou `clutch` para a rota | sem sobrecarga de enxame ou hierarquia |
| Operação por tickets | O sistema de tickets permanece à frente; `orchestrator` complementa contratos de trabalho e evidências | não substituir o regime existente de roteador/pontuação; respeitar o ciclo de vida do ticket |

## Padrões Seguros

Use estes valores, salvo se o usuário, o runtime ou as regras do projeto exigirem algo mais rigoroso:

- no máximo dois workers ativos; comece com um e comprove o benefício do segundo,
- Matruschka desligado, profundidade máxima de spawn `0`,
- nenhum subagente próprio de worker sem autorização explícita,
- um único escritor por repositório ou área claramente delimitada,
- claims de arquivos disjuntos e bloqueios usuais do projeto antes de qualquer escrita,
- o chefe/orquestrador verifica pessoalmente artefatos, diffs e testes,
- mensagens de conclusão só valem após aceitação por evidências,
- ações irreversíveis ou externas permanecem sujeitas à aprovação do usuário,
- incertezas são agrupadas em vez de reportadas como muitas interrupções isoladas.

Ative o Matruschka somente se o usuário o confirmar explicitamente e o contrato indicar, por nível, a classe de modelo/capacidade, o limite de slots ativos, as subtarefas permitidas e a profundidade máxima. Conte agentes ativos, não apenas agentes existentes. Mesmo assim, deve permanecer exatamente um escritor por área.

## Formato do Contrato

```text
SESSION-ORCHESTRIERUNGSVERTRAG
Ziel und Typ: <Ergebnis; Audit/Bauprogramm/Einzelbau/Ticket-Betrieb>
Bausteine: <geladene Skills und optionale Router>
Chef: <Planung, Denkarbeit, Integration, Evidenzabnahme>
Worker-Slots: <Rolle/Fähigkeitsklasse je Slot; Budgetgrenze; Budget/Konto: <budgetierung-Konto, Pfad>>
Parallelität: <maximal aktiv>; Spawn-Tiefe: <0..N>; Matruschka: <aus/an>
Schreibgrenzen: <ein Schreiber je Bereich; Claims; Locks; negative Scopes>
Abnahme: <Artefakte, Tests, Diffs, Quellen; wer prüft>
Eskalation: <Stopps; höchstens drei gebündelte Nutzerfragen>
Autorität: <zulässige Aktionen; extern/irreversibel user-gegatet>
Persistenz: <Chat autoritativ; USMC-Notiz ja/nein und privacy-neutral>
```

## Exemplo

```text
Auftrag: Drei unabhängige Komponenten prüfen und einen Fix integrieren.
Empfehlung: orchestrator + swarm-operations; zwei aktive Read-only-Reviewer,
danach genau ein Integrationsschreiber. Matruschka aus, Tiefe 0. Der Chef prüft
Fundstellen, Diff und Gesamttests. Push oder Veröffentlichung nur im ausdrücklich
autorisierten Scope.
Offene Frage: Ist die zweite parallele Review-Spur den zusätzlichen Verbrauch wert?
Empfehlung: ja, weil die Komponenten unabhängig sind.
```

## Condições de Parada

Pare ou reduza a orquestração quando os escopos se sobrepuserem, os bloqueios estiverem pouco claros, o runtime não oferecer o slot recomendado, o orçamento não estiver confirmado ou a aceitação não puder ser comprovada de forma independente. Pergunte ao usuário em vez de adivinhar uma nova decisão de produto, privacidade ou autoridade.

## Registro de Alterações

### 1.1.0 (2026-10-03)
- `budgetierung` adicionado como componente para cotas de modelo negociadas/conta (tabela de componentes, slots de modelo/orçamento no diálogo de contrato, linha de slots de worker no formato do contrato).

### 1.0.0 (2026-08-20)
- Diálogo de recomendação, tabela de rotas e contrato de sessão compacto introduzidos.
- Padrões seguros definidos para paralelismo, Matruschka, limites de escrita, evidências e ações externas.
- Descrita a integração opcional de `clutch` e de um modelo de preferências autorizado, sem vínculo fixo com modelos nem ampliação de autoridade.
