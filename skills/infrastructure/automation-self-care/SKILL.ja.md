---
name: automation-self-care
version: 1.0.1
type: skill
author: Lukas Geiger + OpenAI
created: 2026-07-28
updated: 2026-07-30
description: >
  スケジューリングされた LLM タスクやデスクトップアプリ自動化向けに、プロバイダー中立なセルフケア・コアセットを構築・運用します。エージェントがネイティブスケジューラーを検出して定期的なクリーンアップ、プロンプト品質、頻度、負荷、リソース、クロスシステム、権限、実行時チェックを導入したい場合や、ロールバック・リードバック・削除保護を備えた既存自動化フリートの継続的改善を行いたい場合に指定します。automation
  self-care, scheduler task care, desktop app automation maintenance,
  automation fleet audit, self-healing schedules, ANTIGRAVITY
  スタイルのメンテナンス・タスクファミリー再構築リクエスト,
  core-set-textautomations, basic-text-automations, textbased-automation-core,
  textbased-automation-drivers, textbased-desktopapp-automations
  などのトリガーに対応します。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, scheduler, desktop-apps, self-care, maintenance, rollback, cross-system]
language: ja
status: active
aliases: [core-set-textautomations, basic-text-automations, textbased-automation-core, textbased-automation-drivers, textbased-desktopapp-automations]
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

> **日本語** — `automation-self-care` の公式日本語版。

# Automation Self-Care

単一のプロバイダー中立な制御ループから、ネイティブでプロバイダー固有のメンテナンスフリートを作成します。エビデンス、可逆的な変更、ネイティブリードバックを要求しつつ、ANTIGRAVITY タスクファミリーの本来の意図を保持します。

## 譲れない境界条件

- 検出、計画、承認、変更、リードバックを相互に独立したフェーズとして扱います。
- ターゲットアプリがサポートする自動化 API、コマンド、または UI を使用してください。ストレージファイルを編集するだけでライブアプリの状態が変更されると仮定してはなりません。
- タスクを提案する前に、ローカルルール、ロック、削除/抑制ログ、既存のスケジュールを読み込んでください。
- スケジューラーのサポートを創作してはなりません。作成/更新/リードバックが証明できない場合は、手動インストール計画を作成し、変更を行う前に停止してください。
- 1 回のケア実行につき、独立してテスト可能なチューニング変更は最大 1 つまでとします。
- ケアタスクが自身を無効化したり、設定されたリカバリーフロアを下回る頻度に低下させたりしないよう保護してください。
- すべての変更をロールバックできるように、以前のプロンプト、スケジュール、モデル、権限、および有効化状態を保持してください。
- 単にスケジューラーが起動したことや exit 0 だけで成功とみなさず、成果のエビデンスが得られて初めて成功とカウントしてください。
- シークレット、プライベートプロンプト、または個人データを共有レジストリにコピーしないでください。

## ワークフロー

### 1. ネイティブ自動化サーフェスの検出

現在の Actor、プロバイダー、アプリクラス、スケジューラーサーフェス、サポートされている操作、状態ファイル、実行履歴、使用状況テレメトリ、およびリードバック方法をインベントリ化します。[provider-adapter-contract.md](references/provider-adapter-contract.md) 内のプロファイル契約を使用して機能を記録してください。

ネイティブなデスクトップアプリのスケジュール、CLI/ヘッドレス実行、OS スケジューラーまたはサービススターター、一般的なスケジューラーサービス、ワークフローエンジン、および未サポートまたは UI 専用の自動化を明確に区別してください。設定ファイルの存在をサポートされた変更パスと同等とみなしてはなりません。

### 2. フリートのインベントリ化

各タスクについて、安定したローカル識別子、目的、プロンプトのフィンガープリント、スケジュール、有効化状態、モデル、権限、ターゲットパス、最後のスケジューラーイベント、最後の成功成果、および現在の所有者を記録します。プロンプトの内容はローカルに保持してください。

アプリがメモリから状態を書き換える可能性がある場合は、変更前に信頼できるライブサーフェスを 2 回確認してください。

### 3. コアセットの設計

[core-set.md](references/core-set.md) をお読みください。以下のいずれかを選択します：

- `compact`: 頻度と負荷分散を組み合わせた 5 つのケアタスク。または
- `full`: 元のメンテナンスファミリーに対応する 9 つの焦点を絞ったタスク。

プロバイダー中立な計画を生成します：

```bash
python scripts/build_core_set.py provider-profile.json \
  --topology compact --out automation-care-plan.json
```

ジェネレーターがタスクを自動的にインストールすることはありません。`blocked` となっているすべての機能をレビューし、計画を適用する前に衝突のないローカル時間を選択してください。

### 4. インストールの段階的実施

ネイティブなプロバイダーアダプターを介してインストールします：

1. まずは読み取り専用モードでのクリーンアップから始めます。
2. リソース保護を追加します。
3. ロールバック機能を備えたプロンプト品質のチューニングを追加します。
4. 十分な実行エビデンスが存在するようになってから、頻度と負荷のチューニングを追加します。
5. 最後にクロスシステム調整を追加します。

ユーザーがアクティブなインストールを明示的に承認しない限り、新規作成またはインポートされたタスクは無効状態のまま作成してください。無人パイロットの場合は、最初に削除ログ、事前状態のスナップショット、実行レシート、およびロールバックパスを要求してください。

### 5. ケアループの実行

各ケアタスクは以下の手順に従います：

```text
follow-up previous change
  -> collect current evidence
  -> classify one cause
  -> choose zero or one change
  -> mutate through native surface
  -> read back
  -> write receipt and next-check condition
```

[core-set.md](references/core-set.md) にある仮説カタログとエビデンスルールを使用してください。原因が不明な場合は、観察、権限の縮小、または安全な一時停止を意味します。勘で修理を行ってはなりません。

### 6. Actor 間での調整

ローカルアプリの状態を信頼できる唯一の情報源（Authoritative）として維持します。タスク契約、カバー率、ステータス、レシート、およびサニタイズされたフィンガープリントのみを共有してください。冗長な読み取り専用レビューは許可されます。単一ライターによる変更には、クレームまたは同等のネイティブロックが必要です。

### 7. ネイティブイベントフックのないシステム（Letter-Hooker 拡張）

トークンやサブスクリプションの制限は容量状態として扱い、壊れた Actor として扱わないでください。元の Actor が成功レシートを生成した後に、委任されたカバー率を返却します。

## 必須のアウトプット

設定またはケア実行ごとに以下を報告してください：

- 検出されたネイティブサーフェスと未サポートの機能。
- 選択されたトポロジーと、作成、提案、またはスキップされたタスク。
- 正確な変更内容と変更前後のリードバック。
- 成果のエビデンスまたは開いている観察ウィンドウ。
- ロールバックの場所と復帰条件。
- 調整レジストリが存在する場合の共有カバー率更新。

## 例

ユーザー：「このデスクトップアプリで自己メンテナンススケジュールを設定してください。」

アプリがスケジュールされたタスクのリスト表示、作成、更新、検証を行えるかを検出します。Compact 計画を生成し、未サポートの情報を提示した上で、承認されたタスクのみをネイティブサーフェス経由でインストールします。ライブスケジューラーへの登録がないタスクプロンプトが含まれるフォルダーは、設定完了とはみなされません。

## 変更履歴

### 1.0.1 (2026-07-30)

- プロバイダー中立なテキスト自動化およびデスクトップアプリ自動化のエイリアスを追加しました。

### 1.0.0 (2026-07-28)

- 元の ANTIGRAVITY メンテナンスファミリー、F1-F6 制御ループ、およびその後のプロバイダー固有の適応策を中立なコアセット Skill に統合しました。