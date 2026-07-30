---
language: en
---

> **English** — Official English version of `bilingual-doc-sync`.

<img src="banner.png" width="100%" alt="bilingual-doc-sync banner">

# Bilingual-Doc-Sync — Keeping Parallel Language Versions Synchronized

## Overview & Purpose

Bilingual documents creepingly diverge: the actively edited version grows while the other becomes outdated — until "translation" is true in name only. This skill makes synchronization testing a defined process with one crucial prior determination: **Which version leads?** Without a primary language rule, every divergence becomes an ad-hoc decision and synchronization becomes unrepeatable.

## Workflow

### 1. Assess Inventory

- Are both (all) language versions present? If one is entirely missing → **catch up** (full translation of the primary version, not a rewrite).
- Check naming conventions (e.g., `DOCUMENT.md` + `DOCUMENT.en.md` or `_de`/`_en` suffixes) and align outliers — discoverability is half of synchronization.

### 2. Clarify Primary Language (Before Every Sync)

- The primary language is the version in which content work is actually done (often EN for research papers, often the native language for local documentation). It wins in case of conflict.
- **Reverse Transfer Exception:** If the secondary version handles something demonstrably better (clearer phrasing, corrected error), it is ADOPTED into the primary version — reverse transfer first, then synchronize normally. Check domain correctness before adopting a "prettier" formulation.

### 3. Check Parallelism

Structure first, then content:

1. **Outline Comparison:** Sections/headings of both versions side-by-side — missing, extra, or reordered sections are the major divergences.
2. **Section-by-Section Sampling** of matching outlines: Are statements, numbers, references, and examples identical? Particularly prone to divergence: changelogs, tables, numerical values, bibliographies/link lists, recently edited sections.
3. **Check Non-Translatable Invariants:** Code blocks, identifiers, formulas, and paths MUST be IDENTICAL in both versions (code is never translated).

### 4. Resolve

- Resolve divergences in the direction of the primary language (or after reverse transfer).
- Respect target language typography (in German real umlauts ä ö ü ß, no ae/oe/ue substitution; quotation mark conventions).
- Update metadata: version numbers, date fields, changelog entries in BOTH versions (the changelog itself is the most frequent point of divergence).

### 5. Document

Record results (what was divergent, what was adopted, what was reverse-transferred).
As a periodic run across an inventory: combine with the rotation framework (`rotation-check`) — one document (pair) per run, registry as memory.

## Extension: Expansion Audit (Should MORE Languages Exist?)

In addition to keeping existing versions synchronized, language maintenance includes asking whether a document/project deserves ADDITIONAL languages:

1. **Evaluate Suitability** instead of blindly translating: Target audience, international usability, store/web presence, content mobility. Not every internal document needs English; not every app needs five languages.
2. **Check Technical Preparation:** Is the target even prepared for language files/parallel versions (i18n structure, naming convention)? If not, THAT is the first task, not the translation.
3. **Document Findings, Do Not Mass-Translate Immediately:** Specific translation tasks go into the project-local TODO file; "no additional language makes sense" is a valid result to be recorded.
4. **QA for Caught-Up Versions:** Sample auto-generated translations against the primary version (Section 3) before considering them "present".

## Example & Application

```text
Task: "Check if the paper is synchronized in DE and EN."

1. Inventory: paper_en.tex (primary) + paper_de.tex present.
2. Outline: DE is missing the new section 4.2 (last EN revision); DE has a better proof paragraph in 3.1.
3. Reverse transfer: 3.1 phrasing domain-checked → adopted into EN.
4. Catch up: 4.2 translated into DE; numbers in Table 2 reconciled (DE had outdated values); bibliography made identical.
5. Registry entry: "paper-X | 2026-07-03 | de-en-sync | 3 divergences resolved, 1 reverse transfer | next check after next EN revision".
```

## Red Flags

| Mindset | Reality |
| --- | --- |
| "I'll just translate the differences from scratch" | Clarify primary language + reverse transfer question first — otherwise the better solution gets overwritten. |
| "The outline matches, so it's synchronized" | Numbers, changelogs, and references diverge first — deep sampling is mandatory. |
| "I'll translate code comments as well" | Code blocks and identifiers remain identical in both versions (English). |
| "I'll synchronize all documents in one go" | One pair per run (rotation framework) keeps synchronization verifiable. |

## Related Skills

- `rotation-check` — Framework for periodic runs over a document inventory.
- `workflow-extract` — When this check should be set up as a standing automation.

## Changelog

### 1.1.0 (2026-07-03)
- Added expansion audit (evaluate i18n suitability, technical preparation, QA for caught-up versions) — integrated instead of a separate i18n-coverage-audit skill (dedup decision).

### 1.0.0 (2026-07-03)
- Initial version. Abstracted from Codex automation "research-paper-de-en-synchronisationscheck", generalized to any parallel language versions (papers, READMEs, skills, website copy).
