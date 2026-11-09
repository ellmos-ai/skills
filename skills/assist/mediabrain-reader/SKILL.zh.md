---
name: mediabrain-reader
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-11-09
description: "当解析、整理及归档媒体清单、阅读书单、影视待看列表或音视频元数据时使用（例如 '分析影音藏品'、'图书与影视编目'、'结构化待看片单'、/mediabrain-reader）。以应用中立的方式组织媒体集合与元数据。切勿用于视频字幕文本的直接提取（使用 utilities/video-transcriber）。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [media, catalog, metadata, export]
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


<img src="banner.png" width="100%" alt="mediabrain-reader banner">

# 媒体目录读取器

## 用途

按类型、状态、主题或重复项评估媒体集合。

**结果:** 目录概览、质量问题以及搜索或清理建议。

## 工作流程

1. 明确目标、背景和所需输出格式。
2. 只使用当前请求中提供的信息。
3. 生成结构清晰且可追溯的结果。
4. 标记假设，并在外部变更前取得确认。

## 示例

**输入:** 按类型和状态总结此 JSON 媒体导出。

**结果:** 目录概览、质量问题以及搜索或清理建议。

## 公共核心与私有扩展

此公共 Skill 只包含可移植的方法。特定应用适配器、账户、本地路径、数据库和个人默认设置必须保留在私有补充配置或私有 fork 中，不得提交到此仓库。

没有私有配置时，Skill 只使用当前请求中明确提供的信息。

## 限制与数据保护

- 默认不持久保存数据。
- 未经明确许可，不打开或修改任何来源、文件或接口。

## 变更记录

### 2.0.0 (2026-07-30)

- 改为用户中立的公共核心；移除私有集成和个人配置。
