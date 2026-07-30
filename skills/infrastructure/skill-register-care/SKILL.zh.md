---
name: skill-register-care
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-07-30
description: >
  保持由三部分组成的技能注册表一致性的维护技能（包含 code-skill-index 分类目录、技能主索引、
  SKILL-MAP 技能族与路由映射图）。当需要在实际技能清单与已文档化的注册表之间进行偏差检查（Drift-Check）时使用：
  报告缺失或冗余条目、修正数量统计、更新日期。当收到 "维护技能注册表"、"更新索引"、"检查注册表偏差"、
  "MAP 中缺少哪些技能" 等指令时也会触发。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, register, index, drift, pflege, meta]
language: zh
status: active

dependencies:
  tools: []
  services: []
  protocols: [skill-explorer, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-register-care/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="skill-register-care banner">
# 技能注册表维护 (Skill-Register-Care)

## 目的

保持技能**注册表**无偏差。注册表由三个相互关联的工件组成 —— 切勿创建第四个注册表，始终在此三个工件的基础上进行扩充：

- `~/.claude/skills/code-skill-index/references/catalog-*.md`（分类目录文件）
- 技能索引 (Master-Liste)
- `<USER_HOME>\OneDrive\.USR\SKILL-MAP.md`（技能族与路由映射图）

## 偏差检查流程 (Drift-Check-Prozedur)

1. **获取实际状态：**
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
   仅 `source=user` 的技能与注册表相关（插件/第三方技能排除在外）。
2. **读取预期状态：** 读取上述三个注册表工件。
3. **对比计算差异：**
   - **缺失**（存在于清单中，不存在于注册表） → 补充登记。
   - **废弃**（存在于注册表中，不再存在于清单中） → 标记/删除。
   - **数量偏差**（例如 "18 个技能" 统计不符） → 修正数字。
4. **补充登记：** 为每个新技能在对应的 `catalog-<kategorie>.md` 中添加一行，在技能索引中添加一行（并更新页眉日期）；如果涉及新/修改的技能族，在 `SKILL-MAP.md` 中添加相应章节。
5. **更新日期：** 将所有被修改文件中的状态日期更新为当前日期。

## 辅助代码片段（列出缺失的用户技能）

```bash
PYTHONIOENCODING=utf-8 python -c "
import json
inv=json.load(open('<USER_HOME>/.skill-inventory.json',encoding='utf-8'))
print('\n'.join(s['dir'] for s in inv['skills'] if s['source']=='user'))
"
```
将输出结果与注册表工件进行比对（手动或通过 grep）。

## 铁律原则

- **切勿创建第四个注册表** —— 只能扩充现有的三个。
- 仅用户自制的技能归入注册表；第三方技能遵循外部路径。
- 切勿猜测日期 —— 必须设置为当前实际日期。

## 更新日志

### 0.1.0 (2026-06-17)
- 初始版本。由审计模式 (P2) 生成。触发原因：在 2026-06-17 的审计中，SKILL-MAP 中缺少了约 10 个用户技能（swarm-operations, model-strategy, agents-bridge, mcp-config-sync, system-onboarding, update-cli-docs, migrate-rename, plugin-system 以及心理咨询和游戏开发技能族）。
