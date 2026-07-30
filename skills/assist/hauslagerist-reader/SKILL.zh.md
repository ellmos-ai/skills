---
name: hauslagerist-reader
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  分析用户提供的库存清单或导出文件，不依赖特定库存软件。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [inventory, export, stock, analysis]
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

<img src="banner.png" width="100%" alt="hauslagerist-reader banner">

# 库存数据读取器

## 用途

评估库存、位置、最低数量和不一致项。

**结果:** 库存概览、缺货、重复项和待确认问题。

## 工作流程

1. 明确目标、背景和所需输出格式。
2. 只使用当前请求中提供的信息。
3. 生成结构清晰且可追溯的结果。
4. 标记假设，并在外部变更前取得确认。

## 示例

**输入:** 分析此 CSV 清单中的缺货和重复记录。

**结果:** 库存概览、缺货、重复项和待确认问题。

## 公共核心与私有扩展

此公共 Skill 只包含可移植的方法。特定应用适配器、账户、本地路径、数据库和个人默认设置必须保留在私有补充配置或私有 fork 中，不得提交到此仓库。

没有私有配置时，Skill 只使用当前请求中明确提供的信息。

## 限制与数据保护

- 默认不持久保存数据。
- 未经明确许可，不打开或修改任何来源、文件或接口。

## 变更记录

### 2.0.0 (2026-07-30)

- 改为用户中立的公共核心；移除私有集成和个人配置。
