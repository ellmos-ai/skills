---
name: mediabrain-reader
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  Analyse les listes et métadonnées de médias indépendamment d'une application particulière.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [media, catalog, metadata, export]
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

<img src="banner.png" width="100%" alt="mediabrain-reader banner">

# Lecteur de catalogue multimédia

## Objectif

Évaluer les collections par type, statut, sujet ou doublons.

**Résultat:** Aperçu du catalogue, problèmes de qualité et suggestions de recherche ou nettoyage.

## Flux de travail

1. Clarifier l'objectif, le contexte et le format de sortie souhaité.
2. Utiliser uniquement les informations fournies dans la demande en cours.
3. Produire un résultat structuré et traçable.
4. Signaler les hypothèses et demander confirmation avant toute modification externe.

## Exemple

**Entrée:** Résume cet export JSON par type et statut.

**Résultat:** Aperçu du catalogue, problèmes de qualité et suggestions de recherche ou nettoyage.

## Noyau public et extensions privées

Ce skill public ne contient que la méthode transférable. Les adaptateurs propres aux applications, comptes, chemins locaux, bases de données et réglages personnels doivent rester dans un profil privé complémentaire ou un fork privé.

Sans profil privé, le skill utilise uniquement les informations fournies explicitement dans la demande en cours.

## Limites et protection des données

- Les données ne sont pas conservées par défaut.
- Aucune source, aucun fichier ni aucune interface n'est ouvert ou modifié sans autorisation explicite.

## Journal des modifications

### 2.0.0 (2026-07-30)

- Noyau public neutre; intégrations privées et profils personnels supprimés.
