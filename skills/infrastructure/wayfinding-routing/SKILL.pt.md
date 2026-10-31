---
name: wayfinding-routing
version: 1.1.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-09-27
description: "Skill universal para navegação, orientação e tolerância a falhas de LLMs. Fornece wayfinding ativo, autoorientação e heurísticas de recuperação quando agentes enfrentam desvio de contexto, ferramentas com falha, loops ou becos sem saída. Inclui as estratégias sinônimas survival-routing, dead-reckoning, pathfinder-routing e celestial-routing."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [wayfinding, wayfinding-routing, survival-routing, dead-reckoning, pathfinder-routing, celestial-routing, self-orientation, resilience, recovery, heuristics]
language: pt
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
translated_from_sha256: 6baf14f778df95316188563ad6be21be8f223d9dd79ec73d7388514b77d45f01
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.501876+00:00"
---
<img src="banner.png" width="100%" alt="wayfinding-routing banner">

# Wayfinding-Routing (Motor de Autoorientação e Fallback de Emergência)

O skill **Wayfinding-Routing**, também conhecido como **`survival-routing`**,
**`dead-reckoning`**, **`pathfinder-routing`** e **`celestial-routing`**,
serve aos agentes LLM como uma estrutura vinculante para navegação e
recuperação de emergência.

Ele dota os agentes de heurísticas proativas de wayfinding para a execução
normal e de protocolos de emergência para desvio de contexto, falhas de
execução recorrentes, APIs indisponíveis ou becos sem saída.

---

## Visão Geral dos Sinônimos e Estratégias

| Estratégia sinônima | Metáfora e princípio central | Caso de uso |
| :--- | :--- | :--- |
| **`wayfinding-routing`** (primária) | **Wayfinding / orientação espacial:** navegação sem GPS externo, por meio de marcos e pistas do ambiente. | Ciclo primário de navegação para sidecars, `workflowhooker` e `automation-self-care`. |
| **`survival-routing`** | **Fallback de emergência e autopreservação:** circuit-breaking e degradação controlada quando ferramentas falham ou surgem loops. | Recuperação de emergência em caso de timeouts, erros repetidos ou limites de permissão. |
| **`dead-reckoning`** | **Navegação estimada náutica:** reconstruir o estado exato a partir de migalhas de pão incrementais, sem fonte externa de status. | Acompanhar os passos de execução em arquivos de scratch ou `TODO.md` para retroceder com precisão. |
| **`pathfinder-routing`** | **Batedor e comando avançado:** verificar e preparar caminhos antecipadamente para equipes multiagente. | Verificação prévia de árvores de diretórios, bloqueios e dependências de tarefas. |
| **`celestial-routing`** | **Navegação astronômica:** alinhar-se a documentos âncora imutáveis de "estrela polar" quando o contexto local está ruidoso. | Retorno a `CLAUDE.md`, `AGENTS.md` e `START.md` quando as instruções do prompt forem contraditórias. |
| **Estratégia `likelihood-routing`** (skill próprio, se instalado) | **Gradiente de probabilidade como sensor de quente/frio:** avaliar arquivos de controle pela probabilidade condicional de sequência (likelihood scoring) de um termo-alvo e seguir o gradiente ($\Delta S$). | Fallback sem serviço de memória, quando um termo técnico específico do projeto não aparece no histórico da sessão. |

---

## Os Cinco Protocolos Centrais de Emergência e Orientação

### 1. `PROTOCOL-ANCHOR-RESET` (Fallback de Estrela Polar / Celestial Routing)

- **Gatilhos:** desvio de contexto, instruções contraditórias do usuário ou
  perda de orientação em sessões longas com muitos turnos.
- **Regra heurística:** interromper a geração livre de texto. Descartar
  suposições transitórias. Reler os documentos âncora raiz (`CLAUDE.md`, `AGENTS.md`, `START.md`). Redefinir o
  estado-alvo para a instrução raiz de referência antes de qualquer nova ação.

### 2. `PROTOCOL-STOP-EXPLAIN` (Loop de Reflexão Rubber-Duck)

- **Gatilho:** um comando de terminal, uma alteração de arquivo ou uma
  requisição de API falha duas vezes com o mesmo erro.
- **Regra heurística:** **bloquear a execução de comandos.** Antes da terceira
  tentativa, o agente deve emitir uma autorreflexão formal:
  1. *Qual foi o erro exato nas tentativas 1 e 2?*
  2. *Por que a hipótese diagnóstica anterior falhou?*
  3. *Qual nova abordagem alternativa será escolhida?*
  A execução só é desbloqueada após essa justificativa explícita.

### 3. `PROTOCOL-GRACEFUL-DEGRADATION` (Cascata de Fallback em Múltiplos Níveis)

- **Gatilho:** a ferramenta primária, o servidor MCP ou a API externa está
  indisponível ou retorna erros.
- **Regra heurística:** nunca falhar abruptamente nem entrar em loop cego.
  Degradar gradualmente:
  - **Nível 1 (ótimo):** API nativa completa ou ferramenta MCP
  - **Nível 2 (ferramenta substituta):** CLI ou script Python local
  - **Nível 3 (estado somente leitura):** leitura direta de arquivos
    (`view_file` ou texto bruto)
  - **Nível 4 (transferência):** apresentar um relatório de status estruturado e
    as opções em aberto para o usuário.

### 4. `PROTOCOL-BREADCRUMB-BACKTRACK` (Dead Reckoning e Detecção de Becos sem Saída)

- **Gatilho:** um caminho complexo de refatoração ou fluxo de trabalho em várias
  etapas encontra um bloqueio insolúvel na etapa N.
- **Regra heurística:** antes de alterações destrutivas, registrar migalhas de
  pão. Se um caminho falhar:
  1. Reverter as alterações não confirmadas e restaurar o estado.
  2. Retroceder até o último checkpoint limpo de migalhas de pão.
  3. Marcar a rota com falha como bloqueada em `TODO.md`.
  4. Tentar o caminho alternativo B.

### 5. `PROTOCOL-CIRCUIT-BREAKER` (Parada de Emergência e Saída Segura)

- **Gatilho:** limite de execução atingido, loop infinito detectado ou erro
  crítico de bloqueio do sistema.
- **Regra heurística:** executar o desligamento de emergência:
  1. Liberar todos os bloqueios de arquivos e de git adquiridos pelo próprio
     agente (`python -m workflowhooker check`).
  2. Salvar o estado parcial atual em `.SYNC/SURVIVAL_STATE.json` ou
     `AUTOMATIONS-MEMORY.md`.
  3. Registrar o incidente em `ANTIGRAVITY-LOG.txt`.
  4. Encerrar de forma limpa com um resumo acionável para o usuário ou o
     orquestrador.

---

## Integração com `automation-self-care` e `workflowhooker`

`wayfinding-routing` fornece a lógica de navegação subjacente para:

- **`automation-self-care`**: verifica os prompts de sidecar quanto à capacidade
  de autocorreção, usando os cinco protocolos.
- **`workflowhooker`**: fornece heurísticas padrão para verificação
  incremental de bloqueios e registro de migalhas de pão.
- **`staircase-routing`**: usa `PROTOCOL-ANCHOR-RESET` para navegação vertical em
  diretórios.
- **Estratégia `likelihood-routing`** (skill próprio, se instalado): fornece o
  gradiente de probabilidade como sensor de quente/frio para
  `PROTOCOL-ANCHOR-RESET`, quando arquivos de controle apontam de forma ambígua para
  vários ramos plausíveis — complementar a `staircase-routing`, que busca
  correspondências de palavras-chave em vez de gradiente.

## Changelog

### 1.1.0 (2026-09-27)
- Estratégia `likelihood-routing` mencionada na tabela de visão geral e na
  seção de integração (sem link — o skill é apenas privado e ainda não faz
  parte deste repositório público; a questão de visibilidade cabe ao usuário).
