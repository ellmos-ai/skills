---
name: pingpong
version: 1.0.0
type: protocol
author: Lukas Geiger, OpenAI Codex
created: 2026-08-03
updated: 2026-08-04
description: >
  Runs a time-bounded, session-scoped radio link over a shared synchronized
  folder. ListenSync systematically scans for assignments and news; WriteSync
  sends deltas and receipts. Use for PingPong, tin-can-phone communication,
  ListenSync, WriteSync, sync listeners, assignment watches, news scans, or
  goal/loop monitoring.

# Compatibility
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Categorization
category: infrastructure
tags: [pingpong, sync, listener, goal, loop, cadence, filecommander]
language: en
status: active

# Dependencies
dependencies:
  tools: [ellmos-filecommander]
  services: []
  protocols: [shared-folder-sync]
  python: []

# Provenance
provenance:
  origin: "custom"
  origin_path: "local-skill/pingpong"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-08-04"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="pingpong banner">

# PingPong

Operate two or more systems as radio stations over a shared sync folder. Keep the functional contract provider-neutral; only the continuation adapter differs.

## Select the mode

- ListenSync: Exactly one systematic listener per host. It scans, accepts applicable assignments, and also performs WriteSync when replying.
- WriteSync: Every working actor may send its own relevant deltas, assignments, news, and receipts. This mode does not start a listener.
- Default to ListenSync when the mode is omitted.

## Define the run contract

1. Default to 24h. Also accept relative durations such as 15m, 2h, 3d, or an absolute ISO-8601 deadline.
2. Measure local start time and state expires_at with date, time, and timezone.
3. Start at 15 minutes. Apply the cadence in references/protocol.en.md unless the user requests a fixed cadence.
4. Define success as: deadline reached, final FileCommander scan evidenced, every applicable input observed before the deadline completed or precisely documented as blocked, state updated, and the owned scheduler stopped.
5. Never claim a scan or successful completion without FileCommander evidence.

## Use the provider adapter

### Codex

Before the first scan, explicitly create a persisted goal containing the full run contract and expires_at. Process exactly one complete scan cycle per continuation. Do not complete the goal after one empty or successful cycle. Wait in real time until next_scan_at, for example:

    python "<skill-root>/scripts/pingpong_runtime.py" wait --until "<next_scan_at>"

At expiry, run the final cycle. Complete the goal only when the success criteria are met.

### Claude Code

Start the task as /loop <cadence> $pingpong. If the skill already runs from a scheduled invocation, do not create a second loop. On a cadence change, replace only the owned cron job. Delete it after the final cycle.

## Run one cycle

Read references/protocol.en.md completely and execute exactly one scan, processing, and state cycle. Use ellmos FileCommander for every access inside the sync folder. A shell listing, scheduler registration, or filename alone is not scan evidence.

Invent no work during idle cycles. Report briefly: scan time, freshness files read, current cadence, empty_runs, next_scan_at, and expires_at.

## Perform WriteSync

Write only to the actor's own system slot or an explicitly global channel. State sender, recipient, time, reference, action, result, open points, and requested cadence. Merge rather than overwrite; include no credentials; respect locks. Read the canonical file back through FileCommander after writing.

## Changelog

### 1.0.0 (2026-08-04)

- Added the provider-neutral ListenSync/WriteSync contract with Codex goal and Claude loop adapters.
- Added FileCommander evidence, freshness guard, adaptive cadence, and absolute expiry criteria.
