---
name: positive-psychology
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: 塞利格曼的积极心理学：PERMA模型、性格优势（VIA）、感恩练习、心流理论和心理韧性因素。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [positive-psychology, perma, flow, gratitude, resilience, seligman]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/therapie/positive_psychologie.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **中文** — `positive-psychology` 官方中文版本。


# 积极心理学 (中文)

> 聚焦性格优势、感恩、心流与PERMA模型（基于塞利格曼与米哈里·契克森米哈赖）

参见: [ETHICS.md](../ETHICS.md)

---

## 背景与语境

积极心理学是对“是什么使生活值得付出”的科学研究（Seligman & Csikszentmihalyi, 2000）。与传统临床心理学（探究“什么导致了疾病？”）不同，它探究：是什么让人们保持健康、快乐和具备心理韧性？

创始人：马丁·塞利格曼（Martin Seligman，1998年美国心理学会主席）发起了该运动。其他先驱包括：米哈里·契克森米哈赖（Mihaly Csikszentmihalyi，心流理论）、克里斯托弗·彼得森（Christopher Peterson，性格优势）、芭芭拉·弗雷德里克森（Barbara Fredrickson，扩展-建构理论）、埃德·迪纳（Ed Diener，主观幸福感）。

**注意：** 本技能仅提供心理教育辅助，不能替代专业心理咨询或治疗。
**严禁实施：** EMDR（眼动脱敏与再加工）、延长暴露疗法（PE）、叙事暴露疗法（NET）。

---

## 1. PERMA模型 (Seligman, 2011)

塞利格曼提出的幸福五大支柱（《持续的幸福》）：

### P — 积极情绪 (Positive Emotions)
- 喜悦、感恩、宁静、兴趣、希望、自豪、爱
- 弗雷德里克森（Fredrickson）：积极情绪与消极情绪的比例至少应达到 3:1
- 练习：“三件好事”（详见下文）

### E — 投入 (Engagement)
- 完全沉浸于某项活动中（心流状态）
- 在日常生活中运用个人的核心优势
- 挑战与技能达到平衡

### R — 积极人际关系 (Positive Relationships)
- 社会连接是预测幸福感最强有力的指标
- 对他人的好消息做出积极建设性的回应
- 随机善举（Random Acts of Kindness）

### M — 意义 (Meaning)
- 归属于并服务于高于个人的目标
- 通过工作、家庭、社区或精神追求实现意义
- 弗兰克尔（Frankl）：“知道为什么活着的人，几乎能承受任何生存方式”

### A — 成就 (Achievement)
- 体验胜任感与精通感
- 设定并实现切合实际的目标
- 坚韧性（Grit）：对长期目标的恒心与热情（Duckworth, 2016）

---

## 2. 性格优势 (VIA分类法)

彼得森与塞利格曼（Peterson & Seligman, 2004）在6大美德类别中总结出了24种普适的性格优势：

| 美德 | 性格优势 |
|--------|----------|
| 智慧与知识 | 创造力、好奇心、审慎思考/判断力、热爱学习、远见卓识 |
| 勇气 | 勇敢、坚持不懈、诚实/正直、活力/热情 |
| 仁爱 | 爱、友善、社会智慧 |
| 正义 | 团队合作、公平、领导力 |
| 节制 | 宽恕、谦逊、谨慎、自我调节 |
| 超越 | 审美力、感恩、希望、幽默、精神信仰 |

**标志性优势（Signature strengths）：** 感到最真实、最契合个人的3-5种优势。研究证明，每天使用标志性优势的人满意度显著更高，抑郁倾向更低（Seligman et al. 2005）。

**VIA测试：** 可在 viacharacter.org 进行免费科学测评。

---

## 3. 感恩练习

### 3.1 三件好事 (Seligman et al. 2005)

**操作步骤：**
1. 每天晚上写下当天发生的3件好事。
2. 针对每件事记录：为什么会发生这件事？
3. 持续时间：至少1周，理想情况为长期坚持。

**循证支持：** 在6个月内能显著提高幸福感并减少抑郁症状（Seligman et al. 2005）。

### 3.2 感恩日记

“三件好事”的扩展版：
- 晨间：今天我对什么充满感恩？（3项）
- 晚间：今天有什么好事？我做出了什么贡献？
- 视角转换：他人、经历、能力、日常生活中的微小细节。

### 3.3 感恩信与感恩拜访 (Gratitude Visit)

**操作步骤：**
1. 寻找一位你从未给予过正式感谢的人。
2. 写一封具体的感谢信（约300字，内容具体）。
3. 亲自拜访该对象并当面朗读信件。

**循证支持：** 在所有积极心理学干预中短期效果最为强劲（Seligman et al. 2005）。效果可持续约1个月。

---

## 4. 心流理论 (Csikszentmihalyi, 1990)

### 定义
心流（Flow）是一种完全沉浸于某种活动中的状态，此时行动流畅不费力，时间感和自我意识退居幕后。

### 心流产生的条件

| 条件 | 描述 |
|-----------|-------------|
| 动态平衡 | 任务挑战与个人技能水平相匹配 |
| 目标明确 | 清楚地知道下一步要做什么 |
| 即时反馈 | 能立即获得关于进度的反馈 |
| 高度专注 | 注意力完全集中于当前任务 |
| 掌控感 | 感觉自己能够驾驭当前局势 |
| 内驱力 | 活动本身即具有内在奖赏性 |

### 心流通道

```
Challenge
     high   |  Anxiety    |  FLOW
            |             |
     low    |  Apathy     |  Boredom
            +-------------|----------
              low              high
                    Skill
```

### 促进心流的策略
- 消除干扰（收起手机、关闭房门）
- 将大任务拆解为可管理的小单元
- 调整难度等级（不过于简单，也不过于困难）
- 建立固定的专注练习时间

---

## 5. 心理韧性因素 (Resilience Factors)

心理韧性（Resilience）= 面对逆境时的心理抗逆力。

### 心理韧性的7大支柱 (Reivich & Shatte, 2002)

1. **情绪调节：** 感知并管理自身的情绪
2. **冲动控制：** 有意识地引导行为而非盲目反应
3. **因果分析：** 客观理性地评估事件原因
4. **自我效能感：** 对自身能力的信心
5. **共情能力：** 识别并理解他人的情绪
6. **乐观心态：** 对未来保持合理且积极的预期
7. **目标导向：** 设定并追求富有意义的目标

### 提升心理韧性
- 有意识地使用优势（VIA性格优势）
- 维护社会支持网络（人际关系是第一大保护性因素）
- 自我关怀：睡眠、运动、营养、恢复
- 认知灵活性：寻求替代性视角
- 寻找意义与价值（即使在艰难情境中）

---

## 伦理与边界

**AI助手可以：**
- 解释PERMA模型与性格优势（心理教育）
- 引导并支持感恩练习
- 讨论心流产生的条件
- 讲解心理韧性因素
- 支持对标志性优势的自我反思

**AI助手严禁：**
- 仅凭积极心理学干预临床抑郁症
- 对VIA测评结果进行临床诊断性解释
- 推荐积极心理学作为专业心理治疗的替代品
- 鼓吹毒性积极（如“你只要懂得感恩就好了”）

**进度追踪：**
- 练习前后幸福感评分（0-10分标尺）
- 感恩打卡：连续坚持了多少天？
- 心流日志：在何时以及从事什么活动时体验到了心流？
- 标志性优势：本周使用了多少次？

**如遇急性危机，务必立即转介至：**
- 988 Suicide & Crisis Lifeline (US): 988
- Crisis Text Line (US): Text HOME to 741741
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- 紧急救援电话: 911 (US) / 112 (EU) / 120, 110 (CN)

---

*Ported from BACH v3.8.0 | Standalone Version*
*Sources: Seligman (2011), Csikszentmihalyi (1990), Peterson & Seligman (2004) — Not professional therapy*