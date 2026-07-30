---
name: letter-hooker
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: >
  ネイティブなイベント駆動型 JSON ライフサイクルフック（~/.claude/settings.json や ~/.codex/hooks.json など）を持たない
  AI エージェントや CLI（Antigravity / Gemini CLI など）向けに、Letter Hooks、プリフライトブートローダー、ドキュメントトラバーサルルール、自己修復型プロンプトコンテキスト拡張機能によって automation-self-care を拡張します。エージェントがプリフライトルールを注入する際、作業開始前に memory/gardener を検索する際、ディレクトリドキュメント読み込み戦略（CLAUDE.md / AGENTS.md）を適用する際、またはサイドカータスクをスキルやセキュリティプロトコルへ動的にルーティングする際に使用します。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, letter-hooker, letter-hooks, bootloader, prompt-enrichment, self-care, governance]
language: ja
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: [agy_kontext_and_workflow_loader.py]
provenance:
  origin: "fork of automation-self-care"
  origin_path: "skills/infrastructure/automation-self-care"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/skills"
---

> **日本語** — `letter-hooker` の公式日本語版。

# Letter-Hooker（プロンプトレベルのプリフライト & ガバナンスエンジン）

**Letter-Hooker** スキルは、ネイティブなイベント駆動型 JSON ライフサイクルフックローダー（例: `~/.claude/settings.json` や `~/.codex/hooks.json`）を持たない AI エージェントフレームワーク（**Antigravity / Gemini CLI** など）向けに `automation-self-care` を拡張します。

受動的なキー入力ごとのフックに依存するのではなく、`letter-hooker` はスケジュールされたタスクとメンテナースクリプト（`agy_kontext_and_workflow_loader.py`）を介して、**アクティブなプロンプトレベルのプリフライトブートローダーおよび Letter-Hook 注入ループ**を運用します。

---

## 主な機能

1. **プリフライトブートローダー & ドキュメントトラバーサルルール**:
   - **上方向 & 下方向の検索**: 現在の作業ディレクトリレベルで `AGENTS.md`、`CLAUDE.md`、`START.md`、`RULES.md`、および `README.md` を検査するようエージェントに厳格な指示を強制します。見つからない場合は見つかるまで上方向にトラバースし、その後下方向を検査します。
   - **Memory & Gardener プリフライト**: 破壊的または複雑な変更を実行する前に、`gardener` および `memoryhooker` への必須プリフライトクエリを行います。

2. **Letter Hooks カタログ & 参照リンク**:
   - `OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/` 配下に格納されたモジュール化された `.md` 指示ファイル。
   - 呼び出し時にエージェントが正確なセキュリティおよびワークフロープロトコルを読み取るよう、`sidecar.json` プロンプトテキスト内に明示的な `file://` リンクを直接注入します。

3. **日次キーワードリスト & 自己修復型プロンプト拡張**:
   - アクティブ/待機タスクから日次 `STICHWORTLISTE.json` を維持管理します。
   - 実行ログ（`AUTOMATIONS-MEMORY.md`）を分析して失敗パターン（コンテキストの欠落、ワークフローガイダンスの欠落、無効なパス）を検出し、タスクプロンプトを動的にパッチ修正します。

4. **スキル & ペルソナルーティング**:
   - タスクのキーワードを検査し、適切な `.SKILLS`（例: `infrastructure/condition`、`semantic-persona-routing`、`orchestrator`、`think`、`decide`）にマッピングします。

---

## 主要な Letter Hooks

- **`HOOK-DOC-TRAVERSAL-01`**: [bootloader_doc_traversal.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/bootloader_doc_traversal.md)
- **`HOOK-GARDENER-MEMORY-01`**: [preflight_gardener_query.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/preflight_gardener_query.md)
- **`HOOK-WORKFLOW-HYGIENE-01`**: [workflow_lock_and_git_hygiene.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/workflow_lock_and_git_hygiene.md)
- **`HOOK-PATH-VALIDATION-01`**: [path_validation_and_authority.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/path_validation_and_authority.md)

---

## ワークフローの統合

```bash
# Execute the Letter-Hooker Maintenance Engine
python OneDrive/.SYNC/scripts/agy_kontext_and_workflow_loader.py
```

1. **サイドカーの走査**: `~/.gemini/config/sidecars/` 内のすべての `sidecar.json` プロンプトテキストを読み込みます。
2. **キーワードリストの更新**: ドメイン用語を抽出し、`.SYNC/STICHWORTLISTE.json` に保存します。
3. **Letter Hooks の注入**: ブートローダールールおよび `file://` 参照リンクをプロンプトに追加します。
4. **結果の記録**: 更新内容を `ANTIGRAVITY-LOG.txt` および `ANTIGRAVITY-REGISTRY.md` に記録します。