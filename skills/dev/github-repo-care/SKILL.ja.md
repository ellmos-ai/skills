---
name: github-repo-care
version: 1.0.0
type: protocol
author: Lukas Geiger + Codex
created: 2026-06-18
updated: 2026-06-18
aliases: [github-pflege, repo-veroeffentlichen, repo-release, privacy-gate, release-gate]
description: GitHub リポジトリを安全に作成、公開、リリース、監査、および保守するためのプロトコル：ローカルルールとロックの確認、最初の git add の前の .gitignore 作成、プライバシーチェックの実行、README/i18n/バナー/メタデータの準備、リリースタグと GitHub リリースの検証、組織プロファイル・llms.txt ファイル・レジストリリンクの更新。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [github, repo, release, privacy, i18n, marketing, ci, documentation]
language: ja
status: active
dependencies: {'tools': ['git', 'gh', 'rg'], 'services': ['GitHub'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.codex/skills/github-repo-care/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': '2026-06-18', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **日本語** — `github-repo-care` の公式日本語版。


# GitHub Repo Care — リポジトリをクリーンに公開・保守する (日本語)

## 使用タイミング

GitHub リポジトリを作成、公開、リリース、監査、または保守する必要がある場合にこの Skill を使用します。最初のパブリックプッシュの前、リリースタグ、リポジトリのメタデータ、組織プロファイル、およびプライバシーチェックにおいて特に重要です。

GitHub への公開ステップを伴わない純粋な実装作業には使用しないでください。関連する開発またはデバッグワークフローを先に完了してから、公開のためにこの Skill を有効化してください。

## コアルール

最初のパブリックプッシュの前にリポジトリを準備します。正しい `.gitignore`、プライバシーゲート、ライセンス、README、メタデータ、およびリリースストーリーは、パブリックな履歴が存在する前に準備する方がはるかに低コストです。

## ワークフローと手順

1. **ローカルルールを読む。** `AGENTS.md`、`CLAUDE.md`、`START.md`、リリース指針、命名指針、およびロック指針が存在する場合は確認します。
2. **ロックを確認する。** `LOCK.txt` または一致する `LOCK.*.txt` がアクティブな場合は、そのスコープを編集しないでください。
3. **リポジトリのアイデンティティを決定する。** 名前、組織、可視性、ライセンス、および 1 文での目的を確認します。
4. **`git add` の前に `.gitignore` を作成する。** シークレット、ローカルデータ、データベース、ビルド出力、仮想環境、キャッシュ、IDE ファイル、およびプライベートメモを除外します。
5. **パブリックな基本ファイルを加える。** 典型的なファイル：`README.md`、`LICENSE`、`CHANGELOG.md`、`SECURITY.md`、`CONTRIBUTING.md`、`CODE_OF_CONDUCT.md`、`llms.txt`、および CI。
6. **発見しやすさを意識して README を書く。** ファーストビュー：目的、インストール、使い方、プライバシーモデル、プロジェクト構造、ライセンス、および標準リポジトリ名。
7. **視覚的シグナルを追加する。** プロジェクトの理解が容易になる場合は、バナー、ロゴ、またはスクリーンショットを追加します。実際の製品画像や明確な概念図が可能な場合は、汎用的な装飾を避けてください。
8. **i18n を計画的に設計する。** 最小限：英語＋プロジェクト言語。ユーザー向けモジュールの推奨標準セット：ドイツ語、英語、スペイン語、簡体字中国語、日本語、ロシア語。
9. **テストとスモークテストを実行する。** 成功を宣言したりリリースを作成したりする前にローカルで検証します。
10. **プライバシーゲートを実行する。** ステージング/追跡対象セットをチェックし、シークレット、ローカルパス、個人可同同定情報 (PII)、`.env`、データベース、プライベートドキュメント、生成された成果物、および文字化け (mojibake) を探します。
11. **コミットしてプッシュする。** ゲートを通過した後にのみコミットします。その後、GitHub リポジトリを作成または接続し、プッシュしてリモート状態を検証します。
12. **メタデータを設定する。** 説明 (description)、トピック (topics)、ホームページ (homepage)、可視性 (visibility)、およびデフォルトブランチをチェックします。
13. **リリースを作成する。** タグと GitHub リリースを作成し、ブランチとタグの両方の CI を検証します。
14. **発見用サーフェスを更新する。** 組織プロファイル、`llms.txt`、中央レジストリ、ローカルモジュールインデックス、およびエコシステム README からリンクします。
15. **最終検証。** リモート README、リリース面、トピック、CI、およびリンクをチェックします。

## プライバシーゲート (Privacy Gate)

表示されている作業ツリーだけでなく、ステージングされた (staged) または追跡された (tracked) セットを検索します。

```bash
git diff --cached --check
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|C:/Us[e]rs/|/c/Us[e]rs/|s[k]-[A-Za-z0-9]|gh[p]_|gh[o]_|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|\\x{C3}|\\x{C2}|\\x{FFFD}" .
```

パブリックモジュールについては、`RELEASE_GATE.md` または同等のゲート記録も作成します：日付、実行したコマンド、結果、残りの警告、および意図的な例外。シークレットが一度コミットされた場合、`HEAD` から削除するだけでは不十分です。シークレットをローテーションしてください。

## GitHub メタデータ

プッシュ後、メタデータとリリースデータを明示的に設定します。

```bash
gh repo edit ORG/REPO --description "具体的で短い説明" \
  --add-topic local-first --add-topic python --add-topic llm
git tag -a v1.0.0 -m "v1.0.0"
git push origin v1.0.0
gh release create v1.0.0 --repo ORG/REPO --title "v1.0.0" --notes "..."
```

続いて検証します：

```bash
gh repo view ORG/REPO --json nameWithOwner,visibility,description,repositoryTopics,url
gh release view v1.0.0 --repo ORG/REPO --json tagName,url,isDraft,isPrerelease
gh run list --repo ORG/REPO --limit 5
```

リリース後に CI が赤（失敗）になっている場合、リポジトリはまだクリーンに公開されていません。作成したばかりの初期リリースの場合は、新しいタグを修正されたコミットに即座に意図的に移動することが許容されます。

## よくあるエラー

| エラー | 修正 |
|---|---|
| `git add` の後に `.gitignore` が追加された | まずステージングを解除し、ignore ルールを修正してから再度追加する |
| UI や Skill が多言語対応であるのに README が単一言語である | 言語リンクまたはローカライズされた README を追加する |
| バナー、トピック、説明がない | 告知前に発見用アセットを追加する |
| リリスタグは存在するが CI が赤になっている | CI を修正し、新しい実行を確認する |
| 組織の README は更新されたが `llms.txt` が漏れている | 人間向けおよびマシン向けのサーフェスの両方を更新する |
| 公開ドキュメントにローカルパスが表示されている | 相対パスまたは汎用的な例に置き換える |
| パブリックリポジトリにテスト用データベースや Notebook 受信トレイが含まれている | 追跡から削除し、ignore ルールを追加してプライバシーゲートを再実行する |

## 最終チェックリスト

- [ ] ローカルルールとロックを確認した。
- [ ] 最初の add の前に `.gitignore` が存在した。
- [ ] パブリックドキュメント、ライセンス、セキュリティ、貢献ガイド、変更履歴、`llms.txt` が存在する。
- [ ] README にリポジトリ名、目的、インストール、使い方、プライバシー、ライセンスが含まれている。
- [ ] i18n の期待を満たしている。
- [ ] 役立つ場合にバナー、ロゴ、またはスクリーンショットが存在する。
- [ ] テストとスモークテストを通過した。
- [ ] プライバシー、パス、シークレット、データベース、文字化けのスキャンがクリーンである。
- [ ] GitHub の説明、トピック、タグ、リリース、CI を検証した。
- [ ] 組織プロファイル、レジストリ、エコシステムのリンクを更新した。

## 変更履歴

### 1.0.0 (2026-06-18)
- 初回のリポジトリ保守および公開プロトコルを作成。