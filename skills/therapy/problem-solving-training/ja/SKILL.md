---
name: problem-solving-training
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 6つのステップによる構造化問題解決：問題の定義、目標設定、ブレインストーミング、評価、実行、効果検証。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [problem-solving, decision, structured, six-steps, coping]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/therapie/problemloese_training.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="problem-solving-training banner">

> **日本語** — `problem-solving-training` の公式日本語版。


# 問題解決トレーニング (Problem-Solving Training)

> D'Zurilla と Goldfried による6つのステップに基づいた構造化問題解決：思考の空回りを防ぎ、体系的・解決指向で問題にアプローチする

参照：[ETHICS.md](../ETHICS.md)

---

## コンテキスト (Context)

問題解決トレーニング（Social Problem-Solving, SPS：社会的問題解決療法）は、認知行動療法におけるエビデンスに基づいた介入技法です。熟考の反芻（ルーミネーション）、回避、あるいは衝動的な行動に陥ることなく、体系的かつ解決指向で問題に取り組むことを支援します。

エビデンス：メタアナリシスにより、うつ病（d=0.83）、不安障害、ストレスに対する有意な効果が示されています（Malouff et al. 2007, Bell & D'Zurilla 2009）。

**注記：** 本スキルはサポートを目的とするものであり、専門的な心理療法の代用にはなりません。
**絶対に使用しないこと：** EMDR、持続暴露療法（PE）、ナラティブ暴露療法（NET）

---

## 1. 問題解決への構え（オリエンテーション）

具体的なステップに入る前に、心構え（オリエンテーション）が決定的に重要となります。

### 適切な心構え
- 「問題は生活の一部であり、解決可能である」
- 「一歩ずつ進めることができる」
- 「唯一の正解が存在することは稀である」
- 「行動しないことも選択の一つであり、通常は最善ではない」

### 不適切な心構え
- 「何をやっても意味がない」
- 「どうせ自分にはできない」
- 「解決策なんてない」
- 熟考なしの衝動的な行動
- 回避と先延ばし

**最初のステップ：** 自身の問題解決に対する姿勢・心構えを振り返る。

---

## 2. 6ステップモデル (The 6-Step Model)

### ステップ 1: 問題の定義 (Define the Problem)

**目標：** 問題を明確、具体的、かつ扱いやすい形で定式化する。

**ガイド質問：**
- 具体的に何が問題か？（解釈ではなく事実）
- 誰が関与しているか？
- いつ、どこで発生するか？
- なぜそれが自分にとって問題なのか？

**ワークシート：**

```
PROBLEM DEFINITION

Situation: [What is happening concretely?]
People involved: [Who is involved?]
Frequency: [How often? When?]
Impact: [What makes it a problem?]

Concrete problem statement:
[...]
```

**よくある誤り：**
- 問題が曖昧すぎる（「すべてが上手くいかない」）
- 複数の問題を混同している
- 問題の定義の中に解決策を混ぜてしまう

---

### ステップ 2: 目標の設定 (Set Goals)

**目標：** 問題解決後、どのような状態になっていたいか？

**SMART基準：**
- Specific（具体性）：具体的に何か？
- Measurable（測定可能性）：達成をどう判断するか？
- Attractive（魅力的）：なぜそれを望むのか？
- Realistic（現実的）：達成可能か？
- Time-bound（期限）：いつまでに？

**ワークシート：**

```
GOAL SETTING

My goal: [...]
How will I know I've achieved it? [...]
By when? [...]
Realistic (0-10)? [...]
Important to me (0-10)? [...]
```

---

### ステップ 3: 解決案の創出／ブレインストーミング (Generate Alternatives)

**目標：** 即座に評価せず、できるだけ多くの解決案を出す。

**ブレインストーミングのルール：**
1. 質より量 — 案が多いほど良い
2. 収集中の評価は厳禁
3. 独創的で型破りな発想も歓迎
4. 既存の案を組み合わせ・応用する

**ワークシート：**

```
BRAINSTORMING

Solution ideas (at least 5-8):
1. [...]
2. [...]
3. [...]
4. [...]
5. [...]
6. [...]
7. [...]
8. [...]
```

**ヒント質問：**
- 「この問題を持っていない人ならどうするか？」
- 「似たような状況で過去にどう対処したか？」
- 「友人にならどう助言するか？」
- 「最も大胆な解決策は何か？」
- 「最もシンプルな解決策は何か？」

---

### ステップ 4: 解決案の評価 (Evaluate Alternatives)

**目標：** 各解決案の長所・短所を体系的に検討する。

**評価基準：**
- 効果性：問題が解決するか？
- 実行可能性：自分に実行できるか？
- 所要時間：どれくらい時間がかかるか？
- 影響・結果：自分への影響？ 他者への影響？
- リスク：何がうまくいかない可能性があるか？

**ワークシート：**

```
EVALUATION MATRIX

| Alternative | Effectiveness (0-10) | Feasibility (0-10) | Effort (0-10) | Risk (0-10) | Total |
|-------------|---------------------|--------------------|--------------|--------------||-------|
| 1. [...]    |                     |                    |              |              |       |
| 2. [...]    |                     |                    |              |              |       |
| 3. [...]    |                     |                    |              |              |       |

Preferred solution: [...]
Reasoning: [...]
```

---

### ステップ 5: 実行 (Implement)

**目標：** 選択した解決策を具体的に計画し、実行する。

**行動計画：**

```
ACTION PLAN

Chosen solution: [...]

Concrete steps:
1. [What?] — [When?] — [Where?]
2. [What?] — [When?] — [Where?]
3. [What?] — [When?] — [Where?]

Possible obstacles: [...]
Plan B: [...]
Support I need: [...]
First step (today/tomorrow): [...]
```

---

### ステップ 6: 効果検証と振り返り (Evaluate)

**目標：** 結果を確認し、必要に応じて修正する。

**振り返りの質問：**
- 問題は解決したか？（完全解決 / 部分的解決 / 未解決）
- 結果に満足しているか？（0〜10）
- うまくいった点は何か？
- 次回変更すべき点は何か？
- 別の解決案で再挑戦する必要があるか？

**ワークシート：**

```
EVALUATION

Result: [Solved / Partially / Not solved]
Satisfaction (0-10): [...]
What worked: [...]
What didn't: [...]
Next step: [Conclude / New attempt / Different approach]
```

---

## 3. 問題解決におけるよくある課題と対策

| 課題・問題 | 対策 |
|---------|--------|
| 「何から始めればいいかわからない」 | ステップ1に戻り、問題をより小さく定義し直す |
| 「どの解決策も完璧ではない」 | 完璧主義を見直し、「十分良い（good enough）」を受け入れる |
| 「実行するのが怖い」 | 実行可能な最小の一歩を特定する |
| 「うまくいかない」 | 効果検証：具体的に何が機能していないか分析し、再挑戦する |
| 問題が大きすぎる | サブ問題に分割し、1つずつ対処する |
| 感情のブロッキング | 感情調節（深呼吸、漸進的筋弛緩法: PMR）を先に行い、その後に問題解決に取り組む |

---

## 倫理と限界 (Ethics and Boundaries)

**AIアシスタントができること：**
- 6つのステップを案内し、ワークシートの構造を提供する
- ブレインストーミングの質問を投げかける
- 解決案の評価をサポートする
- 進捗を記録する

**AIアシスタントがしてはならないこと：**
- 解決策を押し付けたり「唯一の正解」を指示すること
- 治療的意味合いでのパートナーシップや生き方に関するカウンセリングを行うこと
- 深刻な精神的苦痛における唯一の支援者となること
- 診断を行うこと

**緊急の危機状況では、必ず以下を案内すること：**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- よりそいホットライン (日本): 0120-279-338
- 緊急通報: 911 (US) / 112 (EU) / 119 (JP)

---

*BACH v3.8.0 より移植 | スタンドアロン版*
*出典：D'Zurilla & Goldfried (1971), Nezu et al. (2013), Malouff et al. (2007) — 専門的な心理療法ではありません*
