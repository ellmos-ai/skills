---
name: skill-family-care
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-07-30
description: >
  skill-explorer のフル監査を実行することなく、スキルファミリーを最新状態に維持する保守スキル。
  新しいスキルを正しいファミリーに割り当てる場合、ファミリー変更後にヘッダー指示ルーターを更新する場合、
  または不要になったルーターを削除する場合にこのスキルを使用します。「ファミリーの保守」、「新スキルのファミリー割り当て」、
  「ルーターの更新」、「ファミリーヘッダーの設定／削除」などの指示でもトリガーされます。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, familien, pflege, routing, meta]
language: ja
status: active

dependencies:
  tools: []
  services: []
  protocols: [skill-explorer, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-family-care/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="skill-family-care banner">
# スキルファミリーケア (Skill-Family-Care)

## 目的

`skill-explorer` の完全な監査サイクルを実行することなく、スキルの**ファミリー**を最新状態に維持します。インストーラー原則（モノリスではなく軽量なサブスキル）に従って独立化されています。`skill-explorer` のスクリプトを参照し、重複コピーは行いません。

## データソース（重複作成禁止）

- **ファミリーリスト：** `<USER_HOME>\OneDrive\.USR\SKILL-MAP.md`（正格なファミリー／ルーティングマップ）。
- **インベントリ（現状）：** `skill-explorer/scripts/inventory_skills.py`。
- **ルーターの設定／削除：** `skill-explorer/scripts/inject_family_header.py`。
- **設定（リンク済みファミリー）：** `~/.claude/skills/skill-explorer/config.json`。

## タスク

### A — 新しいスキルをファミリーに割り当てる
1. インベントリを再取得：
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
2. `SKILL-MAP.md` から適切なファミリーを選択（軸：フェーズ／幅／硬度／影響／原料）。
3. `config.json`（`families[<fam>].members`）および `SKILL-MAP.md` にメンバーとして登録。

### B — ファミリー変更後にヘッダールーターを更新
```bash
PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inject_family_header.py \
    --family <Familie> --skills s1,s2,s3 --router "<Wegweiser>" --inventory ~/.skill-inventory.json
```
- べき等：同一ファミリーの既存ブロックがある場合は置換されます。
- `editable`/`source=user` のスキルのみが変更対象となります（スクリプト内の安全ゲート）。

### C — 孤立したルーターの削除
同一スクリプトを `--remove` 付きで実行（`--router` は不要）。

## 厳格なルール

- **調査 ≠ 変更（Survey ≠ Mutation）：** ユーザー固有のスキルのみがヘッダーを受け取ります。プラグインや外部スキルには絶対に触れないでください。
- 変更後は毎回 `config.json`（`families[*].linked`、`updated`）を更新してください。
- ファミリーマップの内容を個別スキルにコピーしないでください —— 案内ブロックのみを挿入します。

## 変更履歴

### 0.1.0 (2026-06-17)
- 初版。監査モード (P1) により生成。
