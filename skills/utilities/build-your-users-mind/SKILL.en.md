---
name: build-your-users-mind
version: 1.0.0
type: skill
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  Points to the public, provider-neutral build-your-users-mind module: a
  privacy-aware recipe for building an empirical Theory-of-Mind preference
  model of an authorized user from that user's own interaction logs. Use when
  an operator wants to build, validate, bind, or maintain a decision-avatar
  profile without publishing the personal profile or its evidence.
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [theory-of-mind, user-model, decision-avatar, feedback, privacy, pointer-skill]
language: en
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "external"
  origin_path: "SKILL.md, templates/, scripts/, schemas/, TAXONOMY.md"
  origin_version: "1.0.0"
  origin_repo: "https://github.com/ellmos-ai/build-your-users-mind"
  last_sync_from_origin: "2026-07-30"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="build-your-users-mind banner">

# build-your-users-mind — Public, provider-neutral pointer

This skill is a thin pointer to the public module
[`ellmos-ai/build-your-users-mind`](https://github.com/ellmos-ai/build-your-users-mind).
The module contains the complete recipe, templates, schemas, scripts, tests and
source-adapter documentation. This catalog does not duplicate that code.

## What the module does

With the operator's explicit authorization, the module helps an agent:

1. extract genuine user-authored turns from the operator's own interaction logs;
2. redact sensitive material before persistent storage;
3. reduce and classify evidence about recurring preferences and decisions;
4. create a local preference model with confidence levels and provenance;
5. bind a short pointer into the selected agent runtime; and
6. calibrate predictions against real later feedback.

The public module is a recipe for any user and any supported agent runtime. It
does not contain a model of a specific person.

## Safety and privacy boundary

- Operator authorization is required before reading interaction logs.
- Personal profiles, raw logs, evidence corpora and local paths remain private.
- Predictions are uncertain hypotheses, not mind-reading, diagnosis or statements
  made by the user.
- A preference prediction never expands the agent's authority.
- External, irreversible, safety-critical, legal, medical, employment,
  financial or similarly high-impact actions require explicit confirmation.
- Agent-generated predictions must never become primary evidence about the user.

## Installation

```bash
git clone https://github.com/ellmos-ai/build-your-users-mind.git <clone-path>
```

Follow the module's current `README.md`, `SKILL.md`, `SOURCE-ADAPTERS.md` and
privacy instructions. Keep the generated user profile outside public
repositories. The module repository is authoritative for implementation and
versioning.

## Public core and private profiles

`build-your-users-mind` is the public, user-neutral module name.
`decision-avatar` is the public runtime protocol in this catalog. A named
person's avatar, evidence files, local commands and profile-specific defaults
are private overlays and must not be published under a personal skill name.

## Changelog

### 1.0.0 (2026-07-30)

- Added the neutral pointer to the standalone public module.
- Replaced the previously published personal avatar profile with a strict
  public-core/private-profile boundary.
