---
name: worksheet-generator
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-07-23
updated: 2026-07-23
description: >
  根据支持目标、年龄及难度生成个性化工作单与练习材料。
standalone: true
anthropic_compatible: true
category: education
tags: [worksheets, icf, education, therapy-support, wrapper]
aliases: [worksheet-generator, worksheet-generator-zh]
language: zh
status: active
---

<img src="banner.png" width="100%" alt="worksheet-generator banner">

> **Chinese** — 官方中文文档。

# 练习工作单与教学材料生成指南 (中文版)

本技能支持根据具体支持目标与年龄层，生成结构化的教学工作单及练习材料。

## 1. 概述与目标

- **自适应生成：** 围绕明确的教学与康复目标构建练习题。
- **ICF 编码关联：** 可选关联官方 ICF 功能编码。
- **多格式导出：** 支持导出为 Markdown、HTML 及 DOCX 格式。

## 2. 工作流程与执行步骤

1. **输入目标：** 设定教学支持目标（不含任何个人隐私数据）。
2. **设定难度：** 指定适用年龄段与难易程度。
3. **生成初稿：** 构建练习工作单框架与具体题目。
4. **专业审阅：** 在教学使用前由专业人员复核修改。

## 3. 不可逾越的边界与规则

- **严禁个人信息：** 仅使用抽象的目标与年龄参数。
- **必须专业复核：** 生成材料为初稿草案，必须经教师或专业人员审阅。
- **教学辅助定位：** 仅作为练习辅助材料，非医疗诊疗方案。

## 4. 必需输出与产出物

- 结构化的练习工作单（Markdown / HTML / DOCX 格式）。
- 供教师使用的参考答案与评分说明。
