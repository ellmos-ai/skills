---
name: community-outreach
version: 1.1.0
type: skill
author: Lukas / Antigravity
created: 2026-08-13
updated: 2026-08-29
description: >
  System-agnostic automation for solution-oriented community outreach and repository recommendation
  across forums, Reddit, and social platforms following Human-in-the-Loop principles (EU AI Act compliant).
category: dev
tags: [outreach, marketing, community, automation, scheduler, github, solution-recommender]
language: en
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
provenance:
  origin: custom
  origin_path: skills/dev/community-outreach/
  origin_version: 1.0.0
  last_sync_from_origin: 2026-08-13
dependencies:
  tools: []
  python: [pytest]
status: active
---

<img src="banner.png" width="100%" alt="community-outreach banner">

# Community Outreach & Solution Recommender

A provider-, LLM-, and OS-neutral skill for automated, solution-driven recommendation of open-source software, repositories, and developer tools across developer communities, Reddit discussions, technical forums, and video comments.

---

## 🌟 Core Principles & Safety Guarantees

1. **Human-in-the-Loop and fail-closed publishing:**
   * No automated post goes live without explicit human review.
   * Drafts are staged in `POST-EINGANG.md`. The checkbox `- [x] Genehmigt` only authorizes a publication attempt.
   * History, rotation, outbox, and duplicate registry advance only after a complete `PublishReceipt` bound to the platform and target URL. Without an injected publisher, the queue remains unchanged.
2. **Anti-Spam & 100% Relevance ("Better no post than an irrelevant one"):**
   * Every post directly solves an actual technical problem raised in the target thread.
   * Strict adherence to all board and community guidelines with transparent attribution.
3. **Strict Duplicate Prevention:**
   * Global `POSTVERZEICHNIS.md` index tracks every published thread URL.
   * No discussion thread or video is ever targeted twice.
4. **Fair Round-Robin & Platform Rotation:**
   * Repositories are rotated based on longest abstinence.
   * Target platforms alternate regularly (Reddit $\rightarrow$ YouTube $\rightarrow$ Dev.to/Forums $\rightarrow$ Reddit).
5. **Cut-and-Clue Self-Archiving:**
   * History logs automatically archive to `_archive/` when size thresholds are reached, maintaining clean pointer headers.

---

## 🔄 4-Phase Execution Cycle

1. **Phase 1 (Monitoring Inventory):** Counts published history records as threads requiring review. The core does not retrieve platform replies; that requires a separate authorized inbound adapter.
2. **Phase 2 (Outbound Execution):** Validates approved entries, exact URL duplicates, and an injected publisher. Only a verified `PublishReceipt` causes local state changes. The bundled CLI adapter does not publish by itself.
3. **Phase 3 (Research Task):** Selects the next repository via Fair Round-Robin and returns `needs-action`. A separate research step must persist a reviewed draft with a real, current, unused target URL; the core creates no placeholder target.
4. **Phase 4 (Self-Archiving):** Moves the oldest complete entries into `_archive/`, keeps the newest entries live, and is idempotent.

`--dry-run` is a pure planning mode: it does not invoke a publisher, change a file, or create a directory.

The verified German runtime guide is available at [`references/runtime-readme.md`](references/runtime-readme.md).
Deploy the relative, host-agnostic runtime files with `python scripts/deploy_runtime.py --target <workspace> --json`; add `--check` for a read-only byte comparison.

---

## ⚙️ Multi-Scheduler & Multi-Agent Operations

- **Antigravity Sidecar:** Registered as native background task running when the IDE is active.
- **Codex & Claude Code:** Run via cron, CLI scripts, or workflow loops.
- **Windows Task Scheduler & Unix Crontab:** Native OS-level scheduling options.

---

## Changelog

### 1.1.0 (2026-08-29)
- Added one canonical core with a thin runtime adapter and compatible readers for both earlier data schemas.
- Added fail-closed `PublishReceipt` validation, exact duplicate protection, byte-preserving queue updates, and restart-safe local projection.
- Made dry runs write-free, archiving entry-based and idempotent, and Phase 3 truthfully return `needs-action`.

### 1.0.0 (2026-08-13)
- Initial release: Universal Community Outreach & Solution Recommender Skill.
