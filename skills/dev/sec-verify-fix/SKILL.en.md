---
name: sec-verify-fix
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Independently checks whether a security patch really closes the vulnerability (re-trace the source-to-sink path on the patched state, negative and regression test), rates the regression risk and whether automatic merging would be defensible (default: no for critical/high). Read-only review, applies nothing. Triggers: 'does the patch close the hole', 'review the patch', 'verify the fix', a finding in status fixed. Not for writing the patch (sec-fix), not for general code review."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, patch, review, verification, regression]
language: en
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-verify-fix - does the patch close the hole?

The "verify-fix" phase. Contract: `sec-scan/references/contract.md` (lifecycle §2, rule 7 in §6). Requires a finding with status `fixed` and `fix.patchFile`.

## Independence first

The reviewer is **not** the patch author (rule 7): preferably another provider (Claude <-> Codex), otherwise an independent top-tier subagent with fresh context that receives only the finding, the patch and the code - not the author's reasoning. If you have to check it yourself anyway, say so in the result; `verifiedBy` then stays empty and the status stays `fixed`.

## Procedure

1. **Apply the patch in a scratch copy** (never in the original); check the lock as in `sec-fix` (rule 2). If the patch does not apply cleanly, that already is the result.
2. **Re-trace the path:** walk the original source-to-sink path from `evidence` line by line on the patched state. Is the sink still reachable? Are there parallel paths (other callers, input variants, other encodings) the patch does not cover?
3. **Negative test:** a minimal, non-weaponised input that would have triggered the finding before must now be rejected or neutralised. Scratch copy only, own code only (rule 1). If a test cannot sensibly be run, report it as "not tested".
4. **Regression test:** project tests before/after; legitimate inputs still work. Name red or unrun tests.
5. **Rate the regression risk:** affected runtime paths and callers, changed contracts (signatures, formats, error behaviour), test coverage of the spot, reversibility (pure code patch vs. data migration/configuration). Level low/medium/high with reasons.
6. **Automatic merge?** yes/no with reasons. **Default no for critical/high**; yes only if the path is closed, negative and regression tests are green, risk is low and rollback is simple. The reviewer never decides alone; the repo's merge rules take precedence.

## Result

- **Closes:** yes / partly / no, naming the concrete spot that stays open. On "no"/"partly" the status stays `fixed` and work returns to `sec-fix`; the finding is not dropped.
- **On "yes":** `status: verified`, `fix.verifiedBy: "<provider>/<model>"` and `python scripts/secfind.py validate findings.json coverage.json` (script in `sec-scan`). Reasoning, risk level and merge recommendation go into the report to the user; the contract has no field for them, so do not invent one.
- Applies nothing, commits and pushes nothing (rule 3).

## Changelog

### 0.1.0 (2026-10-31)
- Initial version.
