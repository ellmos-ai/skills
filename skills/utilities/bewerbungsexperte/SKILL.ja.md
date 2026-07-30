---
name: bewerbungsexperte
version: 1.1.0
type: expert
author: BACH Team / ellmos (standalone port)
created: 2026-01-25
updated: 2026-06-22
description: 応募プロセス全体のためのスペシャリスト。求人情報を分析し、プロフィール（LinkedIn/CV）を最適化し、カスタマイズされたカバーレターを生成します。SQLite データベースとフォルダ構造から ASCII 形式の履歴書を生成します。cv_generator.py はスタンドアロン移植版です -- BACH ランタイムは不要です。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [bewerbung, cv, anschreiben, linkedin]
language: ja
status: active
dependencies: {'tools': ['cv_generator.py'], 'services': [], 'protocols': [], 'python': ['sqlite3', 'pathlib', 'argparse', 're']}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/_experts/bewerbungsexperte/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
---

> **日本語** — `bewerbungsexperte` の公式日本語版。


<img src="banner.png" width="100%" alt="bewerbungsexperte banner">
# BEWERBUNGSEXPERTE v1.1 (日本語)

> 次のキャリアステップのための戦略的パートナー。

## アクティベーション

```bash
# データベースアクセスなしのサンプル CV (日本語)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --dry-run

# SQLite データベースから CV を生成 (日本語)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <path/to/data.db>

# CV をファイルに保存 (日本語)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <path> --output lebenslauf.txt

# フォルダスキャン付き (日本語)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <path> --career-path <folder>
```

## サービスカタログ

### 1. CV 生成 (`cv_generator.py`)
- **個人データ:** `assistant_user_profile` テーブルから読み込み（キー/値）
- **職務経歴:** 雇用主フォルダをスキャン（証明書、契約書）
- **学歴:** 学位フォルダをスキャン
- **研修・資格:** 認定証フォルダをスキャン
- **照会先:** `contacts` テーブルから（category='beruflich'）
- **Dry-Run:** データベースなし -- テスト用サンプルデータ

### 2. 求人診断
- **キーワードマッチング:** CV と求人要件の照合（ATS 対応）
- **会社チェック:** 企業文化や福利厚生の調査

### 3. 応募書類サービス
- **CV チューニング:** 経験の構造化とアピールポイントの明確化
- **カバーレター:** 個別化された説得力のある手紙の作成
- **ポートフォリオ:** 成果物や参照資料の相談

## データベーステーブル（オプション）

`cv_generator.py` は、存在する場合以下のテーブルから読み込みます:

- `assistant_user_profile` (key TEXT, value TEXT) — 個人データ
  - フィールド: name, full_name, email, phone, address, birthday, nationality, marital_status
- `contacts` (name, organization, position, phone, email, is_active, category) — 照会先

欠落しているテーブルは無視されます（CV 内の空のセクション）。

## フォルダ構造（--career-path 用など）

```
_Arbeitgeber/
  Firma_A_2020-2023/
    Arbeitsvertrag.pdf
    Arbeitszeugnis.pdf
  Firma_B_2018-2020/
    ...
_Abschluesse/
  Universitaet/
    Bachelor_Zeugnis.pdf
_Fortbildungen/
  Zertifikat_Cloud_AWS_2024.pdf
```

## CLI オプション

```
--db <パス>           SQLite データベースへのパス（--dry-run なしの場合は必須）
--output, -o          出力ファイル（指定なしの場合は stdout）
--career-path         雇用主フォルダへのパス
--education-path      学位フォルダへのパス
--certs-path          認定証フォルダへのパス
--dry-run             データベースアクセスなしのサンプル CV
```

## ワークフロー: CV 生成

1. **準備**
   - SQLite DB を用意（BACH DB または独自の DB）
   - ドキュメントを含むフォルダ構造を作成（オプション）

2. **DB なしのテスト**
   - `python cv_generator.py --dry-run` -- ツールが動作するか確認

3. **生成**
   - `python cv_generator.py --db <パス> --career-path <雇用主>`
   - 出力を確認し必要に応じて調整

4. **エクスポート**
   - `python cv_generator.py --db <パス> --output lebenslauf.txt`

## 依存関係

Python 標準ライブラリのみ: `sqlite3`, `pathlib`, `argparse`, `re`, `datetime`。
pip インストール不要、BACH ランタイムのインポート不要。

## 変更履歴

### 1.1.0 (2026-06-22)
- BACH v1.0.0 からスタンドアロン移植
- ハードコードされた元の DB パスの代わりに `--db <パス>` を使用
- `--dry-run` モードを追加
- `--scan-folders` を削除（BACH の user_data_folders テーブルが必要だったため）
- フッターテキストを中立化
- BACH ランタイムからの独立性を検証

### 1.0.0 (2026-01-25, BACH 内部)
- BACH system/agents/_experts/bewerbungsexperte/ での初期バージョン

---
ステータス: アクティブ
ドメイン: キャリアコンサルティング