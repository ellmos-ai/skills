# Provider adapter contract

## Capability profile

Describe the target without provider-specific fields in the core:

```json
{
  "schema": "automation-self-care.provider.v1",
  "actor_id": "provider-app@host",
  "provider": "provider-name",
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

## Mutation transaction

1. Re-read live state and locks.
2. Confirm the target task and expected precondition fingerprint.
3. Save the before-state through the supported export/snapshot path.
4. Apply one narrow change.
5. Read the live state again.
6. If state differs from the intended change, roll back or record a blocked repair.
7. Write a local receipt containing sanitized fingerprints and evidence pointers.

Raw edits to an implementation file are allowed only when the provider documents
that file as its supported API and a live readback proves the result.

## Unsupported platforms

When no native unattended path exists:

- generate exact manual steps;
- keep the task contract portable;
- mark the deployment `manual` or `blocked`;
- do not claim that a schedule exists;
- allow another actor to cover the task through a supported deployment.
