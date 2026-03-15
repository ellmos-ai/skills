---
name: project-onboarding
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Standard procedure for onboarding new software projects: Feature analysis,
  code quality review, onboarding checklist, and task creation.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: dev
tags: [onboarding, project, intake, analysis, checklist, code-review]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/workflows/projekt-aufnahme.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Standard Onboarding Procedure for New Software Projects

**Version:** 1.0
**Date:** 2026-03-12

---

## Overview

This procedure defines which steps to perform on newly discovered software folders before they are added to a task management system.

```
+─────────────────────────────────────────────────────+
|           STANDARD ONBOARDING PROCEDURE              |
+─────────────────────────────────────────────────────+
|  1. Create feature analysis                          |
|  2. Code quality review (standard tests)             |
|  3. Create TASKS.txt                                 |
|  4. Add to task management                           |
+─────────────────────────────────────────────────────+
```

---

## Phase 1: Feature Analysis

**Purpose:** Understand the tool, its functions, and development status.

**Create file:** `Feature_Analysis_<ToolName>.md`

### Template

```markdown
# Feature Analysis: <ToolName>

## Brief Description
A short sentence describing what the tool does.

---

## Highlights

| Feature | Description |
|---------|-------------|
| **Feature 1** | Description |
| **Feature 2** | Description |

---

## Development Stage Assessment

### Current Status: **<Status> (<X>%)**

Possible statuses:
- Prototype (0-30%)
- Alpha (30-60%)
- Beta (60-85%)
- Production Ready (85-95%)
- Release (95-100%)

| Category | Rating (1-5) | Details |
|----------|:------------:|---------|
| **Functionality** | 3 | |
| **UI/UX** | 3 | |
| **Stability** | 3 | |
| **Documentation** | 3 | |

---

## Recommended Extensions

### Priority: High
1. ...

### Priority: Medium
2. ...

### Priority: Low
3. ...

---

## Technical Details

Framework:      <Framework>
File size:      <X> lines of Python
Main file:      <main.py>

---
*Analysis created: <Date>*
```

---

## Phase 2: Code Quality Review

**Purpose:** Ensure technical quality, identify known issues.

### Recommended Checks

| Test | Tool | Description |
|------|------|-------------|
| **Encoding** | Encoding checker (e.g., `chardet`, `file`) | Ensure UTF-8 |
| **Method Analysis** | Linter (e.g., `pylint`, `flake8`) | Find large methods |
| **Indentation** | Formatter (e.g., `black`, `autopep8`) | Check consistency |
| **Imports** | Import checker (e.g., `isort`, `pylint`) | Find unused imports |

### Check Points

- [ ] All .py files UTF-8 encoded?
- [ ] No unusually large methods (>100 lines)?
- [ ] Consistent indentation (spaces vs tabs)?
- [ ] Unused imports removed?
- [ ] Docstrings present?

### Document Results

Record issues in TASKS.txt under "QUALITY REVIEW".

---

## Phase 3: Create TASKS.txt

**Purpose:** Capture open tasks in a structured format.

**Create file:** `TASKS.txt` in the project folder

### Template

```
TASKS - <ToolName> V<Version>
==============================
Status: <Status>
Date: <Date>

OPEN TASKS:
[ ] <Task 1> - Effort: <LOW|MEDIUM|HIGH>
[ ] <Task 2> - Effort: <LOW|MEDIUM|HIGH>

---
DONE (Archive):
- <Completed task> (<Version>, <Date>)
```

### Status Values

| Status | Meaning |
|--------|---------|
| NEWLY DISCOVERED | Not yet analyzed |
| ANALYSIS NEEDED | Feature analysis in progress |
| QUALITY REVIEW | Code tests running |
| VALIDATED & READY | Ready for features |
| MVP | Minimum Viable Product |
| BUILD ONLY | Only compilation needed |
| BLOCKED | Waiting for user test/decision |

---

## Phase 4: Task Management Integration

After completing phases 1-3:

1. **Transfer tasks:** Create TASKS.txt entries as tasks/issues
2. **Verify:** All tasks correctly categorized?
3. **Categorize:** Assign project to appropriate category (single tool, suite, library, etc.)

### Automatic Onboarding Tasks

For new projects, create the following standard tasks:

| Task | Description | Effort |
|------|-------------|--------|
| onb_1 | Create feature analysis | medium |
| onb_2 | Code quality review | low |
| onb_3 | Create TASKS.txt | low |

Tasks have dependencies: onb_2 depends on onb_1, onb_3 depends on onb_2.

---

## Quick Checklist

```
[ ] 1. Feature_Analysis_<Name>.md created
[ ] 2. Code quality review completed (linter, encoding, imports)
[ ] 3. TASKS.txt created with status
[ ] 4. Tasks added to task management
```

---

## Example: New Tool "MyTool"

```bash
# 1. Feature analysis
# -> Create Feature_Analysis_MyTool.md (see template)

# 2. Code quality
pylint MyTool/main.py
flake8 MyTool/main.py
file -i MyTool/main.py  # Check encoding

# 3. TASKS.txt
# -> Create in tool folder with status "QUALITY REVIEW"

# 4. Create tasks
# -> Capture TASKS.txt entries as issues/tickets
```

---

*Created: 2026-01-10 | Ported: 2026-03-12*
