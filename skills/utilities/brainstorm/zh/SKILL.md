---
name: brainstorm
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: 用于构思和创意的结构化创新方法：SCAMPER、六顶思考帽、思维导图、逆向头脑风暴、TRIZ 以及快速构思。
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

> 面向创新的结构化创意方法 — SCAMPER、六顶思考帽、思维导图、逆向头脑风暴、TRIZ、快速构思

---

## 何时使用？

- 需要新想法 / 新创意
- 陷入僵局 / 遇到创意瓶颈
- 寻求创新方案
- 创造性地解决问题

**触发词：** brainstorm, ideas, creative, innovative, ideation

---

## 方法

### 1. SCAMPER

**替代 (Substitute)、合并 (Combine)、适应 (Adapt)、修改 (Modify)、改作他用 (Put to other use)、消除 (Eliminate)、反转 (Reverse)**

系统化改进现有解决方案：
- **S**ubstitute（替代）：什么可以被替换？
- **C**ombine（合并）：什么可以组合在一起？
- **A**dapt（适应）：什么可以调整或借鉴？
- **M**odify（修改）：什么可以改变或修改？
- **P**ut to other use（改作他用）：还可以用于什么其他用途？
- **E**liminate（消除）：什么可以被移除或简化？
- **R**everse（反转/逆向）：什么可以颠倒或重新排列？

---

### 2. 六顶思考帽（爱德华·德·博诺）

从 6 个视角系统地展开思考：

- **白帽 — 事实：** 我们有哪些信息？还缺少什么？
- **红帽 — 情感：** 感觉如何？直觉、本能感受
- **黑帽 — 批判：** 可能会出什么问题？风险与弱点
- **黄帽 — 乐观：** 有哪些机遇？最佳情况
- **绿帽 — 创意：** 新想法？打破常规的思想？
- **蓝帽 — 整体/元思考：** 过程控制、总结、下一步行动

**流程：** 定义问题（蓝帽） -> 梳理事实（白帽） -> 表达情感（红帽） -> 批判评估（黑帽） -> 挖掘积极面（黄帽） -> 激发新创意（绿帽） -> 总结规划（蓝帽）

---

### 3. 思维导图 (Mind Mapping)

按层级结构对思考进行可视化：
1. 中心主题
2. 主要分支（3-7 个）
3. 每个分类的子分支
4. 添加细节与想法
5. 识别并连接关联点

---

### 4. 逆向头脑风暴 (Reverse Brainstorming)

将问题倒置：“我们如何能让情况变得更糟？”

1. 倒置/反转问题
2. 收集各种“坏主意”
3. 将坏主意反转 = 获得好创意

当直接构思陷入僵局时特别有效。

---

### 5. TRIZ（发明问题解决理论）

适用于软件领域的十大原理：
1. **分割 (Segmentation)：** 将单体拆分为模块
2. **抽取 (Extraction)：** 隔离干扰/有害特性
3. **局部质量 (Local Quality)：** 不同组件具备不同特性
4. **组合 (Merging)：** 合并相似功能
5. **通用性 (Universality)：** 单一元素承担多种功能
6. **嵌套 (Nesting)：** 组件嵌套在组件内部
7. **预先作用 (Preliminary Action)：** 提前进行准备
8. **反馈 (Feedback)：** 监控与自适应
9. **自助 (Self-Service)：** 系统进行自我维护
10. **非对称性 (Asymmetry)：** 非对称设计

---

### 6. 快速构思 (Rapid Ideation)

数量高于质量 — 20 分钟内提出 50+ 个想法。

**规则：**
- 构思期间禁止任何批评
- 欢迎疯狂/大胆的想法
- 在他人的想法基础上进行拓展
- 数量第一

**基于计时器：**
- 第 1 轮（5 分钟）：开放式构思
- 第 2 轮（5 分钟）：变体与衍生
- 第 3 轮（5 分钟）：组合与融合
- 第 4 轮（5 分钟）：极端/极限想法

---

## 工作流与流程

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

## 变更日志

### 1.0.0 (2026-03-15)
- 从 BACH v3.8.0 移植

---

*从 BACH v3.8.0 移植 | 独立版本*
