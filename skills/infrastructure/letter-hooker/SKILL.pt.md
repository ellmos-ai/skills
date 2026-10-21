---
name: letter-hooker
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: "Estende automation-self-care com Letter Hooks, bootloader de preflight, regras de travessia de documentos e enriquecimento de contexto de prompt com autocura para agentes de IA e CLIs sem hooks de ciclo de vida JSON nativos e orientados a eventos (como Antigravity / Gemini CLI). Use quando um agente precisar injetar regras de preflight, pesquisar Memory/Gardener antes de iniciar o trabalho, forçar estratégias de leitura de documentos de diretório (CLAUDE.md / AGENTS.md) ou direcionar dinamicamente tarefas sidecar para skills e protocolos de segurança."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, letter-hooker, letter-hooks, bootloader, prompt-enrichment, self-care, governance]
language: pt
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: [agy_kontext_and_workflow_loader.py]
provenance:
  origin: "fork of automation-self-care"
  origin_path: "skills/infrastructure/automation-self-care"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/skills"
translated_from_sha256: cb03d9a06cc52ced2695c952c855b3d57c168dc5b0a9ad1c412e72da13de1765
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.588386+00:00"
---
<img src="banner.png" width="100%" alt="letter-hooker banner">

# Letter-Hooker (Motor de Preflight & Governança em Nível de Prompt)

A skill **Letter-Hooker** estende `automation-self-care` para frameworks de agentes de IA (como **Antigravity / Gemini CLI**) que não possuem carregadores nativos de hooks de ciclo de vida JSON orientados a eventos (por exemplo, `~/.claude/settings.json` ou `~/.codex/hooks.json`).

Em vez de depender de hooks passivos por pressionamento de tecla, `letter-hooker` opera um **loop ativo de injeção de Letter Hooks e bootloader de preflight em nível de prompt**, por meio de tarefas agendadas e scripts de manutenção (`agy_kontext_and_workflow_loader.py`).

---

## Capacidades Principais

1. **Bootloader de Preflight & Regras de Travessia de Documentos**:
   - **Busca ascendente e descendente**: Impõe instruções estritas para que os agentes verifiquem `AGENTS.md`, `CLAUDE.md`, `START.md`, `RULES.md` e `README.md` no nível do diretório de trabalho atual. Se estiverem ausentes, percorrer para cima até encontrá-los; em seguida, verificar para baixo.
   - **Preflight de Memory & Gardener**: Consulta de preflight obrigatória a `gardener` e `memoryhooker` antes de executar alterações destrutivas ou complexas.

2. **Catálogo de Letter Hooks & Links de Referência**:
   - Arquivos modulares de instruções `.md` em `OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/`.
   - Injeta links explícitos de `file://` diretamente no texto do prompt de `sidecar.json`, para que os agentes leiam os protocolos exatos de segurança e fluxo de trabalho ao serem invocados.

3. **Lista Diária de Palavras-chave & Enriquecimento de Prompt com Autocura**:
   - Mantém uma `STICHWORTLISTE.json` diária a partir de tarefas ativas/em espera.
   - Analisa os logs de execução (`AUTOMATIONS-MEMORY.md`) em busca de padrões de erro (contexto ausente, orientação de fluxo de trabalho ausente, caminhos inválidos) e corrige dinamicamente os prompts das tarefas.

4. **Roteamento de Skills & Personas**:
   - Verifica as palavras-chave das tarefas e as mapeia para as `.SKILLS` correspondentes (por exemplo, `infrastructure/condition`, `semantic-persona-routing`, `orchestrator`, `think`, `decide`).

---

## Letter Hooks Importantes

- **`HOOK-DOC-TRAVERSAL-01`**: [bootloader_doc_traversal.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/bootloader_doc_traversal.md)
- **`HOOK-GARDENER-MEMORY-01`**: [preflight_gardener_query.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/preflight_gardener_query.md)
- **`HOOK-WORKFLOW-HYGIENE-01`**: [workflow_lock_and_git_hygiene.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/workflow_lock_and_git_hygiene.md)
- **`HOOK-PATH-VALIDATION-01`**: [path_validation_and_authority.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/path_validation_and_authority.md)

---

## Integração de Fluxo de Trabalho

```bash
# Letter-Hooker-Wartungs-Engine ausführen
python OneDrive/.SYNC/scripts/agy_kontext_and_workflow_loader.py
```

1. **Varrer sidecars**: Ler todos os textos de prompt `sidecar.json` em `~/.gemini/config/sidecars/`.
2. **Atualizar a lista de palavras-chave**: Extrair termos técnicos e salvá-los em `.SYNC/STICHWORTLISTE.json`.
3. **Injetar Letter Hooks**: Anexar regras do bootloader e links de referência de `file://` aos prompts.
4. **Registrar resultados**: Registrar atualizações em `ANTIGRAVITY-LOG.txt` e `ANTIGRAVITY-REGISTRY.md`.
