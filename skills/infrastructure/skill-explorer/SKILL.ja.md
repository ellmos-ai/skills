---
name: skill-explorer
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: 自らのスキル景観を管理：既存スキルの調査と比較（監査モード）、新しいスキル/プラグインのWeb調査（探索モード）を行い、同時にモノリスを読み込む代わりに軽量なサブスキル（Skill-Finder、ファミリーアンブレラ、メンテナンススキル）を生成するインストーラーでもあります。「スキルの比較/監査」、「どのスキルが重複しているか」、「スキルファミリーの形成」、「スキルのクリーンアップ/集約」、「スキルレジストリの維持」、「トピックXのスキル/プラグインの検索」、「新しいスキルのインストール」、「スキルマーケットプレイスの閲覧」、または `/skill-explorer` に使用します。ファミリーごとのサブレポートと全域で番号付けされた決定リストを提供し、セキュリティチェックと明示的な承認の後にのみインストール/アンインストールを行います。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [skills, audit, cluster, recherche, install, security, installer, meta, workflow, branch, fork]
language: ja
status: active
dependencies: {'tools': ['git'], 'services': ['websearch'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/skill-explorer/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **日本語** — `skill-explorer` の公式日本語版。


# Skill-Explorer — スキル景観の管理（監査・探索・インストーラー） (日本語)

## 概要と目的

スキルインベントリが大きくなるにつれて、重複や未利用のリソース、「どのスキルの代わりにどのスキルを使うか」という曖昧な状況が生じます。また、新しいスキル/プラグインも常に登場しています。`skill-explorer` は3つの役割を1つのツールに統合します：

| 役割 | 実行内容 | 詳細 |
| --- | --- | --- |
| **監査モード**（内部向け） | すべてのスキルを調査し、ファミリーにクラスタリングし、機能/依存関係/リソースを収集して、ファミリーごとのサブレポートと番号付きの推奨事項を作成 | `references/audit-mode.md` |
| **探索モード**（外部向け） | トピックに関する新しいスキル/プラグインをWeb（Web/GitHub/Reddit、バイリンガル）で調査し、比較し、ゲート付きでインストール | `references/explore-mode.md` |
| **インストーラー** | モノリスの代わりに軽量なサブスキルを*生成* — Skill-Finder、ファミリーアンブレラ、メンテナンススキル | 以下 + `references/family-care.md` |

呼び出し：`/skill-explorer`（デフォルトは監査）または「… トピックXについて検索」（探索）。両モードは分類法（`references/clustering.md`）、レポート形式（`references/report-format.md`）、および番号体系を共有しているため、ユーザーは単一の番号付きリストで返答できます。

## インストーラーの原則と永続化

`skill-explorer` 自体がモノリスとして肥大化するのではなく、オンデマンドで軽量かつ個別に読み込み可能なサブスキルを*生成*します。これにより、長すぎる単一スキルを読み込む必要がなくなります：

- **Skill-Finder** ([F]) — すべてのタスクの前にレジストリを読み取り、対応するファミリーにルーティングする、「using-superpowers」のドアマンに類似したアクティブなファインダー/ルーター（`references/skill-finder.md`、テンプレート `assets/skill-finder-template.md`）。
- **ファミリーアンブレラ** (c1) — ファミリー全体を把握しているメタスキル（`assets/family-umbrella-template.md`）。
- **メンテナンススキル**（[P1] ファミリー、[P2] レジストリ） — ファミリー/レジストリを最新に保つ（`references/family-care.md`）。

決定は `~/.claude/skills/skill-explorer/config.json` に永続化されます（`references/config.md`、テンプレート `assets/config.example.json`）。起動時に読み込まれ（既知のファミリー/ルーター/生成されたサブスキル）、実行後に更新されるため、再実行時に重複して作成されることはありません。

## ブランチメカニズム（サードパーティスキルのカスタマイズ）

読み取り専用のスキル（プラグイン、インポートされたサードパーティ）は、オリジナルを変更せずにカスタマイズできます。元のディレクトリが完全にコピーされ（**ブランチ**）、そのコピーのみが編集されます。ブランチには、元のスキルへの参照、ブランチ作成日、作成者、理由の4つの必須フィールドが含まれます。ブランチがオリジナルに取って代わると、オリジナルはランタイムから登録解除されるか（`SKILL.md` → `CONTENT.md`）、ファミリールーターがブランチを指すように変更され、ほぼ同一の2つのスキルが衝突するのを防ぎます。サードパーティのブランチは**プライベート**のまま保持され、公開の `.AI/.SKILLS` ライブラリには入りません。詳細：`references/skill-branching.md`。

## ワークフローと手順

1. **モードの選択：** インベントリの調査/クリーンアップ → 監査モード。外部からの検索/インストール → 探索モード。（探索は以前の監査/`config.json` に基づいて構築可能。）
2. **監査モード**（`references/audit-mode.md`）：インベントリ（スクリプト）→ ファミリークラスタ → サブレポート → **1つの全域で番号付けされた決定リスト**（a/b/c1/c2/c3、および R/F/P1/P2）。
3. **探索モード**（`references/explore-mode.md`）：バイリンガル・多角的な検索 → 候補ごとに3つのカテゴリ → 影響シミュレーション → 番号付きインストール/削除推奨事項。
4. ユーザーの数字による確認の後にのみ**実行**し、スキルの作成/変更を登録して `config.json` を更新します。

## 鉄の掟

- **調査 ≠ 変更：** すべてをクラスタリングしますが、編集するのは**ユーザー所有**のスキルのみです。プラグイン/サードパーティのスキルは読み取り専用です（ヘッダーの変更や削除は不可）。サードパーティスキルをカスタマイズするには、代わりに**ブランチ**（フォークコピー）を作成します。オリジナルは手つかずのまま、すべての変更はコピーに対してのみ行われます（→ `references/skill-branching.md`）。
- **レジストリを拡張し、重複させない：** スキルレジストリ（インデックス + ファミリーマップ + インデックススキル）が存在する場合は、4つ目を作成するのではなく拡張します。
- **セキュリティは主に手動：** すべてのインストールの前に、モデル自身がスキルを読み込んで判断します。`scripts/scan_skill_security.py` は既知の限界を持つサポート用のトリアージにすぎません。絶対に自動インストールしないでください。
- **元データによる登録：** ユーザー作成 → ライブラリ、サードパーティ → 外部パス（ライブラリ**ではない**）。

## オーケストレーション（モデル中立）

ファミリーのサブレポートやソース/言語は独立した作業パスです。プラットフォームがオーケストレーター自体よりも低コストなサブエージェントを提供している場合は、ファミリー/ソースごとに1つのサブエージェントを割り当て、オーケストレーターとしては統合/検証のみを行います（専門家スウォーム）。そうでない場合は、ご自身で逐次実行します。

## リソース

- **モード：** `references/audit-mode.md`, `references/explore-mode.md`
- **共有：** `references/clustering.md`, `references/report-format.md`, `references/config.md`
- **監査：** `references/family-care.md`, `references/skill-finder.md`
- **探索：** `references/research-method.md`, `references/integration-sim.md`, `references/install-uninstall.md`
- **ブランチ：** `references/skill-branching.md`
- **スクリプト：** `scripts/inventory_skills.py`（インベントリ）, `scripts/inject_family_header.py`（ヘッダールーター）, `scripts/scan_skill_security.py`（セキュリティトリアージ）
- **テンプレート：** `assets/family-umbrella-template.md`, `assets/skill-finder-template.md`, `assets/skill-register-template.md`, `assets/config.example.json`, `assets/branch-header.example.md`

## 変更履歴

### 1.1.0 (2026-06-17)
- ブランチメカニズムの追加：サードパーティ/読み取り専用スキルをフォークコピー（ブランチ）経由でカスタマイズ可能に — 元スキルへの参照、日付、作成者、理由を付与し、オリジナルは手つかずのまま保持。鉄の掟「調査 ≠ 変更」にブランチという救済措置を拡張。新セクション `## ブランチメカニズム`。新ファイル：`references/skill-branching.md`、`assets/branch-header.example.md`。

### 1.0.0 (2026-06-17)
- 初版。インベントリ監査（ファミリークラスタリング、番号付き決定）とWeb調査（セキュリティトリアージ付きゲートインストール）を、軽量サブスキルを生成する1つのインストーラーに統合。