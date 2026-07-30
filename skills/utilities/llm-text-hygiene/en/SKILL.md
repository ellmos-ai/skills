---
language: en
description: Clean AI artifacts, chat residue, placeholders, and LLM style patterns from final texts, and audit AI disclosures.
---

> **English** — Official English version of `llm-text-hygiene`.

<img src="banner.png" width="100%" alt="llm-text-hygiene banner">

# LLM-Text-Hygiene — Remove AI residue from finished texts

## Overview & Purpose

AI-assisted texts accumulate residue that remains invisible in draft form and only becomes embarrassing in the published document: snippets of conversation from the chat session, stage directions that break out of the argumentative structure, thank-yous to the language model, leftover placeholders, pushy LLM style patterns — and an AI disclosure that is missing, misplaced, or no longer true. This skill is the systematic cleaning pass before publishing: inspect, clean conservatively, correct the disclosure. **It never changes the substance** — it removes what is not part of the work.

## Audit Checklist

Five finding classes, from clear-cut (fix directly) to sensitive (mark only):

### 1. Chat Residue and Stage Directions (clear-cut → remove/fix)

Sentences that belong to the CREATION of the text, not to the text itself: "As discussed, we keep this part in the paper because...", "Here is the revised section:", "I'd be glad to add...", leftover prompt fragments, meta-comments to the client/requester.
**Detection principle:** The sentence falls out of the text and argument structure — it addresses a conversation situation instead of the reader. When deleting, check if a substantive core needs to be saved (transfer explanation into a footnote/body text).

### 2. Placeholders and Work-in-Progress Markers (clear-cut → resolve)

`[TODO: …]`, `[insert reference]`, `XXX`, `<example here>`, empty sections with headings, "(source?)". Resolve them or — if unresolvable — transfer them as open tasks into the project TODO and remove from the deliverable.

### 3. LLM Acknowledgments and Anthropomorphic Expressions (clear-cut → remove)

Thanking ChatGPT/Claude/Gemini & Co. does not belong in the acknowledgments section — tools are not thanked, their usage is declared in the AI disclosure. Likewise, remove anthropomorphic phrasing about the tool ("the AI kindly suggested").

### 4. AI Disclosure (verify → correct)

- **Present?** If the document was created with AI assistance and the venue/project requires or foresees a disclosure: does the section exist?
- **Correct?** Does it describe the actual usage (neither understated nor exaggerated)? Does it use the disclosure schema of the project/venue if defined (e.g., tiered levels)?
- **Properly placed?** At the venue-standard location (methods/acknowledgments area/dedicated section), identical across all language versions.

### 5. LLM Style Patterns (sensitive → fix clear cases only, mark the rest)

Formulaic transitions ("In summary, it can be said", "It is important to emphasize"), bullet-point inflation where running text belongs, "not only ... but also" chains, em-dash density, hedging phrases, and in English, well-known markers (including "delve", "tapestry", "it's worth noting"). **Caution:** Style is author territory — smooth out only unambiguous formulaic phrasing; present everything else as a findings list to the author instead of rewriting the text. A human-sounding text is not the goal of the skill; the goal is a text free of foreign bodies.

## Workflow

1. **Clarify scope:** Which deliverables (files), which language versions? ALWAYS apply changes synchronously across all versions (cross-check: `bilingual-doc-sync`).
2. **Mechanical scan:** Full-text search for signal patterns (table below) — cheap, finds class 2/3 and parts of class 1 reliably.
3. **Reading pass:** Read the document along the argument structure — class 1 findings are recognised structurally (sentence addresses conversation instead of reader). Check especially: section beginnings/ends, acknowledgments, introduction/conclusion (residue lands there first).
4. **Clean up:** Fix classes 1–3 directly (conservatively, preserving substance), correct class 4, output class 5 as a findings list; smooth out directly only unequivocal cases.
5. **Document:** Record what was found/changed/marked — for papers with versioning obligations, note whether a new version/re-upload is necessary.
6. **Periodic pass over a repository:** Combine with `rotation-check` (one document/project per run, registry as memory).

## Signal Patterns for Mechanical Scanning

| Class | Search Pattern (DE) | Search Pattern (EN) |
| --- | --- | --- |
| Chat Residue | "wie besprochen", "wie gewünscht", "hier ist", "gerne", "im Chat", "wie du sagtest", "lassen wir" | "as discussed", "as requested", "here is the", "I have added", "per your" |
| Placeholders | `TODO`, `XXX`, `[…einfügen]`, `<…>`, "Quelle?" | `TBD`, `[insert`, `placeholder`, `citation needed` |
| LLM Thanks | "Dank an ChatGPT/Claude/Gemini", "mithilfe von KI erstellt" (outside disclosure) | "thanks to ChatGPT/Claude", "grateful to the AI" |
| Style Markers | "zusammenfassend lässt sich", "es ist wichtig zu betonen", "nicht nur … sondern auch" | "delve", "tapestry", "it's worth noting", "in conclusion" |

The table is a starting point, not a filter substitute: patterns deliver candidates; the decision is made in context (steps 3–4). For purely mechanical character hygiene (emoji scan, control characters, broken umlauts), use existing tools — encoding damage is `encoding-fix` territory, not this skill's.

## Example & Application

```text
Request: "Check the paper for AI residue before upload."

1. Scope: paper_de.tex + paper_en.tex.
2. Scan: 1× "as discussed" (EN, section 4), 1× "[TODO: insert reference Smith]" (both),
   acknowledgments mention "valuable help from Claude".
3. Reading pass: In the introduction, a sentence directly addressing the reviewer
   ("We address this objection as requested in 3.2") → stage direction.
4. Fixes: Stage direction deleted (content was already in 3.2), TODO transferred as a task
   to TODO.md + placeholder removed, LLM thank-you deleted, instead
   AI disclosure section clarified regarding actual usage — all in DE and EN.
5. Note: Substantive change → new paper version required, entered into TODO.md.
```

## Red Flags

| Thought | Reality |
| --- | --- |
| "I'll make the text flow better while I'm at it" | Substance and voice belong to the author — the skill removes foreign bodies, it does not polish style. |
| "Style marker found → delete" | Class 5 is marked, not automatically rewritten; smooth out only unambiguous formulaic phrasing. |
| "The German version is enough" | Residue often resides in only ONE version — always check all language versions and keep them in sync. |
| "Remove disclosure, then it's clean" | Backwards: Remove LLM thank-yous, put correct disclosure IN — concealing is not hygiene. |

## Related Skills

- `encoding-fix` — Byte/encoding repair (mojibake); this skill works on the content level.
- `bilingual-doc-sync` — Keeping language versions in sync where fixes are applied.
- `rotation-check` — Scaffolding for periodic runs across a document repository.
- `textproduction` — Text generation (this skill is the QA afterwards).

## Changelog

### 1.0.0 (2026-07-04)
- Initial version. Abstracted from Codex automation "research-llm-muster-check"
  (chat fragments in papers, LLM thank-yous, AI disclosure) and generalized to arbitrary
  deliverable texts; audit catalog extended with placeholders, style patterns, and scan signal table.
