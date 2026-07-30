---
name: law-checker
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-07-23
updated: 2026-07-23
description: 指向独立模块 law-checker（“法律部门”）：基于源数据的德国法律 AI 初步法律评估，配备法规注册表和法规实体化智能体。当需要根据德国法律对某种情况、合同、官方通知或法律问题进行精确引用（条/款、项、句）的核查时使用此技能——具有明确的界限：AI 辅助的初步方向引导，不能替代执业律师。
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance: {'origin': 'external', 'origin_repo': 'https://github.com/ellmos-ai/law-checker', 'origin_path': 'SKILL.md, config.json, agents/gesetzbuch.md, references/', 'origin_version': None, 'last_sync_from_origin': '2026-07-23', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
category: utilities
tags: [legal, law, germany, wrapper, pointer-skill]
language: zh
status: active
---

> **中文** — `law-checker` 官方中文版本。

# law-checker（法律部门）-- 指针技能

此技能是一个**轻量级指针（封装/wrapper）**，指向独立的公共模块仓库 [`ellmos-ai/law-checker`](https://github.com/ellmos-ai/law-checker)（MIT 许可证，公开）。实际技能托管在那里——本仓库仅链接到它并记录安装说明，以便可以通过中央技能目录找到该模块。

## 模块功能

`law-checker` 为德国法律提供基于权威源数据的 AI 初步法律评估：

- **法规注册表 (`config.json`)：** 可切换的法规；每个法律主张都必须由本地获取的官方法律文本支持（在需要时提供条/款、项、句、简短引用、来源、获取日期）。
- **法规实体化智能体 (`agents/gesetzbuch.md`)：** 一个通用智能体，针对任何已注册的法律“从法律条文内部”进行回答——可扩展到添加到注册表中的任意法规。
- **独立的判例法层：** 法院判决仅在经过网络验证后才会被引用（法院、日期、案号，在可用时提供 ECLI）。
- **风险与升级工作流：** 带有风险等级标注、期限纪律和律师专业分流矩阵的报告格式。

## 界限（重要）

- **仅限 AI 辅助的初步方向引导，不能替代个人的法律咨询，也不是由执业律师提供。**
- 不是律所，不是托管的法律服务，也不是截止日期日历。
- 如果涉及真实的法律信函（警告信、官方通知、诉讼、截止日期）：请妥善保管原始文件，记录截止日期，并咨询有资质的律师——切勿将此事自动化处理。

## 安装（通用，无本地路径）

1. 克隆模块：
   ```bash
   git clone https://github.com/ellmos-ai/law-checker.git <clone-path>
   ```
2. 将 `<clone-path>/SKILL.md` 采纳到您自己的技能环境中（例如 `~/.claude/skills/law-checker/` 或智能体运行时的等效位置）。
3. 将采纳的 `SKILL.md` 及其引用中的模块路径设置为 `<clone-path>` ——请勿将真实本地路径或主机名提交到版本化的技能环境中。
4. 加载法规注册表：`python <clone-path>/_tools/gesetze_fetch.py`（获取配置的官方法规文本；文本本身故意未在仓库中提供，以避免重新分发陈旧的门户快照）。
5. 有关结构、许可证和责任详情，请参阅模块仓库的 README。

## 此指针技能的来源

此封装于 2026-07-23 作为 `ellmos-ai/skills` 仓库的展示条目添加。不存在**代码重复**——维护和版本控制仅保留在 `ellmos-ai/law-checker` 模块仓库中。

## 变更日志

### 0.1.0 (2026-07-23)
- `ellmos-ai/law-checker` 的初始指针技能。
