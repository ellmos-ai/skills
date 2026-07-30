---
name: docs-analysis
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: 文档需求分析：分析 docs/ 文件夹中的概念与需求文档，将需求与当前代码进行对比检查，并生成整合的差异报告。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [docs-analysis, requirements, code-review, diff-report, quality-assurance]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/docs-analyse.md', 'origin_version': '1.2.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **中文** — `docs-analysis` 官方中文版本。


# 文档需求分析 (中文)

> 分析所有概念和需求文档，将需求与当前代码进行对比检查，并生成整合的差异报告。

---

## 概述与目的

分析 `../docs/` 文件夹中的所有概念和需求文档，将需求与当前代码进行对比检查，并生成整合的差异报告。

---

## 命名规范

### 前缀与后缀
所有被分析的文档都会获得：
- **前缀：** `conN_`，其中 N = 分析版本（1, 2, 3, ...）
- **后缀：** `_XX`，其中 XX = 完成百分比（四舍五入到最近的 10）

### 归档阈值
- **>= 75% 完成：** 文档移动到 `../docs/_archive/`
- **< 75% 完成：** 文档保留在 `../docs/` 中，带前缀/后缀
- **阈值可配置**（默认：75）

---

## 流程

### 阶段 1：收集文档
- 列出 `../docs/`（根目录）下的所有 `*.md` 和 `*.txt` 文件
- 过滤掉 `README.txt`

### 阶段 2：提取需求
对于每个文档：
- 读取内容
- 识别需求（检查清单、表格、MISSING/TODO 标记）
- 分类：结构、代码、API、数据库模式、CLI、功能

### 阶段 3：代码验证
对于每个需求：
- 确定验证方法（Glob、Grep、Read）
- 执行验证
- 标记为：FULFILLED、PARTIAL、MISSING

### 阶段 4：评估
- 统计已完成与未完成的需求
- 计算完成百分比（%）
- 决定：归档（>= 75%）或保留（< 75%）

### 阶段 5：生成输出
- 创建 `REQUIREMENTS_ANALYSIS.md`（摘要）
- 创建 `consense_diff.md`（仅未完成需求，按优先级）

### 阶段 6：版本控制
- 扫描最高 `conN_` 前缀
- 新版本 = 最高 + 1

### 阶段 7：重命名与移动
- 向文档应用新前缀/后缀
- 归档或保留

---

## 输出

| 文件 | 描述 |
|------|------|
| `conN_REQUIREMENTS_ANALYSIS.md` | 完整分析（版本 N） |
| `consense_diff_N.md` | 整理后的未完成需求 |
| `_archive/conN_*_XX.*` | 已归档（>=75%）文档 |

---

## 优先级分类

| 优先级 | 标准 |
|:------:|------|
| P1 | 核心功能缺失，系统不可用 |
| P2 | 重要功能缺失，存在变通方案 |
| P3 | 可有可无，改善 UX |
| P4 | 美化、文档、代码质量 |

---

## 变更日志

### 1.0.0 (2026-03-15)
- 移植自 BACH v3.8.0

---

*移植自 BACH v3.8.0 | 独立版本*