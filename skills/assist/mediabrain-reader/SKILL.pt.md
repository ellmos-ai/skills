---
name: mediabrain-reader
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: "Analisa listas de mídia e metadados fornecidos, independentemente de um aplicativo de mídia específico."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [media, catalog, metadata, export]
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
translated_from_sha256: 77d211417a391dc3e75418dcc565453e223d6a4a95e85d8385714e844f16a2ba
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.626965+00:00"
---
<img src="banner.png" width="100%" alt="mediabrain-reader banner">

# Leitor de Catálogo de Mídia

## Finalidade

Avaliar os acervos de mídia por tipo, status, tema ou duplicatas.

**Resultado:** Visão geral do catálogo, problemas de qualidade e sugestões concretas de busca ou limpeza.

## Fluxo de trabalho

1. Esclarecer o objetivo, o contexto e o formato de saída desejado.
2. Usar apenas as informações fornecidas na solicitação atual.
3. Elaborar o resultado de forma estruturada e rastreável.
4. Sinalizar as suposições e obter confirmação antes de quaisquer alterações externas.

## Exemplo

**Entrada:** Resuma esta exportação JSON de mídia por tipo e status.

**Resultado:** Visão geral do catálogo, problemas de qualidade e sugestões concretas de busca ou limpeza.

## Núcleo público e extensões privadas

Esta skill pública contém somente o método transferível. Adaptadores específicos de aplicativos, contas, caminhos locais, bancos de dados e preferências pessoais pertencem a um perfil complementar privado ou a um fork privado e não devem ser incluídos neste repositório.

Sem um perfil privado, a skill trabalha apenas com as informações expressamente fornecidas na solicitação atual.

## Limites e privacidade

- Os dados não são armazenados por padrão.
- Nenhuma fonte, arquivo ou interface é aberto ou alterado sem autorização expressa.

## Registro de alterações

### 2.0.0 (2026-07-30)

- Núcleo público neutro quanto ao usuário; integrações privadas e perfis pessoais removidos.
