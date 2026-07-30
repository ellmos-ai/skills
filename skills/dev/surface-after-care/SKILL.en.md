---
language: en
---

<img src="banner.png" width="100%" alt="surface-after-care banner">

> **English** — Official English version of `surface-after-care`.

# Surface After Care — Regular Maintenance Routine for Published Repositories (English)

## When to Use This Skill

Use this skill for a repository that is **already public** and needs regular turn-based review. It is the lightweight/cost-effective tier: everything that can be decided within the repository itself, without inventorying third-party repositories or triggering a legal assessment.

Differentiation from neighboring skills:

| Situation | Skill |
|---|---|
| Repository is being published for the first time | `github-repo-care` |
| Repository is public, routine maintenance check | **this skill** |
| Additional legal check + cross-references across all orgs + app i18n | `full-after-care` (Alias `deep-after-care`) |
| Pure legal/privacy/license audit prior to making public | `repo-publish-check` |
| Keeping language versions content-synchronized | `bilingual-doc-sync` |
| Distributing this routine across many repos, rotating fairly | `rotation-check` |

## Core Idea

A published repository tends to drift apart in two directions: **The documentation describes older software than what actually lives in the repo**, and **files accumulate that were never meant for external eyes**. Neither is usually catastrophic, but both alienate precisely the users you want to gain — one drops off because the installation instructions no longer work, the other stumbles upon `AUFGABEN.txt` or `Plan.txt` in the root directory and gets the impression that someone is only building for themselves.

This routine cleans up both. It is deliberately repeatable: half an hour four times a year is better than one massive annual cleanup.

## Workflow

The sequence is not arbitrary. Step 0 comes first because it determines the scope of all subsequent steps. Step 2 runs before anything pushes changes — otherwise you push improvements on top of a state that still needs cleaning. Step 1 is purely server-side and does not interfere.

### 0. Inventory Distribution Surfaces

**Before changing anything: clarify everywhere this project lives.** The GitHub repo is rarely the only surface. A corrected README is of little use if the npm package page continues to show the old version with incorrect installation instructions — and that is where most users land, because package registries often rank higher in search engines than the repo itself.

```bash
# Manifests reveal distribution channels
cat package.json pyproject.toml setup.py Cargo.toml 2>/dev/null | rg -n "name|version|keywords|repository|homepage"
rg -n "npmjs.com|pypi.org|marketplace|registry|crates.io|hub.docker|zenodo|doi" README* docs/ .github/ 2>/dev/null

# Query published status of channels (only applicable ones)
npm view <package> version description keywords 2>/dev/null
pip index versions <package> 2>/dev/null
gh release list --repo ORG/REPO --limit 5
```

Typical surfaces: npm, PyPI, Crates, Docker Hub, MCP Registry, plugin/skill directories, VS Code or browser marketplaces, app stores, Zenodo/DOI, project website, organization profile, `llms.txt`, mirror repos on other hosts.

Note the list found in the run log. From now on it is the **target set**: Every change from subsequent steps will be mirrored against this list at the end (see "Parity across all surfaces"). If you find a surface that nobody maintains anymore and points to a dead state, that is its own finding — either update or deliberately retract it, but do not leave it stale.

### 1. Set Topics

Topics are the single most important search surface inside GitHub and cost almost nothing.

```bash
gh repo view ORG/REPO --json nameWithOwner,description,repositoryTopics,homepageUrl,visibility
gh repo edit ORG/REPO --add-topic <topic> --add-topic <topic>
```

Aim for about 5–12 topics from three angles: **what it is** (`cli`, `mcp-server`, `python-library`), **what it is about** (`file-management`, `tax`, `note-taking`), and **how it works** (`local-first`, `offline`, `privacy`). Align with topics actually used by comparable projects — invented topics attract no users. Check description and homepage at the same time, as they appear in the same view.

Topics have counterparts on other surfaces from Step 0: `keywords` in `package.json`, `keywords`/`classifiers` in `pyproject.toml`, categories and tags in marketplaces and stores. Keep them content-aligned — they represent the same decision across multiple locations.

### 2a. Privacy Gate — Always Runs

This step is never skipped, even in a seemingly harmless routine. Search within the **tracked** file set, not the visible working directory, because that is precisely the difference between "looks clean" and "is clean".

```bash
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|/home/[a-z]|s[k]-[A-Za-z0-9]{16}|gh[p]_|gh[o]_|AKIA[0-9A-Z]{16}|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|BEGIN [A-Z ]*PRIVATE KEY" $(git ls-files)
rg -n "\x{C3}\x{83}|\x{C2}\x{A0}|\x{FFFD}" $(git ls-files -- '*.md' '*.txt' '*.json')
```

Supplement the pattern with the **names of your own internal storage locations** — pipeline folders, topic directories, private workspaces:

```bash
rg -n "\.SOFTWARE|\.RESEARCH|_control-center|<additional internal folder names>" $(git ls-files)
```

Such references are not secrets and trigger no alerts, so they slip through — but they are **unresolvable** for external readers ("transferred back from the .SOFTWARE pipeline" tells an outsider nothing) and expose internal structure. Replace or remove them, do not merely tolerate them. A search looking only for `C:\Users\…` and token patterns will guaranteed miss them.

Found something? The **type** of finding determines the action — see the "Force Push Rule" section. A secret that has ever been committed is compromised: removing it from `HEAD` is insufficient; it must be rotated.

### 2b. Check Document Publishing Intent

The core of this routine. Go through tracked `.md`, `.txt`, and `.json` files and ask for each file: **Was this ever intended for public consumption?**

```bash
git ls-files -- '*.md' '*.txt' '*.json' | sort
```

Do not guess by filename — take a brief look inside. A `PLAN.md` might be a public roadmap, while an innocent-sounding `notes.md` could be an internal pricing strategy. Three categories:

**Belongs in repo** — README, LICENSE, CHANGELOG, SECURITY, CONTRIBUTING, `docs/`, API references, example configs, genuine roadmaps, manifests (`package.json`, `pyproject.toml`), lockfiles, CI configuration.

**Does not belong in repo, but non-critical** — the standard case for this routine. Task and planning files (`AUFGABEN.txt`, `Plan.txt`, `TODO-intern.md`), session notes and handoffs (`HANDOFF`, `BRIEFING`, `_handoff/`), internal pipeline status files, dev logs, `_archive/`, registry and index JSONs with local paths, intermediate states and generated artifacts, agent working files. These files are not dangerous, but they create clutter and give the impression of an unkempt construction site. Treatment: add to `.gitignore`, run `git rm --cached <file>`, and **push normally**.

**Does not belong in repo and sensitive** — credentials, personal data, customer data, internal costings, pricing and negotiation strategies, unreleased business plans, draft contracts, anything with competitive value. Here a normal commit is not enough; see the Force Push Rule.

For `.json`, a second glance pays off: manifests and lockfiles stay, but local configs, task/registry files, export dumps, and anything with absolute paths or hostnames are typical stowaways.

If you remove a file that someone might search for (a roadmap for instance), briefly mention in the commit message or README where that information now lives — otherwise it looks like a regression.

### 3. Banners

A banner influences whether someone even starts reading. Check whether one exists and is embedded as the first element in the README.

If missing, there are three paths — sensible in this order:

1. **Agent image generator** (e.g. agy; the word "generate" triggers real PNG generation there), when a visual motif fits better than typography.
2. **Codex**, when the banner should be generated from code and a style model exists to reference.
3. **Self-created SVG**, when the banner is primarily a wordmark plus design language — often the fastest and most controllable option, and SVG remains editable later.

Maintain brand consistency if the project belongs to a family: same base color, same aesthetics, same wordmark treatment. A banner that falls out of line looks worse than none at all. Standard size 1200x300; commit PNG into repo, SVG source alongside it.

### 4. Reconcile Claims Against Real State

This is where most value is generated. The README makes claims — verify them instead of taking them at face value:

- **Version** in README/badge against `pyproject.toml`/`package.json`/`__version__` and against the latest release tag. If multiple version locations exist, check all of them.
- **Installation steps**: actually walk through them (at least by reading): Does the package exist under the stated name? Are commands and flags accurate?
- **Feature list** against codebase: Is everything mentioned present, and are new features missing from the list?
- **Numbers** (count of tools, supported formats, test coverage): recount at the source instead of carrying forward. Numbers in READMEs age quietly.
- **Screenshots** against current UI.
- **Requirements** (Python/Node versions, dependencies) against manifests.
- **Links** to sibling projects, docs, and registries: are they still active?

**A correction applies to all surfaces, not just where it was spotted.** If a factual statement proves false — especially when clarified by the project owner —, the same statement very likely exists elsewhere: in the org profile, in `llms.txt`, in the second language version, in the README of a sibling project. Search specifically for it before checking off the task:

```bash
gh search code "<distinctive formulation>" --owner ORG
```

Otherwise you fix one spot and leave three behind — and the discrepancy is only noticed when the next repo is reviewed. That costs time and damages trust in the docs: anyone finding two conflicting descriptions of the same thing trusts neither.

Next, improve **presentation** where it is weak: long option lists become more readable as tables; code blocks need language tags; structure or flow overviews are captured faster as Mermaid diagrams or ASCII trees than in prose; the first screen height should show purpose, installation, and usage example, not badges and backstory. If the README exceeds ~400 lines, move details to `docs/` and link to them.

**Language rule for READMEs:** Default is an **English `README.md`** plus a **German second version**. Exception: The domain of the application is inherently German (German law, German tax/grant system, German-speaking target audience) or only a German version exists so far — then German remains the primary language. For every additional language the project already supports, include a dedicated README version. Stick to the naming convention already used in the repo (`README_de.md`, `README.de.md`, `docs/README.de.md`) and do not introduce a second one alongside it. Cross-link versions in the header line.

### 6. Create Missing Standard Languages

Add missing READMEs for the **standard languages**: German, English, Spanish, Simplified Chinese, Japanese, Russian. The goal is reach, so this applies mainly to user-facing projects — for a developer-oriented library with a purely English audience, a Russian README is not a gain but added maintenance burden. Decide intentionally and record the decision in the run log so the next round does not reopen the discussion.

New versions must be **populated, not just created empty** — a stub saying "TODO: translate" is worse than no file because it feigns completeness. Content parity and back-alignment are handled by `bilingual-doc-sync`; with more than two versions, it is worth bringing in that skill for alignment.

### 7. Visibility and Promotion

Consider which measures actually bring users for **this** specific project, and implement them:

- **Registries** where the project technically belongs: package registries (npm, PyPI), MCP registry, plugin/skill directories, marketplaces.
- **Curated lists** (`awesome-*` and thematic collections), provided admission criteria are genuinely met. A PR to a list whose criteria the project fails costs reputation.
- **Owned surfaces**: organization profile, `llms.txt`, project website, ecosystem README, references from related internal repos.
- **Release notes** as an occasion: A release without narrated highlights goes unnoticed.

**Approval Gate:** Anything outgoing — PRs to external repos, entries in external lists, posts, submissions — must be **proposed and executed only after explicit approval**, unless a standing approval exists for that channel. Changes to owned surfaces do not require this gate. The reason is simple: A retracted PR to an external repo is publicly visible and reflects poorly on the project.

### 8. Entry on Organization Pages

First your own organization: Is the repo listed in the profile README (`ORG/.github` → `profile/README.md`) at all, in the correct section, with an updated description?

```bash
gh api user/orgs --jq '.[].login'
```

Then check **all** organizations and answer one question per organization: Would a visitor to this organization page benefit from this repo? Usually the answer is no — then "do not link" is the correct outcome, not a gap. Where the answer is yes (thematic proximity, shared user base, a tool complementing those projects), add the reference with a sentence explaining the utility, not just stating the name.

The profile lives in a dedicated repo (`ORG/.github`). Changes there are maintained and pushed following the Dirty Tree rule from Step 11.

### 10. Issues and Pull Requests

```bash
gh issue list --repo ORG/REPO --state open --limit 50
gh pr list --repo ORG/REPO --state open --limit 30
```

Work through them rather than just counting them:

- **Fixable bugs**: fix directly — context is already loaded during this routine. Small, clearly outlined fixes with tests and issue references.
- **Already completed issues**: close with a sentence explaining what resolved them.
- **Unclear reports**: require a targeted follow-up question (version, OS, reproduction steps).
- **PRs**: read actual diff, run tests, then merge or provide reasoned feedback. A PR sitting unanswered for months costs more goodwill than a polite rejection.
- **Stale cases**: resolve rather than drag along.

**Approval Gate:** Public comments, closing issues with rationale, and merging third-party contributions represent external communication — present them before execution unless standing approval exists. Pure code fixes in your own repo are exempt.

### 11. Commit, Push, Verify

The routine does not end with edits, but when they are **shipped**. A working directory full of unpushed improvements is the worst outcome: The next session — possibly a different agent or machine — has to onboard into half-finished work, and public surfaces show no improvement.

Before pushing, verify what can be checked: run tests and smoke checks; for doc changes verify links and rendered view. Then bundle into **topically separated commits** instead of dumping everything into one catch-all commit — cleanup, doc updates, and bug fixes are three different things, and anyone wanting to revert one later will be thankful:

```bash
git add .gitignore && git rm --cached <internal files>
git commit -m "chore: remove internal working files from repo"
git commit -am "docs: update README to current state (version, tool count, screenshots)"
git commit -am "fix: <issue number> ..."

git pull --rebase        # if branch diverged, before pushing
git push
```

Then verify instead of assuming: remote README in rendered view, CI run, release and tag state.

```bash
gh run list --repo ORG/REPO --limit 3
gh repo view ORG/REPO --json description,repositoryTopics,url
```

**If CI turns red after a commit touching only documentation**, the cause is almost never your commit. By far the most common case — encountered **three times** in a single day across this repo family — is an **unpinned linter without a locked ruleset**. Check this **first** before suspecting your commit.

The mechanism: If the workflow executes `ruff check` (or flake8, eslint …) against an unpinned dependency (`ruff>=0.12`, or no version at all), and lacks an explicit rule selection (`[tool.ruff.lint] select = [...]`, or a custom `ruff.toml` when `pyproject.toml` is absent), the linter defaults to whatever rules the **newly installed** version enforces. A new linter release shifts this default, turning an unchanged codebase red. Tell-tale signs:

- Rule codes the project never had before (`UP045`, `UP006`, `BLE001`, `RUF100`, `DTZ005`, `N999` …), sometimes in three-digit quantities.
- The failure is often **platform-split**: runners with cached older versions stay green, fresh ones turn red.
- Sometimes a rule flags something unfixable (`N999` flagging the package name itself) — a sure sign it was never standard.

Fix: lock the ruleset that was green before — `select = ["E4","E7","E9","F"]` are classic ruff defaults. If `pyproject.toml` does not exist, create `ruff.toml`. Verify against the **new** linter version itself (install, reproduce findings without config, confirm "passed" with config). The new rules enter the project as a **task** — deliberately adopting rules is a decision, not a side effect of a tool update. This is a real, recurring finding: Without pinning, CI breaks again on the next linter release across **every** similarly configured repo.

Two cases where pushing is **not** done: when a publication or submission hold applies to the project, or when the state is explicitly incomplete. Both are exceptions requiring justification — the standard case is: commit and push.

Under a publication hold, the routine is not aborted but **rerouted**: commit locally on a dedicated branch (`judging-hold/…`, `freeze/…`), leave the main branch untouched at the submitted state, note the hold reason in the run log, and catch up after release. Consistency is essential: Holds apply not just to `git push`, but to **every remotely visible change** — topics, description, homepage, releases, issue/PR actions modify the published project just as much.

If other clones of the repo exist (second machine, deploy copy, mirror), pull them immediately after pushing. A clone ten commits behind produces outdated diagnostic paths during future troubleshooting.

#### Edits to Other Repos — Dirty Tree Exception

This routine regularly generates edits **outside** the target repo: a line in the org profile (Step 8), or a back-reference in a related repo during deeper reviews. Such edits are also committed and pushed — an uncommitted back-reference is no reference.

Check state before touching an external repo:

```bash
git -C <path> status --porcelain
```

**Clean working tree** → make edit, commit in a **separate, topically clear commit** (`docs: link <project>`) and push. Do not mix with commits from the target repo: It is a different repo with its own history and readers.

**Dirty, but external changes are in other files** → your edit can still be safely made. Stage and commit **path-specifically only your file**, ensuring unreviewed foreign work does not tag along:

```bash
git -C <path> add README.md
git -C <path> commit -m "docs: link <project>"     # staged path only
```

Do **not push**. The local commit is harmless; a push might not be: You do not know what the other working state is building towards — it might be mid-amend, rebase, or restructure, and pushing forces integration. The local commit preserves your work without forcing anything on anyone; a future run targeting that repo will find and carry it forward.

**Dirty in the exact file you need to edit** → do not touch. Here you would build on uncommitted foreign work and commit it; understanding that work costs more than this single reference is worth.

**Active Lock (`LOCK*.txt`) in target repo** → **read the lock first instead of treating it as a total ban.** A lock describes its own scope, which is often narrower than "do nothing". Typical cases:

- **Edit Lock** ("someone is actively working here") → touch nothing, not even secondary files.
- **Pure Publish/Push Lock** (submission, judging, freeze) → local work remains allowed, only remote contact is blocked. Work on a dedicated branch and commit locally; **remote-impacting steps are omitted** — not only push, but topics, description, homepage, releases, and issue/PR actions.

Reading a push-only lock as a total ban wastes the entire local part of the routine without safety benefits. Conversely, withholding push while still altering metadata is insufficient. When in doubt, quote the lock and ask.

#### Intent Must Not Be Lost

If an edit is **not** executed for these reasons, move it to the target repo's task list — `AUFGABEN.txt`, `TODO.md`, or `TODO.txt`, depending on what exists there. An entry with date, desired change, and reason:

```markdown
- [ ] [2026-07-24, after-care] Add back-reference to <project> in README
      (skipped: README had uncommitted external edits)
```

This is the difference between "postponed" and "forgotten": The task list is where the next maintainer looks anyway — far more reliable than a note in an external run log. If no task list exists, do not create one; the open item in your own run log suffices.

Under an **active lock this also does not apply** — do not touch the file and keep the note strictly in your own run log. Record it in both cases so rotations are aware of open items.

Finally, update surfaces from Step 0 — see next section.

## Parity Across All Distribution Surfaces

At the conclusion of the routine, check against the list from Step 0: **Every change a user would see must reach every surface where they might look for it.** A repo whose npm page tells a different story than its repo is worse off than one with only a single surface.

The key mechanism: **Package registries show the README from the last publish, not the current repo state.** A README fix becomes visible on npm or PyPI only with a new version release. If the correction is content-relevant (wrong installation, wrong version, outdated feature list), a patch release is required — otherwise the fix remains ineffective.

| Surface | What is maintained there | How it arrives |
|---|---|---|
| npm | README, `description`, `keywords`, repository link | Only via `npm publish` (patch version); metadata comes from `package.json` |
| PyPI | README (`long_description`), classifiers, project URLs | Only via new upload; metadata from `pyproject.toml` |
| MCP Registry / Plugin directories | Description, version, tool list, getting started doc | Via manifest update or resubmission depending on registry |
| Marketplace / Store | Description, screenshots, categories, localized text | Via respective admin console; screenshots age particularly fast there |
| Docker Hub / Container Registry | Description, tags, usage example | Repo description plus new tag |
| Zenodo / DOI | Metadata, authors, version | In-place edit for metadata, new version for content |
| Website / Org Profile / `llms.txt` | Short description, link, positioning | Directly editable — the cheapest surfaces, so never forget them |

When bumping a version, **all version holders** must move together: manifest, code constants, README badges, changelog, release tags, `llms.txt`. A half-bumped version state is harder to diagnose than a consistently old one.

If updating a surface is currently impossible or impractical (e.g. releasing solely for a typo), record it in the run log so future runs do not mistake the discrepancy for oversight.

## Force Push Rule

Standard practice is **no force push**. Retrospectively ignoring internal planning files does not justify rewriting history: Effort is high, every clone and fork breaks, open PRs become invalid — and gain is minimal because content is harmless. Normal approach:

```bash
git rm --cached <file>            # removes from tracking, keeps local copy
# update .gitignore
git commit -m "chore: remove internal working files from repo"
git push
```

Rewriting history (and pushing with `--force-with-lease`) is justified only for **genuine leaks**: Credentials and keys, personal or customer data, and documents with actual competitive value — internal calculations, pricing strategies, unreleased plans, contract details. In that case:

1. **Rotate affected secrets first** — history has already been copied, forked, and cached. Rotation mitigates risk; deletion is cosmetic.
2. Clean history (`git filter-repo` or BFG), push with `--force-with-lease`.
3. Audit forks and caches; contact GitHub support for orphaned objects if necessary.
4. Record event in run log: what, when, which rotation.

When in doubt between "non-critical" and "sensitive": treat as sensitive and escalate. Costs are asymmetric.

## Findings Become Tasks, Not Just Log Lines

A routine check regularly finds more than it can or should fix in a single session: a missing language version, modernization backlog, an unexecuted publication. **Such findings become tasks at the moment of discovery** — otherwise they remain buried in a completed log where future maintainers will not see them.

The task belongs in the **project's local task system** — where whoever works on this project next will look. Typically this is `AUFGABEN.txt` or `TODO.md` in the project directory, which often resides **outside the Git clone** in project management storage. The clone holds code, the project directory holds control; an entry in the clone that vanishes on the next `git clean` is not a task.

Keep three rules in mind:

1. **Separate internal task lists from public roadmaps.** A `TODO.md` might be a curated public roadmap — not a dumping ground for internal rework. Check before appending: If it has headings like "Public roadmap", write to an adjacent internal file (`AUFGABEN.txt`) and mark as internal.
2. **Check existing entries before duplicating.** Often the finding is already documented. Do not create a duplicate; **enrich** it with empirical evidence from this run ("confirmed: `--help` outputs full German text"). A known item with fresh proof is more valuable than a second entry alongside it.
3. **Log completed items.** What the routine fixed belongs as a checked-off item with commit hash. This explains to future runs why a finding disappeared and prevents re-discovery.

Phrase tasks so they make sense without context from this run: what was found, why it matters, what the next step is. "i18n incomplete" is not a task; "Catalog only contains `status.title`, es/zh/ja/ru are empty — migrate CLI strings to catalog first, then populate all six languages" is a task.

## Run Log

Record results in `_after-care/LOG.md` (add folder to `.gitignore` — it is pipeline material, not repo content, following Step 2b). One line per run with date, tier, and conscious decisions:

```markdown
## 2026-07-24 — surface
- Surfaces: GitHub, npm (<package>), MCP Registry, Org Profile, llms.txt
- Topics: +local-first, +mcp-server; keywords in package.json aligned
- Removed: AUFGABEN.txt, _handoff/ (gitignored, no force push needed)
- README: Corrected version 0.9 -> 1.2, tool count 23 -> 26 recounted
- Languages: EN + DE maintained; ES/ZH/JA/RU intentionally omitted (developer audience)
- Issues: #12 fixed, #7 closed (done), #15 follow-up question sent
- Push: 3 commits, CI green; npm republish 1.2.1 due to README fix
- Open: Store screenshots outdated, require fresh build
```

The log saves future runs from re-deliberating decisions and serves as the foundation for rotating checks across many repos (`rotation-check`).

## Common Pitfalls

| Mistake | Correction |
|---|---|
| Examined only working tree, ignored `git ls-files` | Always audit tracked set — that is where issues hide |
| Privacy gate checked only paths and tokens | Search for internal folder/pipeline names — they trigger no alerts but expose structure |
| Removed internal file by rewriting history | For non-critical files `git rm --cached` + normal push is sufficient |
| Removed secret from `HEAD` and marked resolved | Rotate secret; anything else is cosmetic |
| Classified files strictly by filename | Inspect content briefly — names do not reliably convey intent |
| Carried forward numbers in README without recounting | Count at source (tool list, test run, manifest) |
| Added new language version as empty stub | Populate or omit — stubs feign completeness |
| Introduced second README naming convention | Follow existing repo convention |
| Submitted unapproved PR to external list | Escalate external communications; only owned surfaces are pre-approved |
| Counted issues instead of processing them | Fix, close, or ask targeted questions — every item gets a defined status |
| Created banner in external style independently | Follow ecosystem design family |
| Fixed README in repo, npm/PyPI page still shows old docs | Registry pages stem from last publish — issue patch release |
| Bumped version only in manifest | Bump all version holders simultaneously: manifest, code, badge, changelog, tag, `llms.txt` |
| Edits complete, left unpushed | Committing and pushing belong to the routine; only holds justify exceptions |
| Bundled everything into one catch-all commit | Separate cleanup, docs, and fixes — otherwise edits cannot be reverted individually |
| CI turns red after doc commit, self-blame | Unpinned linter without `select` follows new release defaults — lock ruleset |
| Corrected false claim only where spotted | Search org-wide for formulation — usually exists in org profile, `llms.txt`, and second language version |
| Worked in dirty foreign repo with `commit -a` | Stage path-specifically and commit, do not push — leave foreign work untouched |
| Made edit in clean org profile repo, omitted push | Clean foreign repos get their own commit **and** push |
| Recorded skipped edit only in own log | Also add to target repo's task list if one exists |
| Written finding only to run log | Convert to task in local task system — nobody reads old run logs later |
| Attached internal work to public roadmap | Check first; "Public roadmap" means use adjacent internal file |
| Duplicated known finding as new entry | Enrich existing item with empirical proof from current run |
| Written TODO line to locked repo during edit hold | Lock applies to entire project — touch nothing there |
| Treated push lock as total ban, skipped repo entirely | Read lock: if it blocks only publication, run local routine on dedicated branch |
| Withheld push under push lock, but changed metadata | Metadata is remotely visible — under push lock metadata edits are omitted too |

## Completion Checklist

- [ ] Distribution surfaces identified and recorded in run log.
- [ ] Topics, description, and homepage configured and verified.
- [ ] Privacy gate run over tracked set, findings resolved.
- [ ] `.md`/`.txt`/`.json` evaluated for publication intent, internal files ignored.
- [ ] No force push without actual leak; secret rotation executed if leaked.
- [ ] Banner present and embedded in README.
- [ ] Version, features, numbers, screenshots, links verified against actual state.
- [ ] Presentation improved (tables, diagrams, above-the-fold content).
- [ ] README language matrix complete; language decisions documented.
- [ ] Visibility steps executed or submitted for approval.
- [ ] Org profile entry verified, sensible external org links established.
- [ ] External repo edits: clean → committed and pushed; dirty → committed locally; unexecuted → added to target repo task list.
- [ ] Issues and PRs transitioned to defined states.
- [ ] Separated commits created, pushed, CI and remote rendering verified.
- [ ] All distribution surfaces updated to same state (patch release if needed).
- [ ] Unresolved findings added as tasks in local task system.
- [ ] Run log recorded in `_after-care/LOG.md`.

## Changelog

### 1.6.0 (2026-07-24)
- Rule added: A factual correction applies across all surfaces. Empirically learned — a user clarification was corrected in Hub during run 1, but silently lingered in five places in the org profile (EN, DE, `llms.txt`) and was only noticed nine runs later.

### 1.5.0 (2026-07-24)
- Sharpened linter diagnosis after pattern occurred three times in one day (n8n-workflow-manager ruff 0.15, clirec + swarm-ai ruff 0.16): "check first", concrete tell-tale rule codes, platform split, `ruff.toml` fix when `pyproject.toml` missing, verification against new linter version.

### 1.4.0 (2026-07-24)
- Diagnosis added: When CI turns red after a pure doc commit, the most common cause is an unpinned linter without a locked ruleset — a new tool release shifts defaults and turns unchanged code red. Fix: pin ruleset, log new rules as task. Occurred twice in sequence.

### 1.3.0 (2026-07-24)
- New section "Findings Become Tasks": What the routine does not fix itself becomes a task entry in the project's local task system at the moment of discovery — where the next developer looks, not in a completed run log. Includes separation of internal lists from public roadmaps, enriching vs duplicating, logging completed tasks with commit hashes.

### 1.2.0 (2026-07-24)
- Privacy gate additionally searches for names of internal storage locations. They are not secrets, trigger no alerts, and survive gates checking only paths and tokens — but remain unresolvable for readers and expose internal structure.

### 1.1.0 (2026-07-24)
- Locks read rather than treated as blanket bans: a pure publish/push lock reroutes the routine to a local branch instead of aborting. Clarified that under such holds metadata, releases, and issue/PR actions are also omitted — they are remotely visible just like a push.

### 1.0.0 (2026-07-24)
- Initial version. Tier 1 of repository aftercare, derived from `github-repo-care`.