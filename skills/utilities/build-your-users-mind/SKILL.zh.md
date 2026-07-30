---
name: build-your-users-mind
version: 1.0.0
type: skill
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  指向公开且与提供商无关的 build-your-users-mind 模块。该模块提供一种注重隐私的
  方法，在获得明确授权后，从用户自己的交互日志中构建经验性的心智理论偏好模型。
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [theory-of-mind, user-model, decision-avatar, feedback, privacy, pointer-skill]
language: zh
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "external"
  origin_path: "SKILL.md, templates/, scripts/, schemas/, TAXONOMY.md"
  origin_version: "1.0.0"
  origin_repo: "https://github.com/ellmos-ai/build-your-users-mind"
  last_sync_from_origin: "2026-07-30"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="build-your-users-mind banner">

# build-your-users-mind — 公开且提供商中立的指针

此 skill 是指向公开模块
[`ellmos-ai/build-your-users-mind`](https://github.com/ellmos-ai/build-your-users-mind)
的轻量指针。完整方法、模板、架构、脚本、测试和源适配器文档均位于模块仓库中；
本目录不复制这些代码。

## 模块功能

在操作员明确授权后，该模块可帮助智能体：

1. 从操作员自己的交互日志中提取真正由用户输入的内容；
2. 在持久化之前清除敏感材料；
3. 归纳并分类重复出现的偏好和决策证据；
4. 创建带有置信度和来源信息的本地偏好模型；
5. 在选定的智能体运行环境中绑定一个简短指针；
6. 根据之后收到的真实反馈校准预测。

公开模块适用于任何用户和受支持的智能体运行环境，不包含特定个人的模型。

## 安全与隐私边界

- 读取交互日志之前必须获得操作员授权。
- 个人档案、原始日志、证据语料和本地路径必须保持私密。
- 预测是不确定的假设，不是读心、诊断或用户本人的陈述。
- 偏好预测绝不能扩大智能体的权限。
- 外部、不可逆、安全关键、法律、医疗、就业、金融或类似高影响操作必须获得
  明确确认。
- 智能体生成的预测绝不能成为描述用户的第一手证据。

## 安装

```bash
git clone https://github.com/ellmos-ai/build-your-users-mind.git <clone-path>
```

请遵循模块当前的 `README.md`、`SKILL.md`、`SOURCE-ADAPTERS.md` 和隐私说明。
生成的用户档案必须保存在公开仓库之外。模块仓库是实现和版本管理的权威来源。

## 公开核心与私有档案

`build-your-users-mind` 是公开且用户中立的模块名称。
`decision-avatar` 是本目录中的公开运行协议。特定个人的头像、证据文件、本地命令和
个性化默认设置属于私有扩展，不得以个人 skill 名称发布。

## 更新日志

### 1.0.0 (2026-07-30)

- 添加指向独立公开模块的中立指针。
- 将此前发布的个人头像档案替换为严格的公开核心与私有档案边界。
