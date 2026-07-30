---
name: dev-soft-agent
version: 0.1.0
type: agent
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: 自动化软件开发 Pipeline。扫描项目、排定任务优先级、分析代码并编排开发循环。零依赖（仅使用 Python 标准库）。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [development, code-analysis, task-management, automation, pipeline]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/devSoftAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="dev-soft-agent banner">
> **中文** — `dev-soft-agent` 官方中文版本。

# Dev Soft Agent (中文)

自动化软件开发 Pipeline。提取自 BACH 的 ATI Agent，
纯依赖 Python 标准库即可完全独立运行。

## 组件结构

```
scripts/
  config.py              配置（扫描文件夹、命名前缀、权重）
  project_manager.py     项目扫描 + 按命名规范分类
  task_engine.py          TASKS.txt 解析器 + 代码扫描器 (TODO/FIXME)
  code_analyzer.py       静态分析（LOC、导入、类、函数）
  dev_loop.py            编排器 (DevLoop)
  policies/
    naming.py            snake_case / PascalCase / SCREAMING_SNAKE 验证
    encoding.py          UTF-8 强制执行 + BOM 检测
    paths.py             硬编码路径检测
  prompt_templates/
    task_prompt.txt      用于任务处理的 LLM Prompt
    review_prompt.txt    用于代码审查的 LLM Prompt
    analysis_prompt.txt  用于项目分析的 LLM Prompt
```

## 作为 Python 库使用

```python
from scripts.dev_loop import DevLoop
from scripts.config import Config

config = Config()
loop = DevLoop(config)

# 扫描项目 (中文)
projects = loop.scan_projects()

# 选择项目（按命名规范进行加权随机选择） (中文)
project = loop.select_project()

# 分析代码 (中文)
analysis = loop.analyze_project()
print(f"{analysis.total_loc} LOC, {analysis.todo_count} TODOs")

# 加载并排定任务优先级 (中文)
tasks = loop.get_tasks()
for task in tasks:
    print(f"[{task.task_type.name}] {task.description} (Prio: {task.priority})")

# 完成开发会话 (中文)
result = loop.run_session()
loop.save_session()
```

## 作为 CLI 使用

```bash
cd scripts
python -m devSoftAgent scan ~/projects
python -m devSoftAgent select
python -m devSoftAgent analyze /path/to/project
python -m devSoftAgent tasks /path/to/project
python -m devSoftAgent session --project my-project
python -m devSoftAgent status
```

## 命名规范（项目分类）

项目根据其文件夹名称进行分类：

| 前缀 | 标签 | 权重 | 含义 |
|------|------|------|------|
| `RDY` | Ready（已准备就绪） | 1.0 | 最高优先级 |
| `RDY_FAST` | Fast Ready | 0.5 | 快速完成 |
| `FAST` | Fast | 0.33 | 小型任务 |
| `DEV` | Development | 0.17 | 开发中 |
| `REL` | Released | 0.0 | 已发布，无需工作 |
| `ARC` | Archived | 0.0 | 已归档 |

权重决定了随机选择时的概率。

## TASKS.txt 格式

```markdown
# TASKS - 项目名称 (中文)
# 截至: 2026-03-12 (中文)

## OPEN
- [ ] [BUG] Bug 描述
- [ ] [FEATURE] 新功能

## IN PROGRESS
- [-] [REFACTOR] 代码重构

## DONE
- [x] [BUG] 已修复 Bug -- DONE 2026-03-01
```

## 质量策略 (Policies)

可自动针对代码进行检查的质量策略：

- **NamingPolicy：** 模块/函数使用 snake_case，类使用 PascalCase
- **EncodingPolicy：** 强制使用 UTF-8，检测 BOM，标记 CRLF
- **PathPolicy：** 检测并报告硬编码的绝对路径

## 变更日志

### 0.1.0 (2026-03-12)
- 从 MODULAR_AGENTS/devSoftAgent 迁移至 Skill 库
- 项目扫描器、任务引擎、代码分析器、DevLoop
- 3 个策略（命名、编码、路径）
- 3 个 Prompt 模板（任务、审查、分析）