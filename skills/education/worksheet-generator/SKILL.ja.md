---
name: worksheet-generator
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-07-23
updated: 2026-07-23
description: >
  支援目標・対象年齢・難易度に応じた教材・ワークシートの自動構造化生成。
standalone: true
anthropic_compatible: true
category: education
tags: [worksheets, icf, education, therapy-support, wrapper]
aliases: [worksheet-generator, worksheet-generator-ja]
language: ja
status: active
---

<img src="banner.png" width="100%" alt="worksheet-generator banner">

> **Japanese** — 公式日本語ドキュメント。

# ワークシート・教材生成スキル (日本語版)

本スキルは、教育・療法支援のための学習プリントおよび演習課題の構造化生成を提供します。

## 1. 概要と目的

- **適応的教材作成:** 支援目標に応じた段階的演習問題の自動構成。
- **ICFコード連携:** 支援領域コードに基づく課題設計。
- **多角的出力フォーマット:** Markdown、HTML、DOCX形式での出力。

## 2. 実行ワークフローと手順

1. **支援目標の入力:** 匿名化された指導目標および対象年齢の設定。
2. **難易度調整:** 学習者の理解度に応じたタスクレベルの設定。
3. **下案生成:** ワークシート構成案および設問の生成。
4. **専門的確認:** 使用前の専門職による適正確認と最終調整。

## 3. 厳守すべき境界条件とルール

- **個人情報の除外:** 生徒・児童の氏名や個人識別情報を入力しない。
- **事前確認の義務化:** 生成物は原案であり、必ず指導者が確認後に使用する。
- **教育支援用途の限定:** 治療プログラムではなく指導補助ツールとして運用する。

## 4. 必須出力結果と成果物

- 構造化された学習ワークシート（Markdown / HTML / DOCX）。
- 指導者用解答・解説シート。
