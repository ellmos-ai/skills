---
name: sec-scan
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Provider-neutral security scan of an owned repository: threat model, split by trust boundary, targeted review per package (injection, authn/authz, secrets, crypto, deserialisation, paths, SSRF, configuration, vulnerable dependency use), candidates with evidence in findings.json and an honest coverage.json. Modes standard and deep. Use for 'security scan', 'check this repo for vulnerabilities', 'security review', 'full scan', 'import a scanner result into the ellmos format'. Includes the adapter for /claude-security and codex-security. Changes/PRs only: sec-diff-scan. Refuting candidates: sec-validate. Importing foreign reports: sec-triage. Report: sec-report."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, scan, vulnerabilities, sast, source-to-sink, cwe]
language: en
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-scan banner">

> **English** — Official English version of `sec-scan`.

# sec-scan

Core of the ellmos security family. The shared contract (phases, files, lifecycle, severity, rules, adapters) lives in `references/contract.md`, schemas in `schemas/`, the validator in `scripts/secfind.py` + `scripts/seclib.py` (standard library only). This skill cites the contract and does not repeat it. Neighbours: `sec-threat-model`, `sec-diff-scan`, `sec-validate`, `sec-triage`, `sec-report`.

## Modes

- **standard:** one pass, one model, one session.
- **deep:** several independent passes (different package order, split or model), merged by `id`. Only after a cost warning and user confirmation (contract 6.5).

## Procedure

1. **Target and scope:** repo, ref (commit SHA or `working-tree`), excluded paths. Assign a `scanId`. The scan directory is named `sec-scan-<scanId>/` (contract 1), sits under a base folder **outside the repo** and is created only after the preflight.
2. **Preflight:**
   - Own or authorised code? Otherwise abort (contract 6.1).
   - Lock check for the repo and the base folder of the scan directory: `python <lock_scan.py> --check-dir '<path>' --json`, capture the exit code immediately. 0 = free, 1 = locked, anything else (crash, unreadable output) = unknown = stop (contract 6.2). Call the interpreter explicitly, never "open" the script. If `lock_scan.py` does not exist on this host (no ellmos lock system), search the repo and its parent folders for `LOCK*.txt` instead: none = free (note it in the report), one or more = stop.
   - **State egress:** does code go to a provider (hosted review layer, third-party model)? Private repos stay in the local session (contract 6.6). **State cost**, and for `deep` wait for confirmation (6.5).
3. **Threat model:** is `threatmodel.md` present and current? If not, run `sec-threat-model`.
4. **Form packages:** split the repo by trust boundaries and entry points from the model; per package, files and investigation questions. Split very large packages instead of reading them superficially.
5. **Review each package** (source-to-sink: source -> transformation -> sink, read the countermeasures on the path too):
   injection (SQL, shell, template, LDAP/NoSQL), authn/authz and tenant separation, secrets in code, cryptography (algorithms, randomness, key handling), unsafe deserialisation, path/file access (traversal, upload, symlinks), SSRF and open redirect, insecure configuration (debug, CORS, defaults, permissions), use of known-vulnerable dependencies (patterns in code; advisory matching is `security-tech-stack-check`). Do not record findings the path does not support; suspicion without evidence belongs in `coverage.limits`, not in `findings`.
6. **Record a candidate:** `rule` dotted lowercase (`py.sql-injection`), `cwe` where one applies, `severity` and `confidence` per contract 3, `status: candidate`, `location`, `evidence` as quoted code/trace. **Mask secret values** (contract 4). Always derive `id` via `python scripts/secfind.py id RULE PATH -` (snippet on stdin), never by hand.
7. **Keep coverage honest:** `scanned` with depth `read` / `skimmed` / `pattern-only`, `notScanned` with reason (generated, vendored, too large, binary, unreachable), `limits` for method limits. `complete: true` only when `notScanned` is empty (contract 5). `unknown` is not "safe".
8. **Validate:** `python scripts/secfind.py validate findings.json coverage.json`, show exit code (0/1) and output. On errors, fix and rerun.
9. **Wrap up:** candidate count per severity, coverage state, next steps (`sec-validate`, then `sec-triage`, `sec-report`). A partial scan is reported as partial (contract 6.9).

## deep

At least two passes with different splits, each with its own candidate list. Merge by `id`: join equal `id`s (add evidence; on differing severity take the higher one and name the difference in `description`), add new `id`s. Coverage = union of paths read; `provider.model` lists every model involved.

## Adapter

An existing provider scanner can take over the scanning part (contract 7): **Claude** `/claude-security`, **Codex** `codex-security`. Gemini and Kimi have none and follow the procedure above.

1. Run the scanner after preflight (step 2); read its output files and map them field by field onto `findings.json` / `coverage.json`. The scanner's files and fields are not presupposed here; the mapping is built while reading the actual output and noted in `coverage.limits`.
2. **All findings start as `candidate`**, even if the scanner reports them as confirmed. An adapter never skips validation.
3. `provider.name` / `provider.model` after the scan, `provider.engine` = scanner name.
4. Take coverage from the scan report. If it yields none, set `complete: false` and add a `notScanned` entry "scanner coverage unknown" (the validator rejects `complete: false` without a `notScanned` entry; `limits` alone is not enough).
5. Rebuild `id`s via `secfind.py id` so findings coincide with those of other runs. Then step 8.

## Limits

No patching, no commits, no network scans (contract 6.1, 6.3). No runtime exploits; reproduction is `sec-validate`.

## Changelog

### 0.1.0 (2026-10-31)

- First version: modes standard/deep, preflight, packages, adapter.
