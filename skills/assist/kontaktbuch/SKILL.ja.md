---
name: kontaktbuch
version: 2.0.0
type: assist
author: ellmos contributors
created: 2026-07-30
updated: 2026-11-09
description: "プライバシーに配慮しながらアドレス帳を管理し、連絡先情報を更新し、重複エントリーを整理・統合する場合に使用する（例：'連絡先を保存'、'住所録を更新'、'重複した連絡先を整理'、/kontaktbuch）。外部への情報漏洩を防ぎながら、安全に連絡先データを構造化・名寄せする。ソーシャルメディアでの営業・広報活動（dev/community-outreach）には使用しない。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [contacts, organization, deduplication, privacy]
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


<img src="banner.png" width="100%" alt="kontaktbuch banner">

# 連絡先の整理

## 目的

個人のアドレス帳を同梱せず、依頼に必要な連絡先だけを構造化します。

**結果:** 正規化項目、重複候補、不足情報。

## ワークフロー

1. 目的、状況、希望する出力形式を確認する。
2. 現在の依頼で提供された情報だけを使用する。
3. 構造化され追跡可能な結果を作成する。
4. 仮定を明示し、外部変更の前に確認を得る。

## 例

**入力:** この匿名化された連絡先一覧の重複を確認してください。

**結果:** 正規化項目、重複候補、不足情報。

## 公開コアと非公開拡張

この公開 Skill には移植可能な方法だけを含めます。アプリ固有のアダプター、アカウント、ローカルパス、データベース、個人設定は、非公開の追加プロファイルまたは非公開 fork に置き、このリポジトリへコミットしてはいけません。

非公開プロファイルがない場合、現在の依頼で明示された情報だけを使用します。

## 制限とデータ保護

- データは既定では保存しません。
- 明示的な許可なしに、情報源、ファイル、インターフェースを開いたり変更したりしません。

## 変更履歴

### 2.0.0 (2026-07-30)

- 利用者に依存しない公開コアへ変更し、非公開連携と個人プロファイルを削除。
