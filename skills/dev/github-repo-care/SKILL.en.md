---
name: github-repo-care
version: 1.0.0
type: protocol
author: Lukas Geiger + Codex
created: 2026-06-18
updated: 2026-06-18
aliases: [github-pflege, repo-veroeffentlichen, repo-release, privacy-gate, release-gate]
description: >
  Protocol for safely creating, publishing, releasing, auditing, and maintaining GitHub repositories:
  check local rules and locks, create .gitignore before the first add, run privacy checks,
  prepare README/i18n/banner/metadata, verify release tags and GitHub releases, and update
  organization profiles, llms.txt files, and registry links.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: dev
tags: [github, repo, release, privacy, i18n, marketing, ci, documentation]
language: en
status: active

dependencies:
  tools: [git, gh, rg]
  services: [GitHub]
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.codex/skills/github-repo-care/"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-06-18"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# GitHub Repo Care — Publish and Maintain Repositories Cleanly

## When To Use

Use this skill when a GitHub repository needs to be created, published, released, audited, or maintained. It is especially important before the first public push, for release tags, repository metadata, organization profiles, and privacy checks.

Do not use it for pure implementation work without a GitHub publication step. Finish the relevant development or debugging workflow first, then activate this skill for publication.

## Core Rule

Prepare the repository before the first public push. A correct `.gitignore`, privacy gate, license, README, metadata, and release story are much cheaper before public history exists.

## Workflow

1. **Read local rules.** Check `AGENTS.md`, `CLAUDE.md`, `START.md`, release policy, naming policy, and lock policy when present.
2. **Check locks.** If `LOCK.txt` or a matching `LOCK.*.txt` is active, do not edit that scope.
3. **Fix the repository identity.** Confirm name, organization, visibility, license, and one-sentence purpose.
4. **Create `.gitignore` before `git add`.** Exclude secrets, local data, databases, build output, virtual environments, caches, IDE files, and private notes.
5. **Add public basics.** Typical files: `README.md`, `LICENSE`, `CHANGELOG.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `llms.txt`, and CI.
6. **Write the README for discovery.** First viewport: purpose, installation, usage, privacy model, project layout, license, and canonical repository name.
7. **Add visual signals.** Add a banner, logo, or screenshot when it makes the project easier to understand. Avoid generic decoration when a real product image or clear concept image is possible.
8. **Plan i18n deliberately.** Minimum: English plus the project language. Preferred standard set for user-facing modules: German, English, Spanish, Simplified Chinese, Japanese, and Russian.
9. **Run tests and smokes.** Verify locally before claiming success or creating a release.
10. **Run the privacy gate.** Check the staged/tracked set for secrets, local paths, PII, `.env`, databases, private documents, generated artifacts, and mojibake.
11. **Commit and push.** Commit only after the gate passes. Then create or connect the GitHub repository, push, and verify remote status.
12. **Set metadata.** Check description, topics, homepage, visibility, and default branch.
13. **Create the release.** Create the tag and GitHub release; verify CI for both branch and tag.
14. **Update discovery surfaces.** Link from the organization profile, `llms.txt`, central registries, local module indexes, and ecosystem READMEs.
15. **Final verification.** Check the remote README, release page, topics, CI, and links.

## Privacy Gate

Search the staged or tracked set, not only the visible working tree.

```bash
git diff --cached --check
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|C:/Us[e]rs/|/c/Us[e]rs/|s[k]-[A-Za-z0-9]|gh[p]_|gh[o]_|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|\\x{C3}|\\x{C2}|\\x{FFFD}" .
```

For public modules, also document a `RELEASE_GATE.md` or equivalent gate: date, checked commands, result, remaining warnings, and intentional exceptions. If a secret was ever committed, deleting it from `HEAD` is not enough; rotate the secret.

## GitHub Metadata

After the push, set metadata and release data explicitly.

```bash
gh repo edit ORG/REPO --description "Short concrete description" \
  --add-topic local-first --add-topic python --add-topic llm
git tag -a v1.0.0 -m "v1.0.0"
git push origin v1.0.0
gh release create v1.0.0 --repo ORG/REPO --title "v1.0.0" --notes "..."
```

Then verify:

```bash
gh repo view ORG/REPO --json nameWithOwner,visibility,description,repositoryTopics,url
gh release view v1.0.0 --repo ORG/REPO --json tagName,url,isDraft,isPrerelease
gh run list --repo ORG/REPO --limit 5
```

If CI is red after a release, the repository is not cleanly published yet. For a just-created initial release, immediately and intentionally moving the fresh tag to the corrected commit is acceptable.

## Common Mistakes

| Mistake | Fix |
|---|---|
| `.gitignore` is added after `git add` | Unstage first, fix ignore rules, then add again |
| README is monolingual although the UI or skill is multilingual | Add language links or localized READMEs |
| No banner, topics, or description | Add discovery assets before announcement |
| Release tag exists, but CI is red | Fix CI and verify the new run |
| Organization README is updated, but `llms.txt` is missed | Update both human and machine-readable surfaces |
| Local path appears in public docs | Replace it with relative paths or generic examples |
| Public repo contains a test database or notebook inbox | Remove it from tracking, add ignore rules, rerun the gate |

## Final Checklist

- [ ] Local rules and locks checked.
- [ ] `.gitignore` existed before the first add.
- [ ] Public docs, license, security, contributing, changelog, and `llms.txt` present.
- [ ] README includes repo name, purpose, installation, usage, privacy, and license.
- [ ] i18n expectation met.
- [ ] Banner, logo, or screenshot present when useful.
- [ ] Tests and smokes pass.
- [ ] Privacy, path, secret, database, and mojibake scans clean.
- [ ] GitHub description, topics, tag, release, and CI verified.
- [ ] Organization profile, registry, and ecosystem links updated.

## Changelog

### 1.0.0 (2026-06-18)
- Created initial repository care and publication protocol.
