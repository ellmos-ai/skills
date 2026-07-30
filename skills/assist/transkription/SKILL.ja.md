---
name: transkription
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: 音声/動画ファイルをテキストに文字起こしします。オプションのバックエンドとして Whisper (openai-whisper) または Vosk (オフライン) を使用し、存在確認によって検出されます。バックエンドがない場合：ダミー出力のプレースホルダーモード (dry-run)。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [transkription, audio, speech-to-text, whisper, vosk, offline]
language: ja
status: stable
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': [{'name': 'openai-whisper', 'optional': True, 'install': 'pip install openai-whisper', 'purpose': 'STT backend option 1 (cloud/local model)'}, {'name': 'vosk', 'optional': True, 'install': 'pip install vosk', 'purpose': 'STT backend option 2 (fully offline)'}]}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein direkter BACH-Origin vorhanden (transkriptions-service existiert nicht als Datei in BACH/system). Skill neu konzipiert. voice_stt.py aus BACH/hub/_services/voice/ hat das Backend-Muster inspiriert (optionale Imports mit Verfügbarkeits-Flags), wurde aber nicht direkt portiert.\n'}
---

<img src="banner.png" width="100%" alt="transkription banner">

> **日本語** — `transkription` の公式日本語版。


## 概要と目的

音声/動画ファイルをテキストに変換します — クラウドアクセスを必須とせず、ローカルで実行されます。このスキルは Whisper または Vosk がインストールされているかを自動的に検出し、利用可能な最適なバックエンドを選択します。バックエンドがない場合はドライラン（dry-run）モードで動作し、プレースホルダーテキストを返すため、ワークフローは常に機能します。

文字起こし結果はローカルの `transkription/store.db` に保存され、照会可能です。

---

## トリガー

| フレーズ | アクション |
|---|---|
| "Transcribe this audio" | 音声ファイルを文字起こし |
| "Transcribe [file]" | 指定したファイルを文字起こし |
| "Show my transcripts" | 最新の文字起こし一覧を表示 |
| "Search transcript [term]" | 文字起こし結果の全文検索 |
| "Export transcript [ID]" | 文字起こし結果を TXT としてエクスポート |

---

## ワークフローと手順

1. **バックエンド確認**: `whisper` または `vosk` がインポート可能か確認。
2. **ファイル確認**: 入力ファイルが存在すること（音声: wav, mp3, m4a, ogg, flac; 動画: mp4, mkv, webm — ffmpeg 経由で抽出）。
3. **文字起こし**: バックエンドを呼び出して生テキストを取得。
4. **保存**: メタデータ（ファイル、再生時間、言語、バックエンド、タイムスタンプ）とともに `store.db` に結果を保存。
5. **出力**: テキストを返却。オプションで `.txt` としてエクスポート。

---

## CLI エントリーポイント

```bash
# Transcribe file (Deutsch)
python transkription_core.py transcribe audio.wav

# With explicit language (Deutsch)
python transkription_core.py transcribe audio.mp3 --lang de

# Dry-run (no backend required) (Deutsch)
python transkription_core.py transcribe audio.wav --dry-run

# List transcripts (Deutsch)
python transkription_core.py list [--limit 20]

# Full-text search (Deutsch)
python transkription_core.py search "term"

# Export (Deutsch)
python transkription_core.py export <id> [--out file.txt]

# Backend check (Deutsch)
python transkription_core.py check

# Alternative store path (e.g. for tests) (Deutsch)
python transkription_core.py --store /tmp/test.db transcribe audio.wav --dry-run
```

---

## ストレージ

| 項目 | 値 |
|---|---|
| タイプ | SQLite |
| パス (デフォルト) | `skills/assist/transkription/store.db` |
| 上書き設定 | `--store <path>` または環境変数 `TRANSKRIPTION_STORE` |
| テーブル | `transcripts` |

### スキーマ `transcripts`

```sql
CREATE TABLE IF NOT EXISTS transcripts (
    id          TEXT PRIMARY KEY,  -- UUID (short: 8 hex)
    file_path   TEXT NOT NULL,     -- original path of audio file
    file_name   TEXT NOT NULL,     -- filename (without path, for display)
    text        TEXT NOT NULL,     -- transcribed text
    language    TEXT,              -- language (e.g. "de", "en")
    backend     TEXT,              -- "whisper" | "vosk" | "dry-run"
    duration_s  REAL,              -- duration in seconds (if known)
    created_at  TEXT NOT NULL,     -- ISO-8601 timestamp
    tags        TEXT               -- comma-separated tags (optional)
);
```

---

## 動作・方針

- バックエンドがインストールされていない場合、スキルはドライランモード（デモテキスト）で動作します。
- Vosk よりも Whisper が優先されます（ドイツ語の品質が向上するため）。
- Whisper と Vosk の選択は `assist/prefs.json` で設定できます (`transkription_backend: "whisper"|"vosk"|"auto"`)。
- 動画抽出用の ffmpeg は別途必要であり、本スキルには含まれていません。

---

## プライバシー

- **すべての文字起こしデータはローカルに保持されます** — Whisper オンラインモードを使用しない限りクラウド転送はありません。
- Whisper はローカル（tiny/base/medium モデル）または OpenAI API 経由で使用できます。デフォルトではローカルモデルが使用されます。
- `store.db` には機密性の高い会話内容が含まれる可能性があります — **Git にコミットしないでください**。
- 推奨事項: `store.db` を `.gitignore` に追加してください。

---

## 関連リソース

- BACH `hub/_services/voice/voice_stt.py` — バックエンドパターン（インスピレーション、読み取り専用）
- スキル `utilities/yt-transcriber` — YouTube 文字起こし（別スキル、重複ではありません: YT 専用）
- `tools/module-installer/module_installer.py` — レジストリに whisper + vosk が含まれます

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|---|---|---|
| 0.1.0 | 2026-06-22 | 初回作成 — 独自の SQLite ストレージ、Whisper/Vosk 存在確認 |