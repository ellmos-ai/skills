---
name: rpg
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  システムに依存せず、冒険、場面、登場人物、キャンペーン整理を支援します。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [rpg, tabletop, campaign, storytelling]
language: ja
status: stable
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: public-neutral
  origin_license: MIT
  notes: Public core only; adapters and private profiles are excluded.
---

<img src="banner.png" width="100%" alt="rpg banner">

# テーブルトークRPG支援

## 目的

一貫性があり調整可能な案でゲームマスターと参加者を支援します。

**結果:** 場面案、NPCの動機、対立、手掛かり、選択肢。

## ワークフロー

1. 目的、状況、希望する出力形式を確認する。
2. 現在の依頼で提供された情報だけを使用する。
3. 構造化され追跡可能な結果を作成する。
4. 仮定を明示し、外部変更の前に確認を得る。

## 例

**入力:** 手掛かり2つと問題1つを含む港の短い場面を作成してください。

**結果:** 場面案、NPCの動機、対立、手掛かり、選択肢。

## 公開コアと非公開拡張

この公開 Skill には移植可能な方法だけを含めます。アプリ固有のアダプター、アカウント、ローカルパス、データベース、個人設定は、非公開の追加プロファイルまたは非公開 fork に置き、このリポジトリへコミットしてはいけません。

非公開プロファイルがない場合、現在の依頼で明示された情報だけを使用します。

## 制限とデータ保護

- データは既定では保存しません。
- 明示的な許可なしに、情報源、ファイル、インターフェースを開いたり変更したりしません。

## 変更履歴

### 2.0.0 (2026-07-30)

- 利用者に依存しない公開コアへ変更し、非公開連携と個人プロファイルを削除。
