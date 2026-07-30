---
name: gesundheit
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  整理用户自愿提供的健康信息，并准备向专业人士咨询的问题。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [health, organization, questions, safety]
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

<img src="banner.png" width="100%" alt="gesundheit banner">

# 健康信息整理

## 用途

客观总结症状、时间变化、用药和待确认问题。

**结果:** 时间线、结构化观察、安全提示和向医务人员提出的问题。

## 工作流程

1. 明确目标、背景和所需输出格式。
2. 只使用当前请求中提供的信息。
3. 生成结构清晰且可追溯的结果。
4. 标记假设，并在外部变更前取得确认。

## 示例

**输入:** 把这些症状笔记整理成就诊用的简短时间线。

**结果:** 时间线、结构化观察、安全提示和向医务人员提出的问题。

## 公共核心与私有扩展

此公共 Skill 只包含可移植的方法。特定应用适配器、账户、本地路径、数据库和个人默认设置必须保留在私有补充配置或私有 fork 中，不得提交到此仓库。

没有私有配置时，Skill 只使用当前请求中明确提供的信息。

## 限制与数据保护

- 默认不持久保存数据。
- 未经明确许可，不打开或修改任何来源、文件或接口。
- 本 Skill 不作诊断，也不能替代医疗照护。出现紧急危险时应联系当地急救服务。

## 变更记录

### 2.0.0 (2026-07-30)

- 改为用户中立的公共核心；移除私有集成和个人配置。
