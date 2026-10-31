---
name: file-collect-sort-action
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-18
updated: 2026-08-18
description: "「フォルダから特定のファイルを常に取り出して、ある場所に集める」という形のユーザー依頼を検出し、そのためにモジュール file-collect-sort-action(CLI fcsa)をセットアップします。これは設定駆動型のエージェントで、フォルダをスキャンし、テンプレートでファイルを分類して、段階的なアクション(move/copy/duplicate-check/delete/OCR/place-information)を適用します。「<Ordner> から <Dateiart> を常に取り出して <Ziel> に集めて」「フォルダ X を ... で自動的に並べ替えて」「... に届くファイルを ... に集めて」「このフォルダをルールに基づいて片付けて」「<Dateiart> をすべて <Ordner> から自動的に移動して」といった文の際にこのスキルを使用します。必ず最初にドライランをセットアップし、ユーザーの明示的なゴーサインが出てから初めて本番稼働に切り替えます。削除は原則として _trash モードのままです。"
# Kompatibilitaet
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: utilities
tags: [dateien, sortierung, automatisierung, config-driven, ordner-ueberwachung, duplikate, ocr]
language: ja
status: active
visibility: public

# Abhaengigkeiten
dependencies:
  tools: [fcsa]
  services: []
  protocols: []
  python: []
  modules: [file-collect-sort-action]

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 844e8b0e6411e463278a6084440cd4915bf241f8ab5a036d1fa25913e18c681f
translator: "claude-sonnet-5-5"
translated_at: "2026-10-17T17:52:35.759413+00:00"
---
<img src="banner.png" width="100%" alt="file-collect-sort-action banner">

# File Collect Sort Action

> ユーザーは、具体的な依頼でこのモジュールが必要になるまで、これを意図的に受動状態で保留にしていました
> (チケット T-20260818-916568570、ユーザーの発言そのまま: *「いつか『フォルダから
> いつもこういうファイルを取り出して、そこに集めて』と言うから、そうしたら
> うちのモジュールに対応するスキルだと認識して、設定しておいて」*)。このスキルこそ、ユーザーが待っているその認識そのものです。

## このスキルが発動する場面

トリガーは、繰り返し行われる**ルールに基づく収集**を述べるユーザーの文です。
一度きりの「このファイル1つを移動して」ではありません。

- 「`<Ordner>` から `<Dateiart>` を常に取り出して `<Ziel>` に集めて」
- 「フォルダ `<X>` を `<Kriterium>` で自動的に並べ替えて」
- 「`<Quelle>` に届くファイルを `<Ziel>` に集めて」
- 「このフォルダをルールに基づいて片付けて」/「`<Dateiart>` をすべて `<Ordner>` から自動的に移動して」
- **ソース**、**識別の手がかり**(ファイルの種類/名前パターン/内容)、**ターゲット**を示し、それが今回一度だけでなく**繰り返し**行われるべきことを含意するあらゆる言い方

このスキルでは**ありません**: 単一の一度きりのファイルの移動(これはエージェントが設定層なしで直接行います)— `dokument-ingest`(「*内容*を何で読むか」に答えるもので、「*ファイル*をどこに置くか」には答えません)— ファイルを移動せずに行う増分テキストインデックス作成(`gardener`)。

## このモジュールでできること(要約)

`file-collect-sort-action`(略称 **f-csa**、CLI **`fcsa`**)は、3つの設定ファイルと処理メモリを備えた、設定駆動型のスキャン→分類→実行エージェントです。

| ファイル | 役割 |
|---|---|
| `config.json` | `scan_paths`(許可リスト)、フォーマットの包含/除外、重複検出ルール、安全ゲート(`allow_hard_delete`) |
| `categories-definitions.json` | カテゴリごとの識別テンプレート(ファイル名/拡張子/内容)、チェック/ゲート、`default_target`、`default_actions` + `default_stepping` |
| `action-rules.json` | カテゴリごとのアクションパラメータ(move/copy のターゲット、重複モード、削除モード、OCR バックエンド、配置の順序) |
| `processing-csa.json` | **スキャンした各フォルダに**書き込まれます — 既知のファイル、そのカテゴリ、適用済みのアクション、有効な設定のフィンガープリント(Fingerprint) |

既知のアクション ID: `duplicate_check`、`move`、`copy`、`delete`、`ocr_extract`、
`place_information`。ステッピングのセマンティクス: `default_stepping: true` = アクションは記載どおり左から
右へ実行され、二重に記載されたアクション ID は**二重に**実行されます。`false` = 集合
(重複は1回の実行にまとめられます)。

## セキュリティモデル — セットアップ時は必ず遵守すること

- **最初の本番運用の前に、スキャンパスごとにドライランが必須です。** `fcsa run`(`--dry-run` なし)は、まさにそのパスについて記録されたドライランがない場合、実行を拒否します。
- **設定を変更すると、確認が再び無効化されます**(3つすべての設定ファイルにわたるフィンガープリント)。設定を調整するたびに、次の本番実行には再び新しいドライランが必要になります。
- **削除はフェイルクローズドです。** `delete` は常に `trash_dir` へ移動します。ただし、`action-rules.json`（`delete.hard_delete: true`）*と* `config.json`（`allow_hard_delete: true`）の*両方*が明示的に同意した場合は除きます。**このスキルでは追加で次が適用されます：** 完全削除は、別途ユーザーの明示的な許可がない限り決して有効にしないでください。デフォルトは `_trash` のままです。
- **`scan_paths` は明示的な許可リストです。** それ以外のパスはすべて `PathNotAllowedError` を発生させます。`.PRIVAT` または `CREDENTIALS` のセグメントを含むパスは、読み込み時に拒否されます。
- **ドライランは、スキャン対象フォルダに対してバイト単位で影響を与えません。** `processing-csa.json` は本番運用時にのみ書き込まれ、ドライランでは決して書き込まれません。

## 手順：トリガーとなる文から設定済みの自動化まで

1. **依頼を構造化する。** ユーザーの文から、ソース、検出条件、ターゲットを抜き出します。不明な点があれば的確に質問してください（ファイルの種類は？ サブフォルダーも含めるか？ ターゲットで名前が衝突した場合はどうするか — skip/overwrite/rename/quarantine？）。
2. **モジュールを特定する。** まず `fcsa --help` で CLI が利用可能か確認します。ない場合は、現在のシステムで認可されているモジュールまたはパッケージの経路を調べてください。ローカルパス、パッケージ名、並行するチェックアウトを勝手に作り出してはいけません。インストール後は、設定を作成する前に `fcsa --help` を再度実行してください。
3. **設定フォルダーを作成する。** `fcsa init <config-dir>` — `scan_paths` を、まず設定フォルダー**内部**に新しく作成される `inbox/` フォルダーに設定し、実際のユーザーフォルダーを自動的に設定することは決してありません。そのためのサンプルテンプレート：モジュール内の `fcsa/_examples/*.example.json`。
4. **設定を実際の依頼に合わせて調整する。** `scan_paths` を指定されたソースフォルダーに設定し、`categories-definitions.json` に指定されたファイルの種類向けの検出パターンを記入し（`default_target` = 指定されたターゲット）、`action-rules.json` に適切なアクション（通常は `move`、必要に応じてその前に `duplicate_check`）を設定します。`state_dir`/`trash_dir` は `scan_path` の内部に置いてはいけません（モジュールはこれを拒否します — さもないと自己フィードのループになります）。
5. **必ず最初にドライランを提示する：** `fcsa run --config-dir <config-dir> --dry-run` — 結果をユーザーに見せます（何がどこへ移動されるか、何が重複として検出されたか）。
6. **本番有効化はユーザーの明示的な了承を得てからのみ行う。** その後に初めて `fcsa run --config-dir
   <config-dir>`（`--dry-run` なし）を実行します。`fcsa status --config-dir <config-dir>` は、その後の状態を表示します。
7. **段階的に拡張する**（ユーザー：「そして、時間とともにこれが拡張されていく」）：新たにセットアップを始めるのではなく、カテゴリーやフォルダーを追加していきます。3つの設定ファイルは追加方式で保守できます。拡張のたびに、設定のフィンガープリントがあるため、次の本番実行の前に再びドライランが必要です。

## 制限事項 / 既知の未解決事項 (チケット T-20260818-916568570 時点)

- モジュールはパス1であり、ステータスは "development" です — コアパイプライン、CLI、安全ゲートは
  完成してテスト済みです (63/63 テスト) が、**実際のユーザーフォルダに対してはまだ一度も
  本番有効化されていません**。最初の本番有効化は意図的にこのスキルの利用時に行います。
  リポジトリの公開範囲は "private" です — 専用の `repo-publish-check` を行わずに公開しないでください。
- 仕様上の抜け漏れについて、2通りの解釈が文書化されています (モジュール内の `CHANGELOG.md`/`TODO.md`):
  `default_stepping: false` は、二重に列挙されたアクションを**1回**の実行にまとめます。
  結果が `skip` の `duplicate_check` は、そのファイルに対する残りの**すべての**アクションチェーンを中止します (move/copy だけではありません)。
  必要に応じて、設定がこれらに依存する前にユーザーと確認してください。
- OCR は差し替え可能なバックエンドです (`none`/`command`) — 独自の OCR エンジンは同梱されていません。
  実際の OCR 抽出を行うには、`ellmos-filecommander` `fc_ocr` を `command` バックエンドタイプ経由で接続してください。

## 由来

このモジュールはチケット T-20260818-916568570 (パス1、fcsa-worker) で構築され、ユーザーの要望により、
上記で説明したトリガーがまさに発生するまで意図的に受動的に保留 (PARKED/until-trigger) されています。
このスキルは、まさにその保留メモを実行に移すものです。

## 変更履歴

### 1.0.0 (2026-08-18)
- 初版。「ファイルを自動的に収集/整理する」という依頼のトリガー検出、
  ドライラン必須のセットアップ手順、およびユーザーの了承後にのみ行う本番有効化を文書化しました。
