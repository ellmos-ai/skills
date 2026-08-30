---
name: decision-shot
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-24
updated: 2026-08-24
description: >
  Extremely short, substantial output FORMAT for ONE decision or group of
  decisions, when the analysis behind it already exists (produced in chat,
  from `decide`, from `decision-briefing`, from a ticket or a document):
  context in 2-3 lines, pro/con per option as bullet points in
  paveman/caveman-reduced style, talking points, a justified recommendation,
  and a path/link to the full analysis for complete follow-up reading. Use
  this skill for "give me that short with pro/con and a recommendation",
  "executive summary of the decision", "short context on <topic>",
  "summarize decision X in a short form", /decision-shot, or whenever a
  result should be handed to someone who only needs the essence, not the
  full derivation. Do NOT use it to COLLECT many open decisions and poll
  them by letter -- that's decision-briefing; do NOT use it to first ANALYZE
  a decision -- that's decide. decision-shot presupposes a finished analysis
  and only compresses its presentation.
visibility: public
language: en
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: utilities
tags: [entscheidung, executive-summary, kurzform, pro-contra, talking-points, empfehlung]
status: active

dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, knappform, paveman]

provenance:
  origin: "custom"
  decision_ref: "T-20260824-673115956 (Ticket-Master, User order 2026-08-24)"
---

# decision-shot

> The analysis is done. What's needed now is not a second derivation, but
> the essence plus the way back to the full version.

## When to use

- A decision (or a tightly related group, e.g. several sub-questions of the
  same topic) has already been thought through -- in chat, in a ticket, via
  the `decide` framework, or in `decision-briefing`'s phase 2 -- and now
  needs to be made accessible to someone (the user, another agent, a
  handoff document) within seconds.
- Trigger words: "short with pro/con", "executive summary", "short
  context", "talking points on that", "give me that compressed with a
  recommendation", `/decision-shot`.
- **Not** for several still-open, undecided points that the user should
  answer one after another/in a batch by letter -- that's
  [decision-briefing](../decision-briefing/SKILL.md). **Not** to work out a
  decision in the first place -- that's [decide](../decide/SKILL.md).
  decision-shot is pure PRESENTATION of an analysis that already exists.

## Boundary (short version)

| Skill | Does what | Done when |
|---|---|---|
| `decide` | Works out ONE decision with a framework (pro/con matrix, weighted scoring, decision tree, ...) | Analysis is still pending |
| `decision-briefing` | Collects MANY open decisions of one topic, presents them as an A/B/C/D batch, takes letter answers | Several points are still undecided |
| `decision-shot` | Compresses ONE finished analysis (regardless of source) into an executive short form with a link to the full version | Analysis already exists, only the presentation is missing |
| `knappform` | General response-style modifier for EVERY response of the session | Session-wide, topic-independent |
| `paveman` | Deterministically shortens existing PROSE FILES (rule/memory files) | Shortens a file, not chat output |

`decision-shot` doesn't compete with any of the four -- it's the FORMAT used
after `decide` or alongside `decision-briefing`, as soon as the essence
needs to be handed off. The reduced language style follows
`knappform`/`paveman` (see there for the full cut list), but here it's
applied consistently to a fixed five-part format.

## Format (binding, five parts)

```
## <Decision title>

**Context:** <2-3 lines -- what it's about, why now, what's at stake>

**<Option A>**
+ <strongest pro argument>
+ <second pro argument, only if it holds up>
- <strongest con argument>

**<Option B>**
+ <pro>
- <con>
- <con>

**Talking points:**
- <point that lands immediately in a conversation/email>
- <point that preempts a typical objection>

**Recommendation:** <option> -- <one sentence of justification, no repeat of the pro list>

**Full analysis:** <path or link -- ticket file, document, chat reference>
```

## Rules

- **Lines are a budget, not a target.** 2-3 lines of context, 2-4 bullet
  points per option, 2-3 talking points, 1 sentence of recommendation --
  anything more gets cut, not shortened-and-kept-anyway. If an option
  doesn't fit in 4 bullet points, it doesn't belong in this skill, it
  belongs in the full analysis.
- **Reduced style like `knappform`/`paveman`:** no filler words, no stock
  phrases, no evasiveness. Negations (`not`, `never`, `no`, `only`,
  `except`) stay untouched -- cutting them reverses the statement.
- **Pro/con are bullet points, not sentences.** `+`/`-` as a prefix, one
  thought per line, no trailing clause.
- **Talking points are communicative, not analytical.** They answer "what
  do I say when someone asks me" -- not "what does the analysis say".
  Duplicates of the pro/con list are a sign that it hasn't been compressed
  yet.
- **The recommendation justifies itself in one sentence.** No repeat of the
  pro list, no "see above" -- the one sentence has to carry on its own,
  even without the rest of the block.
- **The link/path to the full analysis is mandatory, not optional.**
  decision-shot doesn't replace the analysis, it makes it quickly
  findable. If no tangible source exists (only produced verbally in chat,
  no document), name the chat/session reference as concretely as possible
  (e.g. "this session, answer to Q4") instead of leaving the field empty.
- **Several related decisions** (a group, e.g. several sub-questions of one
  topic): one block per decision, separated by `---`, shared context only
  once at the start if it really applies to all of them.

## Example

```
## Where does the nightly backup job run?

**Context:** Currently on the laptop, which often sleeps and then misses
the job. Mac Studio runs 24/7 and has free capacity.

**Laptop (status quo)**
+ No network dependency
- Job regularly fails when the device sleeps
- No central log overview

**Mac Studio**
+ Runs 24/7, no failures from sleep mode
+ Central logs in one place
- Needs a working Tailscale/SSH as a prerequisite

**Talking points:**
- "The failure isn't a bug in the script, it's a location question."
- "Tailscale already runs stably for other jobs -- no new risk."

**Recommendation:** Mac Studio -- the only option without the known
sleep-mode failure, and the dependency (Tailscale) is already proven in
production.

**Full analysis:** `.SYNC/MAC_STUDIO_COMPUTE_HANDOFF.md`, section "Backup jobs"
```
