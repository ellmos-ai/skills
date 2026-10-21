---
name: condition
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-25
updated: 2026-07-28
description: "Langage de conditions flexible pour objectifs, prompts et missions. Traduit les conditions, les moments et les dépendances d'ordre en portes vérifiables, afin qu'une sous-étape ne soit exécutée qu'après une autorisation attestée. Toujours utiliser pour /condition, /if, /if-only, /when, /after, /and ou /or, ainsi que pour des formulations comme « seulement quand », « dès que », « uniquement si », « après que », « attends que », « ensuite » ou « pas avant ». Également utiliser lorsque plusieurs sous-objectifs dépendent les uns des autres ou qu'un objectif contient une autorisation ultérieure."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [condition, gate, prompt-language, goal, trigger, blocker, timing, dependency, workflow]
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
  origin_path: "condition/SKILL.md"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-07-28"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: d12d1a078138495fee061d4564ba1bc1e486e088023421c05cf21055a844a9c0
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.304476+00:00"
---
<img src="banner.png" width="100%" alt="condition banner">
# condition — Langage de conditions pour objectifs et prompts

## Idée directrice

Les conditions en texte libre sont faciles à manquer. C'est pourquoi chaque condition pertinente doit être traduite en une porte nommée et vérifiable :

> Généreux à la lecture, intransigeant à la preuve.

La saisie peut être en langage naturel et incomplète. La traduction interne doit en revanche établir clairement :

1. quelle condition doit être remplie,
2. quelle sous-étape est bloquée,
3. quelle requête d'outil fait office de preuve,
4. si la non-satisfaction signifie un retard ou une interdiction.

Ne bloquer que la sous-étape concernée. Poursuivre le travail indépendant.

## Éléments de langage

| Expression | Sémantique | Exemple |
| --- | --- | --- |
| `/condition <Bedingung> -> <Schritt>` | Porte canonique | `/condition Tests grün -> Release bauen` |
| `/if <Bedingung> -> <Schritt>` | Synonyme de `/condition` | `/if Review abgeschlossen -> mergen` |
| `/when <Bedingung> -> <Schritt>` | Exécuter dès que la condition survient | `/when Export fertig -> Bericht prüfen` |
| `/if-only <Bedingung> -> <Schritt>` | Seulement en cas de satisfaction ; sinon ne pas exécuter du tout | `/if-only Backup belegt -> Altbestand löschen` |
| `/after <Dauer> -> <Schritt>` | Décalage temporel à partir du moment de la définition | `/after 30 minutes -> Status prüfen` |
| `/and` | Toutes les conditions liées doivent être valides | `/if Tests grün /and Review da -> mergen` |
| `/or` | Une seule condition suffit | `/if Freigabe da /or Notfallregel aktiv -> starten` |

Utiliser des conditions numérotées comme `/condition 1 ...` et `/condition 2 ...` lorsqu'un prompt contient
plusieurs portes. En cas de mélange de `/and` et `/or`, ne pas inventer de priorité
implicite entre opérateurs : utiliser des parenthèses ou des sous-conditions numérotées. Si le sens reste
ambigu, demander avant d'autoriser une étape risquée.

Traiter `/if-only` comme une interdiction. Si la condition ne peut pas être prouvée, ne pas exécuter
l'étape. En cas de formulation peu claire et de conséquences irréversibles, choisir la lecture la plus stricte.

## Déroulement

### 1. Normaliser la condition

Traduire la saisie en une phrase vérifiable. Convertir les temps relatifs en un moment absolu avec fuseau
horaire au moment de la définition.

| Saisie | Condition normalisée | Classe de preuve |
| --- | --- | --- |
| `time 06:00` | L'heure système est au moins 06:00 dans le fuseau convenu | Outil d'horloge/temps |
| `after 2 hours` | L'heure système est au moins le moment de définition plus deux heures | Outil d'horloge/temps |
| `wenn Worker A fertig ist` | L'artefact de réception ou l'état de la tâche A indique l'achèvement | Outil de tâche/fichier |
| `wenn Tests grün sind` | La série de tests prescrite se termine avec succès | Outil de processus/test |
| `nach dem Push` | Le dépôt distant cible contient le commit prévu | Outil de contrôle de version |
| `wenn der User zustimmt` | Un accord explicite figure dans la conversation | Saisie de l'utilisateur |

Si aucune voie de preuve objective n'est identifiable, le signaler ouvertement. Ne formuler aucune porte qui ne
pourrait être fermée que par supposition.

### 2. Consigner l'état de la porte

Si un magasin persistant de portes, de tâches ou de mémoire est disponible, y enregistrer au minimum ces
champs :

```text
id
condition
blocks
mode = wait | only
proof_method
status = open | met | dropped
created_at
evidence
```

Si aucun magasin persistant n'existe, tenir l'état visiblement dans l'objectif courant, le plan de tâches ou le
document de passation. N'affirmer qu'une porte survit aux sessions que si le stockage utilisé est réellement
durable.

Un adaptateur d'exécution existant peut utiliser d'autres noms de commandes. Fonctionnellement, il lui faut :
`open`, `list`, `meet` et `drop`, ou des opérations équivalentes.

### 3. Réordonner le travail

Une porte ouverte ne bloque pas toute la mission. Exécuter toutes les étapes indépendantes et revérifier l'état
de la porte avant toute étape dépendante.

Ne pas interroger activement en boucles courtes d'agent. Pour les attentes longues, utiliser un planificateur,
une tâche en arrière-plan ou un événement qui signale une seule fois à son occurrence. Après le signal de
réveil, vérifier néanmoins la condition elle-même avec l'outil prévu.

### 4. Vérifier strictement et fermer

Exécuter d'abord la requête d'outil, puis fermer la porte avec une preuve concrète. Exemples de preuves
appropriées :

- Temps : horodatage mesuré avec fuseau horaire,
- Fichier : chemin, métadonnées ou empreinte du artefact attendu,
- Tests : commande exécutée, code de sortie et résumé pertinent,
- Dépôt : branche, identifiant de commit et comparaison avec le distant,
- Processus ou tâche : identifiant stable et état final mesuré,
- Accord : réponse explicite de l'utilisateur dans le contexte actuel.

Une estimation, un état supposé ou la simple affirmation d'un autre worker ne suffisent pas lorsqu'une preuve
indépendante devrait être disponible.

Si une modification de la mission rend une porte caduque, la marquer comme `dropped` avec une justification.
Pour `/or`, fermer ou abandonner également les alternatives devenues inutiles afin qu'aucune
porte zombie ne subsiste.

### 5. Escalader

Lorsque toutes les étapes indépendantes sont terminées :

1. vérifier si le travail préalable bloquant peut être accompli activement dans le cadre de la mission,
2. si la condition est purement une attente, utiliser un planificateur ou une tâche de fond adaptée,
3. en cas de décision de l'utilisateur ou de dépendance externe, transmettre avec la porte ouverte et un état
   intermédiaire clair.

Ne déduire aucune autorisation supplémentaire d'une condition. Une porte satisfaite ne modifie que l'ordre ; elle
n'élargit pas le périmètre autorisé de la mission.

## Exemples

### Objectif avec condition temporelle

```text
Ziel: Daten prüfen und Bericht veröffentlichen.
/condition time 16:00 Europe/Berlin -> Veröffentlichung starten
```

La vérification des données peut avoir lieu avant. La publication reste bloquée tant qu'une requête d'heure
actuelle n'atteste pas au moins 16:00.

### Prompt avec plusieurs conditions

```text
/condition 1 Tests erfolgreich
/condition 2 Review freigegeben
/if condition 1 /and condition 2 -> mergen
```

Vérifier les deux portes séparément. Ensuite seulement fusionner.

### Interdiction plutôt que retard

```text
/if-only verifiziertes Backup vorhanden -> alte Dateien löschen
```

Sans sauvegarde attestée, ne rien supprimer et mentionner l'interdiction ouverte dans le rapport final.

## Pièges

- Répéter la condition seulement dans le texte au lieu de la tenir comme état.
- Mettre en pause tout un objectif alors qu'une seule sous-étape est bloquée.
- Enregistrer un temps relatif sans moment de définition ni fuseau horaire.
- Remplacer une preuve d'outil par une supposition ou une auto-déclaration.
- Traiter `/if-only` comme une simple attente.
- Laisser ouvertes des portes alternatives devenues inutiles après `/or`.
- Intégrer des noms de fournisseur, de modèle, d'utilisateur ou d'hôte dans la mécanique générale.
- Traiter un chemin d'exécution local comme un prérequis du langage lui-même.

## Journal des modifications

### 1.1.0 (2026-07-28)

- Formulé de manière neutre vis-à-vis du fournisseur, de l'utilisateur et du système pour les environnements
  d'exécution de compétences partagés.
- Utilisation dans les objectifs et les prompts rendue explicite.
- Environnement d'exécution décrit comme un adaptateur interchangeable ; chemins locaux fixes et noms de modèles supprimés.
- Clarifié les liaisons ambiguës `/and`/`/or`, les états persistants et les limites d'autorisation.

### 1.0.0 (2026-07-25)

- Première version avec `/condition`, `/if`, `/if-only`, `/when`, `/after`, `/and` et `/or`.
