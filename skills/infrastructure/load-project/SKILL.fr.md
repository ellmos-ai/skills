---
name: load-project
version: 1.1.0
type: protocol
author: Claude + Codex
created: 2026-06-17
updated: 2026-07-28
description: "Au début d'une tâche de projet concrète ou lorsque le contexte n'est pas clair : résoudre l'objectif, charger la hiérarchie des règles applicable, suivre les références contraignantes et établir, avant le travail proprement dit, un rapport de situation fondé sur des preuves."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [projekt, boot, kontext, regeln, locks, orientierung, onboarding]
language: fr
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: "local-agent-skills/load-project/"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-07-28"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: ed68a6bc12f6305ac679b3e5f59590526e7ac96f05afeb08c77b00bd55bcdceb
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:32:12.564183+00:00"
---
<img src="banner.png" width="100%" alt="load-project banner">
# Charger le projet

## Objectif

Utilise cette compétence au début d'une tâche de projet concrète ou lorsque le
contexte de travail est devenu peu clair. Le but n'est pas un audit complet du
dépôt, mais le contexte minimal et fiable permettant de poursuivre le travail
en toute sécurité.

## Configuration

Cette compétence n'a pas besoin de noms de répertoires fixes. Les installations
locales peuvent définir facultativement les valeurs suivantes dans leurs règles
générales d'agent ou dans une configuration propre au projet :

- racines d'espace de travail connues,
- outils de fichiers préférés,
- noms de fichiers de démarrage ou de registre supplémentaires,
- vérificateurs de verrous,
- rôles et priorités propres au projet.

En l'absence d'une telle configuration, la compétence travaille uniquement avec
la cible indiquée et les règles de projet qui s'y trouvent.

## Déroulement

### 1. Résoudre la cible

1. Prendre comme point de départ le chemin explicite, le nom du projet ou le
   classeur de travail actuel.
2. Déterminer la racine réelle du projet ou du dépôt.
3. Restreindre les correspondances ambiguës à partir de la tâche, des documents
   racines et des limites du dépôt ; en cas d'objectifs matériellement différents,
   ne pas deviner.

### 2. Charger la hiérarchie des règles

Lire du contexte général vers le contexte spécifique :

1. règles globales d'agent et de sécurité,
2. règles de l'espace de travail ou du pipeline,
3. règles du projet et du dépôt,
4. instructions propres à la tâche.

Les règles plus spécifiques s'appliquent dans leur périmètre ; les limites de
sécurité et d'autorisation de rang supérieur demeurent.

### 3. Lire les documents racines selon leurs rôles

Les noms de fichiers sont des indications, non une norme figée. Recherche ciblée
des documents portant ces rôles :

| Rôle | Contenu typique |
|---|---|
| Entrée | Objectif, navigation, instruction de démarrage |
| Règles | Mode de travail, langue, sécurité, conventions |
| Architecture | Composants, flux de données, frontières |
| Statut | État actuel, problèmes ouverts, dernière vérification |
| Tâches | Travail suivant priorisé |
| Registre | Projets, contrôles ou publications canoniques |
| Preuves | Tests, journaux de vérification, notes de preuve |
| Passation | Travail en cours, modifications étrangères, étape suivante |

Ne charger que les rôles pertinents pour la tâche concrète.

### 4. Suivre les références contraignantes

Lorsqu'une règle lue désigne explicitement d'autres fichiers comme lecture
obligatoire, les charger de manière ciblée. Arrêter les chaînes de références dès
qu'elles n'apportent plus de contexte contraignant supplémentaire pour la tâche.

### 5. Vérifier l'état et les verrous

- Contrôler les verrous selon la politique locale : propriétaire, périmètre,
  horodatage et critère de validité ; en l'absence de règle d'obsolescence définie,
  ne jamais déclarer un verrou périmé de sa propre autorité,
- état du contrôle de version et modifications étrangères,
- processus en cours ou points de contrôle, le cas échéant,
- actualité des registres, des tests et des indications de statut.

Sauvegarder l'état initial des zones concernées avant toute modification, comme
référence de statut et de différences. Si les modifications existantes ne peuvent
pas être attribuées avec certitude, les considérer par précaution comme étrangères
et ne pas y toucher.

Traiter les instantanés comme tels et les revérifier avant les actions risquées.

### 6. Établir le rapport de situation

Avant la mise en œuvre, consigner brièvement :

```text
Ziel:
Projekt-Root:
Geltende Regeln:
Evidenzquellen:
Snapshot-Zeitpunkt:
Relevanter Ist-Zustand:
Locks oder fremde Änderungen:
Erfolgskriterium:
Nächster sicherer Schritt:
```

Ne citer les sources qu'avec le niveau de précision nécessaire à leur
vérifiabilité. Masquer les secrets, les données personnelles et les contenus
confidentiels, et ne pas les reproduire dans le rapport de situation.

Si la tâche est ainsi clairement définie et autorisée, poursuivre directement le
travail.

## Limites

- Pas de recherche de fichiers large et non bornée par défaut.
- Ne pas réinventer les règles ou registres manquants.
- Ne pas traiter un ancien message de statut comme une preuve actuelle.
- Ne pas écraser les modifications étrangères.
- Ne pas effectuer d'intégration de projet si seul le contexte d'une tâche précise
  doit être chargé.

## Journal des modifications

### 1.1.0 (2026-07-28)
- Suppression des liaisons fixes avec les utilisateurs, espaces de travail, outils
  et fournisseurs.
- Introduction de la détection des documents par rôle et d'une configuration
  locale facultative.
- Mise en œuvre opérationnelle de la validité des verrous, de la provenance des
  arbres modifiés, des preuves d'instantanés et des rapports de situation caviardés.

### 1.0.0 (2026-06-17)
- Version initiale locale.
