---
name: cognitive-restructuring
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 认知行为疗法：ABC模型、自动思维、识别认知扭曲以及填写思维记录表。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [cbt, cognitive-restructuring, cognitive-distortions, thought-record, abc-model]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/therapie/kognitive_umstrukturierung.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **中文** — `cognitive-restructuring` 官方中文版本。


# Cognitive Restructuring (中文)

> CBT核心技术：ABC模式，识别与重构非建设性思维

See: [ETHICS.md](../ETHICS.md)

---

## 背景

认知重构是认知行为疗法（CBT）的核心技术。它有助于识别负性自动思维，对其提出质疑，并用更具建设性的替代思维加以重构。

**注意：** 本技能仅提供支持，不能替代专业心理治疗。
**严禁实施：** 眼动脱敏再加工（EMDR）、延长暴露疗法（PE）、叙事暴露疗法（NET）

---

## 1. ABC 模型（Ellis）

ABC模型解释了事件、思维与情绪/行为之间的联系。

```
A (Activating Event)   ->  B (Beliefs / Thoughts)  ->  C (Consequences / Feelings/Behavior)
Trigger                     Evaluation / Belief           Emotional consequence
```

**重要提示：** 引起情绪后果（C）的并不是事件本身（A），而是对事件的认知评估与信念（B）！

**示例：**
```
A: Boss criticizes a report in a meeting
B: "I am incompetent, everyone thinks so now"
C: Shame, withdrawal, avoiding future contributions
```

**目标：** 通过改变 B 来调节和改善 C。

---

## 2. 识别负性自动思维（ANTs）

**什么是负性自动思维（ANTs）？**
- 在应激或高压情境下迅速产生的自动认知评估
- 常被误认为是既成事实，但本质上只是主观解释
- 倾向于夸大、泛化和灾难化

**典型识别特征：**
- 绝对化思维：“总是”、“从不”、“所有人”、“没有人”
- 灾难化：“这一定会以惨败告终”
- 读心术：“他们肯定觉得……”
- 过度概括：“这对我来说永远行不通”

**提问引导：**
- “当那件事发生时，你脑海中浮现了什么想法？”
- “当你回想那个情境时，脑海里有什么词句？”
- “你最担心或害怕发生什么？”

---

## 3. 认知扭曲（思维误区）

| 认知扭曲 | 描述 | 示例 |
|------------|-------------|---------|
| 全或无思维 | 非黑即白的二元思维 | “如果我不能做到完美，我就是个失败者” |
| 过度概括 | 将单次事件总结为普遍规律 | “这种事在我身上总是搞砸” |
| 心理过滤 | 仅关注消极信息，忽略积极信息 | 在整体好评中只盯着一条批评意见 |
| 读心术 | 主观断定他人的想法 | “他们肯定讨厌我” |
| 灾难化 | 盲目假设最坏的结果 | “这将会是一场灾难” |
| 情绪化推理 | 将主观感受等同于客观事实 | “我觉得自己很笨，所以我就是很笨” |
| 应该/必须思维 | 僵硬刻板的规则律令 | “我本应该能够做到这一点的” |
| 个人化 | 盲目将责任完全归咎于自己 | “项目进展不顺利都是我的错” |

---

## 4. 质疑思维（苏格拉底式提问）

**目标：** 不是直接驳斥想法，而是引导对思维进行客观检验与审查。

**提问清单：**

1. **检验证据：**
   - “支持这个想法的证据是什么？”
   - “反对或不支持这个想法的证据是什么？”

2. **寻求替代解释：**
   - “对此是否存在其他解释？”
   - “换作其他人会如何看待这个局势？”

3. **评估后果：**
   - “可能发生的最坏结果是什么？发生的概率有多大？”
   - “可能发生的最佳结果是什么？”
   - “最现实/可能的结果是什么？”

4. **检验实用性：**
   - “保持这种想法有助于我实现目标吗？”
   - “如果有好友产生同样的想法，我会对他/她说什么？”

---

## 5. 认知重构步骤

### 记录格式（思维记录表）

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

## 6. 行为激活

**认知工作的补充手段：** 改变行为有助于巩固和支持思维的重构。

**原理：** 积极活动 -> 改善情绪 -> 产生更具建设性的思维

**步骤：**
1. 列出令人愉悦或富有意义的活动清单
2. 制定活动计划（具体说明：时间、地点、实施方式）
3. 记录实施过程
4. 评估活动前后的情绪状态

**活动示例：**
- 散步（接触自然、呼吸新鲜空气）
- 与重要亲友保持联系与互动
- 创造性活动
- 体育锻炼
- 过去能够带来快乐或成就感的事物

---

## 伦理与边界

**AI 助手可以：**
- 讲解认知扭曲与 ABC 模型
- 提出苏格拉底式提问
- 指导填写思维记录表
- 提供关于 CBT 技术的心理教育

**AI 助手严禁：**
- 替代专业的认知行为心理治疗
- 做出诊断或给出临床治疗建议
- 开展危机干预
- 实施 EMDR、延长暴露疗法（PE）或叙事暴露疗法（NET）

**如遇急性危机，请务必转介至：**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- 紧急救援服务：911 (US) / 112 (EU) / 120 或 110 (CN)

---

## 参考文献

- Beck, A. T. (1979). *Cognitive Therapy and the Emotional Disorders.* Penguin Books.
- Ellis, A. (1962). *Reason and Emotion in Psychotherapy.* Lyle Stuart.

---

*移植自 BACH v3.8.0 | 独立版本*
*参考来源: Beck (1979), Ellis (1962) — 非专业心理治疗*
