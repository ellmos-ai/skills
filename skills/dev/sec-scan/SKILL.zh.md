---
name: sec-scan
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "对自有代码仓库做与供应商无关的安全扫描：威胁模型、按信任边界拆分、逐包定向审查（注入、认证/授权、密钥、加密、反序列化、路径、SSRF、配置、已知漏洞依赖的使用方式），将带证据的候选项写入 findings.json，并给出如实的 coverage.json。提供 standard 与 deep 两种模式。适用于「安全扫描」「检查这个仓库有没有漏洞」「安全审查」「完整扫描」「把扫描器结果导入 ellmos 格式」。包含 /claude-security 与 codex-security 的适配器。仅针对变更/PR：sec-diff-scan。反驳候选项：sec-validate。导入外部报告：sec-triage。报告：sec-report。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, scan, vulnerabilities, sast, source-to-sink, cwe]
language: zh
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-scan

ellmos 安全技能家族的核心。共享契约（阶段、文件、生命周期、严重度、规则、适配器）位于 `references/contract.md`，模式（schema）位于 `schemas/`，校验器位于 `scripts/secfind.py` + `scripts/seclib.py`（仅使用标准库）。本技能引用该契约而不重复其内容。相邻技能：`sec-threat-model`、`sec-diff-scan`、`sec-validate`、`sec-triage`、`sec-report`。

## 模式

- **standard：** 一轮、一个模型、一个会话。
- **deep：** 多轮相互独立的扫描（不同的包顺序、拆分方式或模型），按 `id` 合并。须先给出成本警告并经用户确认（契约 6.5）。

## 流程

1. **目标与范围：** 仓库、ref（提交 SHA 或 `working-tree`）、排除路径。分配一个 `scanId`。扫描目录命名为 `sec-scan-<scanId>/`（契约 1），位于**仓库之外**的基础文件夹下，且仅在预检之后创建。
2. **预检：**
   - 是自有代码或已获授权的代码吗？否则中止（契约 6.1）。
   - 对仓库及扫描目录所在的基础文件夹做锁检查：`python <lock_scan.py> --check-dir '<path>' --json`，并立即记录退出码。0 = 空闲，1 = 已锁定，其他任何结果（崩溃、输出不可读）= 未知 = 停止（契约 6.2）。须显式调用解释器，绝不要「打开」脚本。如果本主机上不存在 `lock_scan.py`（没有 ellmos 锁系统），则改为在仓库及其上级文件夹中搜索 `LOCK*.txt`：没有 = 空闲（在报告中注明），有一个或多个 = 停止。
   - **说明数据外传情况：** 代码是否会发送给某个供应商（托管的审查层、第三方模型）？私有仓库只留在本地会话中（契约 6.6）。**说明成本**，对 `deep` 须等待确认（6.5）。
3. **威胁模型：** `threatmodel.md` 是否存在且是最新的？若否，先运行 `sec-threat-model`。
4. **划分包：** 依据模型中的信任边界与入口点拆分仓库；每个包列出文件与调查问题。非常大的包要继续拆分，而不是草草浏览。
5. **逐包审查**（source-to-sink：source -> 转换 -> sink，同时阅读路径上的防护措施）：
   注入（SQL、shell、模板、LDAP/NoSQL）、认证/授权与租户隔离、代码中的密钥、加密（算法、随机性、密钥处理）、不安全的反序列化、路径/文件访问（路径穿越、上传、符号链接）、SSRF 与开放重定向、不安全的配置（调试、CORS、默认值、权限）、已知存在漏洞的依赖的使用（代码中的模式；公告匹配属于 `security-tech-stack-check`）。路径无法支撑的发现不予记录；没有证据的怀疑应写入 `coverage.limits`，而不是 `findings`。
6. **记录候选项：** `rule` 为点分小写（`py.sql-injection`），适用时填写 `cwe`，`severity` 与 `confidence` 依据契约 3，`status: candidate`，`location`，`evidence` 为引用的代码/调用轨迹。**遮蔽密钥值**（契约 4）。`id` 一律通过 `python scripts/secfind.py id RULE PATH -`（片段经 stdin 传入）生成，绝不手写。
7. **如实记录覆盖范围：** `scanned` 标注深度 `read` / `skimmed` / `pattern-only`，`notScanned` 附原因（生成文件、第三方引入的代码、过大、二进制、不可达），`limits` 记录方法上的局限。仅当 `notScanned` 为空时才可设 `complete: true`（契约 5）。`unknown` 不等于「安全」。
8. **校验：** `python scripts/secfind.py validate findings.json coverage.json`，展示退出码（0/1）与输出。有错误时修正后重跑。
9. **收尾：** 按严重度统计候选项数量、覆盖状态、后续步骤（`sec-validate`，然后 `sec-triage`、`sec-report`）。部分扫描须如实报告为部分扫描（契约 6.9）。

## deep

至少两轮、拆分方式不同，各自有独立的候选列表。按 `id` 合并：相同 `id` 合并（补充证据；严重度不一致时取较高者，并在 `description` 中说明差异），新 `id` 则加入。覆盖范围 = 所读路径的并集；`provider.model` 列出所有参与的模型。

## 适配器

已有的供应商扫描器可以接管扫描部分（契约 7）：**Claude** `/claude-security`，**Codex** `codex-security`。Gemini 与 Kimi 没有，按上述流程进行。

1. 预检（步骤 2）之后运行扫描器；读取其输出文件，并逐字段映射到 `findings.json` / `coverage.json`。此处不预设扫描器的文件与字段；映射在阅读实际输出时建立，并记录在 `coverage.limits` 中。
2. **所有发现都以 `candidate` 开始**，即使扫描器将其报告为已确认。适配器绝不跳过验证。
3. 扫描后设置 `provider.name` / `provider.model`，`provider.engine` = 扫描器名称。
4. 覆盖范围取自扫描报告。若报告未提供，则设 `complete: false`，并在 `notScanned` 中添加一条「扫描器覆盖范围未知」（校验器会拒绝 `notScanned` 为空的 `complete: false`；仅有 `limits` 不够）。
5. 通过 `secfind.py id` 重建 `id`，使发现与其他运行的结果一致。然后执行步骤 8。

## 限制

不打补丁、不提交、不做网络扫描（契约 6.1、6.3）。不做运行时利用；复现属于 `sec-validate`。

## 变更日志

### 0.1.0 (2026-10-31)

- 首个版本：standard/deep 模式、预检、包划分、适配器。
