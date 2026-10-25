---
name: skill-finder
version: 0.9.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-10-03
description: "Localizador/roteador ativo para as suas próprias skills locais (análogo a using-superpowers). Usar SEMPRE no início de uma tarefa não trivial, para verificar se alguma skill de user se aplica e encaminhar para a skill correta. Ativa-se com \"qual skill se aplica\", \"existe uma skill para isso\", \"encontrar skill\", ou em geral antes de tarefas que uma skill local resolve melhor do que trabalho ad hoc."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, finder, routing, discovery, meta]
language: pt
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-finder/"
  origin_version: "0.1.0"
translated_from_sha256: 999cd705d5357d1c4244d420001f12dea37a1b2a9a204c49a7eadf18767228f7
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T12:49:10.031276+00:00"
---
<img src="banner.png" width="100%" alt="skill-finder banner">
# Skill-Finder

## A Regra

Antes de qualquer tarefa não trivial, verificar primeiro se uma skill local a resolve melhor. Mesmo com
pouca suspeita, carregar a skill adequada e **seguir a sua instrução ao vivo** (ler o ficheiro, não
trabalhar de memória). Se nenhuma skill se aplicar, continuar normalmente.

## Encaminhamento por Famílias

<!-- Generiert/aktualisiert aus SKILL-MAP.md + inventory_skills.py. Thema -> Familie -> Skill.
     Pflege: Subskill skill-family-care oder neuer skill-explorer-Audit-Lauf. Stand: 2026-06-17 -->

| Tema / Intenção | Família | Skill(s) |
|-----------------|---------|----------|
| Pensar / analisar um problema | Ferramentas de pensamento | `/structured-thinking` (executa `/think` → `/brainstorm` → `/decide`) |
| novas ideias / criatividade | Ferramentas de pensamento | `/brainstorm` (vs `/think` análise, `/decide` seleção) |
| Pilha de decisões | Ferramentas de pensamento | `/decision-briefing` |
| Qual decisão depende de qual / as recomendações entram em conflito? | Ferramentas de pensamento | `decision-path` (`/decision-path`; grafo de dependências em ASCII, não decide nada) |
| Obter a validação de uma variante global recomendada como UM texto de conceito/implementação | Ferramentas de pensamento | `decision-draw` (`/decision-draw`; aceitação como um todo, correções → decisões individuais) |
| Construir ou usar um perfil de utilizador autorizado | Multi-Agente | `build-your-users-mind` (construção) · `decision-avatar` (utilização) |
| Bug / falha de teste | Codificação e depuração | `/bugfix-protocol` (1 bug), `/bugsweep` (vários, antes de release) |
| projeto ou pipeline novo/existente | Projeto/Pipeline | `/projekt-pipeline-umbrella` (→ bootstrapper/onboarding/optimizer) |
| Jogo Roblox | Desenvolvimento de jogos | `/rbx-dev` (→ `/rojo`, `/rbx-studio`, `/game-design`) |
| Terapia / aconselhamento / crise | Terapia | `/therapie-umbrella` (→ stabilization/guideline/counseling) |
| Apresentação / slides | Office | `/academic-pptx` (conteúdo) + `/pptx` (ficheiro) |
| Limitar em conjunto a orquestração antes de um trabalho multi-agente complexo | Multi-Agente | `choose-your-orchestrator` (`/choose-your-orchestrator`) |
| Executar coordenação multi-agente confirmada | Multi-Agente | `orchestrator`, `/swarm-operations`, `/model-strategy` |
| Candidatura / autogestão | Pessoal | `/bewerbungsexperte`, `/selbstmanagement` |
| Comparar/limpar/encontrar skills | Sistema/Meta | `skill-explorer` (auditoria/exploração), `code-skill-index` (lista) |
| Configurar o sistema / sincronizar MCP / ligar agentes | Sistema/Meta | `/system-onboarding`, `/mcp-config-sync`, `/agents-bridge` |
| Ferramentas de ficheiros | Utilitários | `/document-chunker`, `/migrate-rename`, `/plugin-system` |
| Conservar o histórico de chat como skill | Sistema/Meta | `skill-extractor` (`/skill-extract`) |
| Histórico de chat/automação de terceiros → automatização | Sistema/Meta | `workflow-extract` (`/automations-extract`) |
| verificação recorrente em muitos projetos | Codificação e depuração | `rotation-check` (estrutura de registo/log) |
| problema bloqueado, extrair ideias | Ferramentas de pensamento | `idea-mining` (vs `/brainstorm` = livre/amplo) |
| Manter sincronizadas as versões DE/EN dos documentos | Utilitários | `bilingual-doc-sync` |
| merge muito conflituoso / ramos divergentes (main vs. master) / PR antigo | Codificação e depuração | `reissverschluss-merge` (`/reissverschluss-merge` · `/zipper-merge`; escalonamento: reconstruir em vez de fazer merge) |
| Vestígios de IA/restos de chat em textos, divulgação de IA | Utilitários | `llm-text-hygiene` |
| Condição/momento/ordem na instrução ("só quando", "a partir das 6h", "assim que X terminar") | Processo | `condition` (`/if` · `/when` · `/if-only` · `/after` · `/and` · `/or`) |
| Recolher/ordenar ficheiros de uma pasta por regras ("recolhe sempre Y de X e junta-os em Z", "ordena a pasta automaticamente") | Utilitários | `file-collect-sort-action` |
| Testar em conjunto com o utilizador uma série de apps/GUI (testar ao vivo, avaliar o feedback de imediato + delegar a reparação) | Codificação e depuração | `human-loop-audit` |
| Limpar o projeto após o fim da sessão (resolver/arrumar registos, pôr a documentação no estado atual, retirar restos) | Codificação e depuração | `tidy-up` (`/tidy-up`; conta como fonte de nível 1 de `work-autonomous`) |
| Encurtar ficheiro de regras/memória sem alterar o conteúdo ("CLAUDE.md é demasiado longo", "está a ser truncado") | Utilitários | `paveman` (determinístico, sem chamada de modelo; vs. `knappform` = estilo de fala de LLM) |
| Diagrama Mermaid não renderiza no GitHub ("Unable to render rich display", "o esquema não aparece"), verificar blocos Mermaid em toda a organização | Codificação e depuração | `mermaid-lint` (analisador real sem navegador + releitura na página ativa) |
| Orçamento de modelos, quotas, reviewers/advisors caros usados com limite | Multi-Agente | `budgetierung` (conta + negociação; escolha do modelo em si: `/model-strategy`) |

Lista completa: skill `code-skill-index`.

## Red Flags (racionalizações que significam STOP)

| Pensamento | Realidade |
|------------|-----------|
| "É só uma pergunta rápida." | Perguntas são tarefas — verificar skills primeiro. |
| "Conheço o conceito." | Conhecer o conceito ≠ usar a skill. Ler o ficheiro ao vivo. |
| "A skill é exagero." | O simples torna-se complexo — usar. |
| "Vou explorar primeiro sozinho." | As skills dizem COMO explorar. Verificar primeiro. |

## Manutenção

Atualizar a tabela de encaminhamento quando uma família mudar (subskill `skill-family-care` ou nova
execução `inventory_skills.py` a partir de `skill-explorer`).

## Changelog

### 0.9.0 (2026-10-03)
- Linha de encaminhamento para a nova skill `budgetierung` (família Multi-Agente): negociar, conduzir e ajustar
  quotas de modelos — contabilidade de contas complementar a `model-strategy`
  (aí se define *qual* modelo serve; `budgetierung` regula *quanto* dele).

### 0.8.0 (2026-09-20)
- Linha de encaminhamento para a nova skill `mermaid-lint` (família Codificação e depuração):
  diagramas Mermaid que o GitHub recusa com "Unable to render rich display", bem como
  execuções de verificação em toda a organização sobre todos os blocos ```mermaid.

### 0.7.0 (2026-08-20)
- `choose-your-orchestrator` acrescentado como diálogo prévio de recomendação e contrato para
  trabalho multi-agente complexo; o encaminhamento de execução para `orchestrator`,
  `swarm-operations` e `model-strategy` fica separado disso.

### 0.6.0 (2026-08-19)
- Linha de encaminhamento para a nova skill paveman ("encurtar ficheiro de regras/memória sem alterar o
  conteúdo"): invólucro fino em torno do módulo determinístico de encurtamento já instalado
  `paveman` (T-20260819-213392123); delimitação em relação a `knappform` (estilo de fala de LLM em vez de edição de ficheiro).

### 0.5.0 (2026-08-19)
- Linha de encaminhamento para a nova skill tidy-up ("limpar o projeto após o fim da sessão": uma única
  passagem de Tasksolver+Writer+Maintainer para a pasta do projeto ativo; conta como
  fonte de nível 1 `work-autonomous` para construções de `/goal`).

### 0.4.0 (2026-08-18)
- Linha de encaminhamento para a nova skill human-loop-audit ("testar em conjunto com o utilizador uma série de
  apps/GUI", auditoria de fecho éclair com delegação paralela de reparação; separada do
  homónimo reissverschluss-merge, que é de conteúdo diferente).

### 0.3.0 (2026-08-18)
- Linha de encaminhamento para a nova skill file-collect-sort-action ("recolher/ordenar ficheiros por regras",
  reconhecimento das frases-gatilho f-csa guardadas de T-20260818-916568570).
- Reposto: a linha de encaminhamento de reissverschluss-merge faltava na fonte do repositório de skills
  (existia apenas na implantação `~/.claude/skills/`) — deriva detetada durante a edição e restaurada
  aqui, para que uma futura implantação não a sobrescreva.
- Campo `version:` alinhado com a versão do changelog já alcançada (0.2.0) e contado para
  0.3.0 — antes tinha ficado em 0.1.0.

### 0.2.0 (2026-07-03)
- Linhas de encaminhamento para novas skills: skill-extractor, workflow-extract, rotation-check,
  idea-mining, bilingual-doc-sync (extração de automações Codex).

### 0.1.0 (2026-06-17)
- Versão inicial. Gerada pelo modo de auditoria ([F]) como análogo a using-superpowers. Tabela de encaminhamento
  da auditoria de 2026-06-17 (10 famílias de user).
