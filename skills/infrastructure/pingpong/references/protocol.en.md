# PingPong protocol

## Identity and responsibility

- Actor: <ACCESS-PATH>@<HOSTNAME>.
- Own write slot: read from launch configuration or inventory.
- If the write slot is ambiguous, fail closed and report the missing value. Never guess a destination path.
- Store runtime state and leases outside the synchronized folder, for example under ~/.pingpong/.
- ListenSync observes systematically. WriteSync writes only to the actor's own slot. ListenSync also performs WriteSync.

## FileCommander evidence requirement

Every scan must be evidenced through the FileCommander MCP:

1. capture the current time;
2. list relevant directories narrowly or search with filename-agnostic patterns;
3. inspect candidate metadata;
4. read relevant files completely;
5. only then update state and write receipts.

A shell-only scan, a filename, or memory from an earlier run is not sufficient evidence.

## Freshness guard

At startup and after a long interruption, inspect at least:

- the sync root top level;
- the global message or order channel;
- the actor's own slot;
- known peer slots.

Read the newest three files in every relevant channel completely, regardless of the stored timestamp. Follow LATEST, CURRENT, and version references to their current targets. Only then continue with incremental scanning.

Determine novelty from stable attributes: relative path, modification time, and checksum when needed. Never filter by a date embedded in a filename. Conflict copies are candidates, not authority. WAKE files are hints, not authority.

## Selection and execution

- Check recipient, actor, and host.
- Execute only work addressed to the actor, its host, or explicitly to all listeners.
- Record messages for other systems as seen, but do not execute them.
- Before modifying a target project, read its LOCK, claim, approval, and dirty-state rules.
- Preserve foreign changes and never place credentials in the sync folder.
- Publishing, pushing, deployment, and other external effects require the applicable authorization.
- If work cannot be completed safely, write a BLOCKED receipt with evidence and the next required step to the actor's own slot.

## Cadence mechanism B

The default start interval is 15 minutes. The empty_runs counter tracks consecutive evidenced scans without new work.

| empty_runs | next cadence |
|---:|---:|
| 0 to 3 | 15 minutes |
| 4 to 5 | 30 minutes |
| 6 to 7 | 1 hour |
| 8 to 9 | 2 hours |
| 10 to 11 | 4 hours |
| 12 to 13 | 8 hours |
| 14 to 15 | 16 hours |
| 16 or more | 24 hours |

New work resets empty_runs to 0 and the cadence to 15 minutes. An explicit user instruction for a fixed interval takes precedence.

## State

Runtime state contains at least:

- actor;
- sync_root;
- own_slot;
- started_at;
- expires_at;
- last_scan_at;
- empty_runs;
- current_cadence;
- processed_items with path, modification time, checksum, and result.

State does not replace file evidence. Run one final full scan before completion. The goal is reached when expires_at has passed, the final scan is evidenced, and no accepted work remains open.
