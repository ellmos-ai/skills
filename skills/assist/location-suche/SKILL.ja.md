---
name: location-suche
version: 1.0.0
category: assist
description: OpenStreetMap（Nominatim + Overpass API）を使用した場所、レストラン、ホテルの検索。指定位置周辺の POI（Point of Interest）を返したり、フリーテキストで検索します。
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
language: ja
---

<img src="banner.png" width="100%" alt="location-suche banner">

> **日本語** — `location-suche` の公式日本語版。


# 場所検索 (日本語)

**OpenStreetMap を使用した場所・レストラン・ホテル検索**

---

## 概要と目的

OpenStreetMap のサービスである Nominatim（ジオコーディング）と Overpass（POI 検索）を
使用して、レストラン、ホテル、カフェなどの場所を検索します。
API キーは不要です。永続ストレージはありません。

---

## トリガー

| フレーズ | アクション |
|---|---|
| "Find a restaurant in Munich"（ミュンヘンのレストランを探す） | POI 検索：category=restaurant, near=Munich |
| "Hotels near Vienna"（ウィーン周辺のホテル） | POI 検索：category=hotel, near=Vienna |
| "Where is the Eiffel Tower?"（エッフェル塔はどこ？） | Nominatim フリーテキスト検索 |
| "Find cafes in Berlin"（ベルリンのカフェを探す） | POI 検索：category=cafe, near=Berlin |
| "Search for pharmacy near Potsdam"（ポツダム周辺の薬局を検索） | POI 検索：category=pharmacy, near=Potsdam |

---

## ワークフローと手順

1. **トリガーの検出:** リクエストにカテゴリ（レストラン、ホテルなど）
   と場所が含まれているか確認 → ステップ 2。含まれていない場合はフリーテキスト → ステップ 4。
2. **場所のジオコーディング:** Nominatim が指定された場所の座標を取得します。
3. **POI 検索:** Overpass API が指定検索半径内にある該当カテゴリの施設を検索します。
4. **結果の表示:** 名称、住所、距離（m）のリストを表示します。
5. **フリーテキスト検索（フォールバック）:** Nominatim フリーテキスト検索により直接一致する結果を取得します。

---

## CLI

```bash
# POI search (category + location) (日本語)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py restaurant München

# Geocode location (日本語)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py --geocode "Brandenburg Gate Berlin"

# Adjust radius (default: 1000 m) (日本語)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py hotel Wien --radius 2000

# Help (日本語)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py --help
```

---

## ストレージ

永続ストレージはありません。結果は表示のみ行われ、保存されません。

---

## サポートされているカテゴリ

restaurant, cafe, bar, pub, fast_food, hotel, hostel, guest_house, supermarket,
pharmacy, hospital, bank, atm, fuel, parking, bus_stop, train_station, museum,
cinema, theatre, library, school, university, church

---

## 振る舞い・方針

- 場所が指定されていない場合は、常にユーザーに場所を確認してください。
- 検索結果が 10 件を超える場合は、最も近い 5 件のみを表示し、残りはリクエストに応じて表示します。
- 距離はメートル単位で表示し、1 km 以上の場合は km 単位（小数第 1 位まで）で表示します。
- プライバシー: 公共の Nominatim/Overpass API（openstreetmap.org）以外に
  位置データが保存または送信されることはありません。

---

## プライバシー

検索リクエストは `nominatim.openstreetmap.org` および `overpass-api.de` に送信されます。
ログイン不要、API キー不要、永続的なデータ保存なし。
User-Agent は Nominatim ポリシーに従って設定されます。

---

## 関連リソース

- `reiseroute` — A から B へのルート計画（ジオコーディングに Nominatim を使用）
- `wetter` — 現在地の天気

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|---|---|---|
| 1.0.0 | 2026-06-22 | BACH location_search.py v1.1.0 から作成。ストレージ機能を削除 |