---
name: compare-race
version: 1.0.0
type: pointer
author: Lukas Geiger
created: 2026-08-16
updated: 2026-08-16
description: "同じプロンプトを複数のLLMに送信し、回答を比較したいときに使用します。逐次実行（ストップウォッチ、レーンごとのクリーンな計時）または並列実行（真のレース）のいずれも可能で、モデルごとの反復回数を任意に指定できます。開始モデルが品質、正確性、網羅性、指示への忠実度、レイテンシの各観点で判定します（時間は一つの次元にすぎません）。トリガー: /compare-race、「model race」、「vergleiche modelle」、「gleicher prompt an mehrere modelle」、「モデルを比較」、「同じプロンプトを複数のモデルに」。"
standalone: true
anthropic_compatible: true
bach_compatible: false
category: dev
tags: [model-comparison, race, benchmark, multi-agent, judge, workflow]
language: ja
status: active
visibility: public
pointer: {'module_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race', 'prompt_de': 'prompts/RACE-STARTER.de.md', 'prompt_en': 'prompts/RACE-STARTER.en.md', 'config': 'config/compare-race.config.example.json', 'repo': 'github.com/ellmos-ai/compare-race'}
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['system-auditor'], 'optional_tools': [{'name': 'coma', 'path': '.AI/.MODULES/.ORCHESTRATION/coma/', 'python_module': 'coma', 'usage': 'Ausfuehrungsschicht fuer compare-race run (Spawn/Polling/Dateiprotokoll)', 'note': 'Optional. Ohne coma laeuft der modellmanuelle Weg: Spuren selbst ausfuehren und mit compare-race record einreichen.'}]}
provenance: {'origin': 'module', 'origin_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race/prompts/RACE-STARTER.de.md', 'origin_version': '0.1.0', 'last_sync_from_origin': '2026-08-16', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
translated_from_sha256: eef2d1e681ca3ed6c7fe63a8a36535632cf48a7b990fd8d944c8ef42ea046750
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:46:14.398425+00:00"
---
<img src="banner.png" width="100%" alt="compare-race banner">

# compare-race — ポインタースキル（日本語）

> **このスキルは純粋なポインターです。真実の源泉はモジュールです。**

## モジュールパス

```
<HOME>\OneDrive\.TOPICS\.AI\.MODULES\.ORCHESTRATION\compare-race\
```

リポジトリ: [github.com/ellmos-ai/compare-race](https://github.com/ellmos-ai/compare-race)

## エージェントへの指示

1. モジュールフォルダ内のロールプロンプト **`prompts/RACE-STARTER.de.md`** を読み、それに従ってください。
   あなたは RACE-STARTER であり、デフォルトでは **Judge** も兼ねます（ユーザー決定 2026-08-16）。
2. 設定を確認します（`compare-race config`、ホスト設定は `~/.compare-race/`）。
   モードを選択します: `sequential` = ストップウォッチ（レーンごとのクリーンな単独計測）· `parallel` = 真のレース。**ストップウォッチは比喩にすぎません**。時間は品質、正確性、網羅性、指示への忠実度、コストと並ぶ一つの次元です。
3. レースを開始します（`compare-race run --prompt-file …`）。coma を使わない場合は、`compare-race record` を介したモデル手動の手順を取ります。
4. Judge として、レースフォルダの `RACE.md` にあるルーブリックに記入します。各 RUN ファイルは自分で読み、自身のモデルが参加している場合は偏りを明記してください。
5. 軸の規律: 変動する軸が一つだけの場合にのみ帰属させます（model = レース · run = ばらつき · time = モデルのドリフト）。

## クォータ警告

レースは参加する **すべての** クォータ（claude/codex/agy/kimi）を消費します。大規模なレース（多数のレーン × 反復）の前に、ユーザーに確認してください。
