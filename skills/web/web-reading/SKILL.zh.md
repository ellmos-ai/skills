---
name: web-reading
version: 1.1.0
type: protocol
author: BACH Team
created: 2026-03-12
updated: 2026-07-05
description: 用于读取和提取 Web 内容的路由器和协议。首先决定需要什么（主要文本 vs 结构 vs 截图），然后决定系统上可用的哪个工具可以提供该内容。如果没有合适的内容，建议安装 web-scraper 模块。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: web
tags: [web-scraping, content-extraction, research, router]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['requests', 'beautifulsoup4']}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/webseiten-lesen.md', 'origin_version': '3.8.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
bach_integration: {'handler': 'web-parse, web-scrape', 'db_tables': [], 'hooks': [], 'bach_origin_path': 'system/skills/workflows/'}
---

> **中文** — `web-reading` 官方中文版本。


# Web Reading 网页读取 (Router)

## 概述与目的

获取并处理网页内容——但不要盲目选择工具。本技能进行路由：**目标优先，然后选择最佳可用工具。** 实际实现位于 **`web-scraper` 模块** 中；本技能仅显示当前存在的内容以及如何使用它。

## 步骤 1 — 需要什么？

```
Process a web page?
  |
  +-- Main text (article / prose)   → "Content"     → Step 2A
  +-- Links / forms / headers       → "Structure"   → Step 2B
  +-- Rendered image of the page    → "Screenshot"  → Step 2C
```

## 步骤 2 — 使用哪个工具？(Router)

使用每个列表中**首个可用**的工具。“可用”表示该工具/技能/模块在当前会话中确实存在。

### 2A — 内容（主要文本，干净的 markdown）

| 优先级 | 工具 | 可用条件… | 用法 |
|---|---|---|---|
| 1 | **`defuddle`** 技能 | 已列出 `defuddle` 技能 | 从普通网页提取干净的 markdown |
| 2 | 内置 **`WebFetch`** | Agent 拥有 WebFetch 工具 | 快速读取/总结 URL 内容 |
| 3 | **`fc_web_fetch`** (MCP) | 已加载 FileCommander MCP | `mode: "extract"` |
| 4 | **`web-scraper`** 模块 | 已安装/可导入该模块 | `web-scraper extract <url>` / `extract(url)` |

> 注意：`.md` URL 本身就是 markdown → 直接使用 `WebFetch`，无需提取器。

### 2B — 结构（链接、表单、响应头）

`WebFetch`/`defuddle` **不适用于**此处（它们返回处理后的文本，而非原始结构）。请改用：

| 优先级 | 工具 | 可用条件… | 用法 |
|---|---|---|---|
| 1 | **`fc_web_fetch`** (MCP) | 已加载 FileCommander MCP | `mode: "links" \| "forms" \| "headers"` |
| 2 | **`web-scraper`** 模块 | 已安装/可导入该模块 | `web-scraper links\|forms\|headers <url>` |

### 2C — 网页截图

| 优先级 | 工具 | 可用条件… | 用法 |
|---|---|---|---|
| 1 | **`web-scraper`** 模块 | 带有 `[screenshot]` 扩展包的模块 | `web-scraper screenshot <url> --out img.png` |
| 2 | 浏览器自动化工具 | 例如包含 Playwright/Computer-Use | 视具体页面而定 |

## 步骤 3 — 降级方案：未找到合适工具？

如果针对该用途**没有**可用工具，建议安装 **`web-scraper` 模块**（完整功能：get/links/forms/headers/extract/screenshot）：

```bash
# 从本地模块文件夹 (.MODULES/.TOOLS/web-scraper)
pip install ".[http,extract]"          # + [screenshot] 用于截图

# 然后：
web-scraper extract <url>
```

作为 Python 库使用：

```python
from web_scraper import WebScraper, extract
print(extract("https://example.com")["content"])
```

## 终极方案 — 独立代码片段（除 requests/bs4 外无其他依赖）

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

## 变更日志

### 1.1.0 (2026-07-05)
- 从普通协议重构为 **路由器 (Router)**：检测可用的网页处理能力（`defuddle`、`WebFetch`、`fc_web_fetch`、`web-scraper` 模块），并按用途（内容/结构/截图）进行路由；否则建议安装 `web-scraper` 模块。
- 统一名称为 `web-reading`（在德语版本中原为 `webseiten-lesen`）。
- 从正文中移除了 BACH CLI 示例（符合独立规范；来源在 `bach_integration` 前言元数据中保持记录）。

### 1.0.0 (2026-03-12)
- 从 BACH v3.8.0 工作流 `webseiten-lesen.md` 导出