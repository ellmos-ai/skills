---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, says "grill me" or types /grill-me, or uses any other 'grill' trigger phrase -- including German ones such as "grill mich", "grill mich zu diesem Plan" or "zerpflück meinen Plan im Grill-Modus". Also use when a planning session ends and the user asks whether anything is still open.
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: en
---

<img src="banner.png" width="100%" alt="grilling banner">

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.

## Local additions

These rules extend the upstream method; they do not change it.

1. **Seed the tree from what is already written.** Before the first round, read the plan and the place where the project records its decisions, and collect every item still marked as open, proposed or unconfirmed. Those are frontier candidates. Never re-ask a point that is already decided there; cite it instead.
2. **Write each answer down before the next round.** Record every answer where the project keeps its decisions, marked as decided, with date and source. An answer that exists only in the chat is lost after the next context reset.
3. **Pause, don't restart, on interruptions.** If the user asks for something else first ("transfer first, then grill"), do that, then resume with the remaining frontier. Settled questions stay settled.
4. **Back each recommendation with one reason.** Give the recommended answer and the single fact or rule it rests on. A recommendation is never a decision until the user confirms it.
5. **Show the facts you measured.** When a question rests on something you looked up, state the finding and where you found it, so the user decides on evidence rather than on your summary.
6. **Ask in the user's language.** Questions and recommendations follow the language the user writes in; identifiers stay as they are.
7. **Close with a ledger.** When the frontier is empty, list what was decided and what was deliberately left open, then ask for confirmation of the shared understanding.

<!--
Vendored from mattpocock/skills (skills/productivity/grilling/SKILL.md, MIT
License, Copyright (c) 2026 Matt Pocock -- see LICENSE next to this file).

Improved fork. Modifications vs. upstream:
- `description`: German trigger phrases ("grill mich"), the "grill me" and
  /grill-me triggers, and the end-of-planning trigger were added.
- `category`, `language` and this comment were added (local convention).
- "Local additions" (rules 1-7) were appended after the upstream body. The
  upstream body above that heading is unchanged, so a resync only needs to
  replace that part.

Adopted 2026-08-24 per Ticket T-20260824-594031458, together with the thin
entry point skills/third-party/grill-me/ (upstream
skills/productivity/grill-me, `disable-model-invocation: true`, body
"Call the Skill tool with grilling"). On 2026-10-25 grill-me was removed at
the user's request: one skill instead of two, the triggers moved into this
description. Rules 1-7 come from a planning session of the same day.
-->
