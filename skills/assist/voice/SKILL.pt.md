---
name: voice
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: "Planejar captura de voz, transcrição e síntese de fala com ferramentas opcionais e intercambiáveis."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [voice, speech, stt, tts, provider-neutral]
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
translated_from_sha256: 3f2250be6537e73ff9d9092da422bf9682638622c11522a6d37d3cdcc7de30ba
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:43.682999+00:00"
---
<img src="banner.png" width="100%" alt="voice banner">

# Assistência de voz neutra quanto ao fornecedor

## Finalidade

Definir um fluxo de trabalho de voz sem pressupor um backend privado de fornecedor.

**Resultado:** Plano de execução com formato de entrada, decisão de privacidade, opções de ferramentas e alternativa de contingência.

## Fluxo de trabalho

1. Esclarecer o objetivo, o contexto e o formato de saída desejado.
2. Usar apenas as informações fornecidas no pedido atual.
3. Elaborar o resultado de forma estruturada e rastreável.
4. Sinalizar as suposições e obter confirmação antes de quaisquer alterações externas.

## Exemplo

**Entrada:** Planeje um fluxo de transcrição local para um arquivo de áudio.

**Resultado:** Plano de execução com formato de entrada, decisão de privacidade, opções de ferramentas e alternativa de contingência.

## Núcleo público e extensões privadas

Esta skill pública contém apenas o método transferível. Adaptadores específicos de aplicativos, contas, caminhos locais, bancos de dados e preferências pessoais pertencem a um perfil complementar privado ou a um fork privado e não devem ser incluídos neste repositório.

Sem um perfil privado, a skill trabalha apenas com as informações expressamente fornecidas no pedido atual.

## Limites e privacidade

- Os dados não são armazenados por padrão.
- Nenhuma fonte, arquivo ou interface é aberta ou alterada sem autorização expressa.
- Antes do processamento em nuvem, devem ser esclarecidos o consentimento, a classe de dados e a retenção.

## Registro de alterações

### 2.0.0 (2026-07-30)

- Núcleo público neutro quanto ao usuário; integrações privadas e perfis pessoais removidos.
