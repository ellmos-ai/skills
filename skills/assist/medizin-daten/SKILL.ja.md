---
name: medizin-daten
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: 医療データのローカルかつプライベートな記録：診断、症状の履歴、検査計画。BACH由来なし — 独自のSQLiteストアを備えたカスタム設計。厳密にローカル対応、クラウド転送なし。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [medizin, diagnose, symptome, gesundheit, privat, lokal]
language: ja
status: stable
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin. Skill vollständig neu konzipiert. Kein bestehendes Implementierungs-Vorbild im Ökosystem gefunden.\n'}
---

<img src="banner.png" width="100%" alt="medizin-daten banner">

> **日本語** — `medizin-daten` の公式日本語版。


## 概要と目的

個人の医療データを安全かつローカルに記録します：診断（ICD-10コードは任意）、日付系列付きの症状履歴、検査計画。すべてのデータは `medizin-daten/store.db` 内にのみローカル保存されます。

このスキルは医師の診察に代わるものではなく、医学的判断や主張を行うものでもありません。個人の健康データ管理のための構造化されたノートブックです。

---

## トリガー (Triggers)

| フレーズ | アクション |
|---|---|
| "Record a diagnosis" / 「診断を記録」 | 新しい診断を作成 |
| "Add diagnosis [name]" / 「診断 [名前] を追加」 | 名前付き診断を作成 |
| "Symptom history" / 「症状の履歴」 | 本日の症状を記録 |
| "Record symptom [name]" / 「症状 [名前] を記録」 | 単一の症状をログ記録 |
| "Examination plan" / 「検査計画」 | 今後の予定/検査を表示 |
| "Add appointment" / 「予定を追加」 | 検査の予定を入力 |
| "Show my diagnoses" / 「診断一覧を表示」 | 診断リストを出力 |

---

## ワークフローと手順

1. **モード検出**：診断 / 症状 / 検査計画
2. **入力の構造化**：日付、名称、メモ、任意のICD-10コード
3. **保存**：`store.db` に保存（ローカル、ネットワークアクセスなし）
4. **出力**：LLMコンテキスト用の読みやすい要約

---

## CLI エントリーポイント

```bash
# Create diagnosis (Deutsch)
python medizin_daten_core.py add-diagnosis "Hypertension" [--icd I10] [--note "note"]

# List diagnoses (Deutsch)
python medizin_daten_core.py diagnoses

# Record symptom (Deutsch)
python medizin_daten_core.py add-symptom "Headache" [--severity 7] [--date 2026-06-22] [--note "..."]

# Symptom history for a name (Deutsch)
python medizin_daten_core.py symptom-history "Headache" [--limit 30]

# Plan examination (Deutsch)
python medizin_daten_core.py add-exam "Blood count" [--date 2026-07-01] [--note "fasting"]

# Upcoming examinations (Deutsch)
python medizin_daten_core.py exams [--upcoming]

# Alternative store (e.g. for tests) (Deutsch)
python medizin_daten_core.py --store /tmp/med_test.db diagnoses --dry-run
```

---

## ストア (Store)

| プロパティ | 値 |
|---|---|
| タイプ | SQLite |
| パス（デフォルト） | `skills/assist/medizin-daten/store.db` |
| 上書き | `--store <path>` または環境変数 `MEDIZIN_STORE` |
| テーブル | `diagnoses`, `symptoms`, `examination_plans` |

### スキーマ (Schema)

```sql
CREATE TABLE IF NOT EXISTS diagnoses (
    id          TEXT PRIMARY KEY,     -- UUID (short: 8 hex)
    name        TEXT NOT NULL,        -- name (e.g. "Hypertension")
    icd_code    TEXT,                 -- ICD-10 code optional (e.g. "I10")
    onset_date  TEXT,                 -- onset (ISO-8601, optional)
    status      TEXT DEFAULT 'aktiv', -- aktiv | remission | abgeschlossen
    note        TEXT,                 -- free-text note
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS symptoms (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optional: assignment
    name         TEXT NOT NULL,       -- name (e.g. "Headache")
    severity     INTEGER,             -- 1–10 scale (optional)
    recorded_at  TEXT NOT NULL,       -- ISO-8601 timestamp
    note         TEXT
);

CREATE TABLE IF NOT EXISTS examination_plans (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optional: assignment
    exam_name    TEXT NOT NULL,       -- examination name
    planned_date TEXT,                -- planned date (ISO-8601)
    done_date    TEXT,                -- completed on (NULL = pending)
    note         TEXT,
    created_at   TEXT NOT NULL
);
```

---

## 方針と基本姿勢

- スキルによる医学的推奨や診断は行いません。
- ICD-10コードはフリーテキストとして保存されます — 外部データベースとの照合・検証は行いません。
- 1〜10の重症度スケールはユーザーの主観によるものです。
- 欠落値（日付、重症度）は常に許容されます — ノートブックの原則が適用されます。

---

## プライバシー (Privacy Gate)

> **警告：医療データは特に機密性が高いデータです。**

- `store.db` には高度に機密性の高い健康データが含まれています — **絶対にGitにコミットしないでください**。
- **ネットワークアクセスなし** — すべての操作は完全にローカルで実行されます。
- 外部サービスとの**共有なし**、クラウドバックエンドとの同期なし。
- バックアップの推奨：暗号化されたローカルバックアップ（例：`age`/`gpg`）。
- スキルは起動時に `store.db` がローカルファイルシステムの外にあるかどうかをチェックし、パスが同期フォルダ（OneDriveなど）内にある場合は警告を発行します。
- `~/.gitignore_global` またはローカルの `.gitignore` で `store.db` を除外する必要があります。

---

## 関連リソース

- スキル `assist/gesundheit` — 一般的な健康支援（医療データではない）
- MediPlaner（`tools/module-installer` → `mediplaner`） — 薬管理（別プログラム）

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|---|---|---|
| 0.1.0 | 2026-06-22 | 初回作成 — カスタム設計、プライバシーゲート、3テーブルのスキーマ |