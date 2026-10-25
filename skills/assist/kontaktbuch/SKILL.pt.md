---
name: kontaktbuch
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: "Organiza os dados de contacto fornecidos voluntariamente de forma a minimizar os dados e identifica possíveis duplicados."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [contacts, organization, deduplication, privacy]
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
translated_from_sha256: d9b3652c9acade9d21c9d30f6b8f92c205df1426c25ada123ddd434f7ab397ff
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:32:13.038064+00:00"
---
<img src="banner.png" width="100%" alt="kontaktbuch banner">

# Visão geral dos contactos

## Objetivo

Estruturar contactos para uma tarefa concreta, sem incluir uma agenda pessoal.

**Resultado:** Campos normalizados, possíveis duplicados e informações em falta.

## Fluxo de trabalho

1. Esclarecer o objetivo, o contexto e o formato de saída pretendido.
2. Utilizar apenas as informações fornecidas na tarefa atual.
3. Criar o resultado de forma estruturada e rastreável.
4. Assinalar as suposições e obter confirmação antes de quaisquer alterações externas.

## Exemplo

**Entrada:** Verifica esta lista de contactos anonimizada quanto a duplicados.

**Resultado:** Campos normalizados, possíveis duplicados e informações em falta.

## Núcleo público e extensões privadas

Esta skill pública contém exclusivamente o método transferível. Adaptadores específicos de aplicações, contas, caminhos locais, bases de dados e predefinições pessoais pertencem a um perfil complementar privado ou a um fork privado e não devem ser incluídos neste repositório.

Sem um perfil privado, a skill trabalha apenas com as informações expressamente fornecidas na tarefa atual.

## Limites e proteção de dados

- Os dados não são armazenados por predefinição.
- Nenhuma fonte, ficheiro ou interface é aberto ou alterado sem autorização expressa.

## Registo de alterações

### 2.0.0 (2026-07-30)

- Núcleo público neutro em relação ao utilizador; integrações privadas e perfis pessoais removidos.
