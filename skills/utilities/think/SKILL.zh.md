---
name: think
version: 1.1.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-11-06
description: "当需要在决策或改动之前先理解代码之外的问题时使用：流程、组织、产品、战略、指标或业务层面的系统行为，原因可能有多种，或是需要拆解成若干部分的一团乱麻，或需要 SWOT / 80-20 视角的局面：'为什么总是反复出现 ...'、'找出根本原因'、'五个为什么'、'拆成子问题'、'我该从哪里入手'、'快速做个 SWOT'、'到底发生了什么'、/think。运用分治法、根本原因分析、放宽约束、类比搜索、SWOT、帕累托和鱼骨图，最后给出找到的原因或结构，以及第一个要检查的点。不要用于：软件缺陷（错误信息、失败的构建、测试或部署、回归：bugfix-protocol）、产生大量创意（brainstorm）、在已有选项中做选择（decide）、对照项目历史挖掘创意（idea-mining），或分析-创意-决策的完整流程（structured-thinking）。"

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [thinking, problem-solving, analysis, swot, root-cause, heuristics]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/think.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="think banner">

> **中文** — `think` 官方中文版本。


# Think — 问题解决与分析

> 针对复杂问题的结构化思维过程

---

## 问题解决途径

### 1. Divide & Conquer（分治法）

```
Problem -> Sub-problems -> Solve individually -> Combine
```

### 2. Root Cause Analysis（根本原因分析）

```
Symptom -> Why? -> Why? -> Why? -> Root cause -> Solution
```

### 3. Constraint Relaxation（放宽约束）

```
Unsolvable problem -> Relax constraints -> Solve -> Re-apply constraints
```

### 4. Analogy Search（类比搜索）

```
New problem -> Similar known problem -> Adapt solution
```

---

## 分析方法

| 方法 | 应用 |
|------|------|
| **SWOT** | 优势 / 劣势 / 机会 / 威胁 |
| **利弊分析 (Pro/Con)** | 决策制定 |
| **Pareto** | 80/20 优先级排序 |
| **Fishbone** | 根本原因分析（石川图） |

---

## 决策启发式方法

### 不确定性下

```
1. 最坏的情况是什么？
2. 是否可逆？
3. 不采取行动的代价是什么？
```

### 复杂性下

```
1. 最简单的第一步是什么？
2. 专家会怎么做？
3. 80% 的解决方案会是什么？
```

---

## 变更日志

### 1.1.0 (2026-11-06)
- 重写描述，明确触发条件与边界（docs/CONVENTIONS.md 中的规则）：先写使用场景、用户常见说法和斜杠命令，并在“不要用于”条款中点名相邻技能。

### 1.0.0 (2026-03-15)
- 从 BACH v3.8.0 移植

---

*从 BACH v3.8.0 移植 | 独立版本*