---
name: metacognitive-injectors
version: 1.4.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-30
updated: 2026-07-30
description: "Estratégias metacognitivas de injeção e autodiálogo (Self-Talk, Auditoria Metacognitiva, Hooks de Avaliação, Listas de Verificação Pré-Voo, Persistência de Estado e Personas). Integra a Busca Ativa de Informação (memória do sistema Gardener e USMC), Rehearsal (Recuperação Ativa e Reprodução), a Memória de Trabalho de Baddeley (Estado + Hooks), as Funções Executivas de Miyake, bem como estratégias terapêuticas de TCC/ACT."
standalone: true
anthropic_compatible: true
bach_compatible: true
category: infrastructure
tags: [metacognition, self-talk, metacognitive-injectors, evaluator-hook, quality-gate, multi-agent, auditing, pre-flight-checklist, working-memory, active-retrieval, rehearsal, gardener, usmc, state-persistence, hooks, survival-routing, persona-routing]
aliases: [self-talk, metacognitive-self-talk, metacognitive-auditing, evaluator-hook, preflight-checklist, inner-speech, active-retrieval, rehearsal]
language: pt
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
translated_from_sha256: e692cdc2b2eb66f784fc25d0f36596e1342e828e67d91bc8aeca5eb3f456d8c2
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:50.098377+00:00"
---
<img src="banner.png" width="100%" alt="metacognitive-injectors banner">

# Injetores Metacognitivos (Metacognitive-Injectors, Recuperação Ativa e Busca em Memória)

A habilidade **Metacognitive-Injectors** (também conhecida como **`self-talk`**, **`metacognitive-auditing`**, **`evaluator-hook`**, **`preflight-checklist`**, **`inner-speech`**, **`active-retrieval`** e **`rehearsal`**) estabelece estratégias de automonitoramento fundamentadas na psicologia cognitiva e em princípios terapêuticos para agentes de IA.

---

## 1. Busca Ativa de Informação & Memória do Sistema (Gardener & USMC)

### A. Busca Ativa de Informação nas Memórias do Sistema
- Antes de presunções ou afirmações precipitadas, **pesquisar ativamente nas memórias do sistema**:
  1. **Gardener DB (`gardener.py` / `hb_garden_*`):** Pesquisa efeitos de aprendizagem observados, decisões do usuário e acordos de caminho (por ex., `Gardener().find("companion")`).
  2. **USMC SQLite DB (`usmc_memory.db`):** Consulta fatos armazenados, lições e históricos de sessão.
  3. **Arquivos centrais de regras (`CLAUDE.md`, `.SYNC`, `AGENTS.md`):** Lê convenções existentes e indicações de caminho.

### B. Rehearsal: Recuperação Ativa & Reprodução (Retrieval Practice)
- **Laço de rehearsal subvocal (laço fonológico):**
  Não apenas ler informações passivamente, mas **recuperá-las ativamente, reconstruí-las na memória de trabalho e confrontá-las com a realidade** antes da execução.
  - *"Recuperei na memória o caminho exato do script?"*
  - *"A sintaxe do comando corresponde aos exemplos armazenados na memória do sistema?"*

---

## 2. Fundamentação em Ciência Cognitiva & Terapia

### A. Memória de Trabalho = Estado + Hooks (Baddeley & Cowan)
- **Estado (conteúdo da memória):** Persiste estados intermediários voláteis após cada subetapa em tabelas SQLite (`usmc_memory.db`), `AUTOMATIONS-MEMORY.md` ou buffers de estado locais.
- **Hooks (mecanismo de controle):** Bootloader de pré-voo, Letter-Hooks e Hooks de avaliação PreToolUse/PostToolUse.

### B. Funções Executivas de Miyake (Comando & Controle)
1. **Inibição (controle de impulsos):** Suprime encerramentos precipitados e mensagens de sucesso alucinadas.
2. **Alternância (flexibilidade cognitiva):** Muda dinamicamente para roteamento de sobrevivência, modos de persona ou caminhos alternativos de solução diante de bloqueios.
3. **Atualização (atualização da memória de trabalho):** Atualiza continuamente o estado de trabalho.

### C. Impulsos Terapêuticos (TCC, ACT e terapia orientada a soluções)
- **Reestruturação cognitiva (TCC):** Reenquadrar erros como dados diagnósticos valiosos.
- **Desfusão cognitiva & aceitação (ACT):** Aceitar e explicitar a própria incerteza como estado.
- **Experimentos comportamentais:** Executar smoke-tests/dry-runs para obter evidência empírica real.

---

## 3. Cadeia de Fallback Multimodelo & Interface do Codex Companion

| Prioridade | Consultor / Revisor | Interface / Comando | Função / Regra |
| :--- | :--- | :--- | :--- |
| **Primário (1)** | **Gemini Subagent** | `invoke_subagent` / `define_subagent` | Revisor interno rápido para verificações de rotina. |
| **Secundário (2)** | **Codex Companion (Nativo)** | `node "<USER_HOME>\.codex\.tmp\marketplaces\openai-codex\plugins\codex\scripts\codex-companion.mjs" task "..."` | Codex Companion nativo para revisões e **aceitação `/goal`**. |
| **Terciário (3)** | **Codex CLI Direct** | `codex exec --skip-git-repo-check` | Chamada direta da Codex CLI. |
| **Quaternário (4)** | **Claude CLI / Swarm** | `claude -p ...` / `hb_swarm_consensus` | Terceira opinião em caso de limites de tokens. |

---

## 4. Injeção de Prompt Específica por Área (Tailored Injection Pattern)

O injetor (`agy_metacognitive_prompt_injector.py`) seleciona estratégias específicas para cada área:

- **Bloco base (todos os sidecars):** Contra a execução vazia, aceitação **`/goal`** por modelo externo, Busca Ativa de Informação (Gardener/USMC), Rehearsal (Recuperação Ativa), Lista de Verificação Pré-Voo.
- **Sidecars de pesquisa (`research-*`):** Ampliados com *Pesquisa baseada em evidências (nenhuma fonte sem comprovante de consulta)*, *Reenquadramento de TCC & desfusão cognitiva (resultados negativos como achado)*.
- **Sidecars de software/Roblox (`software-*`, `roblox-*`):** Ampliados com *Laço fonológico & rehearsal*, *Persistência do estado da memória de trabalho*, *Roteamento de sobrevivência*.
- **Maintainer & Generalists (`maintainer-*`, `generalist-*`):** Ampliados com *Busca ativa de informação*, *Skill-Finder* e *Memory Hooks*.
