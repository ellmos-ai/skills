---
name: model-strategy
version: 2.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-06-13
description: マルチモデルオーケストレーションおよびモデル切り替え戦略。スコアベースのモデル選択、クロスエージェント委任 (Gemini, Codex, Ollama)、アドバイザーペアリング、エスカレーションのトリガー、権限マトリクス、およびコスト効率の最適化。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [model-switching, orchestration, multi-model, cost-optimization, routing, cross-agent, advisor]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/ing-strategie.md', 'origin_version': '2.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **日本語** — `model-strategy` の公式日本語版。


# モデル切り替え戦略 (Model-Switching Strategy) (日本語)

> マルチモデルオーケストレーション: スコアベースのモデル選択、クロスエージェント委任、アドバイザーペアリング、エスカレーションのトリガー、およびコスト効率の最適化。

---

## 1. モデルカタログ

### Claude（Agent ツール経由でサブエージェント起動可能）

```
Level 4 (レビュアー):   Opus 4.8  — アドバイザー、数学のレビュー  [ユーザー限定: /model, /advisor]
Level 3 (ストラテジスト):Opus 4.6  — アーキテクチャ、コンセプト      [サブエージェント: model:"opus"]
Level 3 (クリエイティブ):Fable 5   — クリエイティブテキスト、物語   [サブエージェント: model:"fable"]
Level 2 (ワークホース): Sonnet 4.6— 実装、デバッグ               [サブエージェント: model:"sonnet"]
Level 1 (高速):        Haiku 4.5 — ボイラープレート、フォーマット   [サブエージェント: model:"haiku"]
```

### 外部エージェント（コンパニオンスクリプト / SSH）

```
Level 2-3: Gemini 3.5 pro  — 調査、科学データベース            [agy-companion CLI]
Level 2:   Gemini 3.5 flash— 高速調査                          [agy-companion CLI]
Level 2-3: Codex 5.5 (GPT) — コードレビュー、コード生成        [codex-companion CLI]
Level 2:   Codex 4.5 (GPT) — よりシンプルなコードタスク       [codex-companion CLI]
```

### ローカルモデル（トークンフリー、24 時間 365 日）

```
Level 1-2: Ollama (Qwen 3.5:35b-a3b) — Haiku〜Sonnet レベル [<ollama-host>:11434]
           呼び出し: SSH + curl http://<ollama-host>:11434/v1/chat/completions
           または: エージェントシステム制御 API 経由の委任（利用可能な場合）
```

### 到達可能性マトリクス

| モデル | LLM から起動可能 | 呼び出しパス | 制約事項 |
|--------|------------------|--------------|----------|
| Sonnet 4.6 | 可能 | `Agent(model:"sonnet")` | — |
| Opus 4.6 | 可能 | `Agent(model:"opus")` | — |
| Haiku 4.5 | 可能 | `Agent(model:"haiku")` | — |
| Fable 5 | 可能 | `Agent(model:"fable")` | — |
| Opus 4.8 | アドバイザーのみ | セッション内の `advisor()` | ユーザーが `/advisor` を設定する必要あり |
| Gemini 3.5 | 可能 (Bash) | `companion-for-agy "prompt"` | Windows 限定、stdout ワークアラウンド |
| Codex 5.5/4.5 | 可能 (Bash) | `node codex-companion.mjs task "prompt"` | 認証が必要 |
| Ollama | 可能 (SSH/curl) | SSH + curl で Ollama ホスト API へ | VPN/Tailscale がアクティブであること |
| メインモデルとしての Opus 4.8 | 不可 | ユーザー操作: `/model opus 4.8` | ユーザー操作のみ |
| メインモデルとしての Fable 5 | 不可 | ユーザー操作: `/model fable` | ユーザー操作のみ |

---

## 2. スコア計算 (Score Computation)

```
次元 (0-10):
  CLARITY     : タスクがあいまいさなく明確か？
  COMPLEXITY  : 内部コンポーネント数はいくつか？
  CREATIVITY  : 新しいソリューションが必要か？
  CONTEXT     : 事前知識がどれだけ必要か？
  CRITICALITY : 完全性の重要度はどれくらいか？

SCORE = (10 - CLARITY) + COMPLEXITY + CREATIVITY + CONTEXT + CRITICALITY
```

### スコアのしきい値

| スコア | モデル | 適用例 |
|--------|--------|--------|
| 0-8 | Ollama (ローカルホスト) | プロンプト生成、要約、シンプルなテキスト |
| 9-12 | Haiku | __init__.py、フォーマット、ボイラープレート |
| 13-22 | Sonnet | 機能実装、バグ修正、標準的なコード |
| 13-22 | Gemini 3.5 | 調査、文献検索、科学データベース |
| 13-22 | Codex 5.5 | コード生成 (Luau, Node.js)、計算スクリプト |
| 23-28 | Sonnet + アドバイザーレビュー | 品質チェック付きの複雑なコード |
| 23-35 | Fable 5 | クリエイティブテキスト、マーケティング、ストーリーテリング |
| 29-40 | Opus 4.6 | アーキテクチャ、戦略、論文執筆 |
| 35-50 | Opus 4.6 + アドバイザー | 数学的証明、アーキテクチャ決定、統計学 |
| 40-50 | Opus 4.8 (ユーザー推奨) | 数学的証明作業、最高度の厳密性 |

---

## 3. クロスエージェント委任 (Cross-Agent Delegation)

### どの外部エージェントを何に使うか？

| タスク | 最適なエージェント | 理由 |
|--------|-------------------|------|
| 科学文献検索 | Gemini 3.5 pro | ネイティブな OpenAlex/arXiv/PubMed skill |
| コードレビュー（セカンドオピニオン） | Codex 5.5 | 独立した視点 |
| シンプルなテキスト生成 | Ollama (ローカルホスト) | トークンフリー、24/7 |
| クリエイティブテキスト、マーケティング | Fable 5 | 最も強力なクリエイティブ出力 |
| 数学的証明 | Opus 4.8 (アドバイザー) | 最高度の分析深度 |

### 除外事項（ドキュメント化された弱点）

- **Gemini:** 数学的レビュー/証明作業には**使用不可**（証明レビューでの方向エラーが記録済み、2026-06-07）
- **Codex 4.5:** 5.5 が利用不可の場合のみ使用。それ以外は常に 5.5

### 呼び出しパス

> プレースホルダー `<host>`、`<ollama-host>`、`<tailscale-ip>`、`<user>`、および `~/.ssh/<key>` をご自身のインフラストラクチャに合わせて置き換えてください。

**Gemini (companion-for-agy 経由):**
```
companion-for-agy --researcher --json --timeout 120000 "research prompt"
```

**Codex (codex-companion 経由):**
```
node "~/.claude/plugins/cache/openai-codex/codex/1.0.4/scripts/codex-companion.mjs" task --effort high "code prompt"
```

**リモートホスト上の Ollama (SSH 経由):**
```
ssh -i ~/.ssh/<key> <user>@<tailscale-ip> "curl -s http://localhost:11434/v1/chat/completions -d '{\"model\":\"qwen3.5:35b-a3b\",\"messages\":[{\"role\":\"user\",\"content\":\"Prompt\"}]}'"
```

**ツールを備えたエージェントシステムへの委任（例）:**
```
curl -s -X POST http://<host>:8081/api/chat -H "Content-Type: application/json" -d '{"prompt": "...", "chat_id": "claude-delegate"}'
```

---

## 4. アドバイザーペアリング (Advisor Pairing)

### メカニズム

`advisor()` は **セッションレベルのツール** です — アドバイザーモデルはユーザーが `/advisor` で設定し、プログラムから自動設定することはできません。これにより以下のペアリングパターンが生まれます：

| パターン | 仕組み | 使用するタイミング |
|----------|--------|--------------------|
| **セッションアドバイザー** | ユーザーが `/advisor opus 4.8` を設定し、エージェントが `advisor()` を呼び出す | 証明/アーキテクチャの標準 |
| **オーケストレーター兼レビュアー** | Opus メインモデルが Sonnet サブエージェントの出力をレビュー | オーケストレーターが作業者より強力な場合 |
| **反論エージェント** | エージェント A が作業し、エージェント B が敵対的にチェック | 独立した検証、二重の視点 |
| **ユーザー推奨** | エージェントが推奨：「このタスクは opus 4.8 + advisor で実行してください」 | 当前のセッションが弱すぎる場合 |

### いつアドバイザーを推奨すべきか？

- 数学的証明作業（スコア ≥ 35）
- 長期的な影響を伴うアーキテクチャ上の決定
- 統計的手法 / 研究デザイン
- 2 回以上のデバッグサイクルで失敗した複雑なバグ

### いつアドバイザーを使うべきではないか？

- ルーチンコード、コンテンツ整理、フォーマット（スコア < 23）
- シンプルな機能実装
- 明確に定義された非クリティカルなタスク

---

## 5. エスカレーションのトリガー (Escalation Triggers)

### Ollama -> Haiku
- ファイルアクセスが必要
- コード解析が必要

### Haiku -> Sonnet
- 2 つ以上のファイルに影響する
- 複数の選択肢からの決定が必要
- 予期しないエラーが発生した
- 削除操作が要求された

### Sonnet -> Opus
- アーキテクチャ上の決定が必要
- 3 つ以上のシステムを統合する必要がある
- 要件が矛盾している/不透明である
- 戦略的計画が必要

### Sonnet -> Gemini (横方向)
- 科学的調査が必要
- 参考文献の検証

### Sonnet -> Codex (横方向)
- セカンドオピニオンとしてのコードレビュー
- アドバイザーがオーバーロード状態（フォールバックレビュアー）

### Opus -> Opus + アドバイザー
- 証明レビューが必要
- クリティカルなアーキテクチャ決定
- 統計的手法

### ディエスカレーション (De-escalation)
- コンセプトが決定 -> Sonnet が実装を引き継ぐ
- タスクが定型的/反復的 -> Haiku が引き継ぐ
- ツールアクセス不要のテキストのみ -> Ollama が引き継ぐ

---

## 6. 権限マトリクス (Permission Matrix)

| 操作 | Ollama | Haiku | Sonnet | Opus | Gemini | Codex |
|------|--------|-------|--------|------|--------|-------|
| ファイル読み込み | - | 可能 | 可能 | 可能 | 可能* | 可能* |
| ファイル書き込み | - | 可能 | 可能 | 可能 | 可能* | 可能* |
| ファイル削除 | - | - | 可能**| 可能 | - | - |
| システムコマンド | - | - | 可能**| 可能 | 可能* | 可能* |
| アーキテクチャ決定 | - | - | - | 可能 | - | - |
| Web 調査 | - | - | 可能 | 可能 | 可能 | - |
| advisor() 呼び出し | - | - | 可能 | 可能 | - | - |

*独自のサンドボックスモードのコンパニオンスクリプト経由
**ユーザーの確認が必要

---

## 7. コスト効率 (Cost Efficiency)

### ルーティングによるトークン削減

| タスクタイプ | ルーティングなし | ルーティングあり | 削減率 |
|--------------|------------------|------------------|--------|
| 定型作業 | Opus トークン | Ollama (無料) | 100% |
| ボイラープレート | Opus トークン | Haiku トークン | ~80% |
| 標準コード | Opus トークン | Sonnet トークン | ~50% |
| 調査 | Claude トークン | Gemini トークン | ~70% (別予算) |
| コードレビュー | advisor() トークン | Codex トークン | ~60% (別予算) |

---

## 8. 黄金律

> "Opus が思考し、Sonnet が構築し、Haiku が実行し、Ollama が節約する。Gemini が調査し、Codex がレビューし、Fable が語る。"

---

## 変更履歴

### 2.0.0 (2026-06-12)
- クロスエージェント委任: Gemini、Codex、Ollama (ローカルホスト) をルーティング先として追加
- アドバイザーペアリング: 4 つのパターン（セッションアドバイザー、オーケストレーター兼レビュアー、反論エージェント、ユーザー推奨）
- 到達可能性マトリクス: LLM 起動可能 vs ユーザー限定を明確に記述
- Ollama (Qwen 3.5:35b-a3b, Haiku〜Sonnet レベル) を Level 1-2 として追加
- 横方向のエスカレーション: Sonnet -> Gemini (調査)、Sonnet -> Codex (レビュー)
- 除外事項の明記（Gemini は数学不可）
- スコアのしきい値をすべてのモデルに拡張

### 1.0.0 (2026-03-15)
- BACH v3.8.0 から移植 (ing-strategie v2.0.0)

---

*BACH v3.8.0 から移植 | クロスエージェント + アドバイザー v2.0.0 で拡張*