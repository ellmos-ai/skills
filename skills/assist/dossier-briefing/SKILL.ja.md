---
name: dossier-briefing
version: 1.0.0
category: assist
description: トピックや人物の構造化されたリサーチブリーフィングをMarkdownスキャフォールド（標準出力またはファイル）として生成します。永続ストレージはありません。
tags: [briefing, dossier, recherche, markdown, research]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['datetime', 'pathlib', 'textwrap']}
runtime: python3
entry_point: dossier_briefing_core.py
provenance: {'origin': 'BACH persoenlicher-assistent', 'origin_path': 'system/agents/persoenlicher-assistent/tools/dossier_generator.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': 'Alle Origin-DB-Abhaengigkeiten entfernt (create_dossier, update_dossier, DOSSIERS_DIR, DossierGenerator-Klasse mit DB-Methoden). Nur _create_markdown-Logik portiert und verallgemeinert (Person→Subjekt). Kein Store. One-Shot-Scaffold-Generator. Headless, nur Stdlib.\n'}
language: ja
---

<img src="banner.png" width="100%" alt="dossier-briefing banner">

> **日本語** — `dossier-briefing` の公式日本語版。


# Dossier-Briefing（日本語）

**トピックまたは人物の構造化リサーチブリーフィング**

---

## 概要と目的

あらゆる対象（人物、企業、イベント、概念）向けに、空の構造化されたMarkdownブリーフィングを生成します。
このスキャフォールドは、`research-agent` や `web-reading` を使用したその後のリサーチの出発点となります。

---

## トリガー

| フレーズ | アクション |
|---|---|
| 「マリー・キュリーに関するブリーフィングを作成」/ "Create a briefing on Marie Curie" | スキャフォールド: 人物、type=person |
| 「OpenAIに関するドシエ」/ "Dossier on OpenAI" | スキャフォールド: 組織/企業、type=organization |
| 「量子コンピューティングに関するブリーフィング」/ "Briefing on quantum computing" | スキャフォールド: トピック、type=topic |
| 「COP30のリサーチブリーフィングを準備」/ "Prepare a research briefing on COP30" | スキャフォールド: イベント、type=event |

---

## ワークフローと手順

1. **対象の特定:** ユーザーの入力からブリーフィングの名前/タイトルを抽出します。
2. **タイプの検知:** person, organization, topic, event (または unspecified)。
3. **スキャフォールドの生成:** 関連するすべてのセクションを含むMarkdownを作成します。
4. **出力:** 標準出力（stdout）、またはオプションでファイルに書き出します（`-o file.md`）。
5. **リサーチの開始:** 不足しているセクションを埋めるため、スキャフォールドを `research-agent` または `web-reading` に渡します。

---

## CLI

```bash
# Briefing to stdout (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Marie Curie" --typ person

# Write to file (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "OpenAI" --typ organization -o briefing_openai.md

# Topic briefing (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Quantum computing" --typ topic

# Event (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "COP30" --typ event

# Without type (generic) (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "My topic"

# Help (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py --help
```

---

## ブリーフィングのタイプとセクション

| タイプ | セクション |
|---|---|
| `person` | 基本データ、経歴/背景、実績・貢献、情報源、メモ |
| `organization` | プロフィール、沿革、製品/サービス、キーパーソン、情報源、メモ |
| `topic` | 概要、背景/文脈、最新動向、主要な情報源、未解決の課題、メモ |
| `event` | 主要な事実、参加者、背景/タイムライン、重要性、情報源、メモ |
| `unspecified` | 概要、背景、詳細、情報源、メモ |

---

## ストレージ

永続ストレージはありません。スキャフォールドは出力（標準出力またはファイル）されるのみで、
データベースには保存されません。

---

## 基本姿勢

- スキャフォールドは空であり、リサーチによって埋める必要があることを常に強調してください。
- コンテンツを創作したりハルシネーション（虚偽情報の生成）を起こしたりせず、構造のみを提供してください。
- タイプが不明確な場合は確認するか、`unspecified` を使用してください。

---

## プライバシー

ネットワークアクセスなし。ストレージなし。完全にローカル処理。

---

## 関連リソース

- `research-agent` — リサーチ結果でブリーフィングのスキャフォールドを埋めます
- `web-reading` — Webページを読み込み、ブリーフィング用のコンテンツを抽出します

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|---|---|---|
| 1.0.0 | 2026-06-22 | BACH dossier_generator.py v1.0.0 より作成。ストレージ削除および汎用化 |