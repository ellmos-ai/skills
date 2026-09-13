---
name: project-onboarding
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 新软件项目入职的标准流程：功能分析、代码质量审查、入职检查清单和任务创建。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [onboarding, project, intake, analysis, checklist, code-review]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/projekt-aufnahme.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="project-onboarding banner">

> **中文** — `project-onboarding` 官方中文版本。


# 新软件项目标准入职流程 (中文)

**版本：** 1.0
**日期：** 2026-03-12

---

## 概述与目的

本流程定义了在将新发现的软件文件夹添加到任务管理系统之前需要执行的步骤。

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

## 阶段 1：功能分析

**目的：** 理解工具及其功能和开发状态。

**创建文件：** `Feature_Analysis_<ToolName>.md`

### 模板

```markdown
# Feature Analysis: <ToolName> (Deutsch)

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

## 阶段 2：代码质量审查

**目的：** 确保技术质量，识别已知问题。

### 推荐检查项

| 测试项目 | 工具 | 描述 |
|----------|------|------|
| **编码格式** | 编码检查工具 (例如 `chardet`, `file`) | 确保 UTF-8 |
| **方法分析** | Linter (例如 `pylint`, `flake8`) | 查找过大的方法 |
| **缩进** | 格式化工具 (例如 `black`, `autopep8`) | 检查一致性 |
| **导入项** | 导入检查工具 (例如 `isort`, `pylint`) | 查找未使用的导入 |

### 检查要点

- [ ] 所有 .py 文件是否为 UTF-8 编码？
- [ ] 是否没有异常巨大的方法（>100 行）？
- [ ] 缩进是否一致（空格与制表符）？
- [ ] 是否移除了未使用的导入？
- [ ] 是否编写了 Docstring 文档字符串？

### 记录结果

在 TASKS.txt 的 "QUALITY REVIEW" 下记录发现的问题。

---

## 阶段 3：创建 TASKS.txt

**目的：** 以结构化格式记录待办任务。

**创建文件：** 项目文件夹中的 `TASKS.txt`

### 模板

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

### 状态值

| 状态 | 含义 |
|------|------|
| NEWLY DISCOVERED | 尚未分析 |
| ANALYSIS NEEDED | 功能分析进行中 |
| QUALITY REVIEW | 代码测试运行中 |
| VALIDATED & READY | 已准备好开发功能 |
| MVP | 最小可行性产品 |
| BUILD ONLY | 仅需编译构建 |
| BLOCKED | 等待用户测试/决定 |

---

## 阶段 4：任务管理集成

在完成阶段 1-3 之后：

1. **转换任务：** 将 TASKS.txt 条目创建为任务/Issue
2. **验证：** 所有任务是否分类正确？
3. **分类：** 将项目分配到适当的类别（独立工具、套件、库等）

### 自动入职任务

对于新项目，创建以下标准任务：

| 任务 | 描述 | 工作量 |
|------|------|--------|
| onb_1 | 创建功能分析 | 中 |
| onb_2 | 代码质量审查 | 低 |
| onb_3 | 创建 TASKS.txt | 低 |

任务之间存在依赖关系：onb_2 依赖于 onb_1，onb_3 依赖于 onb_2。

---

## 快速检查清单

```
[ ] 1. Feature_Analysis_<Name>.md created
[ ] 2. Code quality review completed (linter, encoding, imports)
[ ] 3. TASKS.txt created with status
[ ] 4. Tasks added to task management
```

---

## 示例与应用

```bash
# 1. Feature analysis (Deutsch)
# -> Create Feature_Analysis_MyTool.md (see template) (Deutsch)

# 2. Code quality (Deutsch)
pylint MyTool/main.py
flake8 MyTool/main.py
file -i MyTool/main.py  # Check encoding

# 3. TASKS.txt (Deutsch)
# -> Create in tool folder with status "QUALITY REVIEW" (Deutsch)

# 4. Create tasks (Deutsch)
# -> Capture TASKS.txt entries as issues/tickets (Deutsch)
```

---

*创建于：2026-01-10 | 移植于：2026-03-12*
