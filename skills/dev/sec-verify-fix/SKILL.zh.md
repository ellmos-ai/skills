---
name: sec-verify-fix
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "独立检查安全补丁是否真正堵住了漏洞（在已打补丁的状态下重新追踪 source-to-sink 路径，做反向测试与回归测试），评估回归风险，以及自动合并是否站得住脚（对 critical/high 默认不允许）。只读审查，不应用任何内容。触发词：「补丁是否堵住了漏洞」「审查这个补丁」「验证这个修复」，以及状态为 fixed 的发现。不用于编写补丁（sec-fix），也不用于一般的代码审查。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, patch, review, verification, regression]
language: zh
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-verify-fix banner">

# sec-verify-fix - 补丁堵住漏洞了吗？

「verify-fix」阶段。契约：`sec-scan/references/contract.md`（生命周期 §2，规则 7 位于 §6）。要求发现的状态为 `fixed` 且带有 `fix.patchFile`。

## 独立性优先

审查者**不是**补丁的作者（规则 7）：最好使用另一个供应商（Claude <-> Codex）；否则使用一个全新上下文的独立顶级子代理，它只收到发现、补丁和代码，而不收到作者的推理过程。如果无论如何只能自己检查，要在结果中说明；此时 `verifiedBy` 保持为空，状态保持 `fixed`。

## 流程

1. **在临时副本中应用补丁**（绝不在原始仓库中）；像 `sec-fix` 那样检查锁（规则 2）。如果补丁无法干净地应用，那本身就是结果。
2. **重新追踪路径：** 在已打补丁的状态下，逐行走一遍 `evidence` 中原来的 source-to-sink 路径。sink 仍然可达吗？是否存在补丁未覆盖的并行路径（其他调用方、输入变体、其他编码）？
3. **反向测试：** 之前会触发该发现的、最小化且不具武器化的输入，现在必须被拒绝或被中和。仅限临时副本，仅限自有代码（规则 1）。如果无法合理地运行测试，就报告为「not tested」。
4. **回归测试：** 对比补丁前后的项目测试；合法输入仍然有效。指出失败或未运行的测试。
5. **评估回归风险：** 受影响的运行时路径和调用方、被改变的约定（签名、格式、错误行为）、该位置的测试覆盖、可逆性（纯代码补丁 vs. 数据迁移/配置）。给出低/中/高的级别并说明理由。
6. **能否自动合并？** 是/否并说明理由。**对 critical/high 默认为否**；只有路径已堵住、反向测试与回归测试均通过、风险低且回滚简单时才为是。审查者绝不单独做决定；以仓库的合并规则为准。

## 结果

- **是否堵住：** 是 / 部分 / 否，并指出仍未堵住的具体位置。结论为「否」或「部分」时，状态保持 `fixed`，工作回到 `sec-fix`；该发现不会被丢弃。
- **结论为「是」时：** `status: verified`，`fix.verifiedBy: "<provider>/<model>"`，并运行 `python scripts/secfind.py validate findings.json coverage.json`（脚本位于 `sec-scan`）。理由、风险级别和合并建议写入给用户的报告；契约中没有对应的字段，所以不要自造字段。
- 不应用、不提交、不推送任何内容（规则 3）。

## 变更日志

### 0.1.0 (2026-10-31)
- 初始版本。
