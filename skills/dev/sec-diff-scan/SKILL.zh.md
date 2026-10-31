---
name: sec-diff-scan
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "对一次变更而不是整个仓库做安全扫描：PR、提交、分支差异或工作区补丁。连同调用方与被调用方一起审查改动的行，查找已知模式的回归，并将候选项写入 findings.json，同时输出列出 diff 文件与上下文文件的 coverage.json。适用于「对这个 PR 做安全审查」「检查这个 diff 有没有漏洞」「合并前看一下」「这次改动有没有打开什么口子」。整仓库扫描：sec-scan。反驳候选项：sec-validate。报告：sec-report。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, scan, diff, pull-request, regression, review]
language: zh
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-diff-scan

与 `sec-scan` 相同，只是范围为一次**变更**。契约、文件格式与规则：`sec-scan/references/contract.md`；模式（schema）与校验器位于 `sec-scan/schemas/` 与 `sec-scan/scripts/`。预检（所有权、锁检查、数据外传、成本）、候选项构造（通过 `secfind.py id` 生成 `id`，遮蔽密钥）以及校验，均与 `sec-scan` > 流程 相同。此处仅列出差异。

## 确定范围

下列来源之一，并始终给出精确的比较基点：

- PR：该 PR 的 base 与 head 提交（本地使用 `git diff <base>...<head>`，或用 `gh` 拉取该 PR；注意数据外传）。
- 提交或分支：`git diff <base>...<branch>`。
- 工作区：`git diff` 与 `git diff --staged`，再加上未跟踪的文件。

`findings.json` > `target.ref` = head 提交（或 `working-tree`），`target.scope` = diff 涉及的文件。若 diff 为空，则中止并说明。

## 流程（代替 sec-scan 的步骤 3-5）

1. **阅读 diff**，而不只是 hunk：每个被改动的文件都要放在所涉函数的上下文中阅读。
2. **引入上下文：** 被改动函数的调用方（谁传入输入？）、被调用方（数据流向哪里？）、记录了假设的配置与测试。若存在 `threatmodel.md` 则使用；否则只需简要自行确定被触及的信任边界（不做完整模型，那是 `sec-threat-model` 的事）。
3. **针对变更的审查问题：**
   - 是否出现新的入口点或新的 sink（shell、SQL、文件系统、反序列化、HTTP 客户端）？
   - 是否有检查被移除、削弱或绕过（认证装饰器、校验、转义、权限检查）？
   - 已知模式的回归：与先前发现或仓库其他位置属于同一类缺陷（若有现成的 `findings.json`，参考其中的 `rule` 值）。
   - manifest/lockfile 中的新依赖或版本变更；变更中的密钥或令牌；配置被进一步放宽（CORS、调试、权限）。
4. **仅当路径确实到达被改动或被触及的位置时才报告发现。** 与变更无关、早已存在于上下文中的缺陷：按契约 3 记录其真实严重程度，并在 `description` 中注明「早已存在，并非本次改动引入」（不要降级为 `info`）；若未经核实，则仅写入 `coverage.limits`；它们不是该 diff 的审查对象。

## 覆盖范围

`coverage.json`：`scanned` = diff 文件（深度通常为 `read`）**以及**额外读取的上下文文件，`notScanned` = 未读取的 diff 文件（二进制、生成文件、过大），并附原因。`limits` 写明：「仅限变更，仓库其余部分未扫描」。`complete` 依据契约 5。一次没有发现的 diff 扫描，并不能说明整个仓库的情况。

## 范围限制

不做整仓库扫描（`sec-scan`），不做运行时检查（`sec-validate`），不做修复。产出：`findings.json`、`coverage.json`、`secfind.py validate` 的退出码。

## 变更日志

### 0.1.0 (2026-10-31)

- 首个版本：变更范围、上下文引入、回归问题。
