---
name: skill-register-care
version: 0.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-09-20
description: "Skill de manutenção que mantém consistente o registro de skills em três partes (catálogos code-skill-index, índice de skills, mapa de famílias/roteamento SKILL-MAP). Use este skill para uma verificação de drift entre o inventário real de skills e o registro documentado: reportar entradas ausentes ou excedentes, corrigir contagens, definir a data de situação. Também acionar em “manter o registro de skills”, “atualizar o índice”, “verificar drift do registro”, “quais skills faltam no mapa”."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, register, index, drift, pflege, meta]
language: pt
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [skill-explorer, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-register-care/"
  origin_version: "0.2.0"
translated_from_sha256: 6a187b857227bb33edb71c82f4b992a376877192b746a6eea17458e9819cae46
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:50.098377+00:00"
---
<img src="banner.png" width="100%" alt="skill-register-care banner">
# Manutenção do Registro de Skills

## Finalidade

Mantém o **registro** livre de drift. O registro consiste em três artefatos interligados — nunca crie
um quarto, sempre estenda estes três:

| Artefato | Função | Manutenção |
|---|---|---|
| `~/.claude/skills/code-skill-index/references/catalog-*.md` | Catálogos de categorias | curado, manual |
| `<USER_HOME>/OneDrive/.SYNC/CLAUDE-CODE-SKILLS.md` | Índice entre sistemas (única visão de skills para o Claude Desktop) | **automatizado**, ver abaixo |
| `<USER_HOME>/OneDrive/.USR/SKILL-MAP.md` | Mapa de famílias/roteamento | curado, manual |

## Automatizado: o índice entre sistemas

O índice **não** é mais atualizado manualmente — isso o deixou parado por três meses
(situação em 21.06. em comparação com 152 skills reais em 20.09.2026; 81 faltavam). Em vez disso:

```bash
PYTHONIOENCODING=utf-8 python "<USER_HOME>/OneDrive/.SYNC/scripts/skill_index_care.py" --check
PYTHONIOENCODING=utf-8 python "<USER_HOME>/OneDrive/.SYNC/scripts/skill_index_care.py" --apply
```

Roda de qualquer forma como **passo 2b na `/sync` diária**; manualmente aqui apenas quando
skills acabaram de ser criadas ou implantadas e o índice precisa estar correto imediatamente. A execução é aditiva e
idempotente: descrições curtas curadas são mantidas, skills ausentes são ordenadas
pela categoria da biblioteca, entradas sem `SKILL.md` ativo são **marcadas em vez de excluídas**.

## Procedimento de verificação de drift (os dois registros curados)

1. **Levantar o estado atual:**
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
   Apenas skills `source=user` são relevantes para o registro (plugins/externos ficam de fora).
2. **Ler o estado desejado:** os três artefatos do registro.
3. **Calcular a diferença:**
   - **Ausente** (no inventário, não no registro) → incluir.
   - **Órfão** (no registro, não mais no inventário) → **verificar primeiro, depois decidir.**
     Uma pasta de skill cujo `SKILL.md` foi renomeado para `CONTENT.md` está *desregistrada*:
     intencionalmente não carregada como skill, mas o conteúdo existe e pode ser encontrado via `code-skill-index`.
     O inventário não a conta, mas ela também não deve ser excluída — marcar.
     Remover de fato somente se a pasta tiver sido eliminada.
   - **Divergência de contagem** (ex.: “18 skills” não confere mais) → corrigir o número.
4. **Incluir:** para cada nova skill, uma linha no `catalog-<kategorie>.md` correspondente, uma linha no
   índice de skills (+ data no cabeçalho) e — em caso de família nova/alterada — uma seção no `SKILL-MAP.md`.
5. **Data de situação** em todos os arquivos afetados definida para a data atual.

## Trecho auxiliar (listar skills de usuário ausentes)

```bash
PYTHONIOENCODING=utf-8 python -c "
import json
inv=json.load(open('<USER_HOME>/.skill-inventory.json',encoding='utf-8'))
print('\n'.join(s['dir'] for s in inv['skills'] if s['source']=='user'))
"
```
Comparar a saída com os artefatos do registro (manualmente ou com grep).

## Regras de ferro

- **Nenhum quarto registro** — apenas estender os três.
- Somente skills criadas pelo usuário pertencem ao registro; terceiros seguem o caminho externo.
- Não adivinhar datas — usar a data atual.
- **Não** manter o índice entre sistemas manualmente; executar `skill_index_care.py`. Quem acrescenta
  linhas manualmente ali cria a próxima drift silenciosa.

## Histórico de alterações

### 0.2.0 (2026-09-20)
- Índice entre sistemas `CLAUDE-CODE-SKILLS.md` migrado para `.SYNC/scripts/skill_index_care.py`
  (aditivo, com marcação, idempotente) e incluído como passo 2b na `/sync` diária. Motivo:
  o índice estava parado desde 2026-06-21 — 81 skills locais faltavam, 15 entradas
  apontavam sem marcação para procedimentos desregistrados, uma para uma pasta sem `SKILL.md`.
- “Órfão” refinado: skills desregistradas (`CONTENT.md` em vez de `SKILL.md`) são marcadas,
  não removidas — ao atualizar o índice, 15 entradas curadas teriam sido excluídas.

### 0.1.0 (2026-06-17)
- Versão inicial. Gerada pelo modo de auditoria (P2). Motivo: na auditoria de 2026-06-17 faltavam ~10 skills do usuário
  no SKILL-MAP (swarm-operations, model-strategy, agents-bridge, mcp-config-sync, system-onboarding,
  update-cli-docs, migrate-rename, plugin-system + as famílias de terapia e desenvolvimento de jogos).
