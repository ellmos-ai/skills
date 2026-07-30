---
language: en
---

<img src="banner.png" width="100%" alt="full-after-care banner">

> **English** — Official English version of `full-after-care`.


# Full After Care — Deep Maintenance Round (Synonym: Deep After Care) (English)

## When to Use This Skill

Use it when a published repository needs a **fundamental** review: not checked for a long time, before a major release, for legally relevant subjects, or when integration with other internal projects is a topic.

The difference from the light round (`surface-after-care`) is effort, not diligence: Stage 2 leaves the boundaries of the individual repo. It queries third-party sources (legal situation), inventories **all** organizations, and intervenes in the application itself (languages). Therefore, it runs less frequently — typically once per repo per year or on demand.

## Workflow

### Stage 1 completely first

Execute **`surface-after-care` completely** — including Step 0 (distribution surfaces), privacy gate, release intention, banners, actual-vs-target comparison, README languages, visibility, organization entry, issues and PRs, as well as commit, push, and surface parity. None of this is repeated or abbreviated here.

The following three steps build on top of it. They generate changes to documentation and code — push them at the same pace as described in Stage 1, in thematically separate commits.

---

### 5. Initial Legal Assessment with Annual Follow-up

#### First: Is an assessment even due?

Check `_after-care/RECHTSCHECK.md` (the folder is gitignored, see below). If there is a check date that is **less than one year** ago, this step is **skipped** — even in the deep round. Obtaining a fresh assessment again costs time and money and brings nothing new.

If the date is **older than one year** or the file does not exist, a check is conducted. The reason for the follow-up is not that the legal opinion degrades, but that the **legal situation** changes: new regulations, altered threshold values, new case law, changed platform rules. A two-year-old opinion can be formally correct and practically outdated.

Outside the annual cycle, a reassessment is due if the **subject matter** has changed: new data categories, new distribution channel, new business model, license change, new dependency with copyleft, expansion to another jurisdiction.

#### Is the repo legally relevant?

Not every project needs this. Triggers include:

- processes personal data, even if only locally
- accesses third-party services, websites, or interfaces (terms of use, scraping)
- provides advice/information in regulated fields (law, medicine, tax, finance)
- carries third-party trademarks, names, or logos in name, docs, or UI
- contains dependencies with copyleft or unclear license, or distributes third-party content
- targets minors, processes payments, or falls under export/crypto rules
- makes automated decisions about people or is classified as an AI system

If none of these apply, document in the run log **that it was checked and negated** — otherwise the next round will ask the same question from scratch.

#### Obtain assessment

Use the legal department (Skill `law-checker`, module `law-checker`) and present the concrete facts: what the application does, what data it touches, through which channels it is distributed, which licenses are involved, who it targets. The more concrete the facts, the more useful the citations. The result is an initial assessment with statutory references — **not legal advice**; for serious risks, the result is a recommendation to seek legal counsel, not the verdict itself.

#### Storage

```
_after-care/
├── LOG.md                    # Run log for both stages
└── RECHTSCHECK.md            # Date, subject matter, result, conditions, follow-up
```

`_after-care/` belongs in `.gitignore`. This is not hiding things, but the same rule as in Step 2b of Stage 1: internal working documents are not repo content. For a legal opinion, an additionally distributed public risk analysis could be interpreted as an admission and provide attackers with a roadmap. Alternatively, storage can take place outside the repo in a dedicated folder — the only important thing is that it is **findable** during the next run, otherwise the annual rule cannot take effect.

Keep the file header machine-readable:

```markdown
# Legal Check — <Project> (English)
checked: 2026-07-24
subject: local file management, no cloud, no third-party personal data
result: unproblematic
conditions: notice of MIT license of embedded library X in README
follow-up: 2027-07-24
```

What becomes **public** from the assessment are only the **consequences**: a license attribution, a disclaimer, a privacy notice, a clarified description of what the app does. These changes belong in the repo — the rationale behind them does not.

---

### 9. Cross-references across all organizations

Stage 1 only asks if the repo is listed on organization pages. Stage 2 goes one level deeper: **Which individual repos from all internal organizations are connected to this one — and do both sides know about it?**

```bash
gh api user/orgs --jq '.[].login'
for ORG in $(gh api user/orgs --jq '.[].login'); do
  gh repo list "$ORG" --limit 200 --json name,description,updatedAt,isArchived,primaryLanguage
done
```

The value does not come from listing, but from recognizing relationships. Relevant types:

- **uses / is used by** — real technical dependency in both directions
- **belongs to the same family** — shared product line, shared prefix, shared architecture
- **solves the same problem differently** — a user landing on one often wants to know about the other
- **predecessor / successor** — superseded projects need a signpost, otherwise users permanently land on dead code
- **building block / composition** — library and the application using it

Set references **bidirectionally**. A one-way street is the most common mistake of this step: adding a list of related projects in the maintained repo, while nothing is written in the related projects. Anyone landing there will never find their way back.

The backlink is actually set in the target repo — according to the **dirty tree rule** from Step 11 of Stage 1, in short: clean tree -> separate commit and push; dirty in other files -> commit exact path, do not push; dirty in target file or active lock -> do not touch. If the reference cannot be set, put it in the target repo's task list (`AUFGABEN.txt`/`TODO.md`), or if locked, only in your own run log. This keeps the round self-contained without risking third-party work states and without losing the reference.

Formulate references benefit-oriented, not as a mere list of names: "**project-b** — reads exports generated by this tool and creates reports from them" is useful, "see also: project-b" is not.

Archived and obviously dead repos are not linked — except as an explicit successor notice in the opposite direction.

This inventory is the most expensive part of the round. If many organizations and repos need to be checked, it pays off to log the repo inventory results in the run log so that the next deep round of another repo can build upon it.

---

### Sync all languages at app level

Stage 1 handles README language versions. Here it is about the **product itself**: UI texts, messages, help, CLI output, error messages, store and registry descriptions.

First determine which languages the application technically already knows and how it manages them:

```bash
rg -l "gettext|i18n|locale|translations|LC_MESSAGES|\.po$|messages\.json" --hidden
fd -e po -e pot -e ftl . 2>/dev/null; ls locales/ i18n/ lang/ translations/ 2>/dev/null
```

Then close the gaps along three questions:

1. **Are languages missing** that the project should have? Standard languages are German, English, Spanish, Simplified Chinese, Japanese, Russian — for user-facing applications. For developer-facing libraries, English alone is often the right answer; an unnecessary language is an ongoing maintenance burden, not a gain.
2. **Are existing languages complete?** After every feature cycle, secondary languages lag behind. New keys without translations often fall back to the primary language silently during operation — therefore explicitly diff against the primary language instead of relying on visual inspection.
3. **Is language selection accessible to users?** A complete translation that nobody can activate acts like none. Switcher present, selection persistent, system language detected as default?

Adhere to the i18n mechanism established in the project and do not introduce a second one alongside it. Test results in the **real interface**, not just in resource files: long strings break layouts, and missing font support only shows up during rendering (missing CJK glyphs appear as empty boxes).

Finally, include the surfaces from Step 0 of Stage 1: Store and registry descriptions have their own language fields that do not automatically move with the app translation.

## Run Log

Add an entry with stage `full` to `_after-care/LOG.md`:

```markdown
## 2026-07-24 — full
- Stage 1 completely executed (see entry above)
- Legal check: due (last 2025-06-02) -> newly obtained, result unproblematic,
  condition license notice library X implemented, follow-up 2027-07-24
- Cross-references: 4 orgs / 38 repos checked, 3 relationships found,
  set bidirectionally; backlink in repo-y open (active lock there)
- App-level languages: ES added (312 keys), JA updated,
  switcher was present but not persistent -> fixed
```

## Common Mistakes

| Mistake | Correction |
|---|---|
| Legal check obtained again even though last one was 3 months ago | Read date in `RECHTSCHECK.md` first — under one year is skipped |
| Legal check skipped because "nothing changed" | The legal situation changes independently of the project; check after one year |
| Legal opinion committed to repo | `_after-care/` belongs in `.gitignore`; only consequences become public |
| Negated legal relevance not documented | Even "not relevant" is a finding and belongs in the log |
| Cross-references only set in maintained repo | Set bidirectionally, otherwise it's a one-way street |
| Checked only own org | Stage 2 means all organizations — that's what distinguishes it from Stage 1 |
| References as plain name list | Explain value in half a sentence, otherwise nobody clicks |
| New language created but not accessible in UI | Test switcher, persistence, and system language detection |
| Translation checked only in resource file | Test in real interface — broken layouts and missing glyphs only show up there |
| Store/registry language fields forgotten | They do not move automatically with the app translation |

## Final Checklist

- [ ] `surface-after-care` completely executed (incl. push and surface parity).
- [ ] Legal relevance checked; result documented — even if negated.
- [ ] Was legal check due? If yes: obtained, conditions implemented, follow-up set.
- [ ] `_after-care/` in `.gitignore`, opinion not tracked.
- [ ] All organizations inventoried, relationships determined.
- [ ] Cross-references set bidirectionally, committed and pushed in target repos.
- [ ] Target repos skipped due to dirty tree or lock noted as open items.
- [ ] App languages complete, switcher accessible, tested in UI.
- [ ] Store/registry language fields synced.
- [ ] Run log entry with stage `full` written.

## Changelog

### 1.0.0 (2026-07-24)
- Initial version. Stage 2 of repo maintenance, building on `surface-after-care`.