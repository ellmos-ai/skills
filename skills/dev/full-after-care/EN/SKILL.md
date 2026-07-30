---
language: en
---

> **English** — Official English version of `full-after-care`.

# Full After Care — Deep Maintenance Round (Synonym: Deep After Care)

## When to Use This Skill

Use it when a published repo needs to be gone through **thoroughly**: not checked for a long time, prior to a major release, in case of legally relevant matters, or when integration with other internal projects is a topic.

The difference from the lightweight round is the effort, not the care: Level 2 leaves the boundaries of the single repo. It queries external sources (legal status), inventories **all** organizations, and intervenes in the application itself (languages). That is why it runs less frequently — typically once per repo per year or on a case-by-case basis.

## Workflow

### Level 1 Completely First

Execute **`surface-after-care` completely** — including Step 0 (distribution surfaces), Privacy Gate, publication intent, banner, actual-vs-target alignment, README languages, visibility, organization entry, issues and PRs, as well as commit, push, and surface parity. None of this is repeated or abbreviated here.

The three following steps are added on top. They generate changes to documentation and code in their own right — push them in the same rhythm as described in Level 1, in thematically separate commits.

---

### 5. Initial Legal Assessment with Annual Resubmission

#### First: Is an Assessment Even Due?

Check `_after-care/RECHTSCHECK.md` (the folder is gitignored, see below). If an inspection date is listed there that is **less than one year ago**, this step is **skipped** — even in the deep round. Obtaining a fresh assessment again costs time and money and brings nothing new.

If the date is **older than one year** or if the file does not exist, an assessment is conducted. The reason for resubmission is not that the opinion degrades, but that the **legal situation** changes: new regulations, altered threshold values, new case law, changed platform rules. A two-year-old legal opinion can be formally correct and practically obsolete.

Outside of the annual rhythm, a re-evaluation is due if the **subject matter** has changed: new data categories, new distribution channel, new business model, license change, new dependency with copyleft, expansion into another jurisdiction.

#### Is the Repo Legally Relevant?

Not every project needs this. Triggers include, among others:

- processes personal data, even if only locally
- accesses third-party services, websites, or APIs (terms of service, scraping)
- provides information in regulated fields (law, medicine, taxes, finance)
- includes third-party trademarks, names, or logos in the name, documentation, or UI
- contains dependencies with copyleft or unclear licenses, or bundles third-party content
- targets minors, processes payments, or falls under export/cryptography regulations
- makes automated decisions about people or is classified as an AI system

If none of this applies, record in the execution log **that it was checked and determined to be negative** — otherwise the next round will ask the exact same question again.

#### Obtaining the Assessment

Use the legal department (skill `law-checker`, module `law-checker`) and present the concrete facts: what the application does, what data it touches, through which channels it is distributed, which licenses are included, who it is aimed at. The more concrete the facts, the more useful the findings. The result is an initial assessment with paragraph citations — **not legal advice**; in case of serious risk, the result is a recommendation to consult a lawyer, not the judgment itself.

#### File Storage

```
_after-care/
├── LOG.md                    # Laufprotokoll beider Stufen
└── RECHTSCHECK.md            # Datum, Gegenstand, Ergebnis, Auflagen, Wiedervorlage
```

`_after-care/` belongs in `.gitignore`. This is not playing hide-and-seek, but the same rule as in Step 2b of Level 1: internal working documents are not repo content. For a legal opinion, there is the added aspect that a publicly bundled risk analysis can be read as an admission and provides attackers with a roadmap. Alternatively, storage can take place outside the repo in a dedicated folder — what matters is that it is **findable** during the next run, otherwise the one-year rule does not apply.

Keep the file header machine-readable:

```markdown
# Rechtscheck — <Projekt> (Deutsch)
geprüft: 2026-07-24
gegenstand: lokale Dateiverwaltung, keine Cloud, keine personenbezogenen Daten Dritter
ergebnis: unbedenklich
auflagen: Hinweis auf MIT-Lizenz der eingebetteten Bibliothek X im README
wiedervorlage: 2027-07-24
```

What becomes **public** from the assessment are only the **consequences**: a license attribution, a disclaimer, a privacy notice, a clarified description of what the app does. These changes belong in the repo — the underlying reasoning does not.

---

### 9. Cross-References Across All Organizations

Level 1 only asks whether the repo is listed on the organization pages. Level 2 goes one level deeper: **Which individual repos from all internal organizations are related to this one — and do both sides know about it?**

```bash
gh api user/orgs --jq '.[].login'
for ORG in $(gh api user/orgs --jq '.[].login'); do
  gh repo list "$ORG" --limit 200 --json name,description,updatedAt,isArchived,primaryLanguage
done
```

The value comes not from listing them, but from recognizing relationships. Relevant types:

- **uses / is used by** — actual technical dependency in both directions
- **belongs to the same family** — shared product line, shared prefix, shared architecture
- **solves the same problem differently** — a user landing on one often wants to know about the other
- **predecessor / successor** — superseded projects need a signpost, otherwise users permanently land on the dead version
- **building block / composition** — library and the application that uses it

Set references **bidirectionally**. A one-way street is the most common mistake in this step: a list of related projects is added to the maintained repo, and nothing is written in the related projects. Anyone landing there will never find their way back.

The backlink is therefore actually set in the target repo — according to the **dirty tree rule** from Step 11 of Level 1, briefly summarized: clean tree → separate commit and push; dirty in other files → path-exact commit, do not push; dirty in target file or active lock → do not touch. If the link is not set, it belongs in the target repo's task list (`AUFGABEN.txt`/`TODO.md`), or if locked, only in your own execution log. This keeps the round self-contained without risking external working states and without losing the reference.

Formulate references with user utility in mind, not as a mere list of names: "**project-b** — reads exports generated by this tool and creates reports from them" is useful, "see also: project-b" is not.

Archived and obviously dead repos are not linked — except as an explicit successor hint in the opposite direction.

This inventory is the most expensive part of the round. If there are many organizations and repos to inspect, it pays to store the result of the repo inventory in the execution log so that the next deep round of another repo can build upon it.

---

### Update All Languages at Application Level

Level 1 takes care of README language versions. Here it is about the **product itself**: UI texts, messages, help docs, CLI output, error messages, store and registry descriptions.

First determine which languages the application already supports technically and how it manages them:

```bash
rg -l "gettext|i18n|locale|translations|LC_MESSAGES|\.po$|messages\.json" --hidden
fd -e po -e pot -e ftl . 2>/dev/null; ls locales/ i18n/ lang/ translations/ 2>/dev/null
```

Then fill in the gaps, guided by three questions:

1. **Are languages missing** that the project should have? Standard languages are German, English, Spanish, Simplified Chinese, Japanese, Russian — for user-facing applications. For developer-focused libraries, English alone is often the right answer; an unnecessary language is a permanent maintenance burden, not a benefit.
2. **Are the existing languages complete?** After every feature cycle, secondary languages fall behind. New keys without translations often fall back to the primary language in operation and thus go completely unnoticed — so diff targetedly against the primary language here instead of relying on appearances.
3. **Is the language selection accessible to users?** A complete translation that nobody can enable is effectively useless. Switcher present, selection persistent, system language detected as default?

Stick to the i18n mechanism established in the project and do not introduce a second one alongside it. Verify the results in the **actual interface**, not just in the resource file: strings that are too long break layouts, and missing font support only shows up during rendering (missing CJK glyphs appear as empty boxes).

Finally, include the surfaces from Step 0 of Level 1: store and registry descriptions have their own language fields that do not automatically move with the app translation.

## Execution Log

Add an entry with level `full` to `_after-care/LOG.md`:

```markdown
## 2026-07-24 — full
- Stufe 1 vollständig gelaufen (siehe Eintrag oben)
- Rechtscheck: fällig (letzter 2025-06-02) -> neu eingeholt, Ergebnis unbedenklich,
  Auflage Lizenzhinweis Bibliothek X umgesetzt, Wiedervorlage 2027-07-24
- Querverweise: 4 Orgas / 38 Repos geprüft, 3 Beziehungen gefunden,
  bidirektional gesetzt; Rückverweis in repo-y offen (dort aktiver Lock)
- Sprachen App-Ebene: ES ergänzt (312 Schlüssel), JA auf Stand gebracht,
  Umschalter war vorhanden aber nicht persistent -> gefixt
```

## Common Pitfalls

| Pitfall | Correction |
|---|---|
| Performed legal check again even though the last one was 3 months ago | Check the date in `_after-care/RECHTSCHECK.md` first — skip if less than a year old |
| Skipped legal check because "nothing has changed" | The legal landscape changes independently of the project; check after one year |
| Legal opinion committed to repo | `_after-care/` belongs in `.gitignore`; only the consequences become public |
| Negative legal relevance not documented | Even "not relevant" is a finding and belongs in the log |
| Cross-references set only in the maintained repo | Set bidirectionally, otherwise it is a one-way street |
| Checked only your own org | Level 2 means ALL organizations — that is precisely what distinguishes it from Level 1 |
| References listed as a mere name list | Explain the benefit in a short sentence, otherwise nobody clicks |
| New language created but not accessible in the UI | Also check switcher, persistence, and system language detection |
| Translation checked only in the resource file | Check in the real interface — layout breaks and missing glyphs only show up there |
| Forgot store/registry language fields | They do not automatically migrate with the app translation |

## Final Checklist

- [ ] `surface-after-care` completely executed (incl. push and surface parity).
- [ ] Legal relevance checked; result documented — even if negative.
- [ ] Was legal check due? If yes: obtained, requirements implemented, resubmission date set.
- [ ] `_after-care/` in `.gitignore`, legal opinion not tracked.
- [ ] All organizations inventoried, relationships determined.
- [ ] Cross-references set bidirectionally, committed and pushed in target repos.
- [ ] Target repos skipped due to dirty tree or lock noted as open action items.
- [ ] App languages complete, switcher accessible, verified in UI.
- [ ] Store/registry language fields updated.
- [ ] Execution log entry written with level `full`.

## Changelog

### 1.0.0 (2026-07-24)
- Initial version. Level 2 of repo maintenance, building upon `surface-after-care`.
