---
name: sec-fix
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "仅在明确请求时，为已确认的发现（状态 validated 或 triaged）生成最小化的安全补丁：在临时副本或 worktree 中进行，绝不在原始仓库中，输出为 patches/<id>.diff，不应用、不提交、不推送。触发词：「修复这个发现」「SEC-... 的补丁」「关闭这个漏洞」。不用于普通的缺陷修复（使用 bugfix-protocol），不用于评判补丁（sec-verify-fix），不用于发现问题（sec-scan）。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, patch, fix, remediation]
language: zh
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-fix - 最小化安全补丁

ellmos 安全技能家族的「fix」阶段。契约：`sec-scan/references/contract.md`（目录 §1，生命周期 §2，规则 §6）。此处只描述其应用方式。

## 何时使用（以及何时不用）

- **仅在明确请求时。** 扫描或验证本身绝不会自动触发修复。
- **仅针对状态为 `validated` 或 `triaged` 的发现。** `candidate` 先经过 `sec-validate`；`rejected` 保持原样。
- 普通的非安全缺陷：`bugfix-protocol`。已有补丁好不好：`sec-verify-fix`。多个发现背后的结构性原因：`sec-hardening`。

## 流程

1. **阅读发现及其周边：** `findings.json`（发现、`evidence`、`recommendation`）、受影响的文件以及该位置的调用方。修复原因，而不是某一个调用点上的症状；如果多个调用方使用同一个不安全的函数，就修补共用的那一处。
2. **检查锁（契约 §6 规则 2）：** `lock_scan.py --check-dir <repo> --json`；退出码 0 = 空闲，1 = 已锁定，其他任何结果 = 未知 = 停止；在没有 `lock_scan.py` 的主机上，改为在仓库及其上级文件夹中搜索 `LOCK*.txt`（没有 = 空闲，否则停止）。绝不触碰 `LOCK.user.*`。
3. **工作副本：** 在原始仓库之外的文件夹中建立临时副本或 `git worktree`。不向原始仓库写入任何内容。
4. **测量基线：** 在打补丁之前先运行一遍项目测试并记录结果（绿/红、数量）。若没有测试，就如实说明，不要凭空编造。
5. **最小化修补：** 以能够切断 source-to-sink 路径的最小改动为准（校验、参数化、允许列表、在正确位置转义）。不重构、不改风格、无必要不引入新依赖。如果项目有测试，则针对该发现的回归测试应包含在补丁中。
6. **再次测量：** 重新运行测试；如实报告前后对比，包括失败的测试和未运行的测试。
7. **保存补丁：** 将工作副本的 `git diff` 保存到扫描目录中的 `patches/<id>.diff`；用 `git apply --check` 对照目标状态检查（不会改变任何内容）。
8. **更新发现：** `status: fixed`，`fix.patchFile: patches/<id>.diff`；然后运行 `python scripts/secfind.py validate findings.json coverage.json`（该脚本位于 `sec-scan`）。

## 限制

- **不应用、不提交、不推送（规则 3）。** 这些需要用户的直接指令。
- **涉及密钥的发现：** 旧值必然会出现在 diff 的 `-` 行中。补丁只保留在扫描目录本地，绝不放入工单、聊天或报告；先在供应商处轮换该密钥（规则 4）。待定：经过遮蔽的 diff 是否仍然可以有效应用，不要臆造。
- 补丁的作者不能审查它：由不同的审查者执行 `sec-verify-fix`（规则 7）。
- 一次修复多个发现时给出成本警告（规则 5）；按顺序逐个处理。

## 变更日志

### 0.1.0 (2026-10-31)
- 初始版本。
