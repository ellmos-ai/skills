---
name: bugfix-protocol
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 体系的な 6 段階デバッグプロトコル。クイックチェック、孤立テスト、20分ルール、バグレポートテンプレートを備えた構造化アプローチ。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [debugging, bugfix, protocol, python, pyqt6, systematic]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/bugfix-protokoll.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **日本語** — `bugfix-protocol` の公式日本語版。


# Bugfix Protocol: 体系的な 6 段階デバッグ

症状の分析から検証まで — バグに対する構造化されたアプローチ。
目的のない手探りの修正を防ぎ、持続可能な修正を保証します。

---

## 概要と目的

| フェーズ | 名称 | 目的 | 最大時間 |
|----------|------|------|----------|
| 1 | クイックチェック | 明白な原因を排除 | 2分 |
| 2 | 診断 | 根本原因を特定 | 10分 |
| 3 | 孤立テスト | バグを再現可能にする | 5分 |
| 4 | 修正 | 最小限の修正 | 10分 |
| 5 | 検証 | 修正の検証 + 副作用の確認 | 5分 |
| 6 | ドキュメント化 | 知識を保存 | 2分 |

**20分ルール：** 20分経っても進展がない場合は、アプローチを変更するか助けを求めてください。

---

## フェーズ 1: クイックチェック (2分)

深掘りする前に — 最も一般的な原因を確認します：

### チェックリスト

- [ ] **文法エラー？** エラーメッセージを注意深く読み、行を確認
- [ ] **インポートエラー？** モジュールはインストールされているか？名前は正しいか？循環インポートはないか？
- [ ] **タイポ？** 変数名/関数名は正しいか？
- [ ] **型エラー？** int の代わりに string？オブジェクトが期待される場所に None？
- [ ] **キャッシュの古化？** `__pycache__` を削除して再起動
- [ ] **環境の違い？** 正しい venv が有効化されているか？正しい Python バージョンか？
- [ ] **エンコーディング？** UTF-8 vs. cp1252 (Windows クラシック)

### クイックアクション

```bash
# キャッシュのクリア
find . -name "__pycache__" -type d -exec rm -rf {} + 2>&1
find . -name "*.pyc" -delete 2>&1

# インポートの確認
python -c "import modulename"

# 構文の確認
python -m py_compile file.py
```

---

## フェーズ 2: 診断 (10分)

### 戦略: Outside-In (外から内へ)

1. **エラーメッセージの分析** — スタックトレース (traceback) を下から上へ読む
2. **最近の変更の確認** — `git diff`, `git log --oneline -10`
3. **診断ツールの利用** — プロジェクト固有の診断ツールを使用

### 診断ツール (例)

プロジェクトに応じて、専用の診断スクリプトが役立つ場合があります：

| ツール | 目的 |
|--------|------|
| `import_diagnose.py` | インポート問題の分析 |
| `method_analyzer.py` | メソッドシグネチャの確認 |
| `env_checker.py` | 内部環境変数/パスの検証 |

> **注:** プロジェクト固有の診断ツールを作成するか、既存のものを使用してください。
> 重要なのは体系的なアプローチであり、特定のツールではありません。

### デバッグ手法

```python
# 1. Print デバッグ (シンプルだが効果的)
print(f"DEBUG: variable={variable!r}, type={type(variable)}")

# 2. ブレークポイント (対話型)
breakpoint()  # Python 3.7+

# 3. 拡張トレースバック
import traceback
traceback.print_exc()

# 4. Print の代わりにロギングを使用
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"State: {state!r}")
```

---

## フェーズ 3: 孤立テスト (5分)

### 最小再現例 (MRE)

目標: 最小限のコードでバグを再現する。

```python
# test_bug.py — 最小再現テスト
"""
Bug: [簡潔な説明]
Expected: [期待される動作]
Actual: [実際の動作]
"""

# 最小限のセットアップ
# ... 必須要素のみ

# バグトリガー
# ... バグを引き起こす正確なコード

# 期待される結果
# assert result == expected, f"Got {result}"
```

### 孤立化戦略

1. **新しいファイル:** 独立したファイルでバグを再現
2. **依存関係の削除:** バグが消えるまで、一つずつ削除
3. **二分探索:** コードブロックを半分にし、どちらの半分にバグが含まれているか確認
4. **Git bisect:** `git bisect start`, `git bisect bad`, `git bisect good <commit>`

---

## フェーズ 4: 修正 (10分)

### 原則

1. **最小限:** 変更は可能な限り少なく
2. **理解:** 決して盲目的に修正しない — なぜ壊れているのかを理解する
3. **単一のタスク:** 1 コミットにつき 1 つの修正。複数の問題を一度に修正しない
4. **后方互換性:** 既存の機能を壊さない

### 修正パターン

```python
# 悪い例: 症状のみの処理
try:
    result = broken_function()
except:  # すべてを無視
    result = default_value

# 良い例: 根本原因の修正
def broken_function():
    if input_data is None:  # 実際の原因: None チェックの欠落
        return default_value
    return process(input_data)
```

### 一般的な修正カテゴリ

| カテゴリ | 典型的な修正 |
|----------|--------------|
| None/Null | ガード節: `if x is None: return default` |
| インデックスエラー | 境界チェック: `if i < len(lst)` |
| 型エラー | 明示的な変換: `str(x)`, `int(x)` |
| インポートエラー | パスの修正、パッケージのインストール |
| エンコーディング | UTF-8 を明示的に指定: `encoding='utf-8'` |
| 競合状態 | ロック/ミューテックス、または順序の変更 |
| 状態バグ | 初期化の確認、リセットの追加 |

---

## フェーズ 5: 検証 (5分)

### チェックリスト

- [ ] **バグが修正された:** 元の問題が発生しなくなった
- [ ] **MRE がパスする:** 孤立テストが最後まで実行される
- [ ] **回帰なし:** 既存のテストが引き続きパスする
- [ ] **エッジケース:** 空の入力、None、大容量データがテストされている
- [ ] **プロジェクトツール:** プロジェクトのツールディレクトリで関連するテスト/検証ツールを確認

### テストコマンド

```bash
# ユニットテスト
python -m pytest tests/ -v

# 影響を受けるテストのみ
python -m pytest tests/test_module.py -v -k "test_name"

# 型チェック
python -m mypy file.py

# リント
python -m flake8 file.py
```

---

## フェーズ 6: ドキュメント化 (2分)

### バグレポートテンプレート

```markdown
## Bug Report: [簡潔なタイトル]

**Date:** YYYY-MM-DD
**Severity:** critical / high / medium / low
**Component:** [モジュール/ファイル]

### Symptom
[ユーザーが見る現象 / エラーメッセージ]

### Root Cause
[技術的な根本原因]

### Fix
[変更内容 + 理由]

### Affected Files
- `file1.py` — [変更点]
- `file2.py` — [変更点]

### Prevention
[今後、この種のバグを防ぐにはどうすればよいか？]
```

### コミットメッセージフォーマット

```
fix: [修正の簡潔な説明]

Cause: [一言で言えば根本原因]
Fix: [変更された内容]
Test: [検証方法]
```

---

## PyQt6 / GUI デバッグ — よくある落とし穴

> このセクションは PyQt6/PySide6 を使用したデスクトップ GUI プロジェクトに関連します。

### PyQt6 の 5 大トラップ

| トラップ | 問題 | 解決策 |
|----------|------|--------|
| **Signal-Slot 切断** | シグナルが接続されているがハンドラーが実行されない | ハンドラー内で `print`、シグネチャの確認 |
| **スレッドセーフ** | ワーカースレッドからの GUI 更新 | `QMetaObject.invokeMethod` またはシグナルを使用 |
| **レイアウトの崩れ** | ウィジェットが非表示/配置ミス | `widget.show()`、レイアウト階層の確認 |
| **イベントループのブロック** | GUI がフリーズする | 長時間の操作を QThread に移動 |
| **ガベージコレクション** | ウィジェットが突然消失する | 参照を `self.widget` として保持 |

### PyQt6 デバッグヘルパー

```python
# ウィジェット階層のダンプ
def dump_widget_tree(widget, indent=0):
    print(" " * indent + f"{widget.__class__.__name__}: {widget.objectName()}")
    for child in widget.findChildren(QWidget):
        if child.parent() == widget:
            dump_widget_tree(child, indent + 2)

# シグナルのデバッグ
from PyQt6.QtCore import QObject
original_connect = QObject.connect
def debug_connect(self, *args, **kwargs):
    print(f"CONNECT: {self.__class__.__name__} -> {args}")
    return original_connect(self, *args, **kwargs)
```

---

## クイックリファレンス

```
バグ発見？
     |
     v
[フェーズ 1: クイックチェック]  ── 明白？ -> 修正
     |
     v
[フェーズ 2: 診断]  ────────────── 原因明確？ -> フェーズ 4
     |
     v
[フェーズ 3: 孤立テスト]  ──────── 再現可能？ -> フェーズ 4
     |                                  |
     |                             再現不可？
     |                                  |
     |                             ログを追加し、
     |                             再発を待つ
     v
[フェーズ 4: 修正]  ─────────────── 最小限 + 理解済み
     |
     v
[フェーズ 5: 検証]  ────────────── テスト成功？ -> フェーズ 6
     |                                  |
     |                             テスト失敗？ -> フェーズ 4 へ戻る
     v
[フェーズ 6: ドキュメント化]  ──── バグレポート + コミット
```

### 20分ルール

20分経過しても行き詰まっている場合：

1. **アプローチの変更** — 別のデバッグ手法を試す
2. **ラバーダック・デバッグ** — 問題を声に出して説明する（または書き出す）
3. **休憩を取る** — 5分間離れ、新鮮な視点で戻る
4. **助けを求める** — 同僚、Stack Overflow、ドキュメントに相談
5. **リセット** — `git stash` で完全に出直す
