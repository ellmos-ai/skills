---
name: decision-briefing
version: 1.0.1
type: skill
author: Lukas Geiger
created: 2026-06-13
updated: 2026-06-13
description: >
  Use whenever several decisions are pending or have accumulated -- whether within
  a topic, project, document, or over the course of a session: inventory them,
  present a numbered briefing with options A/B/C/D and a marked recommendation,
  accept letter answers (including batches), record the results, and write them
  back into the source documents.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: utilities
tags: [entscheidung, briefing, batch, decision-session, priorisierung, workflow]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/agents/_experts/decision-briefing/"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-06-13"
  last_sync_to_origin: null
  local_changes_since_sync: true
  # Note: The scanner component of the BACH original (scanner.py, sources.json,
  # system-wide marker scans) was deliberately removed for the standalone version.
  # Capture is lightweight, based on what is already at hand.
---

# Decision-Briefing — Work Through Many Decisions on One Topic

> A pile of open decisions becomes a numbered briefing with recommendations that the user can answer at lightning speed with single letters — one by one or as a batch.

---

## When to use?

**Always, as soon as several decisions are pending** -- regardless of topic. Typical situations:

- Many open decisions have piled up in one area/topic
- A document (plan, TODO list, concept) contains several undecided points
- Several decision questions have accumulated during a conversation
- The agent itself has several questions for the user -- bundle them as a briefing instead of asking one by one
- The user wants to clear open items quickly and on a solid basis

**Trigger words:** open decisions, decision session, briefing, work through, go through, let's decide all of this

**Scope:** [decide](../decide/SKILL.en.md) provides frameworks for ONE question. `decision-briefing` coordinates working through MANY decisions on one topic — and applies `decide` to complex individual cases.

---

## Core UX

The heart of this skill is the briefing format. Each decision is presented so that answering costs only a single letter:

- **Numbering:** `[E01]`, `[E02]`, … — stable references throughout the session
- **Short question** + 1–2 sentences of context
- **Options as letters** A/B/C/D (2–4 options, more only if necessary)
- **Marked recommendation** with a one-sentence rationale (e.g. `→ Recommendation: A — because …`)
- Optional: consequence note (what follows from the choice)

**User answer formats:**

```
Single:    "E01: A"  or  "1A"
Batch:     "1A 2C 3B"  or  "E01: A, E02: C, E03: B"
Deepen:    "E02: more info"  or  "2?"
Defer:     "E03: later"
```

---

## Workflow (4 Phases)

```
Topic + decisions at hand
     |
     v
Phase 1: CAPTURE & INVENTORY
     |
     v
Phase 2: PREPARE THE BRIEFING
     |
     v
Phase 3: DECISION SESSION
     |
     v
Phase 4: RECORD & WRITE BACK
```

### Phase 1: Capture & Inventory

Sources: what the user names, a document at hand, or the conversation context. No system-wide scan — only what is already there.

1. List all open decisions (one line each: short title)
2. Detect and merge **duplicates** (same question, phrased multiple times)
3. Mark **dependencies** ("E04 depends on E01")
4. Set the **order**: blockers first (decisions that others depend on), then by urgency
5. Show the list to the user for confirmation ("Did I get them all? Anything missing?")

### Phase 2: Prepare the Briefing

Per decision:

```
[E01] <Short question>
  Context: <1-2 sentences: Why is this up? What depends on it?>
  A) <Option>
  B) <Option>
  C) <Option>
  → Recommendation: <letter> — <one-sentence rationale>
  (optional) Consequence: <what follows from the choice / next action>
```

Rules for good options:

- Options must be mutually exclusive and cover the spectrum
- If useful, include a "keep status quo" or "defer" option
- The recommendation is transparently reasoned — never covertly suggestive
- When facts are unclear: clarify first (or flag as an open question), do not guess

### Phase 3: Decision Session

1. Present the briefing — one decision per message or all at once as a batch; with >5 decisions, use blocks of 3–5
2. Accept letter answers and acknowledge them
3. On a "more info" answer: deepen the decision (method toolbox below)
4. For complex individual cases (many criteria, high stakes): escalate to the [decide](../decide/SKILL.en.md) skill (weighted scoring, scenario analysis)
5. Carry deferred decisions forward explicitly as open — never drop them silently

### Phase 4: Record & Write Back

1. Create a **results table**:

```
| No.  | Decision            | Chosen | Status   |
|------|---------------------|--------|----------|
| E01  | <short title>       | A      | decided  |
| E02  | <short title>       | C      | decided  |
| E03  | <short title>       | —      | deferred |
```

2. Write decided items back into the **source documents/TODO files** — at the location of the open question, e.g.:

```
DECISION: <question>
  → DECIDED 2026-06-13: Option A (<short form>)
  → Next action: <if the decision implies a follow-up action>
```

3. Keep **deferred items explicitly open** (in the source document or the TODO list) so they reappear in the next briefing

---

## Example Briefing (fictional)

Topic: relaunch of a club website — 3 open decisions from the project plan.

```
[E01] Which system for the new website?
  Context: Current site is hand-maintained HTML; 2 people will maintain content in the future.
  A) Static site generator (fast, secure, maintained via Git)
  B) Classic CMS with admin interface
  C) Hosted website builder
  → Recommendation: B — two non-technical editors need an interface, not Git.

[E02] How is it hosted?
  Context: Budget ~10 EUR/month, no dedicated admin in the club.
  A) Shared hosting with the current provider
  B) Small dedicated VPS
  C) Managed hosting matching the chosen system
  → Recommendation: C — least maintenance effort without an admin; consequence: depends on E01.

[E03] When does the new site go live?
  Context: Content is 60% migrated; club anniversary in 3 months.
  A) Immediately as a soft launch (rest follows)
  B) After complete content migration
  C) On the anniversary as the deadline
  → Recommendation: A — reversible and yields early feedback; final content follows.
```

The user answers as a batch: **"1B 2C 3A"** → results table, then the three decisions are marked DECIDED in the project plan.

---

## Method Toolbox (for "more info" and deepening)

| Method | When | Summary |
|--------|------|---------|
| **Pro/con matrix** | 2–3 options, quick comparison | Evaluate all options side by side |
| **Weighted scoring** | Multiple criteria | Weighted criteria, points per option (quantitative where possible) |
| **Second-order thinking** | Unclear stakes | What are the consequences of the consequences? |
| **Premortem** | Risky decision | "It failed — why?" Find weak spots in advance |
| **10/10/10 method** | Emotional/temporal distortion | How does the decision look in 10 minutes / 10 months / 10 years? |

---

## Working Principles

- **Never push decisions:** provide information, justify the recommendation transparently — the user decides
- **Bias detection:** name thinking errors when they become visible (confirmation bias, sunk cost)
- **Mind reversibility:** decide reversible choices quickly, treat final ones more thoroughly
- **Respect time pressure:** fast decisions need simpler methods — not every question deserves a weighted scoring analysis

---

## Scope and Synergies

| Function | `decide` | `decision-briefing` |
|---|---|---|
| Structure a single decision with a framework | ✓ | — |
| Inventory many decisions on one topic | — | ✓ |
| Numbered briefing with A/B/C options | — | ✓ |
| Batch answers ("1A 2C 3B") | — | ✓ |
| Write back into source documents | — | ✓ |

**Synergy:** For complex individual cases within a session, `decision-briefing` applies the frameworks from `decide` (weighted scoring, scenario analysis). For the larger thinking process before that (analyze → ideate → decide), see [structured-thinking](../structured-thinking/SKILL.en.md).

---

## Changelog

### 1.0.0 (2026-06-13)
- Ported from the BACH expert `decision-briefing` v1.0.0; scanner component (scanner.py, sources.json, marker scans) deliberately removed — capture is lightweight, based on the context at hand

---

*Ported from BACH | Standalone version without scanner*

**See also:** [decide](../decide/SKILL.en.md) (frameworks for a single decision) | [structured-thinking](../structured-thinking/SKILL.en.md) (analyze → ideate → decide as a meta workflow)
