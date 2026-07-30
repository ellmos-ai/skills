---
name: dossier-briefing
version: 1.0.0
category: assist
description: 生成主题或人员的结构化研究简报 Markdown 骨架（标准输出或文件）。无持久化存储。
tags: [briefing, dossier, recherche, markdown, research]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['datetime', 'pathlib', 'textwrap']}
runtime: python3
entry_point: dossier_briefing_core.py
provenance: {'origin': 'BACH persoenlicher-assistent', 'origin_path': 'system/agents/persoenlicher-assistent/tools/dossier_generator.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': 'Alle Origin-DB-Abhaengigkeiten entfernt (create_dossier, update_dossier, DOSSIERS_DIR, DossierGenerator-Klasse mit DB-Methoden). Nur _create_markdown-Logik portiert und verallgemeinert (Person→Subjekt). Kein Store. One-Shot-Scaffold-Generator. Headless, nur Stdlib.\n'}
language: zh
---

> **中文** — `dossier-briefing` 官方中文版本。


# Dossier-Briefing（中文）

**主题或人员的结构化研究简报**

---

## 概述与目的

为任何主题（人员、公司、事件、概念）生成空白的结构化 Markdown 简报。
该骨架作为后续使用 `research-agent` 或 `web-reading` 进行深入研究的起点。

---

## 触发词

| 短语 | 操作 |
|---|---|
| "居里夫人的研究简报" / "Create a briefing on Marie Curie" | 骨架：人员，type=person |
| "OpenAI 的档案" / "Dossier on OpenAI" | 骨架：公司，type=organization |
| "量子计算简报" / "Briefing on quantum computing" | 骨架：主题，type=topic |
| "准备 COP30 的研究简报" / "Prepare a research briefing on COP30" | 骨架：事件，type=event |

---

## 工作流与步骤

1. **提取主题名称：** 从用户输入中提取简报的名称/标题。
2. **识别类型：** person、organization、topic、event（或 unspecified）。
3. **生成骨架：** 创建包含所有相关章节的 Markdown。
4. **输出：** 标准输出（stdout）或可选地写入文件（`-o file.md`）。
5. **开始研究：** 将骨架移交给 `research-agent` 或 `web-reading` 以填补缺失章节。

---

## CLI

```bash
# Briefing to stdout (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Marie Curie" --typ person

# Write to file (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "OpenAI" --typ organization -o briefing_openai.md

# Topic briefing (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Quantum computing" --typ topic

# Event (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "COP30" --typ event

# Without type (generic) (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "My topic"

# Help (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py --help
```

---

## 简报类型与章节

| 类型 | 章节 |
|---|---|
| `person` | 基本数据、履历/背景、工作与贡献、来源、备注 |
| `organization` | 概况、历史、产品/服务、关键人物、来源、备注 |
| `topic` | 概述、背景/上下文、最新进展、主要来源、待解答问题、备注 |
| `event` | 关键事实、参与者、背景/时间线、意义、来源、备注 |
| `unspecified` | 概述、背景、细节、来源、备注 |

---

## 存储

无持久化存储。骨架仅作为输出生成（标准输出或文件），不会存储在数据库中。

---

## 原则与态度

- 始终强调骨架是空白的，必须通过研究来填充。
- 切勿虚构内容或产生幻觉——仅提供结构。
- 若类型不明确，请询问用户或使用 `unspecified`。

---

## 隐私与安全

无网络访问。无存储。纯本地处理。

---

## 相关资源

- `research-agent` — 使用研究结果填充简报骨架
- `web-reading` — 读取网页并为简报提取内容

---

## 变更日志

| 版本 | 日期 | 变更内容 |
|---|---|---|
| 1.0.0 | 2026-06-22 | 从 BACH dossier_generator.py v1.0.0 创建；已移除存储，泛化处理 |