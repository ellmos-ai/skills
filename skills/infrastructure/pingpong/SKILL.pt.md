---
name: pingpong
version: 1.1.0
type: protocol
author: Lukas Geiger, OpenAI Codex
created: 2026-08-03
updated: 2026-09-13
description: "Opera uma estação de rádio com duração limitada e vinculada à sessão, por meio de uma pasta sincronizada em conjunto. O ListenSync varre sistematicamente em busca de pedidos e novidades; o WriteSync envia deltas e recibos. Usar em PingPong, Dosentelefon (telefone de lata), ListenSync, WriteSync, Sync-Listener (listener de sincronização), Auftragswache (vigia de pedidos), News-Scan (varredura de novidades) ou monitoramento de Goal/Loop."
# Kompatibilität
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: infrastructure
tags: [pingpong, sync, listener, goal, loop, cadence, filecommander]
language: pt
status: active
visibility: public

# Abhängigkeiten
dependencies:
  tools: [ellmos-filecommander]
  services: []
  protocols: [shared-folder-sync]
  python: []

roles:
  - id: pingpong
    label: PingPong
    prompt: skills/infrastructure/pingpong/SKILL.en.md
    request: Read and follow the PingPong protocol for the requested mode and duration.
    modes: [ListenSync, WriteSync]
    providers: [codex, claude]

# Provenance
provenance:
  origin: "custom"
  origin_path: "local-skill/pingpong"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-08-04"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 6f644ddfdc91c21a6250f7af08b78211b2949ad989b2e2f9104d71bed1ef062b
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:50.098377+00:00"
---
<img src="banner.png" width="100%" alt="pingpong banner">

# PingPong

Opere dois ou mais sistemas como estações de rádio por meio de uma pasta de sincronização comum. Mantenha o contrato funcional neutro em relação ao provedor; apenas o adaptador de continuação difere.

## Determinar o modo

- ListenSync: Exatamente um listener sistemático por host. Ele varre, assume os pedidos correspondentes e, em caso de respostas, também executa o WriteSync.
- WriteSync: Cada ator que trabalha pode enviar seus próprios deltas, pedidos, novidades e recibos relevantes. Este modo não inicia um listener.
- Se o modo não estiver definido, use ListenSync.

## Esclarecer a participação (STATE e CALL)

Antes do contrato de execução, a verificação em duas etapas decide se alguém pode ser contatado. `scripts/pingpong_runtime.py check --slot <slot> --sync-root <pfad>` responde com exatamente três valores: Exit 0 `call-for-me` (ativar e iniciar um agente), Exit 1 `idle` (eu mesmo estou ativo, desativar), Exit 3 `check-failed` (ilegível, nunca tratar como ociosidade). A participação exige STATE e CALL simultaneamente; quem convoca um Call o encerra quando o propósito for cumprido, caso contrário ele expira. Regras completas em references/protocol.md.

## Definir o contrato de execução

1. Use 24h por padrão. Aceite também durações relativas como 15m, 2h, 3d ou um horário final absoluto em ISO 8601.
2. Meça o horário local de início e informe expires_at com data, hora e fuso horário.
3. Comece com 15 minutos. Use a cadência de references/protocol.md, a menos que o usuário exija uma cadência fixa.
4. Defina o cumprimento do objetivo como: horário final atingido, varredura final do FileCommander comprovada, todas as entradas correspondentes detectadas até então processadas ou bloqueios precisos documentados, State atualizado e scheduler próprio encerrado.
5. Não afirme varredura nem cumprimento do objetivo sem comprovação do FileCommander.

## Usar o adaptador do provedor

### Codex

Antes da primeira varredura, crie explicitamente um Goal persistido com o contrato de execução completo e expires_at. Em cada continuação, execute exatamente um ciclo completo de varredura. Não encerre o Goal após um ciclo individual vazio ou bem-sucedido. Depois, aguarde de fato até next_scan_at, por exemplo com:

    python "<skill-root>/scripts/pingpong_runtime.py" wait --until "<next_scan_at>"

No momento do vencimento, execute o ciclo de encerramento. Marque o Goal como concluído somente quando o critério de sucesso estiver cumprido.

### Claude Code

Inicie a tarefa como /loop <Kadenz> $pingpong. Se a skill já vier de uma execução agendada, não crie um segundo loop. Ao alterar a cadência, substitua apenas o próprio job de Cron. Exclua-o após o ciclo de encerramento.

## Executar o ciclo

Leia references/protocol.md por completo e execute exatamente um ciclo de varredura, processamento e State descrito ali. Use o ellmos FileCommander para cada acesso à pasta de sincronização. Uma listagem de shell, uma entrada do scheduler ou um nome de arquivo sozinhos não são comprovação de varredura.

Não invente trabalho quando estiver ocioso. Relate de forma breve: horário da varredura, arquivos de Freshness lidos, cadência atual, empty_runs, next_scan_at e expires_at.

## Executar o WriteSync

Escreva apenas no próprio slot do sistema ou em um canal global explicitamente indicado. Informe remetente, destinatário, horário, referência, ação, resultado, pontos em aberto e cadência desejada. Faça merge em vez de sobrescrever; sem credenciais; respeite os locks. Após escrever, releia o arquivo canônico com o FileCommander.

## Changelog

### 1.1.0 (2026-09-13)

- Adicionada a marca de participação por host STATE (campo `pingpong` em `agents/registry/<slot>.state.json`) e arquivos CALL endereçados `call-<von>-to-<an|all>.txt` com expiração; `pingpong_runtime.py` conhece para isso `state`, `call` e a verificação em duas etapas `check` com resultado de três valores. Os nomes antigos `pull-` ainda são lidos temporariamente. Implementação de T-20260830-425388998 conforme decisão do usuário de 2026-09-11 (corte mínimo: apenas STATE, CALL e expiração).

### 1.0.1 (2026-09-09)

- Adicionados metadados declarativos de papel conforme o contrato opcional de papel do Módulo v2; nenhum starter neutro é declarado. A identidade de protocolo existente e o caminho de descoberta são mantidos.

### 1.0.0 (2026-08-04)

- Contrato ListenSync/WriteSync neutro em relação ao provedor, com adaptadores de Goal do Codex e de Loop do Claude.
- Adicionados comprovação via FileCommander, guarda de Freshness, cadência adaptativa e condição absoluta de expiração.
