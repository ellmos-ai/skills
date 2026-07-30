---
name: skill-finder
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-07-30
description: >
  ローカルの自作スキルのためのアクティブなファインダー／ルーター（using-superpowers に相当）。
  非定型なタスクの開始時には「常に」まずユーザーのスキルが適合するかを確認し、正しいスキルにルーティングします。
  「どのスキルが合うか」、「これ用のスキルはあるか」、「スキルを探す」、またはアドホックな作業よりも
  ローカルスキルで解決した方がよい一般的なタスクの前にアクティブ化されます。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, finder, routing, discovery, meta]
language: ja
status: active

dependencies:
  tools: []
  services: []
  protocols: [code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-finder/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="skill-finder banner">
# スキルファインダー (Skill-Finder)

## ルール

非定型なタスクを始める前に、まずローカルスキルの方が適切に解決できるかを確認してください。少しでも懸念がある場合は、適切なスキルを読み込み、**そのライブ指示に従ってください**（ファイルを読み込んで実行し、記憶に頼らないでください）。該当するスキルがない場合は、通常通り進めてください。

## ファミリー指示ルーティング

<!-- SKILL-MAP.md + inventory_skills.py から生成／更新。テーマ -> ファミリー -> スキル。
     保守：サブスキル skill-family-care または新しい skill-explorer 監査の実行。時点：2026-06-17 -->

| テーマ / 目的 | ファミリー | スキル |
|-----------------|---------|----------|
| 思考の整理／問題の分析 | 思考ツール (Denkwerkzeuge) | `/structured-thinking` (`/think` → `/brainstorm` → `/decide` に案内) |
| 新しいアイデア／創造性 | 思考ツール (Denkwerkzeuge) | `/brainstorm` (`/think` 分析、`/decide` 選択と対比) |
| 意思決定スタック | 思考ツール (Denkwerkzeuge) | `/decision-briefing` |
| 許可されたユーザー選好モデルの構築または利用 | マルチエージェント (Multi-Agent) | `build-your-users-mind`（構築）· `decision-avatar`（利用） |
| バグ／テストの失敗 | コーディング＆デバッグ (Coding & Debugging) | `/bugfix-protocol` (1 バグ)、`/bugsweep` (多数、リリース前) |
| 新規／既存のプロジェクトまたはパイプライン | プロジェクト／パイプライン | `/projekt-pipeline-umbrella` (→ bootstrapper/onboarding/optimizer) |
| Roblox ゲーム | ゲーム開発 | `/roblox-dev` (→ `/rojo`, `/roblox-studio`, `/game-design`) |
| セラピー／カウンセリング／危機対応 | セラピー | `/therapie-umbrella` (→ stabilization/guideline/counseling) |
| プレゼンテーション／スライド | オフィス | `/academic-pptx` (内容) + `/pptx` (ファイル) |
| マルチエージェント調整 | マルチエージェント (Multi-Agent) | `/swarm-operations`, `/model-strategy` |
| 応募／セルフマネジメント | 個人 | `/bewerbungsexperte`, `/selbstmanagement` |
| スキルの比較／整理／検索 | システム／メタ | `skill-explorer` (監査／探索)、`code-skill-index` (一覧) |
| システム構築／MCP 同期／エージェント連携 | システム／メタ | `/system-onboarding`, `/mcp-config-sync`, `/agents-bridge` |
| ファイルツール | ユーティリティ | `/document-chunker`, `/migrate-rename`, `/plugin-system` |
| チャット履歴 → スキルとして保存 | システム／メタ | `skill-extractor` (`/skill-extract`) |
| チャット履歴／外部自動化 → 自動化フロー | システム／メタ | `workflow-extract` (`/automations-extract`) |
| 多数のプロジェクトにわたる定期チェック | コーディング＆デバッグ | `rotation-check` (レジストリ／ログ構造) |
| 行き詰まった問題、アイデアの採掘 | 思考ツール (Denkwerkzeuge) | `idea-mining` (`/brainstorm` = 自由／広範と対比) |
| 独／英ドキュメントのバージョン同期維持 | ユーティリティ | `bilingual-doc-sync` |
| テキスト内の AI 痕跡／チャットの残り、AI 開示 | ユーティリティ | `llm-text-hygiene` |
| 依頼内の条件／タイミング／順序（「〜の時のみ」、「6時から」、「Xが完了次第」） | プロセス | `condition` (`/if` · `/when` · `/if-only` · `/after` · `/and` · `/or`) |

完全な一覧：スキル `code-skill-index`。

## レッドフラグ（STOP を意味する自己正当化）

| 考え | 現实 |
|---------|----------|
| 「簡単な質問に過ぎない。」 | 質問もタスクです —— まずスキルを確認してください。 |
| 「概念は知っている。」 | 概念を知っている ≠ スキルを使う。ライブファイルを読んでください。 |
| 「スキルを使うのは大げさだ。」 | 単純なことも複雑になります —— 使用してください。 |
| 「まずは自分で調べてみる。」 | スキルは「どのように調べるか」を教えてくれます。まず確認してください。 |

## 保守

ファミリーが変更された場合はルーティングテーブルを更新してください（サブスキル `skill-family-care` または `skill-explorer` の `inventory_skills.py` の再実行）。

## 変更履歴

### 0.2.0 (2026-07-03)
- 新しいスキルのルーティング行を追加：skill-extractor, workflow-extract, rotation-check, idea-mining, bilingual-doc-sync（Codex 自動化の抽出）。

### 0.1.0 (2026-06-17)
- 初版。監査モード ([F]) により using-superpowers の対応機能として生成。ルーティングテーブルは 2026-06-17 の監査時点（10 個のユーザーファミリー）。
