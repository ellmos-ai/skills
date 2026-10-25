---
name: projekt-pipeline-umbrella
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "Méta-/méga-skill (umbrella) pour la famille « Construction & refonte de projets/pipelines ». Connaît tous les skills permettant de créer, reprendre, refondre et analyser des projets et des pipelines, et oriente vers le bon. Utilisez ce skill lorsqu'il n'est pas clair si quelque chose doit être créé à neuf (Greenfield) ou refondu (existant), ni s'il s'agit d'un projet unique ou d'un pipeline complet. À déclencher également pour « créer un nouveau projet/pipeline », « refondre l'existant », « reprendre un projet », « rénover l'arborescence », « quel bootstrapper convient »."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [projekt, pipeline, bootstrap, umbau, umbrella, meta, routing]
language: fr
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
translated_at: "2026-10-15T11:32:13.586675+00:00"
---
<img src="banner.png" width="100%" alt="projekt-pipeline-umbrella banner">
# Construction & refonte de projets/pipelines — Umbrella

## Objet

Point d'entrée de la famille « Construction & refonte de projets/pipelines ». Les membres se répartissent
selon deux axes : **Greenfield vs. existant** et **niveau projet vs. niveau pipeline**. Cette umbrella
évite la confusion fréquente entre « bootstrap », « optimize » et « onboard ».

## Membres & routage

| Skill | Usage | Quand choisir celui-ci plutôt qu'un autre |
|-------|-------|-------------------------------------------|
| `/project-bootstrapper` | Créer un NOUVEAU projet **dans** un pipeline existant | Greenfield, niveau projet |
| `/pipeline-bootstrapper` | Créer un TOUT NOUVEAU pipeline de niveau supérieur | Greenfield, niveau pipeline (rare) |
| `/project-onboarding` | Reprendre/recenser un projet existant | Existant, niveau projet |
| `/pipeline-optimizer` | Rénover un pipeline/une structure existant(e) (procédure en 6 étapes) | Existant, refonte |
| `/docs-analysis` | Vérifier les documents d'exigences/de conception par rapport au code actuel | Existant, analyse (sans refonte) |
| `/dev-cycle` | Cadre de développement en 8 phases pour la construction proprement dite | transversal : le COMMENT du développement |

> Règle de routage : **nouveau + projet** → `/project-bootstrapper` · **nouveau + pipeline** →
> `/pipeline-bootstrapper` · **reprendre l'existant** → `/project-onboarding` · **refondre l'existant** →
> `/pipeline-optimizer` · **vérifier uniquement** → `/docs-analysis` · **construire** → `/dev-cycle`.

## Combinaisons bien couplées

- `/project-onboarding` (d'abord : recenser l'existant) → `/pipeline-optimizer` (ensuite : refondre ciblé) —
  comprendre avant de rénover (couvre le principe en 6 étapes « lire d'abord, écrire ensuite »).
- `/docs-analysis` (repérer les lacunes) → `/dev-cycle` (combler les lacunes).
- `/project-bootstrapper` (ossature) → `/dev-cycle` (développer le contenu).

## Conventions communes

- Lire toujours en premier les conventions existantes du pipeline (registre, modèles, CLAUDE.md) — ne pas
  créer de standards parallèles.
- Les skills Greenfield créent, les skills existant rénovent — ne pas les mélanger.
- Lire les fichiers actifs des skills individuels avant application.

## Journal des modifications

### 0.1.0 (2026-06-17)
- Version initiale. Générée par le mode d'audit (3c1) pour la famille Projet/Pipeline.
