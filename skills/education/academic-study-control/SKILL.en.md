---
name: academic-study-control
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-06-20
updated: 2026-06-20
description: >
  Use when managing studies, semester planning, module prioritisation,
  deadlines, exam registrations, or institutional emails need to be
  checked, planned, or converted into reminders. Coordinates web research,
  local status files, and optional calendar and mail integration.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: education
tags: [studies, semester, deadlines, exams, planning, calendar, mail, university]
language: en
status: active

dependencies:
  tools: []
  services: []
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

# Academic Study Control

## Overview

Manage studies and deadlines with source verification, privacy compliance, and
realistic planning. This skill is institution- and LMS-neutral: placeholders
(in angle brackets) are adapted to the concrete context by the agent on first use.

## Configuration

| Placeholder | Example value | Meaning |
|---|---|---|
| `<INSTITUTION>` | University of A, TU Berlin | Official name of the institution |
| `<LMS>` | ILIAS, Canvas, Stud.IP | Learning management system |
| `<MODULE_PREFIX>` | MM, MF, MO | Abbreviation used in module codes |
| `<STATUS_FILE>` | STATE.md, SEMESTER.md | Local status file of the student |
| `<INDEX_FILE>` | LLM_INDEX.md, INDEX.md | Local index file |
| `<CALENDAR>` | Google Calendar, iCal | Calendar application (optional) |
| `<MAIL>` | Gmail, Outlook, Thunderbird | Mail client or connector (optional) |

## Workflow

1. **Clarify the goal:** Semester plan, weekly plan, exam registration, re-enrollment,
   deadline check, mail check, module change, or reminders.
2. **Check local state:** `<STATUS_FILE>`, `<INDEX_FILE>`, relevant module folders,
   existing plans, and official documents from the institution.
3. **Check current institutional state live:** Official websites of `<INSTITUTION>`,
   examination office, `<LMS>` announcements, and — if available and requested —
   institutional emails.
4. **Record time references absolutely:** today's date, semester, deadline date,
   source, retrieval date.
5. **Derive a decision or plan** — do not just collect links or information.

## Research

- Always use web research or original documents for current information.
  Dates, exam formats, re-enrollment windows, fees, and announcements change
  regularly.
- Preferred sources: official pages of `<INSTITUTION>`, faculty pages, examination
  office, module handbook, exam portal, `<LMS>`, and official institutional emails.
- When login is required, use computer-use or browser control, but leave
  authentication to the user. Never store credentials, MFA codes, or session data.
- Use `<MAIL>` only when a suitable connector or explicitly provided mail content
  is available. Keep the search query narrow (sender from the institution, module
  codes, examination office, re-enrollment, deadline keywords).
- Mark source conflicts openly and prefer the more official or more recent source.

## Planning

Build plans with buffer time:

1. Mandatory dates and hard deadlines first.
2. Plan backwards from exam and submission dates.
3. Prioritise modules by effort, risk, prior knowledge, and proximity to exams.
4. Set realistic learning blocks per week, including revision and free buffer.
5. Justify plan changes: what is dropped, what moves forward, what risk arises.
6. Output the result in a compact table:
   `Date | Task | Source | Status | Next step`.

## Reminders and Calendar (optional)

Used only when the `<CALENDAR>` connector is available and explicitly requested:

- Create reminders with advance notice: hard deadline, 7 days before, 2 days before,
  and the day before (adjustable).
- Confirm calendar writes briefly before committing, unless the action is
  unambiguously authorised.
- Do not transfer any deadline until it is confirmed from an official source or
  local original document.

## Mail and Portal Check (optional)

For requests such as "check my institutional emails" or similar:

1. Search institutional emails for relevant new messages.
2. Check official deadline pages and module/exam pages.
3. Open `<LMS>` only when needed and with the user's login.
4. Output changes as a delta: new, changed, unchanged, unclear.
5. Name next actions: register, download, follow up, plan, remind.

## Privacy

- Do not output enrollment numbers, certificates, mail full texts, health data,
  or exam data unnecessarily.
- Ask before writing files if sensitive content would be transferred into new
  planning files.
- Abstracted references are sufficient in replies: "Re-enrollment deadline ends
  on …" — no complete mail or document quotations.

## Open Points

- The `author` field follows the `.SKILLS` convention (repository authorship);
  the value contains a personal name but is intended for public repository use.
- Tool integrations (`<MAIL>`, `<CALENDAR>`) are intentionally optional — the skill
  functions fully without them.
