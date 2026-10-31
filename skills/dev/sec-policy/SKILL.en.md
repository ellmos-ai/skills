---
name: sec-policy
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Defines, reviews or updates a repo's SECURITY.md (scope, excluded areas, required security properties, reporting channel, response times, supported versions) and checks its claims against the actual code. The policy is the basis for sec-triage. Triggers: 'create/check SECURITY.md', 'security policy', 'what counts as a vulnerability here', 'define the reporting channel'. Not for findings (sec-scan), not for disclosure reports (sec-writeup)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, policy, security-md, disclosure]
language: en
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-policy - define and review SECURITY.md

The policy says what counts as a vulnerability in this repo. `sec-triage` rates findings against it (contract `sec-scan/references/contract.md` §2: `triaged` = severity and priority decided against the policy). Without a policy, triage guesses.

## Content of a SECURITY.md

| Section | Question it answers |
|---|---|
| Supported versions | which versions receive security fixes? |
| Scope | which components, interfaces, deployments are meant? |
| Excluded | what explicitly does not count (test code, examples, known limitations, attacks that require access to the host system)? |
| Required security properties | what must the project guarantee (e.g. "no secrets in the repo", "network input is validated", "plugins run without file access outside X")? Triage measures against this. |
| Reporting channel | where to report: placeholder `<security-contact>`; or GitHub's private vulnerability reporting if enabled on the repo. **Do not invent an address.** |
| Response times | acknowledgement, assessment, fix target - values come from the maintainer, not the skill; mark suggestions as such. |
| Disclosure | coordinated, deadlines from the maintainer; point to `sec-writeup`. |

## Procedure

1. **Read what exists:** current `SECURITY.md`, README, dependency and build files, code structure (entry points, auth, file access, network, plugin mechanisms).
2. **Claim versus evidence:** check every promise in the policy ("all input is validated", "no telemetry", "versions X.y are maintained") against the code or releases. A contradiction is a finding (`sec-scan`) or a correction of the policy, never silently ignored. What cannot be checked: mark as unverified.
3. **Draft or diff:** new SECURITY.md or a change proposal with open points (`<...>` placeholders) for maintainer decisions. If an answer is missing, ask instead of guessing.
4. **Placement:** draft in chat or in the scan directory. The repo is only written on a direct user order (check the lock, rule 2; no commit/push, rule 3). The file never contains secrets, host paths or private contacts (rule 4).

## Boundaries

Technical hardening proposals: `sec-hardening`. Checking a repo's readiness for publication: `repo-publish-check`.

## Changelog

### 0.1.0 (2026-10-31)
- Initial version.
