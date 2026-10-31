---
name: sec-track
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Makes validated security findings traceable: after preview and confirmation creates a ticket (ticket_writer.py), a GitHub issue or a draft security advisory (gh), checks for duplicates by finding id first, keeps secrets out of the text and writes the reference back into finding.ticket. Triggers: 'track this finding', 'ticket for SEC-...', 'create an advisory', 'put findings in the backlog'. No Linear/Jira. Not for technical reports (sec-report) and not for outward disclosure (sec-writeup)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, tickets, tracking, github, advisory]
language: en
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-track - make findings traceable

The "track" phase. Contract: `sec-scan/references/contract.md` (rule 4 secrets, rule 8 tickets in §6; field `ticket` in §2/schema). Only findings with status `validated` or later - `candidate` is not tracked.

## Choose the target

| Target | When | Tool |
|---|---|---|
| Ticket in the user's ticket system | default, private, no outside effect | `ticket_writer.py` from ticket-master |
| GitHub issue | only **private** repos or pure hardening gaps without an exploit path | `gh issue create` |
| Draft security advisory | vulnerability in a **public** repo | `gh api` (repository security advisories, draft) |

**Public repo + exploitable finding: never a public issue** - that would be a disclosure (egress, rule 6). Use a draft advisory or a private ticket there. No Linear, no Jira.

## Procedure

1. **Select:** which findings, which target. One by one, not as a bulk ticket, so every id gets its own reference.
2. **Duplicate check by finding id** (`SEC-<12 hex>`): is `finding.ticket` already set? Search the ticket directories for the id; on GitHub `gh issue list --state all --search "<id>"`. On a hit, use the existing reference and create nothing new.
3. **Draft the text:** id, title, rule/CWE, severity, location (`path:line`), short impact, recommendation, pointer to the patch file if any. **Never a secret value** (rule 4): the location only. No exploit detail beyond what is needed.
4. **Show a preview and wait for confirmation.** Only then create - tickets, issues and advisories have outside effect or cannot be recalled.
5. **Create:**
   - Ticket (never pick IDs by hand, rule 8): `python <ticket-master>/lib/ticket_writer.py --title "<SEC-id> <title>" --body "<text>" --project <project> --priority <level>`; the CLI prints the path of the created ticket file. The module docs sometimes say `--urgency`; the CLI itself knows `--priority` - read `--help` before use.
   - Issue: `gh issue create --repo <owner/repo> --title ... --body-file <file>`.
   - Advisory: draft via the GitHub REST interface for repository security advisories (`gh api`); check the exact fields in the GitHub docs before use (open, not pinned down here). Leave it as a draft, do not publish.
6. **Write the reference back:** `finding.ticket` = ticket path/id, `owner/repo#nr` or advisory link; then `python scripts/secfind.py validate findings.json coverage.json` (script in `sec-scan`).

## Changelog

### 0.1.0 (2026-10-31)
- Initial version.
