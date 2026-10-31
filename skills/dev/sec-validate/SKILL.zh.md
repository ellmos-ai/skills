---
name: sec-validate
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "尝试反驳 findings.json 中的每一个候选项：追踪 source-to-sink 路径，检查可达性与防护措施，校准严重度，在安全的前提下于本地复现。设置 validatedBy（confirmed/refuted/uncertain）以及状态 validated 或 rejected 并附理由。适用于「核实这些发现」「剔除误报」「这真的可被利用吗」「对扫描结果做独立的二次检查」。验证者应与发现者使用不同的供应商。发现新问题：sec-scan。对外部报告分类：sec-triage。报告：sec-report。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, validation, false-positives, exploitability, review]
language: zh
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-validate

ellmos 安全技能家族的第 3 阶段。契约：`sec-scan/references/contract.md`（生命周期 2，严重度 3，规则 6）。校验器：`sec-scan/scripts/secfind.py`。立场：**反驳，而非确认。** 只有当反驳的尝试失败时，候选项才算 `validated`。

## 输入与独立性

- 输入：一次扫描的 `findings.json` + `coverage.json`，即 `status: candidate` 的候选项（或用户指定的一组 `id`）。
- **独立的验证者（契约 6.7）：** 最好使用与扫描的 `provider.name` 不同的供应商（Claude <-> Codex）。若做不到：使用最高模型级别的独立子代理，它在此之前**不得**阅读发现者的推理过程，并在结果中记录这一点。涉及多个供应商或扇出：先估算成本并警告用户（6.5）。若代码会发送给第三方供应商，须说明数据外传（6.6）。
- 预检同 `sec-scan` 步骤 2（所有权、锁检查，失败即关闭）。

## 针对每个候选项

1. **重新阅读：** 亲自阅读 `location` 处的代码；发现者的 `evidence` 仅作提示。
2. **追踪路径：** source -> 转换 -> sink，每一步都附 file:line。链条中断即为反驳的理由。
3. **可达性：** 哪条路由、调用方或认证方式通向这里？死代码、测试代码、仅管理员可达的路径以及内部调用方，会降低严重度或构成反驳。
4. **查找防护措施：** 校验、转义、参数化查询、框架保护、配置、上游检查、权限。也要看其他位置（中间件、包装层）。
5. **说明攻击者的前提条件**（匿名、账户、本地访问、特定配置）。
6. **在安全时复现：** 仅限本地副本或测试环境，使用合成数据和桩服务；例如针对性的单元测试，或用攻击输入调用该函数。**绝不**针对第三方或生产系统，不得访问外部网络，不得使用真实密钥，不得造成破坏。若无法安全复现，静态论证即可，结论 `uncertain` 是允许的。
7. **依据契约 3 校准严重度**（可达性乘以影响）；重新设定 `confidence`。变更在 `description` 中记为「severity 旧 -> 新：理由」。
8. **写下结论：**

| 结论 | 在 `findings.json` 中的后果 |
|---|---|
| `confirmed` | `status: validated`，`validatedBy: {provider, model, verdict: confirmed}`；路径及任何复现写入 `description`；补充 `impact` 与 `recommendation` |
| `refuted` | `status: rejected`，`rejectedReason` 写明具体的防护措施或链条的断点，`validatedBy.verdict: refuted` |
| `uncertain` | `status` 保持 `candidate`，`validatedBy.verdict: uncertain`，`description` 说明做出判断还缺什么 |

`validatedBy.provider` / `.model` 是**验证者**，而不是发现者。与发现者相同的供应商会触发验证者警告「validated by the same provider」；该警告保持可见，不得压制。

## 收尾

`python sec-scan/scripts/secfind.py validate findings.json coverage.json`，展示退出码。摘要：每种结论的数量、严重度变更、仍未解决的 `uncertain`。继续进行 `sec-triage`（已验证的发现）与 `sec-report`。`description` 或复现输出中不得出现密钥值（契约 6.4）。不打补丁，不提交。

## 变更日志

### 0.1.0 (2026-10-31)

- 首个版本：反驳流程、结论映射、独立性。
