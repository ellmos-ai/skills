# Provider adapter contract

## Capability profile

Describe the target without provider-specific fields in the core:

```json
{
  "schema": "automation-self-care.provider.v1",
  "actor_id": "provider-app@host",
  "provider": "provider-name",
  "app_display_name": "APP NAME",
  "app_class": "desktop-app",
  "timezone": "Area/City",
  "capabilities": [
    "inventory",
    "run-history",
    "create",
    "update",
    "pause",
    "readback",
    "usage-metrics",
    "model-selection",
    "workspace-bindings",
    "permissions"
  ],
  "native_surface": {
    "kind": "api-or-command-or-ui",
    "identifier": "documented local identifier"
  },
  "recovery_floor": {
    "minimum_core_runs_per_day": 1
  }
}
```

Do not place tokens, full prompts, private paths or account identifiers in a shared
profile.

`app_display_name` is a non-sensitive, human-readable app label. New profiles
must set it explicitly. The core-set builder formats every visible care title as
`<APP_DISPLAY_NAME> — <CARE_TITLE>` while preserving `automation-care.*` as the
stable machine identity. For example, a Codex adapter uses `CODEX`, producing
`CODEX — Automation definition hygiene`; the neutral core never hardcodes that
provider name.

Legacy v1 profiles without `app_display_name` remain readable: the builder
derives an uppercase label from `provider` and emits a migration warning. Use
`--strict-profile` in CI or profile review so new profiles cannot rely on that
fallback.

## Adapter operations

An implementation may expose any mechanism, but the logical operations are:

| Operation | Required evidence |
|---|---|
| `discover` | supported native surface and version |
| `inventory` | stable task IDs and current state |
| `create` | native returned ID plus readback |
| `update` | before/after fields plus readback |
| `pause` | state transition plus readback |
| `history` | scheduler event and outcome evidence kept separate |
| `usage` | timestamped capacity measurement and source |

If a write operation lacks readback, treat it as unsupported.

## Identity, title reconciliation and duplicate protection

- Match an existing task by stable `task_id` first, then provider-native ID,
  semantic role and finally the known unprefixed legacy title.
- A visible title is metadata, never identity. Changing the title must not
  change the stable task ID.
- When exactly one semantic match exists, update its title in place.
- When multiple candidates match, stop as `blocked`; never guess.
- Create a task only when no semantic match exists. Re-run inventory before
  creation so a second apply cannot create a duplicate.
- Preserve and read back the non-title fingerprint: status, schedule, model,
  reasoning, prompt fingerprint, permissions, bindings and scope.
- Naming is an additional recognition and self-protection layer. It does not
  replace the recovery floor, stable IDs, suppression, rollback or readback.

## Mutation transaction

1. Re-read live state and locks.
2. Confirm the target task and expected precondition fingerprint.
3. Save the before-state through the supported export/snapshot path.
4. Apply one narrow change.
5. Read the live state again.
6. If state differs from the intended change, roll back or record a blocked repair.
7. Write a local receipt containing sanitized fingerprints and evidence pointers.

For a title-only migration, the intended change set contains exactly `title`.
If any non-title fingerprint changes, roll back and report the migration as
blocked.

Raw edits to an implementation file are allowed only when the provider documents
that file as its supported API and a live readback proves the result.

## Unsupported platforms

When no native unattended path exists:

- generate exact manual steps;
- keep the task contract portable;
- mark the deployment `manual` or `blocked`;
- do not claim that a schedule exists;
- allow another actor to cover the task through a supported deployment.
