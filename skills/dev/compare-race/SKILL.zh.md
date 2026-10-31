---
name: compare-race
version: 1.0.0
type: pointer
author: Lukas Geiger
created: 2026-08-16
updated: 2026-08-16
description: "当用户希望将同一提示词发送给多个 LLM 并比较其回答时使用——可顺序执行（秒表，每条通道干净计时）或并行执行（真正的赛跑），可选择对每个模型重复若干次，由起始模型从质量、正确性、完整性、指令遵循度和延迟等方面进行评判（时间只是其中一个维度）。触发词：/compare-race、'model race'、'比较模型'、'将同一提示词发送给多个模型'。"
standalone: true
anthropic_compatible: true
bach_compatible: false
category: dev
tags: [model-comparison, race, benchmark, multi-agent, judge, workflow]
language: zh
status: active
visibility: public
pointer: {'module_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race', 'prompt_de': 'prompts/RACE-STARTER.de.md', 'prompt_en': 'prompts/RACE-STARTER.en.md', 'config': 'config/compare-race.config.example.json', 'repo': 'github.com/ellmos-ai/compare-race'}
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['system-auditor'], 'optional_tools': [{'name': 'coma', 'path': '.AI/.MODULES/.ORCHESTRATION/coma/', 'python_module': 'coma', 'usage': 'Ausfuehrungsschicht fuer compare-race run (Spawn/Polling/Dateiprotokoll)', 'note': 'Optional. Ohne coma laeuft der modellmanuelle Weg: Spuren selbst ausfuehren und mit compare-race record einreichen.'}]}
provenance: {'origin': 'module', 'origin_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race/prompts/RACE-STARTER.de.md', 'origin_version': '0.1.0', 'last_sync_from_origin': '2026-08-16', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
translated_from_sha256: eef2d1e681ca3ed6c7fe63a8a36535632cf48a7b990fd8d944c8ef42ea046750
translator: "claude-haiku-5-5; revision:gpt-6-sol"
translated_at: "2026-10-15T11:46:14.390544+00:00"
---
<img src="banner.png" width="100%" alt="compare-race banner">

# compare-race — 指针技能（德语）

> **本技能仅为指针。事实来源是模块本身。**

## 模块路径

```
<HOME>\OneDrive\.TOPICS\.AI\.MODULES\.ORCHESTRATION\compare-race\
```

仓库：[github.com/ellmos-ai/compare-race](https://github.com/ellmos-ai/compare-race)

## 给代理的说明

1. 阅读模块文件夹中的角色提示 **`prompts/RACE-STARTER.de.md`** 并遵循它。
   你是 RACE-STARTER，默认也是 **Judge**（用户决定，2026-08-16）。
2. 检查配置（`compare-race config`；主机配置位于 `~/.compare-race/`）。
   选择模式：`sequential` = 秒表（每条通道干净的单独计时）·
   `parallel` = 真正的赛跑。**秒表只是一个比喻**——时间与质量、正确性、完整性、指令遵循度和成本一样，只是评判维度之一。
3. 启动比赛（`compare-race run --prompt-file …`）；若没有 coma 模块，则由当前模型手动执行各条赛道，并通过 `compare-race record` 提交结果。
4. 作为 Judge，在比赛文件夹的 `RACE.md` 中填写评判标准——逐一亲自阅读每个 RUN 文件；若自身模型参赛，须明确说明自身参赛可能造成的评判偏向。
5. 轴向纪律：仅当恰好一个轴发生变化时才作出归因（model = 比赛 · run = 方差 · time = 模型漂移）。

## 配额警告

比赛会消耗**每一个**参与配额（claude/codex/agy/kimi）。进行大型比赛（多条通道 × 多次重复）前，请先询问用户。
