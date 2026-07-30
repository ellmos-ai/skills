---
language: en
---

> **English** — Official English version of `surface-after-care`.

# Surface After Care — Regular Maintenance Routine for a Published Repo

## When this skill applies

Use it for a repository that is **already public** and should undergo routine maintenance. It is the lightweight level: everything that can be decided within the repo itself, without inventorying third-party repos or initiating legal reviews.

Comparison with neighboring skills:

| Situation | Skill |
|---|---|
| Repo is published for the first time | `github-repo-care` |
| Repo is public, routine maintenance | **this skill** |
| Additional legal check + cross-references across all orgs + app i18n | `full-after-care` (alias `deep-after-care`) |
| Pure legal/privacy/license check prior to making public | `repo-publish-check` |
| Keeping language versions synchronized in content | `bilingual-doc-sync` |
| Distributing this routine across many repos in fair rotation | `rotation-check` |

## Core Idea

A published repo drifts apart in two directions: **The documentation describes older software than what is in the repo**, and **files accumulate that were never intended for outside eyes**. Neither is usually catastrophic, but both cost precisely the users you want to gain — one drops off because the installation instructions no longer work, the other because they run into `AUFGABEN.txt` and `Plan.txt` in the root directory and get the impression someone is only working for themselves here.

This routine cleans up both. It is deliberately repeatable: better half an hour four times a year than one massive overhaul once.

## Workflow

The sequence is not arbitrary. Step 0 comes first because it defines the scope of all subsequent steps. Step 2 runs before anything pushes changes — otherwise, you push improvements over a state that still needs cleaning up. Step 1 is purely server-side and does not interfere.

### 0. Inventory distribution channels

**Before anything is modified: clarify everywhere this project lives.** The GitHub repo is rarely the only surface. A corrected README is of little use if the npm package page continues to display the old version with incorrect installation instructions — and that is precisely where most users land, because package registries often rank higher in search engines than the repo.

```bash
# Manifeste verraten die Kanäle (Deutsch)
cat package.json pyproject.toml setup.py Cargo.toml 2>/dev/null | rg -n "name|version|keywords|repository|homepage"
rg -n "npmjs.com|pypi.org|marketplace|registry|crates.io|hub.docker|zenodo|doi" README* docs/ .github/ 2>/dev/null

# Veröffentlichten Stand der Kanäle abfragen (nur was zutrifft) (Deutsch)
npm view <paket> version description keywords 2>/dev/null
pip index versions <paket> 2>/dev/null
gh release list --repo ORG/REPO --limit 5
```

Typical channels: npm, PyPI, Crates, Docker Hub, MCP Registry, plugin/skill directories, VS Code or browser marketplaces, app stores, Zenodo/DOI, project website, organization profile, `llms.txt`, mirror repos on other hosts.

Note down the list found in the execution log. From now on, it forms the **target set**: Every change from the following steps will be mirrored against this list at the end (see "Parity across all distribution channels"). If you find a surface that no one maintains anymore and points to a dead state, that is a separate finding — either update it or deliberately retract it, but do not leave it standing.

### 1. Set topics

Topics are the most important search surface inside GitHub and cost almost nothing.

```bash
gh repo view ORG/REPO --json nameWithOwner,description,repositoryTopics,homepageUrl,visibility
gh repo edit ORG/REPO --add-topic <topic> --add-topic <topic>
```

Target about 5–12 topics from three angles: **what it is** (`cli`, `mcp-server`, `python-library`), **what it is about** (`file-management`, `tax`, `note-taking`), and **how it works** (`local-first`, `offline`, `privacy`). Align with topics actually used by comparable projects — invented topics won't find users. Check description and homepage at the same time; they appear in the same view.

Topics have counterparts on the other channels from Step 0: `keywords` in `package.json`, `keywords`/`classifiers` in `pyproject.toml`, categories and tags in marketplaces and stores. Keep them identical in content — they represent the same decision, just in multiple places.

### 2a. Privacy gate — always runs

This step is never omitted, even during a seemingly harmless round. Search within the **tracked** set, not in the visible working tree, because that is precisely the difference between "looks clean" and "is clean".

```bash
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|/home/[a-z]|s[k]-[A-Za-z0-9]{16}|gh[p]_|gh[o]_|AKIA[0-9A-Z]{16}|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|BEGIN [A-Z ]*PRIVATE KEY" $(git ls-files)
rg -n "\x{C3}\x{83}|\x{C2}\x{A0}|\x{FFFD}" $(git ls-files -- '*.md' '*.txt' '*.json')
```

Add the names of your own internal storage locations to the pattern — pipeline folders, topic directories, private workspaces:

```bash
rg -n "\.SOFTWARE|\.RESEARCH|_control-center|<weitere eigene Ordnernamen>" $(git ls-files)
```

Such references are not secrets and do not trigger alarms, which is why they slip through — but for readers they are **unresolvable** ("re-transferred from the .SOFTWARE pipeline" tells outsiders nothing) and expose internal structures. Replace or remove them, do not merely tolerate them. A search that only checks for `C:\Users\...` and token patterns is guaranteed not to find them.

Found something? Then the **type** of finding determines the procedure — see the "Force-push rule" section. A secret that has ever been committed is burned: removing it from `HEAD` is not enough; it must be rotated.

### 2b. Check publication intent of documents

The core of this routine. Go through tracked `.md`, `.txt`, and `.json` files and ask for each file: **Was it ever intended for outsiders?**

```bash
git ls-files -- '*.md' '*.txt' '*.json' | sort
```

Do not guess by filename — take a brief look inside. A `PLAN.md` can be a public roadmap, while a harmless-sounding `notes.md` might contain internal pricing strategy. Three categories:

**Belongs in the repo** — README, LICENSE, CHANGELOG, SECURITY, CONTRIBUTING, `docs/`, API references, example configs, real roadmaps, manifests (`package.json`, `pyproject.toml`), lockfiles, CI configuration.

**Does not belong in the repo, but non-critical** — the standard case of this routine. Task and planning files (`AUFGABEN.txt`, `Plan.txt`, `TODO-intern.md`), session notes and handovers (`HANDOFF`, `BRIEFING`, `_handoff/`), status files of the project's own pipeline, development logs, `_archive/`, registry and index JSONs with local paths, intermediate states and generated artifacts, agent work files. Such files are not dangerous, but they create clutter and give the impression of an abandoned workspace. Handling: add to `.gitignore`, `git rm --cached <file>`, and **push normally**.

**Does not belong in the repo and is sensitive** — credentials, personally identifiable information (PII), customer data, internal calculations, pricing and negotiation strategies, unreleased business plans, draft contracts, anything with competitive value. A normal commit is not enough here; see the Force-push rule.

For `.json` files, a second look is worthwhile: manifests and lockfiles stay, but local configs, task/registry files, export dumps, and anything with absolute paths or hostnames are typical stowaways.

If you remove a file that someone might search for (such as a roadmap), briefly mention in the commit or README where the information now lives — otherwise it looks like a regression.

### 3. Banner

A banner helps determine whether someone even starts reading. Check whether one exists and is embedded as the first element in the README.

If missing, there are three options — sensible in this order:

1. **Agent image generator** (e.g. agy; the word "generate" is the trigger there for actual PNG creation), when an illustrative visual fits better than typography.
2. **Codex**, when the banner should be created from code and a style example exists to model after.
3. **Self-created as SVG**, when the banner is primarily a wordmark plus design language — this is often the fastest and most controllable variant, and SVG remains editable later.

Maintain family consistency if the project belongs to a group: same base color, same aesthetics, same wordmark treatment. A banner that falls out of line looks worse than none. Usual size 1200x300; save as PNG in the repo, with the SVG source beside it.

### 4. Verify statements against actual state

This is where most value is generated. The README makes claims — check them instead of taking them on faith:

- **Version** in README/badge vs. `pyproject.toml`/`package.json`/`__version__` and against the latest release tag. If there are multiple version holders, check all, not just one.
- **Installation path** actually run through, at least mentally: Does the package exist under the specified name? Are commands and flags correct?
- **Feature list** vs. code: Is everything listed present, and are new features missing from the list?
- **Numbers** (count of tools, supported formats, test coverage) counted at the source rather than copied forward. Numbers in READMEs quietly become outdated.
- **Screenshots** vs. current UI.
- **Requirements** (Python/Node version, dependencies) vs. manifests.
- **Links** to neighboring projects, documentation, and registries: are they still working?

**A correction applies to all channels, not just the one where it was noticed.** If a statement of fact turns out to be incorrect — especially if the client corrects it —, that same statement is highly likely present elsewhere: in the organization profile, in `llms.txt`, in the second language version, in the README of a neighboring project. Search specifically for it before checking off the point:

```bash
gh search code "<prägnante Formulierung>" --owner ORG
```

Otherwise, you fix one spot and leave three standing — and the contradiction is only noticed when the next repo's turn comes. This costs time and damages trust in the documentation: anyone who finds two conflicting descriptions of the same thing trusts neither.

Afterward, improve the **presentation** where it is weak: long lists of options become more readable as tables; code blocks need language tags; a structure or process overview is captured faster as a Mermaid diagram or ASCII tree than in prose; the first screen height should show purpose, installation, and a usage example, not badges and backstory. If the README exceeds ~400 lines, move details to `docs/` and link them.

**Language rule for READMEs:** Standard is an **English `README.md`** plus a **German second version**. Exception: The domain area of the application is inherently German (German law, German tax/funding system, German-speaking target audience) or there is currently exclusively a German version — then German remains the primary language. For every additional language the project already supports, a separate README version belongs alongside. Stick to the naming convention already used in the repo (`README_de.md`, `README.de.md`, `docs/README.de.md`) and do not invent a second one beside it. Cross-link the versions in the header.

### 6. Create missing standard languages

Add the READMEs that are missing from the **standard languages**: German, English, Spanish, Simplified Chinese, Japanese, Russian. The purpose is reach, so this applies primarily to user-facing projects — for a developer-oriented library with a purely English audience, a Russian README is no gain, only additional maintenance burden. Decide consciously and record the decision in the execution log so the next round does not re-discuss it.

New versions must be **filled, not created and left empty** — a stub with "TODO: translate" is worse than no file at all because it fakes completeness. Content alignment and back-syncing is handled by `bilingual-doc-sync`; with more than two versions, it is worth bringing in this skill for comparison.

### 7. Visibility and outreach

Consider which measures actually bring users for **this** project, and execute them:

- **Registries** where the project technically belongs: package registries (npm, PyPI), MCP Registry, plugin/skill directories, marketplaces.
- **Curated lists** (`awesome-*` and topical collections), provided admission criteria are genuinely met. A PR to a list whose criteria the project fails costs reputation.
- **Own surfaces**: Organization profile, `llms.txt`, project website, ecosystem README, references from related internal repos.
- **Release notes** as an occasion: A release without highlighted novelties goes unnoticed.

**Approval gate:** Everything going outward — PRs to external repos, entries in external lists, posts, submissions — is **proposed and executed only after explicit approval**, unless a standing clearance exists for that channel. Changes to internal surfaces do not require this gate. The reason is simple: A retracted PR to an external repo is publicly visible and reflects poorly on the project.

### 8. Entry on organization pages

First, check your own organization: Is the repo listed in the profile README (`ORG/.github` → `profile/README.md`) at all, in the correct category, with an up-to-date description?

```bash
gh api user/orgs --jq '.[].login'
```

Then go through **all** organizations and answer a single question per organization: Would a visitor to this organization page benefit from this repo? Usually the answer is no — in that case, "do not link" is the correct outcome, not a gap. Where the answer is yes (topical affinity, shared user base, a tool complementing projects there), add the reference with a sentence explaining the utility, not just stating the name.

The profile lives in its own repo (`ORG/.github`). Changes there are maintained and pushed alongside — following the dirty tree rule from Step 11.

### 10. Issues and Pull Requests

```bash
gh issue list --repo ORG/REPO --state open --limit 50
gh pr list --repo ORG/REPO --state open --limit 30
```

Work through them instead of merely counting them:

- **Fixable bugs**: fix directly — context is loaded anyway during this routine. Small, clearly outlined fixes with tests and references to issue numbers.
- **Already completed issues**: close with a sentence explaining what resolved them.
- **Unclear reports**: require a targeted follow-up question (version, OS, reproduction steps).
- **PRs**: read the diff, run tests, then merge or reply with clear reasoning. A PR lying unanswered for months costs more goodwill than a polite rejection.
- **Stale cases**: resolve instead of dragging along.

**Approval gate:** Public comments, closing with reasoning, and merging external contributions are outward communications — submit for review before execution unless standing clearance exists. Pure code fixes in your own repo are unaffected.

### 11. Commit, push, verify

The routine does not end with edits, but when they are **pushed out**. A working tree full of unpushed improvements is the worst outcome: The next session — possibly a different agent or machine — must first orient itself in an unfamiliar, half-finished state, while nothing has improved on public surfaces.

Before pushing, briefly verify what is testable: run tests and smoke checks, check links and rendered views for doc updates. Then bundle into **thematically separate commits** rather than throwing everything into one big commit — cleanup, doc updates, and bug fixes are three distinct things, and anyone wishing to revert one later will be grateful:

```bash
git add .gitignore && git rm --cached <interne dateien>
git commit -m "chore: interne Arbeitsdateien aus dem Repo nehmen"
git commit -am "docs: README auf aktuellen Stand (Version, Toolzahl, Screenshots)"
git commit -am "fix: <Issue-Nummer> ..."

git pull --rebase        # bei divergiertem Branch, vor dem Push
git push
```

Afterward, verify rather than assume: remote README in rendered view, CI run, release and tag status.

```bash
gh run list --repo ORG/REPO --limit 3
gh repo view ORG/REPO --json description,repositoryTopics,url
```

**If CI is red even though your commit only touched docs**, the root cause is almost never your change. The single most common case — encountered **three times** in a single day across this repo family — is an **unpinned linter without an explicit rule set**. Check this **first** before suspecting anything in your commit.

The mechanism: If the workflow runs `ruff check` (or flake8, eslint...) against an unpinned dependency (`ruff>=0.12`, or no version at all), and lacks an explicit rule selection (`[tool.ruff.lint] select = [...]`, or a dedicated `ruff.toml` if `pyproject.toml` is missing), the linter defaults to whatever rule set the **freshly installed** version enforces. A new linter release shifts this default, turning an unchanged codebase red. The telltale signs:

- Rule codes never previously in the project (`UP045`, `UP006`, `BLE001`, `RUF100`, `DTZ005`, `N999`...), sometimes in three-digit counts.
- The failure is often **platform-split**: runners with cached older versions remain green, fresh runners turn red.
- Sometimes a rule flags something unfixable (`N999` flagging the package name itself) — a sure sign it was never standard.

Fix: pin the rule set that was previously green — `select = ["E4","E7","E9","F"]` are classic ruff defaults. If no `pyproject.toml` exists, create a `ruff.toml`. Verify against the **new** linter version itself (install, reproduce findings without config, ensure "passed" with config). New rules enter the project as **tasks** — deliberately adopting them is a choice, not a side effect of a tool update. This is a real, recurring finding: without pinning, CI will break again on the next linter release in **every** repo configured this way.

Two cases where pushing is **not** done: when a publication or submission hold applies to the project, or when the state is explicitly unfinished. Both are exceptions requiring rationale — the normal case is: commit and push.

During a publication hold, the routine is not aborted but **rerouted**: commit locally on a separate branch (`judging-hold/...`, `freeze/...`), leave the main branch untouched at the submitted state, record the hold reason in the execution log, and catch up after release. Consistency is key: blocked is not just `git push`, but **every remotely visible change** — topics, description, homepage, releases, issue/PR actions alter the published project just as much.

If other clones of the same repo exist (second device, deploy copy, mirror), pull them immediately after pushing. A clone ten commits behind produces diagnostics during the next troubleshooting session on a state that no longer exists.

#### Changes to other repos — Dirty tree exception

This routine regularly produces changes **outside** the main repo: a line in the organization profile (Step 8), or later during a deep round a back-reference in a related repo. Such changes are likewise committed and pushed — an unpublished back-reference is no back-reference.

Before touching an external repo, briefly check its status:

```bash
git -C <pfad> status --porcelain
```

**Clean working tree** → make the change, commit in a **separate, thematically clean commit** (`docs: link <projekt>`), and push. Do not mix with commits of the main repo: it is a different repo with its own history and readers.

**Dirty, but external changes are in other files** → your own change is still cleanly doable. Stage and commit **path-specifically only your file** so external, unverified work is not included:

```bash
git -C <pfad> add README.md
git -C <pfad> commit -m "docs: link <projekt>"     # nur der gestagte Pfad
```

But **do not push**. The commit is locally harmless; a push would not necessarily be: You do not know what the other work state is heading toward — perhaps it is being amended, rebased, or refactored, and your push forces reconciliation. The local commit protects your work without forcing anything; the run that later turns to that repo will find it and take it along.

**Dirty in the exact file you need to change** → do not touch. Here you would have to build on an external intermediate state and co-commit it; understanding it first costs more than this single link is worth.

**Active lock (`LOCK*.txt`) in target repo** → **read the lock first instead of treating it as a blanket prohibition.** A lock describes its own scope, which is often narrower than "nothing at all". Typical cases:

- **Editing lock** ("someone is currently working here") → touch nothing, not even auxiliary files.
- **Pure publication/push lock** (submission, judging, freeze) → local work remains allowed, only remote contact is blocked. Work on a separate branch and commit locally; **remotely visible steps are omitted** — not only push, but also topics, description, homepage, releases, and issue/PR actions, because they alter the published project as well.

Reading a lock that only blocks push as a complete ban wastes the entire local part of the routine without safety gain. Conversely, omitting the push while still altering metadata is insufficient. If in doubt, quote the lock and ask.

#### The request must not be lost

If a change is **not** executed for any of these reasons, it moves to the target repo's task list — `AUFGABEN.txt`, `TODO.md`, or `TODO.txt`, depending on what exists there. An entry with date, desired change, and reason:

```markdown
- [ ] [2026-07-24, after-care] Rückverweis auf <projekt> im README ergänzen
      (übersprungen: README hatte uncommittete Fremdänderungen)
```

That is the difference between "postponed" and "forgotten": The task list sits right where the next maintainer will look — far more reliable than a note in an external run log. If no task list exists, do not create one; the open item in your own execution log is sufficient.

With an **active lock, even this does not apply** — the file is not touched and the note stays in your own execution log. Record it there in both cases so rotation is aware of the open item.

Finally, service the surfaces from Step 0 — see next section.

## Parity across all distribution channels

At the end of the round, check against the list from Step 0: **Every change a user would see must reach every channel where they look for it.** A repo whose npm page tells a different story is worse off than one with a single channel.

The key mechanism: **Package registries show the README of the last publish, not the current repo state.** A README fix on npm or PyPI only becomes visible with a new release. If the correction is content-relevant (wrong installation, wrong version, outdated feature list), a patch release is required — otherwise the fix remains ineffective.

| Surface | What is maintained there | How it arrives |
|---|---|---|
| npm | README, `description`, `keywords`, repository link | Only via `npm publish` (patch version); metadata comes from `package.json` |
| PyPI | README (`long_description`), classifiers, project URLs | Only via new upload; metadata from `pyproject.toml` |
| MCP Registry / Plugin directories | Description, version, tool list, getting started doc | Depending on registry, manifest update or re-submission |
| Marketplace / Store | Description, screenshots, categories, language versions | Via respective management portal; screenshots age particularly fast there |
| Docker Hub / Container Registry | Description, tags, usage example | Repository description plus new tag |
| Zenodo / DOI | Metadata, authors, version | In-place edit for metadata, new version for content |
| Website / Org profile / `llms.txt` | Short description, link, positioning | Directly editable — the cheapest surfaces, so never forget |

When raising a version, **all version holders** must move simultaneously: manifest, code constant, README badge, changelog, release tag, `llms.txt`. A half-bumped version state is harder to diagnose than an old one throughout.

If an update on a surface is currently impossible or impractical (e.g., a release solely for a typo), record it in the execution log so the next round does not mistake the variance for oversight.

## Force-push rule

The standard is **no force-push**. Retrospectively ignoring internal planning files does not justify rewriting history: Effort is high, every clone and fork breaks, open PRs become unusable — and the benefit is low because the content is harmless. Standard procedure:

```bash
git rm --cached <datei>            # aus dem Tracking, bleibt lokal erhalten
# .gitignore ergänzen (Deutsch)
git commit -m "chore: interne Arbeitsdateien aus dem Repo nehmen"
git push
```

Rewriting history (and pushing with `--force-with-lease`) is justified only for **actual leaks**: credentials and keys, PII or customer data, and documents with genuine competitive value — internal calculations, pricing strategies, unreleased plans, contract details. In that case:

1. **Rotate** affected secrets first — history is already copied, forked, and cached by then. Rotation works, deletion is merely cosmetic.
2. Clean history (`git filter-repo` or BFG), push with `--force-with-lease`.
3. Check forks and caches; contact GitHub support for orphaned objects if needed.
4. Record process in execution log: what, when, which rotation.

When in doubt between "non-critical" and "sensitive": treat as sensitive and present for review. The costs are asymmetrical.

## Findings become tasks, not just log entries

A maintenance round regularly finds more than it can or should fix in the same round: a missing language version, modernization backlog, an unexecuted release. **Such findings become tasks the moment they are discovered** — otherwise they linger in the log of a closed run, where the next maintainer won't see them.

The task belongs in the **folder-local task system of the project** — where whoever works next on this project will check. Typically that is `AUFGABEN.txt` or `TODO.md` in the project folder, which is often **not in the Git clone**, but in the directory where planning lives. The clone holds code, the project folder holds management; an entry in the clone that disappears on the next `git clean` is not a task.

Keep three things in mind:

1. **Separate internal task list from public roadmap.** A `TODO.md` might be a maintained public roadmap — in that case it is no place for internal follow-up. Look inside before appending: If there is a header like "Public roadmap", write to the internal file beside it (`AUFGABEN.txt`) and mark it internal.
2. **Check existing entries instead of duplicating.** Often the finding is already listed. In that case, do not create a new entry, but **enrich** it — with empirical evidence from this run ("confirmed: `--help` outputs fully German text"). A known item with fresh proof is more valuable than a second entry beside it.
3. **Record completed items.** What the round fixed belongs as a checked-off item with commit hash. This explains to the next round why a finding disappeared and prevents re-"discovery".

Formulate the task so it is understandable without the context of this run: what was found, why it matters, what the next step would be. "i18n incomplete" is not a task; "Catalog only contains `status.title`, es/zh/ja/ru are empty — first transfer CLI strings into catalog, then fill all six languages" is one.

## Execution log

Record results in `_after-care/LOG.md` (the folder belongs in `.gitignore` — it is pipeline material, not repo content, following Step 2b). One line per run with date, level, and conscious decisions:

```markdown
## 2026-07-24 — surface
- Flächen: GitHub, npm (<paket>), MCP-Registry, Org-Profil, llms.txt
- Topics: +local-first, +mcp-server; keywords in package.json angeglichen
- Entfernt: AUFGABEN.txt, _handoff/ (gitignored, kein Force-Push nötig)
- README: Version 0.9 -> 1.2 korrigiert, Toolzahl 23 -> 26 nachgezählt
- Sprachen: EN + DE gepflegt; ES/ZH/JA/RU bewusst nicht (entwicklernahes Publikum)
- Issues: #12 gefixt, #7 geschlossen (erledigt), #15 Rückfrage gestellt
- Push: 3 Commits, CI grün; npm-Republish 1.2.1 wegen README-Korrektur
- Offen: Store-Screenshots veraltet, brauchen neuen Build
```

The log saves the next round from re-making the same decisions and serves as the foundation for rotating care runs across many repos (`rotation-check`).

## Common Mistakes

| Mistake | Correction |
|---|---|
| Only checked working tree, not `git ls-files` | Always check tracked set — that's where issues lie |
| Privacy gate only focused on paths and tokens | Search for internal pipeline/folder names too — they trigger no alarm and slip through |
| Removed internal file while rewriting history | For non-critical files, `git rm --cached` + normal push is sufficient |
| Removed secret from `HEAD` and considered done | Rotate secret; anything else is cosmetic |
| Classified files solely by name | Take a brief look inside — names don't reliably convey intent |
| Forwarded numbers in README instead of recounting | Count at the source (tool list, test run, manifest) |
| Created new language version as empty stub | Fill or leave out — a stub fakes completeness |
| Introduced second README naming convention | Adopt existing convention |
| Submitted PR to external list without approval | Present outward communication for review; only internal surfaces are free |
| Counted issues instead of processing them | Fix, close, or ask targeted questions — every case gets a state |
| Generated banner independently in foreign style | Adhere to ecosystem design family |
| Corrected README in repo, npm/PyPI page still shows old | Registry pages come from last publish — follow up with patch release |
| Bumped version only in manifest | All version holders simultaneously: manifest, code, badge, changelog, tag, `llms.txt` |
| Changes finished, but left unpushed | Committing and pushing is part of the round; only holds justify exceptions |
| Everything bundled into one big commit | Separate cleanup, docs, and fixes — otherwise nothing can be individually reverted |
| CI red after doc commit, suspected own changes | Unpinned linter without `select` follows default of new version — pin rule set |
| Corrected false statement only where noticed | Search org-wide for formulation — usually stands in org profile, `llms.txt`, and second language version too |
| Worked in dirty third-party repo with `commit -a` | Stage and commit path-specifically, do not push — third-party work remains untouched |
| Made change in clean org profile repo, but did not push | Clean third-party repos get their own commit **and** their own push |
| Recorded skipped change only in own log | Additionally enter into target repo's task list, if one exists |
| Written finding only into execution log | Becomes task in folder-local task system — nobody looks in old logs later |
| Attached internal follow-up to public roadmap | Check first; "Public roadmap" means: use internal file beside it |
| Duplicated known finding as new entry | Enrich existing item with empirical evidence from this run |
| Written TODO line into locked repo during edit lock | Edit lock applies to whole project — touch nothing there |
| Read push lock as total prohibition and skipped repo entirely | Read lock: if it only blocks publication, local round continues on separate branch |
| Did not push under push lock, but changed topics or description | Metadata is also remotely visible — omitted under publication hold as well |

## Final Checklist

- [ ] Distribution surfaces identified and recorded in execution log.
- [ ] Topics, description, and homepage set and verified.
- [ ] Privacy gate run over tracked set, findings handled.
- [ ] `.md`/`.txt`/`.json` checked for publication intent, internal files ignored.
- [ ] No force-push without actual leak; rotation performed in case of leak.
- [ ] Banner present and embedded in README.
- [ ] Version, features, numbers, screenshots, links verified against actual state.
- [ ] Presentation improved (tables, diagrams, first screen height).
- [ ] README language matrix complete; decisions on further languages documented.
- [ ] Visibility measures implemented or submitted for approval.
- [ ] Entry in own org profile checked, sensible external org links placed.
- [ ] Changes to external repos: clean → committed and pushed; dirty → locally committed;
      not executed → entered in target repo's task list.
- [ ] Issues and PRs brought to a defined state.
- [ ] Separate commits created, pushed, CI and remote view verified.
- [ ] All distribution surfaces brought to same state (patch release if needed).
- [ ] Unresolved findings entered as tasks in folder-local task system.
- [ ] Execution log written to `_after-care/LOG.md`.

## Changelog

### 1.6.0 (2026-07-24)
- Added rule: A content correction applies to all surfaces. Empirically learned — a
  user clarification was corrected in turn 1 in the Hub, but stood unnoticed five more times
  in the organization profile (EN, DE, `llms.txt`) and was only noticed nine turns later.

### 1.5.0 (2026-07-24)
- Sharpened linter diagnosis after pattern occurred three times in one day
  (n8n-workflow-manager ruff 0.15, clirec + swarm-ai ruff 0.16): "check first", concrete
  telltale rule codes, platform split, `ruff.toml` as fix when `pyproject.toml` is missing,
  verification against new linter version.

### 1.4.0 (2026-07-24)
- Added diagnosis: If CI turns red after pure doc commit, most frequent cause
  is unpinned linter without explicit rule set — new tool release shifts default and
  makes unchanged code red. Fix: pin rule set, new rules as task. Occurred twice in a row
  (n8n-workflow-manager with ruff 0.15, clirec with 0.16).

### 1.3.0 (2026-07-24)
- New section "Findings become tasks": What the round does not fix itself becomes, at the moment
  of discovery, an entry in the folder-local task system of the project — where the next maintainer
  looks, not in the log of a closed run. Including separation of internal list and public roadmap,
  enriching instead of duplicating, completed items with commit.

### 1.2.0 (2026-07-24)
- Privacy gate additionally searches for names of own internal storage locations. They are not
  secrets, hence trigger no alarm and survive a gate targeting only paths and tokens — but remain
  unresolvable for readers and expose internal structure.

### 1.1.0 (2026-07-24)
- Locks read instead of treated as blanket prohibition: pure publication/push lock reroutes round
  to local branch instead of aborting. Clarified that metadata, releases, and issue/PR actions
  also fall under such a lock — they are just as remotely visible as a push.

### 1.0.0 (2026-07-24)
- Initial version. Level 1 repo after-care, derived from `github-repo-care`.
