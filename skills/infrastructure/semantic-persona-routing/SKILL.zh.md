---
name: semantic-persona-routing
version: 1.0.0
type: skill
author: Lukas Geiger + OpenAI
created: 2026-07-28
updated: 2026-07-28
description: >
  基于 Persona（人设）、协调 Role（角色）、Expert（专家）与实时 Skill 终点，构建并使用供应商中立的语义路由图。当 LLM 需要将请求通过 Boss 角色路由至专家再到 Skill、从现有 Agent 系统提取便携式 Persona 路由器、将语义领域图与词法 Skill 注册表相结合，或显式暴露缺失的角色到 Skill 端口（而非静默降级）时使用。触发词包括语义 Persona 路由、Persona 伞形架构、角色路由器、Boss Agent 专家 Skill 路由、Agent 角色导出或使 Persona 跨 LLM 供应商复用的请求。
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [persona, semantic-routing, agents, experts, skills, umbrella, provider-neutral]
language: zh
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

> **中文** — `semantic-persona-routing` 官方中文版本。

# 语义 Persona 路由 (Semantic Persona Routing)

优先按能力路由，其次应用个性人设。构建一个便携式映射图，将语义角色选择、确定性终点查找与供应商特定加载保持分离。

## 路由模型 (Routing model)

```text
request
  -> semantic domain/coordinator role
  -> expert capability
  -> explicit or live-resolved skill endpoint
  -> optional persona overlay
  -> provider adapter loads and executes
```

Persona（人设）控制沟通风格、优先级与交互模式。它不赋予工具、权限或领域专业能力。Role（角色）负责协调；Expert（专家）收窄领域；Skill（技能）则是可执行的终点。

## 构建路由映射图 (Build the routing map)

使用显式元数据作为权威依据，词法相似性仅作为候选参考：

```bash
python scripts/build_routing_map.py \
  --roles-dir path/to/roles \
  --personas-dir path/to/personas \
  --skills-dir path/to/skills \
  --out routing-map.json
```

构建器可以理解常见的 `SKILL.md` 字段，例如 `type`、`orchestrates.experts`、`parent_agents`、`skills`、描述信息与出处（provenance）。它能够在无需安装源系统的情况下生成运行时映射图。在扩展格式之前，请先阅读 [routing-map-schema.md](references/routing-map-schema.md)。

切勿自动提升 `candidate_skills`。请先通过实时 Skill 解析器或源元数据对其进行确认。

## 路由请求 (Route a request)

### 1. 语义化选择协调角色 (Select the coordinator role semantically)

将请求与角色名称、描述和使用场景进行比较。优先选择能够协调整个请求的最精准角色。当置信度较低时，保持多个候选角色可见；仅当选择会实质性改变结果时才询问用户。

### 2. 在角色内选择专家 (Select an expert within the role)

除非请求明显跨越多个角色，否则仅使用与所选协调角色关联的专家。直接的专家请求在执行时可以跳过协调角色，但在路由解释中应保留协调角色的链接。

### 3. 解析可执行终点 (Resolve executable endpoints)

按以下顺序解析：

1. 来自显式源元数据或精确出处（provenance）的 `endpoint_skills`；
2. 当前的外部 Skill 解析器或本地 Skill 查找器；
3. 已验证的 `candidate_skills`；
4. 当终点不存在时显示 `GAP`。

切勿将专家名称当成已安装的 Skill 进行路由。缺失终点属于迁移缺口（porting gap），并不意味着可以凭空虚构终点。

在连接实时注册表、词法查找器或供应商特定 Skill 加载器时，请阅读 [endpoint-resolution.md](references/endpoint-resolution.md)。

### 4. 应用 Persona 叠加层 (Apply the persona overlay)

选择附加到所选角色或专家的 Persona。如果有多个 Persona 匹配，优先选择声明的限制和风格与任务相符的那一个。当没有显式连接的 Persona 时，不应用任何 Persona。

Persona 指令不能覆盖安全规则、锁定、用户决策、专业边界或工具权限。

### 5. 加载与执行 (Load and execute)

使用供应商的原生 Skill/Agent 加载机制。在执行前加载所选的实时 Skill 指令。保持路由器精简；执行工作归属于加载了已解析 Skill 的 Worker 或当前 Agent。

## 路由回执 (Route receipt)

返回或记录以下内容：

```text
ROLE: <coordinator or direct>
EXPERT: <expert or n/a>
SKILLS: <verified live endpoints>
PERSONA: <overlay or none>
RESOLUTION: explicit | provenance | live-resolver | verified-candidate | GAP
CONFIDENCE: high | medium | low
WHY: <one short reason>
GAPS: <missing endpoints or stale-map warnings>
```

当源角色或 Skill 清单发生变化时，需重新构建映射图。在终点可用性方面，实时解析器可以替换陈旧的映射图，但绝不能静默重写语义角色分类体系。

## 示例 (Example)

请求："整理我的收据并准备财年概览。"

路由器首先选择办公协调角色，接着选择税务专家，解析出已安装的税务 Skill，最后应用显式关联的细致税务 Persona。如果税务专家存在但未安装可移植的税务 Skill，则报告 `GAP` 并仅通过显式配置的回退方案继续执行。

## 更新日志 (Changelog)

### 1.0.0 (2026-07-28)

- 从经实证的领域路由器模式中提取了供应商中立的角色/专家/Skill 链，并添加了具备显式终点缺口的可移植映射图生成功能。