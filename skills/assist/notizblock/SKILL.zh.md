---
name: notizblock
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-11-09
description: "当以平台中立的方式随手记录、整理及浓缩灵感随笔、即时心得或草稿片段时使用（例如 '快速便签'、'理清思绪想法'、'总结草稿随笔'、/notizblock）。无需依赖特定商业记事应用即可归纳自由文本笔记。切勿用于深度调研简报（使用 assist/dossier-briefing）或故障事件取证日志（使用 infrastructure/incident-notes）。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [notes, capture, summarize, organize]
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


<img src="banner.png" width="100%" alt="notizblock banner">

# 笔记助手

## 用途

把零散想法转化为可检索的主题、任务和决定。

**结果:** 包含标签、任务和待办事项的结构化笔记。

## 工作流程

1. 明确目标、背景和所需输出格式。
2. 只使用当前请求中提供的信息。
3. 生成结构清晰且可追溯的结果。
4. 标记假设，并在外部变更前取得确认。

## 示例

**输入:** 按主题和下一步整理这些会议笔记。

**结果:** 包含标签、任务和待办事项的结构化笔记。

## 公共核心与私有扩展

此公共 Skill 只包含可移植的方法。特定应用适配器、账户、本地路径、数据库和个人默认设置必须保留在私有补充配置或私有 fork 中，不得提交到此仓库。

没有私有配置时，Skill 只使用当前请求中明确提供的信息。

## 限制与数据保护

- 默认不持久保存数据。
- 未经明确许可，不打开或修改任何来源、文件或接口。

## 变更记录

### 2.0.0 (2026-07-30)

- 改为用户中立的公共核心；移除私有集成和个人配置。
