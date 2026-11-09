---
name: notizblock
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-11-09
description: "Utiliser pour consigner, structurer ou synthétiser des notes spontanées, idées ou fragments de texte de manière fluide (ex. 'note rapide', 'organiser mes pensées', 'synthétiser des brouillons', /notizblock). Enregistre et condense les notes brutes sans dépendance envers un outil particulier. Ne PAS utiliser pour des dossiers de recherche approfondis (utiliser assist/dossier-briefing) ou des rapports d'incidents (utiliser infrastructure/incident-notes)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [notes, capture, summarize, organize]
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


<img src="banner.png" width="100%" alt="notizblock banner">

# Assistant de notes

## Objectif

Transformer des idées libres en thèmes, tâches et décisions faciles à retrouver.

**Résultat:** Note structurée avec mots-clés, tâches et points ouverts.

## Flux de travail

1. Clarifier l'objectif, le contexte et le format de sortie souhaité.
2. Utiliser uniquement les informations fournies dans la demande en cours.
3. Produire un résultat structuré et traçable.
4. Signaler les hypothèses et demander confirmation avant toute modification externe.

## Exemple

**Entrée:** Organise ces notes de réunion par thème et prochaine action.

**Résultat:** Note structurée avec mots-clés, tâches et points ouverts.

## Noyau public et extensions privées

Ce skill public ne contient que la méthode transférable. Les adaptateurs propres aux applications, comptes, chemins locaux, bases de données et réglages personnels doivent rester dans un profil privé complémentaire ou un fork privé.

Sans profil privé, le skill utilise uniquement les informations fournies explicitement dans la demande en cours.

## Limites et protection des données

- Les données ne sont pas conservées par défaut.
- Aucune source, aucun fichier ni aucune interface n'est ouvert ou modifié sans autorisation explicite.

## Journal des modifications

### 2.0.0 (2026-07-30)

- Noyau public neutre; intégrations privées et profils personnels supprimés.
