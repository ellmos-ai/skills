---
name: sec-track
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "让已验证的安全发现可追踪：先预览并经确认，再创建工单（ticket_writer.py）、GitHub issue 或安全公告草稿（gh），先按发现 id 检查重复，不让密钥进入文本，并把引用写回 finding.ticket。触发词：「跟踪这个发现」「为 SEC-... 建工单」「创建公告」「把发现放进待办积压」。不使用 Linear/Jira。不用于技术报告（sec-report），也不用于对外披露（sec-writeup）。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, tickets, tracking, github, advisory]
language: zh
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-track - 让发现可追踪

「track」阶段。契约：`sec-scan/references/contract.md`（规则 4 密钥，规则 8 工单，位于 §6；字段 `ticket` 见 `schemas/finding.schema.json`）。仅针对状态为 `validated` 或更靠后的发现，`candidate` 不予跟踪。

## 选择目标

| 目标 | 何时使用 | 工具 |
|---|---|---|
| 用户工单系统中的工单 | 默认，私密，无外部影响 | ticket-master 的 `ticket_writer.py` |
| GitHub issue | 仅限**私有**仓库，或没有利用路径的纯加固缺口 | `gh issue create` |
| 安全公告草稿 | **公开**仓库中的漏洞 | `gh api`（仓库安全公告，草稿） |

**公开仓库 + 可被利用的发现：绝不创建公开 issue**，那会构成披露（数据外传，规则 6）。在这种情况下使用公告草稿或私密工单。不使用 Linear，不使用 Jira。

## 流程

1. **选择：** 哪些发现、哪个目标。逐条处理，而不是做成一个批量工单，使每个 id 都有各自的引用。
2. **按发现 id（`SEC-<12 hex>`）检查重复：** `finding.ticket` 是否已设置？在工单目录中搜索该 id；在 GitHub 上用 `gh issue list --state all --search "<id>"`。如有命中，使用已有的引用，不新建。
3. **起草文本：** id、标题、rule/CWE、严重度、位置（`path:line`）、简短的影响、建议，以及（如果有）指向补丁文件的指引。**绝不写密钥值**（规则 4）：只写位置。除必要之外，不写利用细节。
4. **展示预览并等待确认。** 之后才创建，因为工单、issue 和公告具有外部影响或无法撤回。
5. **创建：**
   - 工单（绝不手选 ID，规则 8）：`python <ticket-master>/lib/ticket_writer.py --title "<SEC-id> <title>" --body "<text>" --project <project> --priority <level>`；该 CLI 会打印所创建工单文件的路径。模块文档有时写作 `--urgency`；CLI 本身认的是 `--priority`，使用前先阅读 `--help`。
   - Issue：`gh issue create --repo <owner/repo> --title ... --body-file <file>`。
   - 公告：通过 GitHub 针对仓库安全公告的 REST 接口（`gh api`）创建草稿；使用前对照 GitHub 文档核对确切的字段（待定，此处不做定论）。保持为草稿，不要发布。
6. **写回引用：** `finding.ticket` = 工单路径/id、`owner/repo#nr` 或公告链接；然后运行 `python scripts/secfind.py validate findings.json coverage.json`（脚本位于 `sec-scan`）。

## 变更日志

### 0.1.0 (2026-10-31)
- 初始版本。
