---
name: rbx-studio
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: ゲーム開発のための Roblox Studio 操作ガイド —— 3D シーンの構築、テスト、パブリッシュを行うビジュアルエディタ。このスキルは以下をカバーします：Studio の基本（Explorer、Workspace、プレイテスト、Place の .rbxl 保存）、Rojo との連携（Connect、シーンモード vs. コードモード）、Roblox-Studio-MCP による AI 制御（execute_luau、insert_from_creator_store、generate_material、screen_capture、Play/Stop、Console 読み取り）、完全なアセットパイプライン（Creator Store → クリーニング → キット化 → シーン構築 → .rbxl → Rojo による動力化）、そして何よりもマーケットプレイスアセットに対する必須のマルウェアスキャン。「Store からアセットを挿入」、「Studio MCP が動作しない」、「studios: []」、「マテリアル生成」、「シーン保存」、「この Roblox アセットは安全か」、「Play 後にスクリプトが消える」などのトリガーにも対応。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [roblox, studio, mcp, assets, creator-store, malware, luau, gamedev]
language: ja
status: active
dependencies: {'tools': ['rojo'], 'services': ['roblox-studio-mcp'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rbx-studio/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **日本語** — `rbx-studio` の公式日本語版。

> **Note:** Not affiliated with Roblox Corporation; "Roblox" is a trademark of its owners. "rbx" is the common community shorthand.

# Roblox Studio — エディタ、テスト、アセット、MCP

## 概要と目的

Roblox Studio は公式エディタです。3D シーンの構築、Play モードでのゲームのテスト、
Creator Store からのアセット挿入、および Place のパブリッシュを行います。Rojo ワークフローにおいて、
Studio は **シーン**（Workspace、Terrain、配置されたモデル）と **テスト** を担当し、
**コード** はファイルシステムから Rojo を介して提供されます（スキル `/rojo` を参照）。

本スキルでは、Studio の基本、シーン作業とコード作業の明確な分離、
Roblox-Studio-MCP による AI 制御、およびすべてのマーケットプレイスアセットに対する
**必須のマルウェアスキャン**を含むアセットワークフローについて説明します。

## 基本操作

- **Explorer** — すべてのインスタンスのツリー構造（Workspace、ServerScriptService、ReplicatedStorage など）。
  Rojo がアクティブな場合、マッピングされた領域はファイルシステムからリアルタイムで反映されます。
- **Play-Test（プレイテスト）** — 緑色の Play ボタン（または F5）でローカルサーバー+クライアントセッションを開始します。
  開始するたびに、**Output コンソールでエラーを確認する** ことが最も重要なデバッグ習慣です。
- **Place の保存** — File → Save As → `.rbxl`（バイナリ）または `.rbxlx`（XML、diff 可能）。
  保存された Place には **シーン** が含まれます。コードは Place 内ではなくファイルシステムに存在します。

## 重要なワークフロー：シーンモード vs コードモード

Connect 実行時、Rojo はマッピングされたすべてのスクリプト領域をファイルシステムの内容で上書きします。
`Workspace`（3D シーン）はマッピングされて**おらず**、そのまま維持されます。ここから日常の作業における
最も重要なルールが導き出されます —— 2つのモードを絶対に混同しないでください。

**モード A — シーンの編集（Rojo OFF）：**
1. Rojo サーバーを停止します（`taskkill //F //IM rojo.exe` または Ctrl+C）。
2. Studio で Place を開き、アセットを配置し、ワールドを構築・配置します。
3. File → Save → `.rbxl` に新しいシーンが保存されます。

**モード B — コードのテスト（Rojo ON）：**
1. Studio で同じ Place を開きます。
2. `rojo serve` を起動 → Studio の Rojo プラグインで Connect をクリック。
3. Play を押してテストします。Rojo がスクリプトを同期し、Workspace は `.rbxl` から読み込まれます。
4. Rojo の実行中は **保存しないでください**（Rojo の状態が `.rbxl` 内に固定化されてしまうため）。

これにより、シーン作業（Studio）とコード作業（エディタ + Rojo）を並行して衝突なく
実行できます —— アーティストはシーンを構築し、デベロッパーはコードを書きます。

## Roblox-Studio-MCP — AI による Studio 制御

Roblox-Studio-MCP を使用すると、Claude/Gemini/Codex が **実行中** の Studio インスタンスを
直接制御できます（コード実行、プロパティ検査、Play/Stop、コンソール読み取り、アセット挿入）。
Rojo を置き換えるものでは**なく**、補完するものです：永続的なコード変更には Rojo、
検査、テスト、アセット挿入、マテリアル生成には MCP を使用します。

```
エディタ + Rojo  ──(永続的なコード同期)──►  Studio (実行中)  ◄──(検査/テスト/挿入)──  MCP ◄── AI
```

### 利用可能な MCP ツール（代表例）

| ツール | 用途 |
| --- | --- |
| `list_roblox_studios` / `set_active_studio` | 開いているインスタンスのリスト表示 / アクティブなインスタンスを選択 |
| `search_game_tree` / `inspect_instance` | 階層の検索 / プロパティの読み取り |
| `execute_luau` | Studio 内で直接 Luau コードを実行 |
| `script_read` / `script_grep` / `script_search` | スクリプトの解析 |
| `multi_edit` | 複数のインスタンス/スクリプトをバッチ変更 |
| `start_stop_play` | Play/Stop の制御 |
| `get_console_output` | Output ログの読み取り |
| `screen_capture` | シーンのスクリーンショット撮影 |
| `insert_from_creator_store` | Creator Store からアセットを挿入 |
| `generate_material` | AI マテリアル/テクスチャ (MaterialVariant) を生成 |
| `character_navigation` / `user_keyboard_input` / `user_mouse_input` | 入力をシミュレート |

### セットアップ（ユーザー非依存）

MCP は Studio に同梱されているサーバーとして動作し、多くの場合、軽量な JSON フィルタリングラッパーを介して接続されます
（一部のクライアントが解析できない非 JSON バナーをフィルタリングします）。

- MCP バッチ (Windows): `%LOCALAPPDATA%\Roblox\mcp.bat`
- オプションのラッパー: `<your roblox-mcp wrapper>`
  （このシステムに存在する場合。Claude/Codex/Gemini で共有）
- クライアント設定: `~/.claude/mcp.json` · `~/.codex/config.toml` · `~/.gemini/antigravity/mcp_config.json`

設定例 (`~/.claude/mcp.json`):
```json
{
  "mcpServers": {
    "Roblox_Studio": {
      "command": "node",
      "args": ["<your roblox-mcp wrapper>",
               "cmd.exe", "/c", "%LOCALAPPDATA%\\Roblox\\mcp.bat"]
    }
  }
}
```

### よくある MCP の問題

| 症状 | 意味 / 対策 |
| --- | --- |
| `studios: []` または `Not connected to WS host` | すぐに「故障」したわけではありません：`initialize` を送信 → 2〜3 秒待機 → `list_roblox_studios`。解決しない場合は Studio を再起動 |
| `Error: connection closed: initialized request` | Studio が開いていません — Studio を起動し、Place をロードして再試行してください |
| MCP 経由で作成したスクリプトが Play/Stop 後に消える | MCP によるコード編集は永続的ではありません — 永続的なコード変更には **Rojo** を使用してください |
| プラグイン VM 内で `require()` 経由の値が不正 | プラグイン VM は独自の require キャッシュを持っています — 確認するには `.Source` を直接読み取るか、Play 後のサーバーログを確認してください |

## アセットパイプライン（Creator Store → ゲーム）

まずグレイボックス（ゲームプレイ検証）、後からアセット（リリース前）。実績のある手順：

```
ストア検索       → 例: "medieval" → 複数の候補を読み込む
選別             → スタイルが合わないものや粗悪なものを除外し、適した 5〜8 個を保持
クリーンアップ   → すべてのスクリプトを削除（マルウェア対策！）、形状/メッシュのみ保持
キット / セット作成 → ベースアセットからバリエーションを作成（同じマテリアル/比率を維持）
シーン構築 (Studio) → アセットを組み合わせて背景・世界を作成（村、アリーナ、公園など）
.RBXL として保存 → 作成した背景が「舞台」となる
ROJO で動的化    → スクリプト / ゲームプレイ / HUD は Rojo 経由で追加。Workspace は変更しない
```

**バリエーション手法（「モジュール式キット」）：** 優れたベースアセットを1つ選び、
そこからセット全体を作成します（家 → 塔、納屋、鍛冶屋、廃墟）。これらはすべてマテリアル、色、
比率を共有しているため、プロの開発スタジオと同様に、最小限の労力で統一感のある外観を実現できます。

**アセットの取得元（優先順位）：** Creator Store（無料、膨大、**マルウェアチェック必須**） →
AI マテリアル（`generate_material`） → 自作メッシュ（Blender → .fbx） → 購入したアセットパック。

## 必須：マーケットプレイスアセットのマルウェアスキャン

Creator Store のアセットには、難読化された悪意のあるスクリプト（バックドア、リモートコード、
ボットネットワークのフック）が含まれている可能性があります。使用前にインポートした**すべて**のアセットを
スキャンし、すべてのスクリプトを削除して、形状/メッシュのみを保持してください。

- パターン参照：[`references/malware-patterns.md`](references/malware-patterns.md) — 既知の8つの
  難読化パターン（反転属性ペイロード、偽のシステムスクリプト、リモート
  `require()`、`loadstring`、`string.char`、`getfenv/setfenv`、非表示の Values、遅延実行）。
- スキャナー：[`scripts/scan_asset_malware.luau`](scripts/scan_asset_malware.luau) — Studio 内で
  `execute_luau`（または Command Bar）を実行して使用します。すべてのパターンに対してインスタンスをチェックし、検出結果を報告します。

**即座の警戒信号（レッドフラグ）：** 純粋な装飾モデル内の大きなスクリプト · 属性内の反転文字列 ·
`require(<number>)` · `loadstring` · ネットワーク機能を必要としないアセット内の `HttpService`。
疑わしい場合はスクリプトを削除してください。検出結果を記録します（例: リファレンスパイプライン内の `_malware_reports/YYYY-MM-DD_*.md`）。

## 重要な Luau/Studio の注意点（抜粋）

Studio で最も頻繁に発生する問題 —— 完全なリストはスキル `/rbx-dev` で管理されています：

- `Model.Position` は存在しません → `model:GetPivot().Position` を使用。
- `tick()` は非推奨です → `os.clock()` / `workspace:GetServerTimeNow()` を使用。
- `SetPrimaryPartCFrame()` は非推奨です → `model:PivotTo(cf)` を使用。
- DataStore の呼び出しは**必ず** `pcall` 内で行ってください。
- Baseplate と手動/動的生成した床が同じ高さ → Z-fighting（ちらつき）：Baseplate を削除するか、
  床を +0.1 studs 上げます。
- パーツバジェットに注意してください（手動/動的生成される部屋1つあたり約50〜80パーツ）。

## 参考文献・関連情報

- 関連スキル：`/rojo`（同期、プロジェクト設定）、`/game-design`（役割、ワークフロー、GDD）、
  メタスキル `/rbx-dev`（アーキテクチャパターン + すべての Luau のレッスン）。
- エンジン/クリエイタードキュメント：Context7 MCP（`/websites/create_roblox_reference_engine`、
  `/roblox/creator-docs`）または <https://create.roblox.com/docs>。
- リファレンスパイプライン（存在する場合）：`<your Roblox project pipeline>`
  （`ROBLOX_MCP_FAQ.md`、`ASSET_PIPELINE.md`、`_malware_reports/PATTERNS.md`）。

## 変更履歴

### 1.0.0 (2026-06-17)
- 初版。.ROBLOX パイプライン（ROBLOX_MCP_FAQ、ASSET_PIPELINE、
  PATTERNS、LESSONS_LEARNED）から抽出され、ユーザー非依存の記述に整理。