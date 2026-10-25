---
name: buero
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: "Organiza tarefas de escritório, correspondência e prazos sem vínculo com um aplicativo de escritório específico."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [office, planning, prioritization, correspondence]
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
translated_from_sha256: bfe1f37906e28ea592e46b37ab66ee9afb13dcc299eb505b0bf68b8b7075eea0
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:32:12.509877+00:00"
---
<img src="banner.png" width="100%" alt="buero banner">

# Assistência de Escritório

## Finalidade

Criar, a partir de temas de escritório não ordenados, uma visão geral de trabalho priorizada e realista.

**Resultado:** Prioridades, próximos passos, responsabilidades e perguntas em aberto.

## Fluxo de Trabalho

1. Esclarecer o objetivo, o contexto e o formato de saída desejado.
2. Usar apenas as informações fornecidas no pedido atual.
3. Elaborar o resultado de forma estruturada e rastreável.
4. Sinalizar as premissas e obter confirmação antes de quaisquer alterações externas.

## Exemplo

**Entrada:** Ordene estas cinco tarefas para o dia de trabalho de hoje.

**Resultado:** Prioridades, próximos passos, responsabilidades e perguntas em aberto.

## Núcleo Público e Extensões Privadas

Esta skill pública contém exclusivamente o método transferível. Adaptadores específicos de aplicativos, contas, caminhos locais, bases de dados e preferências pessoais pertencem a um perfil complementar privado ou a um fork privado e não devem ser incluídos neste repositório.

Sem um perfil privado, a skill trabalha apenas com as informações expressamente fornecidas no pedido atual.

## Limites e Proteção de Dados

- Os dados não são armazenados por padrão.
- Nenhuma fonte, arquivo ou interface é aberto ou alterado sem autorização expressa.

## Registro de Alterações

### 2.0.0 (2026-07-30)

- Núcleo público neutro quanto ao usuário; integrações privadas e perfis pessoais removidos.
