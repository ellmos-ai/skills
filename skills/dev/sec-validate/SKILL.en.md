---
name: sec-validate
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Tries to REFUTE every candidate in findings.json: trace the source-to-sink path, check reachability and countermeasures, calibrate severity, reproduce locally where that is safe. Sets validatedBy (confirmed/refuted/uncertain) and status validated or rejected with a reason. Use for 'verify the findings', 'weed out false positives', 'is this really exploitable', 'independent second check of the scan'. The validator should be a different provider than the finder. Finding new issues: sec-scan. Classifying foreign reports: sec-triage. Report: sec-report."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, validation, false-positives, exploitability, review]
language: en
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-validate banner">

> **English** — Official English version of `sec-validate`.

# sec-validate

Phase 3 of the ellmos security family. Contract: `sec-scan/references/contract.md` (lifecycle 2, severity 3, rules 6). Validator: `sec-scan/scripts/secfind.py`. Stance: **refute, do not confirm.** A candidate counts as `validated` only when the attempt to refute it fails.

## Input and independence

- Input: `findings.json` + `coverage.json` of a scan, candidates with `status: candidate` (or a selection of `id`s named by the user).
- **Independent validator (contract 6.7):** preferably a different provider than the scan's `provider.name` (Claude <-> Codex). Without one: an independent subagent of the top model class that does **not** read the finder's reasoning beforehand; record this in the result. Several providers or a fan-out: estimate cost first and warn the user (6.5). If code goes to a third-party provider, state the egress (6.6).
- Preflight as `sec-scan` step 2 (ownership, lock check, fail-closed).

## Per candidate

1. **Read it afresh:** read the code at `location` yourself; use the finder's `evidence` only as a hint.
2. **Trace the path:** source -> transformations -> sink, each step with file:line. A broken chain is grounds for refutation.
3. **Reachability:** which route, caller or authentication leads there? Dead code, test code, admin-only paths and internal callers lower the severity or refute.
4. **Look for countermeasures:** validation, escaping, parameterised queries, framework protection, configuration, upstream checks, permissions. Also elsewhere (middleware, wrappers).
5. **Name the attacker's preconditions** (anonymous, account, local access, specific configuration).
6. **Reproduce if safe:** only in a local copy or test environment, with synthetic data and stub services; e.g. a targeted unit test or a call to the function with an attack input. **Never** against third-party or production systems, no outbound network access, no real secrets, no destruction. If it cannot be reproduced safely, static argument suffices and verdict `uncertain` is allowed.
7. **Calibrate severity** per contract 3 (reachability times impact); reset `confidence`. Record a change as "severity old -> new: reason" in `description`.
8. **Write the verdict:**

| Verdict | Consequence in `findings.json` |
|---|---|
| `confirmed` | `status: validated`, `validatedBy: {provider, model, verdict: confirmed}`; path and any repro in `description`; add `impact` and `recommendation` |
| `refuted` | `status: rejected`, `rejectedReason` naming the concrete countermeasure or the break in the chain, `validatedBy.verdict: refuted` |
| `uncertain` | `status` stays `candidate`, `validatedBy.verdict: uncertain`, `description` states what is missing for a decision |

`validatedBy.provider` / `.model` are the **validator**, not the finder. The same provider as the finder triggers the validator warning "validated by the same provider"; it stays visible and is not suppressed.

## Wrap-up

`python sec-scan/scripts/secfind.py validate findings.json coverage.json`, show the exit code. Summary: count per verdict, severity changes, open `uncertain`. Continue with `sec-triage` (validated findings) and `sec-report`. No secret values in `description` or repro output (contract 6.4). No patching, no commit.

## Changelog

### 0.1.0 (2026-10-31)

- First version: refutation procedure, verdict mapping, independence.
