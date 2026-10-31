---
name: iterative-bundle-selection
version: 1.2.0
type: skill
author: Lukas Geiger
created: 2026-08-25
updated: 2026-08-25
description: "Réduire progressivement de grandes listes de candidats grâce à des bassins thématiques facultatifs, des niveaux de filtrage et des lots remélangés à plusieurs reprises. À utiliser lorsque l'utilisateur souhaite sélectionner par groupes des compétences, des tâches, des idées, des fichiers ou d'autres entrées, les filtrer selon des caractéristiques, ou ne les mélanger qu'au sein de domaines thématiques communs, sans rejeter définitivement les autres entrées."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [entscheidung, auswahl, datenreduktion, buendel, choice-overload, workflow]
language: fr
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'local_changes_since_sync': True}
translated_from_sha256: 947358cbebcf01dc7e4e4d15c4cf25da6fe10d5454a7e8fc0aa03788bf88f70f
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.284360+00:00"
---
<img src="banner.png" width="100%" alt="iterative-bundle-selection banner">

# Sélection itérative par lots

Réduire de grands ensembles de sélection à l'aide de peu de décisions globales, sans écarter prématurément les candidats non choisis.

## Principe de base

1. Recenser tous les candidats dans un pool commun et les nommer de façon univoque.
2. Définir facultativement des bassins thématiques et attribuer chaque candidat à exactement un bassin principal.
3. Appliquer les filtres souhaités l'un après l'autre, globalement ou au sein de bassins individuels, et conserver leurs résultats séparément.
4. Mélanger au sein de chaque bassin actif et former par défaut des lots de cinq candidats.
5. Étiqueter les lots du premier tour de façon univoque par bassin avec `THEMA-A`, `THEMA-B` …
6. Laisser l'utilisateur choisir des lots entiers.
7. Retirer les lots sélectionnés du pool ouvert et les transmettre à l'action suivante.
8. Rendre les candidats des lots non choisis à leur bassin respectif.
9. Conserver les bassins et les filtres, remélanger séparément chaque bassin et utiliser des étiquettes à tirets.
10. Poursuivre les tours suivants jusqu'à ce que l'utilisateur arrête ou que le pool soit vide.

Un dernier lot peut comporter moins de cinq candidats. Les lots non choisis signifient « encore ouvert », et non « rejeté ».

## Déroulement

### 1. Préparer le pool

- Supprimer les doublons à l'aide de noms ou d'identifiants stables.
- Exclure les candidats déjà sélectionnés ou terminés.
- Signaler les candidats bloqués, sans les supprimer silencieusement.
- Indiquer la taille du pool de départ.

### 2. Constituer les bassins thématiques

Un bassin thématique est un sous-pool délimité. Les candidats de bassins différents ne sont pas mélangés entre eux.

- N'utiliser cette méthode que si l'utilisateur demande des bassins thématiques ou si une séparation thématique paraît expressément pertinente.
- Documenter les bassins avec un identifiant stable, un titre, une règle d'attribution et le nombre de candidats.
- Dériver les bassins des consignes de l'utilisateur, des catégories existantes ou de caractéristiques vérifiables.
- Présenter de manière transparente les attributions déduites automatiquement avant la première action suivante.
- Attribuer par défaut chaque candidat à exactement un bassin principal ; ne pas créer de doublons silencieux dans plusieurs bassins.
- Conserver les candidats ambigus dans `UNZU — Unzugeordnet` jusqu'à ce qu'une attribution soit établie.
- Restituer un bassin de moins de cinq candidats comme petit lot ; ne jamais le compléter avec un autre thème.
- Les filtres peuvent s'appliquer globalement à tous les bassins ou localement à un bassin nommé.
- Les candidats filtrés conservent leur attribution de bassin afin de revenir au bon endroit lors de leur réactivation.
- Lors du partage, de la fusion ou du renommage d'un bassin, n'annuler et reformer que les lots concernés.

Exemple :

```text
DEV  | Entwicklung     | 12 Kandidaten | DEV-A, DEV-B, DEV-C
MED  | Medien          |  7 Kandidaten | MED-A, MED-B
UNZU | Unzugeordnet    |  2 Kandidaten | UNZU-A
```

Dans les tours suivants, indiquer la profondeur du tour par la lettre du lot : `DEV-A′`, `MED-B″`.

### 3. Appliquer les niveaux de filtrage

- Exécuter les filtres facultativement et dans l'ordre indiqué par l'utilisateur.
- Journaliser chaque filtre avec un identifiant stable, son mode, sa règle et son nombre de résultats.
- Effectuer les comparaisons de texte par défaut sans tenir compte de la casse.
- `exclude` retire les résultats du seul pool actif et les place dans le pool filtré.
- `include` ne conserve que les résultats dans le pool actif ; les non-résultats passent dans le pool filtré.
- Si aucun mode n'est indiqué et que l'utilisateur demande de filtrer ou d'épurer le pool, utiliser `exclude` et indiquer cette hypothèse.
- Après chaque niveau, indiquer la taille d'entrée, le nombre de résultats et la taille restante.
- Ne jamais supprimer les candidats filtrés ni les marquer comme rejetés ; l'utilisateur peut désactiver ultérieurement certains filtres.

Exemple :

```text
F1 | exclude | Name enthält "aws"         | 13 Treffer
F2 | exclude | Name enthält "hyperframes" | 8 Treffer
Aktiver Pool: 44 | Filterpool: 21
```

Si un filtre change, annuler tous les lots existants du pool actif avant de remélanger.

### 4. Former le tour

- Remélanger réellement les candidats ; ne pas se contenter de renommer l'ancienne structure en lots.
- Utiliser autant que possible cinq candidats par lot.
- Ne mélanger ensemble que les candidats d'un même bassin thématique.
- Ne dupliquer ni ne perdre aucun candidat.
- Pour les candidats dépendant fonctionnellement les uns des autres, signaler la dépendance au lieu de la taire.

Format de sortie :

```text
Bündel DEV-A: dev-1, dev-2, dev-3, dev-4, dev-5
Bündel MED-A: media-1, media-2, media-3
```

Sans bassins thématiques, continuer à utiliser les étiquettes simples `A`, `B`, `C` …

### 5. Traiter la sélection

- Accepter des réponses telles que `A, D und F`.
- Avant une action suivante, énumérer à nouveau intégralement les candidats contenus.
- Vérifier pour chaque candidat les verrous, prérequis ou essais à blanc nécessaires.
- Journaliser les candidats réussis comme sélectionnés ou terminés.
- Rendre au pool restant les candidats bloqués ou en échec.

### 6. Regrouper le pool restant

- Ne retirer définitivement que les candidats effectivement réussis.
- Rendre tous les autres candidats à leurs bassins précédents et les y remélanger séparément.
- Réappliquer les filtres actifs au pool restant avant chaque nouveau mélange.
- Marquer le tour suivant par des étiquettes à tirets : `DEV-A′`, puis `DEV-A″`, etc.
- Indiquer le pool total, le pool filtré, la taille du pool actif ainsi que la taille de chaque bassin.

## Règles de protection

- Ne jamais interpréter la non-sélection comme un rejet définitif.
- Ne jamais écarter silencieusement les résultats de filtre ; ils restent récupérables dans le pool filtré.
- Ne jamais franchir les limites des bassins lors du mélange.
- Ne pas dupliquer les candidats ni les déplacer entre bassins lors de la redistribution, sauf si l'utilisateur modifie la répartition.
- Ne perdre aucun candidat en raison d'une combinaison de lots défavorable.
- Ne pas forcer les candidats bloqués ; ils restent ouverts.
- Pour les actions suivantes irréversibles ou risquées, faire confirmer d'abord chaque candidat individuellement.
- Si nécessaire, documenter une clé de mélange reproductible ; sinon, une répartition nouvelle et traçable suffit.
- La méthode réduit la complexité de la sélection, mais ne remplace pas l'évaluation métier de chaque candidat.

## Délimitation

- `decide` évalue une décision concrète à l'aide de critères et de cadres d'analyse.
- `decision-briefing` coordonne plusieurs questions de décision différentes.
- `iterative-bundle-selection` réduit un grand pool de candidats de même nature par des choix groupés répétés et un remélange.

## Conclusion

La méthode prend fin lorsque le pool est vide, que l'utilisateur arrête expressément ou qu'il ne reste plus que des candidats nécessitant une décision individuelle. Fournir alors un bref bilan avec les éléments sélectionnés, ouverts et bloqués.

## Journal des modifications

### 1.2.0 (2026-08-25)

- Ajout de bassins thématiques facultatifs comme diviseurs du pool.
- Définition du mélange lié aux bassins, des filtres locaux, des étiquettes univoques de lots et du traitement de `UNZU`.

### 1.1.0 (2026-08-25)

- Ajout de niveaux de filtrage réversibles `include` et `exclude` avant le remélange.
- Définition du journal de filtrage, du pool filtré et du recalcul des lots existants.

### 1.0.0 (2026-08-25)

- Consignation des lots itératifs de cinq, des tours à tirets, du pool restant et du retour des éléments bloqués comme procédure autonome de réduction de données et de décision.
