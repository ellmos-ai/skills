---
name: sec-threat-model
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "基于实际源代码，为自有代码仓库创建或更新威胁模型（资产、信任边界、入口点、数据流、攻击者目标、按优先级排序的调查问题），输出为 threatmodel.md。适用于「威胁模型」「攻击面」「这个仓库应该先审查什么」、安全扫描之前，或架构变更之后。可独立运行，也可作为 sec-scan 的第 1 阶段；本身不查找漏洞（使用 sec-scan / sec-diff-scan），也不检查依赖公告（使用 security-tech-stack-check）。"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, threat-model, attack-surface, trust-boundaries, review]
language: zh
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-threat-model

ellmos 安全技能家族的第 1 阶段（`sec-threat-model`、`sec-scan`、`sec-diff-scan`、`sec-validate`、`sec-triage`、`sec-report`）。共享契约：`sec-scan/references/contract.md`（第 1 节 扫描目录，第 6 节 规则）。此处不重复。

## 规则

- 仅限自有代码或明确获得授权的代码（契约 6.1）。不访问第三方系统的网络，不做端口扫描。
- 模型建立在**已阅读的源代码**之上，而非 README 的说法。只有声称而无法证实的内容，一律作为 `open` 记入，绝不当作事实。
- 只写入扫描目录（`<tmp>/ellmos-security/<repo>/sec-scan-<scanId>/`），绝不写入源码树。写入之前按 `sec-scan` > 预检 所述检查锁。

## 流程

1. **明确范围：** 仓库、ref（提交 SHA 或 `working-tree`）、排除路径。读取现有的 `threatmodel.md`；若已存在，则切换为更新模式：只延续变更，并记录状态与 ref。
2. **阅读结构：** manifest、构建/部署文件、配置、目录树。从代码中推断语言与框架。
3. **找出入口点：** HTTP 路由、CLI 参数、队列/webhook 消费者、文件与格式解析器、IPC/套接字、定时任务、环境变量、插件/脚本加载点。每个入口点给出 file:line 与调用方群体（匿名、已认证、内部）。
4. **列出资产：** 密钥与令牌、个人数据、用户文件、数据库、算力、执行权限、声誉/供应链。给出其在代码中的位置，绝不写出值。
5. **划定信任边界：** 数据从低信任流向高信任之处（网络 -> 进程、用户 -> 管理员、租户 -> 租户、进程 -> 操作系统/shell/数据库、第三方包 -> 自有代码）。强制措施（认证/授权、校验、沙箱）在代码中的哪个位置，或者缺失。
6. **勾画数据流：** 针对最关键的资产与入口点，写出 source -> 转换 -> sink（文本或 Mermaid，要简短）。Sink：shell、SQL、文件系统、反序列化、模板、HTTP 客户端、日志。
7. **推导攻击者目标：** 针对每条边界，攻击者想要什么（代码执行、数据外泄、权限提升、篡改、服务中断）。STRIDE 仅作为思考辅助，不是必须套用的表格。
8. **为调查问题排优先级：** 具体、可检验的问题（「路由 X 中的 `user_id` 是否未经检查就到达了 `db.py` 里的查询？」），按影响乘以可达性排序。`sec-scan` 会把它们转化为调查包。

## 产出：`threatmodel.md`

各节按以下顺序：**状态**（仓库、ref、日期、已读路径）· **资产** · **信任边界** · **入口点**（表格：路径、类型、调用方、认证）· **数据流** · **攻击者目标** · **调查问题**（编号、按优先级排序）· **待定**（假设、未读区域、文档与代码之间的矛盾）。不含密钥值，不含利用说明。

## 范围限制

不发现漏洞，也不指定严重度。`open` 条目很多的模型，比一个看似平滑的模型更诚实。

## 变更日志

### 0.1.0 (2026-10-31)

- 首个版本，作为安全家族的第 1 阶段。
