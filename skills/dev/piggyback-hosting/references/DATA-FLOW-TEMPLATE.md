# Data-flow plan — template

> **A template, and a method.** Copy it into the application's repository as
> `DATA-FLOW.md`, replace every `[REPLACE: ...]`, and delete what does not
> apply. The value is not the table — it is the rule that fills it.

## The rule: only what is in the code

**Every row carries a file and a line number.** A row without evidence is a
belief, and beliefs are what data-flow documents are usually made of. If a fact
cannot be pointed at in the source, it belongs in one of the two honest
categories instead:

- **a deployment fact** — proxy logs, backups, infrastructure. The repository
  cannot know these; the operator must add them.
- **a provider fact** — retention at the API you call, its legal entity, its
  subprocessors. These come from contracts, not from an endpoint name.

Write "not found" where you looked and found nothing. It is a finding, not a
gap in the document.

## Header

```markdown
# [REPLACE: application] data flow

Status: code review on [REPLACE: date]. [REPLACE: state whether a live run happened.]
This document describes the current implementation, not a planned deployment.

"Leaves the computer" means leaving the machine that runs the [REPLACE: runtime]
process. Requests the *browser* makes are marked separately — those leave the
user's device directly, regardless of where the application is hosted.
```

## Operating modes

Before the table, name the modes the application actually has, and be precise
about what each one does **not** do:

- `[REPLACE: test/fixture mode — and what still leaves despite it. A fixture
  mode that still fetches map tiles is not offline.]`
- `[REPLACE: the ordinary mode]`
- `[REPLACE: the mode that costs money or touches third parties, and what gates it]`

## The switchboard

| Data | Collection and use | Storage | Retention implemented in code | Who can see it | Leaves the computer? | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `[REPLACE: what the user types]` | `[REPLACE: what it is used for]` | `[REPLACE: table, file, memory, cookie]` | `[REPLACE: the code that deletes it — or "no automatic expiry found"]` | `[REPLACE: who can reach it; name the routes without an access check]` | `[REPLACE: yes/no and to whom]` | `[REPLACE: file:line]` |
| `[REPLACE: what a third party supplies]` | | | | | | |
| `[REPLACE: what is sent to a provider]` | | | | | | |
| `[REPLACE: credentials]` | | `[REPLACE: environment, file, browser]` | | `[REPLACE: never the interface]` | | |
| `[REPLACE: preferences — language, theme]` | | `[REPLACE: cookie, local storage]` | | | | |

Rows that are easy to forget and usually matter most: **logs**, **backups**,
**caches**, **anything a background job holds**, and **anything the browser
requests from a third party** (fonts, tiles, scripts).

## If the application uses the piggyback modes

> **On the name.** In English this pattern is called *piggyback*: the application
> rides on infrastructure it does not own. The literal mode values are still
> spelled `huckepack-gift` and `huckepack-only-host`, after the German working
> title the code was built under. Prose says piggyback; configuration says
> huckepack.

Add a second table for what changes, and keep the first one — the change is
*where records live*, and readers need both pictures. Rows worth having:

| Data | The point to make |
| --- | --- |
| the database | not on the host; browser copy is the durable one; host memory only, with the actual TTL |
| session token | how a browser addresses its own copy |
| the visitor's key | browser storage, masked display, per-request use, and the test that proves it is not stored |
| background work | if anything outlives a request, say how the session and key travel with it |
| export file | **it is the unmasked database**; say so plainly |
| receipt file | what it contains, where it lands, that numbers are masked |

## Boundaries

Close with the sentences a reader could otherwise take away wrongly. The
recurring ones:

- **Masking a display is not deletion.** If the raw value is in a column, say
  which column.
- **An opaque ID is not authorization.** If any visitor with a link can reach a
  record, that is the finding.
- **Storing nothing is not transmitting nothing.** Where a third party is
  contacted, that transfer is unchanged by any storage decision.
- **`[REPLACE: what this application specifically invites people to misread]`**
