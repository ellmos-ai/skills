---
name: brainstorm
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: 用于想法生成的结构化创意方法：SCAMPER（替换、组合、调整、修改、改变用途、消除、逆转）、六顶思考帽、思维导图、逆向头脑风暴、TRIZ（发明问题解决理论）和快速构思。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [brainstorm, creativity, ideation, scamper, six-hats, innovation]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/brainstorm.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="brainstorm banner">

> **中文** — `brainstorm` 官方中文版本。


# Brainstorm (中文)

> 创新结构化创意——SCAMPER、六顶思考帽、思维导图、逆向头脑风暴、TRIZ、快速构思

---

## 何时使用？

- 需要新想法
- 陷入僵局 / 创意受阻
- 寻求创新突破
- 创造性地解决问题

**触发词：** brainstorm、ideas、creative、innovative、ideation、头脑风暴、创意、想法

---

## 方法

### 1. SCAMPER (奔雷法)

**替换、组合、调整、修改、改变用途、消除、逆转**

系统化改进现有解决方案：
- **S**ubstitute (替换)：有什么可以替代？
- **C**ombine (组合)：有什么可以结合？
- **A**dapt (调整)：有什么可以借鉴/适应？
- **M**odify (修改)：有什么可以改变/放大？
- **P**ut to other use (改变用途)：还能用于其他什么场景？
- **E**liminate (消除)：有什么可以精简/移除？
- **R**everse (逆转)：有什么可以倒置/反转？

---

### 2. 六顶思考帽 (Edward de Bono)

系统地从 6 个视角思考问题：

- **白帽 — 事实：** 我们掌握了什么信息？还缺少什么？
- **红帽 — 情感：** 感觉如何？直觉与预感
- **黑帽 — 批判：** 可能会出什么问题？风险与劣势
- **黄帽 — 乐观：** 有哪些机遇？最佳情况是什么？
- **绿帽 — 创意：** 有什么新想法？打破常规的思想
- **蓝帽 — 总体控制：** 流程控制、总结、下一步行动

**流程：** 明确问题（蓝帽） -> 梳理事实（白帽） -> 表达情感（红帽） -> 批判风险（黑帽） -> 寻求乐观（黄帽） -> 激发生发创意（绿帽） -> 总结决策（蓝帽）

---

### 3. 思维导图 (Mind Mapping)

分层可视化思考：
1. 核心主题
2. 主分支（3-7 个）
3. 各类别的子分支
4. 添加细节与想法
5. 建立关联联系

---

### 4. 逆向头脑风暴 (Reverse Brainstorming)

反向思考问题：“我们怎样才能让情况变得更糟？”

1. 反转问题
2. 收集极坏的想法
3. 逆转 = 极好的想法

在直接构思陷入停滞时尤为有效。

---

### 5. TRIZ (发明问题解决理论)

软件领域的十大核心原理：
1. **分割 (Segmentation)：** 将单体架构拆分为模块
2. **抽取 (Extraction)：** 隔离干扰性/有害属性
3. **局质化 (Local Quality)：** 不同组件赋予不同特性
4. **组合 (Merging)：** 合并相似功能
5. **普遍性 (Universality)：** 单一元素多重功能
6. **嵌套 (Nesting)：** 组件层层嵌套
7. **预先作用 (Preliminary Action)：** 提前做好准备工作
8. **反馈 (Feedback)：** 实时监控与自适应
9. **自助 (Self-Service)：** 系统自主维护
10. **不对称 (Asymmetry)：** 非对称性设计

---

### 6. 快速构思 (Rapid Ideation)

数量高于质量——20 分钟内提出 50+ 个想法。

**规则：**
- 构思过程中禁止任何批评
- 欢迎疯狂/大胆的想法
- 在他人的想法之上建构
- 数量第一

**计时轮次：**
- 第 1 轮（5 分钟）：开放式自由构思
- 第 2 轮（5 分钟）：变体扩展
- 第 3 轮（5 分钟）：交叉组合
- 第 4 轮（5 分钟）：极限/极端构想

---

## 工作流程与步骤

```
1. 用户需求
2. 理解目标
3. 选择方法
4. 激发想法（不做批判！）
5. 聚类归纳
6. 可行性/影响力矩阵评估
7. 筛选 Top 5-10 方案
8. 方案输出 + 建议
```

---

## 变更日志

### 1.0.0 (2026-03-15)
- 从 BACH v3.8.0 移植

---

*从 BACH v3.8.0 移植 | 独立版本*