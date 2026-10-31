# ellmos security contract (v1)

Shared by every `sec-*` skill. Skills cite this file instead of repeating it.
Clean-room: this contract was written from public skill names and open standards (SARIF 2.1.0, CWE). Its structure follows common practice for scan results (document type, schema version, scan id, findings plus coverage); content, field set and wording are independent, and no vendor scan-tool text, schema or code was copied.

## 1. Scan directory

One scan = one directory `sec-scan-<scanId>/` outside tracked source (default location: `<tmp>/ellmos-security/<repo>/sec-scan-<scanId>/`).

| File | Written by | Content |
|---|---|---|
| `threatmodel.md` | `sec-threat-model` | assets, trust boundaries, entry points, attacker goals |
| `findings.json` | `sec-scan`, `sec-diff-scan`, then updated by later phases | `schemas/finding.schema.json` |
| `coverage.json` | scan skills | `schemas/coverage.schema.json` |
| `report.md` / `findings.sarif` | `sec-report` | human report / SARIF 2.1.0 |
| `patches/<id>.diff` | `sec-fix` | proposed patch, never applied by the skill |

Validate after every write: `python scripts/secfind.py validate findings.json coverage.json` (exit 0 = ok).

## 2. Finding lifecycle

`candidate` → `validated` → `triaged` → `fixed` → `verified`; `rejected` from any state (needs `rejectedReason`, stays in the log, SARIF marks it suppressed).

| Status | Set by | Requires |
|---|---|---|
| candidate | scan | evidence, location |
| validated | `sec-validate` | `validatedBy.verdict = confirmed`; validator should be a **different provider** than the finder (same provider only warns) |
| triaged | `sec-triage` | severity decided against the policy and `priority` (P0..P4) set; the validator requires both a confirmed validation and `priority` |
| fixed | `sec-fix` | `fix.patchFile` |
| verified | `sec-verify-fix` | `fix.verifiedBy` (a reviewer other than the fix author) |
| rejected | validate / triage | `rejectedReason` |

Imports without an own scan (`sec-triage` from Code Scanning, Dependabot, tickets): `provider.name` = source, `provider.model` = `n/a`, `provider.engine` = source tool, `scanned` empty, one `notScanned` entry "import without own scan" so `complete` is false. Imported findings stay `candidate` (with severity and `priority` set) until `sec-validate` confirms them; only then they become `triaged`. `priority` is `P0`..`P4` (P0 most urgent), set by `sec-triage`.

## 3. Severity

| Level | Meaning |
|---|---|
| critical | remotely exploitable without credentials **and** leads to code execution, broad data read/write or disclosure of secrets; or direct compromise of secrets/data at scale |
| high | exploitable by an authenticated or adjacent attacker with serious impact; or exploitable without credentials but limited to integrity/availability of individual records (e.g. an unauthenticated delete) |
| medium | exploitable under specific conditions or limited impact |
| low | hardening gap, small impact |
| info | observation, no exploit path |

Severity is reachability times impact: state both in `description` when you deviate from the table. A `rejected` finding keeps its original severity (SARIF marks it suppressed). The provider family is the part of `validatedBy.provider` before the first `-` (`claude-subagent-independent` is family `claude`), so a descriptive provider string never switches the same-provider warning off.

Confidence (`high|medium|low`) says how sure the finder is that the path is real; it is not severity.

## 4. Finding id and rules

- `id = make_id(rule, path, snippet)` (`scripts/seclib.py`): stable across line shifts and whitespace. **Snippet convention** (so independent scanners get the same id): the single source line of the dangerous call or assignment, exactly as in the file; for a secret, that line with the value replaced by `<masked>`. **Path convention:** `location.path` and the `PATH` given to `make_id` are repo-relative with `/` separators and without a leading `./` (`make_id` normalises backslashes and a leading `./`; the validator rejects absolute paths, drive letters and backslashes).
- `rule` is a dotted lowercase name (`py.sql-injection`, `js.path-traversal`, `any.hardcoded-secret`); add `cwe` where one applies.
- `evidence` quotes the code or trace that proves the path. **Never put a secret value in evidence** - quote the line with the value masked. The validator rejects common key patterns.

## 5. Coverage is part of the result

A result without `coverage.json` is not a result. "No findings" is only meaningful with `complete: true`; otherwise state what was not scanned. `unknown` is not "safe".

## 6. Shared ellmos rules (all sec-* skills)

1. **Own code only.** Scan repositories the user owns or is authorised to test. No third-party systems, no port scans.
2. **Locks.** Where the ellmos lock system exists (the script `lock_scan.py` is present), run `lock_scan.py --check-dir <dir> --json` before any write: exit 0 = free, 1 = locked, anything else (crash, unreadable output) = unknown = stop (fail-closed). On a host without that script, look for `LOCK*.txt` files in the target and its parent folders instead: none = free (say so in the report), any = stop. Never touch `LOCK.user.*`.
3. **Patches, not commits.** `sec-fix` writes a patch file. Applying, committing or pushing needs a direct user order.
4. **No secrets in outputs.** Reports, tickets, memory notes and chat name the *location* of a secret, never the value. A leaked secret is rotated at the provider; removing it from history is not enough.
5. **Cost warning.** `deep` scans, multi-provider validation and fan-outs: estimate first, warn, wait for the user.
6. **Egress.** State where the code goes. Provider-hosted review layers send diffs to the provider; private repos default to the local session only.
7. **Independent validation.** Prefer another provider for `validate` and `verify-fix` (Claude <-> Codex). Without one, use an independent top-tier subagent and record that in `validatedBy`.
8. **Tickets.** Tracking uses `ticket_writer.py` (never hand-picked ids) or GitHub issues / draft advisories; the finding stores the reference in `ticket`.
9. **Report outcomes faithfully.** A failed or partial scan is reported as such.

## 7. Provider adapters

| Provider | Native scanner | How it joins |
|---|---|---|
| Claude | `/claude-security` plugin | scan with it, then map its output folder to `findings.json` / `coverage.json` (`sec-scan` > Adapter) |
| Codex | `codex-security` plugin | same, mapped from its scan output |
| Gemini, Kimi | none | follow the own procedure in `sec-scan` |

An adapter never skips validation: mapped findings start as `candidate`.
