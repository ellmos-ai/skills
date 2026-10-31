---
name: backup
version: 1.0.0
type: skill
author: User
created: 2026-08-24
updated: 2026-08-24
description: "通过 fail-closed 的 mac-backup 核心，明确地创建、镜像、验证、恢复或归档文件。用于用户自己的跨主机备份作业；不用于通用云同步或随意的文件复制。"
visibility: public
language: zh
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance:
  origin: "custom"
  origin_repo: "github.com/ellmos-ai/mac-backup"
  last_sync_from_origin: "2026-08-24"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: c50a9f8b557b5e4baa08f880f28ba234c8f56974e644ce57147bde5311a02ad6
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T15:41:56.704466+00:00"
---
<img src="banner.png" width="100%" alt="backup banner">

# 备份

仅使用已安装的 `mac-backup` CLI 作为唯一的传输实现。不要使用原始的 `scp`、`rsync`、SSHFS、资源管理器操作或临时删除来重建流程。

## 请求路由

- 普通的"备份"请求表示 `mirror`；源文件保持不动。
- `archive` 表示清理源文件，是一个单独的、具有破坏性的意图。绝不要从"backup"（备份）、"copy"（复制）或"free some space"（释放一些空间）中推断出它。
- `restore` 写入一个新的目标，且绝不静默覆盖。
- 如果不存在经过检查的作业 JSON，请先准备作业提案，并在 `init-target` 或传输之前暂停。

## 执行

1. 读取作业并运行 `mac-backup plan <job> --json`。
2. 检查返回的源类别、文件数量、字节数、目标卷 ID、加密状态和主机指纹，是否与请求以及当前设备凭证一致。
3. 对于镜像，运行 `mac-backup mirror <job> --json`，然后运行 `mac-backup verify <job> --json`。
4. 对于恢复，使用新的绝对路径作为目标，并通过命令的清单结果验证已恢复的文件。
5. 仅当用户明确要求移除源文件，且经过检查的计划恰好指明该源时，才为归档传递 `--confirm-delete`。策略阻止是正确的结果；绝不绕过 `target_encryption_required`、`source_class_unknown_cleanup_blocked`、`onedrive_dehydrate_not_implemented`、锁、身份不匹配或缺失的锚点。

`init-target` 是特权设置，而非常规执行。它需要独立获取的卷 ID 和加密状态的操作系统凭证；从提议作业中复制的值不算凭证。

在目标验证和真实恢复测试都通过之前，绝不要声称镜像就是完整备份。请将密钥、真实作业文件、本地锚点以及来自工单、Git 和 OneDrive 的用户文件名排除在外。

## 更新日志

### 1.0.0 (2026-08-24)
- 将 `~/.claude/skills/backup/` 部署主版本的中立副本纳入分类库。同步缺口的原因：该 Skill 已部署，但在 `skills/<category>/` 下没有源条目，因此 `skill_sync.py status` 将其报告为 `NUR-ZIEL`（仅目标），而仅扫描 `skills/` 的 `catalog.py`/`build_public_registry.py` 从未看到它——因此无论如何编辑部署副本，它都无法到达公共注册表或 `SKILLS-MAP.md`。
