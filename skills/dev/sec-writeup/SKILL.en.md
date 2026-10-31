---
name: sec-writeup
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Turns notes, PoC and findings into a self-contained, sceptically checked vulnerability report for coordinated disclosure: affected versions, reproduction steps, impact, fix, timeline. PoC kept minimal (no weaponised exploit), secrets redacted, every claim backed by evidence or marked unverified. Triggers: 'write the disclosure', 'vulnerability report', 'advisory text', 'report to the maintainer'. Not for the internal scan report (sec-report) and not for the ticket (sec-track)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, disclosure, writeup, advisory, reporting]
language: en
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-writeup - vulnerability report for disclosure

A report readable without prior knowledge and reproducible by someone who does not know the flaw. Contract: `sec-scan/references/contract.md` (rule 1 own code, rule 4 secrets, rule 6 egress, rule 9 report faithfully).

## Procedure

1. **Collect raw material:** finding (`findings.json`), notes, PoC, patch. Only vulnerabilities in your own or explicitly authorised code (rule 1).
2. **Check sceptically before writing:** try to refute every core claim yourself ("reachable without authentication", "remote code execution", "affects all versions"). Then mark each claim **evidenced** (with evidence: code location, test output, commit) or **unverified** (marked as such in the text). Severity only on the contract's scale (§3); a CVSS number or CVE identifier only if the user supplies it - never invent one.
3. **Determine affected versions from history** (introduction via `git log -S`/`git blame`, fix via commit/tag), do not estimate; state an uncertain boundary as open.
4. **Structure the report:** summary (2-3 sentences) · affected component and versions · attacker prerequisites · reproduction steps · impact (concrete, not exaggerated) · fix/workaround · timeline · credits/contact.
5. **Minimal PoC:** only as much as the maintainer needs to reproduce (input + expected misbehaviour). No weaponised exploit, no target systems, no persistence. When in doubt, describe instead of attaching code.
6. **Redact:** remove secrets, hostnames, internal paths and personal data; findings show the location only, never the value (rule 4). An exposed secret is rotated at the provider.
7. **Timeline with real dates only** (discovery, report, acknowledgement, fix). The disclosure deadline comes from the user or `SECURITY.md` (`sec-policy`), not from the skill.
8. **Delivery:** the draft stays with the user. Sending (email, advisory, platform) has outside effect and needs their explicit approval (rule 6); for public repos prefer a draft advisory or private reporting channel.

## Changelog

### 0.1.0 (2026-10-31)
- Initial version.
