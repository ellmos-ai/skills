---
name: rbx-dev
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: Rojo を使用した Roblox ゲーム開発全般のためのメタスキル — 3つの専門スキル `/rojo`（ファイルシステム→Studio 同期、プロジェクト設定）、`/rbx-studio`（エディタ、MCP、アセット、マルウェアスキャン）、および `/game-design`（役割、ワークフロー、GDD）を理解・統一するエントリーポイントです。Roblox ゲームの計画/構築/設定、新規プロジェクトのスケルトン作成、コードアーキテクチャの定義（Main + マネージャーモジュール、_G.ClientState + HUD、GameEnums 内の Remotes）、Luau/Roblox の落とし穴の回避、またはどの Roblox 専門スキルが適しているか不明な場合に、このスキルを使用してください — ルーティングはここから行われます。「Roblox ゲームを開発する」、「Roblox ゲームを構築する」、「新規 Roblox プロジェクト」、「Luau プロジェクト構造」、「Roblox コードの組織化方法」、「Roblox 開発セットアップ」などのトリガーでも使用します。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [roblox, luau, rojo, studio, game-design, architektur, meta, gamedev]
language: ja
status: active
dependencies: {'tools': ['rojo', 'rokit'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rbx-dev/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **日本語** — `rbx-dev` の公式日本語版。

> **注記:** Roblox Corporation との提携はありません。「Roblox」は所有者の商標です。「rbx」は一般的なコミュニティの略称です。

# Roblox-Dev — Roblox ゲーム開発のためのメタスキル (日本語)

## 概要と目的

Rojo ベースのバージョン管理可能なワークフローによる Roblox ゲーム開発の central entry point です。
このスキルは、プロジェクト構造、アーキテクチャパターン、最も重要な Luau の落とし穴といった包括的な知識を統合し、専門的な質問を以下の3つのサブスキルにルーティングします。

| サブスキル | 用途 |
| --- | --- |
| **`/rojo`** | ファイルシステム→Studio 同期、`default.project.json`、rokit/Wally/Lune、プロジェクトスケルトン、同期の問題 |
| **`/rbx-studio`** | Studio の操作、シーン vs コードモード、Studio MCP、アセットパイプライン、**マルウェアスキャン** |
| **`/game-design`** | 役割とサブタスク、開発チェーン、ゲームデザインドキュメント（KONZEPT.md）、マルチエージェント |

> ルーティングルール：**同期/ビルド/セットアップ**に関する場合 → `/rojo`。**Studio でのエディタ/アセット/テスト**に関する場合
> → `/rbx-studio`。**コンセプト/役割/プロセス**に関する場合 → `/game-design`。**コードアーキテクチャ、
> Luau の落とし穴、または全体のフロー**に関する場合 → このスキルにとどまります。

## スタックの概要

- **言語:** Luau（`.lua` ではなく `.luau`）。コードは英語、コメント/ドキュメントは日本語、UI テキストは対象言語。
- **同期:** rokit 経由の Rojo（ツールバージョンをピン留め）。ファイルシステム = 唯一の真実のソース（source of truth）。
- **ツール:** Rojo（同期/ビルド）、Lune（Studio 外でのテスト/スクリプト）、Wally（パッケージ）、
  オプションで Knit（サービス/コントローラーフレームワーク、新規プロジェクト）、Selene（リンター）。
- **制御:** AI 駆動による検査/テスト/アセット挿入のための Roblox-Studio-MCP。

## プロジェクト構造 (標準)

```
ProjektName/
├── default.project.json     # Rojo-Mapping
├── rokit.toml               # gepinnte Tool-Versionen
├── wally.toml               # Package-Dependencies
├── KONZEPT.md               # Game Design Document
├── src/
│   ├── shared/              # → ReplicatedStorage(.ProjektName.shared)
│   │   ├── Config.luau      # zentrale Werte, States, Gameplay-Parameter
│   │   ├── GameEnums.luau   # Enums, Remote-Namen, Konstanten
│   │   └── *Defs.luau       # Datendefinitionen (Items, Einheiten, Level)
│   ├── server/              # → ServerScriptService(.ProjektName)
│   │   ├── Main.server.luau # EINZIGER Server-Entry-Point (Script)
│   │   └── *Manager.luau    # ModuleScripts, von Main per require() geladen
│   ├── client/              # → StarterPlayerScripts(.ProjektName)
│   │   └── GameClient.client.luau   # Client-Entry-Point (LocalScript)
│   └── gui/                 # → StarterGui(.ProjektName)
│       └── *HUD.client.luau # GUI-Aufbau + Heartbeat-Loop
└── assets/                  # optionale .rbxm/.rbxl (scriptfrei)
```

スケルトンは `/rojo` が `scaffold_roblox_project.sh` 経由で作成します。

## アーキテクチャパターン

**サーバー — Main + マネージャーモジュール。** プロジェクトにつき Script は **1つ** のみ：`Main.server.luau`。これが
remotes フォルダーを集中作成し、`require()` を介してすべての機能モジュールを読み込みます：
```lua
Main.server.luau (Script)
  ├─ require(StationManager)     -- .luau ModuleScripts
  ├─ require(PlayerSession)
  └─ erstellt RemoteEvents → verbindet OnServerEvent-Handler
```
他のすべてのサーバーファイルは `.luau`（ModuleScripts）です。

**クライアント — 共有状態 + HUD。** GameClient が共有状態を書き込み、HUD が
Heartbeat でそれを読み取ります：
```lua
-- GameClient:
_G.ClientState = { gameState = "Lobby", health = 100 }
-- HUD:
RunService.Heartbeat:Connect(function()
    local cs = _G.ClientState; if not cs then return end
    healthBar.Size = UDim2.new(cs.health / cs.maxHealth, 0, 1, 0)
end)
```

**Remotes — GameEnums に一元化。** リモート名を `GameEnums.Remotes` に一度だけ定義します。
サーバーはそれらからイベントを作成し、クライアントは同じ名前でそれらを検索します。これにより、
サーバーとクライアント間での文字列の不一致を防ぎます。

## ゲームの全体的なフロー

1. **コンセプト** (`/game-design`)：KONZEPT.md — ジャンル、USP、3〜4のコアメカニクス、マネタイズ。
2. **セットアップ** (`/rojo`)：スケルトンを作成し、`default.project.json` のマッピングを定義。
3. **バックエンド**：Config → GameEnums → *Defs → Main.server → *Manager。
4. **フロントエンド**：GameClient → HUD。
5. **グレーボックステスト** (`/rbx-studio`)：ゲームプレイ優先、パーツ + 必要に応じて AI マテリアル。
6. **アセットのアップグレード** (`/rbx-studio`)：Creator Store アセット、**マルウェアスキャン**、.rbxl としてのシーン。
7. **テスト** (`/game-design`)：QA + ゲーム批評家 + ペルソナブラインドテスト、イテレーション。
8. **リリース** (`/game-design` ビジネス役割)：ストアページ、マネタイズ、ライブオプス。

## Luau/Roblox の落とし穴 (ショートリスト)

最も一般的な落とし穴 — アノテーション付きの完全なリスト：
[`references/lessons-learned-luau.md`](references/lessons-learned-luau.md)。

- 同じ行にさらにコードが続く場合、`task.wait(x)` の後にセミコロンを付ける。
- `Model.Position` は存在しない → `model:GetPivot().Position` を使用。
- 辞書型に対する `#table` は 0 → 手動でカウント。
- `mouse.Hit` は nil になる可能性がある → 使用前に確認。
- DataStore の呼び出しは**常に** `pcall` 内で行う。
- `tick()` は非推奨 → `os.clock()`；`SetPrimaryPartCFrame` → `PivotTo` を使用。
- イベント名は `GameEnums.Remotes` に一元化；すべての RemoteEvent は `Main.server.luau` で作成。
- 循環 `require` は禁止（デッドロックが発生します）。
- `require()` は `.luau` ModuleScripts でのみ使用し、Scripts/LocalScripts では絶対に使用しない。

## 各コミットの前 (チェックリスト)

- [ ] 複数ステートメントの行で `task.wait(...)` の後にセミコロンがあるか
- [ ] `Model.Position`、`tick()`、`SetPrimaryPartCFrame` を使用していないか
- [ ] DataStore が `pcall` 内にあり、`mouse.Hit` の nil チェックが行われているか
- [ ] イベント名がサーバー↔クライアント間で一致しているか（GameEnums 経由）
- [ ] すべての RemoteEvents が `Main.server.luau` で作成されているか
- [ ] 循環 require がないか
- [ ] マーケットプレイスのアセットがスキャンされ（`/rbx-studio` → マルウェアスキャン）、レポートが記録されているか

## 知識ソース

- **現在のエンジン/クリエイタードキュメント:** Context7 MCP — `resolve-library-id` →
  `/websites/create_roblox_reference_engine`（エンジン API）および `/roblox/creator-docs`
  （チュートリアル/ガイド）；フォールバック <https://create.roblox.com/docs>。
- **リファレンスパイプライン**（このシステムに存在する場合）: `<your Roblox project pipeline>` —
  `SKILL.md`、`GUIDE.md`、`LESSONS_LEARNED.md`、`ROJO_FAQ.md`、`ROBLOX_MCP_FAQ.md`、
  `AGENT_ROLES.md`、`_malware_reports/PATTERNS.md`、`_knowledge/`（ローカル API キャッシュ）を含む。

## 変更履歴

### 1.0.0 (2026-06-17)
- 初版。`/rojo`、`/rbx-studio`、`/game-design` を統括するメタスキル。`.ROBLOX` パイプラインから抽出したプロジェクト構造、アーキテクチャパターン、Luau の教訓をユーザー中立で記述。