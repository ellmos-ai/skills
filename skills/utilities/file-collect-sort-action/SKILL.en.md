---
name: file-collect-sort-action
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-18
updated: 2026-08-18
description: >
  Recognizes user requests of the form "always pull certain files from a
  folder and collect them at a destination" and sets up the module
  file-collect-sort-action (CLI fcsa) for it — a configuration-driven agent
  that scans folders, categorizes files by template and applies staged
  actions (move/copy/duplicate-check/delete/OCR/place-information). Use
  this skill for sentences like "always pull <file type> from <folder> and
  collect them in <destination>", "automatically sort folder X by ...",
  "collect incoming files from ... into ...", "clean up this folder based
  on rules", or "automatically move all <file type> from <folder>". ALWAYS
  sets up a dry run first and only arms it after explicit user go-ahead;
  deletion always stays in `_trash` mode by default.

# Compatibility
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Categorization
category: utilities
tags: [dateien, sortierung, automatisierung, config-driven, ordner-ueberwachung, duplikate, ocr]
language: en
status: active
visibility: public

# Dependencies
dependencies:
  tools: [fcsa]
  services: []
  protocols: []
  python: []
  modules: [file-collect-sort-action]

# Provenance
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# File Collect Sort Action

> The user has deliberately parked this module passively until a concrete
> order needs it (ticket T-20260818-916568570, user verbatim: *"at some
> point I'll say pull such-and-such files from the folder and collect them
> there -> then you recognize the skill for our module and set it up"*).
> This skill IS the recognition it has been waiting for.

## When this skill applies

Triggers are user sentences that describe a recurring **collect-by-rule**
task — not a one-off "move this one file":

- "Always pull `<file type>` from `<folder>` and collect them in
  `<destination>`"
- "Automatically sort folder `<X>` by `<criterion>`"
- "Collect incoming files from `<source>` into `<destination>`"
- "Clean up this folder based on rules" / "automatically move all `<file
  type>` from `<folder>`"
- Any variant that names **source**, **recognition feature** (file
  type/name pattern/content) and **destination** and implies that this
  should happen **repeatedly** (not just once, right now)

**Not** this skill: moving a single, one-off file (an agent does that
directly, without a configuration layer) — `dokument-ingest` (answers
"what do I read the *content* with", not "where does the *file* belong")
— incremental text indexing without moving files (`gardener`).

## What the module can do (short version)

`file-collect-sort-action` (short name **f-csa**, CLI **`fcsa`**) is a
configuration-driven scan→categorize→act agent with three configuration
files and a processing memory:

| File | Role |
|---|---|
| `config.json` | `scan_paths` (allowlist), format include/exclude, duplicate detection rules, safety gates (`allow_hard_delete`) |
| `categories-definitions.json` | recognition templates per category (filename/extension/content), checks/gates, `default_target`, `default_actions` + `default_stepping` |
| `action-rules.json` | action parameters per category (move/copy targets, duplicate mode, delete mode, OCR backend, placement order) |
| `processing-csa.json` | written **into every scanned folder** — known files, their category, applied actions, effective settings fingerprint |

Known action IDs: `duplicate_check`, `move`, `copy`, `delete`,
`ocr_extract`, `place_information`. Stepping semantics: `default_stepping:
true` = actions run left to right as listed, an action ID listed twice
runs **twice**; `false` = a set (duplicates collapse into one execution).

## Safety model — ALWAYS observe during setup

- **A dry run is mandatory before the first live run ever**, per scan
  path. `fcsa run` (without `--dry-run`) refuses without a logged dry run
  for exactly that path.
- **A settings change disarms the confirmation again** (fingerprint over
  all three config files) — after every config adjustment, the next live
  run needs a fresh dry run again.
- **Deletion is fail-closed.** `delete` always moves to `trash_dir`,
  unless *both* `action-rules.json` (`delete.hard_delete: true`) *and*
  `config.json` (`allow_hard_delete: true`) explicitly agree. **This skill
  additionally requires:** never enable hard delete without a separate,
  explicit user approval — the default stays `_trash`.
- **`scan_paths` is an explicit allowlist**, every other path throws
  `PathNotAllowedError`; paths with a `.PRIVAT` or `CREDENTIALS` segment
  are rejected on load.
- **A dry run is byte-for-byte consequence-free** for the scanned folder:
  `processing-csa.json` is only ever written on a live run, never on a
  dry run.

## Procedure: from the trigger sentence to the set-up automation

1. **Structure the order.** Extract source, recognition feature(s) and
   destination(s) from the user sentence. Ask targeted follow-up questions
   where unclear (which file type? include subfolders? what happens on a
   name collision at the destination — skip/overwrite/rename/quarantine?).
2. **Locate the module.** First check with `fcsa --help` whether the CLI
   is available. If missing, determine the module or package path
   authorized for the current system; do not invent a local path, package
   name or parallel checkout. After an installation, run `fcsa --help`
   again before creating configurations.
3. **Create the config folder.** `fcsa init <config-dir>` — initially
   writes `scan_paths` to a fresh `inbox/` folder **inside** the config
   folder itself, never automatically onto a real user folder. Example
   templates for this: `fcsa/_examples/*.example.json` in the module.
4. **Tailor the config to the real order.** Set `scan_paths` to the named
   source folder, enter the recognition template(s) for the named file
   type in `categories-definitions.json` (`default_target` = the named
   destination), configure the matching actions in `action-rules.json`
   (typically `move`, possibly `duplicate_check` before it). `state_dir`/
   `trash_dir` must NOT lie inside a `scan_path` (the module rejects
   that — otherwise a self-feeding loop).
5. **Always present a dry run first:** `fcsa run --config-dir
   <config-dir> --dry-run` — show the user the result (what would be
   moved where, what gets recognized as a duplicate).
6. **Arm it only after explicit user go-ahead.** Only then `fcsa run
   --config-dir <config-dir>` (without `--dry-run`). `fcsa status
   --config-dir <config-dir>` then shows the state.
7. **Extend it step by step** (user: "and then this grows over time"): add
   further categories/folders instead of starting a new setup — the three
   config files are maintainable additively. Because of the settings
   fingerprint, every extension needs a dry run again before the next
   live run.

## Boundaries / known open points (as of ticket T-20260818-916568570)

- The module is pass 1, status "development" — the core pipeline, CLI and
  safety gates are finished and tested (63/63 tests), but **never yet
  armed against a real user folder**. This skill's deployment is
  deliberately the first arming. Repo visibility is "private" — no
  publication without its own `repo-publish-check`.
- Two readings of specification gaps are documented (`CHANGELOG.md`/
  `TODO.md` in the module): `default_stepping: false` collapses an action
  listed twice into **one** execution; `duplicate_check` with result
  `skip` aborts the **entire** remaining action chain for the file (not
  just move/copy). Clarify with the user if needed before a config relies
  on this.
- OCR is a pluggable backend (`none`/`command`) — no OCR engine is
  bundled. For real OCR extraction, wire up `ellmos-filecommander`'s
  `fc_ocr` via the `command` backend type.

## Origin

Module built in ticket T-20260818-916568570 (pass 1, fcsa-worker), at the
user's request deliberately parked passively (PARKED/until-trigger) until
exactly the trigger described above occurs. This skill implements exactly
that parking note.

## Changelog

### 1.0.0 (2026-08-18)
- Initial version. Trigger recognition for "collect/sort files
  automatically" orders, setup procedure with mandatory dry run and arming
  only after user go-ahead documented.
