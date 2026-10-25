---
name: notizblock
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: "Captura, organiza e condensa notas fornecidas, sem vínculo com um local de armazenamento ou com um aplicativo de notas."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [notes, capture, summarize, organize]
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
translated_from_sha256: e956e35efbd48948ef39712e761072ea2b368aa7216661bf649ab1ca7167532e
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.346187+00:00"
---
<img src="banner.png" width="100%" alt="notizblock banner">

# Assistente de Notas

## Finalidade

Transformar ideias soltas em temas, tarefas e decisões facilmente localizáveis.

**Resultado:** Nota estruturada com palavras-chave, tarefas e pontos em aberto.

## Fluxo de trabalho

1. Esclarecer o objetivo, o contexto e o formato de saída desejado.
2. Usar apenas as informações fornecidas no pedido atual.
3. Elaborar o resultado de forma estruturada e rastreável.
4. Sinalizar suposições e obter confirmação antes de quaisquer alterações externas.

## Exemplo

**Entrada:** Organize estas notas de conversa por temas e próximos passos.

**Resultado:** Nota estruturada com palavras-chave, tarefas e pontos em aberto.

## Núcleo público e extensões privadas

Esta skill pública contém apenas o método transferível. Adaptadores específicos de aplicativos, contas, caminhos locais, bancos de dados e preferências pessoais pertencem a um perfil complementar privado ou a um fork privado e não devem ser incluídos neste repositório.

Sem um perfil privado, a skill trabalha somente com as informações expressamente fornecidas no pedido atual.

## Limites e privacidade

- Os dados não são armazenados por padrão.
- Nenhuma fonte, arquivo ou interface é aberta ou alterada sem autorização expressa.

## Registro de alterações

### 2.0.0 (2026-07-30)

- Núcleo público neutro quanto ao usuário; integrações privadas e perfis pessoais removidos.
