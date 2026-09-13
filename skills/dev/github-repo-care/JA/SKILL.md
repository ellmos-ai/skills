---
name: github-repo-care
version: 1.0.0
type: protocol
author: Lukas Geiger + Codex
created: 2026-06-18
updated: 2026-06-18
aliases: [github-pflege, repo-veroeffentlichen, repo-release, privacy-gate, release-gate]
description: GitHub リポジトリを安全に作成、公開、リリース、監査、保守するためのプロトコル。ローカルルールとロックの確認、最初の git add 前の .gitignore 作成、プライバシーチェックの実行、README/i18n/バナー/メタデータの準備、リリースタグおよび GitHub releases の検証、組織プロファイル、llms.txt ファイル、レジストリリンクの更新を行います。

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

<img src="banner.png" width="100%" alt="github-repo-care banner">

> **日本語** — `github-repo-care` の公式日本語版。


# GitHub Repo Care — リポジトリをクリーンに公開・保守する（日本語）

## 使用タイミング

GitHub リポジトリの作成、公開、リリース、監査、または保守を行う場合にこのスキルを使用します。最初のパブリックプッシュ、リリースタグ、リポジトリのメタデータ、組織プロファイル、およびプライバシーチェックの前に特に重要です。

GitHub への公開ステップを伴わない純粋な実装作業には使用しないでください。関連する開発またはデバッグのワークフローを先に完了してから、公開のためにこのスキルを有効化してください。

## 核心ルール

最初のパブリックプッシュの前にリポジトリを準備します。適切な `.gitignore`、プライバシーゲート、ライセンス、README、メタデータ、およびリリースストーリーは、パブリックな履歴が存在する前の方がはるかに低コストで対応できます。

## ワークフローと手順

1. **ローカルルールを確認する。** 存在する場合は `AGENTS.md`、`CLAUDE.md`、`START.md`、リリース方針、命名方針、およびロック方針を確認します。
2. **ロックを確認する。** `LOCK.txt` または該当する `LOCK.*.txt` が有効な場合は、そのスコープを編集しないでください。
3. **リポジトリのアイデンティティを決定する。** 名前、組織、公開設定、ライセンス、および一言での目的を確認します。
4. **`git add` の前に `.gitignore` を作成する。** シークレット、ローカルデータ、データベース、ビルド出力、仮想環境、キャッシュ、IDE ファイル、およびプライベートノートを除外します。
5. **公開用の基本ファイルを追加する。** 一般的なファイル: `README.md`、`LICENSE`、`CHANGELOG.md`、`SECURITY.md`、`CONTRIBUTING.md`、`CODE_OF_CONDUCT.md`、`llms.txt`、および CI。
6. **発見しやすさを意識して README を執筆する。** ファーストビュー: 目的、インストール方法、使用方法、プライバシーモデル、プロジェクト構成、ライセンス、および標準リポジトリ名。
7. **視覚的要素を追加する。** プロジェクトの理解が容易になる場合は、バナー、ロゴ、またはスクリーンショットを追加します。実際の製品画像や明確なコンセプト画像が利用可能な場合は、汎用的な装飾を避けてください。
8. **i18n（多言語対応）を意図的に計画する。** 最低限: 英語 + プロジェクト言語。ユーザー向けモジュールで推奨される標準セット: ドイツ語、英語、スペイン語、簡体字中国語、日本語、ロシア語。
9. **テストとスモークテストを実行する。** 完了を宣言したりリリースを作成したりする前に、ローカルで検証します。
10. **プライバシーゲートを実行する。** ステージング/追跡対象（staged/tracked）のファイルセットをチェックし、シークレット、ローカルパス、個人情報（PII）、`.env`、データベース、プライベートドキュメント、生成された成果物、および文字化け（mojibake）がないか確認します。
11. **コミットしてプッシュする。** ゲートを通過した後にのみコミットします。その後、GitHub リポジトリを作成または接続し、プッシュしてリモート状態を検証します。
12. **メタデータを設定する。** description、topics、homepage、visibility、およびデフォルトブランチを確認します。
13. **リリースを作成する。** タグと GitHub release を作成し、ブランチとタグの両方で CI を検証します。
14. **発見面（Discovery Surface）を更新する。** 組織プロファイル、`llms.txt`、中央レジストリ、ローカルモジュールインデックス、およびエコシステムの README からリンクを設定します。
15. **最終検証。** リモートの README、リリースページ、Topics、CI、およびリンクを確認します。

## プライバシーゲート (Privacy Gate)

可視の作業ツリーだけでなく、ステージングまたは追跡対象のセットを検索します。

```bash
git diff --cached --check
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|C:/Us[e]rs/|/c/Us[e]rs/|s[k]-[A-Za-z0-9]|gh[p]_|gh[o]_|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|\\x{C3}|\\x{C2}|\\x{FFFD}" .
```

パブリックモジュールの場合は、`RELEASE_GATE.md` または同等のゲートドキュメントも記録します: 日付、確認したコマンド、結果、残りの警告、および意図的な例外。過去にシークレットをコミットしてしまった場合、`HEAD` から削除するだけでは不十分です。シークレットをローテーション（更新）してください。

## GitHub メタデータ

プッシュ後、メタデータとリリースデータを明示的に設定します。

```bash
gh repo edit ORG/REPO --description "Short concrete description" \
  --add-topic local-first --add-topic python --add-topic llm
git tag -a v1.0.0 -m "v1.0.0"
git push origin v1.0.0
gh release create v1.0.0 --repo ORG/REPO --title "v1.0.0" --notes "..."
```

その後、検証します:

```bash
gh repo view ORG/REPO --json nameWithOwner,visibility,description,repositoryTopics,url
gh release view v1.0.0 --repo ORG/REPO --json tagName,url,isDraft,isPrerelease
gh run list --repo ORG/REPO --limit 5
```

リリース後に CI が失敗（赤色）している場合、リポジトリはまだクリーンに公開されていません。作成したばかりの初期リリースについては、新しく作成したタグを修正後のコミットに即座かつ意図的に移動することが許容されます。

## よくある間違い

| 間違い | 修正方法 |
|---|---|
| `git add` の後に `.gitignore` を追加した | 最初にステージングを解除（unstage）し、除外ルールを修正してから再度 add する |
| UI やスキルが多言語対応しているのに README が単一言語である | 言語リンクまたはローカライズされた README を追加する |
| バナー、Topics、または Description がない | 告知前に発見用アセットを追加する |
| リリースタグが存在するが、CI が失敗している | CI を修正し、新しい実行を確認する |
| 組織の README は更新されたが、`llms.txt` が漏れている | 人間用とマシン用の両方の表面を更新する |
| 公開ドキュメントにローカルパスが表示されている | 相対パスまたは汎用的な例に置き換える |
| パブリックリポジトリにテスト用データベースや Notebook の受信箱が含まれている | 追跡から削除し、除外ルールを追加して、再度ゲートを実行する |

## 最終チェックリスト

- [ ] ローカルルールとロックを確認した。
- [ ] 最初の add の前に `.gitignore` が存在していた。
- [ ] 公開ドキュメント、ライセンス、セキュリティ、貢献ガイドライン、変更履歴、および `llms.txt` が存在する。
- [ ] README にリポジトリ名、目的、インストール方法、使用方法、プライバシー、ライセンスが含まれている。
- [ ] i18n の期待を満たしている。
- [ ] 有用な場合にバナー、ロゴ、またはスクリーンショットが存在する。
- [ ] テストおよびスモークテストが通過している。
- [ ] プライバシー、パス、シークレット、データベース、および文字化けのスキャンがクリーンである。
- [ ] GitHub の description、topics、タグ、リリース、および CI が検証されている。
- [ ] 組織プロファイル、レジストリ、およびエコシステムへのリンクが更新されている。

## 変更履歴

### 1.0.0 (2026-06-18)
- リポジトリの保守および公開に関する初期プロトコルを作成。
