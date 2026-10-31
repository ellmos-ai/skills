---
name: sec-report
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "通过脚本 render_report.py，根据 findings.json 与 coverage.json 生成安全报告 report.md（按严重度分组、含列出缺口的覆盖范围一节、被驳回的发现单独列出、不粉饰的摘要）以及 findings.sarif（SARIF 2.1.0）。适用于「撰写安全报告」「总结扫描结果」「导出 SARIF」「用于 code scanning 的报告」。数据无效时中止；部分扫描会如实报告为部分扫描。新发现：sec-scan / sec-diff-scan。验证：sec-validate。分类：sec-triage。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, report, sarif, coverage, findings]
language: zh
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-report

ellmos 安全技能家族的最后阶段。契约：`sec-scan/references/contract.md`（文件 1，严重度 3，覆盖范围 5，规则 6）。该脚本从同级文件夹 `sec-scan/scripts` 导入 `seclib`（在仓库的 `skills/dev/` 中，以及在扁平部署的 `~/.claude/skills/` 中；两个文件夹必须并排放置）。仅使用标准库。

## 用法

```
python scripts/render_report.py FINDINGS COVERAGE OUTDIR [--lang de|en]
```

须显式调用解释器。`OUTDIR` 是扫描目录；先按 `sec-scan` 步骤 2 检查锁（失败即关闭）。结果：`OUTDIR/report.md` 与 `OUTDIR/findings.sarif`。退出码：0 = 已写入，1 = 输入无法读取或无效（**不写入任何内容**），2 = 用法错误。展示退出码与输出。报告默认语言为德语；使用 `--lang en` 可得到英文。

## 行为

- **先校验**（`seclib.validate_findings`）。列出错误，并且不会基于损坏的数据生成报告。先修复原因（`sec-scan`、`sec-validate`），再重新渲染。
- **report.md：** 标题部分（目标、ref、扫描器）· 摘要 · 警告 · 按严重度（从 critical 到 info）排列的发现，含位置、置信度、状态、验证者、证据、描述、影响、建议、工单 · **被驳回的发现单独列出**并附理由 · 覆盖范围（已扫描及其深度、未扫描及其原因、局限）。
- **诚实性（契约 5、6.9）：** `complete: false` 会作为「PARTIAL SCAN」出现在最顶部。没有发现但覆盖不完整时，会写明「NOT a clean result」。只有「覆盖完整且没有发现」才可以读起来像一份干净的结果。警告（例如发现者与验证者使用同一供应商）会出现在报告中。
- **findings.sarif：** 由 `seclib.to_sarif` 生成的 SARIF 2.1.0；被驳回的发现以 `suppressions` 的形式保留在日志中。可直接用作 code scanning 的上传文件。上传属于对外发布，需要用户下达指令。

## 交出之前

回读报告：不含密钥值（校验器只能识别常见模式；契约 6.4），只给出位置。工单系统和聊天中的报告同样不含值。公开仓库中的漏洞走私密报告渠道（SECURITY.md），而不是公开 issue。

## 测试

在技能文件夹中运行 `python -m pytest tests -q -p no:cacheprovider`（覆盖报告、SARIF、部分扫描、反引号证据，以及无输出的负面用例）。

## 变更日志

### 0.1.0 (2026-10-31)

- 首个版本，附带 `render_report.py`：由已验证的数据生成 report.md 与 findings.sarif。
