---
name: wetter
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: wttr.in（無料、APIキー不要）を介して、指定された場所や座標の天気に関する質問に回答します。現在の天気 + 3日間の予報。位置情報はリクエストまたは設定から取得し、オプションの短期キャッシュも利用可能です。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [wetter, wttr, vorschau, assist]
language: ja
status: active
dependencies: {'tools': ['wetter_core.py'], 'services': [], 'protocols': [], 'python': ['urllib', 'json']}
provenance: {'origin': 'bach', 'origin_path': 'system/hub/_services/weather/weather_service.py', 'origin_version': '1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **日本語** — `wetter` の公式日本語版。


# 天気 (日本語)

日常利用に最適な、キー不要で高速な天気情報。

## 概要と目的

APIキーなしで「天気はどうなる？」という質問に回答します（データソース: wttr.in）。
現在の天気（気温、体感温度、風速、湿度、UV）とコンパクトな3日間の予報を提供します。
**ユーザー中立:** コード内に固定された位置情報はありません。位置情報はリクエストまたは `assist/prefs.json` (`wetter_default_location`) から取得し、LLMがユーザーと対話的に入力します。

## トリガー

| ユーザー入力 | アクション |
|---|---|
| 「ポツダムの天気は？」/「ハンブルクの天気はどうなる？」 | `wetter_core.py "<location>"` |
| 「明日の天気は？」（位置指定なし） | `wetter_core.py --default`（prefsからの位置情報） |
| 「デフォルトの天気の場所はポツダムです」 | `wetter_core.py --set-default "Potsdam"` |
| 座標が判明している場合 | `wetter_core.py <lat> <lon>` |

## ワークフローと手順

```
1. 位置の決定：リクエストから取得。なければ prefs.json (wetter_default_location) から取得。
   それもなければユーザーに対話形式で確認し、必要に応じてデフォルトとして保存。
2. wetter_core.py の呼び出し (wttr.in, リトライ2回, 30分キャッシュ)。
3. 読みやすい形式で天気情報と3日間の予報を表示。
```

## CLI エントリポイント (wetter_core.py)

```bash
python wetter_core.py "Potsdam"          # 位置
python wetter_core.py 52.6789 13.5878   # 座標
python wetter_core.py --default         # prefs.json からの位置情報
python wetter_core.py --set-default "Potsdam"
```

## ストレージ (オプション)

- **必須ストレージなし。** オプションの短期キャッシュ `assist/wetter/.cache.json`
  (TTL 30分, ベストエフォート) — 繰り返しのネットワーク呼び出しを防止。
- `assist/prefs.json` (`wetter_default_location`) に位置情報の設定を保存。

## 方針

APIキー不要のデフォルトソースとして wttr.in を使用しますが、ユーザーの好みに応じて他の天気バックエンド（DWD/OpenWeatherなど）にも対応可能です。

## プライバシー

- 位置名/座標のみが wttr.in に送信されます（クエリに必須）。
- テレメトリなし、アカウント不要。キャッシュと設定はローカルに保存されます。

## 関連リソース

- `assist/AGENTS.md` — 統括ルーター
- `assist/reiseroute/` — 旅行計画での天気利用（計画中）

## 変更履歴

### 0.1.0 (2026-06-22)
- 初版。BACH `hub/_services/weather/weather_service.py` (MIT) から移植。
- 拡張機能: 位置名サポート（座標のみでない）、3日間の予報、オプションのキャッシュ、設定に基づくデフォルト位置情報。ユーザー中立。