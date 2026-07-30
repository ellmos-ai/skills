---
language: fr
---

<img src="banner.png" width="100%" alt="law-checker banner">

> **Français** — Documentation officielle complète traduite en français pour la compétence `law-checker`.



> **English** — Offizielle English-Version / Documento Oficial en English.


# law-checker (Legal Department) -- Pointer Skill (English)

This skill is a **thin pointer (wrapper)** to the standalone, public module
repository [`ellmos-ai/law-checker`](https://github.com/ellmos-ai/law-checker)
(MIT license, public). The actual skill lives there -- this repository only
links to it and documents installation, so the module is discoverable through
the central skill catalog.

## What the module does

`law-checker` produces source-grounded AI first-look legal assessments for
German law:

- **Statute registry** (`config.json`): togglable statutes; every statute
  claim must be backed by locally fetched official law texts (article or
  section, paragraph, sentence where needed, short quote, source, retrieval
  date).
- **Statute-embodiment agent** (`agents/gesetzbuch.md`): a generic agent that
  answers "from inside the statute" for any registered law -- scales to
  arbitrary statutes added to the registry.
- **Separate case-law layer:** court decisions are cited only after web
  verification (court, date, docket number, ECLI where available).
- **Risk and escalation workflow:** report format with a risk-level scale,
  deadline discipline, and a lawyer-specialty routing matrix.

## Boundaries (important)

- **AI-assisted first orientation only, not a substitute for individual legal
  advice, and not performed by a licensed lawyer.**
- Not a law firm, not a hosted legal service, not a deadline calendar.
- If real legal mail is involved (warning letter, official notice, lawsuit,
  deadline): secure the original document, note the deadline, and consult a
  qualified lawyer -- do not automate the matter.

## Installation (generic, no local paths)

1. Clone the module:
   ```bash
   git clone https://github.com/ellmos-ai/law-checker.git <clone-path>
   ```
2. Adopt `<clone-path>/SKILL.md` into your own skill environment (e.g.
   `~/.claude/skills/law-checker/` or the equivalent for your agent runtime).
3. Set the module path in the adopted `SKILL.md` and its references to
   `<clone-path>` -- do NOT commit real local paths or hostnames into a
   versioned skill environment.
4. Load the statute registry: `python <clone-path>/_tools/gesetze_fetch.py`
   (fetches the configured official statute texts; the texts themselves are
   deliberately not in the repo, to avoid redistributing stale portal
   snapshots).
5. For structure, license, and liability details, see the module repo's
   README.

## Origin of this pointer skill

This wrapper was added on 2026-07-23 as a showcase entry for the
`ellmos-ai/skills` repository. There is **no code duplication** -- maintenance
and versioning stay solely in the `ellmos-ai/law-checker` module repo.

## Journal des Modifications

### 0.1.0 (2026-07-23)
- Initial pointer skill for `ellmos-ai/law-checker`.