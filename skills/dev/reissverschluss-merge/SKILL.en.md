---
name: reissverschluss-merge
version: 1.0.0
type: skill
language: en
author: Claude (extracted from live-merge multi-repo PR session)
created: 2026-08-07
provenance:
  origin: live-session-extraction
  extracted: 2026-08-07
  method: skill-extractor
updated: 2026-08-07
description: >
  Zipper merge procedure for high-conflict branch merges: When two divergent branches
  or a PR and its target branch BOTH carry valuable, seemingly incompatible changes,
  do not arbitrarily pick one side. Compare section by section using a decision table
  (Take/Why), commit incrementally, and push only upon completion. Final escalation
  tier: Rebuild rather than merge — extract intent/functionality and rebuild cleanly.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
aliases:
  - zipper-merge
  - zipper-procedure
  - reissverschluss
tags: [git, merge, conflict, pull-request, branch, rebase, dev-workflow]
---

<img src="banner.png" width="100%" alt="reissverschluss-merge banner">

# Zipper Merge Procedure

## When to Use

Two branches of the same repository have **diverged significantly** and **both hold value** —
typically: `main` vs. `master` after parallel maintenance, an older PR against an evolved
target branch, or two agent/team branches with distinct fixes.
A default merge would either overwrite one side (`ours`/`theirs`) or produce a tangled
mess of unresolved conflicts. The zipper merge procedure solves this by making the teeth
of both sides **mesh section by section**: for each section, the provably better version wins
— or a reasoned mixture is produced.

**Not required** for trivial conflicts (one side clearly outdated, few hunks): simply merge
normally. The procedure becomes worthwhile when multiple files or sections require careful
evaluation.

## Phase 0 — Situation Assessment & Base Selection

1. **Review both sides completely** (not just conflict markers):
   `git log --oneline A..B` and `B..A`, `git diff A...B --stat`, then read divergent files
   from both branches.
2. **Choose base by reality, not timestamp.** The base must be the branch aligning with
   **published reality**: Registry status (npm/PyPI/…), deployed version, green CI, release tags.
   A branch with a newer date but no external reality alignment is material, not base.
3. **Check consistency of both sides** — often BOTH are internally inconsistent (e.g., base
   has version X without matching changelog; other side updates changelog but lags on version).
   Record these findings in the table, never ignore them.

## Phase 1 — Decision Table (The Core)

For each divergent section (file, block, field — as fine-grained as needed), create a row:

| Section | Take | Why |
|---|---|---|
| `package.json` → version | Base | matches public registry |
| `overrides` block | Counterpart | contains security bumps missing in base |
| ↳ entry `X` inside | **mix** | take counterpart entry, but bump to newer base version |
| Changelog `[Unreleased]` | **mix** | merge both blocks, eliminate duplicates |

Rules:

- **Facts over assumptions.** Every "Why" cell must rely on testable facts: registry query,
  test suite run, advisory database, or isolated test installation of the disputed file.
- **"Mix" is a legitimate verdict** — the zipper may interlock both teeth within a section.
- **Discard is a legitimate verdict** — what is unsupportable on both sides (dead badge,
  half-baked feature) gets removed. Half-way states are the worst outcome.
- The completed table serves as the **implementation contract** — sufficient to resume
  mechanically across agent turns or session handoffs.

## Phase 2 — Implementation: Sectional Commits, Final Push

1. Start a genuine merge on the base branch: `git merge <counterpart>`
   (deliberately WITHOUT `-X ours/theirs` — conflicts should remain visible).
2. Resolve conflicts **section by section** strictly following the table.
3. **One commit per logical section** (or for a single merge commit: document each resolution
   step in the commit message). Each commit message names the table verdict. This ensures every
   zipper tooth is traceable and revertible.
4. **Run tests after implementation** (suite, build, installability) — proceed only when green.
5. **Push only at the very end** — local history can be adjusted during the procedure; remote
   only sees verified final results.
6. **Close divergence without deletion:** fast-forward the lower branch to the result
   (`git checkout <counterpart> && git merge --ff-only <base>`). Both branch pointers then
   align without losing history.

## Escalation Tier — Rebuild Instead of Merge (Last Step)

When a zipper merge is no longer feasible, **do not merge — rebuild**: distill the
**intent and functionality** of the branch/PR (WHAT it intended to achieve, not HOW) and
implement it cleanly on the current baseline. Close the old branch/PR referencing the rebuild.

Escalation triggers (any single one suffices):

- Counterpart is **provably broken** (e.g. was never installable, build crashes).
- Conflict noise ≫ substance: small change smeared across hundreds of shifted lines.
- History is poisoned (e.g. same version number assigned to distinct content on both sides).
- PR is so old that its underlying API/context no longer exists.

## Common Pitfalls

- **Duplicate `[Unreleased]` changelog blocks:** merge cleanly, never drop one silently.
- **Both sides assigned same version number for different content:** verify registry before merge;
  record correction in unified changelog.
- **Merge as audit opportunity:** catch unnoticed issues (open advisories, dead links), but
  record them as separate commits.
- **Adopting solely because newer:** timestamps are not arguments; verify substance.
- **Force push reflex:** procedure works cleanly with standard merge + fast-forward.

## Related Skills

- `bugfix-protocol` — when a merge uncovers genuine defects.
- `skill-extractor` — origin of this skill (live session distillation).

## Changelog

### 1.0.0 (2026-08-07)
- Initial release. Extracted from live merge session on 2026-08-06 (main/master reconciliation
  across repositories with decision tables, rebuild escalation, fast-forward completion).
