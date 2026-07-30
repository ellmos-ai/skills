---
name: skill-family-care
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-07-30
description: >
  保持技能族（Skill Families）最新状态的维护技能，无需运行完整的 skill-explorer 审计。
  当需要将新技能归类到正确的技能族、在技能族变更后更新页眉路由块，或删除废弃的路由块时使用此技能。
  当收到 "维护技能族"、"将新技能分配到技能族"、"更新路由"、"设置/删除技能族页眉" 等指令时也会触发。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, familien, pflege, routing, meta]
language: zh
status: active

dependencies:
  tools: []
  services: []
  protocols: [skill-explorer, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-family-care/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="skill-family-care banner">
# 技能族维护 (Skill-Family-Care)

## 目的

保持技能**族**（Families）处于最新状态 —— 无需运行 `skill-explorer` 的完整审计流程。按照安装器原则（精简的子技能而非庞大的单体）独立拆分。直接引用 `skill-explorer` 的脚本，不进行重复复制。

## 规范数据源（请勿重复创建）

- **技能族列表：** `<USER_HOME>\OneDrive\.USR\SKILL-MAP.md`（权威的技能族/路由映射图）。
- **技能清单（当前状态）：** `skill-explorer/scripts/inventory_skills.py`。
- **设置/删除路由：** `skill-explorer/scripts/inject_family_header.py`。
- **配置（已链接的技能族）：** `~/.claude/skills/skill-explorer/config.json`。

## 任务事项

### A — 将新技能归类到技能族
1. 重新生成技能清单：
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
2. 从 `SKILL-MAP.md` 中选择匹配的技能族（维度：阶段/宽度/刚性/影响/原料）。
3. 在 `config.json`（`families[<fam>].members`）及 `SKILL-MAP.md` 中将该技能登记为成员。

### B — 技能族变更后更新页眉路由
```bash
PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inject_family_header.py \
    --family <Familie> --skills s1,s2,s3 --router "<Wegweiser>" --inventory ~/.skill-inventory.json
```
- 幂等操作：若已存在同一技能族的路由块，将被直接替换。
- 仅修改 `editable`/`source=user` 类型的技能（脚本内部的安全关卡）。

### C — 删除废弃的路由块
使用相同脚本并附加 `--remove` 参数（无需指定 `--router`）。

## 铁律原则

- **审查 ≠ 修改 (Survey ≠ Mutation)：** 仅用户自有的技能可以注入页眉。切勿修改插件或外部技能。
- 每次修改后，必须更新 `config.json`（`families[*].linked`, `updated`）。
- 切勿将技能族映射图中的具体内容复制到单个技能中 —— 仅注入指引路由块。

## 更新日志

### 0.1.0 (2026-06-17)
- 初始版本。由审计模式 (P1) 生成。
