---
name: decide
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: 结构化决策：优缺点矩阵、加权评分、决策树、情景分析和艾森豪威尔矩阵。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [decision, evaluation, prioritization, framework]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/decide.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="decide banner">

> **中文** — `decide` 官方中文版本。


# Decide — 结构化决策 (中文)

> 通过结构化框架与评估方法做出理性决策

---

## 适用场景

- 在多个选项之间做出选择
- 需要列出优缺点清单
- 多标准决策
- 对重要决策感到不确定

**触发词 (Trigger words):** decide, choose, compare, evaluate, weigh

---

## 决策框架

### 1. 优缺点矩阵 (简单)

在 2 个选项之间快速决策。

```
PRO A:                    CON A:
- Advantage 1             - Disadvantage 1
- Advantage 2             - Disadvantage 2

PRO B:                    CON B:
- Advantage 1             - Disadvantage 1
- Advantage 2             - Disadvantage 2

Recommendation: [A/B] because [reasoning]
```

---

### 2. 加权评分 (复杂)

带精细权重的多标准决策。

| 标准 | 权重 | 选项 A | 得分 A | 选项 B | 得分 B |
|-----------|--------|----------|---------|----------|---------|
| 标准 1 | 30% | 8 | 2.4 | 6 | 1.8 |
| 标准 2 | 25% | 7 | 1.75 | 9 | 2.25 |
| 总计 | 100% | - | X.XX | - | X.XX |

**流程:**
1. 收集评估标准
2. 分配权重（总和 = 100%）
3. 选项打分（1-10 分制）
4. 计算得分（评分 x 权重）
5. 对比并给出建议

---

### 3. 决策树 (顺序)

具有清晰 if-then 路径的决策：
1. 确定起始问题
2. 第一层分支（最重要的标准）
3. 下一层级（第二重要的标准）
4. 最终导向具体选项

---

### 4. 情景分析 (不确定性)

```
Best Case (X% probability):
  Outcome: +Y points -> Expected value: +Z

Realistic Case (X%):
  Outcome: +Y -> Expected value: +Z

Worst Case (X%):
  Outcome: -Y -> Expected value: -Z

Total expected value: [Sum]
```

---

### 5. 艾森豪威尔矩阵 (优先级排序)

```
              URGENT          NOT URGENT
IMPORTANT     1. DO           2. PLAN
NOT IMPORTANT 3. DELEGATE     4. ELIMINATE
```

---

## 质量检查清单

在给出最终建议前进行检查：
- [ ] 是否已识别所有相关标准？
- [ ] 是否考虑了用户价值观？
- [ ] 是否考虑了长期影响？
- [ ] 是否识别并评估了风险？
- [ ] 是否进行了偏见检查？
- [ ] 是否评估了可逆性？

---

## 最佳实践

### 确定标准
- 具体且可衡量
- 数量适中（3-7 个为宜）
- 各标准相互独立

### 权重分配
- 总和 = 100%
- 最重要的标准权重 >= 25%
- 不设置低于 5% 的权重

### 给出建议
- 明确且论据充分
- 提及备选方案
- 指出潜在风险
- 考虑决策的可逆性

---

## 工作流与步骤

```
1. User request
2. Understand decision
3. Identify options (2-5)
4. Choose framework
5. Collect criteria
6. Apply framework
7. Bias check (optional)
8. Make recommendation
9. Document reasoning
```

---

## 更新日志

### 1.0.0 (2026-03-15)
- 从 BACH v3.8.0 移植

---

*从 BACH v3.8.0 移植 | 独立版本*