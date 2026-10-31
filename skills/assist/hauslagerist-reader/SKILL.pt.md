---
name: hauslagerist-reader
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: "Analisa listas de estoque ou exportações fornecidas, sem vínculo com um programa de gestão de armazém específico."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [inventory, export, stock, analysis]
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
translated_from_sha256: cfd7bc0fd235b05d91c79f55acff551f441e047584956a88790e1fb142218f88
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:32:12.620489+00:00"
---
<img src="banner.png" width="100%" alt="hauslagerist-reader banner">

# Leitor de Dados de Estoque

## Finalidade

Avaliar estoques, locais de armazenamento, quantidades mínimas e inconsistências de forma rastreável.

**Resultado:** Visão geral do estoque, faltas, duplicatas e necessidade de esclarecimento.

## Fluxo de trabalho

1. Esclarecer o objetivo, o contexto e o formato de saída desejado.
2. Usar apenas as informações fornecidas no pedido atual.
3. Elaborar o resultado de forma estruturada e rastreável.
4. Sinalizar suposições e obter confirmação antes de quaisquer alterações externas.

## Exemplo

**Entrada:** Analise esta lista CSV em busca de faltas de estoque e entradas duplicadas.

**Resultado:** Visão geral do estoque, faltas, duplicatas e necessidade de esclarecimento.

## Núcleo público e extensões privadas

Esta skill pública contém apenas o método transferível. Adaptadores específicos de aplicativos, contas, caminhos locais, bancos de dados e preferências pessoais pertencem a um perfil complementar privado ou a um fork privado e não devem ser incluídos neste repositório.

Sem um perfil privado, a skill trabalha somente com informações fornecidas explicitamente no pedido atual.

## Limites e privacidade

- Os dados não são armazenados por padrão.
- Nenhuma fonte, arquivo ou interface é aberta ou alterada sem autorização explícita.

## Registro de alterações

### 2.0.0 (2026-07-30)

- Núcleo público neutro quanto ao usuário; integrações privadas e perfis pessoais removidos.
