---
name: formbuilder-reader
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  Examine les descriptions de formulaires selon leur structure, validation, clarté et accessibilité.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [forms, schema, validation, accessibility]
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

<img src="banner.png" width="100%" alt="formbuilder-reader banner">

# Lecteur de structure de formulaire

## Objectif

Analyser des formulaires JSON, YAML, CSV ou texte indépendamment d'une application.

**Résultat:** Carte des champs, risques de validation, constats d'accessibilité et améliorations.

## Flux de travail

1. Clarifier l'objectif, le contexte et le format de sortie souhaité.
2. Utiliser uniquement les informations fournies dans la demande en cours.
3. Produire un résultat structuré et traçable.
4. Signaler les hypothèses et demander confirmation avant toute modification externe.

## Exemple

**Entrée:** Examine ce formulaire JSON pour les champs obligatoires et les libellés clairs.

**Résultat:** Carte des champs, risques de validation, constats d'accessibilité et améliorations.

## Noyau public et extensions privées

Ce skill public ne contient que la méthode transférable. Les adaptateurs propres aux applications, comptes, chemins locaux, bases de données et réglages personnels doivent rester dans un profil privé complémentaire ou un fork privé.

Sans profil privé, le skill utilise uniquement les informations fournies explicitement dans la demande en cours.

## Limites et protection des données

- Les données ne sont pas conservées par défaut.
- Aucune source, aucun fichier ni aucune interface n'est ouvert ou modifié sans autorisation explicite.

## Journal des modifications

### 2.0.0 (2026-07-30)

- Noyau public neutre; intégrations privées et profils personnels supprimés.
