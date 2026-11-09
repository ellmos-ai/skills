---
name: finanz-versicherung
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-11-09
description: "当梳理、归档和核对个人或企业的财务单据、保险保单与合同文本时使用（例如 '整理保险保单'、'梳理财务资料'、'核对合同续约期限'、/finanz-versicherung）。在不提供法律或投资咨询的前提下输出中立清单、截止日期时间表与审查清单。切勿用于具备法律效力的税务或投资建言。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [finance, insurance, documents, checklist]
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


<img src="banner.png" width="100%" alt="finanz-versicherung banner">

# 财务与保险概览

## 用途

在不提供建议或产品推荐的前提下整理合同、期限、文件和问题。

**结果:** 事实概览、期限清单以及咨询专业人士的问题。

## 工作流程

1. 明确目标、背景和所需输出格式。
2. 只使用当前请求中提供的信息。
3. 生成结构清晰且可追溯的结果。
4. 标记假设，并在外部变更前取得确认。

## 示例

**输入:** 根据这些匿名合同信息创建续期清单。

**结果:** 事实概览、期限清单以及咨询专业人士的问题。

## 公共核心与私有扩展

此公共 Skill 只包含可移植的方法。特定应用适配器、账户、本地路径、数据库和个人默认设置必须保留在私有补充配置或私有 fork 中，不得提交到此仓库。

没有私有配置时，Skill 只使用当前请求中明确提供的信息。

## 限制与数据保护

- 默认不持久保存数据。
- 未经明确许可，不打开或修改任何来源、文件或接口。
- 本 Skill 不能替代财务、税务、法律或保险专业建议。

## 变更记录

### 2.0.0 (2026-07-30)

- 改为用户中立的公共核心；移除私有集成和个人配置。
