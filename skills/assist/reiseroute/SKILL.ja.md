---
name: reiseroute
version: 1.0.0
category: assist
description: OSRM（Open Source Routing Machine）を使用した A から B へのルート計画。車、自転車、徒歩に対応。API キー不要。
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
language: ja
---

<img src="banner.png" width="100%" alt="reiseroute banner">

> **日本語** — `reiseroute` の公式日本語版。


# Travel Route (日本語)

**OSRM（Open Source Routing Machine）によるルート計画**

---

## 概要と目的

パブリックな OSRM サービス（`router.project-osrm.org`）を利用して、2 つの場所
（地名または座標）間のルートを計画します。距離、移動時間、移動手段を返します。
API キーやアカウントは不要です。

---

## トリガー

| フレーズ | アクション |
|---|---|
| 「ベルリンからハンブルクへのルートを計画して」 | 車のルート、地名のジオコーディング |
| 「ミュンヘンからウィーンまで車でどのくらいかかりますか？」 | 車のルート + 時間 |
| 「ポツダムからベルリンへのサイクリングルート」 | 自転車モード |
| 「ベルリンのクロイツベルクからミッテまで徒歩で行く」 | 徒歩モード |
| 「52.52,13.41 から 53.55,9.99 へのルート」 | 直接座標 |

---

## ワークフローと手順

1. **出発地と目的地を抽出:** ユーザー入力から取得します。
2. **モードの検出:** 車（デフォルト）、自転車、徒歩。
3. **ジオコーディング:** Nominatim 経由で地名 → 座標に変換します。
4. **OSRM への問い合わせ:** 距離（km）+ 所要時間（フォーマット済み）を返します。
5. **結果の出力:** 簡潔なテキストサマリーを出力します。

---

## CLI

```bash
# 2地点間の車のルート (日本語)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Berlin" "Hamburg"

# 自転車 (日本語)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Potsdam" "Berlin" --modus fahrrad

# 徒歩 (日本語)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Kreuzberg, Berlin" "Mitte, Berlin" --modus fuss

# 座標を直接指定 (lat,lon) (日本語)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "52.5200,13.4050" "53.5500,9.9937"

# JSON 出力 (日本語)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Munich" "Vienna" --json

# ヘルプ (日本語)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py --help
```

---

## モード

| モード | エイリアス | OSRM プロファイル |
|---|---|---|
| auto（デフォルト） | car, pkw, fahren | driving |
| fahrrad | bike, rad, radfahren | cycling |
| fuss | foot, laufen, gehen, zu fuss | foot |

---

## ストレージ

永続的なストレージはありません。ルートは保存されません。

---

## 振る舞い

- 計算する前に、必ず出発地と目的地を明記してください。
- 地名にあいまいさがある場合は確認してください（例：「ウィーン」＝オーストリアの首都か同名の他の都市か？）。
- 注意: OSRM はリアルタイム交通情報を考慮しない最短ルートを提供します。
- 非常に長い徒歩ルート（20 km 超）の場合は注意を促してください。

---

## プライバシー

リクエストは `nominatim.openstreetmap.org`（ジオコーディング）および
`router.project-osrm.org`（ルーティング）に送信されます。ログイン不要、API キー不要、
データの永続保存なし。

---

## 関連リソース

- `location-suche` — POI 検索（Nominatim を使用）
- `wetter` — 目的地の天気

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|---|---|---|
| 1.0.0 | 2026-06-22 | BACH routing_service.py v1.0 から作成。ジオコーディングを統合 |