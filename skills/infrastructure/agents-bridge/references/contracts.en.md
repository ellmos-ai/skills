# agents-bridge 3 file contracts

## Authority and pointer graph

A profile declares exactly one `primary_surface`. The same provider/path pair
appears exactly once in `provider_surfaces` with `strategy: primary`.
`truth_sources` are ordered, and every `pointer_graph` edge references declared
surface or truth IDs. A filename never establishes authority.

Discovery may select only one existing surface marked
`agents-bridge-primary: true`. Multiple markers produce `status: blocked` with
candidates and a required decision. No marker produces `needs-user-selection`.

## Data-flow matrix of the reproduced reference structure

This redacted matrix describes the observed structure; it is not a new default:

| Native surface | Data flow | Profile role |
|---|---|---|
| Codex `AGENTS.md` | loads a Codex-specific pointer, then shared rules | loader |
| `GPT.md` | points to the selected primary and further ordered sources | loader |
| Claude `CLAUDE.md` | reaches primary and shared rules directly | explicit primary or loader |
| Gemini `GEMINI.md` | reaches the same shared sources through a loader or projection | loader/projection |
| Shared memory index | points to separate provider-owned silos | index, no merge |
| Provider silo | distinct owner and writers; declared readers | separate truth |
| Messenger | sender outbox → recipient inbox → ACK/receipt | append-only file events |

Another instance may select `AGENTS.md`, `GPT.md`, `GEMINI.md`, or a custom
relative path as primary. The profile represents the graph; the program does
not hard-code it.

## Projections

Loaders and redirects are preferred. A projection is allowed only when a
provider cannot load references natively. Its generated header records the v3
marker, profile ID, `generated_at`, SHA-256 source hashes, and edit provenance.
`verify` reports changes specifically as `projection-drift`. Controlled
regeneration uses `capture --regenerate-projections` into a new package, then
goes through preview and restore again.

## Package and restore

Capture reads only declared profile paths and explicit includes; excludes take
precedence while traversing directories. Only regular UTF-8 text files inside
the instance root are accepted. The package manifest binds the profile and
content hash, file size, source/package hashes, synthesized/projection flags,
directory scope, and privacy events. It never stores the absolute source root.

Plan classifies `create`, `update`, and `unchanged`. Applied restore checks the
previewed before-hash, backs up every changed existing file, writes atomically,
and reads the resulting hash back. A receipt binds the target, backup, package
hash, and each action. Rollback fails closed after later target drift. An
unchanged second restore is idempotent.

## Messaging, memory, presence, and locks

Messaging creates immutable event files, per-actor inboxes/outboxes, handoffs,
ACKs, sender receipts, and an append-only provenance log. Actors must be
declared, and message bodies pass the privacy gate.

The shared memory index points to silos that each declare an owner, writers,
readers, scope, refresh rule, and merge rule. `automatic` merge is invalid;
cross-silo merge or overwrite is a manual decision.

Presence and cooperative claims use bounded leases. A live foreign claim fails
closed, and only its owner can release it. These contracts do not launch
providers and are not a scheduler or ticket system.

## Privacy

Default `reject` mode stops on detected credentials, private keys, or personal
absolute home paths. Explicit `redact` mode records and replaces findings with
neutral placeholders. Binary files, non-UTF-8 text, symlink escapes, and
unmanifested package files are rejected.
