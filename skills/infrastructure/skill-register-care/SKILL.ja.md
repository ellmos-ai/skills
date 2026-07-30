---
name: skill-register-care
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-07-30
description: >
  3 つの部分からなるスキルレジストリ（code-skill-index カタログ、スキルインデックス、SKILL-MAP
  ファミリー／ルーティングマップ）を一貫した状態に維持する保守スキル。実際のスキルインベントリと
  ドキュメント化されたレジストリの間のずれチェック（Drift-Check）に使用します：欠落または過剰なエントリの報告、
  カウントの修正、更新日付の設定。「スキルレジストリの保守」、「インデックスの更新」、「レジストリドリフトのチェック」、
  「マップに不足しているスキル」などの指示でもトリガーされます。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, register, index, drift, pflege, meta]
language: ja
status: active

dependencies:
  tools: []
  services: []
  protocols: [skill-explorer, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-register-care/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="skill-register-care banner">
# スキルレジストリケア (Skill-Register-Care)

## 目的

**レジストリ**をドリフトのない状態に維持します。レジストリは相互に関連する 3 つの成果物で構成されています —— 第 4 のレジストリを作成せず、常にこの 3 つを拡張します：

- `~/.claude/skills/code-skill-index/references/catalog-*.md`（カテゴリカタログ）
- スキルインデックス（マスターリスト）
- `<USER_HOME>\OneDrive\.USR\SKILL-MAP.md`（ファミリー／ルーティングマップ）

## ドリフトチェック手順

1. **現状の取得：**
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
   `source=user` のスキルのみがレジストリ対象です（プラグイン／外部スキルは除外）。
2. **目標状態の読み込み：** 3 つのレジストリ成果物を読み込みます。
3. **差分の抽出：**
   - **欠落**（インベントリに存在し、レジストリに未存在） → 追加。
   - **孤立**（レジストリに存在し、インベントリに存在しない） → マーク／削除。
   - **カウントの不一致**（例：「18 スキル」の数値が合わない） → 数値を修正。
4. **追加登録：** 新しいスキルごとに対応する `catalog-<kategorie>.md` に 1 行、スキルインデックスに 1 行（+ ヘッダー日付）を追加し、新規／変更されたファミリーの場合は `SKILL-MAP.md` にセクションを追加します。
5. **更新日付の設定：** 変更されたすべてのファイルの更新日付を現在の日付に設定します。

## 補助スニペット（不足しているユーザー主導スキルの列挙）

```bash
PYTHONIOENCODING=utf-8 python -c "
import json
inv=json.load(open('<USER_HOME>/.skill-inventory.json',encoding='utf-8'))
print('\n'.join(s['dir'] for s in inv['skills'] if s['source']=='user'))
"
```
出力結果をレジストリ成果物と照合します（手動または grep 経由）。

## 厳格なルール

- **第 4 のレジストリを作成しない** —— 常にこの 3 つのみを拡張します。
- ユーザーが作成したスキルのみがレジストリに属します。サードパーティ製は外部パスに従います。
- 日付を推測しない —— 現在の実際の日付を設定します。

## 変更履歴

### 0.1.0 (2026-06-17)
- 初版。監査モード (P2) により生成。契機：2026-06-17 の監査時に SKILL-MAP に約 10 個のユーザー固有スキルが不足していたため（swarm-operations, model-strategy, agents-bridge, mcp-config-sync, system-onboarding, update-cli-docs, migrate-rename, plugin-system + セラピーおよびゲーム開発ファミリー）。
