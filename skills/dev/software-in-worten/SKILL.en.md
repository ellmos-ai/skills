---
name: software-in-worten
version: 1.0.0
type: method
author: ellmos (from a design conversation with Lukas Geiger, 2026-08-02)
created: 2026-08-02
description: >
  Translates between a user interface and text — in both directions. From
  a described interface a skill emerges; from a skill an interface
  emerges. Use it when an application is being designed and the flow is
  still unclear, when an existing tool should be made available as a
  skill, when the interface and agent access drift apart, or when a skill
  gets too long and nobody knows why.
category: dev
tags: [design, ui, skills, methodik, uebersetzung, entwurf]
language: en
status: stable
visibility: public
standalone: true
---

<img src="banner.png" width="100%" alt="software-in-worten banner">

# Software in Words

## The thought

Humans design **visually**: *how do I want to operate this?* Agents read
**text**. As long as both are created separately, they drift apart — the
interface can do something the skill doesn't know about, and vice versa.

But both are the same thing, only in different states of matter. There is
a translation, and whoever knows it works in both directions:

> **Design an interface out of words. And turn an interface back into
> words.**

---

## The translation table

| In the interface | What it means | In text |
|---|---|---|
| **Cursor** | *I can select* — the space of what's possible | the set of options at this point |
| **Highlighting** | *this is what I want* | a selection, a value |
| **Click** | *I decide, I want to go there* | **the prompt** — the user's answer |
| **Field, switch, setting** | a decision that stays | **config** |
| **Settings of the whole software** | decisions that apply everywhere | **policies** |
| **Form, input mask** | a collection of related decisions | **template** |
| **Button that starts something** | *something is happening now* | a **skill** or **workflow** is triggered |
| **What happens afterward** | the sequence of steps | instructions in the skill — or a **script** |
| **Progress indicator** | *it's running, and how far along* | status messages in the flow |
| **Success message, result view** | *this is what came out* | the return value — in the interface only laid out more nicely |
| **Project** | a bounded body of work | a **folder** — and because it itself sits in a folder, part of the software |
| **View, tab, panel** | a state you're currently in | a step in the flow tree |

**The central row is the click.** A click is nothing other than what a
user would say in a conversation — just faster. **The click is the
prompt.** And a prompt is followed by a reaction: a new question, a new
view, a new state.

---

## The flow is a tree

Every application is a sequence of decisions, with something happening
between them:

```
Preconditions clarified?   →  references · candidate list · numbers · order
        ↓
User's consent             →  START
        ↓
Do they want to follow along?  →  yes: open a following-along view
Do they want interim updates?  →  yes: report on every event (through, rejected, status)
        ↓
        [ EXECUTION — often outsourced to other software ]
        ↓
The return comes back       →  evaluate it
        ↓
What do they want to know?  →  the result in their own terms:
                                "ordered from X, 40 minutes, 30 euros"
```

**Three parts, always the same:**

1. **Decisions** — if-then, until everything necessary is in place
2. **Execution** — often not even in your own tool, but outsourced
3. **Feedback** — the result handed back to the human, in their language

The third part is the one most underestimated during design.
**Communication runs through the senses** — as text, as image, as sound.
An interface designs this out; a skill describes *what* gets reported and
*when*.

---

## The middle layer: the blueprint

Between "described" and "built" there's a missing step. It's called the
**blueprint** and is **text whose layout corresponds to the image** — a
screen you can read:

```
 What are you craving?    [ Burger                        ]
 Where to deliver?        [ Dorfstraße 1, 16321 Bernau     ]
 Maximum amount           [ 35 ] €   ⓘ Final amount at the door
 Mode                     (•) Delivery  ( ) Table  ( ) Pickup

 Candidates (drag to reorder)                   ↻ search again
 ┌────────────────────────────────────────────────────┐
 │ ≡ 1  Burger House Dorfstadt      ★ Favorite   open │
 │ ≡ 2  Pizzeria Roma                             open │
 └────────────────────────────────────────────────────┘

 [ View dry run ]   [ Really call → 4 calls, ~€0.20 ]
```

**Why this step gives so much:**

A blueprint is **simultaneously readable and viewable**. The human sees
their picture again, the agent sees fields, types and order. It's created
in minutes, costs nothing, and can be corrected in conversation — unlike a
built interface.

**And the skill falls out of the blueprint almost by itself:**

> **What does the agent have to be able to do, know and perform — in what
> order — to fill out this blueprint?**

Every field becomes a question. The layout becomes the order. What's
pre-filled isn't asked about. What stands as a button becomes a step.
After that, you enrich it with whatever the agent additionally needs to
know — domain knowledge, boundaries, pitfalls.

**So three stages:** description → **blueprint** → skill *(and from there
just as easily into a built interface)*.

### An empty field is a question — and the question has a purpose

`[ 35 ] €` looks like a number. But it's actually a **data query addressed
to a human**, and it has a reason that usually stays unsaid:

> **We need this maximum amount because it's the condition under which the
> order happens at all.**

The field therefore carries three things at once: **what** belongs in it,
**why** it's needed, and **where it takes effect later**. In an interface
this lives in the layout and the help text. In text it has to be written
down — otherwise it gets lost.

**That's why a field legend belongs under every blueprint:**

| | |
|---|---|
| **Question** | how a human would be asked about it |
| **Type** | number, text, choice, list, ordered list, date … |
| **Purpose** | what the value is needed for later — *"abort criterion in the cascade"* |
| **Precondition** | what has to exist for the field to make sense at all |
| **Postcondition** | what holds once it's filled |
| **If empty** | silently accept · set a default · ask · block |
| **If wrong** | message, follow-up question, correction suggestion |

**The last two rows are the ones most likely to be forgotten** — and the
ones that cause the most trouble in operation. *"Price doesn't matter"* is
a valid answer and has to be provided for as such, not as an error.

### The field is open — the question narrows it down

An empty field is **everything and nothing**, like an empty context
window: an invitation to write anything into it. But what?

**The restriction doesn't come from the field, but from what surrounds
it** — usually from the connected text before it, above it or next to it:

> *"How much should this cost at most?"*

This question restricts **semantically and pragmatically**. The field
itself still allows anything — and if someone uses that freedom, **it
loses its purpose**. That's why field conditions step in: *numbers only*.
Not because "thirty-five" would be incomprehensible, but because it's
harder to process and takes longer to write.

**From this follows the working direction: the field rules are derived
from the question, not the other way around.** Whoever fixes the data
type first has already forgotten the question.

And the question usually also carries the **purpose** — that's why an info
icon often sits next to it for humans:

> *"We don't accept any offer above this price."*

That's not politeness, it's the field's actual meaning: **a user
preference that later acts as a hard gate.**

### The control boundary — and why everything has to be handed over

A field is followed by a chain:

```
Field "maximum amount"
   → the value is needed later          (purpose)
   → for a check                        (gate)
   → so the counter-value has to be raised (a new question, elsewhere)
   → none of us asks that question       (it sits inside the prompt)
```

**And here runs the decisive line: with the prompt, it leaves our control
layer.** After that there's no more access — no follow-up, no
intervention, no second chance.

That's why **everything** needed over there has to be handed over:

- **the value itself** — €35
- **the instruction to raise the counter-value** — ask for the price
- **what applies if it's higher** — decline, say thanks, end politely
- **what applies if none is given** — don't estimate, decline
- **what applies if the other party doesn't want to talk to a machine** —
  ask for a personal callback and return the number as a value

The last point shows the direction people think of least often when
designing: **the exception case also has to return a value**, otherwise
nothing reaches the human except "didn't work".

### The prompt is a generated skill

That makes clear what a prompt actually is:

> **A prompt is a skill that the interface has just assembled** — from the
> decisions, clicks and values of this one run. Personalized, tailored to
> the purpose, and forced to express everything intended **in language**.

A fixed, written skill says how it's done *always*. A prompt says how it
should run *this time*. Both are the same form — one stays, the other
arises in the moment and is gone afterward.

**In practice this means:** whoever treats prompt construction as
text-snippet tinkering builds bad prompts. Whoever treats it as *skill
generation* — with purpose, rules, boundaries, exceptions and return
values — builds good ones.

### Waiting isn't doing nothing, it's not knowing

After submitting, the human has given up control. What they need now
isn't patience, it's **information**: *what's happening right now? where
do we stand?*

The agent gets that anyway — it queries the progress. **The human sees
none of it, unless someone translates it.** That's exactly why progress
bars, running logs and status lines exist: they aren't decoration, they're
the translation of a data stream into something a waiting person can bear.

### The feedback is a prompt in reverse

The success message isn't a conclusion, it's a **handover back**:

> *"This is the result of your order."*

Only with this can the human evaluate and act further. And that's exactly
why it has to be complete: *"Ordered — but three pizzas instead of one.
Good thing the callback number is there, I'll call myself."*

**Without a usable return, nobody can keep processing.** A message that
only says "it worked" hasn't closed the loop.

### Question and field analysis

For **every** element of a blueprint — field, button, choice, display —
the same questions:

| | |
|---|---|
| **What's wanted, and for what?** | the intent behind the element |
| **What happens on submission?** | processed immediately, or only stored? |
| **Where and when is the value needed again?** | the place where it takes effect |
| **How long does it have to be held onto?** | beyond the click? beyond the run? |
| **What has to happen with it?** | check, hand over, display, discard |

The maximum amount, for example, is **not needed immediately**. It's
stored, carried along, and only takes effect later in the conversation —
so it needs a place to live, and a spot where it migrates into the prompt.

### Branches determine the questioning algorithm

A choice is rarely just a value. Often it's a **switch** that rearranges
the entire further flow:

| Mode | First question in the conversation | What drops out | What's added |
|---|---|---|---|
| **Delivery** | *"Do you deliver here?"* — a no ends the call immediately | — | delivery address |
| **Pickup** | drops out | the delivery question | pickup time |
| **Table** | *"Are you open, and is there a table free at X?"* | the whole price check | number of people, children, seating preference, time window |

**The order in the conversation follows exclusion power, not curiosity.**
Whoever doesn't deliver doesn't need to be asked about the food — the
hardest condition comes first, because it leads fastest to the next
candidate.

And: **much stays the same across the branches.** The maximum amount
applies for delivery just as for pickup, and so does the candidate list.
Only the questioning algorithm changes.

### The circle

```
Problem  →  use case  →  will             "I'm out in the country and hungry"
   ↓
what I want becomes conditions            5 people · 7pm · Italian · not the one place
   ↓
conditions need data                      → this gives rise to the FIELDS
   ↓
fields + decisions                        → this becomes the PROMPT (the generated skill)
   ↓
                [ execution beyond the control boundary ]
   ↓
receive and store the return              → only what was handed over before comes back
   ↓
translate into what can be seen and heard → a MESSAGE to the human
   ↓
they evaluate and decide again            → back to the top
```

**The use case justifies the data, the data justifies the fields.**
Whoever starts with the fields invents forms. Whoever starts with the
will gets them for free.

### Between two blueprints stands the causality

A blueprint is a **static layout**. Several of them in a row still don't
make a flow — something happens in between, and **that in-between is the
actual logic**: what happens when this is clicked? which check runs? what
gets stored? what gets triggered?

Three ways to make this time dimension visible:

1. **Labeling in the image** — arrows and short notes between the
   blueprints
2. **Before/after pairs** — the same excerpt in two states, "before the
   click" and "after the click"
3. **Writing it out** — pre- and postconditions as text under the image

The third way carries the furthest, because it's executable. The first
two help the human understand.

### The data model follows from the fields

Whoever describes an "add contact" field has already decided that there
are addressees, that they get stored, and which details belong to them.
**The data table follows the fields, not the other way around.**

That's why it pays off to make the field legend complete before any
schema is designed: every field with a type and a purpose is a column,
every repeatable group is a table, every relation between fields is a
reference.

## Direction 1: from words to an interface

**When the flow was described first.**

1. **Collect decisions.** Every point where something gets fixed. Sort
   them:
   - **Mandatory** — it can't proceed without it → a **required field**
   - **Derivable** — can come from context or existing data → a
     **pre-filled field** with a correction option
   - **Optional** — improves the result → a **collapsed section**
   - **Gate** — irreversible, costs money, reaches other people → a
     **confirmation step**
2. **Bundle what belongs together** → one mask, one template.
3. **Cut the tree into views.** One state = one view.
4. **Design the feedback.** What gets reported when? Progress, interim
   state, result.
5. **Fix what applies throughout, once** — color, typography, cut,
   motion. These are policies for the interface.

**The payoff:** a form that emerges from a conversation flow is almost
always leaner than one from the drawing board. While phrasing it, you
notice which question is superfluous.

## Direction 2: from an interface to words

**When the application already exists or is already described.**

1. **Phrase every click as a question.** What is this button actually
   asking the user?
2. **Every field as a config entry** — with a default value, a type and
   help text.
3. **Every view as a step** in the flow.
4. **Every message as a return value** — what gets reported, in what
   words?
5. **Check what the interface knows implicitly** — orderings, locks,
   dependencies, that are written nowhere but only sit in the layout.
   **That's the part that's most easily lost in translation.**

### Why this direction is harder — and how to walk it anyway

Direction 1 comes easy, direction 2 feels tough. There's a reason for
that:

> **A skill is time. A screen is space.**
> First this, then that — versus everything visible at once.

So you don't translate line by line, but **cut a flow into surfaces**. The
cutting edge is always the same:

**A screen arises where the flow waits for a human.**

Everything between two waiting points runs by itself — that becomes
**no** screen, at most a progress indicator. Whoever builds a view for
every step builds a click prison.

**And the if-then chains?** They don't all become visible. Four cases:

| Kind of condition | What it becomes |
|---|---|
| **A human sets it** ("at most €35") | a **field** — before the start |
| **The system checks it** ("price above limit") | a **result** — afterward, with a reason |
| **It changes what the human sees** ("no match") | a **state** of the same screen, not a new one |
| **It's pure mechanics** (retries, timeouts, format checks) | **nothing at all** — it stays invisible |

**The fourth case is the most common.** Most branches in a script never
belong on a screen. Whoever shows them anyway confuses a flowchart with an
interface.

**In practice, four steps:**

1. **Mark waiting points** — every place where a human decides, confirms
   or enters something. These are the screens, and there are usually
   surprisingly few of them.
2. **Collect backward** — what has to be known before this waiting point?
   These values are the screen's fields.
3. **Collect forward** — what happens afterward, and what of it does the
   human need to learn? That's the feedback.
4. **Leave the rest out** — everything that's neither input nor a message
   stays invisible.

---

## The gradient: skill ↔ script

```
far from the software                                     close to the software
   skill carries everything                              script carries everything
        │                                                       │
   verbose text                ────────────►         terse operating instructions
   every step explained                               "call this, then that"
   works without a tool                                only works with the tool
```

**The more a process is automated, the less a skill has to explain.** It
gets shorter and more concrete — at some point it's little more than an
operating guide for the scripts: *when do you reach for this tool, what
do you feed it, how do you recognize that it worked.*

Two converse conclusions that help in everyday work:

- **If a skill gets too long, a script is missing.** Length is a signal:
  whatever repeats and is mechanical belongs automated.
- **If a script becomes incomprehensible, a skill is missing.** A tool
  without text about it is only usable by whoever built it.

---

## The shared currency

**Every setting exists three times** — as a config value, as a question in
the skill, as a field in the interface. So they don't drift apart, the
representation is described **once** and read by all three:

```yaml
field: sample.method
label: "Sampling method"                          # interface
question: "How should the sample be drawn — random, stratified or census?"  # skill
type: choice
options: [random, stratified, census]
default: random
help: "Stratified only if the characteristics are present in the base data."
locked: false        # true = can't be turned off, doesn't appear in any interface
```

**Whatever is `locked` never shows up as an option anywhere.** Some things
aren't a setting, they're part of the scaffolding.

---

## When this skill helps

- An application is being designed and the flow is still unclear →
  **direction 1**
- An existing tool should be made usable for agents → **direction 2**
- The interface and agent access drift apart → introduce a **shared
  currency**
- A skill gets too long and nobody knows why → check the **gradient**
- A design conversation should be captured before it evaporates → table +
  tree

## Related

`condition` translates conditions, points in time and orderings into
checkable gates (`/if`, `/when`, `/after`, `/and`, `/or`) — the same move
for the special case of flow control. `skill-extractor` derives skills
from conversation transcripts. `plugin-system` makes your own scripts
discoverable.
