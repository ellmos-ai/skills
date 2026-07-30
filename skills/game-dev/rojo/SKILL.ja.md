---
name: rojo
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: Rojo の操作 — Studio エディタの代わりに VS Code / Claude Code でプロフェッショナルな Roblox 開発を行うための、ファイルシステムから Roblox Studio への同期ツール。`rojo serve`/`rojo build`、`default.project.json` の記述やデバッグ、rokit/rokit.toml とツールバージョン（Rojo, Lune, Wally）、ネスト vs フラットパス配備（ReplicatedStorage.Project.shared）、接続/ポート/同期のトラブル、または Roblox プロジェクトのスケルトンを作成する際など、Rojo が関わるすべての場面でこの skill を使用します。「rojo connect が動かない」、「Studio でスクリプトが間違った場所に入る」、「src/ を Studio にマッピングする方法」、「ポート 34872 が使用中」、「Rojo での ModuleScript と Script の違い」といった指示でもトリガーされます。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [rojo, roblox, luau, rokit, wally, lune, sync, build, gamedev]
language: ja
status: active
dependencies: {'tools': ['rojo', 'rokit'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rojo/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="rojo banner">

> **日本語** — `rojo` の公式日本語版。


# Rojo — ファイルシステム → Roblox Studio 同期

## 概要と目的

Rojo は、通常のファイルシステムプロジェクト（Git でバージョン管理された `src/` 内の `.luau` ファイル）
を Roblox Studio に接続します。お好みのエディタ（VS Code、Claude Code）でコードを記述すると、Rojo
が実行中の Studio インスタンスへリアルタイムで同期します。これにより、内蔵の Studio スクリプトエディタに
依存せず、本物のアプローチで Roblox コードをバージョン管理、Diff 比較、編集できるようになります。

Rojo のセットアップ、`default.project.json` のマッピング、ツールチェーン（rokit/Wally/Lune）、
および一般的な同期トラブル全般にこの skill を使用してください。

## メンタルモデル

```
VS Code / Claude Code          rojo serve            Roblox Studio
   src/server/*.luau   ──────►  (localhost:34872) ──►  ServerScriptService.*
   src/client/*.luau            Live-Sync               StarterPlayerScripts.*
   src/shared/*.luau                                    ReplicatedStorage.*
   src/gui/*.luau                                       StarterGui.*
```

**核心ルール：** ファイルシステムが唯一の正しい情報源（Source of Truth）です。接続のたびに、Rojo は
マッピングされた Studio 領域をファイルシステムの内容で上書きします。したがって、Studio 内でコードを
直接編集しないでください（次の同期で失われます）。必ずエディタ側で編集してください。`Workspace`
（3D シーン、地形）は Rojo のマッピング対象外であり保持されます — シーンとコードのワークフローについては
`/rbx-studio` skill を参照してください。

## ファイル拡張子 → Roblox タイプ（Rojo の規約）

Rojo は拡張子からインスタンスタイプを推測します。これは最も頻繁に発生するエラーの原因です：

| ファイル           | Roblox タイプ | `require()` 可能 | 役割                      |
| ------------------ | ------------- | --------------- | ------------------------- |
| `Foo.luau`         | ModuleScript  | **はい**        | ロジックモジュール、定義  |
| `Foo.server.luau`  | Script        | いいえ          | サーバーエントリーポイント |
| `Foo.client.luau`  | LocalScript   | いいえ          | クライアントエントリーポイント |
| `init.luau`        | フォルダノード自体になる | はい  | フォルダを ModuleScript 化 |

> 経験則： `.server.luau`/`.client.luau` にするのは**エントリーポイントのみ**です。
> `require()` 経由で読み込まれるすべてのファイルは `.luau` ModuleScript でなければなりません。
> Script/LocalScript に対して `require()` を呼び出すと "Attempted to call require with invalid argument(s)" エラーが発生します。

## CLI コマンド

```bash
rojo serve default.project.json     # ライブ同期サーバーの起動（デフォルトポート 34872）
rojo serve                          # default.project.json を自動使用
rojo build default.project.json -o game.rbxlx   # 単一ビルド → Place ファイル (XML)
rojo build default.project.json -o game.rbxl    # 単一ビルド → Place ファイル (バイナリ)
rojo plugin install                 # Rojo Studio プラグインのインストール（初回のみ）
rojo --version                      # インストールされているバージョンの確認
```

`rojo serve` 実行後：Studio で Rojo プラグインを開き → **Connect** (localhost:34872)。
`rojo build` は Studio の実行を必要としないため、CI、スモークテスト、リリースに最適です。

## `default.project.json` — マッピング

このファイルは、ファイルシステムのパスを Roblox データモデルの階層にマッピングします。キー：

- `name` — プロジェクト名（表示用）
- `$className` — ノードの Roblox クラス（`DataModel`, `ServerScriptService`, `Folder` …）
- `$path` — このノードの下に同期されるファイルシステムパス（プロジェクトルートからの相対パス）

すぐに使用できる標準テンプレートは [`assets/default.project.json`](assets/default.project.json) にあります。

### フラット vs ネスト — 最も重要な決定

コードはマッピングと一致させる必要があります。2つのバリエーション：

**フラット（Flat）** — `src/server` の内容が `ServerScriptService` の直下に配置されます：
```json
"ServerScriptService": { "$className": "ServerScriptService", "$path": "src/server" }
```
→ コードの参照例：`ReplicatedStorage.Config`, `ReplicatedStorage.GameEnums`。

**ネスト（Nested）** — 内容が `ServerScriptService.ProjectName` の下に配置されます：
```json
"ServerScriptService": {
  "$className": "ServerScriptService",
  "ProjektName": { "$path": "src/server" }
}
```
→ コードの参照例：`ReplicatedStorage.ProjectName.shared.Config` など。

どちらも有効です。プロジェクト全体で**いずれか 1 つ**のパターンに決め、すべての
`require`/`WaitForChild` パスで整合性を保ってください。不一致時の症状：期待するノードが
別の場所に存在するため、`WaitForChild(...)` が無制限に停止（infinite yield）します。

## rokit によるツールチェーン

[rokit](https://github.com/rojo-rbx/rokit) はツールチェーンマネージャーです。プロジェクト（または親フォルダ）の
`rokit.toml` で正確なツールバージョンを固定し、すべての環境で再現可能なビルドを実現します。
不足している場合、`Failed to find tool 'rojo' in any project manifest file` エラーが表示されます。

標準の `rokit.toml`（[`assets/rokit.toml`](assets/rokit.toml) を参照）：
```toml
[tools]
rojo = "rojo-rbx/rojo@7.4.4"
lune = "lune-org/lune@0.10.4"
wally = "UpliftGames/wally@0.3.2"
```

> バージョンに関する注意点：7.4.4 はリファレンスパイプライン全体で一貫して固定されているバージョンです。
> 新しいプロジェクトでは 7.6.x を使用できますが、メジャーバージョン間でプロジェクトフォーマットが変更される可能性があるため、まずは `rojo build` でプロジェクトに対して動作確認を行ってください。

クローン/セットアップ後：`rokit install` を実行して固定されたすべてのツールを取得します。

- **Lune** — Studio 外部の Luau ランナー（単体テスト、ビルドスクリプト、アセット処理）。
- **Wally** — パッケージマネージャー：`wally install` → `Packages/` → Studio 内の
  `ReplicatedStorage.Packages` に配置されます。依存関係は `wally.toml`（[`assets/wally.toml`](assets/wally.toml)
  を参照）に記述します（例：フレームワーク `sleitnick/knit@1.7.0`）。

## 新しいプロジェクトの作成

スクリプト [`scripts/scaffold_roblox_project.sh`](scripts/scaffold_roblox_project.sh) は
完全な Rojo スケルトン（project.json, rokit.toml, wally.toml, 初期ファイルを含む
`src/{shared,server,client,gui}/`、KONZEPT スタブ）を作成します：

```bash
bash scripts/scaffold_roblox_project.sh MeinSpiel        # フラットマッピング（デフォルト）
bash scripts/scaffold_roblox_project.sh MeinSpiel --nested   # ネストマッピング
```

実行後：`cd MeinSpiel && rokit install && rojo serve`。

## トラブルシューティング

| 症状 | 原因 | 解決策 |
| --- | --- | --- |
| `Failed to find tool 'rojo'` | `rokit.toml` が存在しない | プロジェクトまたは親フォルダに Rojo のバージョンを固定した `rokit.toml` を作成し、`rokit install` を実行 |
| `require` が "invalid argument(s)" をスローする | Script/LocalScript に対して `require()` を実行した | `.luau` ModuleScript のみ require 可能です。拡張子を確認してください |
| ポート 34872 が使用中 (`os error 10048`) | 古い Rojo プロセスが実行中 | `tasklist \| grep -i rojo` → `taskkill //PID <PID> //F` を実行し、再度 `rojo serve` を実行 |
| スクリプトが Studio 内の間違った場所に配置される | ネストではなくフラットマッピング（またはその逆）になっている | `default.project.json` をコードのパスに合わせて調整（上記参照） |
| `WaitForChild` が無制限に停止する | 期待するノードが存在しない / 生成前にサーバーエラーが発生 | **最初にサーバーコンソールのエラーを確認してください**。マッピングと生成順序を確認します |
| ファイル名変更後に同期が停止する | Rojo が名前変更を即座に検知できない | サーバーを停止（Ctrl+C）して再起動し、Studio で Disconnect → Reconnect を実行 |
| 再接続後に Studio での変更が消える | ファイルシステムではなく Studio で編集した | コード変更は**エディタ側でのみ**行ってください。Rojo はマッピング領域を上書きします |

### Rojo の既知の制限事項

1. **地形/Workspace の同期非対応** — 3D シーンと地形は Studio 内で構築するか、コードで動的に生成します。
2. **`.rbxl` のマージ非対応** — Place ファイルはバイナリであり git マージできません。プライマリソースとして使用しないでください。
3. **Play モード中のライブ同期非対応** — 実行中に行った変更は Stop 時に破棄されます。
4. **Git Bash のパス変換問題** — `/c/...` が `C:/...` に変換され Rojo パスが壊れることがあります。不安な場合は相対パスまたはネイティブ Windows パスを使用してください。

## リンティング（Selene）

Roblox Luau プロジェクトは通常 **Selene**（ルートに `selene.toml`、`std = "roblox"`）で
リンティングされます。プロジェクトが共有クライアント状態のために `_G` を使用している場合は、
`global_usage = "allow"` でグローバル変数を許可します。Roblox API 定義（`roblox.yml`）が含まれるディレクトリから Selene を実行してください。

## 参考文献

- 関連 skill：`/rbx-studio`（Studio 操作、MCP、アセット）、`/game-design`
  （役割、ワークフロー、GDD）、メタ skill `/rbx-dev`（上記 3 つとアーキテクチャパターンを統合）。
- 最新のエンジン/Rojo ドキュメント：Context7 MCP（`resolve-library-id` →
  `/websites/create_roblox_reference_engine`, `/roblox/creator-docs`）または
  <https://rojo.space/docs/>。
- 本システムに存在する場合、プロジェクト豊富なリファレンスパイプラインは
  `<your Roblox project pipeline>` にあります（`ROJO_FAQ.md`, `SKILL.md` を含む）。

## 変更履歴

### 1.0.0 (2026-06-17)
- 初版。.ROBLOX パイプライン（ROJO_FAQ, ROJO_START, _template）から抽出され、中立的な表現で記述されました。