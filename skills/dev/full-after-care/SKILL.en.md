---
name: full-after-care
version: 1.0.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-07-24
updated: 2026-07-30
aliases: [deep-after-care, repo-after-care-full, tiefe-repo-pflege, repo-tiefenpflege]
description: >
  Deep maintenance round for a published GitHub repository (Level 2): contains the
  full surface-after-care execution and supplements it with three expensive steps —
  preliminary legal assessment via the legal department with annual resubmission
  (opinion remains gitignored in the repo), cross-references to related repos across ALL
  organizations, and updating all languages at the app level, not just in docs. Use this skill
  on "full after care", "deep after care", "deep repo care", "large round", "thorough repo review",
  when a repo hasn't been checked in a while, before major releases, or when legal relevance,
  cross-references, or multilingualism are explicitly required. For the inexpensive, frequently repeated
  round use surface-after-care instead; for initial publishing use github-repo-care.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: dev
tags: [github, repo, maintenance, legal, i18n, cross-linking, organization, documentation]
language: en
status: active

dependencies:
  tools: [git, gh, rg]
  services: [GitHub]
  protocols: [surface-after-care]
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="full-after-care banner">

# Full After Care — The Deep Round (Synonym: Deep After Care)

## When to use this skill

Use it when a published repo needs to be reviewed **thoroughly**: not checked for a long time, before a major release, for legally relevant subjects, or when integration with other personal/organization projects is at issue.

The difference compared to the inexpensive round is effort, not care: Level 2 leaves the boundaries of the individual repo. It queries external sources (legal situation), inventories **all** organizations, and modifies the application itself (languages). That is why it runs less often — typically once per repo per year or on specific occasions.

## Workflow

### Level 1 first in full

Execute **`surface-after-care` completely** — including Step 0 (distribution channels), privacy gate, intent to publish, banners, actual vs. target comparison, README languages, visibility, organization entry, issues and PRs as well as commit, push, and surface parity. None of this is repeated or cut short here.

The following three steps are added on top. They generate changes to documentation and code — push them in the same cadence as described in Level 1, in thematically separate commits.

---

### 5. Preliminary legal assessment with annual resubmission

#### First: Is an assessment even due?

Check `_after-care/RECHTSCHECK.md` (the folder is gitignored, see below). If there is an audit date that is **less than one year** old, this step is **skipped** — even in the deep round. Obtaining a fresh assessment again costs time and money and brings no new insight.

If the date is **older than one year** or the file does not exist, an assessment is conducted. The reason for resubmission is not that the opinion degenerates, but that the **legal situation** changes: new regulations, updated thresholds, new case law, altered platform rules. A two-year-old legal opinion can be formally correct yet practically outdated.

Outside the annual cadence, a re-evaluation is due when the **subject matter** has changed: new data categories, new distribution channels, new business model, license change, new dependency with copyleft, expansion to another jurisdiction.

#### Is the repo legally relevant?

Not every project needs this. Triggers include:

- processes personal data, even if only locally
- accesses external services, websites, or APIs (terms of service, scraping)
- provides advice in regulated domains (law, medicine, tax, finance)
- carries external trademarks, names, or logos in title, docs, or UI
- contains dependencies with copyleft or unclear licensing, or bundles external content
- targets minors, processes payments, or falls under export/crypto regulations
- makes automated decisions about humans or is classified as an AI system

If none of this applies, record in the execution log **that it was checked and negative** — otherwise the next round will ask the same question all over again.

#### Obtaining an assessment

Use the legal department (Skill `law-checker`, Module `law-checker`) and present the concrete facts: what the application does, what data it touches, which channels it is distributed through, which licenses are included, who its audience is. The more concrete the facts, the more useful the references. The result is a preliminary assessment with paragraph citations — **not legal advice**; for serious risk, the result is a recommendation to obtain legal counsel, not the verdict itself.

#### Storage

```
_after-care/
├── LOG.md                    # Execution log of both levels
└── RECHTSCHECK.md            # Date, subject, result, conditions, resubmission
```

`_after-care/` belongs in `.gitignore`. This is not secrecy, but the same rule as in Step 2b of Level 1: internal working documents are not repo content. For a legal assessment, an additionally published risk analysis might be read as an admission and provide attackers with a roadmap. Alternatively, storage can take place outside the repo in a dedicated folder — the only important thing is that it is **findable** during the next run, otherwise the annual rule will not take effect.

Header of the file, keep machine-readable:

```markdown
# Legal check — <Project>
checked: 2026-07-24
subject: local file management, no cloud, no personal data of third parties
result: unproblematic
conditions: Note on MIT license of embedded library X in README
resubmission: 2027-07-24
```

What becomes **public** from the assessment are only the **consequences**: a license attribution, a disclaimer, a privacy notice, a clarified description of what the app does. These changes belong in the repo — the underlying rationale does not.

---

### 9. Cross-references across all organizations

Level 1 only asks if the repo is listed on the organization pages. Level 2 goes one level deeper: **Which individual repos from all owned organizations are linked to this one — and do both sides know about it?**

```bash
gh api user/orgs --jq '.[].login'
for ORG in $(gh api user/orgs --jq '.[].login'); do
  gh repo list "$ORG" --limit 200 --json name,description,updatedAt,isArchived,primaryLanguage
done
```

Value is created not by listing, but by recognizing relationships. Relevant types:

- **uses / is used by** — actual technical dependency in both directions
- **belongs to the same family** — shared product line, shared prefix, shared architecture
- **solves the same problem differently** — a user landing on one often wants to know about the other
- **predecessor / successor** — superseded projects need a signpost, otherwise users permanently stay on dead code
- **building block / composition** — library and the application using it

Set references **bidirectionally**. A one-way link is the most common mistake of this step: one adds a list of related projects to the maintained repo, while nothing is listed in the related projects. Anyone landing there will never find their way back.

The reciprocal reference is actually set in the target repo — following the **Dirty Tree Rule** from Step 11 of Level 1, summarized briefly: clean tree → separate commit and push; dirty in other files → commit path-specifically, do not push; dirty in the target file or active lock → do not touch. If the reference is not set, add it to the target repo's task list (`AUFGABEN.txt`/`TODO.md`), or if locked, only to your own execution log. Thus the round remains self-contained without risking external work states and without losing the reference.

Formulate references benefit-oriented, not as a mere list of names: "**project-b** — reads exports generated by this tool and creates reports from them" is useful, "see also: project-b" is not.

Archived and obviously dead repos are not linked — except as an explicit successor note pointing in the other direction.

This inventory is the most expensive part of the round. When many organizations and repos need to be checked, it pays to store the inventory results in the execution log so the next deep round of another repo can build upon it.

---

### Catching up all languages at the app level

Level 1 takes care of README language versions. Here it is about the **product itself**: UI text, messages, help screens, CLI output, error messages, store and registry descriptions.

First determine which languages the application already supports technically and how it manages them:

```bash
rg -l "gettext|i18n|locale|translations|LC_MESSAGES|\.po$|messages\.json" --hidden
fd -e po -e pot -e ftl . 2>/dev/null; ls locales/ i18n/ lang/ translations/ 2>/dev/null
```

Then close the gaps along three questions:

1. **Are languages missing** that the project should have? Standard languages are German, English, Spanish, Simplified Chinese, Japanese, Russian — for user-facing applications. For developer-focused libraries, English alone is often the right answer; an unnecessary language is permanent maintenance overhead, not a gain.
2. **Are existing languages complete?** After every feature cycle, secondary languages fall behind. New keys without translation often fall back to the primary language silently during runtime — therefore explicitly diff against the primary language here instead of relying on appearance.
3. **Is the language selector accessible to users?** A complete translation that nobody can enable is equivalent to none. Selector present, selection persistent, system language detected as default?

Adhere to the i18n mechanism established in the project and do not introduce a second one alongside it. Test results in the **actual user interface**, not just in resource files: strings that are too long break layouts, and missing character set support only shows up in rendering (missing CJK glyphs appear as empty boxes).

Finally, include the surfaces from Step 0 of Level 1: store and registry descriptions have their own language fields that do not automatically move with app translations.

## Execution log

Append an entry with the level `full` to `_after-care/LOG.md`:

```markdown
## 2026-07-24 — full
- Level 1 completed in full (see entry above)
- Legal check: due (last 2025-06-02) -> re-obtained, result unproblematic,
  condition regarding license note for library X implemented, resubmission set to 2027-07-24
- Cross-references: 4 orgs / 38 repos checked, 3 relationships found,
  set bidirectionally; reciprocal reference in repo-y open (active lock there)
- App level languages: ES added (312 keys), JA brought up to date,
  selector existed but was not persistent -> fixed
```

## Common mistakes

| Mistake | Correction |
|---|---|
| Re-obtained legal check although the last one was 3 months ago | Read date in `RECHTSCHECK.md` first — skip if under one year |
| Skipped legal check because "nothing changed" | The legal situation changes independently of the project; audit after one year |
| Committed legal opinion into repo | `_after-care/` belongs in `.gitignore`; only consequences become public |
| Negative legal relevance left undocumented | Even "not relevant" is a finding and belongs in the log |
| Cross-references set only in maintained repo | Set bidirectionally, otherwise it is a one-way street |
| Only checked own org | Level 2 means all organizations — that is what distinguishes it from Level 1 |
| References as a plain list of names | Explain benefit in half a sentence, otherwise nobody clicks |
| Added new language, but inaccessible in UI | Verify selector, persistence, and system language detection |
| Translation verified only in resource file | Verify in actual UI — layout breaks and missing glyphs only show up there |
| Forgot store/registry language fields | They do not migrate automatically with app translation |

## Final checklist

- [ ] `surface-after-care` fully completed (incl. push and surface parity).
- [ ] Legal relevance checked; result documented — even if negative.
- [ ] Legal check due? If yes: obtained, conditions implemented, resubmission set.
- [ ] `_after-care/` in `.gitignore`, legal opinion untracked.
- [ ] All organizations inventoried, relationships determined.
- [ ] Cross-references set bidirectionally, committed and pushed in target repos.
- [ ] Target repos skipped due to dirty tree or locks noted as open items.
- [ ] App languages complete, selector accessible, verified in UI.
- [ ] Store/registry language fields updated.
- [ ] Execution log entry with level `full` written.

## Changelog

### 1.0.0 (2026-07-24)
- Initial version. Level 2 of repo maintenance, building on `surface-after-care`.
