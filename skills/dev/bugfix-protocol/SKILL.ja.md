---
name: bugfix-protocol
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 体系的な6段階のデバッグプロトコル。クイックチェック、孤立テスト、20分ルール、バグレポートテンプレートを備えたバグへの構造化アプローチ。
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

<img src="banner.png" width="100%" alt="bugfix-protocol banner">
> **日本語** — `bugfix-protocol` の公式日本語版。

# Bugfix Protocol: 体系的6段階デバッグプロトコル (日本語)

症状分析から検証に至るバグへの構造的アプローチ。
あてのない試行錯誤を防ぎ、持続可能な修正を実現します。

---

## 概要と目的

| フェーズ | 名前 | 目標 | 最大時間 |
|----------|------|------|----------|
| 1 | クイックチェック | 明白な原因の排除 | 2分 |
| 2 | 診断 | 根本原因の特定 | 10分 |
| 3 | 孤立テスト | バグの再現性の確保 | 5分 |
| 4 | 修正 (Fix) | 最小限の修正 | 10分 |
| 5 | 検証 | 修正の検証と副作用のチェック | 5分 |
| 6 | ドキュメント化 | ナレッジの保存 | 2分 |

**20分ルール:** 20分経っても進展がない場合は、アプローチを変更するか助けを求めてください。

---

## フェーズ 1: クイックチェック (2分)

深く調査する前に — 最も一般的な原因を確認します：

### チェックリスト

- [ ] **文法エラー？** エラーメッセージを注意深く読み、該当行を確認
- [ ] **インポートエラー？** モジュールはインストールされているか？正しい名前か？循環インポートか？
- [ ] **タイポ（一字違い）？** 変数名/関数名は正しいか？
- [ ] **型違い？** int のはずが string になっていないか？オブジェクト期待値に None が入っていないか？
- [ ] **古いキャッシュ？** `__pycache__` を削除して再起動
- [ ] **環境の違い？** 正しい venv が有効か？正しい Python バージョンか？
- [ ] **文字コード (Encoding)？** UTF-8 vs. cp1252 (Windows の伝統的エンコーディング)

### クイックアクション

```bash
# キャッシュのクリア (日本語)
find . -name "__pycache__" -type d -exec rm -rf {} + 2>&1
find . -name "*.pyc" -delete 2>&1

# インポートの確認 (日本語)
python -c "import modulename"

# 文法チェック (日本語)
python -m py_compile file.py
```

---

## フェーズ 2: 診断 (10分)

### 戦略：外側から内側へ (Outside-In)

1. **エラーメッセージの分析** — トレースバックを一番下から上に向かって読む
2. **最近の変更点の確認** — `git diff`, `git log --oneline -10`
3. **診断ツールの活用** — プロジェクト固有の診断ツールを使用

### 診断ツール（例）

プロジェクトによっては、専用の診断スクリプトが役立ちます：

| ツール | 目的 |
|--------|------|
| `import_diagnose.py` | インポート問題の分析 |
| `method_analyzer.py` | メソッドシグネチャの確認 |
| `env_checker.py` | 環境変数/パスの検証 |

> **注:** プロジェクト固有の診断ツールを作成するか、既存のものを使用してください。
> 重要なのは特定のツールではなく、体系的なアプローチです。

### デバッグ手法

```python
# 1. Print デバッグ（迅速かつ効果的） (日本語)
print(f"DEBUG: variable={variable!r}, type={type(variable)}")

# 2. ブレークポイント（対話型） (日本語)
breakpoint()  # Python 3.7+

# 3. 拡張トレースバック (日本語)
import traceback
traceback.print_exc()

# 4. print の代わりに Logging を使用 (日本語)
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
# test_bug.py — 最小再現テスト (日本語)
"""
Bug: [短い説明]
Expected: [期待される挙動]
Actual: [実際の挙動]
"""

# 最小限のセットアップ (日本語)
# ... 必要最小限のみ (日本語)

# バグトリガー (日本語)
# ... バグを引き起こす正確なコード (日本語)

# 期待される結果 (日本語)
# assert result == expected, f"Got {result}" (日本語)
```

### 孤立化戦略

1. **新しいファイル:** 別のファイルでバグを再現する
2. **依存関係の削除:** バグが消えるまで1つずつ削除する
3. **二分探索:** コードブロックを半分にし、どちらにバグが含まれているか確認する
4. **Git bisect:** `git bisect start`, `git bisect bad`, `git bisect good <commit>`

---

## フェーズ 4: 修正 / Fix (10分)

### 原則

1. **最小限:** 変更は可能な限り少なく
2. **理解:** 暗闇で修正しない — なぜ壊れているのかを理解する
3. **単一の変更:** 1コミットにつき1つの修正。複数の問題を一度に修正しない
4. **下位互換性:** 既存の機能を壊さない

### 修正パターン

```python
# BAD: 症状だけを治療する (日本語)
try:
    result = broken_function()
except:  # すべてを握りつぶす
    result = default_value

# GOOD: 根本原因を修正する (日本語)
def broken_function():
    if input_data is None:  # 実際の原因: None チェックの欠落
        return default_value
    return process(input_data)
```

### よくある修正カテゴリ

| カテゴリ | 典型的な修正 |
|----------|--------------|
| None/Null | ガード句: `if x is None: return default` |
| インデックスエラー | 境界チェック: `if i < len(lst)` |
| 型エラー | 明示的変換: `str(x)`, `int(x)` |
| インポートエラー | パスの修正、パッケージのインストール |
| エンコーディング | UTF-8 を明示的に指定: `encoding='utf-8'` |
| レースコンディション | ロック/ミューテックス、または順序の変更 |
| ステートバグ | 初期化の確認、リセットの追加 |

---

## フェーズ 5: 検証 (5分)

### チェックリスト

- [ ] **バグが修正された:** 元の問題が発生しなくなった
- [ ] **MRE がパスする:** 孤立テストが最後まで実行される
- [ ] **デグレード（回帰）がない:** 既存のテストが引き続きパスする
- [ ] **境界値ケース:** 空の入力、None、大容量データがテストされている
- [ ] **プロジェクトツール:** プロジェクトのツールディレクトリで関連するテスト/検証ツールを確認

### テストコマンド

```bash
# ユニットテスト (日本語)
python -m pytest tests/ -v

# 影響を受けるテストのみ (日本語)
python -m pytest tests/test_module.py -v -k "test_name"

# 型チェック (日本語)
python -m mypy file.py

# リント (日本語)
python -m flake8 file.py
```

---

## フェーズ 6: ドキュメント化 (2分)

### バグレポートテンプレート

```markdown
## バグレポート: [短いタイトル]

**日付:** YYYY-MM-DD
**重要度:** 緊急 / 高 / 中 / 低
**コンポーネント:** [モジュール/ファイル]

### 症状
[ユーザーに見える挙動 / エラーメッセージ]

### 根本原因
[技術的な根本原因]

### 修正 (Fix)
[変更内容 + 理由]

### 影響を受けるファイル
- `file1.py` — [変更点]
- `file2.py` — [変更点]

### 再発防止策
[今後このタイプのバグをどう防ぐか？]
```

### コミットメッセージフォーマット

```
fix: [修正の短い説明]

Cause: [一言で言えば根本原因]
Fix: [変更内容]
Test: [検証方法]
```

---

## PyQt6 / GUI デバッグ — よくある落とし穴

> このセクションは PyQt6/PySide6 を使用したデスクトップ GUI プロジェクトに関連します。

### PyQt6 5大トラップ

| トラップ | 問題 | 解決策 |
|----------|------|--------|
| **シグナル・スロットの切断** | シグナルは接続されているがハンドラが実行されない | ハンドラ内で `print`、シグネチャの確認 |
| **スレッドセーフ** | ワーカースレッドからの GUI 更新 | `QMetaObject.invokeMethod` またはシグナルを使用 |
| **レイアウトの崩れ** | ウィジェットが非表示/配置ミス | `widget.show()`、レイアウト階層の確認 |
| **イベントループのフリーズ** | GUI がフリーズする | 重い処理を QThread に移動 |
| **ガベージコレクション** | ウィジェットが突然消える | 参照を `self.widget` として保持 |

### PyQt6 デバッグヘルパー

```python
# ウィジェット階層のツリー表示 (日本語)
def dump_widget_tree(widget, indent=0):
    print(" " * indent + f"{widget.__class__.__name__}: {widget.objectName()}")
    for child in widget.findChildren(QWidget):
        if child.parent() == widget:
            dump_widget_tree(child, indent + 2)

# シグナルデバッグ (日本語)
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
[フェーズ 1: クイックチェック] ───── 明白か？ -> 修正 (FIX)
     |
     v
[フェーズ 2: 診断] ────────────────── 原因明確か？ -> フェーズ 4
     |
     v
[フェーズ 3: 孤立テスト] ──────────── 再現可能か？ -> フェーズ 4
     |                                      |
     |                                再現不可か？
     |                                      |
     |                                ログを追加し、
     |                                再発を待つ
     v
[フェーズ 4: 修正] ────────────────── 最小限かつ理解済み
     |
     v
[フェーズ 5: 検証] ────────────────── テスト成功（グリーン）か？ -> フェーズ 6
     |                                      |
     |                                テスト失敗（レッド）か？ -> フェーズ 4 へ戻る
     v
[フェーズ 6: ドキュメント化] ──────── バグレポート + コミット
```

### 20分ルール

20分経っても行き詰まっている場合：

1. **アプローチを変える** — 別のデバッグ手法を試す
2. **ラバーダック・デバッグ** — 声に出して問題を説明する（または書き出す）
3. **休憩を取る** — 5分間離れ、新鮮な視点で戻る
4. **助けを求める** — 同僚、Stack Overflow、ドキュメントに相談する
5. **リセット** — `git stash` で完全に最初からやり直す