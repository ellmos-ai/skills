---
name: bewerbungsexperte
version: 1.1.0
type: expert
author: BACH Team / ellmos (standalone port)
created: 2026-01-25
updated: 2026-06-22
description: 応募プロセス全体のためのスペシャリスト。求人情報の分析、プロフィール（LinkedIn/CV）の最適化、テーラーメイドのカバーレターの生成を行います。SQLiteデータベースとフォルダ構造からASCII履歴書を生成します。cv_generator.py はスタンドアロンで移植されており、BACHランタイムは不要です。
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

## 起動

```bash
# データベースアクセスなしのサンプルCV（日本語）
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --dry-run

# SQLiteデータベースからCVを生成（日本語）
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad/zu/daten.db>

# CVをファイルに保存（日本語）
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad> --output lebenslauf.txt

# フォルダスキャン付き（日本語）
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad> --career-path <ordner>
```

## サービスカタログ

### 1. CV生成（`cv_generator.py`）
- **個人データ:** `assistant_user_profile` テーブルから読み込み（キー/値）
- **職歴:** 雇用主フォルダをスキャン（証明書、契約書）
- **学歴:** 学位フォルダをスキャン
- **研修・資格:** 認定証フォルダをスキャン
- **推薦人:** `contacts` テーブルから（category='beruflich'）
- **ドライラン:** データベースなし -- テスト用のサンプルデータ

### 2. 求人診断
- **キーワードマッチング:** CVと求人要件の照合（ATS safe）
- **企業チェック:** 企業文化や福利厚生の調査

### 3. 応募書類サービス
- **CVチューニング:** 経験の構造化と要点整理
- **カバーレター:** 個別化された説得力のある書類の作成
- **ポートフォリオ:** 制作実績や推薦人に関するアドバイス

## データベーステーブル（任意）

`cv_generator.py` は、存在する場合以下のテーブルから読み込みます：

- `assistant_user_profile` (key TEXT, value TEXT) — 個人データ
  - フィールド: name, full_name, email, phone, address, birthday, nationality, marital_status
- `contacts` (name, organization, position, phone, email, is_active, category) — 推薦人

存在しないテーブルは無視されます（CVの該当セクションは空になります）。

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

## CLIオプション

```
--db <pfad>           SQLiteデータベースへのパス（--dry-run なしの場合は必須）
--output, -o          出力ファイル（指定なしの場合は stdout）
--career-path         雇用主フォルダへのパス
--education-path      学位・学歴フォルダへのパス
--certs-path          資格・研修フォルダへのパス
--dry-run             データベースアクセスなしのサンプルCV
```

## ワークフロー: CV生成

1. **準備**
   - SQLite DBを用意する（BACH DBまたは自作DB）
   - ドキュメントを含むフォルダ構造を作成する（任意）

2. **DBなしのテスト**
   - `python cv_generator.py --dry-run` -- ツールが正常に動作するか確認

3. **生成**
   - `python cv_generator.py --db <pfad> --career-path <arbeitgeber>`
   - 出力を確認し、必要に応じて微調整

4. **エクスポート**
   - `python cv_generator.py --db <pfad> --output lebenslauf.txt`

## 依存関係

Python標準ライブラリのみ: `sqlite3`、`pathlib`、`argparse`、`re`、`datetime`。
pipインストール不要、BACHランタイムのインポート不要。

## 変更履歴

### 1.1.0 (2026-06-22)
- BACH v1.0.0 からスタンドアロン版として移植
- ハードコードされたオリジナルのDBパスの代わりに `--db <pfad>` を使用
- `--dry-run` モードを追加
- `--scan-folders` を削除（BACHの user_data_folders テーブルが必要だったため）
- フッターテキストを中立化
- BACHランタイムからの独立性を検証済み

### 1.0.0 (2026-01-25、BACH内部)
- BACH system/agents/_experts/bewerbungsexperte/ における初期バージョン

---
ステータス: アクティブ
ドメイン: キャリアコンサルティング
