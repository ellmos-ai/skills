---
name: pipeline-optimizer
version: 1.2.0
type: protocol
author: Lukas Geiger (method) + Claude (write-up)
created: 2026-05-16
updated: 2026-06-13
aliases: [project-folder-optimizer, pipeline-renovator, project-renovator]
description: 结构化的6步骤流程，用于改进、改造或重构现有的流水线（pipeline）、独立项目文件夹、文档结构或软件技术栈。可调用为“pipeline optimizer”（针对整个主题流水线，例如软件、研究或游戏开发流水线）或“project-folder optimizer”（针对流水线内的独立项目文件夹，例如单个软件工具或论文项目）。触发于诸如“改进流水线X”、“优化技术栈”、“重构Y”、“改造”、“流水线重构”、“清理项目文件夹”、“改进文件夹结构”、“统一规范”、“文档整合”、“集成到现有系统”或针对既有结构的任何实质性干预等任务。提供既有资产调查、目的明确化、理想蓝图草图、差距规划、实证痛点识别以及使用全新的子智能体进行重新测试。防止并行标准、重复建设和流水线中断。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [pipeline, renovation, refactoring, stack, workflow, lessons-learned]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/pipeline-optimizer/', 'origin_version': '1.1.1', 'last_sync_from_origin': '2026-05-16', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **中文** — `pipeline-optimizer` 官方中文版本。


# Pipeline Optimizer / Project-Folder Optimizer (中文)

**无不兼容问题的6步骤改造流程** — 适用于两个层级：

| 触发器名称 | 作用域 | 示例 |
|---|---|---|
| **Pipeline optimizer** | 整个流水线、技术栈、文档结构 | 您的主题流水线，例如 `software/`、`research/`、`games/`、智能体系统 |
| **Project-folder optimizer** | 流水线内的独立项目文件夹 | 软件工具、论文项目、游戏项目 |

这里的**流水线（pipeline）**是指面向主题的顶层结构，多个项目在其中基于共享规范共同存在（例如包含发布规则的软件流水线、包含出版流程的研究流水线）。

两者均采用相同的6步骤工作流 — 唯一的区别在于**作用域**（全流水线范围 vs. 单个项目），并相应决定步骤 A 中既有资产调查的深度。

## 何时适用本 Skill

当要求您改进、重构或扩展**现有**结构时（而非用于全新的空地建设/greenfield），即适用本 Skill。具体触发词：

**流水线层级**（作用域：整个流水线）：
- “改进流水线 X”
- “优化技术栈”
- “改造软件流水线”
- “研究流水线中的文档整合”
- 对主题流水线、中央 `_tools/` 或系统组件进行实质性干预

**项目文件夹层级**（作用域：单个项目文件夹）：
- “清理 / 优化项目文件夹 X”
- “改进 Y 中的文件夹结构”
- “重构单个工具”
- “统一论文项目设置”
- “使游戏项目文件夹符合流水线标准”

**横向/跨切面：**
- “重构 X / 将其集成到现有 Y”
- “重构”、“整合”
- “统一规范”
- “集成到现有系统”

## 既有建筑/资产比喻

改造房屋首先需要知道**它是用什么建造的**（石头、木头、塑料）、**它的用途是什么**（山间小屋、软件工坊）以及**它已经在哪里发挥作用**。这一原则同样适用于流水线。

---

## 实施步骤 — 6个步骤（切勿跳过，切勿重排顺序）

### 步骤 A — 调查既有资产

**问题：** 房屋是由什么构成的？

**流水线作用域**（所有根文档 + 工具 + 模板）：
- [ ] **完整阅读所有根文档**（不仅是代码片段/插入点）
- [ ] 检查模板文件夹（`_templates/`、`_TEMPLATES/`）和工具文件夹（`_tools/`）
- [ ] 规范文件：例如 GITHUB-POLICY.md、RELEASE-MANAGEMENT.md、QUALITY_RULES.md、NAMING-SYSTEM.md、出版流程等…
- [ ] 状态快照：例如 PROJECT_STATUS.md、状态概览、releases.json、注册表文件
- [ ] 检查清单：例如发布检查清单、构建/PDF检查清单
- [ ] 工作流文件：AGENTS.md、GUIDE.md、SKILL.md
- [ ] 经验教训文件：LESSONS_LEARNED.md、MEMORY.md、循环状态文件

**项目文件夹作用域**（单个项目实质内容 + 相关的流水线规范）：
- [ ] **阅读项目文件夹中的所有 Markdown 和控制文件**（README、CHANGELOG、TASKS/TODO、DONE、CONCEPT、行动计划、证明笔记等）
- [ ] **调查代码结构：** src/、tests/、构建配置（pyproject.toml、requirements.txt、项目清单、工具链文件等）
- [ ] **考量父流水线的规范**（例如对于软件项目：GitHub 策略、命名系统、发布管理、模板）
- [ ] **扫描项目中现有的工具/脚本**（`_tools/`、`_scripts/`、build_*.bat、START 脚本）
- [ ] **配置文件：** `.gitignore`、LICENSE、NOTICE、SECURITY.md、CODE_OF_CONDUCT.md

**反模式：** 使用 `grep -l "<keyword>"` 查找插入点并在不了解文件上下文的情况下直接插入。

**输出：** 在所选作用域内包含所有相关规范、工具和模板的清单记录。

### 步骤 B — 明确存在目的

**问题：** 房屋为何而存在？

用 1-2 句话明确阐述其存在目的。

**流水线示例：**

| 流水线 | 目的 |
|---|---|
| 软件流水线 | 开发、测试并发布桌面应用 + 浏览器工具到应用商店/GitHub |
| 研究流水线 | 撰写学术论文、同行评审并发布至代码库/预印本服务器 |
| 游戏流水线 | 开发游戏并发布到目标平台 |
| 智能体系统 | 用于多智能体协同编排的 LLM 系统 |

**项目文件夹示例：**

| 项目文件夹 | 目的 |
|---|---|
| `software/PlannerApp` | 计划管理桌面应用，商业项目，私有仓库 |
| `research/CosmologyModel` | 模型论文系列 + 数值计算 |
| `games/SortingChaos` | 分类游戏，Alpha 阶段，关卡推进 |

存在目的**指导每一次干预** — 不服务于该目的的措施将被直接舍弃。

### 步骤 C — 勾勒理想蓝图

**问题：** 为此目的打造的完美房屋应该是什么样子？

- 从您自身的视角进行勾勒（简短，最多 10 点）
- 引入最佳实践对比（例如 SaaS 的 Vercel 栈，研究领域的 scientific-python 栈）
- 切勿陷入细节优化 — 高层级的概要草图即可

**输出：** 5-10 点“每个流水线的理想状态”

### 步骤 D — 差距分析与规划

**每个流水线需回答四个问题：**

1. **房屋已经具备什么？** — 即使解决方式与理想状态不同，但**功能上等效**。
   *示例：* 理想状态要求“使用 pip-licenses 处理第三方许可证”。现实情况：通过自定义生成器脚本包裹它 → 功能等效，无需干预。

2. **什么妨碍了功能？** — 当前导致中断或产生额外负担的既有结构。

3. **什么是不具备功能的？** — 死代码、过时的规范、未使用的工具。

4. **什么能显著改进功能？** — 带来预期收益的具体干预措施。

→ 由此制定**具体计划**：
- 什么需要**新建**？
- 什么需要**扩展**？
- 什么需要**拆除**？
- 什么保持**不变**（明确指出这一点非常重要！）

**输出：** 包含列 *干预事项* / *现有状况* / *改进措施* / *依据理由* 的计划表

### 步骤 E — 基于实证开展工作

切勿仅自顶向下规划 — 收集实际痛点：

- [ ] **已知 Bug**：Issue 跟踪器、TASKS/TODO/DONE 文件
- [ ] **错误历史**：经验教训文件、Bug 修复日志、检查注册表
- [ ] **自动化中断**：“有什么工作是我总是必须手动完成的？”
- [ ] **用户访谈**：针对性询问 — 痛点、愿望、变通方案
- [ ] **自我测试**：完整走一遍流水线（创建新项目、运行构建、模拟发布）— 在何处发生中断？

实证发现的痛点将确定步骤 D 中计划的**优先级**。

### 步骤 F — 实施后重新测试

- [ ] 委派**全新的子智能体**（不受改造上下文的影响）走一遍变更后的工作流
- [ ] **可衡量的前后对比值**：配置时间、错误率、手动步骤数量、构建时间
- [ ] **防回归检查**：变更后现有工作流是否仍正常运行？
- [ ] 如果**没有可衡量的改进**或出现回归：**回滚**改造或重新调整

## 反模式（严格禁止）

| 反模式 | 损害 | 解药 |
|---|---|---|
| 仅搜索插入点而非阅读文档 | 产生并行标准 | 完整执行步骤 A |
| 1:1 硬套“来自 X 的最佳实践” | 不兼容 | 步骤 D 进行功能等效对比 |
| 创建新文件而不检查现有规范 | 内容重复（例如 NOTICE.md ↔ THIRD_PARTY_LICENSES.txt） | 步骤 A + 步骤 D |
| 无实证依据地自顶向下规划 | 解决方案偏离实际痛点 | 在确定计划前执行步骤 E |
| 不测试自己的变更 | 未检测到回归错误 | 使用全新的智能体执行步骤 F |
| 状态不明确时“稍后澄清” | 用户随后才发现冲突 | 不确定时，再次与用户共同复核步骤 D |

## 案例研究 — NOTICE.md 事件

**任务：** 在多个主题流水线（软件、研究、游戏）中实施流水线改进。

**错误：** 跳过了步骤 A — 仅搜索插入点，而没有阅读完整的规范文件。

**后果：** 在 7 个文件中引入 `NOTICE.md` 作为“新许可证文件”，尽管 `THIRD_PARTY_LICENSES.txt` + 自定义许可证生成器（围绕 `pip-licenses` 的包装器）已经建立 — 并已记录在流水线的 GitHub 规范（必选文件 + 许可证检查清单）中。所有软件项目此前均已包含 THIRD_PARTY 文件。

**发现：** 仅在用户质问后才被发现（“我很确定我们之前已经有权限/许可证管理了”）。

**纠正：** 从项目模板中删除了 NOTICE.md，调整了另外 6 个文件，改为引用现有的许可证生成器而非 `pip-licenses`。

**教训：** 如果完整执行了步骤 A，冲突在写入前就会被检测出来。

## 经验法则

1. **对于“改进流水线”，首先阅读的时间要与编写的时间一样长。**
2. **在没有证明不存在现有标准之前，绝不建立新标准。**
3. **使用现有的工具/包装器，而非新建并行的工具。**
4. **“机械堆砌”通常比“扩展现有内容”更糟糕。**
5. **在发生冲突时回滚**永远优于维护两套并行标准。

## 完成检查清单

在将流水线改造报告为“已完成”之前：

- [ ] 步骤 A：是否已阅读所有相关的根文档？
- [ ] 步骤 B：是否用 1-2 句话阐明了流水线目的？
- [ ] 步骤 C：是否勾勒了理想蓝图（5-10 点）？
- [ ] 步骤 D：是否有带表格的差距分析（保留什么 / 扩展什么 / 新建什么 / 废除什么）？
- [ ] 步骤 E：是否核实了实证数据（Bug、教训、自测、用户访谈）？
- [ ] 计划是否已与用户达成一致？
- [ ] 步骤 F：是否使用全新的子智能体进行了测试 — 改进是否可衡量？
- [ ] 是否未引入并行标准？
- [ ] 发生冲突时：是否已回滚或坦诚说明情况？

## 最佳项目文件夹结构（适用于项目文件夹优化器）

当本 Skill 应用于**单个项目文件夹**时，以下组合建议可作为理想参考（步骤 C）：

### Anthropic 标准 (Claude Code)

| 文件/文件夹 | 功能 |
|---|---|
| `CLAUDE.md`（根目录） | 由 Claude Code 自动加载，包含项目特定指令 |
| `.claude/settings.json` | 权限、环境变量、模型选择（提交至 Git） |
| `.claude/settings.local.json` | 本地重写（切勿提交，添加到 `.gitignore`） |
| `.claude/commands/*.md` | 自定义斜杠命令 |
| `.claude/agents/*.md` | 自定义子智能体 |
| `.claude/skills/<name>/SKILL.md` | 项目 Skills |

### 您自己的项目文档模板（推荐）

如果您维护自己的项目文档模板（例如在 `<your-workspace>/_templates/project-docs/` 下），**三种构建配置文件**大有裨益。示例划分：**MINIMAL（最小化）** 提供会话核心集，包含 7 个根文件（`AGENTS.md`、`CLAUDE.md`、`README.md`、`START.md`、`STATE.md`、`TODO.md`、`DONE.md`）加上 `_tools/`。**STANDARD（标准）** 增加了 `CHANGELOG.md`、`DECISIONS.md` 和 `PATTERNS.md`。**FULL（完整）** 扩展至 14 个根文件，并额外增加了 `ARCHITECTURE.md`、`WORKFLOWS.md`、`TOOLS.md`、`GLOSSARY.md` 以及 `workflows/` 和 `.github/`。

→ **使用此类模板作为新项目的基底**（复制而非手动创建）。

### 特定流水线的补充内容（示例）

根据流水线的不同，还会增加其他强制性文件 — 典型模式：

- **软件项目：** LICENSE、CODE_OF_CONDUCT.md、SECURITY.md、CONTRIBUTING.md、THIRD_PARTY_LICENSES.txt（生成的）、pyproject.toml/requirements.txt、流水线中央发布注册表中的条目。→ 如果可用：使用流水线的 cookiecutter 模板。
- **研究项目：** 概念文档、行动计划、出版计划、归档/源码/结果/数据文件夹（`_archive/`、`_sources/`、`_results/`、`_data/`）、用于 LaTeX 的 `paper/`。对于推导证明项目：包含证明链和状态的证明笔记文件。
- **游戏项目：** 引擎的项目清单和工具链文件（例如对于 Roblox/Rojo：default.project.json、rokit.toml、wally.toml、selene.toml）、游戏设计文档、根据引擎规范设立的 `src/{server,client,shared}/`。

### 完整细节参考

→ 参阅本 Skill 文件夹中的 **`references/optimal-project-structure.md`**（德文）。包含：
- 示例 `settings.json`（Anthropic 模式）
- 必选 `.gitignore` 条目
- 反模式（不属于项目文件夹的内容）
- 按流水线类型推荐的工作流（软件/研究/游戏）
- 文档文件的 YAML 标头规范
- 自动检查草图

## 相关 Skills（何时使用其他 Skill 代替本 Skill？）

| Skill | 何时使用 |
|---|---|
| **`project-onboarding`** | 将外部现有仓库导入您自己的系统 |
| Project bootstrapper（若可用） | 在现有流水线中创建新项目（绿地开发，无需重构） |
| Pipeline bootstrapper（若可用） | 创建全新的流水线（罕见情况） |
| System onboarding（若可用） | 配置一台新机器 |

**pipeline optimizer** 负责**改造**，而非新建或导入。如果您的 Skill 集合包含 Skill 索引，请在其中搜索匹配的引导（bootstrapping）Skills。

## 交叉引用

- 细节参考：`references/optimal-project-structure.md`（在本 Skill 文件夹中）
- Anthropic Claude Code 文档：`https://docs.claude.com/en/docs/claude-code`
- 若可用：全局用户规则（例如您 `~/CLAUDE.md` 中的“改造”章节）和特定流水线的技术栈描述

## 作用域选择：流水线 vs. 项目文件夹

如果不清楚指的是哪个作用域，**请在步骤 A 前进行明确**：

| 线索 | 作用域 |
|---|---|
| “改进整个软件流水线” | 流水线 |
| “清理工具 X 的文件夹” | 项目文件夹 |
| “同步中央发布注册表” | 流水线（中央资产） |
| “重构游戏 Y 中的 AssetBuilder” | 项目文件夹 |
| “在整个流水线范围内引入检查规范” | 流水线 |
| “在项目 Z 中创建检查文件” | 项目文件夹 |

在**项目文件夹作用域**下，还需始终简要检查父流水线的规范（扩展的步骤 A），以确保干预措施与流水线保持兼容。

---

## 更新日志

### 1.2.0 (2026-06-13)
- 首次发布于 Skill 库：个人路径、具体的流水线/项目名称以及对私有 Skill 的引用均替换为通用示例；流程本身（6个步骤、反模式、案例研究、检查清单）保持不变

### 1.1.1 (2026-06-01) 及更早版本
- 内部版本（私有 Skill 目录，发布之前）
