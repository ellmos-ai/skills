---
name: cognitive-restructuring
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 認知行動療法：ABCモデル、自動思考、認知の歪みの同定、思考記録表のつけ方。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [cbt, cognitive-restructuring, cognitive-distortions, thought-record, abc-model]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/therapie/kognitive_umstrukturierung.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **日本語** — `cognitive-restructuring` の公式日本語版。


# Cognitive Restructuring (日本語)

> CBT的中核技法：ABCモデル、非機能的思考の同定と修正

See: [ETHICS.md](../ETHICS.md)

---

## コンテキスト

認知の再構成（Cognitive Restructuring）は、認知行動療法（CBT）の中核的な技法です。ネガティブな自動思考を特定し、それに反証を試み、より適応的な代替思考へと置き換える支援を行います。

**注意：** 本機能はサポートを目的とするものであり、専門的な心理療法の代わりになるものではありません。
**絶対に使用不可：** EMDR（眼球運動による脱感作と再処理療法）、持続暴露療法（PE）、ナラティブ暴露療法（NET）

---

## 1. ABCモデル（エリス）

ABCモデルは、出来事、思考、感情がどのように関連しているかを説明するモデルです。

```
A (Activating Event)   ->  B (Beliefs / Thoughts)  ->  C (Consequences / Feelings/Behavior)
Trigger                     Evaluation / Belief           Emotional consequence
```

**重要：** 感情的結果（C）を引き起こすのは出来事（A）そのものではなく、その評価や認知（B）です！

**例：**
```
A: Boss criticizes a report in a meeting
B: "I am incompetent, everyone thinks so now"
C: Shame, withdrawal, avoiding future contributions
```

**目標：** Bを修正することでCに影響を与える。

---

## 2. ネガティブな自動思考（ANTs）の特定

**自動思考（ANTs）とは？**
- ストレス状況下で素早く自動的に生じる評価・思考
- 解釈に過ぎないにもかかわらず、しばしば事実として知覚される
- 誇張、一般化、破局化へと傾斜しやすい

**代表的な特徴：**
- 決定論的・絶対的思考：「いつも」「絶対に」「全員」「誰も〜ない」
- 破局化：「これは悲惨な結末になる」
- 読心（心の読みすぎ）：「彼らは〜と考えているに違いない」
- 過度の一般化：「自分には何をやってもうまくいかない」

**同定のための質問例：**
- 「その出来事が起きた時、心の中にどのような考えが浮かびましたか？」
- 「その状況を思い浮かべた時、どのような言葉が出てきますか？」
- 「どのようなことが起こるのではないかと恐れていますか？」

---

## 3. 認知の歪み（思考のエラー）

| 認知の歪み | 説明 | 例 |
|------------|-------------|---------|
| 白黒思考 | 全か無か思考（二元論的思考） | 「完璧にできないなら、自分は失敗者だ」 |
| 過度の一般化 | 1つの事例＝普遍的なパターンとみなす | 「自分は何をやってもいつも失敗する」 |
| メンタルフィルター | ネガティブな側面のみに着目する | フィードバックの中のたった1つの批判ばかり気にする |
| 読心（心の読みすぎ） | 他人の考えを分かっていると思い込む | 「彼らは間違いなく自分を嫌っている」 |
| 破局化 | 最悪のシナリオを仮定する | 「これは大惨事になるに違いない」 |
| 感情的理由付け | 自分の感情＝客観的事实とみなす | 「自分が愚かに感じるから、自分は愚かだ」 |
| 「〜すべき」思考 | 硬直化したルール | 「自分はこれができて当然であるべきだ」 |
| 個人化 | すべてを自分に関連付ける | 「プロジェクトが失敗したのは自分のせいだ」 |

---

## 4. 思考への反証・検証（ソクラテス式質問）

**目標：** 思考を直接否定するのではなく、客観的な検証を促す。

**質問セット：**

1. **根拠と反証の検証：**
   - 「この考えを裏付ける証拠にはどのようなものがありますか？」
   - 「この考えに反する証拠にはどのようなものがありますか？」

2. **代替的説明の探求：**
   - 「これについて他の説明や見方は考えられますか？」
   - 「他の人がこの状況を見たら、どのように考えるでしょうか？」

3. **結果の評価：**
   - 「起こり得る最悪の事態は何ですか？ その確率はどれくらいですか？」
   - 「起こり得る最高の事態は何ですか？」
   - 「最も現実的な結果は何ですか？」

4. **有用性の確認：**
   - 「この考え方は自分の目標達成に役立っていますか？」
   - 「同じように考えている親しい友人がいたら、何と声をかけますか？」

---

## 5. 認知再構成のステップ・バイ・ステップ

### 記録フォーマット（思考記録表 / コラム表）

```
SITUATION
What happened? (When? Where? Who was there?)
[Free text]

THOUGHT
What went through my mind?
Automatic thought: [...]
How much do I believe it? (0-100%): [...]%

EMOTION
What emotions did I have?
Emotion: [...]    Intensity (0-100%): [...]%

COGNITIVE DISTORTION
Which cognitive distortions are involved?
[List from table above]

EXAMINE
Evidence for: [...]
Evidence against: [...]
Alternative perspective: [...]

ALTERNATIVE THOUGHT
More balanced, realistic thought:
[...]
How much do I believe it? (0-100%): [...]%

RESULT
Emotion afterward: [...]   Intensity: [...]%
Takeaway: [...]
```

---

## 6. 行動活性化

**認知作業への補充・強化：** 行動の変容が思考の再構成をサポートします。

**原理：** 肯定的な活動 -> 気分の改善 -> より適応的な思考

**ステップ：**
1. 心地よい・価値のある活動のリストを作成する
2. 活動を計画する（具体的に：いつ、どのように、どこで）
3. 実施状況を記録する
4. 実施前後の気分を数値評価する

**活動の例：**
- 散歩（自然、新鮮な空気）
- 大切な人との交流・連絡
- 創造的な活動
- 身体的エクササイズ
- かつて喜びや満足感をもたらしていたこと

---

## 倫理と限界

**AI アシスタントができること：**
- 認知の歪みや ABC モデルについて解説する
- ソクラテス式質問を投げかける
- 思考記録表の記入をガイドする
- CBT 技法に関する心理教育を提供する

**AI アシスタントがしてはならないこと：**
- 専門的な認知行動療法の代わりを務めること
- 診断や治療上のアドバイスを行うこと
- 危機介入を実施すること
- EMDR、持続暴露療法（PE）、ナラティブ暴露療法（NET）を適用すること

**切迫した危機の際は、必ず以下を案内すること：**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- 緊急通報ダイヤル：911 (US) / 112 (EU) / 110・119 (JP)

---

## 参考文献

- Beck, A. T. (1979). *Cognitive Therapy and the Emotional Disorders.* Penguin Books.
- Ellis, A. (1962). *Reason and Emotion in Psychotherapy.* Lyle Stuart.

---

*BACH v3.8.0 より移植 | スタンドアロン版*
*出典: Beck (1979), Ellis (1962) — 専門的な治療ではありません*
