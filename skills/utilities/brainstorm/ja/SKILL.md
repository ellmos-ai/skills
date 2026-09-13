---
name: brainstorm
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: アイデア発想のための体系的なクリエイティビティ手法：SCAMPER、6つの思考ハット、マインドマッピング、逆ブレインストーミング、TRIZ、ラピッドアイディエーション。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [brainstorm, creativity, ideation, scamper, six-hats, innovation]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/brainstorm.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="brainstorm banner">

> **日本語** — `brainstorm` の公式日本語版。


# Brainstorm (日本語)

> イノベーションのための体系的なクリエイティビティ — SCAMPER、6つの思考ハット、マインドマッピング、逆ブレインストーミング、TRIZ、ラピッドアイディエーション

---

## いつ使用するか？

- 新しいアイデアが必要なとき
- 行き詰まり／創造性のブロックがあるとき
- イノベーションが求められるとき
- 課題をクリエイティブに解決したいとき

**トリガーワード:** brainstorm, ideas, creative, innovative, ideation

---

## 手法

### 1. SCAMPER

**Substitute（代用）、Combine（結合）、Adapt（適応）、Modify（修正）、Put to other use（転用）、Eliminate（削減）、Reverse（逆相）**

既存の解決策を体系的に改善する：
- **S**ubstitute（代用）: 何を置き換えられるか？
- **C**ombine（結合）: 何と組み合わせられるか？
- **A**dapt（適応）: 何を応用・適応できるか？
- **M**odify（修正）: 何を変更・修正できるか？
- **P**ut to other use（転用）: 他にどのような用途に使えるか？
- **E**liminate（削減）: 何を削除・削減できるか？
- **R**everse（逆相）: 何を逆転・逆配置できるか？

---

### 2. 6つの思考ハット（エドワード・ド・ボノ）

6つの視点から体系的に思考を深める：

- **白のハット — 事実:** どのような情報があるか？何が不足しているか？
- **赤のハット — 感情:** 直感や感情はどう感じているか？
- **黒のハット — 批判:** 何が失敗し得るか？リスク、弱点
- **黄のハット — 楽観:** どのような機会・メリットがあるか？最善のケース
- **緑のハット — 創造:** 新しいアイデアはあるか？枠にとらわれない発想
- **青のハット — メタ（全体統括）:** プロセス管理、要約、次のステップ

**プロセス:** 問題の定義（青） -> 事実の確認（白） -> 感情の共有（赤） -> 批判・リスク評価（黒） -> メリットの抽出（黄） -> 新しいアイデア（緑） -> 統括・要約（青）

---

### 3. マインドマッピング (Mind Mapping)

思考を階層的に視覚化する：
1. 中央のテーマ
2. メインの枝（3〜7個）
3. 各カテゴリのサブ枝
4. 詳細とアイデアの追加
5. 関連性・接続の特定

---

### 4. 逆ブレインストーミング (Reverse Brainstorming)

問題を逆転させる: 「どうすれば状況をさらに悪化させられるか？」

1. 問題を逆転・反転させる
2. 悪いアイデアを収集する
3. 反転させる = 優れたアイデアになる

直接的なアイデア出しが行き詰まったときに特に効果的です。

---

### 5. TRIZ（発明的課題解決理論）

ソフトウェアに役立つ10の原理:
1. **分割 (Segmentation):** モノリスをモジュールに分割する
2. **抽出 (Extraction):** 邪魔な属性や要素を分離・隔離する
3. **局所的品質 (Local Quality):** コンポーネントごとに異なる特性を持たせる
4. **併合・結合 (Merging):** 類似した機能を結合する
5. **汎用性 (Universality):** 1つの要素に複数の機能を持たせる
6. **入れ子構造 (Nesting):** コンポーネントの中にコンポーネントを配置する
7. **先回りアクション (Preliminary Action):** 事前に準備を行う
8. **フィードバック (Feedback):** 監視と適応
9. **セルフサービス (Self-Service):** システムが自己メンテナンスする
10. **非対称性 (Asymmetry):** 非対称なデザイン

---

### 6. ラピッドアイディエーション (Rapid Ideation)

量より質 — 20分で50以上のアイデアを出す。

**ルール:**
- アイデア出しの最中は批判禁止
- 奇抜な・突拍子もないアイデアも大歓迎
- 他人のアイデアを発展・ビルドアップさせる
- まずは「量」を最優先

**タイマーベース:**
- ラウンド1 (5分): オープンなアイデア出し
- ラウンド2 (5分): バリエーション・派生
- ラウンド3 (5分): アイデアの結合・組み合わせ
- ラウンド4 (5分): エクストリーム（極端な）アイデア

---

## ワークフローと手順

```
1. User request
2. Understand goal
3. Choose method(s)
4. Generate ideas (no criticism!)
5. Clustering
6. Feasibility/Impact matrix
7. Top 5-10 selection
8. Output + recommendation
```

---

## 変更履歴

### 1.0.0 (2026-03-15)
- BACH v3.8.0 から移植

---

*BACH v3.8.0 から移植 | スタンドアロン版*
