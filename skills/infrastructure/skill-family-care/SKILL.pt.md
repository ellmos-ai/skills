---
name: skill-family-care
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "Skill de manutenção que mantém as famílias de skills atualizadas, sem executar a auditoria completa do skill-explorer. Use este skill quando um novo skill precisar ser atribuído à família correta, um roteador de cabeçalho de família precisar ser atualizado após uma alteração de família, ou um roteador órfão precisar ser removido. Também acione com \"manter famílias\", \"atribuir novo skill a uma família\", \"atualizar roteador\", \"definir/remover cabeçalho de família\"."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, familien, pflege, routing, meta]
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
  origin_path: "~/.claude/skills/skill-family-care/"
  origin_version: "0.1.0"
translated_from_sha256: b4d39973bb0e97c3190c0f821fe0a351a0f338cdfd1ea6fff26d44d1ca476c21
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.851076+00:00"
---
<img src="banner.png" width="100%" alt="skill-family-care banner">
# Manutenção de Famílias de Skills

## Finalidade

Mantém as **famílias** de skills atualizadas — sem a execução completa da auditoria de `skill-explorer`. Desmembrado
segundo o princípio do instalador (subskill enxuto em vez de monólito). Referencia os scripts de
`skill-explorer`, não os copia.

## Fontes (não duplicar)

- **Lista de famílias:** `<USER_HOME>\OneDrive\.USR\SKILL-MAP.md` (mapa canônico de famílias/roteamento).
- **Inventário (estado atual):** `skill-explorer/scripts/inventory_skills.py`.
- **Definir/remover roteador:** `skill-explorer/scripts/inject_family_header.py`.
- **Configuração (quais famílias estão vinculadas):** `~/.claude/skills/skill-explorer/config.json`.

## Tarefas

### A — Atribuir um novo skill a uma família
1. Reexecutar o levantamento do inventário:
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
2. Escolher a família adequada em `SKILL-MAP.md` (eixos: fase/amplitude/rigidez/efeito/matéria-prima).
3. Registrar o skill como membro em `config.json` (`families[<fam>].members`) e em `SKILL-MAP.md`.

### B — Atualizar o roteador de cabeçalho após alteração de família
```bash
PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inject_family_header.py \
    --family <Familie> --skills s1,s2,s3 --router "<Wegweiser>" --inventory ~/.skill-inventory.json
```
- Idempotente: um bloco existente da mesma família é substituído.
- Somente skills `editable`/`source=user` são modificados (controle de acesso no script).

### C — Remover um roteador órfão
Mesmo script com `--remove` (não é necessário `--router`).

## Regras de ferro

- **Levantamento ≠ Mutação:** apenas skills próprios do usuário recebem cabeçalho. Nunca alterar plugins/externos.
- Após cada alteração, atualizar `config.json` (`families[*].linked`, `updated`).
- Não copiar conteúdo do mapa de famílias para os skills individuais — apenas o bloco de indicação.

## Changelog

### 0.1.0 (2026-06-17)
- Versão inicial. Gerada pelo modo de auditoria (P1).
