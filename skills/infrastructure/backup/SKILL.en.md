---
name: backup
version: 1.0.0
type: skill
author: User
created: 2026-08-24
updated: 2026-08-24
description: Plan, mirror, verify, restore or explicitly archive files through the fail-closed mac-backup core. Use for the user's own cross-host backup jobs; do not use for generic cloud sync or casual file copying.
visibility: public
language: en
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
---

# Backup

Use the installed `mac-backup` CLI as the only transfer implementation. Do not recreate the flow
with raw `scp`, `rsync`, SSHFS, Explorer actions or ad-hoc deletion.

## Route the request

- An ordinary "backup" request means `mirror`; the source remains untouched.
- `archive` means source cleanup and is a separate destructive intent. Never infer it from
  "backup", "copy" or "free some space".
- `restore` writes to a new destination and does not silently overwrite.
- If no reviewed job JSON exists, prepare a job proposal and stop before `init-target` or transfer.

## Execution

1. Read the job and run `mac-backup plan <job> --json`.
2. Check that the returned source class, file count, byte count, target volume ID, encryption state
   and host fingerprint match the request and current device receipt.
3. For mirror, run `mac-backup mirror <job> --json`, then `mac-backup verify <job> --json`.
4. For restore, use a new absolute destination and verify the restored files through the command's
   manifest result.
5. For archive, pass `--confirm-delete` only when the user explicitly requested source removal and
   the reviewed plan names exactly that source. A policy block is the correct result; never bypass
   `target_encryption_required`, `source_class_unknown_cleanup_blocked`,
   `onedrive_dehydrate_not_implemented`, a lock, identity mismatch or missing anchor.

`init-target` is privileged setup, not routine execution. It requires an independently obtained
operating-system receipt for volume ID and encryption; a value copied from the proposed job is not
evidence.

Never claim that a mirror is a complete backup until target verify and a real restore drill have
both passed. Keep secrets, real job files, local anchors and user file names out of tickets, Git and
OneDrive.

## Changelog

### 1.0.0 (2026-08-24)
- Neutralized copy of the `~/.claude/skills/backup/` deployment master, added to the categorized
  library. Root cause of the sync gap: the skill was deployed but had no source entry under
  `skills/<category>/`, so `skill_sync.py status` reported it as `NUR-ZIEL` (target-only) and
  `catalog.py`/`build_public_registry.py` (which only scan `skills/`) never saw it — it could
  therefore never reach the public registry or `SKILLS-MAP.md`, no matter how the deployment copy
  was edited.
