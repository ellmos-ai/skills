---
name: steuer-assistent
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-07-23
updated: 2026-07-23
description: >
  Points to the standalone module steuer-assistent: a local, offline-first
  receipt worksheet for German employee income-related expenses
  (Werbungskosten) -- record, sum to the cent, private ZIP export. Use this
  skill when Werbungskosten receipts should be prepared in a structured way
  -- with a clear boundary: not tax advice, no deductibility check, no
  creation or submission of a tax return (that happens via ELSTER or
  approved software).

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

provenance:
  origin: "external"
  origin_repo: "https://github.com/ellmos-ai/steuer-assistent"
  origin_path: "SKILL.md, steuer_assistent/ (CLI module)"
  origin_version: null
  last_sync_from_origin: "2026-07-23"
  last_sync_to_origin: null
  local_changes_since_sync: false

category: utilities
tags: [tax, germany, receipts, finance, wrapper, pointer-skill]
language: en
status: active
---

# steuer-assistent -- Pointer Skill

This skill is a **thin pointer (wrapper)** to the standalone, public module
repository
[`ellmos-ai/steuer-assistent`](https://github.com/ellmos-ai/steuer-assistent)
(MIT license, public). The actual skill lives there -- this repository only
links to it and documents installation.

Note: `steuer-assistent` is scoped to German tax law (employee
income-related expenses, "Werbungskosten"); its CLI and documentation are
German-language by design.

## What the module does

`steuer-assistent` is a small, offline-first Python module for
self-categorized receipts for German employee income-related expenses
(Werbungskosten):

- Record receipts (category, amount, date, optional note).
- Sum recorded expenses to the cent, per year.
- Export a private, non-official ZIP worksheet (CSV + summary + a
  non-official notice, without the receipt files themselves).
- Local store (default `%USERPROFILE%\.steuer-assistent\steuer.db`), no
  network access, no cloud upload, no access to other databases.

## Boundaries (important)

- **Not tax advice.** The module does not assess the deductibility of
  individual items, and it does not create or submit a tax return.
- Official electronic submission happens exclusively through ELSTER or
  approved software -- not through this module.
- Scope: a private worksheet for employee income-related expenses; no
  business/self-employment expense tracking.

## Installation (generic, no local paths)

1. Clone the module:
   ```bash
   git clone https://github.com/ellmos-ai/steuer-assistent.git <clone-path>
   ```
2. Install and verify:
   ```bash
   cd <clone-path>
   python -m pip install -e .
   python -B -m pytest tests -q -p no:cacheprovider
   ```
3. Adopt `<clone-path>/SKILL.md` into your own skill environment (e.g.
   `~/.claude/skills/steuer-assistent/`). Do NOT commit real local paths or
   hostnames into a versioned skill environment.
4. Adjust the store path if needed via `STEUER_ASSISTENT_DB=<path>` or
   `--store <path>`; the default is the user's home directory.
5. For CLI commands, privacy, and boundaries, see the module repo's README.

## Origin of this pointer skill

This wrapper was added on 2026-07-23 as a showcase entry for the
`ellmos-ai/skills` repository. There is **no code duplication** -- maintenance
and versioning stay solely in the `ellmos-ai/steuer-assistent` module repo.

## Changelog

### 0.1.0 (2026-07-23)
- Initial pointer skill for `ellmos-ai/steuer-assistent`.
