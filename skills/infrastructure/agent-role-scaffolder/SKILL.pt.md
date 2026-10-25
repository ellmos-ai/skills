---
name: agent-role-scaffolder
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-25
updated: 2026-08-25
description: "Cria e verifica novas funções de agentes no ecossistema ellmos: subagentes nativos do Claude Code (definição de função persistente) e workers companheiros (instância reutilizada via SendMessage para uma série de tickets/tarefas). Formaliza o conhecimento até agora não formalizado sobre a construção de funções de agentes em curso (ati-agent, bueroassistent, versicherungs-agent e outros) em um procedimento reutilizável de scaffold e verificação. Use esta skill quando uma nova função deve surgir (\"criar nova função de agente\", \"criar subagente\", \"iniciar worker companheiro\") ou quando um agente existente deve ser verificado segundo as convenções da casa (\"este agente está configurado corretamente?\")."
visibility: public
language: pt
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
translated_from_sha256: 55b76ad25a5d65f61987662e674bc9c74ea0f6a8586ad4748268bc9441711db5
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.079853+00:00"
---
<img src="banner.png" width="100%" alt="agent-role-scaffolder banner">

# agent-role-scaffolder

<!-- FAMILY-ROUTER:Agenten-Orchestrierung START -->
> **Família de orquestração de agentes — guia:** escolher/escalonar modelo ->
> `model-strategy`; escolher padrão de orquestração -> `choose-your-orchestrator`;
> operações de enxame (5 padrões básicos + 2 modos) -> `swarm-operations`; decompor/delegar/
> receber tarefa -> `orchestrator`; mensagens entre provedores/presença/locks -> `agents-bridge`;
> **criar ou verificar uma nova função -> esta skill (agent-role-scaffolder)**.
<!-- FAMILY-ROUTER:Agenten-Orchestrierung END -->

## Finalidade

Este ecossistema já possui uma família madura de skills de orquestração
(`model-strategy`, `swarm-operations`, `orchestrator`, `choose-your-orchestrator`,
`agents-bridge`) — mas **nenhuma delas trata da pergunta "como criar uma nova função
corretamente".** Essa lacuna é preenchida por `agent-role-scaffolder`. Ele não duplica
as skills citadas, mas **direciona para elas** sempre que for necessário escalonamento,
padrão de orquestração ou mensagens entre provedores.

**Origem:** decisão do usuário M5 do ticket `T-20260825-935905816`
(varredura completa do marketplace): veredito (b) — o conhecimento próprio sobre construção de agentes
existia, mas não estava formalizado. O plugin oficial do Claude Code
`agent-sdk-dev` (claude-plugins-official, Apache-2.0) serviu como
**modelo estrutural**: um arquivo de comando de scaffolding mais dois subagentes verificadores
temáticos com checklist e um formato de relatório PASS/PASS-WITH-WARNINGS/FAIL.
Foi adotada a **forma** (catálogo de perguntas de scaffold → montagem → checklist de
verificação com relatório estruturado), não o texto nem o objeto — aquele plugin constrói
apps brutos do Claude Agent SDK (Python/TypeScript), esta skill constrói
**funções de agentes próprias do ellmos** (definições de subagentes e workers companheiros).
O original NÃO está instalado; ele fica somente leitura no cache local do marketplace e foi
apenas lido (`.PLUGINS/CLAUDE.md` regra 5: ideias livres, formulações não). Entrada de registro:
`.AI/.PLUGINS/PLUGIN-REGISTER.md`, status `zitiert`.

## Dois caminhos de construção — ambos pertencem aqui

No ecossistema ellmos, novas funções surgem por dois caminhos estruturalmente diferentes,
que não devem ser confundidos (análogo à separação TS/Python do plugin modelo — aqui, porém,
ao longo da fronteira real do sistema):

| | **Subagente nativo** | **Worker companheiro** |
|---|---|---|
| O que surge | uma definição de função persistente (`~/.claude/agents/<name>.md`, iniciável pela ferramenta `Agent`) | uma instância nomeada ad hoc, reutilizada via `SendMessage` para UMA série de tarefas |
| Tempo de vida | persistente, reutilizável entre sessões | pela duração de uma série de tickets/temas, depois descartada |
| Exemplos no acervo | `ati-agent`, `bueroassistent`, `versicherungs-agent`, `gesundheitsassistent`, `persoenlicher-assistent`, `production`, `research-agent`, `reflection-agent`, `test-agent`, `entwickler-agent` | este próprio modelo de sessão (p. ex. `skillcreator-bau`, `policyreg-decisions`, `workflowhooker-ausbau` — workers nomeados no sistema de tickets) |
| Camada de ciclo de vida | registro de agentes próprio do Claude Code | **COMA** (`.MODULES/.ORCHESTRATION/coma`) — quando iniciado entre processos, não apenas dentro da ferramenta |
| Guia de construção aqui | `references/subagent-role-scaffold.md` | `references/companion-worker-scaffold.md` |

**Regra prática:** se a capacidade precisa de um nome próprio, reutilizável por muitas sessões,
com descrição fixa de gatilho (p. ex. "sempre que houver questões sobre comprovantes fiscais") → subagente nativo.
Se é uma série limitada, mas coesa, de tarefas que um coordenador delega no momento (cadeia de tickets,
mudança de tema) → worker companheiro.

## Procedimento

1. **Escolher o caminho de construção** (tabela acima) — em caso de dúvida, perguntar ao usuário, não supor.
2. **Percorrer as perguntas de scaffold** (ver `references/*.md` correspondente) — análogo
   ao plugin modelo, uma a uma, não todas de uma vez: finalidade/gatilho,
   necessidade de ferramentas (`Tools:`), escolha do modelo (→ **passo 3**), necessidade de coordenação
   (agente chefe com especialistas ou função única?).
3. **Não decidir a escolha do modelo aqui — delegar a `model-strategy`.**
   Seleção baseada em pontuação, delegação entre agentes, pareamento de consultor e gatilhos de escalonamento
   já estão resolvidos ali; aqui há apenas a referência. Regra prática do acervo: subagentes **não herdam
   automaticamente** o modelo principal (ver memória de feedback `feedback_subagenten_modellstaffelung`).
4. **Verificar o padrão de orquestração**, se a nova função deve colaborar com outras — `choose-your-orchestrator` escolhe
   o padrão, `swarm-operations` fornece os 5 padrões básicos + 2 modos, `orchestrator` o protocolo de
   decompor/delegar/receber.
5. **Respeitar as convenções de equipe/mensagens** (`references/
   model-staffing-and-messaging.md`): `SendMessage` para comunicação entre agentes,
   reivindicação de ticket por nome de arquivo na delegação de tickets, "referenciar em vez de repetir" ao
   atribuir tarefas (não recontar regras centrais no prompt, apenas o que é específico da tarefa).
6. **Verificar** — executar o checklist correspondente no arquivo `references/*.md` escolhido e
   gerar o relatório no formato `PASS / PASS MIT WARNUNGEN / FAIL` (estrutura abaixo).
7. **Catalogar se necessário** — uma nova função permanente pertence ao registro adequado
   (`~/.claude/agents/`, eventualmente agrupamento em plugin); um worker companheiro não precisa de entrada no
   registro, apenas de uma passagem inicial de tarefa clara.

## Formato do relatório de verificação (para ambos os caminhos)

Estrutura deliberadamente herdada do plugin modelo (forma, não texto) — quatro
seções, concisas:

- **Status:** PASS | PASS COM AVISOS | FAIL
- **Pontos críticos:** o que torna a função inutilizável (descrição de gatilho ausente,
  `Tools:` amplo ou restrito demais, modelo sem justificativa por `model-strategy`, nenhuma
  delimitação em relação a uma função existente verificada)
- **Avisos:** subótimo, mas funcional (p. ex. modelo principal herdado em vez de escalonado,
  nenhum critério de rotação para um worker companheiro de longa duração)
- **Verificações aprovadas + recomendações:** o que está correto e o que vem a seguir

## Skills relacionadas

- `model-strategy` — escolha/escalonamento de modelo (passo 3, aqui apenas referenciado).
- `swarm-operations` — padrões de enxame para colaboração entre várias funções.
- `choose-your-orchestrator` — escolhe o padrão de orquestração adequado.
- `orchestrator` — protocolo para decompor/delegar/receber.
- `agents-bridge` — mensagens entre provedores/presença/locks, caso a nova função precise
  comunicar-se com Codex/Gemini/Kimi além do Claude Code.
- `skill-explorer` — verifica se uma capacidade já existe ANTES de construir uma nova função
  (evitar duplicação).

## Histórico de alterações

### 1.0.0 (2026-08-25)
- Versão inicial. Construída segundo a decisão do usuário M5 (`T-20260825-935905816`) via
  `ellmos-skill-creator`. Formaliza o padrão de worker companheiro (fonte primária:
  `_control-center/_TICKETS/README.md`, seção "Princípio orientador
  (economia de contexto)"), o ciclo de vida COMA (fonte primária:
  `.MODULES/.ORCHESTRATION/coma/README.md`) e o padrão observado "agente chefe coordena especialistas"
  de funções existentes. Direciona deliberadamente para `model-strategy`/`swarm-operations`/`orchestrator`/
  `choose-your-orchestrator`/`agents-bridge` em vez de duplicá-los.
  Modelo `agent-sdk-dev` (claude-plugins-official) NÃO instalado, apenas lido e citado
  estruturalmente (`.PLUGINS/CLAUDE.md` regra 5).
