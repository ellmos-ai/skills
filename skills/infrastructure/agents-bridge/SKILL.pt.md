---
name: agents-bridge
version: 3.0.1
type: skill
author: Lukas Geiger + Codex
created: 2026-07-04
updated: 2026-08-22
description: "agents-bridge — the Lifeboat, também: Time Capsule. Ponte de arquivos portátil e neutra quanto ao provedor para superfícies de bootstrap, ponteiros de verdade, silos de memória separados, mensagens, presença, bloqueios cooperativos e recuperação reversível do host."
standalone: true
anthropic_compatible: true
category: infrastructure
tags: [multi-agent, bootstrap, recovery, messaging, memory, provider-neutral]
language: pt
status: active
visibility: public
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
translated_from_sha256: 332b9782849063f2901c750f364f3d66446b1f1f236d8fd8a6f5b67e9757e2f5
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="agents-bridge banner">

> **Português** — Versão oficial em português / Documento Oficial em Português.

# AGENTS-BRIDGE — the Lifeboat, também: Time Capsule (Português)

> **Apelidos „Lifeboat" (em alemão, bote salva-vidas) e „Time Capsule":** agents-bridge
> É o conjunto de recuperação dos arquivos de regras dos agentes (CLAUDE.md/
> GEMINI.md/GPT.md/AGENTS.md) — até agora essa função existia apenas sem
> um nome reconhecível. „Lifeboat" combina com a família de nomes náuticos em torno da
> metáfora da ponte (Wheelhouse, Deep-Diver, Lower Decks); „Time Capsule"
> enfatiza o outro lado da mesma função — um estado lacrado e verificado por hash,
> que pode ser restaurado íntegro mais tarde. Nenhuma renomeação: o nome técnico continua sendo `agents-bridge`,
> ambos os apelidos são sinônimos descritivos.

Use esta skill para capturar, verificar, transferir ou restaurar um pequeno sistema
multi-provedor baseado em arquivos. Por instância existe exatamente um arquivo
de provedor principal, escolhido explicitamente. Nenhum provedor, nome de arquivo,
host ou diretório de nuvem é canônico por implicação.

## Fluxo de trabalho e procedimento

1. Leia todas as instruções locais, bloqueios e regras de privacidade da origem e do
   destino. Preserve as alterações alheias.
2. Execute `python scripts/bridge.py discover --root <instanz>`. `discover`
   só pode assumir um marcador único `agents-bridge-primary: true`.
   Com nenhuma reivindicação ou com várias, o fluxo para com um briefing de decisão; não há
   nome de arquivo padrão.
3. Crie um perfil conforme `references/profile-v3.schema.json`. Ele nomeia
   a superfície principal, as superfícies dos provedores, as fontes de verdade, o grafo de ponteiros,
   a recuperação, os silos de memória, os mensageiros, a presença, os bloqueios e as
   inclusões/exclusões de privacidade.
4. Valide o perfil e capture a instância sem mutar a origem:

   ```text
   python scripts/bridge.py profile-validate --profile <profil.json>
   python scripts/bridge.py capture --profile <profil.json> --root <quelle> --output <neues-paket>
   ```

5. Verifique o pacote com `doctor` e gere uma prévia com `plan` ou `restore` sem
   `--apply`. Arquivos existentes nunca são sobrescritos às cegas.
6. Aplique a restauração somente após a verificação com `--apply --yes --backup-dir
   <backup> --receipt <receipt.json>`. Em seguida, `verify` e um
   teste de leitura nativo real para Claude, Codex/GPT, Gemini ou o provedor neutro.
7. Em caso de erro: esclareça o drift ou reverta o recibo exato com `rollback --yes`.
   Uma segunda restauração deve relatar `idempotent`.
8. Use `message send|ack|status`, `memory`, `presence` e
   `lock claim|release|status` apenas como pequenos contratos de arquivo. O mensageiro não substitui
   o Ticket-Master nem o agendador; os silos de memória nunca são mesclados automaticamente.

## Limites de segurança

- Um loader ou redirecionamento é preferível. Uma projeção só é permitida se as referências
  nativas não funcionarem; ela contém hashes de origem, proveniência, `generated_at` e um
  identificador de drift. A regeneração controlada ocorre somente em um novo pacote com
  `capture --regenerate-projections`.
- Todos os caminhos de perfil são codificados em UTF-8, relativos e neutros quanto à plataforma. As exportações
  são manifestadas e limitadas a inclusões/exclusões.
- Segredos, credenciais e caminhos absolutos pessoais são rejeitados de forma fail closed
  ou substituídos e registrados no modo explícito `redact`.
- Quando houver um Controlroom, ele mantém a autoridade de coordenação.
  `agents-bridge` fica então restrito a adaptador de bootstrap, recuperação e arquivos
  e não duplica nenhum runtime central.

Contratos e exemplos estão em `references/contracts.de.md`,
`references/truth-topologies.md`, `references/inventory-contract.md` e
`references/migration-2-to-3.de.md`. A versão em inglês é `SKILL.en.md`.
