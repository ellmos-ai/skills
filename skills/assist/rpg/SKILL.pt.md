---
name: rpg
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: "Oferece suporte neutro quanto ao sistema para aventuras, cenas, personagens e organização de campanhas."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [rpg, tabletop, campaign, storytelling]
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
translated_from_sha256: e3212bbae62e830a6854e001ae90aa69fb5961b11dea658eff62149ab81a6f01
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.544713+00:00"
---
<img src="banner.png" width="100%" alt="rpg banner">

# Ajuda para RPG de mesa

## Finalidade

Apoiar mestres de jogo e grupos com rascunhos consistentes e adaptáveis.

**Resultado:** Rascunho de cena, motivações de PNJ, conflitos, pistas e variantes opcionais.

## Fluxo de trabalho

1. Esclarecer objetivo, contexto e formato de saída desejado.
2. Usar apenas as informações fornecidas no pedido atual.
3. Criar o resultado de forma estruturada e rastreável.
4. Sinalizar suposições e obter confirmação antes de quaisquer alterações externas.

## Exemplo

**Entrada:** Crie um rascunho curto de cena no porto com duas pistas e uma complicação.

**Resultado:** Rascunho de cena, motivações de PNJ, conflitos, pistas e variantes opcionais.

## Núcleo público e extensões privadas

Esta skill pública contém apenas o método transferível. Adaptadores específicos de aplicativos, contas, caminhos locais, bancos de dados e predefinições pessoais pertencem a um perfil complementar privado ou a um fork privado e não devem ser incluídos neste repositório.

Sem perfil privado, a skill trabalha apenas com as informações expressamente fornecidas no pedido atual.

## Limites e privacidade

- Os dados não são armazenados por padrão.
- Nenhuma fonte, arquivo ou interface é aberta ou alterada sem autorização expressa.

## Registro de alterações

### 2.0.0 (2026-07-30)

- Núcleo público neutro quanto ao usuário; integrações privadas e perfis pessoais removidos.
