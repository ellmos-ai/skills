---
name: gesundheit
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-11-09
description: "個人の健康メモ、症状の時系列記録の整理、または医師の診察前の質問準備を行う場合に使用する（例：'医師への相談を準備'、'症状記録を整理'、'健康に関する質問をまとめる'、/gesundheit）。提供された健康データを客観的に整理し、医療従事者に尋ねるべき要点を準備する。医学的診断の確定、治療方針の指示、緊急対応には使用しない。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [health, organization, questions, safety]
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


<img src="banner.png" width="100%" alt="gesundheit banner">

# 健康情報の整理

## 目的

症状、経過、薬、未解決の質問を事実に基づいて要約します。

**結果:** 時系列、構造化した観察、安全上の注意、医療専門家への質問。

## ワークフロー

1. 目的、状況、希望する出力形式を確認する。
2. 現在の依頼で提供された情報だけを使用する。
3. 構造化され追跡可能な結果を作成する。
4. 仮定を明示し、外部変更の前に確認を得る。

## 例

**入力:** この症状メモを受診用の短い時系列にしてください。

**結果:** 時系列、構造化した観察、安全上の注意、医療専門家への質問。

## 公開コアと非公開拡張

この公開 Skill には移植可能な方法だけを含めます。アプリ固有のアダプター、アカウント、ローカルパス、データベース、個人設定は、非公開の追加プロファイルまたは非公開 fork に置き、このリポジトリへコミットしてはいけません。

非公開プロファイルがない場合、現在の依頼で明示された情報だけを使用します。

## 制限とデータ保護

- データは既定では保存しません。
- 明示的な許可なしに、情報源、ファイル、インターフェースを開いたり変更したりしません。
- 診断や治療の代替ではありません。緊急の危険がある場合は地域の救急サービスを利用してください。

## 変更履歴

### 2.0.0 (2026-07-30)

- 利用者に依存しない公開コアへ変更し、非公開連携と個人プロファイルを削除。
