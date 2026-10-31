---
name: sec-writeup
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "将笔记、PoC 和发现整理成一份可独立阅读、经过审慎检验的漏洞报告，用于协调披露：受影响版本、复现步骤、影响、修复、时间线。PoC 保持最小化（不含武器化的利用代码），密钥已脱敏，每一项声明要么有证据支撑，要么标明未验证。触发词：「撰写披露报告」「漏洞报告」「公告文本」「向维护者报告」。不用于内部的扫描报告（sec-report），也不用于工单（sec-track）。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, disclosure, writeup, advisory, reporting]
language: zh
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-writeup - 用于披露的漏洞报告

一份无需背景知识就能读懂、并且不了解该缺陷的人也能复现的报告。契约：`sec-scan/references/contract.md`（规则 1 自有代码，规则 4 密钥，规则 6 数据外传，规则 9 如实报告）。

## 流程

1. **收集原始材料：** 发现（`findings.json`）、笔记、PoC、补丁。仅限自有代码或明确获得授权的代码中的漏洞（规则 1）。
2. **动笔之前先审慎检验：** 亲自尝试反驳每一项核心声明（「无需认证即可到达」「远程代码执行」「影响所有版本」）。然后把每项声明标记为**有证据**（附证据：代码位置、测试输出、提交）或**未验证**（在文中如此标明）。严重度只使用契约的等级（§3）；CVSS 数值或 CVE 编号只有在用户提供时才使用，绝不自行编造。
3. **根据历史确定受影响的版本**（用 `git log -S`/`git blame` 找出引入时间，用提交/标签确定修复时间），不要估计；不确定的边界要标明为待定。
4. **组织报告结构：** 摘要（2-3 句话）· 受影响的组件与版本 · 攻击者的前提条件 · 复现步骤 · 影响（具体，不夸大）· 修复/缓解措施 · 时间线 · 致谢/联系方式。
5. **最小化 PoC：** 只提供维护者复现所需的内容（输入 + 预期的异常行为）。不提供武器化的利用代码，不涉及目标系统，不做持久化。拿不准时，用描述代替附带代码。
6. **脱敏：** 移除密钥、主机名、内部路径和个人数据；发现只给出位置，绝不给出值（规则 4）。已暴露的密钥须在供应商处轮换。
7. **时间线只使用真实日期**（发现、报告、确认、修复）。披露期限来自用户或 `SECURITY.md`（`sec-policy`），而不是由技能给出。
8. **交付：** 草稿留给用户。发送（邮件、公告、平台）具有外部影响，需要用户的明确批准（规则 6）；对于公开仓库，优先使用公告草稿或私密报告渠道。

## 变更日志

### 0.1.0 (2026-10-31)
- 初始版本。
