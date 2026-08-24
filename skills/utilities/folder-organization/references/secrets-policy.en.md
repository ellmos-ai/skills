# Secrets Policy

This policy runs before content analysis, hashing, and semantic organization. It does not claim
complete secret discovery; it handles accidental exposure and unsafe cloud placement fail-closed.

## Invariants

- Never copy a detected or suspected secret value into prompts, chat, reports, manifests, names,
  pointers, logs, or errors.
- Classify protected names such as `.env`, private keys, and credential files by path and metadata
  only. Do not semantically open them or send them to a model.
- `--hash-all` never bypasses this protection.
- A content match emits only a signal ID, never the matched text or surrounding context.
- A match is not proof of a real secret, and a clean result is not proof that a file is secret-free.

“Do not open” means do not display, semantically read, or transmit content to a model. An explicitly
approved localization may copy the file as opaque bytes and compare local hashes when tool output
does not reveal content.

## Defaults and configuration

[`../config.json`](../config.json) defines protected names and template exclusions, local signal
rules, configured or heuristic cloud roots, `cloud_action`, `local_secret_root`, and `pointer_mode`.
A run-specific `--config` may override them; nested objects merge with safe defaults. Public skill
configuration must not contain user paths, accounts, or keys.

## Incidental discovery

1. Stop further content output.
2. Do not repeat the value or context; report only file, signal ID, and `secret-candidate` status.
3. Check already produced output for exposure. Treat possible exposure as unresolved and recommend
   rotation; never claim the secret was revoked or deleted.
4. Remove the item from normal sorting, Cut-and-Clue, archive, and review-trash processing until the
   secrets policy is resolved.

## Transactional cloud localization

A path marker is only a cloud suspicion. Refresh provider status, sync root, and locks when those
capabilities exist. Then:

1. Resolve `local_secret_root` and prove it is outside every cloud/sync root. Block when the target,
   local storage, or restrictive permissions cannot be verified.
2. Show a dry run with source, opaque pointer ID, pointer mode, affected references, and rollback.
   `localize-after-approval` still requires explicit approval for the concrete run.
3. Copy opaque bytes to a temporary local name, set restrictive permissions, and compare internal
   source/destination hashes. Atomically finalize the local name. Never overwrite.
4. Map the opaque ID to the local path only in a restrictive local `SECRET-POINTER-MAP.json`; never
   sync that map back to the cloud.
5. Check runtime references. A pointer is not a functioning `.env`; block source mutation until a
   dependent application is safely reconfigured and tested.
6. Only after local readback and hash equality, remove or replace the cloud source with a recoverable
   operation. Prefer provider recycle/version recovery when available.
7. Write the non-secret pointer and recheck cloud source, local target, mapping, references, and
   rollback receipt.

## Pointer modes

- `control-file` (default): entry in the nearest suitable control file, normally
  `SECRETS-POINTERS.md`; least likely to break an application.
- `sidecar`: `<filename>.secret-pointer` beside the former location.
- `placeholder`: dummy at the old filename; only after proving no process will load it as a secret.

A cloud pointer contains at most an opaque ID, status, review date, and non-sensitive policy hint.
By default it contains no local absolute path, secret value, account identifier, or recovery data.

## Hard blockers

- unclear scope or missing approval;
- missing local target, target inside another sync root, or unverifiable permissions;
- active writer, cloud lock, collision, or incomplete copy;
- signed, evidentiary, or runtime-critical file without a verified replacement path;
- a pointer or report would disclose sensitive data or a private local path.
