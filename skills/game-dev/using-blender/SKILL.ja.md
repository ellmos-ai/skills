---
name: using-blender
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-06-20
updated: 2026-06-20
description: .blend、.fbx、.obj、.glb、glTF、マテリアル、シーン検査、bpy 自動化、ヘッドレス Blender バッチ実行、エクスポート/再インポート検証、プレビュー、およびオプションの Blender MCP 制御を扱う AI エージェント向けの汎用 Blender ワークフロースキル。ユーザーに依存しない方法で Blender や 3D アセットファイルを開く、検査する、作成する、自動化する、変換する、最適化する、レンダリングする、または検証するタスクで使用します。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
dependencies: {'tools': ['blender'], 'services': [], 'protocols': [], 'python': []}
category: game-dev
tags: [blender, bpy, 3d, assets, fbx, glb, gltf, mcp]
language: ja
status: active
provenance: {'origin': 'custom', 'origin_path': 'skills/game-dev/using-blender', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': 'None', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
---

> **日本語** — `using-blender` の公式日本語版。

# Blender の使用

## 基本ルール

タスクに応じて、次の 3 つのモードで Blender を操作します。

1. **GUI モード:** ユーザーがアセットの表示、確認、または手動編集を希望する場合に、Blender を画面上に開きます。
2. **ヘッドレスモード:** エクスポート、再インポート、バッチ処理、または決定論的検証が必要な場合は、`blender --background --python <script.py>` を使用します。
3. **MCP モード:** 実行中の Blender アドオンが意図的に接続されており、ライブシーン制御が必要な場合にのみ使用します。事前にセキュリティとライセンスの状況を確認してください。

## 標準ワークフロー

1. 目的の明確化: 表示、作成、変換、最適化、レンダリング、または検証。
2. 既存ファイルの事前確認: マニフェスト、README、エクスポートフォーマット、既存の検証結果を最初に確認します。
3. Blender パスの特定: PATH 上の `blender`、プロジェクト固有の設定、またはユーザーパス。公開可能なドキュメントにローカルのプライベートパスを記載しないでください。
4. 自動化には、入力、出力、およびエラーを明示する小規模な `bpy` スクリプトを使用します。
5. エクスポート後は毎回、結果を利用可能と判断する前に、少なくとも 1 回の再インポートまたは読み込みチェックを実行します。
6. 成果物を簡潔にドキュメント化: ソース、エクスポートフォーマット、ツールバージョン、検証ステータス、および既知の制限。

## エクスポートおよび検証ルール

- 一般的な Web/プレビュー用途には `.glb` を優先します。
- ターゲットワークフローで必要な場合は、ゲームエンジンや DCC 交換用に `.fbx` または `.obj/.mtl` も追加で提供します。
- ラウンドトリップ（往復）検証では常に次を確認します: ファイルが存在する、空でない、再インポート可能である、予期されるオブジェクト名/マテリアル名が存在する。
- 大規模アセットではメトリクスを収集します: メッシュ数、マテリアル、バウンディングボックス、ファイルサイズ、およびオプションでポリゴン（三角形）数。
- レンダリングチェックでは、コストのかかる Cycles や Full HD レンダリングを開始する前に、小さなプレビュー解像度を使用します。

## セキュリティルール

- `bpy` コードはファイルシステムアクセス権を持つローカル Python コードです。自作したスクリプトまたは監査済みのスクリプトのみを実行してください。
- ライセンスおよびデータプライバシーの確認なしに、外部の Blender アドオン、アセットダウンローダー、またはテレメトリサーバーを有効にしないでください。
- 任意の `execute_python` ツールを持つ MCP サーバーを使用する場合は、事前にスコープ、ネットワーク、作業ディレクトリ、およびタイムアウトを制限してください。
- マーケットプレイスまたは外部アセットについては、ライセンスを個別に確認してください。技術的に読み込み可能であることが使用権を意味するわけではありません。

## MCP オプション

ライブ制御のために Blender MCP サーバーを選択、インストール、または評価する場合は、[references/blender-mcp-review.md](references/blender-mcp-review.md) を参照してください。

## 変更履歴

### 1.0.0 (2026-06-20)
- GUI、ヘッドレス、MCP ルーティングを備えた、ユーザー非依存の初期 Blender スキル。