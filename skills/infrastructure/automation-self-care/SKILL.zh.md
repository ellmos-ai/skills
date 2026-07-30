---
name: automation-self-care
version: 1.0.1
type: skill
author: Lukas Geiger + OpenAI
created: 2026-07-28
updated: 2026-07-30
description: >
  构建并运行独立于提供商的自愈核心集，用于定时 LLM 任务和桌面应用自动化。适用于
  Agent 需要探索其原生调度器、安装定期卫生检查、提示词质量检查、频率与负载检查、资源检查、跨系统协调、权限及运行时检查，或通过回滚、回读和删除保护持续改进现有自动化舰队的场景。可由
  automation self-care、scheduler task care、desktop app automation
  maintenance、automation fleet audit、self-healing schedules、要求重新创建
  ANTIGRAVITY 风格维护任务族的请求、core-set-textautomations、basic-text-automations、textbased-automation-core、textbased-automation-drivers
  或 textbased-desktopapp-automations 触发。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, scheduler, desktop-apps, self-care, maintenance, rollback, cross-system]
language: zh
status: active
aliases: [core-set-textautomations, basic-text-automations, textbased-automation-core, textbased-automation-drivers, textbased-desktopapp-automations]
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

> **中文** — `automation-self-care` 官方中文版本。

# Automation Self-Care

基于单个独立于提供商的控制回路，创建原生的、针对特定提供商的维护 Fleet。在保留 ANTIGRAVITY 任务族原始意图的同时，要求提供证据、可逆变更以及原生回读。

## 不可逾越的边界

- 将探索、规划、审批、变更和回读视为相互独立的阶段。
- 使用目标应用所支持的自动化 API、命令行或 UI。绝不可假设编辑存储文件就能改变运行中的应用状态。
- 在提出任务方案前，先读取本地规则、锁、删除/抑制日志以及已有调度计划。
- 切勿虚构调度器支持。若无法证明创建、更新或回读可行，需生成手动安装方案并在变更前停止。
- 每次自愈运行最多仅允许进行一项可独立测试的调优变更。
- 保护自愈任务，防止其自我禁用或将其运行频率降低至配置的恢复下限以下。
- 保存先前的提示词、调度计划、模型、权限和启用状态，以便能够回滚每次变更。
- 只有在获得结果证据后才算成功，不能仅凭调度器启动或退出代码为 0。
- 切勿将密钥、私密提示词或个人数据复制到共享注册表中。

## 工作流

### 1. 探索原生自动化界面

盘点当前的 Actor、提供商、应用类型、调度器界面、支持的操作、状态文件、运行历史、使用情况遥测及回读方法。在 [provider-adapter-contract.md](references/provider-adapter-contract.md) 中使用 Profile 契约记录相关能力。

明确区分原生桌面应用调度、CLI/无头（headless）执行、操作系统调度器或服务启动器、通用调度器服务、工作流引擎以及不支持或仅支持 UI 的自动化。切勿将配置文件的存在等同于支持的变更路径。

### 2. 盘点 Fleet

为每个任务捕获稳定的本地标识符、用途、提示词指纹、调度计划、启用状态、模型、权限、目标路径、上次调度器事件、上次成功结果及当前所有者。提示词内容保持本地化。

当应用可以从内存重写状态时，在变更前对权威的实时界面进行两次检查。

### 3. 设计核心集 (Core Set)

阅读 [core-set.md](references/core-set.md)。选择以下任一方案：

- `compact`：结合频率与负载分发的五个自愈任务；或
- `full`：对应原始维护任务族的九个专项任务。

生成独立于提供商的方案：

```bash
python scripts/build_core_set.py provider-profile.json \
  --topology compact --out automation-care-plan.json
```

生成器绝不会自行安装任务。在应用方案前，请审查每一个处于 `blocked` 状态的能力，并选择无冲突的本地时间。

### 4. 阶段化安装

通过原生提供商适配器进行安装：

1. 首先以只读模式运行卫生检查。
2. 添加资源保护。
3. 添加带有回滚机制的提示词质量调优。
4. 仅在拥有足够运行证据后，再添加频率与负载调优。
5. 最后添加跨系统协调。

创建的新任务或导入的任务应默认处于禁用状态，除非用户明确批准激活安装。对于无人值守的试点运行，首先需要准备删除日志、变更前状态快照、运行回执及回滚路径。

### 5. 运行自愈回路

每个自愈任务均遵循以下流程：

```text
follow-up previous change
  -> collect current evidence
  -> classify one cause
  -> choose zero or one change
  -> mutate through native surface
  -> read back
  -> write receipt and next-check condition
```

使用 [core-set.md](references/core-set.md) 中的假设目录和证据规则。原因未知意味着进行观察、缩小权限或安全暂停；切勿凭空猜测修复方案。

### 6. 跨 Actor 协调

保持本地应用状态的权威性。仅共享任务契约、覆盖范围、状态、回执和已脱敏的指纹。允许冗余的只读审查；单写者的变更需要申请 Claim 或等效的原生锁。

### 7. 无原生事件钩子的系统（Letter-Hooker 扩展）

将 Token 或订阅限制视为容量状态，而非故障 Actor。在原始 Actor 生成成功回执后，归还委托的覆盖范围。

## 必需输出

针对每次配置或自愈运行报告以下内容：

- 已探索的原生界面及不支持的能力；
- 选定的拓扑以及已创建、已建议或已跳过的任务；
- 确切的变更及变更前后的回读结果；
- 结果证据或开启的观察窗口；
- 回滚位置及返回条件；
- 共享覆盖范围更新（若存在协调注册表）。

## 示例

用户：“在此桌面应用中设置自我维护的调度计划。”

探索应用是否能够列出、创建、更新和验证定时任务。生成 Compact 方案，展示不支持的能力，然后仅通过原生界面安装经批准的任务。仅包含任务提示词而没有实时调度器注册信息的文件夹不能算作已完成的配置。

## 更新日志

### 1.0.1 (2026-07-30)

- 添加了独立于提供商的文本自动化和桌面应用自动化别名。

### 1.0.0 (2026-07-28)

- 将原始 ANTIGRAVITY 维护任务族、F1-F6 控制回路以及后续特定提供商的适配整合为一个中立的核心集 Skill。