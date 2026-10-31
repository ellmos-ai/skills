---
name: therapie-umbrella
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "Meta-/Umbrella-Skill para a família „Terapia / Aconselhamento\". Conhece todos os skills terapêuticos (estabilização, visão geral de métodos, condução da conversa + procedimentos especiais desregistrados) e encaminha para o adequado. Use este skill quando não estiver claro qual skill de terapia/aconselhamento se encaixa, quando for necessária uma visão geral dos procedimentos disponíveis, ou quando uma situação de aconselhamento/crise precisar ser primeiro contextualizada. Também acione para „qual método terapêutico se encaixa\", „estruturar o aconselhamento\", „crise — o que fazer\", „escolher a abordagem terapêutica\"."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: therapy
tags: [therapie, beratung, umbrella, meta, routing]
language: pt
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [counseling-basics, guideline-therapies-overview, stabilization-techniques, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/therapie-umbrella/"
  origin_version: "0.1.0"
translated_from_sha256: 11cdb04f6cb7265c340ca6748ebb395ec6b6bc445fb3dad494f25cfcffd81259
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.468231+00:00"
---
<img src="banner.png" width="100%" alt="therapie-umbrella banner">
# Terapia / Aconselhamento — Umbrella

## Finalidade

Ponto de entrada para a família „Terapia / Aconselhamento". Reúne o roteamento geral e encaminha
para o skill adequado em casos especiais. Três skills de entrada ativos formam a frente;
por trás há uma cauda mais longa de procedimentos especiais desregistrados, acessíveis via `code-skill-index`
(catálogo `catalog-therapy.md`).

## Membros & Roteamento

| Skill | Para quê | Quando usar este em vez dos outros |
|-------|----------|------------------------------------|
| `/stabilization-techniques` | Intervenção em crise, grounding, lugar seguro, PMR, pânico, Window of Tolerance | **Primeiro** em sofrimento agudo/crise — estabilização antes da metodologia |
| `/guideline-therapies-overview` | Visão geral dos procedimentos de diretriz: TCC, ACT, terapia do esquema, exposição, sistêmica, psicodinâmica | Quando o **método** adequado deve ser escolhido/explicado |
| `/counseling-basics` | Condução da conversa: escuta ativa, espelhamento, validação, MI/OARS, perguntas circulares | Quando se trata do **COMO da conversa**, não do método |
| (skills especiais desregistrados) | Procedimentos individuais (genograma, detalhes de exposição, psicologia positiva, …) | Quando um procedimento individual específico for necessário em profundidade → via `code-skill-index` |

> Regra de roteamento: crise aguda → `/stabilization-techniques` · escolher/explicar método →
> `/guideline-therapies-overview` · técnica de conversa → `/counseling-basics` · procedimento individual em profundidade →
> skill especial desregistrado via `code-skill-index`.

## Combinações bem acopladas

- `/stabilization-techniques` (primeiro, agudo) → `/guideline-therapies-overview` (depois, médio prazo):
  primeiro estabelecer segurança/Window of Tolerance, depois escolher o procedimento de diretriz adequado.
- `/counseling-basics` acompanha **ambos** — a postura conversacional (MI/OARS, validação) sustenta
  tanto a estabilização quanto o trabalho metodológico.

## Convenções comuns

- Não substituir o diagnóstico; trabalhar de forma psicoeducativa e orientada a recursos.
- Window of Tolerance como eixo condutor: em hiperexcitação, estabilizar primeiro, não confrontar.
- Ler os arquivos ativos dos skills individuais antes da aplicação — este umbrella não reproduz conteúdos.

## Changelog

### 0.1.0 (2026-06-17)
- Versão inicial. Gerada pelo modo de auditoria (1c1) para a família Terapia / Aconselhamento.
