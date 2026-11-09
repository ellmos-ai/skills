---
name: formbuilder-reader
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-11-09
description: "当审查表单设计规范、JSON Schema 或 UI 输入表单的结构、无障碍访问性及校验逻辑时使用（例如 '验证表单模式'、'检查表单无障碍访问'、'审核表单输入字段'、/formbuilder-reader）。评估输入字段、错误提示、易用性及 WCAG 无障碍标准。切勿用于自动化网页表单提交（使用 web/web-reading）。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [forms, schema, validation, accessibility]
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


<img src="banner.png" width="100%" alt="formbuilder-reader banner">

# 表单结构读取器

## 用途

独立于具体应用分析 JSON、YAML、CSV 或文本表单。

**结果:** 字段图、验证风险、无障碍发现和具体改进建议。

## 工作流程

1. 明确目标、背景和所需输出格式。
2. 只使用当前请求中提供的信息。
3. 生成结构清晰且可追溯的结果。
4. 标记假设，并在外部变更前取得确认。

## 示例

**输入:** 检查此 JSON 表单的必填字段和标签清晰度。

**结果:** 字段图、验证风险、无障碍发现和具体改进建议。

## 公共核心与私有扩展

此公共 Skill 只包含可移植的方法。特定应用适配器、账户、本地路径、数据库和个人默认设置必须保留在私有补充配置或私有 fork 中，不得提交到此仓库。

没有私有配置时，Skill 只使用当前请求中明确提供的信息。

## 限制与数据保护

- 默认不持久保存数据。
- 未经明确许可，不打开或修改任何来源、文件或接口。

## 变更记录

### 2.0.0 (2026-07-30)

- 改为用户中立的公共核心；移除私有集成和个人配置。
