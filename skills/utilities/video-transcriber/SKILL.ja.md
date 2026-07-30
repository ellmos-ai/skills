---
name: video-transcriber
version: 1.1.0
type: tool
author: Lukas Geiger
created: 2026-04-04
updated: 2026-06-20
description: オンライン動画ソースから動画の書き起こし（字幕）とメタデータを取得し、Markdown、JSON、またはプレーンテキストで出力します。現在サポート中：YouTube。手動作成字幕を優先し、自動生成字幕にフォールバックします。

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [video, transcript, subtitles, metadata, research, youtube]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['youtube-transcript-api', 'yt-dlp']}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/youtube_extractor.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-04-04', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="video-transcriber banner">

> **日本語** — `video-transcriber` の公式日本語版。


# Video Transcriber (日本語)

オンライン動画の書き起こし（字幕）およびメタデータ（タイトル、チャンネル、日付、再生回数、
概要）を取得します。手動で作成された字幕を優先し、自動生成された字幕に
フォールバックします。Markdown、JSON、またはプレーンテキストで出力します。

現在サポートされているソース：**YouTube**（youtube.com, youtu.be, youtube-nocookie.com）。

動画の場合、内容を手動で要約する代わりにこのツールを使用してください ——
書き起こしが信頼できる情報源です。

> **注意：** このツールは YouTube または Google と提携、承認、スポンサー関係に
> ありません。使用はユーザー自身の責任において行ってください。ユーザーは、該当プラットフォームの
> 利用規約および適用される著作権法を遵守する全責任を負います。DRM、ペイウォール、
> またはアクセス制限の回避は不可。大量のスクレイピングは不可。権利者の同意なしに
> 著作権で保護された書き起こしを再配布することは不可。

## 依存関係とライセンス

```bash
pip install youtube-transcript-api   # 書き起こし（必須） — MITライセンス
pip install yt-dlp                   # メタデータ（オプション、フォールバック: noembed） — Unlicense (パブリックドメイン)
```

## 使い方

> **Windowsに関する注意：** 常に `PYTHONIOENCODING=utf-8` を設定してください。そうしないと、
> 出力時にウムラウトや特殊文字が文字化けします（cp1252エンコーディング）。

```bash
# デフォルト：タイムスタンプ付きMarkdown
PYTHONIOENCODING=utf-8 python video_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"

# 出力フォーマットを選択
PYTHONIOENCODING=utf-8 python video_transcriber.py URL --format markdown|json|plain

# ファイルに保存
PYTHONIOENCODING=utf-8 python video_transcriber.py URL -o transcript.md

# 優先言語（デフォルト: de en）
PYTHONIOENCODING=utf-8 python video_transcriber.py URL --lang de en fr
```

### オプション

| オプション | 効果 |
|------------|------|
| `--format markdown\|json\|plain` | 出力フォーマット（デフォルト: markdown） |
| `--output, -o <file>` | stdout ではなくファイルに書き込む |
| `--lang <codes...>` | 優先する字幕言語（デフォルト: de en） |
| `--meta-only` | メタデータのみ、書き起こしなし |
| `--transcript-only` | 書き起こしのみ、メタデータなし |
| `--no-timestamps` | タイムスタンプなしの書き起こし |
| `--no-meta` | 高速化: yt-dlp メタデータをスキップ |

### Pythonライブラリとして

```python
from video_transcriber import extract_video_id, fetch_metadata, fetch_transcript, format_markdown

video_id = extract_video_id("https://www.youtube.com/watch?v=VIDEO_ID")
meta = fetch_metadata(video_id)
transcript = fetch_transcript(video_id, languages=["de", "en"])
output = format_markdown(meta, transcript)
```

## 典型的なユースケース

- リサーチ：動画コンテンツをテキストとして引用可能にする
- 出典分析：講演における論理展開/比喩の検証
- 要約：ハルシネーションの代わりに信頼できる基盤としての書き起こし

## 制限事項

- 動画に字幕（手動または自動）がある場合のみ動作
- 自動字幕には認識エラーが含まれる場合があります
- 音声ダウンロードなし、組み込み音声認識なし

## 変更履歴

### 1.1.0 (2026-06-20)
- `yt-transcriber` から `video-transcriber` に名称変更（YouTubeのブランディングポリシー：
  "yt" は明示的に禁止された略称です。RECHTSCHECK_2026-06-20.md を参照）
- スクリプト：`yt_transcriber.py` → `video_transcriber.py`
- 免責事項と依存関係ライセンスを追加（ユーザーの責任、利用規約、承認なし）
- YouTubeは情報源として記述的にのみ言及され、名前/ブランドコンポーネントとしては使用されません
- 下位互換性ラッパー `yt_transcriber.py` を旧パスに保持

### 1.0.0 (2026-06-12)
- SKILL.md を追加（ツールはスクリプト + README としてすでに存在していました）
- スクリプト v1.0.0：書き起こし + メタデータ、3つの出力フォーマット、言語優先設定