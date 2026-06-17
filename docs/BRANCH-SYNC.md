# Branch Sync Protection — Two-Order Branch Model

> This document describes how the sync infrastructure handles **branched skills**:
> locally customised forks of third-party or plugin-supplied skills, and locally injected
> family-router heads. Together these form a two-order branch model that prevents
> accidental overwrites and unintended publication.

---

## Overview: Two Orders

| Order | What it covers | Where documented |
|-------|---------------|-----------------|
| **1st order** — *creating* a branch | Copy a read-only plugin/third-party skill, add provenance frontmatter, edit only the copy | `~/.claude/skills/skill-explorer/references/skill-branching.md` |
| **2nd order** — *sync respects* branches | Both sync scripts automatically detect branched skills and leave them untouched / out of the public library | **This document** |

---

## Detection Contract

A local skill (`~/.claude/skills/<name>/`) is treated as **branched** when its `SKILL.md`
(fallback: `CONTENT.md`) satisfies **at least one** of the following:

| Signal | Meaning | Detected by |
|--------|---------|------------|
| Frontmatter line `origin: branch` (with or without quotes) | Customised fork of a third-party or plugin skill | Both scripts |
| Body contains `<!-- FAMILY-ROUTER:` | Locally injected family-router head (Head-Router-Branch) | Both scripts |

A skill that matches either signal is called **branched** throughout this document.
The two signals are not mutually exclusive; a skill can carry both (label: `fork+router`).

---

## Script 1 — `skill_sync.py` (Library → Master, can overwrite)

`skill_sync.py` is the deploy tool that copies skills from the public `.AI/.SKILLS` repo
into `~/.claude/skills/`. It is the only direction that can overwrite existing local content,
which makes branch protection here the most critical safety guarantee.

### `status` command

Branched skills appear in the drift report with a dedicated label:

```
[BRANCH:fork]        — provenance.origin: branch
[BRANCH:router]      — FAMILY-ROUTER marker
[BRANCH:fork+router] — both signals present
```

The summary line at the end counts branched skills separately (real output format):

```
  80 Skills: 26 OK, 22 abweichend, 12 nur Quelle, 20 nur Ziel, 20 gebrancht
```

### `deploy` command (bulk — no arguments)

Branched skills are **skipped automatically** — they receive the same treatment as skills
listed in `.sync-hold`:

```
UEBERSPRUNGEN (BRANCH:fork): deep-research-fork
UEBERSPRUNGEN (BRANCH:router): skill-finder
```

Running a bulk `deploy` is therefore safe even when branched skills exist locally.

### `deploy <name>` (named — single skill)

When a branched skill is named explicitly, the deploy is **skipped without `--force`**,
and a hint is printed (real output):

```
UEBERSPRUNGEN (BRANCH:router): 'counseling-basics' ist lokal gebrancht (nicht ueberschrieben). Deploy erzwingen mit --force.
```

### `--force` flag

`--force` overrides branch protection for the named skill and deploys the repo version,
overwriting the local branch. Use deliberately and only when you intentionally want to
replace the local customisation with the upstream version.

### Relation to `.sync-hold`

Branch protection builds on the existing `.sync-hold` mechanism. A branched skill is
treated as if it were on hold automatically — no manual `.sync-hold` entry is needed.
`--force` works the same way for both.

---

## Script 2 — `sync_skills.sh` (Master → Codex-Mirror + Library, additive)

`sync_skills.sh` copies skills outward from `~/.claude/skills/` into the Codex mirror
and the public `.AI/.SKILLS` library. It is additive (never overwrites existing entries).

### Library: branched skills are skipped

Branched skills are **not copied into the public library** (`ellmos-ai/skills`, MIT).
The log line:

```
Library-Skip (gebrancht/router-geschuetzt): deep-research-fork
```

The summary counter:

```
Branch-Skip (Library): 2
```

**Why:** Third-party forks contain upstream code that must not be redistributed under the
library's MIT licence without explicit permission. Locally injected router heads contain
private path/project references that have no place in a public catalogue.

### Codex mirror: unaffected

The private 1:1 Codex mirror (`~/.codex/skills/`) is **not subject to branch filtering**.
A branched skill that does not yet exist in the Codex mirror will be copied there as
normal (additive only — existing entries are never touched).

---

## Signal → Detection → Effect (summary table)

| Signal in `SKILL.md` | Detected as | `skill_sync.py` bulk deploy | `skill_sync.py` named deploy | `sync_skills.sh` Library | `sync_skills.sh` Codex |
|---|---|---|---|---|---|
| `origin: branch` | `fork` | skipped | skipped (hint + `--force`) | skipped | copied if new |
| `<!-- FAMILY-ROUTER:` | `router` | skipped | skipped (hint + `--force`) | skipped | copied if new |
| both | `fork+router` | skipped | skipped (hint + `--force`) | skipped | copied if new |
| neither | — | deployed normally | deployed normally | copied if new | copied if new |

---

## Why this exists

Two failure modes motivated the branch protection:

1. **`skill_sync.py deploy` wiping local edits.** A bulk deploy from the library would
   overwrite any locally customised family-router head or third-party fork with the
   unmodified upstream version.

2. **`sync_skills.sh` pushing private forks to the public repo.** A customised copy of a
   plugin-provided skill could inadvertently be committed to `ellmos-ai/skills` and
   published under MIT.

Branch protection at the sync layer makes both operations safe by default. `--force` is
the deliberate override when you consciously want to replace a local branch with the
upstream version.

---

## Related documents

- **1st-order (creating a branch):** `~/.claude/skills/skill-explorer/references/skill-branching.md`
- **Sync architecture overview:** `~/OneDrive/.SYNC/SKILL-SYSTEM-ARCHITECTURE.md`
- **Hold mechanism:** `.sync-hold` file in `~/.claude/skills/` (one skill name per line)
- **Conventions / frontmatter spec:** [`docs/CONVENTIONS.md`](CONVENTIONS.md)
