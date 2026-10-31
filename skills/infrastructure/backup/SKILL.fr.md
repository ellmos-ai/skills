---
name: backup
version: 1.0.0
type: skill
author: User
created: 2026-08-24
updated: 2026-08-24
description: "Planifie, reflète, vérifie, restaure ou archive explicitement des fichiers via le cœur fail-closed mac-backup. À utiliser pour les tâches de sauvegarde inter-hôtes propres à l'utilisateur ; ne pas utiliser pour la synchronisation cloud générale ni pour la copie occasionnelle de fichiers."
visibility: public
language: fr
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance:
  origin: "custom"
  origin_repo: "github.com/ellmos-ai/mac-backup"
  last_sync_from_origin: "2026-08-24"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: c50a9f8b557b5e4baa08f880f28ba234c8f56974e644ce57147bde5311a02ad6
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:46:14.327021+00:00"
---
<img src="banner.png" width="100%" alt="backup banner">

# Sauvegarde

Utiliser la CLI `mac-backup` installée comme seule implémentation de transfert. Ne pas reconstruire le flux
avec du `scp`, `rsync`, SSHFS, des actions de l'Explorateur ni une suppression ad hoc.

## Acheminer la demande

- Une demande ordinaire de « sauvegarde » signifie `mirror` ; la source reste intacte.
- `archive` signifie nettoyage de la source et constitue une intention distincte et destructive. Ne jamais la déduire de
  « backup », « copy » ou « free some space ».
- `restore` écrit vers une nouvelle destination et n'écrase jamais silencieusement.
- S'il n'existe pas de job JSON vérifié, préparer une proposition de job et s'arrêter avant `init-target` ou
  le transfert.

## Exécution

1. Lire le job et exécuter `mac-backup plan <job> --json`.
2. Vérifier que la classe de source renvoyée, le nombre de fichiers, le nombre d'octets, l'identifiant du volume de destination,
   l'état de chiffrement et l'empreinte de l'hôte correspondent à la demande et à la preuve actuelle de l'appareil.
3. Pour un miroir, exécuter `mac-backup mirror <job> --json`, puis `mac-backup verify <job> --json`.
4. Pour une restauration, utiliser une nouvelle destination absolue et vérifier les fichiers restaurés à partir du résultat
   du manifeste de la commande.
5. Pour une archive `--confirm-delete`, ne la transmettre que si l'utilisateur a explicitement demandé la suppression de la source et si le
   plan vérifié nomme exactement cette source. Un blocage par la politique est le résultat correct ; ne jamais contourner
   `target_encryption_required`, `source_class_unknown_cleanup_blocked`, `onedrive_dehydrate_not_implemented`, un verrou, un écart d'identité
   ou une ancre manquante.

`init-target` est une configuration privilégiée, et non une exécution de routine. Elle nécessite une preuve indépendante
du système d'exploitation pour l'identifiant du volume et le chiffrement ; une valeur copiée depuis le job proposé n'est pas une preuve.

Ne jamais affirmer qu'un miroir constitue une sauvegarde complète avant que la vérification de la destination et un véritable
test de restauration n'aient tous deux réussi. Ne pas inclure les secrets, les fichiers de tâches réels, les ancres locales ni les noms de fichiers personnels
dans les tickets, Git ou OneDrive.

## Journal des modifications

### 1.0.0 (2026-08-24)
- Copie neutralisée du master de déploiement `~/.claude/skills/backup/`, intégrée à la
  bibliothèque catégorisée. Cause de l'écart de synchronisation : la compétence était déployée mais n'avait pas d'entrée source sous
  `skills/<category>/` ; `skill_sync.py status` la signalait donc comme `NUR-ZIEL`
  (cible uniquement), et `catalog.py`/`build_public_registry.py` (qui ne scannent que `skills/`) ne la voyaient
  jamais — elle ne pouvait donc jamais atteindre le registre public ni `SKILLS-MAP.md`, quelle que soit la façon dont la copie de déploiement était modifiée.
