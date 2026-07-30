---
name: haushalt-manager
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: >
  特定アプリに依存せず、家事、習慣、担当を計画します。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [household, routines, tasks, planning]
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

<img src="banner.png" width="100%" alt="haushalt-manager banner">

# 家事プランナー

## 目的

定期的な家事と単発の家事を現実的に配分します。

**結果:** 作業量、優先順位、担当、余裕を含む週間計画。

## ワークフロー

1. 目的、状況、希望する出力形式を確認する。
2. 現在の依頼で提供された情報だけを使用する。
3. 構造化され追跡可能な結果を作成する。
4. 仮定を明示し、外部変更の前に確認を得る。

## 例

**入力:** これらの家事からバランスのよい週間計画を作成してください。

**結果:** 作業量、優先順位、担当、余裕を含む週間計画。

## 公開コアと非公開拡張

この公開 Skill には移植可能な方法だけを含めます。アプリ固有のアダプター、アカウント、ローカルパス、データベース、個人設定は、非公開の追加プロファイルまたは非公開 fork に置き、このリポジトリへコミットしてはいけません。

非公開プロファイルがない場合、現在の依頼で明示された情報だけを使用します。

## 制限とデータ保護

- データは既定では保存しません。
- 明示的な許可なしに、情報源、ファイル、インターフェースを開いたり変更したりしません。

## 変更履歴

### 2.0.0 (2026-07-30)

- 利用者に依存しない公開コアへ変更し、非公開連携と個人プロファイルを削除。
