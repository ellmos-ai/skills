---
name: decision-avatar
version: 1.0.0
type: protocol
author: Claude + Codex
created: 2026-07-28
updated: 2026-07-28
description: "En présence d'un profil de décision local et explicitement autorisé : prédire des décisions récurrentes à partir de retours documentés, calibrer la confiance et séparer strictement la prédiction, la décision et l'exécution."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [entscheidung, avatar, theory-of-mind, feedback, konfidenz, provenance]
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
  origin_path: "private decision-avatar profile (not published)"
  origin_version: "1.2.0"
  origin_repo: null
  last_sync_from_origin: "2026-07-28"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: f8f1e1078180113ac0e75055f001fe4d080762ce53c2245d7798ee885f90e570
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:32:13.145691+00:00"
---
<img src="banner.png" width="100%" alt="decision-avatar banner">
# Avatar de décision

## Objectif

Cette compétence ne reproduit pas une personne. Elle fournit une procédure vérifiable
permettant de dériver, pour des types de décisions récurrents, une préférence probable
à partir de preuves réelles et autorisées.

Utilise-la uniquement lorsqu'un profil de décision local existe et que son utilisation
est admissible pour la tâche en cours. Sans profil, la compétence ne fournit aucune
décision par procuration.

L'utilisation n'est réputée autorisée que si la mission, la règle applicable à l'agent
ou les métadonnées du profil autorisent explicitement le but actuel. La simple
accessibilité d'un fichier de profil ne vaut pas consentement.

## Principes fondamentaux

1. **La preuve prime sur la supposition.** Les déclarations directes et les décisions
   confirmées pèsent plus lourd que les schémas déduits.
2. **Une prédiction n'est pas une déclaration de la personne.** Les sorties de l'agent
   ne doivent pas être réintégrées dans le profil comme de nouvelles preuves primaires.
3. **Décider n'est pas exécuter.** Une recommandation peut être déterminée alors que
   sa mise en œuvre exige une autorité supplémentaire.
4. **Un silence d'approbation n'est pas un retour.** L'absence d'objection ne confirme
   aucune prédiction.
5. **Les profils restent locaux et privés.** Aucune donnée personnelle, aucun secret
   ni contenu sensible ne doit être repris dans des fichiers de compétence partagés.

## Modèle de profil portable

Les noms de fichiers sont configurables librement ; seuls ces rôles sont nécessaires :

| Rôle | Contenu |
|---|---|
| Méthodologie | niveaux de preuve, protection des données et règles de calibrage |
| Préférences documentées | déclarations directes et décisions confirmées |
| Hypothèses | règles déduites avec confiance et sources |
| Actions | actes accomplis sur la base d'une prédiction |
| Retour | confirmation, correction ou rejet par la personne |

Les décisions récentes et liées au projet prévalent sur les préférences générales.

Chaque preuve utilisée devrait comporter au minimum :

```text
Quellen-ID:
Datum:
Entscheidungstyp und Gültigkeitsbereich:
Status: bestätigt/korrigiert/widerrufen
Gültig bis: <optional>
```

Ne pas utiliser de preuves révoquées, expirées ou hors de leur périmètre de validité.
En cas de preuves confirmées contradictoires, la preuve la plus spécifique l'emporte
d'abord, puis la plus récente. Si le conflit persiste, fixer la confiance à « faible »
et escalader.

## Boucle de décision

### 0. Vérifier la règle locale prioritaire

S'il existe pour le projet en cours ou le type de décision concerné une règle confirmée,
utilise-la et documente sa source.

### 1. Rechercher des preuves réelles

N'utiliser que des preuves admissibles selon la méthodologie locale. Les listes de tâches,
journaux d'agent, réponses antérieures de l'avatar et arguments de la session en cours ne
sont pas des déclarations de la personne.

### 2. Former la prédiction

Toujours présenter le résultat avec sa justification et l'un des trois niveaux suivants :

- **élevé :** plusieurs preuves directes, cohérentes et pertinentes,
- **moyen :** schéma plausible avec preuve limitée ou indirecte,
- **faible :** situation inédite, preuves contradictoires ou absence de schéma fiable.

Les décisions lourdes de conséquences ne sont pas automatiquement « faibles ». La confiance
mesure la preuve de la préférence, non l'étendue de l'exécution ultérieure.

### 3. Séparer les modes

| Mode | Résultat | Effet de bord |
|---|---|---|
| Prédire | position probable + preuves + confiance | aucun |
| Décider | choix concret + justification + confiance | aucun |
| Agir | mise en œuvre autorisée et sûre + journal d'actions | possible |

En mode action, les règles d'autorité et de sécurité de l'environnement d'exécution
s'appliquent en outre. Une faible confiance ou l'absence de pouvoir d'exécution conduit à
une escalade, non à une exécution silencieuse.

### 4. Calibrer à partir du retour

Après un retour réel :

1. Marquer la prédiction comme confirmée, corrigée ou rejetée.
2. Éventuellement recueillir une échelle d'évaluation.
3. Noter la différence entre erreur de direction et erreur de périmètre.
4. Ajuster l'hypothèse et la confiance.
5. Ne reporter dans les préférences documentées que les retours réels.

## Format de sortie

```text
Entscheidungstyp:
Modus:
Wahrscheinliche Präferenz:
Konfidenz:
Zulässige Belege:
Gegenbelege oder Unsicherheit:
Ausführung autorisiert: ja/nein
Nächster Schritt:
```

Dans les sorties, ne mentionner que les identifiants de sources caveardés et le résumé de
preuve nécessaire à la décision. Ne reproduire ni déclarations privées, ni chemins absolus
de profil, ni données brutes sensibles.

## Limites

- Aucun diagnostic ni affirmation sur les états internes d'une personne.
- Aucune utilisation d'un profil hors de son but autorisé.
- Aucune reprise automatique d'hypothèses de l'agent comme connaissances de la personne.
- Aucune exécution fondée uniquement sur une prédiction lorsqu'une nouvelle autorité serait requise.

## Journal des modifications

### 1.0.0 (2026-07-28)
- Extraction de la précognition de retour, de la calibration de confiance et de la séparation
  de provenance, à partir d'une configuration personnelle d'avatar, sous forme de protocole
  autonome et portable.
- Opérationnalisation de l'autorisation, du cycle de vie des preuves, de la résolution des
  conflits et de la sortie caveardée.
