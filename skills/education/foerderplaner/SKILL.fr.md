---
name: foerderplaner
version: 2.0.0
type: skill
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  Planifie l'enseignement, les activités et le soutien individuel sans générateur de rapports ni modèles personnels.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: education
tags: [education, support, lesson-planning, differentiation]
language: fr
status: stable
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: public-neutral
  origin_license: MIT
  notes: Public core only; adapters and private profiles are excluded.
---

# Planificateur d'enseignement et de soutien

## Objectif

Transformer la situation initiale et l'objectif en étapes concrètes et évaluables.

**Résultat:** Objectifs, mesures, différenciation, critères d'observation et dates de révision.

## Flux de travail

1. Clarifier l'objectif, le contexte et le format de sortie souhaité.
2. Utiliser uniquement les informations fournies dans la demande en cours.
3. Produire un résultat structuré et traçable.
4. Signaler les hypothèses et demander confirmation avant toute modification externe.

## Exemple

**Entrée:** Planifie quatre semaines de soutien à la compréhension pour un groupe anonymisé.

**Résultat:** Objectifs, mesures, différenciation, critères d'observation et dates de révision.

## Noyau public et extensions privées

Ce skill public ne contient que la méthode transférable. Les adaptateurs propres aux applications, comptes, chemins locaux, bases de données et réglages personnels doivent rester dans un profil privé complémentaire ou un fork privé.

Sans profil privé, le skill utilise uniquement les informations fournies explicitement dans la demande en cours.

## Limites et protection des données

- Les données ne sont pas conservées par défaut.
- Aucune source, aucun fichier ni aucune interface n'est ouvert ou modifié sans autorisation explicite.
- Le skill ne crée ni rapports de soutien, ni certificats, ni évaluations officielles. Les rapports généraux peuvent être produits séparément avec `report-forge`; les modèles personnels restent privés.

## Journal des modifications

### 2.0.0 (2026-07-30)

- Noyau public neutre; intégrations privées et profils personnels supprimés.
