---
name: tageszeitung
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: 从 RSS 订阅源和 Web 来源创建个性化的每日报纸。从 BACH 新闻系统（news.py + newspaper_generator.py）移植。独立的 SQLite 存储（无 Origin-DB）。feedparser 为可选依赖 — 支持 stdlib XML 回退。通过 Edge Headless (msedge.exe) 导出 PDF。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [zeitung, news, rss, feed, pdf, tageszeitung]
language: zh
status: stable
dependencies: {'tools': [{'name': 'msedge.exe', 'optional': True, 'purpose': 'HTML → PDF (Edge Headless); without Edge: HTML output only'}], 'services': [], 'protocols': [], 'python': [{'name': 'feedparser', 'optional': True, 'install': 'pip install feedparser', 'purpose': 'RSS parsing (main backend). Fallback: defusedxml → regex'}, {'name': 'defusedxml', 'optional': True, 'install': 'pip install defusedxml', 'purpose': 'XXE-safe XML parser as fallback when feedparser is missing. Without defusedxml a regex fallback is used (no ET.fromstring on network data).'}]}
provenance: {'origin': 'bach-port', 'origin_path': 'BACH/system/hub/news.py + hub/_services/newspaper/newspaper_generator.py', 'origin_version': 'news.py v1.x, newspaper_generator.py v1.x', 'origin_repo': 'ellmos-ai/bach (privat)', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'notes': 'Schema (news_sources + news_items) 1:1 aus BACH news.py portiert. BaseHandler-Abhängigkeit entfernt. Origin-DB-Pfad entfernt. DB-Pfad konfigurierbar. newspaper_generator.py-Logik (HTML-Render + Edge-PDF) userneutral übernommen.\n'}
---

<img src="banner.png" width="100%" alt="tageszeitung banner">

> **中文** — `tageszeitung` 官方中文版本。


## 概述与目的

从配置的 RSS 订阅源和网页源获取文章，按分类排序并渲染为 HTML/PDF 每日报纸。文章在本地存储于 `tageszeitung/store.db` 中并标记为已读。

---

## 触发词

| 短语 | 动作 |
|---|---|
| "创建我的每日报纸" | 获取文章 + 渲染 PDF |
| "今天的每日报纸" | 渲染今天的报纸 |
| "添加订阅源 [URL]" | 注册 RSS 来源 |
| "显示我的来源" | 输出来源列表 |
| "获取新闻" | 获取所有来源（不渲染） |

---

## 工作流程与步骤

1. **检查来源**：从 `news_sources` 读取所有活跃来源。
2. **获取内容**：通过 feedparser（或 xml.etree 回退）获取 RSS，通过 urllib 获取网页内容。
3. **去重**：UNIQUE(source_id, url) 防止重复。
4. **渲染**：按分类分组未读文章 → HTML → PDF。
5. **交付**：将 HTML/PDF 放置在输出文件夹中（路径可配置）。

---

## CLI 入口点

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

## 存储

| 属性 | 值 |
|---|---|
| 类型 | SQLite |
| 路径（默认） | `skills/assist/tageszeitung/store.db` |
| 覆盖 | `--store <path>` 或环境变量 `TAGESZEITUNG_STORE` |
| 数据表 | `news_sources`, `news_items` |

### 模式 Schema（移植自 BACH news.py）

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

## 运行原则

- 优先使用 feedparser；若无 feedparser，则使用 xml.etree 回退处理简单的 RSS 2.0 订阅源。
- PDF 生成需要在系统 PATH 或 `MSEDGE_PATH` 环境变量中存在 `msedge.exe`。若无 Edge，则仅渲染 HTML。
- 每个分类的最大文章数：可通过 `assist/prefs.json` 进行配置（`tageszeitung_max_per_category`，默认值：5）。

---

## 隐私

- 文章内容保存在本地 `store.db` 中。
- 无外部分析服务 — 仅调用配置的 RSS/Web 来源。

---

## 相关资源

- BACH `hub/news.py` — 源文件（只读）
- BACH `hub/_services/newspaper/newspaper_generator.py` — 源文件（只读）

---

## 变更日志

| 版本 | 日期 | 变更内容 |
|---|---|---|
| 0.1.0 | 2026-06-22 | 初始创建 — 移植 BACH 模式，独立存储，feedparser 为可选依赖 |