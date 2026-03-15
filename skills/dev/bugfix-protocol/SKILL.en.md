---
name: bugfix-protocol
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Systematic 6-phase debugging protocol. Structured approach to bugs
  with quick checks, isolated testing, 20-minute rule, and bug report
  template.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: dev
tags: [debugging, bugfix, protocol, python, pyqt6, systematic]
language: en
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/workflows/bugfix-protokoll.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Bugfix Protocol: Systematic 6-Phase Debugging

A structured approach to bugs — from symptom analysis to verification.
Prevents aimless trial-and-error and ensures fixes are sustainable.

---

## Overview

| Phase | Name | Goal | Max. Time |
|-------|------|------|-----------|
| 1 | Quick Checks | Rule out obvious causes | 2 min |
| 2 | Diagnosis | Locate root cause | 10 min |
| 3 | Isolated Test | Make bug reproducible | 5 min |
| 4 | Fix | Minimal correction | 10 min |
| 5 | Verification | Verify fix + check side effects | 5 min |
| 6 | Documentation | Preserve knowledge | 2 min |

**20-Minute Rule:** If no progress after 20 minutes, change approach or seek help.

---

## Phase 1: Quick Checks (2 min)

Before diving deep — check the most common causes:

### Checklist

- [ ] **Syntax error?** Read error message carefully, check line
- [ ] **Import error?** Module installed? Correct name? Circular import?
- [ ] **Typo?** Variable/function names correct?
- [ ] **Wrong data type?** String instead of int? None where object expected?
- [ ] **Stale cache?** Delete `__pycache__`, restart
- [ ] **Wrong environment?** Correct venv active? Correct Python version?
- [ ] **Encoding?** UTF-8 vs. cp1252 (Windows classic)

### Quick Actions

```bash
# Clear cache
find . -name "__pycache__" -type d -exec rm -rf {} + 2>&1
find . -name "*.pyc" -delete 2>&1

# Check imports
python -c "import modulename"

# Check syntax
python -m py_compile file.py
```

---

## Phase 2: Diagnosis (10 min)

### Strategy: Outside-In

1. **Analyze error message** — Read traceback from bottom to top
2. **Check recent changes** — `git diff`, `git log --oneline -10`
3. **Use diagnostic tools** — Use project-specific diagnostic tools

### Diagnostic Tools (Examples)

Depending on the project, specialized diagnostic scripts may be helpful:

| Tool | Purpose |
|------|---------|
| `import_diagnose.py` | Analyze import problems |
| `method_analyzer.py` | Check method signatures |
| `env_checker.py` | Validate environment variables/paths |

> **Note:** Create project-specific diagnostic tools or use existing ones.
> The systematic approach matters, not the specific tool.

### Debugging Techniques

```python
# 1. Print debugging (quick but effective)
print(f"DEBUG: variable={variable!r}, type={type(variable)}")

# 2. Breakpoint (interactive)
breakpoint()  # Python 3.7+

# 3. Extended traceback
import traceback
traceback.print_exc()

# 4. Logging instead of print
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"State: {state!r}")
```

---

## Phase 3: Isolated Test (5 min)

### Minimal Reproducible Example (MRE)

Goal: Reproduce the bug with minimal code.

```python
# test_bug.py — Minimal Reproduction Test
"""
Bug: [Short description]
Expected: [What should happen]
Actual: [What happens instead]
"""

# Minimal setup
# ... only the essentials

# Bug trigger
# ... exact code that triggers the bug

# Expected result
# assert result == expected, f"Got {result}"
```

### Isolation Strategies

1. **New file:** Reproduce the bug in a separate file
2. **Remove dependencies:** One by one, until the bug disappears
3. **Binary search:** Halve the code block, check which half contains the bug
4. **Git bisect:** `git bisect start`, `git bisect bad`, `git bisect good <commit>`

---

## Phase 4: Fix (10 min)

### Principles

1. **Minimal:** Change as little as possible
2. **Understand:** Never fix blindly — understand WHY it's broken
3. **One thing:** One fix per commit, don't fix multiple issues at once
4. **Backward-compatible:** Don't break existing functionality

### Fix Patterns

```python
# BAD: Treating the symptom
try:
    result = broken_function()
except:  # Swallow everything
    result = default_value

# GOOD: Fix the root cause
def broken_function():
    if input_data is None:  # Actual cause: missing None check
        return default_value
    return process(input_data)
```

### Common Fix Categories

| Category | Typical Fix |
|----------|------------|
| None/Null | Guard clause: `if x is None: return default` |
| Index error | Bounds check: `if i < len(lst)` |
| Type error | Explicit conversion: `str(x)`, `int(x)` |
| Import error | Fix path, install package |
| Encoding | Specify UTF-8 explicitly: `encoding='utf-8'` |
| Race condition | Lock/Mutex, or change order |
| State bug | Check initialization, add reset |

---

## Phase 5: Verification (5 min)

### Checklist

- [ ] **Bug is fixed:** Original problem no longer occurs
- [ ] **MRE passes:** Isolated test runs through
- [ ] **No regression:** Existing tests still pass
- [ ] **Edge cases:** Empty input, None, large data tested
- [ ] **Project tools:** Check project tools directory for relevant test/validation tools

### Test Commands

```bash
# Unit tests
python -m pytest tests/ -v

# Only affected tests
python -m pytest tests/test_module.py -v -k "test_name"

# Type check
python -m mypy file.py

# Lint
python -m flake8 file.py
```

---

## Phase 6: Documentation (2 min)

### Bug Report Template

```markdown
## Bug Report: [Short Title]

**Date:** YYYY-MM-DD
**Severity:** critical / high / medium / low
**Component:** [Module/File]

### Symptom
[What the user sees / error message]

### Root Cause
[Technical root cause]

### Fix
[What was changed + why]

### Affected Files
- `file1.py` — [Change]
- `file2.py` — [Change]

### Prevention
[How can this type of bug be prevented in the future?]
```

### Commit Message Format

```
fix: [Short description of the fix]

Cause: [Root cause in one sentence]
Fix: [What was changed]
Test: [How verified]
```

---

## PyQt6 / GUI Debugging — Common Pitfalls

> This section is relevant for desktop GUI projects with PyQt6/PySide6.

### Top 5 PyQt6 Traps

| Trap | Problem | Solution |
|------|---------|---------|
| **Signal-Slot Disconnect** | Signal connected but handler doesn't run | `print` in handler, check signature |
| **Thread Safety** | GUI update from worker thread | `QMetaObject.invokeMethod` or use signal |
| **Layout Cascade** | Widget invisible/misplaced | `widget.show()`, check layout hierarchy |
| **Event Loop Block** | GUI freezes | Move long operations to QThread |
| **Garbage Collection** | Widget suddenly disappears | Keep reference as `self.widget` |

### PyQt6 Debug Helpers

```python
# Dump widget hierarchy
def dump_widget_tree(widget, indent=0):
    print(" " * indent + f"{widget.__class__.__name__}: {widget.objectName()}")
    for child in widget.findChildren(QWidget):
        if child.parent() == widget:
            dump_widget_tree(child, indent + 2)

# Signal debugging
from PyQt6.QtCore import QObject
original_connect = QObject.connect
def debug_connect(self, *args, **kwargs):
    print(f"CONNECT: {self.__class__.__name__} -> {args}")
    return original_connect(self, *args, **kwargs)
```

---

## Quick Reference

```
BUG FOUND?
     |
     v
[Phase 1: Quick Checks]  ──── Obvious? -> FIX
     |
     v
[Phase 2: Diagnosis]  ────────── Cause clear? -> Phase 4
     |
     v
[Phase 3: Isolated Test]  ── Reproducible? -> Phase 4
     |                              |
     |                         Not reproducible?
     |                              |
     |                         Add logging,
     |                         wait for recurrence
     v
[Phase 4: Fix]  ─────────────── Minimal + understood
     |
     v
[Phase 5: Verification]  ────── Tests green? -> Phase 6
     |                              |
     |                         Tests red? -> Back to Phase 4
     v
[Phase 6: Documentation]  ───── Bug report + commit
```

### 20-Minute Rule

If you're stuck after 20 minutes:

1. **Change approach** — Try a different debugging technique
2. **Rubber duck** — Explain the problem out loud (or write it down)
3. **Take a break** — Step away for 5 minutes, return with fresh eyes
4. **Get help** — Ask a colleague, Stack Overflow, documentation
5. **Reset** — `git stash`, start completely fresh
