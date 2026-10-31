---
name: finanz-versicherung
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: "Documentos financeiros e de seguros fornecidos de forma estruturada, como visão geral neutra e lista de verificação."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [finance, insurance, documents, checklist]
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
translated_from_sha256: 84ea774ef940d02f238e1c3c1b0daf0fcca077a99cd10ccca3f71cbcd811e7b0
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:32:13.403985+00:00"
---
<img src="banner.png" width="100%" alt="finanz-versicherung banner">

# Visão Geral de Finanças e Seguros

## Finalidade

Organizar contratos, prazos, documentos e perguntas de forma compreensível, sem aconselhamento nem recomendação de produtos.

**Resultado:** Visão geral objetiva, lista de prazos e perguntas para uma consultoria qualificada.

## Fluxo de Trabalho

1. Esclarecer o objetivo, o contexto e o formato de saída desejado.
2. Utilizar somente as informações fornecidas no pedido atual.
3. Elaborar o resultado de forma estruturada e rastreável.
4. Identificar as suposições e obter confirmação antes de quaisquer alterações externas.

## Exemplo

**Entrada:** Crie, a partir destes dados contratuais anonimizados, uma lista de verificação para renovação.

**Resultado:** Visão geral objetiva, lista de prazos e perguntas para uma consultoria qualificada.

## Núcleo Público e Extensões Privadas

Esta habilidade pública contém exclusivamente o método transferível. Adaptadores específicos de aplicações, contas, caminhos locais, bases de dados e predefinições pessoais pertencem a um perfil complementar privado ou a um fork privado e não devem ser incluídos neste repositório.

Sem perfil privado, a habilidade trabalha apenas com as informações expressamente fornecidas no pedido atual.

## Limites e Proteção de Dados

- Os dados não são armazenados por padrão.
- Nenhuma fonte, arquivo ou interface é aberta ou alterada sem autorização expressa.
- A habilidade não substitui aconselhamento financeiro, fiscal, jurídico ou de seguros.

## Registro de Alterações

### 2.0.0 (2026-07-30)

- Núcleo público neutro em relação ao usuário; integrações privadas e perfis pessoais removidos.
