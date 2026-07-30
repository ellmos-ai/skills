---
name: letter-hooker
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: >
  为缺少原生事件驱动型 JSON 生命周期钩子（如 Antigravity / Gemini CLI）的 AI Agent
  和 CLI 扩展 automation-self-care，提供 Letter Hooks、Preflight Bootloader、文档遍历规则以及自愈式
  Prompt 上下文增强功能。当 Agent 需要注入预检规则、在开始工作前查询 memory/gardener、强制执行目录文档读取策略（CLAUDE.md / AGENTS.md），或将 sidecar 任务动态路由至 Skill 和安全协议时使用。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [automation, letter-hooker, letter-hooks, bootloader, prompt-enrichment, self-care, governance]
language: zh
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: [agy_kontext_and_workflow_loader.py]
provenance:
  origin: "fork of automation-self-care"
  origin_path: "skills/infrastructure/automation-self-care"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/skills"
---

> **中文** — `letter-hooker` 官方中文版本。

# Letter-Hooker（Prompt 级预检与治理引擎）

**Letter-Hooker** Skill 为缺乏原生事件驱动型 JSON 生命周期钩子加载器（例如 `~/.claude/settings.json` 或 `~/.codex/hooks.json`）的 AI Agent 框架（如 **Antigravity / Gemini CLI**）扩展了 `automation-self-care`。

`letter-hooker` 并非依赖按键触发的被动式钩子，而是通过定时任务和维护脚本（`agy_kontext_and_workflow_loader.py`）运行**主动的 Prompt 级预检 Bootloader 与 Letter-Hook 注入循环**。

---

## 核心功能

1. **预检 Bootloader 与文档遍历规则**：
   - **向上与向下搜索**：对 Agent 执行严格指令，检查当前工作目录层级的 `AGENTS.md`、`CLAUDE.md`、`START.md`、`RULES.md` 及 `README.md`。若缺失，则向上遍历直至找到，随后向下检查。
   - **Memory 与 Gardener 预检**：在执行破坏性或复杂修改前，必须向 `gardener` 和 `memoryhooker` 发起预检查询。

2. **Letter Hooks 目录与参考链接**：
   - 模块化 `.md` 指令文件，存储于 `OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/` 下。
   - 将显式的 `file://` 链接直接注入 `sidecar.json` 提示词文本中，以便 Agent 在调用时读取精确的安全与工作流协议。

3. **每日关键词列表与自愈式 Prompt 增强**：
   - 从活动/备用任务中维护每日 `STICHWORTLISTE.json`。
   - 分析执行日志（`AUTOMATIONS-MEMORY.md`）中的失败模式（缺少上下文、缺少工作流指导、无效路径），并动态修补任务 Prompt。

4. **Skill 与 Persona 路由**：
   - 检查任务关键词并将其映射到相应的 `.SKILLS`（例如 `infrastructure/condition`、`semantic-persona-routing`、`orchestrator`、`think`、`decide`）。

---

## 核心 Letter Hooks

- **`HOOK-DOC-TRAVERSAL-01`**: [bootloader_doc_traversal.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/bootloader_doc_traversal.md)
- **`HOOK-GARDENER-MEMORY-01`**: [preflight_gardener_query.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/preflight_gardener_query.md)
- **`HOOK-WORKFLOW-HYGIENE-01`**: [workflow_lock_and_git_hygiene.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/workflow_lock_and_git_hygiene.md)
- **`HOOK-PATH-VALIDATION-01`**: [path_validation_and_authority.md](file:///<USER_HOME>/OneDrive/.SYNC/antigravity_kontext_and_workflow_loader_package/letter_hooks/path_validation_and_authority.md)

---

## 工作流集成

```bash
# Execute the Letter-Hooker Maintenance Engine
python OneDrive/.SYNC/scripts/agy_kontext_and_workflow_loader.py
```

1. **扫描 Sidecar**：读取 `~/.gemini/config/sidecars/` 中的所有 `sidecar.json` Prompt 文本。
2. **更新关键词列表**：提取领域术语并保存至 `.SYNC/STICHWORTLISTE.json`。
3. **注入 Letter Hooks**：在 Prompt 中追加 Bootloader 规则和 `file://` 参考链接。
4. **记录结果**：将更新记录至 `ANTIGRAVITY-LOG.txt` 与 `ANTIGRAVITY-REGISTRY.md`。