---
name: cognitive-restructuring
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 认知行为疗法（CBT）：ABC 模型、自动思维、识别认知歪曲以及填写思维记录表。
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


# 认知重塑（中文）

> CBT 核心技术：ABC 图式、识别与修改非功能性思维

参见：[ETHICS.md](../ETHICS.md)

---

## 背景

认知重塑（Cognitive Restructuring）是认知行为疗法（CBT）的核心技术。它有助于识别自动负性思维、对其发起挑战，并用更有建设性、更符合现实的替代思维予以替换。

**注意：** 本技能仅提供支持，不能替代专业心理治疗。
**严禁实施：** EMDR（眼动脱敏再加工）、Prolonged Exposure（持续暴露疗法 PE）、Narrative Exposure Therapy（叙事暴露疗法 NET）

---

## 1. ABC 模型（埃利斯）

ABC 模型解释了事件、思维与感受之间的联系。

```
A（激发事件 Activating Event）  ->  B（信念/思维 Beliefs/Thoughts）  ->  C（结果/情绪与行为 Consequences）
触发因素                              评估 / 解释                            情绪与行为后果
```

**重要前提：** 产生情绪（C）的并不是事件本身（A），而是对事件的评估与解读（B）！

**示例：**
```
A：上司在会议上批评了一份报告
B：“我很无能，现在大家肯定都这么想”
C：羞耻、退缩、避免在未来的会议中发言
```

**目标：** 改变 B，从而改善 C。

---

## 2. 识别自动负性思维（ANTs）

**什么是自动负性思维（ANTs）？**
- 在应激情境中快速、自动涌现的评估
- 往往被个体视作事实，尽管它们只是主观解释
- 容易倾向于夸大、过度概括和灾难化

**典型识别特征：**
- 绝对化思维：“总是”、“从不”、“所有人”、“没有人”
- 灾难化：“这下彻底完蛋了”
- 读心术：“他们肯定认为……”
- 过度概括：“我做这事就从来没成功过”

**识别引导提问：**
- “事情发生时，你脑海里闪过了什么想法？”
- “当你回想那个情境时，脑海里出现了哪些词句？”
- “你害怕可能会发生什么？”

---

## 3. 认知歪曲（思维误区）

| 认知歪曲 | 描述 | 示例 |
|------------|-------------|---------|
| 非黑即白（全或无思维） | 极端的二元思维 | “如果我做不到完美，我就是个失败者” |
| 过度概括 | 以偏概全，单次事件代表整体 | “我做这事总是搞砸” |
| 心理过滤 | 仅关注负面信息，忽略正面 | 在大量好评中只关注唯一的一条批评 |
| 读心术 | 盲目坚信知道别人的想法 | “他们肯定非常讨厌我” |
| 灾难化 | 预想最坏的结果 | “这将会是一场彻底的灾难” |
| 情绪化推理 | 将感觉等同于现实 | “我觉得自己很傻，所以我就是很傻” |
| 应该/必须思维 | 刻板僵化的规则 | “我应该/必须能够做到这一点” |
| 个人化 | 将不相关的客观事件归咎于自己 | “项目没做好完全是我的责任” |

---

## 4. 质疑与辩驳思维（苏格拉底式提问）

**目标：** 不是直接反驳用户的想法，而是引导其进行理性审视。

**提问清单：**

1. **检验证据：**
   - “支持这个想法的证据是什么？”
   - “反对这个想法的证据有哪些？”

2. **寻求替代解释：**
   - “对此还有其他解释的可能吗？”
   - “换作其他人会如何看待这个情境？”

3. **评估后果：**
   - “可能发生的最坏情况是什么？发生的概率有多大？”
   - “可能发生的最理想情况是什么？”
   - “最现实、可能发生的结果是什么？”

4. **检验有用性：**
   - “保持这种想法有助于你实现目标吗？”
   - “如果是你的好朋友有这种想法，你会对他/她说什么？”

---

## 5. 认知重塑步骤指南

### 思维记录表格式（Thought Record）

```
情境（SITUATIONS）
发生了什么？（时间？地点？当时有谁在场？）
[自由文本]

自动思维（THOUGHTS）
当时我脑海里浮现了什么想法？
自动思维：[...]
我对该想法的相信程度 (0-100%)：[...]%

情绪（EMOTIONS）
我当时有什么情绪体验？
情绪：[...]    强度 (0-100%)：[...]%

认知歪曲（COGNITIVE DISTORTIONS）
涉及到了哪些认知歪曲？
[参考上表清单]

辩驳与检验（EXAMINE）
支持的证据：[...]
反对的证据：[...]
替代视角：[...]

替代思维（ALTERNATIVE THOUGHTS）
更客观、更平衡的替代思维：
[...]
我对替代思维的相信程度 (0-100%)：[...]%

结果与复盘（RESULT）
重塑后的情绪：[...]   强度：[...]%
总结与收获：[...]
```

---

## 6. 行为激活

**对认知工作的补充：** 改变行为有助于巩固思维的转变。

**原理：** 积极活动 -> 情绪改善 -> 更有建设性的思维

**步骤：**
1. 列出愉悦/有意义的活动清单
2. 计划活动（具体到：时间、地点、方式）
3. 追踪执行情况
4. 评估活动前后的情绪变化

**活动示例：**
- 散步（拥抱自然、呼吸新鲜空气）
- 与对你重要的人保持联系
- 创意手作或艺术活动
- 体育锻炼
- 过去曾带来快乐的事情

---

## 伦理与边界

**AI 助手可以：**
- 讲解认知歪曲与 ABC 模型
- 运用苏格拉底式提问
- 引导填写思维记录表
- 提供关于 CBT 技术的心理教育

**AI 助手不得：**
- 替代专业的认知行为心理治疗
- 提供诊断或治疗方案
- 进行危机干预
- 实施 EMDR、Prolonged Exposure（PE）或 Narrative Exposure Therapy（NET）

**在发生急性危机时，请务必联系：**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): 发送 HOME 至 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- 中国心理危机干预热线: 010-82951332 / 400-161-9995
- 紧急救援电话: 911 (US) / 112 (EU) / 110 (CN)

---

## 参考文献

- Beck, A. T. (1979). *Cognitive Therapy and the Emotional Disorders.* Penguin Books.
- Ellis, A. (1962). *Reason and Emotion in Psychotherapy.* Lyle Stuart.

---

*移植自 BACH v3.8.0 | 独立版本*
*参考文献：Beck (1979), Ellis (1962) — 非专业替代医疗服务*