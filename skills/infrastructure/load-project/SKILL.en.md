---
language: en
---

> **English** — Official English version of `load-project`.

# Load Project (English)

## Overview & Purpose

Use this skill at the beginning of a specific project task or when the working context has become unclear. The goal is not a full repository audit, but the smallest viable context needed to proceed safely with work.

## Configuration

The skill does not require fixed directory names. Local installations can optionally define the following values in their general agent rules or in a project-local configuration:

- known workspace roots,
- preferred file tools,
- names of additional boot or registry files,
- lock checkers,
- project-specific roles and priorities.

If no such configuration exists, the skill operates exclusively with the specified target and the project rules found there.

## Workflow

### 1. Resolve Target

1. Take an explicit path, project name, or current working directory as the starting point.
2. Determine the actual project or repository root.
3. Narrow down ambiguous matches based on the task, root documents, and repository boundaries; do not guess when targets are materially different.

### 2. Load Rule Hierarchy

Read from general to specific context:

1. global agent and security rules,
2. workspace or pipeline rules,
3. project and repository rules,
4. task-specific instructions.

More specific rules apply within their scope; higher-level security and authorization boundaries remain in force.

### 3. Read Root Documents by Role

Filenames are hints, not a fixed standard. Target documents with these roles specifically:

| Role | Typical Content |
|---|---|
| Entry | Purpose, navigation, startup instructions |
| Rules | Working methods, language, security, conventions |
| Architecture | Components, data flow, boundaries |
| Status | Current state, open issues, last verification |
| Tasks | Prioritized upcoming work |
| Registry | Canonical projects, checks, or publications |
| Evidence | Tests, audit logs, proof notes |
| Handover | Work in progress, third-party changes, next step |

Load only the roles relevant to the specific task.

### 4. Follow Binding References

If a read rule explicitly designates additional files as required reading, load them specifically. Terminate reference chains as soon as they no longer provide additional binding context for the task.

### 5. Check State and Locks

- Check locks against the local policy for owner, scope, timestamp, and validity criteria; without a defined stale rule, never unilaterally declare a lock stale,
- Version control status and third-party changes,
- Running processes or checkpoints, if relevant,
- Currency of registries, tests, and status reports.

Save the initial state of the affected areas before making changes as a status/diff baseline. If existing changes cannot be confidently attributed, treat them as third-party modifications as a precaution and leave them untouched.

Treat snapshots as temporary state and recheck them before taking risky actions.

### 6. Create Situation Report

Document briefly before implementation:

```text
Ziel:
Projekt-Root:
Geltende Regeln:
Evidenzquellen:
Snapshot-Zeitpunkt:
Relevanter Ist-Zustand:
Locks oder fremde Änderungen:
Erfolgskriterium:
Nächster sicherer Schritt:
```

Name sources only as precisely as necessary for verifiability. Redact secrets, personal data, and confidential content; do not copy them into the situation report.

If the task is clear and authorized as a result, proceed directly with execution.

## Limitations

- No broad, unrestricted file searches by default.
- Do not invent missing rules or registries.
- Do not treat old status reports as current evidence.
- Do not overwrite third-party changes.
- Do not perform project onboarding when only loading context for a specific task.

## Changelog

### 1.1.0 (2026-07-28)
- Removed fixed user, workspace, tool, and provider bindings.
- Introduced role-based document discovery and optional local configuration.
- Operationalized lock validity, dirty-tree provenance, snapshot evidence, and redacted situation reports.

### 1.0.0 (2026-06-17)
- Initial local version.