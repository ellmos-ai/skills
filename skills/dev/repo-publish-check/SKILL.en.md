---
name: repo-publish-check
description: User-neutral repository review before publication or during a later public re-check. Covers privacy, secrets, licenses, third-party content, documentation, and approval status without publishing the repository itself.
version: 1.1.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-07-30
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [release, privacy, license, repository, publication]
language: en
status: active
dependencies:
  tools: [git]
  services: []
  protocols: []
  python: []
---

<img src="banner.png" width="100%" alt="repo-publish-check banner">

# Repo Publish Check

## Purpose

Review a repository before first publication or during a later public
re-check. A negative outcome is valid. Change visibility only after the
repository owner has explicitly approved it.

This skill does not produce legal opinions. For a legally sensitive domain or
unclear case, use the public `law-checker` skill. Neither skill replaces
professional legal advice.

## Privacy of review records

Never commit review reports or risk assessments to the reviewed repository.
Store them in a private review area outside the project or in a gitignored
directory such as `<private-review-dir>`. Publish only the required fixes, such
as license attribution, a privacy notice, or a more accurate description.

## Review workflow

1. **Define the release set:** inspect `git ls-files`, package allowlists, and
   `.gitignore`; exclude internal notes, reports, test data, local settings,
   and lock files.
2. **Scan privacy and secrets:** search the working tree and all reachable
   history for credentials, tokens, private keys, local user paths, contact
   details, and personal data. Classify and remediate every finding.
3. **Verify license and provenance:** provide a suitable `LICENSE`, state what
   it covers, and inventory third-party code, prompts, documentation, and
   media with their origin and license.
4. **Define purpose and boundaries:** document what the project does and does
   not do. For law, health, finance, security, or personal data, document data
   flows and excluded uses. Route legal questions through `law-checker`.
5. **Review privacy and cloud use:** minimize data, disclose external
   processing, and warn users not to post confidential case data in public
   issues.
6. **Review AI and product claims:** document intended purpose, role, limits,
   and transparency notes. Do not imply certification or quality that is not
   evidenced.
7. **Review name and presentation:** check package and repository names,
   possible trademark conflicts, README claims, descriptions, and badges.
8. **Conclude:** record findings, fixes, open risks, and a traffic-light result
   in the private report; verify the final commit and obtain explicit owner
   approval before a separate authorized publication step.

## Existing public repositories

At minimum, re-check privacy and secrets, license coverage, third-party
content, disclaimers, and public presentation. Report critical historical
findings to the repository owner instead of silently overwriting them.

An organization may maintain a private review queue and report store. Those
belong to its private workflow, not to this public skill.

## Limits

- This skill does not publish anything.
- It does not replace legal advice or an official trademark search.
- A clean source scan does not prove that earlier public copies, registries, or
  caches have been removed.
