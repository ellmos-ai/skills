---
name: sec-hardening
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "基于发现、事件报告或评估，推导结构性的加固建议，而不是一次性的补丁：归并根本原因，给出加固前后的架构图（ASCII）、带权衡（工作量、风险、效果）的备选方案、实施顺序，以及每项建议的证据。交付一份文档，不修改任何代码。触发词：「怎样从根本上加固」「为什么总是出现这类发现」「让架构更安全」「根据事件制定行动计划」。不用于修复单个发现（sec-fix），也不用于紧急防御（protection-shield）。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, hardening, architecture, root-cause]
language: zh
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-hardening - 从结构入手，而不是逐个修补

当同一类发现反复出现时，原因通常在于结构（没有集中的校验、未经检查的信任边界、代码中的密钥）。本技能在这个层面提出变更建议。契约：`sec-scan/references/contract.md`（发现 §1/§2，规则 4 密钥，规则 5 成本）。

## 输入

`findings.json`（最好是 `validated` 或更靠后的状态）、事件报告、评估、`threatmodel.md` 以及对代码的了解。没有证据支撑的输入，就不提建议；假设要标明为假设。

## 流程

1. **归并根本原因：** 按根源而不是按文件对发现分组，例如「每个路由都自己拼 SQL」「每个 handler 里都重复做访问检查」「配置中包含密钥」。为每一组列出发现的 id。
2. **用 ASCII 图勾画当前架构：** 信任边界、数据流，以及检查目前在哪里发生（或没有发生）。
3. **每个原因对应多个方案**（至少两个，其中包括「只做单个补丁」）：描述、**工作量**、**实施风险**（回归、迁移）、**效果**（哪一类发现会消失，哪些仍然存在）、依赖项。以表格呈现。
4. **每个原因给出建议**，附理由和一幅**目标图**（ASCII），与当前图并列。
5. **顺序：** 什么先做，因为它能一次关闭多个发现或是前置条件；什么可以后做。以及可以单独交付的中间步骤。
6. **每项建议的证据：** 发现的 id、代码位置（`path:line`）、测量数据。没有证据的建议要标明为假设。不要编造以时间计的工作量；只使用相对值（小/中/大），或由用户给出。

## 产出

一份文档（例如扫描目录中的 `hardening.md`，或在聊天中），各节：出发点、原因、当前图/目标图、方案、建议、顺序、待解决的问题。**不修改任何代码**，不生成补丁，不提交任何内容（规则 3）；个别步骤通过 `sec-fix` 或常规开发来执行。文档中不含密钥值（规则 4）。

## 变更日志

### 0.1.0 (2026-10-31)
- 初始版本。
