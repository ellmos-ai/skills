---
name: foerderplaner
version: 2.0.0
type: skill
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: "Planeamento de aulas, ofertas de aprendizagem e apoio individualizado, sem gerador de relatórios nem modelos pessoais."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: education
tags: [education, support, lesson-planning, differentiation]
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
translated_from_sha256: 95cabbcba2285720897ad37a00645a0f619516ee39e090f4f318320fbd8d613c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.289788+00:00"
---
<img src="banner.png" width="100%" alt="foerderplaner banner">

# Planeador de aulas e apoio

## Finalidade

Desenvolver, a partir da situação inicial e do objetivo de aprendizagem, passos concretos e verificáveis de apoio e de ensino.

**Resultado:** Objetivos, medidas, diferenciação, critérios de observação e datas de revisão.

## Fluxo de trabalho

1. Esclarecer o objetivo, o contexto e o formato de saída pretendido.
2. Utilizar apenas as informações fornecidas no pedido atual.
3. Elaborar o resultado de forma estruturada e compreensível.
4. Assinalar as suposições e obter confirmação antes de quaisquer alterações externas.

## Exemplo

**Entrada:** Planeia um apoio de quatro semanas sobre leitura para compreensão do sentido, para um grupo de alunos anonimizado.

**Resultado:** Objetivos, medidas, diferenciação, critérios de observação e datas de revisão.

## Núcleo público e extensões privadas

Esta skill pública contém apenas o método transferível. Adaptadores específicos de aplicações, contas, caminhos locais, bases de dados e predefinições pessoais pertencem a um perfil complementar privado ou a um fork privado e não devem ser incluídos neste repositório.

Sem perfil privado, a skill trabalha apenas com as informações expressamente fornecidas no pedido atual.

## Limites e proteção de dados

- Os dados não são guardados por predefinição.
- Nenhuma fonte, ficheiro ou interface é aberta ou alterada sem autorização expressa.
- A skill não cria relatórios de apoio, certificados nem avaliações oficiais. Para a elaboração geral de relatórios pode ser utilizado separadamente `report-forge`; os modelos pessoais de relatório permanecem privados.

## Registo de alterações

### 2.0.0 (2026-07-30)

- Núcleo público neutro em relação ao utilizador; integrações privadas e perfis pessoais removidos.
