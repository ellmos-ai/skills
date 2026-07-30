---
name: kalender
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: ユーザー適応型バックエンド選択（Flag 3）を備えたカレンダーSkill。デフォルト：ローカル SQLite ストレージ。オプション：Google Calendar MCP、Routinika、または UpToday をバックエンドとして使用（assist/prefs.json で制御）。設定がない場合、LLM は対話形式でユーザーに確認します。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [kalender, termine, events, ics, google-calendar, routinika]
language: ja
status: stable
dependencies: {'tools': [], 'services': [{'name': 'Google Calendar MCP', 'optional': True, 'purpose': 'Backend option when kalender_backend=google in prefs.json'}], 'protocols': [{'name': 'ICS / iCalendar', 'optional': True, 'purpose': 'Import/export of appointments (RFC 5545 subset)'}], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin gefunden (kein kalender-Service in BACH/system/). Skill vollständig neu konzipiert mit Flag-3-Logik (user-adaptive backend). ICS-Felder angelehnt an RFC 5545, kein externer ICS-Parser benötigt.\n'}
---

<img src="banner.png" width="100%" alt="kalender banner">

> **日本語** — `kalender` の公式日本語版。


## 概要と目的

予定の記録、照会、管理を、選択可能なバックエンドで行います。コア
（`kalender_core.py`）は常に**ローカル SQLite ストレージ**をデフォルトとして使用します。
LLM は必要に応じて `assist/prefs.json` から代替バックエンドを選択します。

**Flag 3 — バックエンド選択:**

| prefs.json 内の `kalender_backend` | 動作 |
|---|---|
| `local` (デフォルト) | この Skill フォルダ内の SQLite ストレージ |
| `google` | Google Calendar MCP（LLM パスのみ、core.py には含まれず） |
| `routinika` | module-installer 経由の Routinika カレンダー（v0.1 未実装） |
| `uptoday` | module-installer 経由の UpToday カレンダー（v0.1 未実装） |
| 未設定 | LLM が対話形式で希望のバックエンドをユーザーに確認 |

> `kalender_core.py` は `local` バックエンドのみを実装しています。
> Google Calendar MCP およびその他のバックエンドは LLM 駆動であり、コアではなく SKILL.md に記載されています。

---

## トリガー

| フレーズ | アクション |
|---|---|
| "予定を追加" | 新しい予定を記録 |
| "今日の予定は？" | 今日の予定を照会 |
| "今週の予定は？" | 7 日間の概要 |
| "[日付] に [タイトル] の予定" | 日付を指定して予定を作成 |
| "[月] のすべての予定" | 月間概要 |
| "予定 [ID] を削除" | 予定を削除 |
| "予定をエクスポート" | 全体/個別予定の ICS エクスポート |

---

## ワークフローと手順

1. **バックエンドの確認**: `assist/prefs.json` → `kalender_backend` を読み込む。
2. **設定がない場合**: LLM がユーザーに質問: ローカルカレンダー、Google Calendar、その他？
3. **ローカルバックエンド**: core.py — SQLite ストレージで予定を作成/照会/削除。
4. **Google バックエンド**: LLM が Google Calendar MCP を直接呼び出し（core.py は関与しない）。
5. **出力**: 読みやすい予定リストまたは確認メッセージ。

---

## CLI エントリポイント

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

## ストレージ

| プロパティ | 値 |
|---|---|
| タイプ | SQLite（ローカルバックエンド） |
| パス（デフォルト） | `skills/assist/kalender/store.db` |
| 上書き | `--store <path>` または環境変数 `KALENDER_STORE` |
| テーブル | `events` |

### スキーマ

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

## 設計方針

- コアは `local` バックエンドのみを実装 — 軽量で外部依存関係はありません。
- ICS エクスポートは、一般的なすべてのカレンダーアプリにインポート可能な RFC 5545 サブセット（VCALENDAR + VEVENT）を生成します。
- ICS インポート（解析）は v0.1 では未実装です — v0.2 で計画されています。
- 繰り返しルール（`recurrence`/RRULE）は保存されますが評価されません — 評価は v0.2 の予定です。

---

## プライバシー

- ローカルの予定は `store.db` に保存されます — コアにはネットワークアクセスがありません。
- Google Calendar バックエンドを使用する場合、Google Calendar MCP がデータを処理します — Google のプライバシーポリシーが適用されます。
- `store.db` を Git にコミットしないでください（推奨: `.gitignore`）。

---

## 関連リソース

- Google Calendar MCP (`mcp__claude_ai_Google_Calendar__*`) — 代替バックエンド（LLM 駆動）
- Skill `assist/haushalt-manager` — Routinika 連携（在宅確認パターン）
- `tools/module-installer/module_installer.py` — 将来の Routinika/UpToday バックエンド連携用

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|---|---|---|
| 0.1.0 | 2026-06-22 | 初回作成 — Flag-3 ロジック、ローカルバックエンド、ICS エクスポート |