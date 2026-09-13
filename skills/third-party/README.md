# Third-party skills

Foreign skills we redistribute — either **vendored unmodified** or as an
**improved fork**. Everything here belongs to someone else; we only pass it on
because its licence allows it, and we say so on every single skill.

Material we merely *use and recommend* does **not** live here. It stays out of
this repository entirely (see `skills/_reference/`, gitignored) — using
something and redistributing it are different questions, and only the second one
needs permission.

## What a skill in this areal must carry

```yaml
---
name: some-foreign-skill
description: >
  What it does.
third_party: true
license: MIT                 # SPDX identifier
upstream: https://github.com/someone/their-repo
---
```

Plus the upstream **`LICENSE` file** next to the skill. That file is the legally
graspable unit — a frontmatter field is a claim, the licence text is the thing
itself.

These five fields are the whole contract. The nine house fields every other
skill carries (`standalone`, `bach_compatible`, `provenance`, `visibility`, …)
are *our* convention, not an external standard: no foreign skill has them.
Requiring them would mean editing foreign frontmatter, which inflates every diff
against upstream, makes resyncing painful, and turns "vendored unmodified" into
a fiction. Under Apache-2.0 it would even trigger the obligation to document
modifications — for a change nobody wanted.

`category:` may keep its real value here. The folder says where a skill *comes
from*, not what it is *about*: a foreign video skill stays `utilities` even
though it sits under `third-party/`.

## Which licences are allowed

Maintained in `build_public_registry.py` so the gate and the documentation
cannot drift apart.

- **Permissive** — MIT, Apache-2.0, BSD-2/3-Clause, ISC, 0BSD, Unlicense,
  CC0-1.0, CC-BY-3.0/4.0. Keep the notice, that is all.
- **Copyleft** — GPL, LGPL, AGPL, MPL-2.0, CC-BY-SA-4.0. Allowed, but they bind
  derived work to the same terms. A fork of one of these stays under that
  licence; it does not become MIT because this repository is MIT. The upstream
  `LICENSE` file is mandatory here, and the repository root LICENSE notes that
  subdirectories may differ.
- **Not allowed** — anything else. Unlicensed material means *all rights
  reserved*, so it must not be redistributed at all. Non-commercial (NC) clauses
  are excluded on purpose: "non-commercial" is not cleanly separable in this
  setup, and a rule nobody can apply reliably is worse than no rule.

## Fork or verbatim?

Both live here. The difference belongs in the skill, not in a second folder:
record what you changed. Apache-2.0 requires exactly that when you modify, and
whoever reads the skill later needs to know which parts are ours.

## If the privacy gate trips on foreign text

Upstream documentation may legitimately contain what our content scan hunts for
— an example API key, a concrete path in someone's tutorial. Add the file to
`THIRD_PARTY_SCAN_EXCEPTIONS` in `testing/privacy_gate.py`, with a reason.

**Never fix it by editing the upstream text.** That contradicts "vendored
unmodified", inflates the diff, and under Apache-2.0 creates a documentation
obligation. An exception is honest; a silent edit is not.

## What the gate enforces

Folder and flag must agree — a skill in this directory declares
`third_party: true`, and a skill declaring it lives in this directory. The
redundancy is deliberate, but it only helps because `testing/privacy_gate.py`
compares the two. Two switches that nobody compares are precisely what once left
a private skill readable on GitHub.

On top of that: a declared licence, from the allow-list, with its `LICENSE` file
present, and an `upstream` pointer. Fail-closed, and here without the
counter-argument that applies to `visibility` — redistributing without
permission is a legal wrong, failing to redistribute is an inconvenience.
