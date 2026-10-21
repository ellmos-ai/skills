---
name: cloud-communication-protocols
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-01
updated: 2026-08-25
language: fr
visibility: public
standalone: true
anthropic_compatible: true
category: infrastructure
tags: [ping-pong, agent-beam, listeners, cross-machine, sync-yard, coordination]
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
description: "Skill parapluie pour les protocoles de communication cloud entre agents sur des machines différentes (Ping-Pong, agent-beam, Listener et protocoles futurs). À utiliser lorsque le travail est coordonné entre machines via un dossier de synchronisation partagé ou un Message-Yard."

translated_from_sha256: 9f6c20f17b3f62f11b709c05cde26d3c28b48495a60ffaa26cf96a17af27a8ce
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:46:14.369387+00:00"
---
<img src="banner.png" width="100%" alt="cloud-communication-protocols banner">

# cloud-communication-protocols

Famille de protocoles permettant à deux agents ou plus, sur des machines
différentes, de se coordonner via un dossier partagé synchronisé dans le
cloud (le "Yard") plutôt que via un canal direct. Ce skill est le
**parapluie** : il rassemble les protocoles, indique lesquels sont
éprouvés et verrouille ceux qui sont encore au stade de concept.

## Quand l'utiliser

- Le travail s'étend sur deux machines ou plus (vérification, configurations
  miroir, pilotes) et il n'existe pas de canal direct agent à agent.
- Un vocabulaire commun pour les tâches, les réponses, le rythme et
  l'escalade est nécessaire entre ces machines.

## Protocoles de cette famille

### 1. Ping-Pong (éprouvé, protocole de base)

Deux workers ou plus, avec des scans planifiés décalés, comblent la latence
de synchronisation cloud : chaque côté scanne le Yard à la recherche de
tâches qui lui sont adressées, exécute, dépose sa réponse et peut émettre
des tâches de suivi pour l'autre côté.

Règles fondamentales : écrire uniquement dans son propre créneau, fournir
des preuves pour chaque action, idempotence, aucun secret dans le Yard
(seulement des clés publiques, empreintes ou chemins), deltas d'erreur
coopératifs, vérification privilégiant la relecture par rapport au journal.

**Rythme : fréquence d'interrogation adaptative.** Le contrôle du rythme ne
fait pas partie des règles de charge utile du protocole de base, mais toute
implémentation en a besoin : un intervalle d'interrogation fixe soit inonde
un Yard vide, soit manque du travail frais. Deux mécanismes s'appliquent et
doivent tous deux être traités explicitement, sans rester implicites :

- **A — Auto-ajustement (par défaut, aucune saisie de l'opérateur ; le
  motif `cooldown`/Backoff).** Tâche nouvelle trouvée → passer
  directement à l'intervalle le plus rapide (par ex. 15 min). Exécution vide
  → refroidir selon une échelle : après 4 exécutions vides consécutives →
  30 min, après 2 de plus → 1 h, puis doubler à chaque nouvelle série vide
  (2 h, 4 h, 8 h) jusqu'à un plafond strict (24 h, jamais davantage).
  Persister le compteur de vacuité et l'intervalle courant dans un petit
  fichier d'état côté worker (et non dans la mémoire de conversation) afin
  qu'ils survivent aux redémarrages ; un changement de rythme signifie
  supprimer l'ancienne tâche planifiée et en créer une nouvelle à
  l'intervalle voulu, le compteur étant conservé. Schéma de référence
  complet, schéma du fichier d'état et autres types de boucles (rafale,
  assistance au réveil) : skill d'accompagnement **`cron-tuner`**.
- **B — Remplacement demandé par le pair.** Chaque côté peut fixer
  explicitement le rythme de l'autre dans le texte de la tâche —
  `CADENCE: match 15m` pour se synchroniser sur une fenêtre plus étroite, ou
  `CADENCE: pause 1h → 2h after 3
  empty` pour ralentir un côté lorsqu'il effectue un travail
  de fond planifiable. Celui qui modifie le rythme d'un pair confirme le
  nouvel intervalle dans le delta suivant (la relecture vaut aussi pour les
  horloges).

Les deux mécanismes ne modifient que le temps de réaction, jamais les règles
du protocole de base (discipline de créneau, preuves, absence de secrets).
Un canal réciproque `WAKE: <Grund>` autorise des scans hors cycle
comme indication, jamais comme autorité ; à supprimer après lecture.

Spécification complète et preuves de référence :
`dev-bricks/system-gap-master` → `docs/communications-protocols-skill.md`.

### 2. agent-beam (concept, verrouillé)

Pour les tâches urgentes : un paquet composé d'un prompt et d'un script de
démarrage est déposé dans le créneau cible, et un watcher sur la machine
cible lance avec lui une exécution d'agent locale — l'agent « atterrit » avec
la tâche et le script de démarrage et commence immédiatement.

Verrouillé : nécessite un contrat de confiance signé pour le script de
démarrage, une étape de quarantaine/relecture et une autorisation explicite
de l'opérateur avant toute activation.

### 3. Listener / Ear-to-Ear-Listening (concept, verrouillé)

Des watchers surveillent les déclencheurs dans le Yard (arrivées de
fichiers, fichiers drapeaux, modifications de registre) et démarrent des
agents sur l'autre machine. « Ear-to-Ear » : le listener d'un hôte observe
la boîte de réception de l'autre hôte.

Verrouillé : les règles de debouncing, les listes blanches de déclencheurs
par créneau et un contrat de sécurité sont nécessaires en premier.

## Invariants communs (tous les protocoles)

- Le Yard est un transport, jamais un espace de travail et jamais un
  coffre-fort de secrets.
- Chaque action laisse une preuve vérifiable ; « terminé » sans artefact
  n'est pas terminé.
- La gestion des erreurs est coopérative : deltas d'erreur avec hypothèse et
  contre-test, avis secondaires bienvenus.
- L'absence d'un partenaire est traitée par la règle de vacance de la
  plateforme (par ex. 48 h), et non par escalade.

## Ajouter de nouveaux protocoles

Les nouveaux protocoles rejoignent cette famille en tant que sous-chapitres
de `communications-protocols-skill.md` (d'abord au stade de concept, avec leur propre
contrat de sécurité et leurs preuves avant de passer à « éprouvé »). Les
lister ici avec une ligne chacun : nom, état (concept/pilote/éprouvé),
objectif.
