---
name: pingpong
version: 1.1.0
type: protocol
author: Lukas Geiger, OpenAI Codex
created: 2026-08-03
updated: 2026-09-13
description: "通过共同同步的文件夹运行一个有时间限制、与会话绑定的电台。ListenSync 系统性地扫描任务与最新动态；WriteSync 发送增量与回执。适用于 PingPong、Dosentelefon（罐头电话/对讲）、ListenSync、WriteSync、Sync-Listener（同步监听器）、Auftragswache（任务监视）、News-Scan（新闻扫描）或 Goal-/Loop-Überwachung（Goal/Loop 监控）等场景。"
# Kompatibilität
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: infrastructure
tags: [pingpong, sync, listener, goal, loop, cadence, filecommander]
language: zh
status: active
visibility: public

# Abhängigkeiten
dependencies:
  tools: [ellmos-filecommander]
  services: []
  protocols: [shared-folder-sync]
  python: []

roles:
  - id: pingpong
    label: PingPong
    prompt: skills/infrastructure/pingpong/SKILL.en.md
    request: Read and follow the PingPong protocol for the requested mode and duration.
    modes: [ListenSync, WriteSync]
    providers: [codex, claude]

# Provenance
provenance:
  origin: "custom"
  origin_path: "local-skill/pingpong"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-08-04"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 6f644ddfdc91c21a6250f7af08b78211b2949ad989b2e2f9104d71bed1ef062b
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="pingpong banner">

# PingPong

将两个或更多系统作为电台，通过共同的同步文件夹运行。保持业务契约与提供方无关；只有延续适配器有所不同。

## 确定模式

- ListenSync：每台主机恰好一个系统性监听器。它进行扫描，接收匹配的任务，并在收到回复时同时执行 WriteSync。
- WriteSync：每个工作中的参与者都可以发送自己相关的增量、任务、最新动态和回执。此模式不启动监听器。
- 若未指定模式，则使用 ListenSync。

## 澄清参与状态（STATE 与 CALL）

在运行契约之前，通过两阶段检查确定是否有人可以联系。`scripts/pingpong_runtime.py check --slot <slot> --sync-root <pfad>` 恰好返回三个值：退出码 0 `call-for-me`（激活并生成一个代理）、退出码 1 `idle`（我本人处于活动状态，停用）、退出码 3 `check-failed`（不可读，切勿视为空闲）。参与需要同时具备 STATE 与 CALL；发起呼叫者在目的达成时结束它，否则它将过期。完整规则见 references/protocol.md。

## 设定运行契约

1. 默认使用 24h。也接受相对时长，如 15m、2h、3d，或绝对的 ISO-8601 结束时间点。
2. 测量本地开始时间，并以日期、时间与时区给出 expires_at。
3. 从 15 分钟开始。除非用户要求固定节奏，否则使用 references/protocol.md 中的节奏。
4. 将目标达成定义为：达到结束时间，FileCommander 的最终扫描有据可查，截至该时间检测到的所有匹配输入均已处理或被精确阻塞并记录，状态已更新，且自身调度器已结束。
5. 没有 FileCommander 证据时，不得声称已扫描或已达成目标。

## 使用提供方适配器

### Codex

在首次扫描之前，明确创建一个持久化的 Goal，包含完整的运行契约与 expires_at。每次延续只执行一个完整的扫描周期。不得在空的或成功的单次周期之后结束 Goal。之后真实等待至 next_scan_at，例如：

    python "<skill-root>/scripts/pingpong_runtime.py" wait --until "<next_scan_at>"

在到期时间执行结束周期。只有满足成功标准时，才将 Goal 标记为已完成。

### Claude Code

以 /loop <Kadenz> $pingpong 的形式启动任务。若该技能已来自计划运行，则不要再创建第二个 loop。节奏变更时，仅替换自身的 Cron 任务。在结束周期之后将其删除。

## 执行周期

完整阅读 references/protocol.md，并恰好执行其中描述的一个扫描、处理与状态周期。对同步文件夹的每次访问都使用 ellmos FileCommander。仅凭 Shell 列表、调度器条目或文件名不构成扫描证据。

空闲时不要虚构工作。简要报告：扫描时间、已读取的新鲜度文件、当前节奏、empty_runs、next_scan_at 与 expires_at。

## 执行 WriteSync

只写入自己的系统槽位或明确声明的全局通道。注明发送者、接收者、时间、关联、动作、结果、未决事项以及期望的节奏。合并而非覆盖；不得包含凭据；遵守锁定。写入后使用 FileCommander 回读规范文件。

## 变更日志

### 1.1.0 (2026-09-13)

- 新增主机相关的参与标记 STATE（字段 `pingpong` 位于 `agents/registry/<slot>.state.json` 中）以及带过期机制的定向 CALL 文件 `call-<von>-to-<an|all>.txt`；为此 `pingpong_runtime.py` 引入 `state`、`call` 以及具有三值结果的两阶段检查 `check`。旧的 `pull-` 名称在过渡期内仍可读取。依据 2026-09-11 的用户决定实施 T-20260830-425388998（最小化改动：仅 STATE、CALL 与过期机制）。

### 1.0.1 (2026-09-09)

- 依据可选的 Modul-v2 角色契约新增声明式角色元数据；没有中立启动器声明角色。既有协议身份与发现路径保持不变。

### 1.0.0 (2026-08-04)

- 提供方无关的 ListenSync/WriteSync 契约，附带 Codex Goal 与 Claude Loop 适配器。
- 新增 FileCommander 证据、新鲜度防护、自适应节奏与绝对过期条件。
