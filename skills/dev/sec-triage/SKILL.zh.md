---
name: sec-triage
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "将已有的发现（扫描器报告、SARIF、GitHub code scanning、Dependabot、工单）转换为 ellmos 安全家族的 findings.json 格式，按 id 去重，依据仓库的安全策略（SECURITY.md）设定严重度与优先级，并关联工单。仅做静态评估。适用于「对这些扫描结果分类」「给 Dependabot 告警排优先级」「导入 code scanning 发现」「整理安全发现的积压」。发现新漏洞：sec-scan。反驳或复现：sec-validate。报告：sec-report。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, triage, sarif, dependabot, code-scanning, prioritisation]
language: zh
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-triage banner">

# sec-triage

ellmos 安全技能家族的第 4 阶段。契约：`sec-scan/references/contract.md`（文件 1，生命周期 2，严重度 3，id 4，规则 6）。校验器：`sec-scan/scripts/secfind.py`。**仅依据静态证据：** 不做新的发现（`sec-scan`），不做运行时验证（`sec-validate`）。

## 输入

已有的发现：SARIF 文件或扫描器报告、GitHub code scanning 与 Dependabot（通过 `gh` 或从网页界面导出，注意数据外传）、工单、审计清单。若已存在 `findings.json` 则续用，否则新建（扫描目录依契约 1）。预检同 `sec-scan` 步骤 2（所有权、锁检查，失败即关闭）。

## 流程

1. **映射：** 每条来源发现对应一个条目。将 `rule` 规范化为点分小写（`py.sql-injection`；原始规则标识符与来源写入 `description`），`cwe` 取自来源的标签，`location` 取自告警，`severity` 起初沿用来源给出的值，`status: candidate`。
2. **固定证据：** 取告警中的代码片段，否则读取所指文件中的该位置并引用。若无法获得证据（文件缺失、行号已移动、告警不含代码），**不要**用编造的证据导入该发现；把它作为未导入列入 `coverage.limits` 并说明原因。遮蔽密钥值（契约 4）。对于依赖告警：`rule` 例如 `dep.vulnerable-dependency`，`location` = manifest/lockfile 中的那一行，`evidence` = 该行；公告 id 与受影响版本写入 `description`。
3. **去重：** 通过 `python sec-scan/scripts/secfind.py id RULE PATH -` 生成 `id`。相同的 `id`（包括来自多个来源的）合并为一条发现，并在 `description` 中列出各来源；严重度不一致时取较高者并注明。
4. **阅读策略：** `SECURITY.md`（严重度定义、期限、受支持版本、报告渠道）以及项目已有的决定。若没有，则适用契约 3，并在结果中说明。
5. **设定严重度与优先级：** 对照策略核查严重度，并附理由进行调整；由严重度、暴露程度和期限推导优先级，写入 `priority`（`P0`-`P4`，P0 最紧急；把策略中的等级映射到此），理由写入 `description`。
6. **状态：** 依据校验器，`triaged` 要求 `validatedBy.verdict == confirmed`。已验证（`validated`）的发现变为 `triaged`。已导入但尚未验证的发现保持 `candidate`，设定好严重度/优先级，然后交给 `sec-validate`。仅当策略明确涵盖时才予以排除（例如不受支持的版本）：`rejected` 并附 `rejectedReason`。
7. **工单：** 仅当用户或策略要求时：`ticket_writer.py`（绝不手选 id）或 GitHub issue/草稿公告；公开仓库中的漏洞应作为**私密**的公告草稿，而不是公开 issue。把引用记入 `ticket`。工单中不得出现密钥值（契约 6.4）。
8. **覆盖范围：** 纯导入不扫描任何内容。`scanned: []`，`notScanned` 加一条「import without own scan, repo not read」（因此 `complete: false`），`limits` 写明来源、导入状态以及未导入的发现。`provider.name` = 来源（例如 `github-code-scanning`），`model` = `n/a`，`engine` = 来源工具。
9. **检查：** `python sec-scan/scripts/secfind.py validate findings.json coverage.json`，展示退出码。然后用 `sec-validate` 处理候选项，用 `sec-report` 生成报告。

## 变更日志

### 0.1.0 (2026-10-31)

- 首个版本：导入、按 id 去重、依策略分类。
