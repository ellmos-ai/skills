---
name: sec-report
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Produces the security report report.md (grouped by severity, coverage section with gaps, rejected findings separate, summary without sugar-coating) and findings.sarif (SARIF 2.1.0) from findings.json and coverage.json via the script render_report.py. Use for 'write the security report', 'summarise the scan result', 'export SARIF', 'report for code scanning'. Aborts on invalid data; a partial scan is reported as partial. New findings: sec-scan / sec-diff-scan. Verifying: sec-validate. Classifying: sec-triage."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, report, sarif, coverage, findings]
language: en
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

> **English** — Official English version of `sec-report`.

# sec-report

Final phase of the ellmos security family. Contract: `sec-scan/references/contract.md` (files 1, severity 3, coverage 5, rules 6). The script imports `seclib` from the sibling folder `sec-scan/scripts` (in the repo `skills/dev/` and in a flat deployment `~/.claude/skills/`; both folders must sit side by side). Standard library only.

## Usage

```
python scripts/render_report.py FINDINGS COVERAGE OUTDIR [--lang de|en]
```

Call the interpreter explicitly. `OUTDIR` is the scan directory; check the lock first as in `sec-scan` step 2 (fail-closed). Result: `OUTDIR/report.md` and `OUTDIR/findings.sarif`. Exit codes: 0 = written, 1 = input unreadable or invalid (**nothing** written), 2 = wrong usage. Show exit code and output. The default report language is German; use `--lang en` for English.

## Behaviour

- **Validates first** (`seclib.validate_findings`). Errors are listed and no report is produced from broken data. Fix the cause first (`sec-scan`, `sec-validate`), then render again.
- **report.md:** header (target, ref, scanner) · summary · warnings · findings by severity (critical to info) with location, confidence, status, validator, evidence, description, impact, recommendation, ticket · **rejected findings separate** with reason · coverage (scanned with depth, not scanned with reason, limits).
- **Honesty (contract 5, 6.9):** `complete: false` appears at the very top as "PARTIAL SCAN". No findings plus incomplete coverage reads "NOT a clean result". Only "No findings with complete coverage" may read like a clean result. Warnings, such as the same provider for finder and validator, appear in the report.
- **findings.sarif:** SARIF 2.1.0 from `seclib.to_sarif`; rejected findings stay in the log as `suppressions`. Usable directly as a code-scanning upload. Uploading is a publication to the outside and needs a user order.

## Before handing it on

Read the report back: no secret values (the validator only catches common patterns; contract 6.4), locations only. Reports in ticket systems and chats likewise without values. Vulnerabilities in public repos go through the private reporting channel (SECURITY.md), not a public issue.

## Test

`python -m pytest tests -q -p no:cacheprovider` in the skill folder (report, SARIF, partial scan, backtick evidence, negative case without output).

## Changelog

### 0.1.0 (2026-10-31)

- First version with `render_report.py`: report.md and findings.sarif from validated data.
