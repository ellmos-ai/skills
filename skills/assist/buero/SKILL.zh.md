---
name: buero
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-11-09
description: "当需要组织日常办公事务、商务函电、公文起草以及行政截止日期时使用（例如 '整理办公文档'、'起草商务信函'、'管理办公截止期限'、/buero）。以平台中立的方式梳理典型办公室工作、公函及期限清单。切勿用于私人日常简短邮件（使用 privat-mail-writer）或营销推广。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [office, planning, prioritization, correspondence]
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


<img src="banner.png" width="100%" alt="buero banner">

# 办公助手

## 用途

将未整理的办公事项转化为现实且有优先级的工作概览。

**结果:** 优先级、下一步、负责人和待确认问题。

## 工作流程

1. 明确目标、背景和所需输出格式。
2. 只使用当前请求中提供的信息。
3. 生成结构清晰且可追溯的结果。
4. 标记假设，并在外部变更前取得确认。

## 示例

**输入:** 请为今天整理这五项任务。

**结果:** 优先级、下一步、负责人和待确认问题。

## 公共核心与私有扩展

此公共 Skill 只包含可移植的方法。特定应用适配器、账户、本地路径、数据库和个人默认设置必须保留在私有补充配置或私有 fork 中，不得提交到此仓库。

没有私有配置时，Skill 只使用当前请求中明确提供的信息。

## 限制与数据保护

- 默认不持久保存数据。
- 未经明确许可，不打开或修改任何来源、文件或接口。

## 变更记录

### 2.0.0 (2026-07-30)

- 改为用户中立的公共核心；移除私有集成和个人配置。
