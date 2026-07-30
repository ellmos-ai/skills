---
name: plugin-system
version: 1.0.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: Python アプリケーション向けの汎用プラグインシステム。自動検出、検証、耐障害性を備える。依存関係ゼロ（Python 標準ライブラリのみ）。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [plugin, framework, extensibility, cli, architecture]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/plugins', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **日本語** — `plugin-system` の公式日本語版。


# Plugin System (日本語)

Python CLI アプリケーション向けの耐障害性の高いプラグインシステム。
欠陥のあるプラグインがあっても、アプリケーションの残りの部分が停止することはありません。

## 主な機能

- **自動検出（Auto-Discovery）:** ディレクトリ内のプラグインを自動的に検索
- **検証（Validation）:** 各プラグインクラスの `name`、`version`、`execute()` をチェック
- **耐障害性（Fault Tolerance）:** 不具合のあるプラグインはログに記録されますが、読み込まれません
- **依存関係ゼロ（Zero Dependencies）:** Python 標準ライブラリのみを使用

## 構成ファイル

```
scripts/
  plugin_system.py       コア：PluginBase (ABC) + PluginManager
  cli_demo.py            argparse を使用したデモ CLI
  test_plugin_system.py  16 以上の単体テスト
examples/
  hello.py               Hello World プラグイン
  calculator.py          電卓プラグイン
  systeminfo.py          システム情報プラグイン
```

## クイックスタート

### 1. プラグインの作成

```python
from plugin_system import PluginBase

class MyPlugin(PluginBase):
    name = "MyPlugin"
    version = "1.0.0"

    def execute(self, *args, **kwargs):
        return {"status": "ok", "message": "Hello!"}
```

### 2. PluginManager の使用

```python
from plugin_system import PluginManager

manager = PluginManager(plugins_dir="./my_plugins")
plugins = manager.discover_plugins()

# すべてのプラグインを一覧表示
manager.list_plugins()

# プラグインの実行
success, result = manager.execute_plugin("MyPlugin", param="value")
if success:
    print(result)
```

### 3. アプリケーションへの統合

```python
class MyApp:
    def __init__(self):
        self.plugins = PluginManager("./plugins")
        self.plugins.discover_plugins()

    def run_command(self, command, **params):
        success, result = self.plugins.execute_plugin(command, **params)
        return result if success else None
```

## プラグインインターフェース

すべてのプラグインは以下を満たす必要があります：

| 要求事項 | 詳細 |
|-------------|---------|
| `PluginBase` の継承 | `from plugin_system import PluginBase` |
| `name` の設定 | クラス属性、空不可 |
| `version` の設定 | クラス属性、セマンティックバージョニング |
| `execute()` の実装 | 任意の `*args, **kwargs` を受け取る |

## 耐障害性

| エラー種別 | 挙動 |
|-----------|----------|
| プラグイン内の `SyntaxError` | プラグインはスキップされ、残りが読み込まれます |
| 属性の欠落 | プラグインは `is_valid=False` とマークされます |
| `execute()` 内の例外 | `(False, error_message)` を返します |
| ディレクトリ内にプラグインなし | クラッシュせず、空のリストを返します |

## 変更履歴

### 1.0.0 (2026-03-12)
- MODULAR_AGENTS/plugins からスキルライブラリへの移行
- PluginBase ABC + PluginManager
- 3つのサンプルプラグイン（Hello, Calculator, SystemInfo）
- 16以上の単体テスト
- argparse を使用した CLI デモ