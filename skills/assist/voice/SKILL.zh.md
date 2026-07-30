---
name: voice
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  使用可替换的可选工具规划录音、转写和语音输出。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [voice, speech, stt, tts, provider-neutral]
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

<img src="banner.png" width="100%" alt="voice banner">

# 供应商中立的语音助手

## 用途

定义不依赖私有后端供应商的语音流程。

**结果:** 包含输入格式、隐私决定、工具选项和回退方案的流程计划。

## 工作流程

1. 明确目标、背景和所需输出格式。
2. 只使用当前请求中提供的信息。
3. 生成结构清晰且可追溯的结果。
4. 标记假设，并在外部变更前取得确认。

## 示例

**输入:** 为音频文件规划本地转写流程。

**结果:** 包含输入格式、隐私决定、工具选项和回退方案的流程计划。

## 公共核心与私有扩展

此公共 Skill 只包含可移植的方法。特定应用适配器、账户、本地路径、数据库和个人默认设置必须保留在私有补充配置或私有 fork 中，不得提交到此仓库。

没有私有配置时，Skill 只使用当前请求中明确提供的信息。

## 限制与数据保护

- 默认不持久保存数据。
- 未经明确许可，不打开或修改任何来源、文件或接口。
- 在云端处理前，必须明确同意、数据分类和保留期限。

## 变更记录

### 2.0.0 (2026-07-30)

- 改为用户中立的公共核心；移除私有集成和个人配置。
