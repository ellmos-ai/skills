---
name: projekt-pipeline-umbrella
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "Meta-/Umbrella-Skill para a família \"Construção e Reestruturação de Projetos/Pipelines\". Conhece todos os skills para criar, registrar, reestruturar e analisar projetos e pipelines e encaminha para o adequado. Use este skill quando não estiver claro se algo deve ser criado do zero (Greenfield) ou reestruturado (Existente), ou se trata de um único projeto ou de uma pipeline inteira. Também acione com \"criar novo projeto/pipeline\", \"reestruturar existente\", \"incorporar projeto\", \"renovar estrutura de pastas\", \"qual bootstrapper serve\"."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [projekt, pipeline, bootstrap, umbau, umbrella, meta, routing]
language: pt
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [project-bootstrapper, pipeline-bootstrapper, project-onboarding, pipeline-optimizer, docs-analysis, dev-cycle]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/projekt-pipeline-umbrella/"
  origin_version: "0.1.0"
translated_from_sha256: 4a9761a120e11fee3911e26619e8d3b27f0b91e19925d6bc41ba7e44792a96c9
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="projekt-pipeline-umbrella banner">
# Construção & Reestruturação de Projetos/Pipelines — Umbrella

## Finalidade

Ponto de entrada para a família "Construção & Reestruturação de Projetos/Pipelines". Os membros se
organizam ao longo de dois eixos: **Greenfield vs. Existente** e **nível de Projeto vs. nível de Pipeline**. Esta
umbrella evita a confusão frequente entre "bootstrap", "optimize" e "onboard".

## Membros & Roteamento

| Skill | Para quê | Quando usar este em vez dos outros |
|-------|----------|------------------------------------|
| `/project-bootstrapper` | Criar um NOVO projeto **dentro** de uma pipeline existente | Greenfield, nível de projeto |
| `/pipeline-bootstrapper` | Criar uma pipeline NOVA de nível superior, por completo | Greenfield, nível de pipeline (raro) |
| `/project-onboarding` | Incorporar/capturar um projeto existente | Existente, nível de projeto |
| `/pipeline-optimizer` | Renovar pipeline/estrutura existente (procedimento de 6 passos) | Existente, reestruturação |
| `/docs-analysis` | Verificar documentos de requisitos/conceito contra o código atual | Existente, análise (sem reestruturação) |
| `/dev-cycle` | Estrutura de desenvolvimento em 8 fases para a construção propriamente dita | transversal: o COMO do desenvolvimento |

> Regra de roteamento: **novo + projeto** → `/project-bootstrapper` · **novo + pipeline** →
> `/pipeline-bootstrapper` · **incorporar projeto existente** → `/project-onboarding` · **reestruturar existente** →
> `/pipeline-optimizer` · **apenas verificar** → `/docs-analysis` · **construir** → `/dev-cycle`.

## Combinações bem acopladas

- `/project-onboarding` (primeiro: incorporar o projeto existente) → `/pipeline-optimizer` (depois: reestruturar de forma direcionada) —
  primeiro entender, depois renovar (cobre o princípio dos 6 passos "primeiro ler, depois escrever").
- `/docs-analysis` (encontrar lacunas) → `/dev-cycle` (fechar lacunas).
- `/project-bootstrapper` (estrutura) → `/dev-cycle` (desenvolver o conteúdo).

## Convenções comuns

- Leia sempre primeiro as convenções existentes da pipeline (registro, templates, CLAUDE.md) — não crie
  padrões paralelos.
- Skills Greenfield criam, skills para projetos existentes renovam — não misture.
- Leia os arquivos atuais (em produção) dos skills individuais antes de aplicar.

## Changelog

### 0.1.0 (2026-06-17)
- Versão inicial. Gerada pelo modo de auditoria (3c1) para a família Projeto/Pipeline.
