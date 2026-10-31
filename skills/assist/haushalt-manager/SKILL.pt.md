---
name: haushalt-manager
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: "Planeje tarefas domésticas, rotinas e responsabilidades sem vínculo com um aplicativo específico."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [household, routines, tasks, planning]
language: pt
status: stable
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: public-neutral
  origin_license: MIT
  notes: Public core only; adapters and private profiles are excluded.
translated_from_sha256: ae0664c321208aed38a5774c87643a6d92d7008fd806358c1d756a3bcb66ebd5
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:32:13.490110+00:00"
---
<img src="banner.png" width="100%" alt="haushalt-manager banner">

# Planejamento doméstico

## Finalidade

Distribuir de forma realista tarefas recorrentes e pontuais.

**Resultado:** Plano semanal com esforço, prioridade, responsável e margem de tempo.

## Fluxo de trabalho

1. Esclarecer o objetivo, o contexto e o formato de saída desejado.
2. Usar apenas as informações fornecidas no pedido atual.
3. Elaborar o resultado de forma estruturada e rastreável.
4. Sinalizar as suposições e obter confirmação antes de quaisquer alterações externas.

## Exemplo

**Entrada:** Crie, a partir destas tarefas, um plano semanal equilibrado.

**Resultado:** Plano semanal com esforço, prioridade, responsável e margem de tempo.

## Núcleo público e extensões privadas

Esta skill pública contém somente o método transferível. Adaptadores específicos de aplicativos, contas, caminhos locais, bancos de dados e preferências pessoais pertencem a um perfil complementar privado ou a um fork privado e não devem ser incluídos neste repositório.

Sem um perfil privado, a skill trabalha apenas com as informações expressamente fornecidas no pedido atual.

## Limites e privacidade

- Os dados não são armazenados por padrão.
- Nenhuma fonte, arquivo ou interface é aberta ou alterada sem autorização explícita.

## Registro de alterações

### 2.0.0 (2026-07-30)

- Núcleo público neutro quanto ao usuário; integrações privadas e perfis pessoais removidos.
