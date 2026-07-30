---
name: project-onboarding
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 新软件项目接管与新成员入职的标准流程：功能分析、代码质量审查、入职检查清单以及任务创建。
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


# 新软件项目标准接管/入职规程 (中文)

**版本：** 1.0
**日期：** 2026-03-12

---

## 概述与目的

本规程定义了在将新发现的软件文件夹添加到任务管理系统之前需要执行的步骤。

```
+─────────────────────────────────────────────────────+
|               标准接管/入职规程                      |
+─────────────────────────────────────────────────────+
|  1. 创建功能分析                                     |
|  2. 代码质量审查（标准测试）                           |
|  3. 创建 TASKS.txt                                   |
|  4. 添加至任务管理                                   |
+─────────────────────────────────────────────────────+
```

---

## 第一阶段：功能分析

**目的：** 理解工具、其功能以及开发状态。

**创建文件：** `Feature_Analysis_<ToolName>.md`

### 模板

```markdown
# 功能分析：<ToolName> (中文)

## 简短描述
用一句话简要描述该工具的功能。

---

## 核心亮点

| 特性 | 描述 |
|---------|-------------|
| **特性 1** | 描述 |
| **特性 2** | 描述 |

---

## 开发阶段评估

### 当前状态：**<Status> (<X>%)**

可能的状态：
- Prototype (原型阶段 0-30%)
- Alpha (Alpha 阶段 30-60%)
- Beta (Beta 阶段 60-85%)
- Production Ready (生产就绪 85-95%)
- Release (正式发布 95-100%)

| 类别 | 评分 (1-5) | 详细信息 |
|----------|:------------:|---------|
| **功能性** | 3 | |
| **UI/UX** | 3 | |
| **稳定性** | 3 | |
| **文档** | 3 | |

---

## 推荐扩展

### 优先级：高
1. ...

### 优先级：中
2. ...

### 优先级：低
3. ...

---

## 技术细节

框架：            <Framework>
文件大小：        Python 代码共 <X> 行
主文件：          <main.py>

---
*分析创建于：<Date>*
```

---

## 第二阶段：代码质量审查

**目的：** 确保技术质量，识别已知问题。

### 推荐检查项目

| 测试项 | 工具 | 描述 |
|------|------|-------------|
| **编码 (Encoding)** | 编码检查工具（如 `chardet`、`file`） | 确保为 UTF-8 |
| **函数/方法分析** | Linter 代码检查（如 `pylint`、`flake8`） | 查找过长的函数/方法 |
| **缩进 (Indentation)** | 格式化工具（如 `black`、`autopep8`） | 检查一致性 |
| **导入 (Imports)** | 导入检查工具（如 `isort`、`pylint`） | 查找未使用的导入 |

### 检查清单

- [ ] 所有 .py 文件是否均为 UTF-8 编码？
- [ ] 是否存在异常庞大的函数/方法（>100 行）？
- [ ] 缩进是否一致（空格 vs 制表符）？
- [ ] 是否已移除未使用的导入？
- [ ] 是否包含 Docstrings 文档注释？

### 记录结果

在 `TASKS.txt` 中的 "QUALITY REVIEW" 标题下记录发现的问题。

---

## 第三阶段：创建 TASKS.txt

**目的：** 以结构化格式记录待办任务。

**创建文件：** 项目文件夹中的 `TASKS.txt`

### 模板

```
TASKS - <ToolName> V<Version>
==============================
状态: <Status>
日期: <Date>

待办任务 (OPEN TASKS):
[ ] <任务 1> - 工作量: <LOW|MEDIUM|HIGH>
[ ] <任务 2> - 工作量: <LOW|MEDIUM|HIGH>

---
已完成 (DONE - Archive):
- <已完成的任务> (<Version>, <Date>)
```

### 状态值说明

| 状态 | 含义 |
|--------|---------|
| NEWLY DISCOVERED | 新发现，尚未分析 |
| ANALYSIS NEEDED | 功能分析正在进行中 |
| QUALITY REVIEW | 代码测试/审查运行中 |
| VALIDATED & READY | 验证通过，已准备好进行特性开发 |
| MVP | 最小可行性产品 (Minimum Viable Product) |
| BUILD ONLY | 仅需编译/构建 |
| BLOCKED | 阻塞，等待用户测试或决策 |

---

## 第四阶段：集成至任务管理

完成第一至三阶段后：

1. **迁移任务：** 将 TASKS.txt 中的条目作为 Task/Issue 创建
2. **校验：** 所有任务分类是否准确？
3. **分类归档：** 将项目分配至恰当的类别（独立工具、套件、库等）

### 自动入职任务

对于新项目，自动创建以下标准任务：

| 任务 ID | 描述 | 工作量 |
|------|-------------|--------|
| onb_1 | 创建功能分析文件 | medium |
| onb_2 | 代码质量审查 | low |
| onb_3 | 创建 TASKS.txt | low |

任务存在依赖关系：onb_2 依赖于 onb_1，onb_3 依赖于 onb_2。

---

## 快速检查清单

```
[ ] 1. 已创建 Feature_Analysis_<Name>.md
[ ] 2. 已完成代码质量审查（Linter、编码、导入检查）
[ ] 3. 已创建包含状态的 TASKS.txt
[ ] 4. 任务已添加至任务管理系统
```

---

## 示例与应用

```bash
# 1. 功能分析
# -> 创建 Feature_Analysis_MyTool.md（参见模板）

# 2. 代码质量检查
pylint MyTool/main.py
flake8 MyTool/main.py
file -i MyTool/main.py  # 检查编码

# 3. 创建 TASKS.txt
# -> 在工具文件夹中创建，状态设为 "QUALITY REVIEW"

# 4. 创建任务
# -> 将 TASKS.txt 条目录入为 Issues/Tickets
```

---

*创建时间：2026-01-10 | 迁移时间：2026-03-12*