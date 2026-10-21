---
name: therapie-umbrella
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "Méta-/skill ombrelle pour la famille « Thérapie / Conseil ». Connaît tous les skills thérapeutiques (stabilisation, aperçu des méthodes, conduite de l'entretien + skills spécialisés désenregistrés) et oriente vers le skill approprié. Utilisez ce skill lorsqu'il n'est pas clair quel skill de thérapie/conseil convient, lorsqu'un aperçu des procédures disponibles est nécessaire, ou lorsqu'une situation de conseil/crise doit d'abord être située. À déclencher aussi pour « quelle méthode thérapeutique convient », « structurer un conseil », « crise — que faire », « choisir une démarche thérapeutique »."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: therapy
tags: [therapie, beratung, umbrella, meta, routing]
language: fr
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
translated_at: "2026-10-15T15:41:56.704466+00:00"
---
<img src="banner.png" width="100%" alt="therapie-umbrella banner">
# Thérapie / Conseil — Ombrelle

## Objet

Point d'entrée pour la famille « Thérapie / Conseil ». Regroupe le routage transversal et oriente
vers le skill approprié pour les cas spécifiques. Trois skills d'entrée actifs forment le front ;
derrière se trouve une longue queue de procédures spécialisées désenregistrées, accessibles via `code-skill-index`
(catalogue `catalog-therapy.md`).

## Membres & routage

| Skill | Pour quoi | Quand choisir celui-ci plutôt que les autres |
|-------|-----------|----------------------------------------------|
| `/stabilization-techniques` | Intervention de crise, ancrage, lieu sûr, RMP, panique, fenêtre de tolérance | **D'abord** en cas de détresse aiguë/crise — stabiliser avant la méthodique |
| `/guideline-therapies-overview` | Aperçu des procédures recommandées : TCC, ACT, thérapie des schémas, exposition, systémique, psychodynamique | Lorsqu'il faut choisir/expliquer la **méthode** appropriée |
| `/counseling-basics` | Conduite de l'entretien : écoute active, reflet, validation, EM/OARS, questions circulaires | Lorsqu'il s'agit du **COMMENT de l'entretien**, et non de la méthode |
| (skills spécialisés désenregistrés) | Procédures isolées (génogramme, détails de l'exposition, psychologie positive, …) | Lorsqu'une procédure isolée précise est nécessaire en profondeur → via `code-skill-index` |

> Règle de routage : crise aiguë → `/stabilization-techniques` · choisir/expliquer une méthode →
> `/guideline-therapies-overview` · technique d'entretien → `/counseling-basics` · procédure isolée en profondeur →
> skill spécialisé désenregistré via `code-skill-index`.

## Combinaisons bien couplées

- `/stabilization-techniques` (d'abord, aigu) → `/guideline-therapies-overview` (ensuite, à moyen terme) :
  établir d'abord la sécurité/la fenêtre de tolérance, puis choisir la procédure recommandée appropriée.
- `/counseling-basics` accompagne **les deux** — la posture d'entretien (EM/OARS, validation) porte
  aussi bien la stabilisation que le travail méthodique.

## Conventions communes

- Ne pas se substituer à l'établissement d'un diagnostic ; travailler de manière psychoéducative et centrée sur les ressources.
- Fenêtre de tolérance comme axe directeur : en cas de suractivation, stabiliser d'abord, ne pas confronter.
- Lire les fichiers à jour (live) des skills individuels avant application — cette ombrelle ne reproduit aucun contenu.

## Journal des modifications

### 0.1.0 (2026-06-17)
- Version initiale. Générée par le mode d'audit (1c1) pour la famille Thérapie / Conseil.
