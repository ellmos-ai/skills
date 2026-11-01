---
name: sec-hardening
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Derives structural hardening proposals from findings, incident reports or assessments instead of one-off patches: bundle root causes, before/after architecture picture (ASCII), alternatives with trade-offs (effort, risk, effect), implementation order, evidence per proposal. Delivers a document and changes no code. Triggers: 'how do we harden this fundamentally', 'why do findings like this keep appearing', 'make the architecture safer', 'action plan from the incident'. Not for fixing a single finding (sec-fix) and not for acute defence (protection-shield)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, hardening, architecture, root-cause]
language: en
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-hardening banner">

# sec-hardening - structural instead of piece by piece

When findings of the same class keep recurring, the cause usually lies in the structure (no central validation, unchecked trust boundary, secrets in code). This skill proposes changes at that level. Contract: `sec-scan/references/contract.md` (findings §1/§2, rule 4 secrets, rule 5 cost).

## Input

`findings.json` (ideally `validated` or later), incident reports, assessments, `threatmodel.md` and knowledge of the code. No proposals without evidenced input; mark assumptions as such.

## Procedure

1. **Bundle root causes:** group findings by root, not by file: e.g. "every route builds SQL itself", "access check repeated in each handler", "configuration contains secrets". Name the finding ids per group.
2. **Sketch the current architecture** as an ASCII picture: trust boundaries, data flow, where the check does (not) happen today.
3. **Options per cause** (at least two, including "single patches only"): description, **effort**, **implementation risk** (regressions, migration), **effect** (which finding class disappears, which remains), dependencies. As a table.
4. **Recommendation** per cause with reasoning and a **target picture** (ASCII) next to the current one.
5. **Order:** what first because it closes several findings at once or is a prerequisite; what can wait. Intermediate steps that can ship on their own.
6. **Evidence per proposal:** finding ids, code locations (`path:line`), measurements. A proposal without evidence is marked as a hypothesis. No invented effort figures in time; only relative (small/medium/large) or given by the user.

## Output

One document (e.g. `hardening.md` in the scan directory, or in chat), sections: starting point, causes, current/target pictures, options, recommendation, order, open questions. **Changes no code**, creates no patches and commits nothing (rule 3); individual steps are carried out via `sec-fix` or normal development. No secret values in the document (rule 4).

## Changelog

### 0.1.0 (2026-10-31)
- Initial version.
