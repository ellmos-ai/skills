---
name: surface-after-care
version: 1.6.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-07-24
updated: 2026-07-30
aliases: [repo-after-care, repo-pflege, after-care, repo-nachpflege, repo-wartung]
description: >
  Regular maintenance round for an already published GitHub repository (Level 1,
  low-cost and frequently repeatable): first identify all distribution channels of the project
  (npm, PyPI, registries, marketplaces, stores, website) and mirror changes there later,
  then set topics, run privacy gate, check documents for intent to publish and retroactively ignore
  internal planning files, add banners, align statements in the README with the actual code state,
  improve presentation, complete README language versions, implement visibility measures, check entry
  on the organization page, and process open issues and pull requests.
  Use this skill when an existing repo needs to be maintained, cleaned up, updated, polished,
  or "reviewed again", when a repo appears outdated or cluttered, on phrases like "repo maintenance",
  "after care", "bring repo up to date", "clean up and push", or during rotating quality rounds across multiple repos.
  For the deep round including legal check and cross-organization references, use full-after-care instead;
  for initial publishing, use github-repo-care.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: dev
tags: [github, repo, maintenance, privacy, i18n, documentation, visibility, issues]
language: en
status: active

dependencies:
  tools: [git, gh, rg]
  services: [GitHub]
  protocols: []
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

<img src="banner.png" width="100%" alt="surface-after-care banner">
# Surface After Care — The Regular Maintenance Round for a Published Repo

## When to use this skill

Use it for a repository that is **already public** and needs routine review. It is the low-cost tier: everything that can be decided within the repo itself without inventorying third-party repos or initiating a legal review.

Distinction from neighboring skills:

| Situation | Skill |
|---|---|
| Repo is published for the first time | `github-repo-care` |
| Repo is public, regular maintenance round | **this skill** |
| Additional legal check + cross-references across all orgs + app i18n | `full-after-care` (Alias `deep-after-care`) |
| Pure legal/privacy/license check prior to making public | `repo-publish-check` |
| Keep document language versions synchronized in content | `bilingual-doc-sync` |
| Distribute this round across many repos, fairly rotating | `rotation-check` |

## Core Idea

A published repo drifts apart in two directions: **The documentation describes older software than what resides in the repo**, and **files accumulate that were never intended for external eyes**. Neither is usually dramatic, but both cost exactly the users you want to win over — one drops off because the installation guide no longer works, the other because they encounter `AUFGABEN.txt` and `Plan.txt` in the root directory, getting the impression someone here is only working for themselves.

This round cleans up both. It is deliberately repeatable: better half an hour four times a year than one massive overhaul.

## Workflow

The sequence is not arbitrary. Step 0 comes first because it determines the scope of all subsequent steps. Step 2 runs before anything that pushes changes — otherwise you push improvements over a state that still needs cleaning. Step 1 is purely server-side and does not interfere.

### 0. Inventory distribution surfaces

**Before changing anything: clarify where this project is located everywhere.** The GitHub repo is rarely the only surface. A corrected README is of little use if the npm package page continues to show the old version with incorrect installation instructions — and that is where most users land, because package registries often rank better in search engines than the repo.

```bash
# Manifests reveal channels
cat package.json pyproject.toml setup.py Cargo.toml 2>/dev/null | rg -n "name|version|keywords|repository|homepage"
rg -n "npmjs.com|pypi.org|marketplace|registry|crates.io|hub.docker|zenodo|doi" README* docs/ .github/ 2>/dev/null

# Query published state of channels (only applicable ones)
npm view <paket> version description keywords 2>/dev/null
pip index versions <paket> 2>/dev/null
gh release list --repo ORG/REPO --limit 5
```

Typical surfaces: npm, PyPI, Crates, Docker Hub, MCP registry, plugin/skill directories, VS Code or browser marketplaces, app stores, Zenodo/DOI, project website, organization profile, `llms.txt`, mirror repos on other hosts.

Note the list found in the execution log. From now on, it is the **target set**: Every change from the following steps is mirrored against this list at the end (see "Parity across all surfaces"). If you find a surface that nobody maintains anymore pointing to dead code, that is a finding in itself — either update or deliberately withdraw, but do not leave it abandoned.

### 1. Set topics

Topics are the most important search surface inside GitHub and cost almost nothing.

```bash
gh repo view ORG/REPO --json nameWithOwner,description,repositoryTopics,homepageUrl,visibility
gh repo edit ORG/REPO --add-topic <topic> --add-topic <topic>
```

Aim for roughly 5–12 topics from three angles: **what it is** (`cli`, `mcp-server`, `python-library`), **what it is about** (`file-management`, `tax`, `note-taking`), and **how it works** (`local-first`, `offline`, `privacy`). Align with topics actually used in comparable projects — invented topics won't find users. Check description and homepage at the same time; they appear in the same view.

Topics have a counterpart on the other surfaces from Step 0: `keywords` in `package.json`, `keywords`/`classifiers` in `pyproject.toml`, categories and tags in marketplaces and stores. Keep them identical in content — they represent the same decision in multiple places.

### 2a. Privacy Gate — always runs

This step is never omitted, even during a seemingly harmless round. Search within the **tracked** set, not the visible working tree, because that is the difference between "looks clean" and "is clean".

```bash
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|/home/[a-z]|s[k]-[A-Za-z0-9]{16}|gh[p]_|gh[o]_|AKIA[0-9A-Z]{16}|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|BEGIN [A-Z ]*PRIVATE KEY" $(git ls-files)
rg -n "\x{C3}\x{83}|\x{C2}\x{A0}|\x{FFFD}" $(git ls-files -- '*.md' '*.txt' '*.json')
```

Supplement the pattern with the **names of your own internal repositories/folders** — pipeline folders, topic directories, private workspaces:

```bash
rg -n "\.SOFTWARE|\.RESEARCH|_control-center|<weitere eigene Ordnernamen>" $(git ls-files)
```

Such references are not secrets and do not trigger security scanners, so they slip through — but they are **unresolvable** for external readers ("transferred back from .SOFTWARE pipeline" tells strangers nothing) and leak your internal structure. Replace or remove them, do not merely tolerate them. A search looking only for `C:\Users\…` and token patterns is guaranteed not to catch them.

Found something? Then the **nature** of the finding dictates the procedure — see section "Force-Push Rule". A secret once committed is compromised: removing it from `HEAD` is insufficient, it must be rotated.

### 2b. Check publication intent of documents

The actual core of this round. Go through tracked `.md`, `.txt`, and `.json` files and ask for each: **Was this ever intended for external eyes?**

```bash
git ls-files -- '*.md' '*.txt' '*.json' | sort
```

Do not guess by filename — take a brief look inside. A `PLAN.md` might be a public roadmap, a harmless-sounding `notes.md` the internal pricing strategy. Three categories:

**Belongs in repo** — README, LICENSE, CHANGELOG, SECURITY, CONTRIBUTING, `docs/`, API references, sample configs, real roadmaps, manifests (`package.json`, `pyproject.toml`), lockfiles, CI configuration.

**Does not belong in repo, but uncritical** — the standard case of this round. Task and planning files (`AUFGABEN.txt`, `Plan.txt`, `TODO-intern.md`), session notes and handoffs (`HANDOFF`, `BRIEFING`, `_handoff/`), own pipeline status files, dev diaries, `_archive/`, registry and index JSONs with local paths, intermediate states and generated artifacts, agent working files. These files are not dangerous, but they create clutter and the impression of an unkempt construction site. Remedy: update `.gitignore`, `git rm --cached <file>` and **push normally**.

**Does not belong in repo and sensitive** — Credentials, personal data, customer data, internal calculations, pricing/negotiation strategies, unpublished business plans, draft contracts, anything with competitive value. Here a normal commit is insufficient, see Force-Push Rule.

For `.json` files, take a second look: manifests and lockfiles remain, but local configs, task/registry files, export dumps, and anything with absolute paths or hostnames are typical stowaways.

If you remove a file that someone might search for (a roadmap for instance), briefly mention in the commit or README where the information now lives — otherwise it looks like a regression.

### 3. Banner

A banner often decides whether someone starts reading at all. Check if one exists and is embedded as the first element in the README.

If missing, there are three paths — recommended in this order:

1. **Agent image generator** (e.g., agy; the word "generate" triggers real PNG generation there) if a visual motif fits better than typography.
2. **Codex**, if the banner should be generated from code and an aesthetic reference exists to align with.
3. **Self-built as SVG**, if the banner is primarily a wordmark plus form language — this is often the fastest and most controllable option, and SVG remains editable later.

Maintain the design family if the project belongs to a group: same base color, same aesthetics, same wordmark treatment. A banner that falls out of line looks worse than none. Standard size 1200x300; save PNG in repo, keep SVG source alongside.

### 4. Align statements against actual code state

Here lies the most value. The README makes claims — verify them instead of believing them:

- **Version** in README/badge against `pyproject.toml`/`package.json`/`__version__` and against the latest release tag. If there are multiple version carriers, check all of them.
- **Installation path** run through, at least by reading: Does the package exist under the named name? Do commands and flags match?
- **Feature list** against code: Is everything listed present, and is anything new missing from the list?
- **Numbers** (number of tools, supported formats, test coverage) recount at the source instead of carrying forward. Numbers in READMEs age quietly.
- **Screenshots** against current UI.
- **Requirements** (Python/Node version, dependencies) against manifests.
- **Links** to neighbor projects, docs, and registries: do they still work?

**A correction applies to all surfaces, not just the one where it was noticed.** If a statement turns out to be wrong — especially if clarified by the owner —, the same statement is very likely present elsewhere: in the organization profile, in `llms.txt`, in the second language version, in the README of a neighbor project. Search specifically for it before marking the item as done:

```bash
gh search code "<concise phrase>" --owner ORG
```

Otherwise you fix one spot and leave three standing — and the contradiction only surfaces when the next repo comes around. That not only wastes time, it damages trust in documentation: Anyone finding two descriptions of the same thing believes neither.

Then improve **presentation** where it is weak: long option lists become more readable as tables; code blocks need language tags; a structure or workflow overview is captured faster as a Mermaid diagram or ASCII tree than in prose; the first screen height should show purpose, installation, and a usage example, not badges and backstory. If the README exceeds ~400 lines, delegate details to `docs/` and link them.

**Language rule for READMEs:** Default is an **English `README.md`** plus a **German second version**. Exception: The domain of the application is German itself (German law, German tax/funding system, German-speaking target audience) or there is currently only a German version — then German remains the primary language. For every additional language the project already supports in code, a matching README version belongs alongside. Adhere to the naming convention already established in the repo (`README_de.md`, `README.de.md`, `docs/README.de.md`) and do not invent a second one. Cross-link versions mutually in the header.

### 6. Add missing standard languages

Add README versions missing from the **standard languages**: German, English, Spanish, Simplified Chinese, Japanese, Russian. The purpose is reach, so this applies primarily to user-facing projects — for a developer-focused library with a purely English audience, a Russian README is not a gain, only additional maintenance burden. Decide consciously and log the decision so the next round doesn't debate it anew.

New versions are **populated, not created empty** — a stub with "TODO: translate" is worse than no file because it feigns completeness. Content parallelism and realignment are handled by `bilingual-doc-sync`; with more than two versions, it pays to invoke that skill.

### 7. Visibility and Promotion

Consider which measures actually bring users for **this** project and implement them:

- **Registries** where the project technically belongs: Package registries (npm, PyPI), MCP registry, plugin/skill directories, marketplaces.
- **Curated lists** (`awesome-*` and thematic collections), provided admission criteria are genuinely met. A PR to a list whose criteria the project fails costs reputation.
- **Own surfaces**: Organization profile, `llms.txt`, project website, ecosystem README, links from related own repos.
- **Release notes** as occasion: A release without a narrative behind new features goes unnoticed.

**Approval Gate:** Anything going outward — PRs to external repos, entries in external lists, posts, submissions — is **proposed and executed only after explicit approval**, unless permanent authorization exists for that channel. Changes to own surfaces do not require this gate. The reason is simple: A retracted PR on a foreign repo is publicly visible and reflects back on the project.

### 8. Entry on organization pages

First the own organization: Is the repo listed in the profile README (`ORG/.github` → `profile/README.md`) at all, in the correct section, with an up-to-date description?

```bash
gh api user/orgs --jq '.[].login'
```

Then go through **all** organizations and answer a single question per organization: Would a visitor to this organization page benefit from this repo? Mostly the answer is no — then "do not link" is the correct result and not a gap. Where the answer is yes (thematic proximity, shared users, a tool complementing projects there), set the reference with a line explaining the benefit, not just naming the repo.

The profile lives in its own repo (`ORG/.github`). Changes there are maintained and pushed alongside — following the Dirty Tree Rule from Step 11.

### 10. Issues and Pull Requests

```bash
gh issue list --repo ORG/REPO --state open --limit 50
gh pr list --repo ORG/REPO --state open --limit 30
```

Work through them instead of merely counting:

- **Fixable bugs** repair directly — context is loaded anyway during this round. Small, well-defined fixes with tests and reference to issue number.
- **Already resolved issues** close with a sentence explaining what fixed them.
- **Unclear reports** request targeted clarification (version, OS, reproduction steps).
- **PRs**: Read diff thoroughly, run tests, then merge or reply with reasoning. A PR lying unhandled for months costs more goodwill than a polite rejection.
- **Stale cases** resolve instead of dragging along.

**Approval Gate:** Public comments, closing with reasoning, and merging external contributions are outward communication — present prior to execution unless permanent authorization exists. Pure code fixes in own repo are exempt.

### 11. Commit, push, verify

The round does not end with edits, but when they are **pushed out**. A working tree full of unpushed improvements is the worst outcome: The next session — possibly another agent or device — must first orient itself in an unfamiliar, half-finished state, and nothing has improved on public surfaces.

Before pushing, briefly secure what is verifiable: run tests and smoke checks, verify links and rendered view for doc edits. Then bundle into **thematically separate commits** rather than dumping everything into one catch-all commit — cleanup, doc updates, and bug fixes are three different things, and whoever needs to revert one later will be grateful:

```bash
git add .gitignore && git rm --cached <interne dateien>
git commit -m "chore: remove internal work files from tracking"
git commit -am "docs: update README (version, tool count, screenshots)"
git commit -am "fix: <issue number> ..."

git pull --rebase        # if branch diverged, before pushing
git push
```

Then verify instead of assuming: Remote README in rendered view, CI run, release and tag state.

```bash
gh run list --repo ORG/REPO --limit 3
gh repo view ORG/REPO --json description,repositoryTopics,url
```

**If CI turns red even though your commit only touched docs**, the cause is almost never your change. By far the most common case — encountered **three times** in a single day across this repo family — is an **unpinned linter without a fixed rule selection**. Check this **first** before suspecting your commit.

The mechanism: If the workflow runs `ruff check` (or flake8, eslint …) against an unpinned dependency (`ruff>=0.12`, or no version at all), and lacks explicit rule selection (`[tool.ruff.lint] select = [...]`, or a `ruff.toml` if `pyproject.toml` is missing), then the linter follows the default of the **newly installed** version. A new linter release shifts this default, making unchanged code turn red. Tell-tale signs:

- Rule codes the project never had (`UP045`, `UP006`, `BLE001`, `RUF100`, `DTZ005`, `N999` …), sometimes in three-digit numbers.
- The failure often breaks **across platforms**: Runners with cached older versions remain green, fresh runners turn red.
- Sometimes a rule flags something unfixable (`N999` on package name itself) — a sure sign it was never standard.

Fix: Pin the rule selection that was previously green — `select = ["E4","E7","E9","F"]` are classic ruff defaults. If `pyproject.toml` doesn't exist, create `ruff.toml`. Verify against the **new** linter version itself (install, reproduce findings without config, see "passed" with config). New rules become a **task** for the project — adopting them consciously is a decision, not a side effect of a tool update. This is a real, recurring finding: Without the pin, CI breaks again on the next linter release across **every** similarly configured repo.

Two cases where pushing is **not** performed: if a publication/submission freeze applies to the project, or if the state is explicitly unfinished. Both are exceptions requiring rationale — the standard case is: commit and push.

Under a publication freeze, the round is not aborted, but **redirected**: commit locally on a dedicated branch (`judging-hold/…`, `freeze/…`), leave the main branch untouched on the submitted state, record the freeze reason in the execution log, and catch up after release. Consistency is vital: Frozen is not just `git push`, but **any remotely visible change** — topics, description, homepage, releases, issue/PR actions modify the published project just as well.

If other clones of the same repo exist (second device, deploy copy, mirror), pull them immediately after push. A clone ten commits behind produces diagnostic errors against a state that no longer exists during the next debugging session.

#### Edits to other repos — Dirty Tree Exception

This round regularly produces changes **outside** the maintained repo: a line in the organization profile (Step 8), later in the deep round a reciprocal link in a related repo. Such changes are also committed and pushed — an unpushed reciprocal link is no link.

Before touching a foreign repo, briefly check its status:

```bash
git -C <path> status --porcelain
```

**Clean working tree** → make edit, commit in a **separate, thematically clear commit** (`docs: link <project>`) and push. Do not mix with commits of the maintained repo: It is a different repo with its own history and readers.

**Dirty, but external edits are in other files** → your edit can still be made cleanly. Stage and commit **path-specifically only your file**, so foreign, unverified work is not included:

```bash
git -C <path> add README.md
git -C <path> commit -m "docs: link <project>"     # only staged path
```

But **do not push**. The commit is locally harmless; a push might not be: You don't know what the other work state aims for — maybe it is currently being amended, rebased, or sliced differently, and your push forces others to resolve it. The local commit secures work without imposing; the run later focusing on that repo will find it and take it along.

**Dirty in the exact file you must edit** → do not touch. Here you would build on a foreign intermediate state and commit it along; understanding it first costs more than this single link is worth.

**Active lock (`LOCK*.txt`) in target repo** → **first read the lock instead of treating it as a blanket ban.** A lock describes its own scope, which is often narrower than "nothing at all". Typical cases:

- **Edit lock** ("someone is actively working here") → touch nothing, not even side files.
- **Pure publication/push lock** (submission, judging, freeze) → local work remains allowed, only remote contact is blocked. Work on a dedicated branch and commit locally; **remote-visible steps drop out** — not just push, but also topics, description, homepage, releases, and issue/PR actions.

Reading a lock that only blocks push as a total prohibition wastes the entire local part of the round with no safety gain. Conversely, omitting only push while altering metadata is insufficient. When in doubt, cite the lock and ask.

#### The request must not be lost

If an edit is **not** executed due to one of these reasons, record it in the target repo's task list — `AUFGABEN.txt`, `TODO.md`, or `TODO.txt`, depending on what exists there. An entry with date, desired edit, and reason:

```markdown
- [ ] [2026-07-24, after-care] Add reciprocal link to <project> in README
      (skipped: README had uncommitted third-party edits)
```

That is the difference between "postponed" and "forgotten": The task list resides where the next maintainer of that repo looks anyway — more reliable than a note in the log of a foreign run. If no task list exists, do not create one; the open item in your own log is sufficient.

Under an **active lock, even this does not apply** — the file is left untouched and the note stays solely in your own execution log. Record it there in both cases so rotation knows about open points.

Finally, service the surfaces from Step 0 — see next section.

## Parity across all distribution surfaces

At the end of the round, check against the list from Step 0: **Every change a user would see must arrive on every surface where they look for it.** A repo whose npm page tells a different story than GitHub is worse off than one with only a single surface.

The decisive mechanism: **Package registries display the README of the last publish, not the current repo state.** A README correction on npm or PyPI becomes visible only with a new version. If the correction is content-relevant (wrong installation, wrong version, outdated feature list), a patch release belongs with it — otherwise the fix remains ineffective.

| Surface | What is maintained there | How it arrives |
|---|---|---|
| npm | README, `description`, `keywords`, repository link | Only via `npm publish` (patch version); metadata comes from `package.json` |
| PyPI | README (`long_description`), classifiers, project URLs | Only via new upload; metadata from `pyproject.toml` |
| MCP registry / Plugin directories | Description, version, tool list, entry docs | Depends on registry: manifest update or resubmission |
| Marketplace / Store | Description, screenshots, categories, language versions | Via respective management UI; screenshots age particularly fast there |
| Docker Hub / Container registry | Description, tags, usage example | Repo description plus new tag |
| Zenodo / DOI | Metadata, authors, version | In-place edit for metadata, new version for content |
| Website / Org profile / `llms.txt` | Short description, link, positioning | Directly editable — cheapest surfaces, never forget them |

When a version is bumped, **all version carriers** must move simultaneously: manifest, code constant, README badge, changelog, release tag, `llms.txt`. A half-bumped version state is harder to diagnose than an consistently old one.

If an update on a surface is currently impossible or impractical (e.g., a release solely for a typo), record it in the execution log so the next round does not mistake the deviation for an oversight.

## Force-Push Rule

The default is **no force push**. Retroactively ignoring internal planning files does not justify rewriting history: Effort is high, every clone and fork breaks, open PRs become unusable — and gain is minor because content is uncritical. Standard way:

```bash
git rm --cached <file>            # remove from tracking, keep locally
# update .gitignore
git commit -m "chore: remove internal work files from tracking"
git push
```

Rewriting history (and pushing with `--force-with-lease`) is justified only for **actual leaks**: credentials and keys, personal or customer data, and documents with genuine competitive value — internal calculations, pricing strategies, unpublished plans, contract internals. In that case:

1. **Rotate affected secrets first** — history is already copied, forked, and cached by then. Rotation works; deletion is cosmetic.
2. Clean history (`git filter-repo` or BFG), push with `--force-with-lease`.
3. Check forks and caches; contact GitHub support for orphaned objects if necessary.
4. Record procedure in execution log: what, when, which rotation.

When in doubt between "uncritical" and "sensitive": treat as sensitive and present for review. Costs are asymmetric.

## Findings become tasks, not just log lines

A maintenance round regularly finds more than it can or should resolve in the same run: a missing language version, a modernization backlog, a publication that never happened. **Such findings become tasks at the moment of discovery** — otherwise they remain buried in the log of a completed run where the next project maintainer will not look.

The task belongs in the **folder-local task system of the project** — where the person working next on this project checks. Typically that is `AUFGABEN.txt` or `TODO.md` in the project folder, which is often **not inside the Git clone**, but in the directory where project planning lives. The clone contains code; the project folder contains management; an entry in the clone that disappears on the next `git clean` is no task.

Keep three things in mind:

1. **Separate internal task list from public roadmap.** A `TODO.md` can be a maintained public roadmap — then it is no dumping ground for internal rework. Look inside before appending: If a heading like "Public roadmap" appears, write to the internal file alongside (`AUFGABEN.txt`) and mark it internal.
2. **Check existing entries before duplicating.** Often the finding is already listed. Then do not create a new entry, but **enrich** it — with empirical evidence from this run ("confirmed: `--help` outputs German text"). A known point with fresh evidence is more valuable than a second duplicate entry.
3. **Log completed items.** What the round resolved belongs as a checked-off item with commit hash. That explains to the next round why a finding disappeared and prevents re-discovering it.

Formulate tasks so they make sense without the context of this run: what was found, why it matters, what the next step would be. "i18n incomplete" is not a task; "Catalog contains only `status.title`, there es/zh/ja/ru are empty — first transfer CLI strings to catalog, then populate all six languages" is one.

## Execution log

Record results in `_after-care/LOG.md` (the folder belongs in `.gitignore` — it is pipeline material, not repo content, following Step 2b). One line per run with date, level, and conscious decisions:

```markdown
## 2026-07-24 — surface
- Surfaces: GitHub, npm (<paket>), MCP registry, Org profile, llms.txt
- Topics: +local-first, +mcp-server; keywords in package.json aligned
- Removed: AUFGABEN.txt, _handoff/ (gitignored, no force push needed)
- README: Version 0.9 -> 1.2 corrected, tool count 23 -> 26 recounted
- Languages: EN + DE maintained; ES/ZH/JA/RU consciously skipped (dev-focused audience)
- Issues: #12 fixed, #7 closed (done), #15 question asked
- Push: 3 commits, CI green; npm republish 1.2.1 due to README fix
- Open: Store screenshots outdated, require new build
```

The log saves the next round from making the same decisions again and forms the basis for rotating maintenance runs across many repos (`rotation-check`).

## Common mistakes

| Mistake | Correction |
|---|---|
| Looked only at working tree, not `git ls-files` | Always check tracked set — that is where issues hide |
| Privacy gate searched only paths and tokens | Also search for own pipeline/folder names — they trigger no alerts and slip through |
| Internal file removed while rewriting history | For uncritical files, `git rm --cached` + normal push is sufficient |
| Secret removed from `HEAD` and considered done | Rotate secret; anything else is cosmetic |
| Classified files strictly by filename | Look inside briefly — names don't convey intent reliably |
| Recarried numbers in README without recounting | Count at source (tool list, test run, manifest) |
| Created new language version as empty stub | Populate or omit — a stub feigns completeness |
| Introduced second README naming convention | Adopt existing convention in repo |
| Submitted PR to foreign list without approval | Present external communication first; only own surfaces are free |
| Counted issues instead of processing | Fix, close, or request info — every case gets a state |
| Created banner independently in foreign style | Maintain ecosystem design family |
| README in repo fixed, npm/PyPI page still shows old | Registry pages stem from last publish — patch release needed |
| Version bumped only in manifest | All version carriers simultaneously: manifest, code, badge, changelog, tag, `llms.txt` |
| Changes ready, but left unpushed | Committing and pushing belongs to round; only freezes justify exception |
| Everything in single catch-all commit | Separate cleanup, docs, and fixes — otherwise nothing can be reverted individually |
| CI red after doc commit, suspected self | Unpinned linter without `select` follows default of new version — pin ruleset |
| Corrected wrong statement only where noticed | Search org-wide for phrase — usually stands in org profile, `llms.txt`, and 2nd language version |
| Worked in dirty foreign repo with `commit -a` | Stage path-specifically and commit, do not push — foreign work remains untouched |
| Made edit in clean org profile repo, but did not push | Clean foreign repos get separate commit **and** separate push |
| Skipped edit noted only in own log | Additionally record in target repo's task list, if one exists |
| Finding written only to log | It becomes a task in folder-local task system — nobody looks in log later |
| Internal rework attached to public roadmap | Check inside first; "Public roadmap" means: use internal file alongside |
| Known finding duplicated as new entry | Enrich existing point with empirical evidence from this run |
| Under edit lock wrote TODO line into locked repo | Lock applies to entire project — touch nothing there |
| Read push lock as total prohibition and skipped repo entirely | Read lock: if it blocks only publish, run local round on dedicated branch |
| Under push lock omitted push, but edited topics/description | Metadata is remotely visible — under publication freeze it drops out as well |

## Final checklist

- [ ] Distribution surfaces identified and noted in execution log.
- [ ] Topics, description, and homepage set and verified.
- [ ] Privacy gate run over tracked set, findings handled.
- [ ] `.md`/`.txt`/`.json` checked for publication intent, internal files ignored.
- [ ] No force push without actual leak; rotation conducted upon leak.
- [ ] Banner present and embedded in README.
- [ ] Version, features, numbers, screenshots, links verified against actual state.
- [ ] Presentation improved (tables, diagrams, first screen height).
- [ ] README language matrix complete; decisions on further languages documented.
- [ ] Visibility measures implemented or presented for approval.
- [ ] Entry in own org profile checked, meaningful foreign org links set.
- [ ] Edits to foreign repos: clean → committed and pushed; dirty → committed locally;
      unexecuted → recorded in target repo task list.
- [ ] Issues and PRs brought to defined state.
- [ ] Separate commits created, pushed, CI and remote view verified.
- [ ] All distribution surfaces brought to same state (patch release if needed).
- [ ] Unresolved findings recorded as tasks in folder-local task system.
- [ ] Execution log written in `_after-care/LOG.md`.

## Changelog

### 1.6.0 (2026-07-24)
- Added rule: A content correction applies to all surfaces. Empirically learned — a user clarification was corrected in run 1 in hub, but stood unnoticed five more times in org profile (EN, DE, `llms.txt`) and was only noticed nine runs later.

### 1.5.0 (2026-07-24)
- Sharpened linter diagnosis after pattern occurred three times in a single day (n8n-workflow-manager ruff 0.15, clirec + swarm-ai ruff 0.16): "check first", concrete culprit rule codes, platform split, `ruff.toml` fix when `pyproject.toml` is missing, verification against new linter version.

### 1.4.0 (2026-07-24)
- Added diagnosis: If CI turns red after a pure doc commit, most frequent cause is unpinned linter without fixed ruleset — new tool release shifts default and makes unchanged code red. Fix: pin ruleset, new rules as task. Occurred twice in a row (n8n-workflow-manager with ruff 0.15, clirec with 0.16).

### 1.3.0 (2026-07-24)
- New section "Findings become tasks": What the round cannot fix itself becomes an entry in folder-local task system of project upon discovery — where next maintainer looks, not in log of completed run. Includes separation of internal list and public roadmap, enriching instead of duplicating, completed items with commit.

### 1.2.0 (2026-07-24)
- Privacy gate additionally searches for names of own internal folders. They are not secrets, thus trigger no alarms and survive gates targeting only paths and tokens — but remain unresolvable for readers and leak internal structure.

### 1.1.0 (2026-07-24)
- Locks read instead of treated as blanket bans: pure publication/push lock redirects round to local branch instead of aborting. Clarified that under such lock metadata, releases, and issue/PR actions drop out as well — they are remotely visible just like push.

### 1.0.0 (2026-07-24)
- Initial version. Level 1 of repo maintenance, derived from `github-repo-care`.
