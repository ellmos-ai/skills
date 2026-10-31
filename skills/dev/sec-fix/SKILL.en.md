---
name: sec-fix
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Produces, ONLY on explicit request, a minimal security patch for a confirmed finding (status validated or triaged) - in a scratch copy or worktree, never in the original, as patches/<id>.diff without applying, committing or pushing. Triggers: 'fix this finding', 'patch for SEC-...', 'close this vulnerability'. Not for ordinary bug fixing (use bugfix-protocol), not for judging a patch (sec-verify-fix), not for finding issues (sec-scan)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, patch, fix, remediation]
language: en
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-fix - minimal security patch

The "fix" phase of the ellmos security family. Contract: `sec-scan/references/contract.md` (directory §1, lifecycle §2, rules §6). Only the application is described here.

## When (and when not)

- **Only on explicit request.** A scan or validation never triggers a fix by itself.
- **Only findings with status `validated` or `triaged`.** `candidate` goes through `sec-validate` first; `rejected` stays as it is.
- Ordinary non-security bug: `bugfix-protocol`. Whether an existing patch is good: `sec-verify-fix`. A structural cause behind several findings: `sec-hardening`.

## Procedure

1. **Read the finding and its surroundings:** `findings.json` (finding, `evidence`, `recommendation`), the affected file and the callers of the spot. Fix the cause, not the symptom at one call site; if several callers use the same unsafe function, patch the shared point.
2. **Check the lock (contract §6 rule 2):** `lock_scan.py --check-dir <repo> --json`; exit 0 = free, 1 = locked, anything else = unknown = stop; on a host without `lock_scan.py`, search the repo and its parent folders for `LOCK*.txt` instead (none = free, otherwise stop). Never touch `LOCK.user.*`.
3. **Working copy:** scratch copy or `git worktree` in a folder outside the original. Nothing is written to the original.
4. **Measure the baseline:** run the project's tests once before the patch and record the result (green/red, count). If there are no tests, say so - do not invent any.
5. **Patch minimally:** the smallest change that closes the source-to-sink path (validation, parameterisation, allowlist, escaping at the right place). No refactoring, no style fixes, no new dependencies without need. A regression test for the finding belongs in the patch if the project has tests.
6. **Measure again:** rerun the tests; report before/after honestly, including red tests and tests that did not run.
7. **Store the patch:** `git diff` of the working copy to `patches/<id>.diff` in the scan directory; check with `git apply --check` against the target state (changes nothing).
8. **Update the finding:** `status: fixed`, `fix.patchFile: patches/<id>.diff`; then `python scripts/secfind.py validate findings.json coverage.json` (script lives in `sec-scan`).

## Limits

- **No applying, no commit, no push (rule 3).** That needs a direct user order.
- **Secret findings:** the old value necessarily appears in the `-` lines of the diff. Keep the patch local in the scan directory, never in a ticket, chat or report; rotate the secret at the provider first (rule 4). Open: whether a masked diff would be usefully applicable - do not invent.
- The patch author does not review it: `sec-verify-fix` with a different reviewer (rule 7).
- Cost warning when fixing many findings at once (rule 5); work through them serially.

## Changelog

### 0.1.0 (2026-10-31)
- Initial version.
