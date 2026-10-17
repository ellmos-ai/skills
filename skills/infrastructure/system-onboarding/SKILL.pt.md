---
name: system-onboarding
version: 1.2.0
type: skill
author: ellmos contributors
created: 2026-05-16
updated: 2026-07-29
description: "Protocolo de integração neutro quanto ao fornecedor para uma estação de trabalho nova, recém-configurada ou substituída. Configura os pré-requisitos do sistema operacional, os ambientes de execução dos agentes, as superfícies de regras compartilhadas, as skills portáteis, a configuração verificada e as evidências pós-instalação, sem copiar credenciais, prompts privados ou configuração específica do host para um repositório."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [onboarding, setup, agent-runtimes, windows, macos, verification, sync]
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
  origin_path: "internal onboarding protocol (sanitized for portable publication)"
  origin_version: "1.2.0"
  last_sync_from_origin: "2026-07-29"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 72ff75f716678c2531313f547e3c66d68df91777e120a80f43a554ecebc36899
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.164575+00:00"
---
<img src="banner.png" width="100%" alt="system-onboarding banner">

# Integração do sistema

Use este protocolo para configurar uma estação de trabalho nova ou recém-reinstalada
para trabalho com agentes local-first. Trata-se de um guia de sequência e verificação,
não é um instalador nem uma fonte de credenciais. Determine as instruções específicas
de cada produto a partir da documentação atual do respectivo fornecedor antes de alterar
um sistema ativo (live).

## Ativação

Use a skill para uma estação de trabalho nova, um sistema operacional recém-instalado,
um equipamento substituto ou a recuperação controlada de um único ambiente de execução
de agente. Primeiro, determine o sistema operacional, o ambiente de execução de destino,
a pessoa responsável, a superfície de regras compartilhada e se é desejada uma
reconstrução completa ou um reparo limitado de componentes. Não presuma que uma
configuração copiada de um host seja segura ou suportada em outro.

## Fluxo de trabalho ordenado

1. Configure as atualizações do sistema operacional, o Git, o controle de código-fonte
   autenticado, o Python e, se necessário, a versão LTS do Node.js atualmente suportada.
2. Instale apenas os ambientes de execução de agentes solicitados, por meio de seus
   instaladores suportados. Conclua os fluxos nativos de autenticação sem armazenar
   tokens em arquivos de projeto.
3. Crie as raízes de configuração local e carregue uma superfície de regras canônica
   explicitamente selecionada. Mescle os modelos; nunca sobrescreva cegamente o estado
   local existente.
4. Instale skills portáteis, bem como a configuração de MCP ou de plugins, somente por
   meio dos procedimentos de implantação documentados de cada um. Trate os formatos de
   configuração dos fornecedores como diferentes entre si.
5. Configure a sincronização compartilhada somente depois que o ambiente de execução
   local estiver funcionando. Compartilhe contratos e evidências higienizados, não
   credenciais, prompts completos nem caminhos locais da máquina.
6. Restaure agendadores ou automações apenas por meio da interface nativa suportada.
   Preserve o estado anterior e mantenha as novas tarefas desativadas até que a pessoa
   responsável autorize a ativação.
7. Execute as verificações pós-instalação pertinentes e grave uma evidência local que
   distinga instalação, configuração, registro do agendador e resultado bem-sucedido.

Leia apenas a referência correspondente ao sistema de destino:

- [Visão geral](references/overview.md) para limites e armazenamento de dados;
- [Lista de verificação do Windows](references/windows-checklist.md) para Windows;
- [Lista de verificação do macOS](references/mac-checklist.md) para macOS; e
- [Verificação pós-instalação](references/post-install.md) para verificação e recuperação.

## Limites

- Nunca publique credenciais, códigos de recuperação, prompts privados, identificadores
  de conta ou logs brutos em um repositório compartilhado ou em uma pasta de
  sincronização.
- Mantenha ambientes virtuais, caches de dependências e artefatos grandes de execução
  fora de pastas de projeto sincronizadas com a nuvem.
- Não declare uma configuração copiada como fonte de verdade. O host de destino deve
  determinar seu próprio estado suportado e confirmá-lo por releitura de verificação (readback).
- Não considere um agendamento registrado apenas porque existe um arquivo de tarefa.
  O registro nativo e a evidência de resultado são requisitos separados.
- Ao reparar um host existente, inventarie seu estado atual e seus bloqueios antes de
  alterar qualquer configuração.

## Evidência de conclusão

Um registro completo de integração documenta o sistema operacional de destino, os
ambientes de execução selecionados, as versões verificadas, as referências canônicas de
regras carregadas, as skills ou extensões explicitamente implantadas, as capacidades não
suportadas e as decisões do usuário adiadas. A conclusão bem-sucedida de um comando, por
si só, não comprova que um aplicativo carregou sua nova configuração nem que uma tarefa
agendada alcançou o resultado pretendido.

## Registro de alterações

### 1.2.0 (2026-07-29)

- A sequência de integração reutilizável e as referências de plataforma foram
  transferidas para o catálogo público de skills, após a remoção de caminhos específicos
  do host, detalhes de contas e material operacional privado.
