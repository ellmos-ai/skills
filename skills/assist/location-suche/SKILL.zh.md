---
name: location-suche
version: 1.0.0
category: assist
description: 通过 OpenStreetMap（Nominatim + Overpass API）搜索地点、餐馆和酒店。返回地点附近的兴趣点（POI）或通过自由文本进行搜索。
tags: [location, openstreetmap, poi, nominatim, overpass, restaurant, hotel]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['urllib.request', 'urllib.parse', 'urllib.error', 'json', 'time']}
runtime: python3
entry_point: location_suche_core.py
provenance: {'origin': 'BACH persoenlicher-assistent', 'origin_path': 'system/agents/persoenlicher-assistent/tools/location_search.py', 'origin_version': '1.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': 'Alle Origin-DB-Abhaengigkeiten entfernt (save_location, list_locations, _ensure_table, _get_db). Kein Store. Userneutral (keine privaten Pfade). Headless, nur Stdlib.\n'}
language: zh
---

<img src="banner.png" width="100%" alt="location-suche banner">

> **中文** — `location-suche` 官方中文版本。


# 地点搜索 (中文)

**通过 OpenStreetMap 搜索地点、餐馆和酒店**

---

## 概述与目的

使用 OpenStreetMap 服务 Nominatim（地理编码）和 Overpass（POI 搜索）
搜索餐馆、酒店、咖啡馆和其他场所。无需 API 密钥，无持久化存储。

---

## 触发词

| 短语 | 操作 |
|---|---|
| "Find a restaurant in Munich"（在慕尼黑找一家餐馆） | POI 搜索：category=restaurant, near=Munich |
| "Hotels near Vienna"（维也纳附近的酒店） | POI 搜索：category=hotel, near=Vienna |
| "Where is the Eiffel Tower?"（埃菲尔铁塔在哪里？） | Nominatim 自由文本搜索 |
| "Find cafes in Berlin"（在柏林查找咖啡馆） | POI 搜索：category=cafe, near=Berlin |
| "Search for pharmacy near Potsdam"（搜索波茨坦附近的药店） | POI 搜索：category=pharmacy, near=Potsdam |

---

## 工作流与步骤

1. **检测触发条件：** 请求是否包含类别（餐馆、酒店等）
   和地点 → 步骤 2。否则使用自由文本 → 步骤 4。
2. **地理编码地点：** Nominatim 提供指定地点的坐标。
3. **搜索 POI：** Overpass API 在半径范围内搜索该类别的场所。
4. **显示结果：** 包含名称、地址、距离（米）的列表。
5. **自由文本搜索（回退方案）：** Nominatim 自由文本搜索提供直接匹配结果。

---

## CLI

```bash
# POI search (category + location) (中文)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py restaurant München

# Geocode location (中文)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py --geocode "Brandenburg Gate Berlin"

# Adjust radius (default: 1000 m) (中文)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py hotel Wien --radius 2000

# Help (中文)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py --help
```

---

## 存储

无持久化存储。结果仅显示，不保存。

---

## 支持的类别

restaurant, cafe, bar, pub, fast_food, hotel, hostel, guest_house, supermarket,
pharmacy, hospital, bank, atm, fuel, parking, bus_stop, train_station, museum,
cinema, theatre, library, school, university, church

---

## 处理原则

- 如果未提供地点，务必询问用户具体的地点。
- 如果结果超过 10 个，仅显示最近的 5 个，其余根据请求显示。
- 距离以米为单位表示，超过 1 公里后以公里为单位（保留 1 位小数）。
- 隐私：除发送至 OpenStreetMap 的公共 Nominatim/Overpass API（openstreetmap.org）外，
  不存储或传输任何位置数据。

---

## 隐私

搜索请求发送至 `nominatim.openstreetmap.org` 和 `overpass-api.de`。
无需登录，无需 API 密钥，无持久化数据存储。
User-Agent 根据 Nominatim 策略进行设置。

---

## 相关资源

- `reiseroute` — 从 A 到 B 的路线规划（同样使用 Nominatim 进行地理编码）
- `wetter` — 当前位置的天气

---

## 更新日志

| 版本 | 日期 | 变更 |
|---|---|---|
| 1.0.0 | 2026-06-22 | 基于 BACH location_search.py v1.1.0 创建；已移除存储功能 |