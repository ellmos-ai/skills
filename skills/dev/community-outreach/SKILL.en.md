---
name: community-outreach
version: 1.0.0
type: skill
author: Lukas / Antigravity
created: 2026-08-13
updated: 2026-08-13
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

1. **Human-in-the-Loop & EU AI Act Compliance:**
   * No automated post goes live without explicit human review.
   * Drafts are staged in `POST-EINGANG.md`. Only when the checkbox `- [x] Genehmigt` (Approved) is set will the post be published.
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

1. **Phase 1 (Inbound Feedback Check):** Scans active threads in `POST-AUSGANG.md` for replies or feedback.
2. **Phase 2 (Outbound Execution):** Identifies approved entries (`- [x] Genehmigt`) in `POST-EINGANG.md`, posts them via browser session, transfers them to `POST-AUSGANG.md`, and indexes URLs in `POSTVERZEICHNIS.md`.
3. **Phase 3 (Research & Staging):** Selects the next repository via Fair Round-Robin, finds a matching online query, drafts a high-quality response, and stages it for approval in `POST-EINGANG.md`.
4. **Phase 4 (Self-Archiving):** Cleans up logs exceeding capacity into `_archive/`.

---

## ⚙️ Multi-Scheduler & Multi-Agent Operations

- **Antigravity Sidecar:** Registered as native background task running when the IDE is active.
- **Codex & Claude Code:** Run via cron, CLI scripts, or workflow loops.
- **Windows Task Scheduler & Unix Crontab:** Native OS-level scheduling options.
- **ellmos-scheduler:** Central daemon for multi-agent environments.

---

## Changelog

### 1.0.0 (2026-08-13)
- Initial release: Universal Community Outreach & Solution Recommender Skill.
