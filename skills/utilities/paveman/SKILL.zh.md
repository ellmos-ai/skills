---
name: paveman
version: 1.0.1
type: skill
author: Lukas Geiger + Claude
created: 2026-08-19
updated: 2026-08-20
description: "识别用于精简规则或记忆文件的请求（\"精简我的 CLAUDE.md\"、\"MEMORY.md 太长了\"、\"压缩文档，但不改动技术内容\"、\"这个规则文件被字符上限截断了\"），并为此使用 paveman 模块——一个确定性、无模型的 CLI 工具，用于精简 Markdown/文本文件中的散文，默认试运行，支持回滚，并带有对路径、标题和代码的严格保护校验器。当出现类似\"精简 <Datei>\"、\"这个文件太长/被截断了\"、\"shrink this rule file\"、\"压缩但不改变内容\"的表述，或规则/记忆文件明显触及字符或行数上限时，请使用此技能。"
# Kompatibilität
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: utilities
tags: [kürzen, kompression, regeldatei, gedächtnis, deterministisch, dry-run, rollback, dokumentation]
language: zh
status: active
visibility: public

# Abhängigkeiten
dependencies:
  tools: [paveman]
  services: []
  protocols: []
  python: []
  modules: [paveman]

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: cb1c7bfcbc7a4592a1df4a844c4e3d2a5f5da3f268d81b246c0ce05024927bc1
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="paveman banner">

# Paveman — 确定性精简规则与记忆文件

> 围绕单独提供的模块 `paveman` 的轻量、与用户无关的技能包装器。
> 该技能判断何时适合使用该工具，并说明其安全流程。它不假定特定计算机、固定安装路径或个人配置。

## 何时触发此技能

触发条件是用户希望精简**现有的规则、约定或记忆文件**，同时不改变其专业内容：

- "精简 `<Datei>`" / "这个文件太长" / "在 X 个字符或行处被截断"
- "压缩文档，但不要改动技术内容或代码"
- "MEMORY.md 或 CLAUDE.md 变得太长了"
- "让这个规则文件更简洁，但保持含义不变"
- 任何表示**精简现有文件**的变体，而非**新写内容**或**翻译**（见下方区分）

**不属于**此技能的情况：

- **`knappform`** —— 改变模型在当前对话中自身的表达方式（LLM 通信风格，基于模型，无文件访问）。`paveman` 则在不调用模型的情况下，确定性地改变现有文件的内容。两者可以并存；在技术和功能上彼此独立。
- **`bilingual-doc-sync`** —— 补充缺失的语言版本。`paveman` 精简一个版本，不做任何翻译。
- **`llm-text-hygiene`** —— 删除文本中的 AI 痕迹或聊天残留。其目的与精简不同。
- 撰写或编造新内容 —— `paveman` 只精简已有内容。

## 模块能做什么

`paveman` 是一个基于规则、确定性的 Markdown 和文本散文精简器：不调用模型，不消耗 token，不发送网络请求。各系统的部署方式可能不同；以该系统授权的模块或软件包版本为准。

| 参数 | 作用 |
|---|---|
| *(无参数)* | **试运行（默认）。** 显示差异和节省的字符数，不写入任何内容。 |
| `--apply` | 实际写入；写入前自动创建备份。 |
| `--rollback` | 恢复最近一次备份。 |
| `--locker` | 将路径或标题偏差仅报告为警告，而非错误。 |
| `--kontext N` | 设置差异的上下文行数。 |

**保护校验器在每次调用时都会运行。** 代码块、路径和标题不得被修改。在默认模式下，偏差会阻止写入，而不仅仅是报告。

## 流程 —— 始终按此顺序执行

1. **先试运行。** 不带 `--apply` 运行 `paveman <Datei>`。向用户展示节省的字符数、差异以及校验器状态（"OK"或具体错误信息）。
2. **仅在用户明确批准后写入。** 然后才运行 `paveman <Datei> --apply`；绝不要从试运行自动切换到写入模式。
3. **写入前说明 `--rollback`。** 让用户事先知道如何撤销不理想的结果。
4. **认真对待校验器错误。** 不要仅为绕过错误而使用 `--locker`。先确认偏差确实无害；较宽松的模式需要用户的明确决定。
5. **尊重已精心编排的内容。** 基于规则的工具无法可靠判断某个表述是否有意写得详细。如有疑问，请仔细检查试运行的差异。

## 前提条件 —— 检查模块可用性

1. 使用 `paveman --help` 检查该 CLI 在当前环境中是否可用。
2. 若命令缺失，找到为该系统授权的模块或软件包获取途径。不要编造本地路径结构、软件包名称或代码仓库。
3. 若无法解析出任何已授权的来源，应将缺失的前提条件作为单独的设置步骤报告，而不是盲目执行该技能或创建并行模块。
4. 安装后，先重新运行 `paveman --help`，然后执行一次无害的试运行；真正的写入测试仍需获得批准。

## 示例

```text
User: „Kürze meine CLAUDE.md, sie wird beim Sessionstart abgeschnitten.“

→ `paveman CLAUDE.md` (Trockenlauf)
→ Ergebnis: „12.400 → 9.800 Zeichen (-21 %), Validator: OK.“
→ Diff zeigen und auf `--rollback` hinweisen.
→ Nutzer bestätigt.
→ `paveman CLAUDE.md --apply`
```

```text
User: „MEMORY.md ist zu voll, kürze sie bitte.“

→ Trockenlauf: „893 → 893 Zeichen, keine Regel griff — der Text ist bereits knapp.“
→ Kein `--apply` empfehlen; den fehlenden Mehrwert ehrlich melden.
```


## 更新日志

### 1.0.1 (2026-08-20)

- 彻底将公开包装器与计算机名称、本地检出路径、安装数据、私有工单引用和本地测试结果解耦。
- 新增与用户无关的可用性和安装约定，并修正为正确的德语变音符号。

### 1.0.0 (2026-08-19)

- 包装器的首个公开版本，包含试运行、批准步骤、回滚和校验器边界。
- 明确与 `knappform`、`bilingual-doc-sync` 和 `llm-text-hygiene` 的区别。
