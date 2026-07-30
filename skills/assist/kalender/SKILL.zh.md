---
name: kalender
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: 适配用户首选后端的日历 Skill（Flag 3）。默认：本地 SQLite 存储。可选：Google Calendar MCP、Routinika 或 UpToday 作为后端 —— 通过 assist/prefs.json 控制。未设置偏好时，LLM 将交互式询问用户。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [kalender, termine, events, ics, google-calendar, routinika]
language: zh
status: stable
dependencies: {'tools': [], 'services': [{'name': 'Google Calendar MCP', 'optional': True, 'purpose': 'Backend option when kalender_backend=google in prefs.json'}], 'protocols': [{'name': 'ICS / iCalendar', 'optional': True, 'purpose': 'Import/export of appointments (RFC 5545 subset)'}], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin gefunden (kein kalender-Service in BACH/system/). Skill vollständig neu konzipiert mit Flag-3-Logik (user-adaptive backend). ICS-Felder angelehnt an RFC 5545, kein externer ICS-Parser benötigt.\n'}
---

> **中文** — `kalender` 官方中文版本。


## 概述与用途

捕获、查询和管理预约行程 —— 支持可选择的后端。核心模块
（`kalender_core.py`）始终默认使用**本地 SQLite 存储**。
如果需要，LLM 会从 `assist/prefs.json` 中选择替代后端。

**Flag 3 — 后端选择：**

| prefs.json 中的 `kalender_backend` | 行为 |
|---|---|
| `local`（默认） | 此 Skill 文件夹中的 SQLite 存储 |
| `google` | Google Calendar MCP（仅 LLM 路径，不在 core.py 中） |
| `routinika` | 通过 module-installer 使用 Routinika 日历（v0.1 未实现） |
| `uptoday` | 通过 module-installer 使用 UpToday 日历（v0.1 未实现） |
| 未设置 | LLM 交互式询问用户的偏好后端 |

> `kalender_core.py` 仅实现 `local` 后端。
> Google Calendar MCP 和其他后端由 LLM 驱动，并记录在 SKILL.md 中，不在核心模块中。

---

## 触发词

| 短语 | 动作 |
|---|---|
| "添加预约" | 捕获新预约 |
| "今天有什么行程？" | 查询今天的预约 |
| "本周有什么行程？" | 7 天概览 |
| "[日期] 有 [标题] 的预约" | 创建带有日期的预约 |
| "[月份] 的所有预约" | 月度概览 |
| "删除预约 [ID]" | 移除预约 |
| "导出预约" | 导出全部/单个预约为 ICS |

---

## 工作流与步骤

1. **检查后端**：读取 `assist/prefs.json` → `kalender_backend`。
2. **未指定偏好**：LLM 询问用户：本地日历、Google Calendar 还是其他？
3. **本地后端**：core.py —— 在 SQLite 存储中创建/查询/删除预约。
4. **Google 后端**：LLM 直接调用 Google Calendar MCP（不涉及 core.py）。
5. **输出**：可读的预约列表或确认信息。

---

## CLI 入口点

```bash
# Create appointment (Deutsch)
python kalender_core.py add "Dentist" --date 2026-07-01 --time 10:00 [--duration 60] [--location "Dr. X practice"]

# Today's appointments (Deutsch)
python kalender_core.py today

# Weekly overview (Deutsch)
python kalender_core.py week [--from 2026-06-22]

# Monthly overview (Deutsch)
python kalender_core.py month [--month 2026-07]

# All appointments (optionally with search term) (Deutsch)
python kalender_core.py list [--search "Dentist"] [--limit 50]

# Delete appointment (Deutsch)
python kalender_core.py delete <id>

# ICS export (Deutsch)
python kalender_core.py export [--id <id>] [--out calendar.ics]

# Backend check (Deutsch)
python kalender_core.py check-backend

# Alternative store (e.g. for tests) (Deutsch)
python kalender_core.py --store /tmp/kal_test.db today --dry-run
```

---

## 存储

| 属性 | 值 |
|---|---|
| 类型 | SQLite（本地后端） |
| 路径（默认） | `skills/assist/kalender/store.db` |
| 覆盖 | `--store <path>` 或环境变量 `KALENDER_STORE` |
| 数据表 | `events` |

### 表结构 (Schema)

```sql
CREATE TABLE IF NOT EXISTS events (
    id           TEXT PRIMARY KEY,      -- UUID (short: 8 hex)
    title        TEXT NOT NULL,         -- appointment name
    date         TEXT NOT NULL,         -- ISO date YYYY-MM-DD
    time         TEXT,                  -- HH:MM (optional)
    duration_min INTEGER,               -- duration in minutes (optional)
    location     TEXT,                  -- location (optional)
    description  TEXT,                  -- note/description
    recurrence   TEXT,                  -- ICS RRULE (optional, e.g. "FREQ=WEEKLY")
    ics_uid      TEXT UNIQUE,           -- ICS UID for import/export
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);
```

---

## 设计理念

- 核心仅实现 `local` 后端 —— 轻量级，无外部依赖。
- ICS 导出生成有效的 RFC 5545 子集（VCALENDAR + VEVENT），可导入所有常用日历应用。
- ICS 导入（解析）在 v0.1 中尚未实现 —— 计划在 v0.2 中提供。
- 重复规则（`recurrence`/RRULE）会保存但不进行评估 —— 评估功能计划在 v0.2 中提供。

---

## 隐私保护

- 本地预约保存在 `store.db` 中 —— 核心模块无需网络连接。
- 使用 Google Calendar 后端时，由 Google Calendar MCP 处理数据 —— 适用 Google 的隐私政策。
- 请勿将 `store.db` 提交到 Git（建议添加到 `.gitignore`）。

---

## 相关资源

- Google Calendar MCP (`mcp__claude_ai_Google_Calendar__*`) —— 替代后端，由 LLM 驱动
- Skill `assist/haushalt-manager` —— Routinika 集成（状态检查模式）
- `tools/module-installer/module_installer.py` —— 用于未来的 Routinika/UpToday 后端集成

---

## 变更日志

| 版本 | 日期 | 变更内容 |
|---|---|---|
| 0.1.0 | 2026-06-22 | 初始创建 —— Flag-3 逻辑、本地后端、ICS 导出 |