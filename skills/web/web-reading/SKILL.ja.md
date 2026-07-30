---
name: web-reading
version: 1.1.0
type: protocol
author: BACH Team
created: 2026-03-12
updated: 2026-07-05
description: Webコンテンツの読み取りと抽出のためのルーターおよびプロトコル。最初に何が必要か（メインテキスト vs 構造 vs スクリーンショット）を決定し、次にシステム上で利用可能などのツールがそれを処理するかを決定します。適切なものが存在しない場合は、web-scraper モジュールのインストールを推奨します。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: web
tags: [web-scraping, content-extraction, research, router]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['requests', 'beautifulsoup4']}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/webseiten-lesen.md', 'origin_version': '3.8.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
bach_integration: {'handler': 'web-parse, web-scrape', 'db_tables': [], 'hooks': [], 'bach_origin_path': 'system/skills/workflows/'}
---

<img src="banner.png" width="100%" alt="web-reading banner">

> **日本語** — `web-reading` の公式日本語版。


# Web Reading (ルーター)

## 概要と目的

Webコンテンツを取得・処理しますが、盲目的にツールを選択しないでください。このスキルは**まず目的を決め、次に利用可能な最適なツールを選択する**ルーティングを行います。実際の機能実装は **`web-scraper` モジュール** に存在し、このスキルは現在何が存在し、それをどのように使用するかのみを示します。

## ステップ 1 — 何が必要か？

```
Process a web page?
  |
  +-- Main text (article / prose)   → "Content"     → Step 2A
  +-- Links / forms / headers       → "Structure"   → Step 2B
  +-- Rendered image of the page    → "Screenshot"  → Step 2C
```

## ステップ 2 — どのツールか？(ルーター)

各リストで**最初に利用可能な**ツールを使用してください。「利用可能」とは、そのツール/スキル/モジュールが現在のセッションに実際に存在することを意味します。

### 2A — コンテンツ（メインテキスト、クリーンな Markdown）

| 優先度 | ツール | 利用可能条件… | 使い方 |
|---|---|---|---|
| 1 | **`defuddle`** スキル | スキル `defuddle` が一覧にある | 通常のWebページからクリーンな Markdown を取得 |
| 2 | 組み込み **`WebFetch`** | エージェントが WebFetch ツールを所有 | URL の迅速な読み取り/要約 |
| 3 | **`fc_web_fetch`** (MCP) | FileCommander MCP が読み込まれている | `mode: "extract"` |
| 4 | **`web-scraper`** モジュール | モジュールがインストール/インポート可能 | `web-scraper extract <url>` / `extract(url)` |

> 注: `.md` URL は既に Markdown です → エクストラクターなしで `WebFetch` を直接使用してください。

### 2B — 構造（リンク、フォーム、ヘッダー）

`WebFetch`/`defuddle` はここでは**適していません**（生構造ではなく処理済みテキストを返すため）。代わりに以下を使用してください：

| 優先度 | ツール | 利用可能条件… | 使い方 |
|---|---|---|---|
| 1 | **`fc_web_fetch`** (MCP) | FileCommander MCP が読み込まれている | `mode: "links" \| "forms" \| "headers"` |
| 2 | **`web-scraper`** モジュール | モジュールがインストール/インポート可能 | `web-scraper links\|forms\|headers <url>` |

### 2C — スクリーンショット

| 優先度 | ツール | 利用可能条件… | 使い方 |
|---|---|---|---|
| 1 | **`web-scraper`** モジュール | `[screenshot]` エクストラ付きモジュール | `web-scraper screenshot <url> --out img.png` |
| 2 | ブラウザ自動化ツール | Playwright/Computer-Use などが存在する | ページ依存 |

## ステップ 3 — フォールバック：適切なものが見つからない場合

目的に適したツールが**存在しない**場合は、**`web-scraper` モジュール**のインストールを推奨します（全機能: get/links/forms/headers/extract/screenshot）：

```bash
# ローカルモジュールフォルダ (.MODULES/.TOOLS/web-scraper) から
pip install ".[http,extract]"          # + スクリーンショット用 [screenshot]

# その後:
web-scraper extract <url>
```

ライブラリとして使用：

```python
from web_scraper import WebScraper, extract
print(extract("https://example.com")["content"])
```

## 最終手段 — スタンドアロンスニペット（requests/bs4 以外の依存関係なし）

```python
import requests
from bs4 import BeautifulSoup

def extract_content(url: str) -> str:
    """Simple content extraction."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)
```

## 変更履歴

### 1.1.0 (2026-07-05)
- 単純なプロトコルから**ルーター**へと再構築：利用可能な Web 機能（`defuddle`、`WebFetch`、`fc_web_fetch`、`web-scraper` モジュール）を検出し、目的（コンテンツ/構造/スクリーンショット）に応じてルーティング。それ以外の場合は `web-scraper` モジュールを推奨。
- 名前を `web-reading` に統一（DE版では `webseiten-lesen` でした）。
- 本文から BACH CLI の例を削除（スタンドアロン準拠。元データは `bach_integration` フロントマターに記録されています）。

### 1.0.0 (2026-03-12)
- BACH v3.8.0 ワークフロー `webseiten-lesen.md` からのエクスポート