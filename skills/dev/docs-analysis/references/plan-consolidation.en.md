# Plan consolidation / document synopsis

Combine planning, status and handoff documents into one current plan of open items.
Archive evidenced completions and fully superseded sources while preserving valid
decisions, constraints and dependencies.

## Entry and collaboration

Load `folder-organization/SKILL.md` and its `references/cut-and-clue.md` through skill
discovery or the installed sibling directory. In the categorized library it lives at
`skills/utilities/folder-organization`. That skill handles archive transactions,
original preservation, clues, references and readback. `docs-analysis` handles content,
status and the consolidated plan. If unavailable, draft the synopsis but leave archiving
pending until the dependency is available; do not invent a second archive implementation.

Limit sources to the named folder and explicitly included tickets/registers. Follow local
control files, archive conventions and locks. Control files, active runtime files, secrets
and other workers' areas are not blanket archive candidates. Analysis-only requests produce
a draft and archive proposal. An explicit consolidation-and-archiving request authorizes
the necessary reversible changes within scope; do not request authorization already given.
Update extra registers only when requested or required by local workflow.

## Resolve sources and status

Read every relevant source completely, including attachments and referenced continuations
needed to assess status. Report unreadable or incomplete sources as gaps; do not archive
them. Filenames and modification dates alone do not establish validity or completion.

Track each distinct item's source/section, status, evidence and destination:

| Status | Treatment |
|---|---|
| open / partially complete | Remaining work and acceptance criterion in the current plan |
| complete | Completion archive only with verifiable evidence |
| superseded / abandoned | Record the decision and successor; do not count as complete |
| uncertain / conflicting | Keep a clarification item and both sources in the current plan |

A checkbox or unsupported completion claim is initially a reported status. Verify evidence
appropriate to the task, such as an artifact, test, release or ticket acceptance. Do not
replace missing evidence with assumptions. Separate achieved progress from remaining work.
Merge duplicate items while keeping every source anchor. A newer statement only replaces an
older one when substantive supersession is established.

## Write the current plan

Prefer the existing canonical filename and structure; otherwise use a name such as
`CURRENT-PLAN.md`. State the review date, source scope and direct predecessors with archive
paths at the top. Preserve a versioned copy before replacing an existing plan.

Include the goal, still-valid decisions and all open, partial and uncertain items. For each,
record a stable ID, concrete remaining work, priority, dependencies/blockers, acceptance
criterion and sources. Only carry forward evidenced owners and deadlines. Link archived
completion history rather than repeating it. Active prerequisites must not disappear with
completed tasks.

For requested ticket/register updates, follow their native workflow. Read IDs, status,
dependencies and current content before writing. Amend existing entries with plan/evidence
links without overwriting others' notes. Consolidated documentation does not mean the project
or ticket is complete; remaining work stays open. For entries outside scope, propose changes
instead of applying them.

## Archive and verify

Show a concrete source-to-destination plan before changes. Assign each source a justified
action: keep, archive as fully superseded, separate mixed content with Cut-and-Clue, or retain
for clarification. **No 75-percent rule:** A document with open work can be archived only
after that work is fully represented in the current plan. A request to archive all other
documents does not override missing content.

Use `folder-organization` to preserve byte-identical originals, hashes, provenance and restore
paths. Clues/sidecars point to the current plan without modifying evidentiary originals.
Place the manifest and any completion history under the local archive structure. Preserve
links, attachments and historical evidence. Re-read sources that changed after analysis
before replacing or moving them.

Acceptance: Every source item maps to the active plan, completion archive or a justified
supersession in the manifest; no open item exists only in the archive. Independently read
back the plan, archive and updated tickets; verify links and original hashes. On repeat runs,
reuse IDs and mappings without duplicate items or new archives of unchanged sources.

Report plan/archive paths, source coverage, updated ticket IDs and unresolved/locked sources.
Explicitly leave failed register updates pending rather than claiming full completion.
