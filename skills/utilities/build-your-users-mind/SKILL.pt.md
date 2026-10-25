---
name: build-your-users-mind
version: 1.0.0
type: skill
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: "Remete para o módulo público e agnóstico de fornecedor build-your-users-mind: um procedimento consciente da privacidade para construir um modelo empírico de preferências de teoria da mente de um usuário autorizado a partir de seus próprios registros de interação. Use quando uma pessoa responsável quiser criar, validar, conectar ou manter um perfil de avatar de decisão, sem publicar o perfil pessoal ou suas evidências."
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [theory-of-mind, user-model, decision-avatar, feedback, privacy, pointer-skill]
language: pt
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "external"
  origin_path: "SKILL.md, templates/, scripts/, schemas/, TAXONOMY.md"
  origin_version: "1.0.0"
  origin_repo: "https://github.com/ellmos-ai/build-your-users-mind"
  last_sync_from_origin: "2026-07-30"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 50187ac74941737bc5831d58dafc99f662904adaa573192e2a0a4ae8841bc607
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:47.212732+00:00"
---
<img src="banner.png" width="100%" alt="build-your-users-mind banner">

# build-your-users-mind — referência pública e agnóstica de fornecedor

Esta skill é uma referência enxuta ao módulo público
[`ellmos-ai/build-your-users-mind`](https://github.com/ellmos-ai/build-your-users-mind).
O módulo contém o procedimento completo, modelos, esquemas, scripts, testes
e a documentação dos adaptadores de fonte. Este catálogo não duplica o código.

## O que o módulo faz

Com a autorização explícita da pessoa responsável, o módulo ajuda um agente a:

1. extrair contribuições genuinamente escritas pelo usuário a partir de seus
   próprios registros de interação;
2. redigir conteúdo sensível antes do armazenamento persistente;
3. reduzir e classificar evidências sobre preferências e decisões recorrentes;
4. construir um modelo local de preferências com níveis de confiança e
   rastreabilidade de origem;
5. conectar uma referência breve ao ambiente de execução do agente escolhido; e
6. calibrar previsões com base em feedback real e posterior.

O módulo público é um procedimento para usuários arbitrários e ambientes de
execução de agentes suportados. Não contém o modelo de nenhuma pessoa
específica.

## Limite de segurança e privacidade

- Antes de ler registros de interação, é necessária a autorização da pessoa
  responsável.
- Perfis pessoais, registros brutos, corpora de evidências e caminhos locais
  permanecem privados.
- As previsões são hipóteses incertas, não leitura de mentes, não diagnóstico e
  não declarações do usuário.
- Uma previsão de preferência nunca amplia as permissões do agente.
- Ações externas, irreversíveis, críticas para a segurança, jurídicas,
  médicas, profissionais, financeiras ou de consequências semelhantes exigem
  confirmação explícita.
- Previsões geradas pelo agente nunca devem se tornar evidência primária sobre
  o usuário.

## Instalação

```bash
git clone https://github.com/ellmos-ai/build-your-users-mind.git <clone-path>
```

Siga os arquivos atuais `README.md`, `SKILL.md`,
`SOURCE-ADAPTERS.md` e as instruções de privacidade do módulo. Mantenha o perfil
de usuário gerado fora de repositórios públicos. Para implementação e
versionamento, o repositório do módulo é a referência oficial.

## Núcleo público e perfis privados

`build-your-users-mind` é o nome público e neutro em relação ao usuário do módulo.
`decision-avatar` é o protocolo público de execução deste catálogo. O avatar
de uma pessoa nomeada, arquivos de evidências, comandos locais e instruções
específicas de perfil são extensões privadas e não devem ser publicados sob o
nome de uma skill pessoal.

## Registro de alterações

### 1.0.0 (2026-07-30)

- Adicionada a referência neutra ao módulo público independente.
- Substituído o perfil pessoal de avatar anteriormente publicado por um limite
  estrito entre núcleo público e perfil privado.
