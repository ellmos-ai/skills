---
name: reiseroute
version: 1.0.0
category: assist
description: 通过 OSRM（Open Source Routing Machine）规划从 A 到 B 的路线。支持汽车、自行车和步行。无需 API 密钥。
tags: [routing, navigation, osrm, openstreetmap, reise]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['urllib.request', 'urllib.parse', 'urllib.error', 'json']}
runtime: python3
entry_point: reiseroute_core.py
provenance: {'origin': 'BACH hub routing-service', 'origin_path': 'system/hub/_services/routing/routing_service.py', 'origin_version': '1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': 'urllib.parse-Import an den Kopf verschoben (war im Original nur im else-Zweig). geocode_place (Nominatim) integriert. Keine Origin-DB. Kein Store. Userneutral, headless, nur Stdlib.\n'}
language: zh
---

<img src="banner.png" width="100%" alt="reiseroute banner">

> **中文** — `reiseroute` 官方中文版本。


# Travel Route (中文)

**通过 OSRM（Open Source Routing Machine）进行路线规划**

---

## 概述与用途

通过公共 OSRM 服务（`router.project-osrm.org`）规划两个地点（名称或坐标）
之间的路线。返回距离、旅行时间和交通方式。无需 API 密钥，无需账户。

---

## 触发词

| 短语 | 动作 |
|---|---|
| “规划从柏林到汉堡的路线” | 汽车路线，地理编码地点名称 |
| “开车从慕尼黑到维也纳需要多长时间？” | 汽车路线 + 时间 |
| “从波茨坦到柏林的自行车路线” | 自行车模式 |
| “从柏林克罗伊茨贝格步行到米特区” | 步行模式 |
| “从 52.52,13.41 到 53.55,9.99 的路线” | 直接坐标 |

---

## 工作流程与步骤

1. **提取起点和终点：** 从用户输入中提取。
2. **检测模式：** 汽车（默认）、自行车、步行。
3. **地理编码：** 通过 Nominatim 将地点名称转换为坐标。
4. **查询 OSRM：** 返回距离（千米）+ 时长（已格式化）。
5. **输出结果：** 简明的文本摘要。

---

## CLI

```bash
# 两个地点之间的汽车路线 (中文)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Berlin" "Hamburg"

# 自行车 (中文)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Potsdam" "Berlin" --modus fahrrad

# 步行 (中文)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Kreuzberg, Berlin" "Mitte, Berlin" --modus fuss

# 直接使用坐标 (lat,lon) (中文)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "52.5200,13.4050" "53.5500,9.9937"

# JSON 输出 (中文)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Munich" "Vienna" --json

# 帮助 (中文)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py --help
```

---

## 模式

| 模式 | 别名 | OSRM 配置 |
|---|---|---|
| auto（默认） | car, pkw, fahren | driving |
| fahrrad | bike, rad, radfahren | cycling |
| fuss | foot, laufen, gehen, zu fuss | foot |

---

## 存储

无持久化存储。路线不会被保存。

---

## 行为准则

- 在计算之前始终明确说明起点和终点。
- 如果地点存在歧义，请进行澄清（例如“维也纳”是奥地利首都还是同名城市？）。
- 注意：OSRM 提供的是最快路线，不包含实时路况。
- 对于非常长的步行路线（> 20 千米），给出提示。

---

## 隐私与数据保护

请求将发送至 `nominatim.openstreetmap.org`（地理编码）和
`router.project-osrm.org`（路线规划）。无需登录、无需 API 密钥、
无持久化数据存储。

---

## 相关资源

- `location-suche` — POI 搜索（同样使用 Nominatim）
- `wetter` — 目的地的天气

---

## 变更日志

| 版本 | 日期 | 变更 |
|---|---|---|
| 1.0.0 | 2026-06-22 | 基于 BACH routing_service.py v1.0 创建；集成地理编码 |