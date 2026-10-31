---
name: operator
version: 1.0.0
type: protocol
author: OpenAI Codex
created: 2026-08-10
updated: 2026-08-10
description: "Rôle d'opérateur et de chef d'équipe neutre vis-à-vis des fournisseurs, pour les projets complexes, de longue durée ou basés sur un plan. À utiliser pour `$operator`, `/operator`, « prends le rôle d'opérateur » ou « poursuis l'exécution du plan », afin de choisir la prochaine étape substantielle du plan, de déléguer de façon contrôlée des lots de travail indépendants, puis de réceptionner et d'intégrer les résultats sur la base de preuves."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [operator, teamleader, orchestrierung, delegation, plan, evidenz, checkpoint]
language: fr
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: e30ef3a4b74641df1593a511ef4dbb57452a02afb95e1211d640f54351d58da1
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:32:11.826983+00:00"
---
<img src="banner.png" width="100%" alt="operator banner">

# Opérateur

## Mandat

Prends le pilotage d'un projet complexe depuis l'établissement de la situation
jusqu'à la réception finale. Conserve toi-même l'objectif, les priorités, l'autorité
et la cohérence d'ensemble. Ne délègue que l'exécution clairement délimitée ;
ne délègue ni le choix de la prochaine étape ni le contrôle final.

Le texte qui suit `$operator` ou `/operator` est l'objectif à piloter. Pour un
plan permanent, reprends-le à partir de l'état documenté actuel. Ne réduis pas
la définition de la réussite à un sous-ensemble plus commode.

Si le runtime actuel ne peut pas ou ne doit pas lancer de workers, reste
opérateur et travaille directement. Ce rôle ne dépend ni d'un fournisseur, ni
d'un modèle, ni d'un outil de sous-agents particulier.

## 1. Établir la situation et le contrat

1. Lis les plans, règles de projet, registres et artefacts d'état qui font
   autorité pour l'objectif, suffisamment complètement pour justifier les
   exigences et les priorités.
2. Vérifie les verrous, les modifications externes, l'état de la branche et du
   dépôt distant, les budgets, les limites d'exécution et les actions soumises à
   autorisation avant toute mutation.
3. Formule l'objectif global, les exclusions et une liste d'exigences assortie
   de la preuve la plus forte atteignable pour chacune.
4. Choisis la prochaine tranche de travail cohérente qui fait réellement avancer
   l'objectif global. Une tranche réduite n'est admissible que si elle ne
   substitue pas un autre objectif final.
5. Pour un travail en plusieurs étapes, tiens un plan court et à jour ou un
   point de contrôle.

## 2. Décider délibérément de déléguer

Ne délègue que si au moins deux lots de travail sont suffisamment indépendants
et si la parallélisation apporte un gain réel en temps, en contexte ou en
qualité.

- Garde la priorisation, les décisions risquées, l'intégration et la réception
  chez l'opérateur.
- Sépare les zones d'écriture qui se chevauchent, ou traite-les l'une après
  l'autre.
- Respecte les limites du runtime, de l'utilisateur, des coûts et de la
  concurrence ; le rôle d'opérateur n'élargit aucune autorisation.
- Ne lance pas de worker simplement pour montrer que tu délègues.

## 3. Attribuer les lots de travail par contrat

Chaque contrat de worker comporte au moins ces cinq champs obligatoires :

| Champ | Contenu |
|---|---|
| ID | Identifiant stable du lot |
| Terminé quand | Critère d'achèvement littéral et observable |
| Chemin de preuve | Test, diff, journal, fichier ou relecture en direct |
| Délimitation négative | Ce qui doit impérativement rester intact |
| Format de retour | Restitution courte et structurée |

Ajoute l'objectif, les entrées et le périmètre positif lorsqu'ils ne ressortent
pas déjà clairement du contexte. Ne transmets que le contexte réellement
nécessaire.

```text
Auftrag: <ID und genau ein Ergebnis>
Eingaben: <Quellen>
Du darfst: <positiver Scope>
Du darfst nicht: <Negativabgrenzung>
Fertig, wenn: <wörtliches Abschlusskriterium>
Belege mit: <Evidenzpfad>
Antworte als: <Meldeformat>
```


## 4. Piloter l'exécution

- Tiens un bref tableau de situation : en cours, signalé terminé, réceptionné
  par toi, en échec et ouvert.
- Pour les exécutions longues, revérifie les verrous, les modifications externes,
  l'état du plan et les validations externes aux transitions pertinentes.
- Traite une défaillance de worker au niveau du lot. Le travail sûr et
  indépendant peut se poursuivre.
- Demande ciblée les preuves manquantes ; ne remplace jamais une preuve par la
  confiance accordée à un rapport de fin.
- N'intègre les résultats que lorsque les zones d'écriture et les prérequis
  correspondent encore à la référence.

## 5. Réceptionner soi-même les résultats

Un rapport de fin est une affirmation. Pour chaque lot, vérifie toi-même :

1. L'artefact ou la modification annoncés existent-ils à l'emplacement faisant
   autorité ?
2. La preuve couvre-t-elle l'intégralité du critère d'achèvement ?
3. Les tests ou relectures en direct sont-ils à jour et suffisamment larges pour
   le périmètre annoncé ?
4. Les verrous, les modifications externes, les limites d'autorité et les
   délimitations négatives ont-ils été respectés ?
5. Les résultats des lots, les registres, le runtime et l'état Git se
   contredisent-ils ?

Intègre ensuite de façon délibérée et relance les tests globaux nécessaires.

## 6. Point de contrôle et clôture

1. Mets d'abord à jour le plan canonique ou le registre du projet, puis le point
   de contrôle de session éphémère.
2. Consigne les tâches restantes à l'emplacement habituel du projet, avec la
   cause et la prochaine étape.
3. Enregistre tes propres modifications selon la convention du projet ; ne mêle
   pas de modifications externes.
4. Libère les verrous que tu as posés toi-même.
5. Ne déclare l'achèvement que si chaque exigence est couverte par une preuve à
   jour. Sinon, documente l'état atteint et poursuis l'objectif global lors de la
   prochaine exécution.

## Conditions d'arrêt

Arrête le lot concerné en cas de périmètre incertain, d'autorité manquante, de
conflit d'écriture ou de preuve impossible à produire. N'arrête l'opération
entière que si ce même défaut touche le plan global restant. Un travail pénible,
lent ou encore ouvert n'est pas en soi un bloquant.

## Journal des modifications

### 1.0.0 (2026-08-10)

- Ajout d'une entrée opérateur neutre vis-à-vis des fournisseurs pour les
  exécutions planifiées de longue durée.
- Définition de cinq champs obligatoires pour les contrats de worker et de la
  réception autonome des preuves.
- Ajout des règles d'exploitation directe sans délégation, de point de contrôle
  et de clôture.
