---
name: file-collect-sort-action
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-18
updated: 2026-08-18
description: "Reconnaît les demandes d'utilisateur de la forme « récupère toujours certains fichiers d'un dossier et rassemble-les à une destination » et met en place pour cela le module file-collect-sort-action (CLI fcsa) — un agent piloté par configuration qui analyse des dossiers, catégorise des fichiers par gabarit et applique des actions échelonnées (move/copy/duplicate-check/delete/OCR/place-information). Utilise ce skill pour des phrases comme « récupère toujours <Ordner> depuis <Dateiart> et rassemble-les dans <Ziel> », « trie automatiquement le dossier X selon ... », « rassemble les fichiers entrants de ... dans ... », « nettoie ce dossier selon des règles » ou « déplace automatiquement tous les <Dateiart> de <Ordner> ». Mets TOUJOURS en place d'abord un essai à blanc (dry-run) et ne passe en mode réel qu'après un feu vert explicite de l'utilisateur ; la suppression reste en principe en mode _trash."
# Kompatibilitaet
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: utilities
tags: [dateien, sortierung, automatisierung, config-driven, ordner-ueberwachung, duplikate, ocr]
language: fr
status: active
visibility: public

# Abhaengigkeiten
dependencies:
  tools: [fcsa]
  services: []
  protocols: []
  python: []
  modules: [file-collect-sort-action]

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 844e8b0e6411e463278a6084440cd4915bf241f8ab5a036d1fa25913e18c681f
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:43.290037+00:00"
---
<img src="banner.png" width="100%" alt="file-collect-sort-action banner">

# File Collect Sort Action

> L'utilisateur a volontairement mis ce module en veille passive jusqu'à ce qu'une tâche concrète en ait besoin
> (ticket T-20260818-916568570, utilisateur, mot pour mot : *« ich werde irgendwann mal sagen hole aus dem
> ordner immer die und die dateien und sammle sie dort -> dann erkennst du den skill zu
> unserem modul und richtest das ein »*). Ce skill EST la reconnaissance qu'il attend.

## Quand ce skill s'applique

Les déclencheurs sont des phrases utilisateur qui décrivent une **collecte récurrente selon une règle** —
et non un simple « déplace ce fichier une fois » :

- « Récupère toujours `<Ordner>` depuis `<Dateiart>` et rassemble-les dans `<Ziel>` »
- « Trie automatiquement le dossier `<X>` selon `<Kriterium>` »
- « Rassemble les fichiers entrants de `<Quelle>` dans `<Ziel>` »
- « Range ce dossier selon des règles » / « déplace automatiquement tous les `<Dateiart>` de `<Ordner>` »
- Toute variante qui nomme une **source**, un **critère de reconnaissance** (type de fichier/motif de nom/contenu) et une
  **destination**, et implique que cela doit se produire **de façon répétée** (pas seulement une fois)

**Pas** ce skill : déplacer un fichier unique et ponctuel (un agent le fait directement,
sans couche de configuration) — `dokument-ingest` (répond à « comment lire le *contenu* »,
et non « où *va* le fichier ») — l'indexation incrémentale de texte sans déplacer de fichiers
(`gardener`).

## Ce que le module peut faire (résumé)

`file-collect-sort-action` (nom court **f-csa**, CLI **`fcsa`**) est un agent scan→catégoriser→agir piloté par configuration,
avec trois fichiers de configuration et une mémoire de traitement :

| Fichier | Rôle |
|---|---|
| `config.json` | `scan_paths` (liste blanche), inclusion/exclusion de formats, règles de détection de doublons, verrous de sécurité (`allow_hard_delete`) |
| `categories-definitions.json` | Gabarits de reconnaissance par catégorie (nom de fichier/extension/contenu), contrôles/verrous, `default_target`, `default_actions` + `default_stepping` |
| `action-rules.json` | Paramètres d'action par catégorie (cibles move/copy, mode de doublon, mode de suppression, backend OCR, ordre de placement) |
| `processing-csa.json` | est écrit **dans chaque dossier analysé** — fichiers connus, leur catégorie, actions appliquées, empreinte des réglages effectifs (fingerprint) |

Identifiants d'action connus : `duplicate_check`, `move`, `copy`, `delete`, `ocr_extract`,
`place_information`. Sémantique d'enchaînement : `default_stepping: true` = les actions s'exécutent de gauche à droite
dans l'ordre listé, un identifiant d'action listé deux fois s'exécute **deux fois** ; `false` = ensemble
(les doublons se réduisent à une seule exécution).

## Modèle de sécurité — À RESPECTER TOUJOURS lors de la mise en place

- **Le dry-run est obligatoire avant toute première exécution réelle**, pour chaque chemin analysé. `fcsa run` (sans
  `--dry-run`) refuse sans dry-run journalisé pour ce chemin précis.
- **Toute modification de réglage désarme à nouveau la confirmation** (empreinte sur les trois
  fichiers de configuration) — après chaque ajustement de configuration, la prochaine exécution réelle exige à nouveau un
  dry-run frais.
- **La suppression est fail-closed.** `delete` déplace toujours vers `trash_dir`, sauf si *à la fois*
  `action-rules.json` (`delete.hard_delete: true`) *et* `config.json`
  (`allow_hard_delete: true`) donnent explicitement leur accord. **Pour ce skill, s'ajoute en outre :**
  n'activer jamais la suppression définitive sans accord utilisateur séparé et explicite — la valeur par défaut reste
  `_trash`.
- **`scan_paths` est une liste blanche explicite** ; tout autre chemin lève
  `PathNotAllowedError` ; les chemins contenant un segment `.PRIVAT` ou `CREDENTIALS` sont rejetés au chargement.
- **Le dry-run n'a aucun effet, octet pour octet, sur le dossier analysé** : `processing-csa.json`
  n'est écrit que lors d'une exécution réelle, jamais lors d'un dry-run.

## Déroulé : de la phrase déclencheur à l'automatisation mise en place

1. **Structurer la tâche.** Extraire de la phrase de l'utilisateur la source, le ou les critères de reconnaissance et la ou les
   destinations. En cas de doute, poser une question ciblée (type de fichier ? inclure les sous-dossiers ?
   Que faire en cas de collision de nom à la destination — skip/overwrite/rename/quarantine ?).
2. **Localiser le module.** Vérifier d'abord avec `fcsa --help` que le CLI est disponible. S'il manque,
   identifier la voie de module ou de paquet autorisée pour le système actuel ; ne pas inventer de chemin local,
   de nom de paquet ni de copie de dépôt parallèle. Après une installation, relancer `fcsa --help`
   avant de créer les configurations.
3. **Créer le dossier de configuration.** `fcsa init <config-dir>` — écrit d'abord `scan_paths` dans un
   dossier `inbox/` neuf **à l'intérieur** du dossier de configuration lui-même, jamais automatiquement
   dans un vrai dossier utilisateur. Modèles d'exemple : `fcsa/_examples/*.example.json`
   dans le module.
4. **Adapter la configuration à la tâche réelle.** Régler `scan_paths` sur le dossier source indiqué, saisir dans
   `categories-definitions.json` le ou les gabarits de reconnaissance pour le type de fichier
   indiqué (`default_target` = destination indiquée), configurer dans `action-rules.json` les actions
   adéquates (typiquement `move`, éventuellement `duplicate_check` avant). `state_dir`/`trash_dir` NE doivent PAS se trouver
   dans un `scan_path` (le module le refuse — sinon boucle d'auto-alimentation).
5. **Toujours présenter d'abord le dry-run :** `fcsa run --config-dir <config-dir> --dry-run` — montrer le résultat à
   l'utilisateur (ce qui serait déplacé où, ce qui serait détecté comme doublon).
6. **Passer en réel uniquement sur feu vert explicite de l'utilisateur.** Seulement alors `fcsa run --config-dir
   <config-dir>` (sans `--dry-run`). `fcsa status --config-dir <config-dir>` affiche ensuite
   l'état.
7. **Étendre progressivement** (utilisateur : « et ensuite cela s'étend avec le temps ») : ajouter d'autres
   catégories/dossiers au lieu de recommencer une nouvelle mise en place — les trois
   fichiers de configuration se maintiennent de façon additive. Chaque extension exige à nouveau, à cause de
   l'empreinte des réglages, un dry-run avant la prochaine exécution réelle.

## Limites / points ouverts connus (état au ticket T-20260818-916568570)

- Le module est en passe 1, statut « development » — le pipeline central, le CLI et les verrous de sécurité sont
  terminés et testés (63/63 tests), mais **jamais encore passés en réel sur un vrai dossier utilisateur**. La première mise en
  service réelle est précisément l'usage de ce skill. La visibilité du dépôt est « private » — pas de publication sans
  son propre `repo-publish-check`.
- Deux lectures de lacunes de spécification sont documentées (`CHANGELOG.md`/`TODO.md` dans le
  module) : `default_stepping: false` réduit une action listée deux fois à **une** seule
  exécution ; `duplicate_check` avec le résultat `skip` interrompt **toute** la chaîne d'actions restante
  pour le fichier (et pas seulement move/copy). Si besoin, clarifier avec l'utilisateur avant qu'une configuration
  ne s'y fie.
- L'OCR est un backend enfichable (`none`/`command`) — aucun moteur OCR propre n'est fourni. Pour une
  véritable extraction OCR, raccorder `ellmos-filecommander` `fc_ocr` via le type de backend `command`.

## Provenance

Module construit dans le ticket T-20260818-916568570 (passe 1, fcsa-worker), mis en veille passive (PARKED/until-trigger)
à la demande de l'utilisateur jusqu'à exactement le déclencheur décrit ci-dessus. Ce skill met en œuvre précisément cette
note de mise en veille.

## Journal des modifications

### 1.0.0 (2026-08-18)
- Version initiale. Reconnaissance des déclencheurs pour les tâches « collecter/trier des fichiers automatiquement »,
  procédure de mise en place avec obligation de dry-run et passage en réel uniquement sur feu vert de l'utilisateur documentés.
