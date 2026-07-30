---
name: therapie-umbrella
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: >
  「療法／カウンセリング」ファミリーのためのメタ／アンブレラスキル。すべての療法スキル
  （安定化、手法の概要、対話技術＋未登録の専門的療法）を把握し、適切なスキルへルーティングします。
  どの療法／カウンセリングスキルが適しているか不明な場合、利用可能な手法の概要が必要な場合、
  またはカウンセリング／危機状況をまず分類する必要がある場合にこのスキルを使用してください。
  「どの治療法が合うか」「相談を構造化する」「危機―どう対応すべきか」「治療方針の選択」などのプロンプトでも起動します。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: therapy
tags: [therapie, beratung, umbrella, meta, routing]
language: ja
status: active

dependencies:
  tools: []
  services: []
  protocols: [counseling-basics, guideline-therapies-overview, stabilization-techniques, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/therapie-umbrella/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="therapie-umbrella banner">

# 療法／カウンセリング — アンブレラ

## 目的

「療法／カウンセリング」ファミリーのエントリーポイントです。全体的なルーティングをまとめ、専門的なケースでは適切なスキルへ誘導します。3つのアクティブなエントリーポイントスキルが前面に配置されており、その背景には `code-skill-index`（カタログ `catalog-therapy.md`）経由でアクセス可能な未登録の専門療法のリストが存在します。

## メンバーとルーティング

| スキル | 用途 | 他のスキルの代わりにこれを使う場合 |
|--------|------|-----------------------------------|
| `/stabilization-techniques` | 危機介入、グラウンディング、安心できる場所（Safe Place）、PMR、パニック、耐性の窓（Window of Tolerance） | 急性ストレス／危機時には**まず最初**に — 手法の前に安定化 |
| `/guideline-therapies-overview` | 標準ガイドライン療法の概要：CBT、ACT、スキーマ療法、暴露療法、システム療法、精神分析的心理療法 | 適切な**手法**を選択・説明したい場合 |
| `/counseling-basics` | 対話技術：アクティブリスニング、ミラーリング、バリデーション、MI/OARS、円環的質問 | 療法の手法ではなく、**対話の進め方（HOW）**に焦点を当てる場合 |
| (未登録の専門スキル) | 個別手法（ジェノグラム、暴露療法の詳細、ポジティブ心理学など） | 具体的な個別手法を深掘りして使用したい場合 → `code-skill-index` 経由 |

> ルーティングルール：急性危機 → `/stabilization-techniques` · 手法の選択／説明 →
> `/guideline-therapies-overview` · 対話技術 → `/counseling-basics` · 深い個別手法 →
> `code-skill-index` 経由の未登録専門スキル。

## 相性の良い組み合わせ

- `/stabilization-techniques`（最初に、急性期）→ `/guideline-therapies-overview`（その後に、中期的）：
  まず安全性／耐性の窓を確保し、その後に適した標準ガイドライン療法を選択する。
- `/counseling-basics` は**両方**に随行 — カウンセリングの姿勢（MI/OARS、バリデーション）が安定化および手法の適用の双方を支えます。

## 共通の規約

- 診断の代用としないこと。サイコエデュケーション（心理教育）およびリソース指向でアプローチする。
- 耐性の窓（Window of Tolerance）を指導軸とする：過覚醒時にはまず安定化を図り、直ちに直面化（直面療法）を行わない。
- 適用前に各スキルの最新ファイルを読み込むこと — このアンブレラスキル自体はコンテンツを複製しません。

## 変更履歴 (Changelog)

### 0.1.0 (2026-06-17)
- 初期バージョン。療法／カウンセリングファミリー向けに監査モード (1c1) により生成。
