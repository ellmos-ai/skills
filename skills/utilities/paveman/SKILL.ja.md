---
name: paveman
version: 1.0.1
type: skill
author: Lukas Geiger + Claude
created: 2026-08-19
updated: 2026-08-20
description: "既存のルールファイルやメモリファイル（「CLAUDE.md を短くして」「MEMORY.md が長すぎる」「技術的な内容に触れず、ドキュメントを圧縮して」「このルールファイルは文字数の上限で切り捨てられる」など）を短くする依頼を検出し、その際にモジュール paveman を使用します。paveman は、モデルを使用しない決定的な CLI ツールで、Markdown やテキストファイルの散文を短縮します。既定はドライラン（試行実行）で、ロールバックと、パス・見出し・コードを対象とする厳格な保護バリデーターを備えています。「<Datei> を短くして」「このファイルは長すぎる／切り捨てられる」「shrink this rule file」「内容を変えずに圧縮して」などの表現や、ルールファイルやメモリファイルが文字または行の上限に達していることが明らかな場合に、このスキルを使用してください。"
# Kompatibilität
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: utilities
tags: [kürzen, kompression, regeldatei, gedächtnis, deterministisch, dry-run, rollback, dokumentation]
language: ja
status: active
visibility: public

# Abhängigkeiten
dependencies:
  tools: [paveman]
  services: []
  protocols: []
  python: []
  modules: [paveman]

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: cb1c7bfcbc7a4592a1df4a844c4e3d2a5f5da3f268d81b246c0ce05024927bc1
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:31:29.342138+00:00"
---
<img src="banner.png" width="100%" alt="paveman banner">

# Paveman — ルールファイルおよびメモリファイルを決定的に短縮する

> 別途提供されるモジュール `paveman` を呼び出す、薄いユーザー非依存のスキルラッパーです。
> このスキルは、ツールが適しているタイミングを判断し、その安全な手順を説明します。特定のマシン、
> 固定のインストールパス、個人用のプロファイルは前提としません。

## このスキルが適用される場面

トリガーとなるのは、**既存のルール・規約・メモリファイル**を、その内容の意味を変えずに短くしたいというユーザーの発話です。

- 「`<Datei>` を短くして」／「このファイルは長すぎる」／「X 文字または行で切り捨てられる」
- 「技術やコードに触れずに、ドキュメントを圧縮して」
- 「MEMORY.md や CLAUDE.md が長くなりすぎた」
- 「このルールファイルを簡潔にして。ただし意味は変えないで」
- **既存ファイルを短くする**ことを指すあらゆる表現。**新規作成**や**翻訳**を指すものは含みません（後述の区別を参照）。

**このスキルの対象外**:

- **`knappform`** — 会話中にモデル自身が話す様式（LLM のコミュニケーションスタイル。モデルベースで、ファイルアクセスはありません）を変更します。一方 `paveman` は、モデル呼び出しなしで既存ファイルの内容を決定的に変更します。両者は併用できます。技術的にも機能的にも別物です。
- **`bilingual-doc-sync`** — 不足している言語版を生成します。`paveman` は一つの版を短くするだけで、翻訳は行いません。
- **`llm-text-hygiene`** — テキストから AI の痕跡やチャットの残りを取り除きます。短縮とは別の目的です。
- 新しい内容を書いたり、作り出したりすること — `paveman` は、既にあるものを短くするだけです。

## モジュールの機能

`paveman` は、Markdown やテキストファイル向けのルールベースで決定的な散文短縮ツールです。モデル呼び出し、トークン、ネットワーク送信はありません。提供方法はシステムごとに異なる場合があります。正となるのは、そのシステムで承認されたモジュールまたはパッケージのバージョンです。

| フラグ | 効果 |
|---|---|
| *（フラグなし）* | **ドライラン（既定）。** 差分と文字数の削減量を表示し、何も書き込みません。 |
| `--apply` | 実際に書き込みます。書き込み前に自動でバックアップを作成します。 |
| `--rollback` | 直近のバックアップを復元します。 |
| `--locker` | パスや見出しの逸脱を、エラーではなく警告としてのみ報告します。 |
| `--kontext N` | 差分のコンテキスト行数を指定します。 |

**保護バリデーターは、毎回の呼び出しで実行されます。** コードブロック、パス、見出しを変更してはなりません。標準モードでは、逸脱を報告するだけでなく、逸脱があれば書き込みを阻止します。

## 手順 — 必ずこの順序で実行

1. **まずドライランを行う。** `--apply` を付けずに `paveman <Datei>` を実行します。文字数の削減量、差分、バリデーターの状態（「OK」または具体的なエラーメッセージ）をユーザーに提示してください。
2. **明示的な承認を得た場合のみ書き込む。** その後にのみ `paveman <Datei> --apply` を実行します。ドライランから書き込みモードへ自動で切り替えてはなりません。
3. **書き込み前に `--rollback` について触れておく。** 望ましくない結果をどのように取り消せるかを、ユーザーが事前に知っている必要があります。
4. **バリデーターのエラーを軽視しない。** `--locker` を、エラーを回避するためだけに使用しないでください。まず、その逸脱が本当に無害かを確認します。より緩いモードは、ユーザーが意図的に選択する必要があります。
5. **意図的に作成された内容を尊重する。** ルールベースのツールは、ある表現が意図的に詳しく書かれているかを確実に判断できません。判断に迷う場合は、ドライランの差分を慎重に確認してください。

## 前提条件 — モジュールの利用可能性を確認する

1. `paveman --help` で、現在の環境で CLI が利用可能かを確認します。
2. コマンドが見つからない場合は、このシステムで承認されたモジュールまたはパッケージの入手経路を確認してください。ローカルのパス構造、パッケージ名、リポジトリを推測で作り出してはなりません。
3. 承認された入手元を解決できない場合は、不足している前提条件を独立したセットアップ項目として報告してください。スキルを盲目的に実行したり、並行するモジュールを作成したりしてはなりません。
4. インストール後は、まず再度 `paveman --help` を実行し、その後に無害なドライランを行ってください。実際の書き込みテストには、引き続きユーザーの承認が必要です。

## 例

```text
User: „Kürze meine CLAUDE.md, sie wird beim Sessionstart abgeschnitten.“

→ `paveman CLAUDE.md` (Trockenlauf)
→ Ergebnis: „12.400 → 9.800 Zeichen (-21 %), Validator: OK.“
→ Diff zeigen und auf `--rollback` hinweisen.
→ Nutzer bestätigt.
→ `paveman CLAUDE.md --apply`
```

```text
User: „MEMORY.md ist zu voll, kürze sie bitte.“

→ Trockenlauf: „893 → 893 Zeichen, keine Regel griff — der Text ist bereits knapp.“
→ Kein `--apply` empfehlen; den fehlenden Mehrwert ehrlich melden.
```


## 変更履歴

### 1.0.1 (2026-08-20)

- 公開ラッパーから、マシン名、ローカルのチェックアウトパス、インストール情報、非公開のチケット参照、ローカルのテスト結果を完全に切り離しました。
- ユーザー非依存の利用可能性・インストールの取り決めを追加し、ドイツ語の正しいウムラウト（ä、ö、ü）に修正しました。

### 1.0.0 (2026-08-19)

- ドライラン、承認ステップ、ロールバック、バリデーターの境界を備えた、公開版ラッパーの最初のリリース。
- `knappform`、`bilingual-doc-sync`、`llm-text-hygiene` との区別を明記しました。
