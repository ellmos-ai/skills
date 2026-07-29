---
name: system-onboarding
version: 1.2.0
type: skill
author: ellmos contributors
created: 2026-05-16
updated: 2026-07-29
description: Provider-neutral onboarding protocol for a new, rebuilt, or replacement workstation. It establishes the operating-system prerequisites, agent runtimes, shared rule surfaces, portable skills, verified configuration and post-install evidence without copying credentials, private prompts, or host-specific configuration into a repository.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [onboarding, setup, agent-runtimes, windows, macos, verification, sync]
language: de
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'internal onboarding protocol (sanitized for portable publication)', 'origin_version': '1.2.0', 'last_sync_from_origin': '2026-07-29', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **Deutsche Übersetzung** — Offizielle deutsche Version von `system-onboarding`.


# System Onboarding

Use this protocol to establish a new or rebuilt workstation for local-first agent
work. It is a sequencing and verification guide, not an installer and not a source
of credentials. Resolve product-specific instructions from each provider's current
documentation before changing a live system.

## Activation

Use for a new workstation, a reinstalled operating system, a replacement device, or
a controlled recovery of one agent runtime. First identify the operating system,
target runtime, owner, shared rule surface, and whether the request is a full rebuild
or a bounded component repair. Do not assume that a configuration copied from one
host is safe or supported on another.

## Ordered workflow

1. Establish operating-system updates, Git, authenticated source control, Python and
   the current supported Node.js LTS where needed.
2. Install only the requested agent runtimes through their supported installers and
   complete their native login flows without placing tokens in project files.
3. Create local configuration roots and load an explicitly selected, canonical rule
   surface. Merge templates; never overwrite existing local state blindly.
4. Install portable skills and MCP or plugin configuration only through their stated
   deployment procedures. Treat each provider's configuration format as distinct.
5. Configure shared synchronization only after the local runtime works. Share
   sanitized contracts and receipts, not credentials, full prompts, or machine-local
   paths.
6. Recreate a scheduler or automation only through its supported native surface.
   Preserve prior state and leave new work disabled until its owner approves activation.
7. Run the appropriate post-install checks and write a local receipt that distinguishes
   installation, configuration, scheduler registration and successful outcome.

Read only the matching reference for the target platform:

- [overview](references/overview.md) for boundaries and data placement;
- [Windows checklist](references/windows-checklist.md) for Windows;
- [macOS checklist](references/mac-checklist.md) for macOS; and
- [post-install](references/post-install.md) for verification and recovery.

## Boundaries

- Never publish credentials, recovery codes, private prompts, account identifiers, or
  raw logs to a shared repository or synchronization folder.
- Keep virtual environments, dependency caches and large runtime artifacts out of
  cloud-synchronized project folders.
- Do not make a copied configuration authoritative. The target host must discover and
  read back its own supported state.
- Do not register a schedule merely because a task file exists. Native registration
  and outcome evidence are separate requirements.
- When an existing host is being repaired, inventory its current state and locks before
  changing any configuration.

## Completion evidence

A complete onboarding receipt records the target operating system, selected runtimes,
their verified versions, the canonical rule references loaded, the explicit skills or
extensions deployed, unsupported capabilities, and any deferred user decisions. A
successful command exit alone is not evidence that an application loaded its new
configuration or that a scheduled task achieved its intended outcome.

## Changelog

### 1.2.0 (2026-07-29)

- Ported the reusable onboarding sequence and platform references into the public
  skills catalog after removing host-specific paths, account details and private
  operational material.
