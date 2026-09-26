---
name: bilingual-doc-sync
version: 1.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-09-26
description: >
  Keep parallel language versions of a document (Paper DE/EN, README + README_de,
  SKILL.md + SKILL.en.md, website texts) synchronized: bring missing versions up to date,
  verify section parallelism, resolve divergences — with a clear lead-language rule and
  controlled back-transfer when the secondary version solves something better. Use this skill
  when asked "are DE and EN in sync?", "update the English/German version",
  "translation is outdated", for bilingual papers/READMEs/skills, or as a
  periodic check across a document inventory. Also includes the expansion audit:
  evaluating whether a project/document deserves ADDITIONAL languages (i18n suitability by
  target audience, technical preparation, no blind mass translation).

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: utilities
tags: [übersetzung, zweisprachig, synchronisation, paper, readme, i18n, dokumentation]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="bilingual-doc-sync banner">
# Bilingual-Doc-Sync — Keeping Parallel Language Versions Synchronized

## Purpose

Bilingually maintained documents subtly diverge over time: the actively edited version
grows while the other becomes outdated — until "translation" is true in name only. This
skill turns synchronization checking into a defined workflow with a crucial
upfront decision: **Which version is leading?** Without a lead language rule, every divergence
becomes a case-by-case debate and the alignment process becomes non-repeatable.

## Workflow

### 0. Detect Single-Language Content (BEFORE every alignment)

Divergence is not always "outdated" — sometimes it is **new, genuine content that so far
exists in only one version** (an external contribution/PR in a non-lead language, a change
that landed in the secondary version first, or content loss through a history rewrite or
similar). The original workflow only knew "enter it in EN or DE, then ship to all" — no
case for content that exists in only one version. Reference case: `ellmos-ai/skills` PR #1
added a Chinese-language discovery link only to README.md; a later history rewrite lost it
again because no step checked whether content exists that has no counterpart in any other
version (T-20260926-967984806).

- **Check, don't assume:** Before the actual alignment (Step 3), diff against the last
  known synchronized state (or directly against the other versions) and specifically look
  for content that is new in ONE version and has no counterpart in ANY other — not just for
  sections missing from the lead language.
- **Tool:** `scripts/check_language_parity.py <file1> <file2> [...]` extracts Markdown AND
  HTML links (`[text](url)`, `<a href="url">`, `<img src="url">`) from all supplied
  versions (links stay unchanged across translation and are thus a robust,
  language-independent indicator) and reports Exit 1 for any link that doesn't appear in
  ALL versions. Exit 0 means: no link-subset mismatch found — not proof of full parity, but
  a targeted Step-0 smoke test before the manual alignment. Links inside a
  `<!-- lang-only: <code> -->` block are only checked against files whose language code is
  named in the marker (detected from the filename, e.g. `README_zh.md` → `zh`, `README.md`
  → `en`) — they don't count as "missing from the other versions" there. The script also
  filters out `shields.io` badge URLs with encoded label text by default (the translated
  label often sits directly in the URL — expected translation variance, not real content
  loss; `--include-badges` turns the filter off). Non-UTF-8-readable files and missing
  arguments exit with code 2 and an error message, not a traceback.
- **Decision on a find:** single-language content is NEVER silently discarded. Three ways
  out, none of them silent deletion:
  (a) **translate and adopt into ALL versions** — the normal case for generally relevant
  content;
  (b) **deliberately scoped to one/several language(s)** ("lang-only") — when the content
  only applies to that audience (reference case T-20260926-967984806: a Chinese-language
  discovery link is not relevant to DE/ES/JA/RU readers; translating it into all six
  versions was itself the mistake — user correction after the first version of this step).
  Marker: **`<!-- lang-only: <code>[,<code>...] --> … <!-- /lang-only -->`** (HTML comment,
  invisible in Markdown renderers; comma-separate for multiple target languages, e.g.
  `zh,ja`). No established industry standard found for this narrow case (P-009 checked) —
  HTML comments are the most portable, invisibly-rendering choice for Markdown. Marked
  content is **neither translated nor reported as missing** during alignment;
  (c) **escalate as a conflict** when it's unclear whether the content is still wanted
  (e.g. seems to contradict the lead version) — ask the user/decision chain.
  In all three cases: never remove content from the version where it lives without comment,
  just because the others don't have it.

### 1. Inventory Check

- Are both (or all) language versions present? If one is completely missing → **catch up** (full
  translation of the leading version, not a rewrite).
- Check naming conventions (e.g., `DOCUMENT.md` + `DOCUMENT.en.md` or `_de`/`_en` suffixes)
  and align outliers — discoverability is half of synchronization.

### 2. Clarify Lead Language (before every alignment)

- The lead language is the version in which content work primarily takes place (often EN for papers,
  native language for local documentation). It takes precedence in case of conflicts.
- **Back-transfer exception:** If the secondary version demonstrably solves something better (clearer
  phrasing, corrected error), it is ADOPTED into the lead version — back-transfer first, then
  synchronize normally. Verify domain correctness before adopting a "prettier" phrasing.

### 3. Verify Parallelism

Structure first, then content:

1. **Outline comparison:** Sections/headings of both versions side by side —
   missing, extra, or reordered sections represent major divergences.
2. **Section-by-section sampling** of the matching outline: statements, numbers,
   cross-references, examples identical? Particularly prone to divergence: changelogs, tables,
   numerical values, bibliography/link lists, recently edited sections.
3. **Check non-translatable invariants:** Code blocks, identifiers, formulas, paths
   must be IDENTICAL in both versions (code is never translated).

### 4. Resolve Divergences

- Resolve divergences towards the lead language (or following back-transfer).
- Respect target language typography (e.g. proper quotation mark conventions).
- Update metadata: version numbers, date fields, changelog entries in BOTH
  versions (the changelog itself is the most frequent point of divergence).

### 5. Document Results

Record findings (what was divergent, what was adopted, what was back-transferred).
For a periodic run over an inventory: combine with the rotation framework
(`rotation-check`) — one document (pair) per run, using the registry as memory.

## Extension: Expansion Audit (Should MORE languages exist?)

In addition to keeping existing versions synchronized, language maintenance involves asking whether a
document/project deserves ADDITIONAL languages:

1. **Assess suitability** instead of blind translation: target audience, international utility,
   store/web presence, content portability. Not every internal document needs English;
   not every app needs five languages.
2. **Check technical preparation:** Is the target system prepared for language files / parallel
   versions (i18n structure, naming conventions)? If not, THAT is the first
   task, not the translation.
3. **Document findings, do not mass-translate immediately:** Place concrete translation tasks
   into the project-local TODO file; "no further language makes sense" is a valid,
   record-worthy result.
4. **QA for added versions:** Sample auto-generated translations
   against the lead version (Section 3) before considering them "present".

## Example

```text
Task: "Check if the paper in DE and EN is synchronized."

1. Inventory: paper_en.tex (leading) + paper_de.tex present.
2. Outline: DE is missing the new section 4.2 (latest EN revision); DE has a
   better proof paragraph in 3.1.
3. Back-transfer: 3.1 phrasing verified technically → adopted into EN.
4. Catch-up: 4.2 translated into DE; numbers in Table 2 reconciled (DE had
   outdated values); bibliography aligned identically.
5. Registry entry: "paper-X | 2026-07-03 | de-en-sync | 3 divergences resolved,
   1 back-transfer | next check after next EN revision".
```

## Red Flags

| Thought | Reality |
| --- | --- |
| "I'll just translate the differences fresh" | Clarify lead language + back-transfer question first — otherwise the better solution gets overwritten. |
| "The outline matches, so it's synchronized" | Numbers, changelogs, and references diverge first — deep sampling is mandatory. |
| "I'll translate code comments as well" | Code blocks and identifiers remain identical in both versions (English). |
| "I'll synchronize all documents in one go" | One pair per run (rotation framework) keeps alignment verifiable. |

## Related Skills

- `rotation-check` — Framework for periodic runs over a document inventory.
- `workflow-extract` — When this check should be set up as a standing automation.

## Changelog

### 1.2.0 (2026-09-26)
- Added Step 0 "Detect Single-Language Content" (T-20260926-967984806): divergence can be
  new, not-yet-propagated content rather than staleness; three ways out (translate
  everywhere / mark lang-only / escalate as conflict), never silent deletion. New
  `<!-- lang-only: <code> -->` marker for content deliberately scoped to an audience.
- Added `scripts/check_language_parity.py` + `scripts/test_check_language_parity.py`: finds
  links present in only a subset of language versions (Markdown and HTML links), respects
  the lang-only marker, filters shields.io badge noise, exits with code 2 (not a traceback)
  on non-UTF-8 files.

### 1.1.0 (2026-07-03)
- Added expansion audit (evaluate i18n suitability, technical preparation, QA for
  added versions) — integrated instead of a separate i18n-coverage-audit skill
  (deduplication decision).

### 1.0.0 (2026-07-03)
- Initial version. Abstracted from Codex automation
  "research-paper-de-en-synchronisationscheck", generalized to any parallel
  language versions (papers, READMEs, skills, website texts).
