---
name: sec-diff-scan
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Security scan of a change instead of the whole repository: PR, commit, branch diff or working-tree patch. Reviews changed lines together with their callers and callees, looks for regressions of known patterns and writes candidates to findings.json plus coverage.json listing diff and context files. Use for 'security review of this PR', 'check this diff for vulnerabilities', 'look at this before merge', 'did this change open something up'. Whole-repo scan: sec-scan. Refuting candidates: sec-validate. Report: sec-report."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, scan, diff, pull-request, regression, review]
language: en
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

> **English** — Official English version of `sec-diff-scan`.

# sec-diff-scan

Like `sec-scan`, but the scope is a **change**. Contract, file formats and rules: `sec-scan/references/contract.md`; schemas and validator in `sec-scan/schemas/` and `sec-scan/scripts/`. Preflight (ownership, lock check, egress, cost), candidate construction (`id` via `secfind.py id`, mask secrets) and validation work as in `sec-scan` > Procedure. Only the differences are listed here.

## Resolve the scope

One of these sources, always with the exact comparison point:

- PR: base and head commit of the PR (locally `git diff <base>...<head>`, or fetch the PR with `gh`; mind egress).
- Commit(s) or branch: `git diff <base>...<branch>`.
- Working tree: `git diff` and `git diff --staged` plus untracked files.

`findings.json` > `target.ref` = head commit (or `working-tree`), `target.scope` = the diff files. If the diff is empty, abort and say so.

## Procedure (instead of sec-scan steps 3-5)

1. **Read the diff**, not just the hunks: every changed file in the context of the affected function.
2. **Pull in context:** callers of changed functions (who feeds inputs in?), callees (where does the data flow?), configuration and tests that document assumptions. Use `threatmodel.md` if present; otherwise determine only the touched trust boundaries yourself, briefly (no full model; that is `sec-threat-model`).
3. **Review questions for changes:**
   - New entry points or new sinks (shell, SQL, filesystem, deserialisation, HTTP client)?
   - Was a check removed, weakened or bypassed (auth decorator, validation, escaping, permission check)?
   - Regression of known patterns: the same bug class as in earlier findings or elsewhere in the repo (`rule` values from an existing `findings.json`, if available).
   - New dependency or changed version in manifest/lockfile; secrets or tokens in the change; further configuration opening (CORS, debug, permissions).
4. **Report a finding only if the path really reaches the changed or touched spot.** Pre-existing flaws in the context that are unrelated to the change: record as `info` with a note in `description`, or name them in `coverage.limits`; they are not the subject of the diff.

## Coverage

`coverage.json`: `scanned` = the diff files (depth usually `read`) **and** the additionally read context files, `notScanned` = diff files that were not read (binary, generated, too large), with reason. `limits` states: "change only, rest of the repo not scanned". `complete` follows contract 5. A clean diff scan says nothing about the repository.

## Scope limits

No whole-repo scan (`sec-scan`), no runtime check (`sec-validate`), no fix. Output: `findings.json`, `coverage.json`, exit code of `secfind.py validate`.

## Changelog

### 0.1.0 (2026-10-31)

- First version: change scope, context pull-in, regression questions.
