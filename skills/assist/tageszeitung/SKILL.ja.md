---
name: tageszeitung
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: RSSフィードやWebソースから個人の日刊紙を作成します。BACHニュースシステム（news.py + newspaper_generator.py）から移植。独自のSQLiteストア（Origin-DBなし）。feedparserはオプション — stdlib経由のXMLフォールバックあり。Edge Headless（msedge.exe）によるPDFエクスポート。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [zeitung, news, rss, feed, pdf, tageszeitung]
language: ja
status: stable
dependencies: {'tools': [{'name': 'msedge.exe', 'optional': True, 'purpose': 'HTML → PDF (Edge Headless); without Edge: HTML output only'}], 'services': [], 'protocols': [], 'python': [{'name': 'feedparser', 'optional': True, 'install': 'pip install feedparser', 'purpose': 'RSS parsing (main backend). Fallback: defusedxml → regex'}, {'name': 'defusedxml', 'optional': True, 'install': 'pip install defusedxml', 'purpose': 'XXE-safe XML parser as fallback when feedparser is missing. Without defusedxml a regex fallback is used (no ET.fromstring on network data).'}]}
provenance: {'origin': 'bach-port', 'origin_path': 'BACH/system/hub/news.py + hub/_services/newspaper/newspaper_generator.py', 'origin_version': 'news.py v1.x, newspaper_generator.py v1.x', 'origin_repo': 'ellmos-ai/bach (privat)', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'notes': 'Schema (news_sources + news_items) 1:1 aus BACH news.py portiert. BaseHandler-Abhängigkeit entfernt. Origin-DB-Pfad entfernt. DB-Pfad konfigurierbar. newspaper_generator.py-Logik (HTML-Render + Edge-PDF) userneutral übernommen.\n'}
---

> **日本語** — `tageszeitung` の公式日本語版。


## 概要と目的

設定されたRSSフィードやWebソースから記事を取得し、カテゴリ別に分類してHTML/PDFの日刊紙としてレンダリングします。記事はローカルの `tageszeitung/store.db` に保存され、既読としてマークされます。

---

## トリガー

| フレーズ | アクション |
|---|---|
| "日刊紙を作成して" | 記事の取得 + PDFレンダリング |
| "今日の日刊紙" | 今日の新聞をレンダリング |
| "フィードを追加 [URL]" | RSSソースを登録 |
| "ソース一覧を表示" | ソースリストを出力 |
| "ニュースを取得" | 全ソースを取得（レンダリングなし） |

---

## ワークフローと手順

1. **ソースの確認**: `news_sources` からすべてのアクティブなソースを読み込みます。
2. **取得**: feedparser（または xml.etree フォールバック）経由でRSS、urllib 経由でWebを取得。
3. **重複排除**: UNIQUE(source_id, url) により重複を防止。
4. **レンダリング**: 未読記事をカテゴリ別にグループ化 → HTML → PDF。
5. **配信**: HTML/PDFを出力フォルダ（設定可能なパス）に配置。

---

## CLI エントリポイント

```bash
# Add source (Deutsch)
python tageszeitung_core.py add-source "Heise" rss https://www.heise.de/rss/heise-atom.xml --category tech

# Fetch all sources (Deutsch)
python tageszeitung_core.py fetch

# Render daily newspaper (HTML + PDF if Edge available) (Deutsch)
python tageszeitung_core.py render [--date 2026-06-22] [--out /path/]

# List sources (Deutsch)
python tageszeitung_core.py sources

# Unread articles (Deutsch)
python tageszeitung_core.py items [--limit 50] [--category tech]

# Mark article as read (Deutsch)
python tageszeitung_core.py read <item_id>

# Alternative store (e.g. for tests) (Deutsch)
python tageszeitung_core.py --store /tmp/t.db sources --dry-run
```

---

## ストア

| 属性 | 値 |
|---|---|
| タイプ | SQLite |
| パス（デフォルト） | `skills/assist/tageszeitung/store.db` |
| 上書き | `--store <path>` または環境変数 `TAGESZEITUNG_STORE` |
| テーブル | `news_sources`, `news_items` |

### スキーマ（BACH news.py から移植）

```sql
CREATE TABLE IF NOT EXISTS news_sources (
    id           TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    type         TEXT NOT NULL DEFAULT 'rss',  -- rss | web
    url          TEXT NOT NULL UNIQUE,
    category     TEXT DEFAULT 'Allgemein',
    schedule     TEXT DEFAULT 'daily',
    is_active    INTEGER DEFAULT 1,
    last_fetched TEXT,
    fetch_count  INTEGER DEFAULT 0,
    error_count  INTEGER DEFAULT 0,
    last_error   TEXT,
    created_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS news_items (
    id           TEXT PRIMARY KEY,
    source_id    TEXT NOT NULL REFERENCES news_sources(id),
    title        TEXT NOT NULL,
    content      TEXT,
    summary      TEXT,
    url          TEXT,
    author       TEXT,
    published_at TEXT,
    fetched_at   TEXT NOT NULL,
    is_read      INTEGER DEFAULT 0,
    category     TEXT,
    UNIQUE(source_id, url)
);
```

---

## 動作方針

- feedparser が優先されます。feedparser がない場合、xml.etree フォールバックがシンプルな RSS 2.0 フィードを処理します。
- PDF 生成には、システム PATH または `MSEDGE_PATH` 環境変数に `msedge.exe` が必要です。Edge がない場合は HTML のみがレンダリングされます。
- カテゴリあたりの最大記事数: `assist/prefs.json` で設定可能（`tageszeitung_max_per_category`、デフォルト: 5）。

---

## プライバシー

- 記事の内容はローカルの `store.db` に保存されます。
- 外部の解析サービスは使用しません — 設定された RSS/Web ソースのみにアクセスします。

---

## 関連リソース

- BACH `hub/news.py` — 移植元（読み取り専用）
- BACH `hub/_services/newspaper/newspaper_generator.py` — 移植元（読み取り専用）

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|---|---|---|
| 0.1.0 | 2026-06-22 | 初版作成 — BACH スキーマを移植、独自ストア、feedparser はオプション |