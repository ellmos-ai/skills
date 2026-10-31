---
name: ellmos-security
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Entry point and router of the provider-neutral ellmos security family (sec-*): places phases from threat model through scan, validation, triage, fix, verification and tracking to the report, and points to the right skill. Triggers: 'security review', 'check this repo for vulnerabilities', 'which security skill', 'security-check a PR', 'check a third-party plugin', 'SECURITY.md', 'disclosure'. Performs no checks itself; the work is done by the sec-* skills and the neighbour skills that are only linked here."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, router, umbrella, vulnerability, appsec]
language: en
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# ellmos-security - entry point of the security family

The family checks your own code for vulnerabilities and takes every finding from suspicion to a tracked, verified fix. All skills share one contract (file formats, lifecycle, severity, rules): `sec-scan/references/contract.md`. They run on Claude, Codex, Gemini and Kimi and depend on no vendor-specific scanner; such scanners are only adapters (table below).

## Phases

| Phase | Skill | When |
|---|---|---|
| Model | `sec-threat-model` | before the first scan: assets, trust boundaries, entry points |
| Scan | `sec-scan` | whole repo or a path |
| Scan (change) | `sec-diff-scan` | pull request, commit range, diff |
| Validation | `sec-validate` | confirm or refute each `candidate` independently |
| Triage | `sec-triage` | severity and priority against the policy |
| Fix | `sec-fix` | on request only, patch as a file |
| Verification | `sec-verify-fix` | does the patch close the hole, regression risk |
| Tracking | `sec-track` | ticket, issue or draft advisory |
| Report | `sec-report` | `report.md` and `findings.sarif` |

Cross-cutting: `sec-policy` (SECURITY.md), `sec-hardening` (structural measures), `sec-writeup` (disclosure report), `sec-supplychain` (third-party code before installing).

## What do I want?

- Check a repo -> `sec-scan` (for a new project, `sec-threat-model` first)
- Check a PR or diff -> `sec-diff-scan`
- Follow up an existing finding -> `sec-validate` -> `sec-triage` -> `sec-fix` -> `sec-verify-fix` -> `sec-track`
- Results as a report -> `sec-report`
- Set or review a repo's rules -> `sec-policy`
- Solve recurring finding classes fundamentally -> `sec-hardening`
- Report or disclose a flaw -> `sec-writeup`
- Install a third-party skill, plugin, MCP server or hook -> `sec-supplychain`

## Neighbour skills (maintained separately, part of the family)

- `security-tech-stack-check` + `tech-detect`: dependencies and CVEs against the measured tech stack.
- `protection-shield`: acute defence and recurring log/stack checks on your own systems.
- `repo-publish-check`: publication gate before making a repo public.
- If present on your system: a private security signpost and a skill for personal accounts/data (not code). They are not part of this public family.

## Provider adapters (contract §7)

| Provider | Native scan tool | How it joins | Cost note |
|---|---|---|---|
| Claude | `/claude-security` plugin | scan with it, map its output folder to `findings.json`/`coverage.json` | multi-agent plugin scan: estimate and warn first (rule 5); mind egress (rule 6) |
| Codex | `codex-security` plugin | same, from its scan output | as above |
| Gemini, Kimi | none | own procedure from `sec-scan` | tokens of the running session; estimate `deep` scans first |

Adapters never skip validation: mapped findings start as `candidate`. Exact mapping steps: `sec-scan`, Adapter section.

## Quick start

**Whole repo:** `sec-threat-model` (short) -> `sec-scan` -> `python scripts/secfind.py validate findings.json coverage.json` (script in `sec-scan`) -> `sec-validate` with another provider -> `sec-triage` -> `sec-report`.

**Pull request:** `sec-diff-scan` on the diff -> findings in the PR go straight to the author; if confirmed `sec-validate`, then as above. Check coverage in `coverage.json`: having seen only the diff does not mean "code is safe".

**One confirmed finding to a ticket:** `sec-triage` (severity against `SECURITY.md`) -> on request `sec-fix` -> `sec-verify-fix` with a different reviewer -> `sec-track` (preview, confirmation, write `finding.ticket` back).

## Shared rules (short form, the contract §6 is authoritative)

Own code only · lock before every write · patches instead of commits · no secret values in outputs · cost and egress warning before big runs · independent validation · a result without `coverage.json` is not a result.

## Changelog

### 0.1.0 (2026-10-31)
- Initial version of the router.
