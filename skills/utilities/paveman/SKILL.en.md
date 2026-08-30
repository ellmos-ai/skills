---
name: paveman
version: 1.0.1
type: skill
author: Lukas Geiger + Claude
created: 2026-08-19
updated: 2026-08-20
description: >
  Recognizes orders to shorten a rule or memory file ("shorten my
  CLAUDE.md", "MEMORY.md is too long", "compress the docs without touching
  the technical content", "this rule file gets truncated past the
  character limit") and uses the module paveman for it — a deterministic,
  model-free CLI tool for shortening prose in Markdown/text files, with a
  dry run as the default, rollback and a strict protection validator for
  paths, headings and code. Use this skill for sentences like "shorten
  <file>", "this file is too long/gets truncated", "shrink this rule
  file", "compress without changing the content", or whenever a rule/
  memory file is noticeably hitting a character or line limit.

# Compatibility
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Categorization
category: utilities
tags: [kürzen, kompression, regeldatei, gedächtnis, deterministisch, dry-run, rollback, dokumentation]
language: en
status: active
visibility: public

# Dependencies
dependencies:
  tools: [paveman]
  services: []
  protocols: []
  python: []
  modules: [paveman]

# Provenance
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Paveman — deterministically shorten rule and memory files

> Thin, user-neutral skill wrapper around the separately provided module
> `paveman`. The skill recognizes when the tool fits and describes its
> safe procedure. It assumes neither a specific machine, nor a fixed
> installation path, nor a personal profile.

## When this skill applies

Triggers are user sentences that want to shorten an **existing rule,
convention or memory file** without changing its substantive content:

- "Shorten `<file>`" / "this file is too long" / "gets truncated at X
  characters or lines"
- "Compress the docs without touching technical content or code"
- "MEMORY.md or CLAUDE.md has gotten too full"
- "Make this rule file more compact, but leave the meaning unchanged"
- Any variant that means **shortening an existing file**, not **writing
  new content** and not **translating** (see boundary below)

**Not** this skill:

- **`knappform`** — changes how the model itself speaks in the running
  conversation (LLM communication style, model-based, no file access).
  `paveman` instead changes the content of an existing file
  deterministically and without a model call. Both can coexist; they are
  technically and functionally separate.
- **`bilingual-doc-sync`** — brings missing language versions up to date.
  `paveman` shortens one version and translates nothing.
- **`llm-text-hygiene`** — removes AI traces or chat leftovers from texts.
  That's a different purpose than shortening.
- Writing or inventing new content — `paveman` only shortens what's
  already there.

## What the module can do

`paveman` is a rule-based, deterministic prose shortener for Markdown and
text files: no model call, no tokens, no network transmission. Provisioning
can differ by system; what's authoritative is the module or package state
authorized there.

| Flag | Effect |
|---|---|
| *(no flag)* | **Dry run (default).** Shows the diff and character savings, writes nothing. |
| `--apply` | Actually writes; a backup is created automatically beforehand. |
| `--rollback` | Restores the last backup. |
| `--locker` | Reports path or heading deviations only as a warning instead of an error. |
| `--kontext N` | Sets the number of diff context lines. |

The **protection validator runs on every call**. Code blocks, paths and
headings must not be changed. In the default mode, a deviation prevents
writing instead of just reporting it.

## Procedure — always in this order

1. **Dry run first.** Run `paveman <file>` without `--apply`. Show the
   user the character savings, the diff and the validator status ("OK" or
   a concrete error message).
2. **Write only after explicit approval.** Only then run `paveman <file>
   --apply`; never switch automatically from dry run to write mode.
3. **Mention `--rollback` before writing.** The user should know in
   advance how to undo an unwanted result.
4. **Take validator errors seriously.** Don't use `--locker` just to get
   past an error. First check whether the deviation is actually harmless;
   the softer mode requires a deliberate user decision.
5. **Respect curated content.** A rule-based tool doesn't reliably
   recognize whether a phrasing is deliberately verbose. When in doubt,
   carefully review the dry-run diff.

## Prerequisite — check module availability

1. Check with `paveman --help` whether the CLI is available in the
   current environment.
2. If the command is missing, determine the module or package path
   authorized for this system. Do not invent a local path structure, a
   package name or a repository.
3. If no authorized source can be resolved, report the missing
   prerequisite as its own setup point instead of blindly running the
   skill or creating a parallel module.
4. After an installation, first run `paveman --help` again and then a
   harmless dry run; a real write test remains subject to approval.

## Examples

```text
User: "Shorten my CLAUDE.md, it gets truncated at session start."

→ `paveman CLAUDE.md` (dry run)
→ Result: "12,400 → 9,800 characters (-21%), validator: OK."
→ Show the diff and point out `--rollback`.
→ User confirms.
→ `paveman CLAUDE.md --apply`
```

```text
User: "MEMORY.md is too full, please shorten it."

→ Dry run: "893 → 893 characters, no rule matched — the text is already
compact."
→ Don't recommend `--apply`; honestly report the lack of added value.
```

## Changelog

### 1.0.1 (2026-08-20)

- Fully decoupled the public wrapper from machine names, local checkout
  paths, installation dates, private ticket references and local test
  results.
- Added a user-neutral availability and installation contract and
  restored real German umlauts.

### 1.0.0 (2026-08-19)

- Initial public version of the wrapper with dry run, approval step,
  rollback and validator boundaries.
- Boundary against `knappform`, `bilingual-doc-sync` and
  `llm-text-hygiene`.
