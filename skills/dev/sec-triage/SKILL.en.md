---
name: sec-triage
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Converts existing findings (scanner reports, SARIF, GitHub code scanning, Dependabot, tickets) into the findings.json format of the ellmos security family, de-duplicates them by id, sets severity and priority against the repository's security policy (SECURITY.md) and links tickets. Static evaluation only. Use for 'classify these scan results', 'prioritise Dependabot alerts', 'import code scanning findings', 'sort the security finding backlog'. Finding new vulnerabilities: sec-scan. Refuting or reproducing: sec-validate. Report: sec-report."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, triage, sarif, dependabot, code-scanning, prioritisation]
language: en
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

> **English** — Official English version of `sec-triage`.

# sec-triage

Phase 4 of the ellmos security family. Contract: `sec-scan/references/contract.md` (files 1, lifecycle 2, severity 3, id 4, rules 6). Validator: `sec-scan/scripts/secfind.py`. **Static evidence only:** no new discovery (`sec-scan`), no runtime validation (`sec-validate`).

## Input

Existing findings: SARIF files or scanner reports, GitHub code scanning and Dependabot (export via `gh` or from the web UI, mind egress), tickets, audit lists. If a `findings.json` already exists it is continued, otherwise created (scan directory per contract 1). Preflight as `sec-scan` step 2 (ownership, lock check fail-closed).

## Procedure

1. **Map:** one entry per source finding. Normalise `rule` to dotted lowercase (`py.sql-injection`; put the original rule identifier and source into `description`), `cwe` from the source's tags, `location` from the alert, `severity` initially as the source states it, `status: candidate`.
2. **Secure the evidence:** code excerpt from the alert, otherwise read the spot in the named file and quote it. If no evidence can be established (file missing, line moved, alert without code), do **not** import the finding with invented evidence; list it in `coverage.limits` as not imported, with the reason. Mask secret values (contract 4). For dependency alerts: `rule` e.g. `dep.vulnerable-dependency`, `location` = manifest/lockfile line, `evidence` = that line; advisory id and affected version in `description`.
3. **De-duplicate:** build `id` via `python sec-scan/scripts/secfind.py id RULE PATH -`. Equal `id`s (also across several sources) merge into one finding, list the sources in `description`; on differing severity take the higher one and note it.
4. **Read the policy:** `SECURITY.md` (severity definitions, deadlines, supported versions, reporting channel) and any project decisions. If there is none, contract 3 applies and the result says so.
5. **Set severity and priority:** check severity against the policy and adjust with a reason; derive priority from severity, exposure and deadlines and set it in `priority` (`P0`-`P4`, P0 most urgent; map the policy's levels onto it), with the reason in `description`.
6. **Status:** per the validator, `triaged` requires `validatedBy.verdict == confirmed`. Already validated findings (`validated`) become `triaged`. Imported, not yet validated findings stay `candidate` with severity/priority set and go on to `sec-validate`. Exclude only if the policy explicitly covers it (e.g. unsupported version): `rejected` with `rejectedReason`.
7. **Tickets:** only if the user or the policy requires it: `ticket_writer.py` (never hand-picked ids) or GitHub issue/draft advisory; vulnerabilities in public repos as a **private** advisory draft, not a public issue. Record the reference in `ticket`. No secret values in tickets (contract 6.4).
8. **Coverage:** a pure import scans nothing. `scanned: []`, `notScanned` with an entry "import without own scan, repo not read" (so `complete: false`), `limits` with sources, import state and findings not imported. `provider.name` = source (e.g. `github-code-scanning`), `model` = `n/a`, `engine` = source tool.
9. **Check:** `python sec-scan/scripts/secfind.py validate findings.json coverage.json`, show the exit code. Then `sec-validate` for candidates, `sec-report` for the report.

## Changelog

### 0.1.0 (2026-10-31)

- First version: import, de-duplication by id, policy triage.
