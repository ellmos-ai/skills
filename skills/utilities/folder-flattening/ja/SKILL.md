---
name: folder-flattening
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: ネストされたフォルダ階層をフラットでマシン読み取り可能なレイアウトに再構築します。インテリジェントなマージロジックを備えた Bash ベース。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [folder, flattening, filesystem, bash, reorganization, cleanup]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/ordner-flattening.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **日本語** — `folder-flattening` の公式日本語版。

# ワークフロー: Folder Flattening

目的: ネストされたフォルダ構造をフラットでマシン読み取り可能な構造に変換します。
利点: ディレクトリの手動クリック探査が不要になり、データベース（`Verzeichnis.db`）を介して検索できます。
テーマ的に意義がある場合は重複が許可されます。

---

## フェーズ概要

| フェーズ | 処理内容 | スクリプトセクション |
|-------|-------------|----------------|
| 1 | フラット化（Flatten）: すべてのサブフォルダを1つの階層に移動 | `phase_flatten` |
| 2 | 短縮（Shorten）: 長いパス名を最後のセグメントに切り詰め、衝突時はマージ | `phase_shorten` |
| 3 | クリーンアップ: 複数のアンダースコア（`___`）を解消し、末尾の `_` を削除 | `phase_cleanup_underscores` |
| 4 | グループ化: 数字フォルダ、CDフォルダ、短い名前をコレクションフォルダに移行 | `phase_group_problematic` |
| 5 | トリプレット分析: 3つのスライドグループで最小長の名前をマージターゲットに設定 | `phase_tripel_merge` |
| 6 | メディアフォーマットマージ: ファイルタイプ別にフォルダを統合（テンプレート） | `phase_media_merge` |
| 7 | クリーンアップ: 空フォルダを削除 | `phase_cleanup_empty` |

---

## 重要なルール

### トリプレット分析マッチング
- **部分文字列**: `EducationalBrochures` 内の `Education` -> `Education` へマージ
- **複数形/ウムラウト**: `Room` = `Rooms`, `Part` = `Parts`, `Book` = `Books`
- **最初の単語**: `Autism ADHD` は `Autism Career` と一致（接頭辞が同じ）

### 最小長
- スペースなしの単一単語名: **少なくとも8文字**（`Hand`、`House`、`Form` などの誤統合を防止）
- スペースあり（例: `ICF Catalog`）: **3文字以上でOK**
- これにより `ICF`、`ASD Women` などが保持されます

### マージ後の再起動
マージが完了するたびにフォルダリストが再読み込みされ、マージターゲットから再開されます。
これにより、たとえば `Autism` は次に進む前にすべての拡張名を収集します。

---

## メディアフォーマットマージ（テンプレートシステム）

フェーズ6ではテンプレート配列 `MEDIA_TYPES` を使用します。各エントリーの定義:
- ターゲットフォルダ（`_` プレフィックス付き）
- このタイプに属するファイル拡張子

```bash
MEDIA_TYPES=(
    "_Audio|mp3|m4a|wav|flac|ogg|wma|aac|opus|aiff"
    "_Video|mp4|avi|mkv|mov|wmv|flv|webm|m4v|mpg|mpeg|3gp"
    "_Images|jpg|jpeg|png|gif|bmp|tiff|tif|webp|svg|ico|heic|heif|raw|cr2|nef"
    # Extensible:
    # "_Spreadsheets|xlsx|xls|csv|ods"
    # "_Presentations|pptx|ppt|odp"
    # "_Code|py|js|ts|sh|bat|ps1"
    # "_CAD|dwg|dxf|step|stl"
    # "_3D|obj|fbx|blend|gltf|glb"
    # "_Fonts|ttf|otf|woff|woff2"
)
```

単一タイプのファイル**のみ**を含むフォルダが移動対象となります。
サブフォルダを含むフォルダはスキップされます。

### 新しいメディアタイプの追加

`MEDIA_TYPES` 配列に新しい行を追加するだけです:
```bash
"_TargetFolder|ext1|ext2|ext3"
```

---

## 実行

```bash
# Complete run:
cd /path/to/target/directory
bash ordner_flattening_komplett.sh

# Or individual phases:
bash ordner_flattening_komplett.sh --phase flatten
bash ordner_flattening_komplett.sh --phase tripel
bash ordner_flattening_komplett.sh --phase media
bash ordner_flattening_komplett.sh --phase cleanup
```

---

## 運用実績値（2026-01-26 セッション）

- 開始時: 206 フォルダ + 252 ルーズファイル、約 5600 ネストサブフォルダ
- フラット化後: 1階層に約 2200 フォルダ
- 短縮＋クリーンアップ後: 約 2005 フォルダ
- グループ化（数値、CD）後: 約 2005 -> コレクションフォルダ作成
- トリプレット v1 後: 約 1561 フォルダ
- トリプレット v2（8文字ルール）後: さらに削減
- メディアフォーマットフェーズ: 音声/動画/画像フォルダを統合
