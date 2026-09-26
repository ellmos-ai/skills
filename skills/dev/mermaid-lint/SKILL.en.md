---
name: mermaid-lint
version: 1.0.0
type: tool
author: Lukas Geiger + Claude
created: 2026-09-20
updated: 2026-09-20
aliases: [mermaid, mermaid-error, diagram-render-error, unable-to-render-rich-display]
description: Finds and fixes Mermaid diagrams that GitHub refuses to render ("Unable to render rich display"). Checks every ```mermaid block with the real Mermaid parser without a browser, then proves the result against the live GitHub page.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [mermaid, markdown, github, readme, diagram, lint, documentation]
language: en
status: active
visibility: public
dependencies: {'tools': ['node', 'git'], 'services': ['GitHub'], 'protocols': [], 'python': [], 'npm': ['mermaid', 'jsdom', 'playwright-core']}
---

<img src="banner.png" width="100%" alt="mermaid-lint banner">

# mermaid-lint

A Mermaid diagram with a syntax error shows **"Unable to render rich display"** on
GitHub instead of the graphic. It goes unnoticed locally because nothing checks the
block. This skill closes that gap.

## When to use

- A README or document shows a render error instead of a diagram on GitHub.
- Before publishing or releasing anything with diagrams in its documentation.
- After any Markdown rework that touches Mermaid blocks.
- Across many repositories, when it is unclear where things are broken.

## The two tools

### 1. `mermaid_lint.mjs` — syntax check without a browser

```
node mermaid_lint.mjs <repo-path> [...] [--json]
node mermaid_lint.mjs --from <list.txt> [--json]
```

Walks every `.md` file, extracts each ```mermaid block and runs it through
`mermaid.parse()` — **the same parser GitHub uses in the browser**. Exit 0 means every
block parses, exit 1 means at least one is broken. Output names file, block number,
line and the verbatim parser error.

`--from <file>` reads one path per line. Prefer it over many arguments: Windows paths
with backslashes are silently mangled by the Bash shell (`D:\code\my-repo`
becomes `D:codemy-repo`). Write paths with forward slashes.

A single process handles hundreds of repositories because Mermaid loads once.
No Puppeteer, no Chromium download.

### 2. `readback.mjs` — proof against the live page

```
node readback.mjs <github-url> [...]
```

Opens the pages in the installed Edge (no browser download) and counts real render
errors. Verdict per page: `OK`, `DEFEKT` (broken), `UNKLAR` (unclear) or
`KEIN-MERMAID` (no Mermaid).

## Three traps that make this skill necessary

**GitHub renders Mermaid inside sandboxed iframes** from
`viewscreen.githubusercontent.com`. The host page cannot see their content. Anything
that only inspects `document.body.innerText` or `msedge --dump-dom` reports zero errors
on **every** page — including a demonstrably broken one. `readback.mjs` therefore reads
all frames.

**A single broken verdict is not trustworthy.** While loading, GitHub briefly shows a
placeholder that looks like a render error. Measured 2026-09-20: the same page reported
`ERR=1` first, then `ERR=0` twice. `readback.mjs` retries negative verdicts
automatically; an `OK` is never retried.

**`mermaid.parse()` needs a DOM**, otherwise it fails on `DOMPurify.addHook` and
reports valid flowcharts as broken. `mermaid_lint.mjs` sets up a jsdom window first.
Any environment error that still slips through is collected separately under
`envIssues` and is **not** counted as a syntax error.

## Always check against a negative control

Before trusting a green result, point the tool at a state you know is broken — for
instance the commit before your fix:

```
node readback.mjs "https://github.com/<org>/<repo>/blob/<old-sha>/README.md"
```

If that also reports `OK`, your readback measures nothing. That is exactly how the
iframe trap above was found.

## Common causes and their minimally invasive fix

| Parser error | Cause | Fix |
|---|---|---|
| `Expecting '+', '-', '()', 'ACTOR', got 'loop'` | participant named like a reserved word: `loop`, `alt`, `opt`, `par`, `end`, `critical`, `break`, `rect`, `note` | Declare an alias: `participant L as Loop`, messages use `L`. The **displayed name stays** — do not rename. |
| `got 'PS'` in a flowchart | parentheses in a node label | Quote the label: `A["Start (here)"]` |
| `Lexical error ... Unrecognized text` | backticks or a colon in a label | Quote the label, drop the backticks |
| `Expecting 'SEMI', 'NEWLINE', 'EOF'` in `graph`/`flowchart` | `Note:` only exists in sequence and class diagrams | Move the note out of the block, put it below as a Markdown line so the information stays visible |
| `Expecting 'SOLID_OPEN_ARROW' ... got 'NEWLINE'` in a sequence diagram | **HTML entity** in the message text (`&lambda;`, `&Delta;`, `&ge;`). Neither the parentheses nor the `=` break it here — the entity's trailing `;` is read as a statement terminator and everything after it becomes a new statement. | Replace the entity with the literal character (λ, Δ, ≥), leave the rest untouched. Parentheses may stay. Never alter numeric values or their notation. |
| semicolon in a sequence message | read as a statement terminator | replace with ` - ` |

Inside **quoted flowchart labels** entities are harmless — the rule applies to sequence
messages only. `mermaid_lint.mjs` reports such entities as a separate `[WARN]` line
(field `warnings` in JSON) in addition to the parser error, because the parser only says
`got 'NEWLINE'` and never names the cause.

**Principle:** minimally invasive. Layout, node IDs, ordering and visible text stay
unchanged wherever possible. In scientific repositories this applies especially to
numeric values and their notation. Where EN/DE parity exists, keep both structurally
identical.

## Running across many repositories

1. Inventory via `gh repo list <org> --limit 200 --json name,isArchived,isPrivate,defaultBranchRef`.
2. Bring clones **up to the remote state** and take divergence seriously. Linting a
   stale clone measures the wrong state. If `git pull --ff-only` fails, check against
   `origin` instead of the working tree:
   `git archive origin/<branch> | tar -x -C <tempdir>` and lint that directory.
3. **Same-named repositories in different orgs** (typically `.github`) must not map to
   the same clone, or you check one repository nine times. On a name collision, clone
   shallow into `<org>__<repo>` and lint the fresh copy.
4. Check locks before any change (`lock_scan.py`, `LOCK*.txt` in the clone **and** at
   the OneDrive project path), set your own lock, remove it after the push.
   **Read the scope, not just the file's existence:** a `LOCK.team.*` whose
   `expires_after` has passed can be ignored; `LOCK.user.zenodo-upload.txt` blocks only
   the external Zenodo write and explicitly permits documentation changes. A
   `LOCK.user.until-winners-announcement.txt` (judging) blocks every push — check such
   a repository read-only and file the finding as a ticket.
5. Fix, lint until green, commit, `git pull --rebase`, push.
6. Readback with a negative control. Only then is it done.

## Setup

```
npm install mermaid jsdom playwright-core
```

In the scripts' folder or globally; `playwright-core` uses the installed Edge
(`channel: 'msedge'`) and downloads no browser of its own. Only the readback needs it —
the syntax check runs without it.

## Related

- `_tools/lint_mermaid.py` in GithubBot: older regex-based linter with `--fix`. It
  repairs known patterns automatically but **does not know about reserved words** and
  does not replace this skill. Sensible order: `mermaid_lint.mjs` to diagnose, then
  `lint_mermaid.py --fix` for bulk patterns, then lint again.
- `github-repo-care`: the overall protocol for repository care and publication.
