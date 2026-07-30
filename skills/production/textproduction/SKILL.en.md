---
language: en
---

> **English** — Official English version of `textproduction`.


# Textproduction — Router (English)

This skill covers all text production formats. It routes to the
appropriate subskill — read the detailed instructions in the subfolder.

## Routing Table

| Subskill | Trigger Examples | Detailed Instructions |
|---|---|---|
| **text** | "Write a blog post", "5 LinkedIn posts", "Newsletter", "Product description", "Formal email", "Summarize X" | `text/WORKFLOW.md` |
| **storys** | "Write a screenplay", "Short story", "Create RPG adventure", "Character Sheet", "Worldbuilding" | `storys/WORKFLOW.md` |
| **pr** | "Draft press release", "Position paper", "PR package", "Generate PDF" | `pr/WORKFLOW.md` (+ `pr/press_compiler.py`) |

## Workflow & Procedure

```
1. User request → Routing table above → determine matching subskill.
2. Read detailed instructions in subfolder (WORKFLOW.md).
3. Select prompt pattern, fill placeholders, generate text.
4. Quality check (specified per subskill).
```

## Notes

- **User-neutral:** No personal data, API keys, or account details in the skill.
  Configuration (tonality, character limits, contact details for PR) is the user's responsibility.
- **PR Tool:** `pr/press_compiler.py` compiles press releases and position papers
  to PDF via LaTeX (pdflatex/xelatex). One-time setup: copy `pr/config.example.json`
  to `pr/config.json` and enter contact details.
- Optional style optimization: DeepL Write (free up to 500,000 characters/month).

## Changelog

### 2.0.0 (2026-06-22)
- Restructuring to router pattern: SKILL.md = entry point + routing table.
- Three subskills: text/ (6 text types), storys/ (4 narrative formats),
  pr/ (press release + position paper + LaTeX PDF compiler).
- press_compiler.py + LaTeX templates + config.example.json moved here from
  ai-media-editor/production/pr/ (SSOT).
- Updated related skills references to internal subskill paths.

### 1.0.0 (2026-06-22)
- Initial version. Extracted from ai-media-editor/production/text/WORKFLOW.md.
- Provenance: BACH agents/_experts/textproduction/ (MIT).