---
name: migrate-rename
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: ラッパーファイルを使用した進化的なファイルのリネーム。ハードブレイク（強制断绝）なしでリネームを可能にし、日常的な使用を通じて参照が自然に更新されます。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [migration, renaming, wrapper, evolutionary, refactoring]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/migrate-rename.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **日本語** — `migrate-rename` の公式日本語版。


# ラッパーを使用したファイルのリネーム（進化的移行）(日本語)

> ハードブレイク（強制破断）なしでファイルのリネームを可能にします。参照は日常的な使用を通じて自然に更新されます。

---

## 原理: 進化的移行

```
変更前:                          変更後:
old_file.md                      new_file.md (リネーム済み)
   |                                |
   +-- 参照 A                       +-- old_file.md (ラッパー)
   +-- 参照 B                              |
   +-- 参照 C                              +-- ログテーブル
                                           +-- 手順指示
                                           +-- new_file.md へのリンク
```

古いパスにアクセスが発生した際：
1. ラッパーファイルに到達
2. ログにエントリを追加
3. ここへ誘導した参照箇所を修正
4. 実際のファイルへ移動

---

## ステップ・バイ・ステップ

### 1. ファイルのリネーム

```bash
mv old_file.md new_file.md
```

### 2. ラッパーファイルの作成

以下の内容で `old_file.md` を作成します：

```markdown
# OLD_FILE.md - リダイレクト済み (日本語)

**ステータス:** このファイルは `new_file.md` にリネームされました

---

## 移行ログ

| 日付 | 担当者 | 呼び出し元 | 参照修正済み？ |
|------|--------|------------|----------------|
| YYYY-MM-DD | [名前] | 初回移行 | 該当なし（ラッパー作成） |

---

## 手順指示

1. **ログエントリを残す**（上の表に入力）
2. **呼び出し元の確認**: 何があなたをここに誘導しましたか？
3. **参照の修正**: `old_file.md` -> `new_file.md` に変更
4. **実際のファイルへ移動**: [new_file.md](new_file.md)

---

**対象ファイル:** [new_file.md](new_file.md)
```

### 3. 重要な参照の即时修正
- ヘルプファイル（プライマリドキュメント）
- システムプロンプトの参照箇所
- パスを直接使用する CLI コード

### 4. 残りの参照を演進的に移行
残りの箇所は、使用に伴って自動的に修正されます。

---

## ラッパー手法をいつ使用すべきか？

**推奨 — ラッパーが有用:**
- 潜在的な参照箇所が多数ある
- さまざまなパートナー/ツールから参照されている
- 重大なシステムファイルではない

**非推奨 — すべて直接変更:**
- 判明している参照箇所が少なめ
- 重大なシステムファイル（設定、DB スキーマ）
- パフォーマンスが重要なパス

---

## クリーンアップ

約 30 日後、またはログに新しいエントリが表示されなくなった場合：
1. ラッパーファイルを `_archive/deprecated/` に移動
2. または完全削除（新しいエントリがない場合）

---

## 変更履歴

### 1.0.0 (2026-03-15)
- BACH v3.8.0 から移植

---

*BACH v3.8.0 から移植 | スタンドアロン版*