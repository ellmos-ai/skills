---
name: haushalt-manager
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-11-09
description: "当规划家庭杂务分工、居室保洁日常流程、家电维护周期或日程表时使用（例如 '制定家务分工表'、'规划清洁日常流程'、'跟踪居家设施维护周期'、/haushalt-manager）。以应用中立的方式科学规划家庭事务与周期性职责。切勿用于办公公文归档（使用 assist/buero）或库存备件核查（使用 assist/hauslagerist-reader）。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [household, routines, tasks, planning]
language: zh
status: stable
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: public-neutral
  origin_license: MIT
  notes: Public core only; adapters and private profiles are excluded.
---


<img src="banner.png" width="100%" alt="haushalt-manager banner">

# 家务规划

## 用途

现实地分配周期性任务和一次性任务。

**结果:** 包含工作量、优先级、负责人和缓冲时间的周计划。

## 工作流程

1. 明确目标、背景和所需输出格式。
2. 只使用当前请求中提供的信息。
3. 生成结构清晰且可追溯的结果。
4. 标记假设，并在外部变更前取得确认。

## 示例

**输入:** 根据这些任务创建均衡的周计划。

**结果:** 包含工作量、优先级、负责人和缓冲时间的周计划。

## 公共核心与私有扩展

此公共 Skill 只包含可移植的方法。特定应用适配器、账户、本地路径、数据库和个人默认设置必须保留在私有补充配置或私有 fork 中，不得提交到此仓库。

没有私有配置时，Skill 只使用当前请求中明确提供的信息。

## 限制与数据保护

- 默认不持久保存数据。
- 未经明确许可，不打开或修改任何来源、文件或接口。

## 变更记录

### 2.0.0 (2026-07-30)

- 改为用户中立的公共核心；移除私有集成和个人配置。
