---
name: gesundheit
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: "Organiza informações de saúde fornecidas voluntariamente e prepara perguntas para profissionais de saúde."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [health, organization, questions, safety]
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
translated_from_sha256: 32342ae24156a200730212467cab366bd47e231bac5ee6ccf3f25afe867f2b64
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:32:12.802429+00:00"
---
<img src="banner.png" width="100%" alt="gesundheit banner">

# Organizar informações de saúde

## Finalidade

Resumir de forma objetiva sintomas, linhas do tempo, medicamentos e perguntas em aberto.

**Resultado:** Linha do tempo, observações estruturadas, avisos e perguntas para profissionais de saúde.

## Fluxo de trabalho

1. Esclarecer o objetivo, o contexto e o formato de saída desejado.
2. Usar apenas as informações fornecidas no pedido atual.
3. Elaborar o resultado de forma estruturada e rastreável.
4. Sinalizar suposições e obter confirmação antes de quaisquer alterações externas.

## Exemplo

**Entrada:** Organize estas anotações sobre queixas como uma linha do tempo curta para a consulta médica.

**Resultado:** Linha do tempo, observações estruturadas, avisos e perguntas para profissionais de saúde.

## Núcleo público e extensões privadas

Esta skill pública contém exclusivamente o método transferível. Adaptadores específicos de aplicativos, contas, caminhos locais, bancos de dados e preferências pessoais pertencem a um perfil complementar privado ou a um fork privado e não devem ser incluídos neste repositório.

Sem perfil privado, a skill trabalha apenas com as informações expressamente fornecidas no pedido atual.

## Limites e privacidade

- Os dados não são armazenados por padrão.
- Nenhuma fonte, arquivo ou interface é aberta ou alterada sem autorização expressa.
- A skill não faz diagnósticos e não substitui tratamento médico. Em caso de perigo agudo, são responsáveis os serviços locais de emergência.

## Registro de alterações

### 2.0.0 (2026-07-30)

- Núcleo público neutro quanto ao usuário; integrações privadas e perfis pessoais removidos.
