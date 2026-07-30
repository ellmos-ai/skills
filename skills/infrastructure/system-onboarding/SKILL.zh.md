---
name: system-onboarding
version: 1.2.0
type: skill
author: ellmos contributors
created: 2026-05-16
updated: 2026-07-29
description: >
  用于全新、重建或替换工作站的跨供应商通用入职集成协议。它建立了操作系统前置条件、
  Agent 运行时、共享规则集、便携式技能、验证配置及安装后凭证，而无需将凭据、
  私有提示词或特定主机配置复制到代码库中。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [onboarding, setup, agent-runtimes, windows, macos, verification, sync]
language: zh
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: "internal onboarding protocol (sanitized for portable publication)"
  origin_version: "1.2.0"
  last_sync_from_origin: "2026-07-29"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

> **中文** — `system-onboarding` 官方中文版本。

# 系统入职集成

使用本协议为本地优先的 Agent 工作建立全新或重建的工作站。这是一份排序与验证指南，而非安装程序或凭据来源。在更改运行中的系统前，请先查阅各供应商的最新官方文档以了解特定产品的说明。

## 激活

适用于全新工作站、重装操作系统、替换设备或对单个 Agent 运行时进行受控恢复。首先确认操作系统、目标运行时、所有者、共享规则集，以及该请求是全面重建还是受限组件修复。切勿假设从某台主机复制的配置在另一台主机上是安全或受支持的。

## 有序工作流

1. 建立操作系统更新、Git、已身份验证的源码控制、Python 以及必要时当前受支持的 Node.js LTS。
2. 仅通过官方支持的安装程序安装所需的 Agent 运行时，并完成其原生登录流程，切勿将 Token 放入项目文件中。
3. 创建本地配置根目录并加载显式选择的规范规则集。合并模板；切勿盲目覆盖现有的本地状态。
4. 仅通过指定的部署程序安装便携式技能以及 MCP 或插件配置。将每个供应商的配置格式视为独立的。
5. 仅在本地运行时正常工作后，才配置共享同步。仅共享经过脱敏处理的契约和收据，不得共享凭据、完整提示词或本机局部路径。
6. 仅通过受支持的原生接口重建计划任务调度器或自动化流程。保留原有状态，在所有者批准激活前保持新工作处于禁用状态。
7. 运行相应的安装后检查，并编写一份清晰区分安装、配置、调度器注册及成功结果的本地收据。

请仅阅读与目标平台相匹配的参考文档：

- [概览](references/overview.md) 了解边界与数据放置；
- [Windows 检查清单](references/windows-checklist.md) 适用于 Windows；
- [macOS 检查清单](references/mac-checklist.md) 适用于 macOS；以及
- [安装后检查](references/post-install.md) 用于验证与恢复。

## 边界与限制

- 切勿将凭据、恢复代码、私有提示词、账户标识符或原始日志发布到共享仓库或同步文件夹中。
- 将虚拟环境、依赖缓存和大文件运行时构件排除在云同步的项目文件夹之外。
- 切勿将复制的配置作为权威依据。目标主机必须自行检测并读回其自身受支持的状态。
- 切勿仅因任务文件存在就注册定时调度。原生注册与执行结果证据是两个独立的要求。
- 在修复现有主机时，请在更改任何配置前先盘点其当前状态与锁文件。

## 完成证据

一份完整的入职收据记录了目标操作系统、选定的运行时及其已验证的版本、已加载的规范规则参考、已部署的显式技能或扩展、不受支持的功能以及任何缓议的用户决策。仅凭命令成功退出不足以证明应用程序已加载其新配置，也不足以证明计划任务达到了预期的结果。

## 变更日志

### 1.2.0 (2026-07-29)

- 在移除特定主机的路径、账户详情和私密操作材料后，将可复用的入职集成顺序及平台参考文档移植到公共技能目录中。