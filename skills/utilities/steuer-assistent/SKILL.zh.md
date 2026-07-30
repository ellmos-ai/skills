---
name: steuer-assistent
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-07-23
updated: 2026-07-23
description: 指向独立模块 steuer-assistent：一个针对德国雇员相关收入费用（Werbungskosten）的本地、离线优先的收据工作表 —— 记录、精确到分的汇总、私有 ZIP 导出。当需要以结构化方式准备 Werbungskosten 收据时使用此 skill —— 具有明确界限：非税务咨询，不做可扣除性检查，也不创建或提交报税单（报税需通过 ELSTER 或获批软件进行）。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance: {'origin': 'external', 'origin_repo': 'https://github.com/ellmos-ai/steuer-assistent', 'origin_path': 'SKILL.md, steuer_assistent/ (CLI module)', 'origin_version': None, 'last_sync_from_origin': '2026-07-23', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
category: utilities
tags: [tax, germany, receipts, finance, wrapper, pointer-skill]
language: zh
status: active
---

<img src="banner.png" width="100%" alt="steuer-assistent banner">

> **中文** — `steuer-assistent` 官方中文版本。


# steuer-assistent -- Pointer Skill (中文)

本 skill 是指向独立公共模块仓库
[`ellmos-ai/steuer-assistent`](https://github.com/ellmos-ai/steuer-assistent)
（MIT 许可证，公开）的**轻量级指针（wrapper）**。实际的 skill 保存在该仓库中 —— 本仓库仅建立链接并记录安装说明。

注意：`steuer-assistent` 仅适用于德国税法（雇员相关收入费用，"Werbungskosten"）；其 CLI 和文档按设计均为德语。

## 模块的功能

`steuer-assistent` 是一个用于德国雇员相关收入费用（Werbungskosten）自定义分类收据的小型离线优先 Python 模块：

- 记录收据（类别、金额、日期、可选备注）。
- 按年度汇总已记录的费用，精确到分。
- 导出私有的非官方 ZIP 工作表（包含 CSV + 摘要 + 非官方声明，不包含收据文件本身）。
- 本地存储（默认 `%USERPROFILE%\.steuer-assistent\steuer.db`），无网络访问，无云端上传，无法访问其他数据库。

## 边界（重要）

- **非税务咨询。** 该模块不评估单个项目的可扣除性，也不创建或提交报税单。
- 官方电子提交仅通过 ELSTER 或获批的软件进行 —— 不能通过此模块进行。
- 范围：雇员相关收入费用的私有工作表；不包含商业/自雇费用跟踪。

## 安装（通用，无本地路径）

1. 克隆模块：
   ```bash
   git clone https://github.com/ellmos-ai/steuer-assistent.git <clone-path>
   ```
2. 安装并验证：
   ```bash
   cd <clone-path>
   python -m pip install -e .
   python -B -m pytest tests -q -p no:cacheprovider
   ```
3. 将 `<clone-path>/SKILL.md` 采纳到您自己的 skill 环境中（例如 `~/.claude/skills/steuer-assistent/`）。切勿将真实的本地路径或主机名提交到版本控制的 skill 环境中。
4. 如果需要，可以通过 `STEUER_ASSISTENT_DB=<path>` 或 `--store <path>` 调整存储路径；默认值为用户的主目录。
5. 有关 CLI 命令、隐私和边界，请参阅模块仓库的 README。

## 此 pointer skill 的来源

此 wrapper 于 2026-07-23 添加，作为 `ellmos-ai/skills` 仓库的展示条目。**无代码重复** —— 维护和版本控制仅保留在 `ellmos-ai/steuer-assistent` 模块仓库中。

## 变更日志

### 0.1.0 (2026-07-23)
- `ellmos-ai/steuer-assistent` 的初始 pointer skill。