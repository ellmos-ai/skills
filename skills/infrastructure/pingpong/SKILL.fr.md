---
name: pingpong
version: 1.1.0
type: protocol
author: Lukas Geiger, OpenAI Codex
created: 2026-08-03
updated: 2026-09-13
description: "Fait fonctionner une station radio limitée dans le temps et liée à une session, via un dossier partagé et synchronisé. ListenSync analyse systématiquement les demandes et les nouveautés ; WriteSync envoie les deltas et les accusés de réception. À utiliser pour PingPong, téléphone à ficelle, ListenSync, WriteSync, écouteur de synchronisation, veille des tâches, analyse des nouveautés ou surveillance de Goal/Loop."
# Kompatibilität
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: infrastructure
tags: [pingpong, sync, listener, goal, loop, cadence, filecommander]
language: fr
status: active
visibility: public

# Abhängigkeiten
dependencies:
  tools: [ellmos-filecommander]
  services: []
  protocols: [shared-folder-sync]
  python: []

roles:
  - id: pingpong
    label: PingPong
    prompt: skills/infrastructure/pingpong/SKILL.en.md
    request: Read and follow the PingPong protocol for the requested mode and duration.
    modes: [ListenSync, WriteSync]
    providers: [codex, claude]

# Provenance
provenance:
  origin: "custom"
  origin_path: "local-skill/pingpong"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-08-04"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 6f644ddfdc91c21a6250f7af08b78211b2949ad989b2e2f9104d71bed1ef062b
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:46:14.384972+00:00"
---
<img src="banner.png" width="100%" alt="pingpong banner">

# PingPong

Faites fonctionner deux systèmes ou plus comme stations radio via un dossier de synchronisation commun. Gardez le contrat fonctionnel indépendant du fournisseur ; seul l'adaptateur de poursuite diffère.

## Déterminer le mode

- ListenSync : Exactement un écouteur systématique par hôte. Il analyse, prend en charge les demandes pertinentes et exécute également WriteSync pour les réponses.
- WriteSync : Chaque acteur en activité peut envoyer ses propres deltas, demandes, nouveautés et accusés de réception pertinents. Ce mode ne démarre aucun écouteur.
- Si le mode est absent, utilisez ListenSync.

## Clarifier la participation (STATE et CALL)

Avant le contrat d'exécution, la vérification en deux étapes détermine si quelqu'un peut être joint. `scripts/pingpong_runtime.py check --slot <slot> --sync-root <pfad>` répond avec exactement trois valeurs : Exit 0 `call-for-me` (activer et lancer un agent), Exit 1 `idle` (je suis moi-même actif, désactiver), Exit 3 `check-failed` (illisible, ne jamais le traiter comme une inactivité). La participation exige STATE et CALL en même temps ; celui qui lance un Call y met fin une fois son but atteint, sinon il expire. Règles complètes dans references/protocol.md.

## Définir le contrat d'exécution

1. Utilisez 24h par défaut. Acceptez aussi des durées relatives comme 15m, 2h, 3d ou un instant de fin absolu au format ISO 8601.
2. Mesurez l'heure locale de départ et indiquez expires_at avec la date, l'heure et le fuseau horaire.
3. Commencez avec 15 minutes. Utilisez la cadence de references/protocol.md, sauf si l'utilisateur exige une cadence fixe.
4. Définissez l'atteinte du but ainsi : heure de fin atteinte, analyse finale FileCommander attestée, toutes les entrées pertinentes détectées jusque-là traitées ou bloquées et documentées précisément, state mis à jour et propre planificateur arrêté.
5. N'affirmez ni analyse ni atteinte du but sans preuve FileCommander.

## Utiliser les adaptateurs de fournisseur

### Codex

Créez explicitement, avant la première analyse, un Goal persistant avec le contrat d'exécution complet et expires_at. Traitez exactement un cycle d'analyse complet par poursuite. Ne terminez pas le Goal après un cycle isolé vide ou réussi. Attendez ensuite réellement jusqu'à next_scan_at, par exemple avec :

    python "<skill-root>/scripts/pingpong_runtime.py" wait --until "<next_scan_at>"

Exécutez le cycle de clôture à l'heure d'expiration. Ne marquez le Goal comme terminé que si le critère de réussite est rempli.

### Claude Code

Lancez la tâche sous la forme /loop <Kadenz> $pingpong. Si la compétence provient déjà d'une exécution planifiée, ne créez pas de deuxième boucle. Pour changer la cadence, remplacez uniquement sa propre tâche Cron. Supprimez-la après le cycle de clôture.

## Exécuter le cycle

Lisez intégralement references/protocol.md et exécutez exactement un cycle d'analyse, de traitement et de state qui y est décrit. Pour chaque accès au dossier de synchronisation, utilisez ellmos FileCommander. Un listing shell, une entrée du planificateur ou un simple nom de fichier ne constitue pas une preuve d'analyse.

En cas d'inactivité, n'inventez aucun travail. Signalez brièvement : heure d'analyse, fichiers de fraîcheur lus, cadence actuelle, empty_runs, next_scan_at et expires_at.

## Exécuter WriteSync

N'écrivez que dans son propre emplacement système ou dans un canal global explicitement prévu. Indiquez expéditeur, destinataire, heure, référence, action, résultat, points ouverts et cadence souhaitée. Fusionnez au lieu d'écraser ; aucun identifiant ; respectez les verrous. Relisez le fichier canonique avec FileCommander après l'écriture.

## Journal des modifications

### 1.1.0 (2026-09-13)

- Ajout de la marque de participation par hôte STATE (champ `pingpong` dans `agents/registry/<slot>.state.json`) et des fichiers CALL adressés `call-<von>-to-<an|all>.txt` avec expiration ; `pingpong_runtime.py` connaît pour cela `state`, `call` et la vérification en deux étapes `check` avec un résultat à trois valeurs. Les anciens noms `pull-` sont encore lus à titre transitoire. Mise en œuvre de T-20260830-425388998 selon la décision de l'utilisateur du 2026-09-11 (modification minimale : seulement STATE, CALL et expiration).

### 1.0.1 (2026-09-09)

- Ajout de métadonnées de rôle déclaratives selon le contrat optionnel de rôle du module v2 ; aucun démarreur neutre ne les déclare. L'identité de protocole existante et le chemin de découverte sont conservés.

### 1.0.0 (2026-08-04)

- Contrat ListenSync/WriteSync indépendant du fournisseur, avec adaptateurs Codex Goal et Claude Loop.
- Ajout de la preuve FileCommander, du garde de fraîcheur, de la cadence adaptative et de la condition d'expiration absolue.
