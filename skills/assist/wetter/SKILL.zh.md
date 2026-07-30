---
name: wetter
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: 通过 wttr.in（免费，无需 API 密钥）回答特定位置或坐标的天气问题。包含当前天气 + 3 天预报。位置来自用户请求或首选项；支持可选的短期缓存。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [wetter, wttr, vorschau, assist]
language: zh
status: active
dependencies: {'tools': ['wetter_core.py'], 'services': [], 'protocols': [], 'python': ['urllib', 'json']}
provenance: {'origin': 'bach', 'origin_path': 'system/hub/_services/weather/weather_service.py', 'origin_version': '1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="wetter banner">

> **中文** — `wetter` 官方中文版本。


# 天气 (中文)

用于日常使用的快速、免 API 密钥的天气信息。

## 概述与用途

在无需 API 密钥的情况下回答“天气怎么样？”等问题（数据源：wttr.in）。
提供当前天气（温度、体感温度、风速、湿度、紫外线）以及紧凑的 3 天预报。
**用户中立：** 代码中无固定位置——位置来自请求或 `assist/prefs.json` (`wetter_default_location`)，LLM 会与用户互动填写该信息。

## 触发条件

| 用户输入 | 操作 |
|---|---|
| "波茨坦的天气？" / "汉堡的天气怎么样？" | `wetter_core.py "<location>"` |
| "明天的天气？"（未提供位置） | `wetter_core.py --default`（位置来自首选项） |
| "我的默认天气位置是波茨坦" | `wetter_core.py --set-default "Potsdam"` |
| 已知坐标 | `wetter_core.py <lat> <lon>` |

## 工作流程与步骤

```
1. 确定位置：来自请求；否则来自 prefs.json (wetter_default_location)；
   否则与用户交互式询问 + 可选保存为默认值。
2. 查询 wetter_core.py (wttr.in, 2 次尝试, 30 分钟缓存)。
3. 显示易读的天气文本 + 3 天预报。
```

## CLI 入口点 (wetter_core.py)

```bash
python wetter_core.py "Potsdam"          # 位置
python wetter_core.py 52.6789 13.5878   # 坐标
python wetter_core.py --default         # 来自 prefs.json 的位置
python wetter_core.py --set-default "Potsdam"
```

## 存储（可选）

- **无强制存储。** 可选的短期缓存 `assist/wetter/.cache.json`
  （TTL 30 分钟，尽力而为）—— 避免重复的网络调用。
- 位置首选项保存在 `assist/prefs.json` (`wetter_default_location`) 中。

## 设计理念

我们使用 wttr.in 作为无需密钥的默认数据源，但如果用户喜欢，也支持扩展其他天气后端（例如 DWD/OpenWeather）。

## 隐私

- 仅将位置名称/坐标发送至 wttr.in（查询所必需）。
- 无遥测，无账户。缓存和首选项保存在本地。

## 相关资源

- `assist/AGENTS.md` — 顶层路由
- `assist/reiseroute/` — 用于行程规划的天气信息（计划中）

## 变更日志

### 0.1.0 (2026-06-22)
- 初始版本。从 BACH `hub/_services/weather/weather_service.py` (MIT) 移植。
- 扩展功能：支持位置名称（不仅限于坐标）、3 天预报、可选缓存、基于首选项的默认位置。用户中立。