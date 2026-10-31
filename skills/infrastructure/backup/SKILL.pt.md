---
name: backup
version: 1.0.0
type: skill
author: User
created: 2026-08-24
updated: 2026-08-24
description: "Planeja, espelha, verifica, restaura ou arquiva arquivos explicitamente através do núcleo fail-closed mac-backup. Usar para os próprios jobs de backup entre hosts do usuário; não para sincronização geral em nuvem ou cópia casual de arquivos."
visibility: public
language: pt
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance:
  origin: "custom"
  origin_repo: "github.com/ellmos-ai/mac-backup"
  last_sync_from_origin: "2026-08-24"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: c50a9f8b557b5e4baa08f880f28ba234c8f56974e644ce57147bde5311a02ad6
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="backup banner">

# Backup

Usar a CLI `mac-backup` instalada como a única implementação de transferência. Não reconstruir o fluxo com `scp`, `rsync`, SSHFS, ações do Explorer ou exclusão ad hoc.

## Direcionar a solicitação

- Um pedido comum de "backup" significa `mirror`; a origem permanece intacta.
- `archive` significa limpeza da origem e é uma intenção destrutiva separada. Nunca inferir a partir de "backup", "copy"/"cópia" nem de "free some space"/"liberar espaço".
- `restore` grava em um novo destino e nunca sobrescreve silenciosamente.
- Se não existir um JSON de job verificado, preparar uma proposta de job e pausar antes de `init-target` ou da transferência.

## Execução

1. Ler o job e executar `mac-backup plan <job> --json`.
2. Verificar que a classe de origem, a contagem de arquivos, a contagem de bytes, o ID do volume de destino, o status de criptografia e a impressão digital do host retornados correspondem à solicitação e ao comprovante atual do dispositivo.
3. Para mirror, executar `mac-backup mirror <job> --json` e depois `mac-backup verify <job> --json`.
4. Para restore, usar um novo destino absoluto e verificar os arquivos restaurados pelo resultado do manifesto do comando.
5. Para archive, passar `--confirm-delete` somente se o usuário tiver pedido explicitamente a remoção da origem e o plano verificado nomear exatamente essa origem. Um bloqueio de política é o resultado correto; nunca contornar `target_encryption_required`, `source_class_unknown_cleanup_blocked`, `onedrive_dehydrate_not_implemented`, um lock, um desvio de identidade ou uma âncora ausente.

`init-target` é uma configuração privilegiada, não uma execução de rotina. Requer um comprovante do sistema operacional, obtido de forma independente, para o ID do volume e a criptografia; um valor copiado do job proposto não é comprovante.

Nunca afirmar que um mirror é um backup completo antes de a verificação do destino e um teste real de restore terem sido aprovados. Manter segredos, arquivos de job reais, âncoras locais e nomes de arquivos do usuário fora de tickets, Git e OneDrive.

## Changelog

### 1.0.0 (2026-08-24)
- Cópia neutralizada do master de implantação `~/.claude/skills/backup/`, incluída na biblioteca categorizada. Causa da lacuna de sincronização: a skill estava implantada, mas não tinha entrada de origem em `skills/<category>/`, então `skill_sync.py status` a relatava como `NUR-ZIEL` (apenas destino) e `catalog.py`/`build_public_registry.py` (que só varrem `skills/`) nunca a viam — por isso ela nunca conseguia alcançar o registro público ou `SKILLS-MAP.md`, não importando como a cópia de implantação fosse editada.
