---
name: decision-shot
version: 1.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-24
updated: 2026-09-18
description: "极简、实质性的输出格式，用于一个决策或决策组，当其背后的分析已经存在（来自聊天、来自`decide`、来自`decision-briefing`、来自工单或文档）时：2-3行背景，每个选项的利弊以精简风格的要点列出，谈话要点，一个有理有据的建议，以及指向完整分析的路径/链接以供完整阅读。当“给我简短版本，带利弊和建议”、“决策的执行摘要”、“关于<Thema>的简短背景”、“用简短形式总结决策X”、/decision-shot，或当结果要交给只需要要点而非完整推导的人时，使用此技能。不要用于汇总多个未决决策并按字母逐一询问——那是decision-briefing的工作；不要用于先对决策进行分析——那是decide的工作。decision-shot以已完成的分析为前提，只压缩其呈现方式。"
visibility: public
language: zh
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: utilities
tags: [entscheidung, executive-summary, kurzform, pro-contra, talking-points, empfehlung]
status: active

dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, knappform, paveman]

provenance:
  origin: "custom"
  decision_ref: "T-20260824-673115956 (Ticket-Master, User-Auftrag 2026-08-24)"
translated_from_sha256: 26ff135e844d526543d9f5df212d36e408a427a71cc13a9e744a55abdb5ed991
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.035916+00:00"
---
<img src="banner.png" width="100%" alt="decision-shot banner">

# decision-shot

> 分析已经完成。现在需要的不是第二次推导，而是精华，以及回到完整内容的路径。

## 何时使用

- 某个决策（或紧密相关的一组决策，例如同一主题下的多个子问题）已经过充分思考——在聊天中、在工单中、通过`decide`框架，或在`decision-briefing`的第2阶段——现在需要在几秒钟内交给某人（用户、另一个代理、交接文档）。
- 触发词：“带利弊的简短版本”、“执行摘要”、“简短背景”、“关于此的谈话要点”、“给我压缩版并附建议”、`/decision-shot`。
- **不要**用于仍有多个未决、未定的问题、需要用户按批次逐个用字母回答的情况——那是[decision-briefing](../decision-briefing/SKILL.md)。**不要**用于仍需先推敲决策的情况——那是[decide](../decide/SKILL.md)。decision-shot纯粹是对已有分析的呈现。

## 区别（简要）

| 技能 | 作用 | 何时完成 |
|---|---|---|
| `decide` | 用框架（利弊矩阵、加权评分、决策树……）推敲一个决策 | 分析尚未完成 |
| `decision-briefing` | 收集某主题下的多个未决决策，以A/B/C/D批次呈现，接收字母回答 | 多个问题仍未定 |
| `decision-shot` | 将一份已完成的分析（无论来源）压缩为带完整版链接的执行式简短版 | 分析已存在，只缺呈现 |
| `knappform` | 适用于会话中每一条回复的通用回答风格修饰符 | 会话范围内，与主题无关 |
| `paveman` | 确定性地压缩现有的散文文件（规则/记忆文件） | 压缩文件，而非聊天输出 |

`decision-shot`与上述四者都不冲突——它是在`decide`之后或与`decision-briefing`并行使用的格式，一旦需要传递精华就会用到。精简的语言风格参照`knappform`/`paveman`（完整删除清单见那里），但在此会一致地应用于固定的五部分格式。

## 格式（强制，五部分）

```
## <Entscheidungstitel>

**Kontext:** <2-3 Zeilen -- worum es geht, warum jetzt, was auf dem Spiel steht>

**<Option A>**
+ <staerkstes Pro-Argument>
+ <zweites Pro-Argument, nur falls es traegt>
- <staerkstes Contra-Argument>

**<Option B>**
+ <Pro>
- <Contra>
- <Contra>

**Talking Points:**
- <Punkt, der im Gespraech/in einer Mail sofort zieht>
- <Punkt, der einen typischen Einwand vorwegnimmt>

**Empfehlung:** <Option> -- <ein Satz Begruendung, keine Wiederholung der Pro-Liste>

**Vollanalyse:** <Pfad oder Link -- Ticket-Datei, Dokument, Chat-Referenz>
```

## 规则

- **面向用户的文本不含技术编号/缩写（口语化的第一人称）：** 对人可见的文本（标题、背景、选项、谈话要点、建议）中**不得**出现内部缩写、工单编号（`T-...`）、D编号或相对文件路径。背景应以第一人称描述情况和计划行动（“我建议……”）。技术引用（工单ID、精确文件路径）只能出现在结尾的`**Vollanalyse:**`行或参考表格中。
- **行数是预算，而非目标。** 2-3行背景，每个选项2-4个要点，2-3条谈话要点，1句建议——超出的部分会被删除，而不是压缩后仍然保留。如果某个选项放不进4个要点，它就不属于此技能，而应放入完整分析。
- **与`knappform`/`paveman`相同的精简风格：** 无填充词、无客套话、不回避。否定词（`nicht`、`nie`、`kein`、`nur`、`außer`）保持不变——删去它们会颠倒含义。
- **利弊是要点，不是句子。** 以`+`/`-`作为前缀，每行一个观点，不加附注。
- **谈话要点是沟通性的，不是分析性的。** 它们回答的是“如果有人问我，我该说什么”——而不是“分析里写了什么”。与利弊列表重复，说明尚未凝练。
- **建议用一句话自证理由。** 不重复利弊列表，不写“见上文”——这一句话在没有该块其余内容的情况下也必须成立。
- **指向完整分析的链接/路径是必填项，而非可选。** decision-shot不取代分析，它只是让分析更容易快速找到。如果没有可用的具体来源（仅在聊天中口头形成，没有文档），请尽可能具体地说明聊天/会话的出处（例如“本次会话，对F4的回答”），而不是留空。
- **多个相关决策**（一组，例如某主题下的多个子问题）：每个决策一个块，用`---`分隔，只有在确实适用于所有决策时，共同背景才只在开头写一次。

### 保存的decision-shot中的会话溯源

若decision-shot作为重要的新持久工件被保存，文件以以下内容结尾：

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

会话ID首先取自明确的运行时/CLI参数，其次取自权威的提供方环境或钩子；若两者都缺失，则填写`unbekannt`。切勿猜测数值。子代理使用父会话。常规聊天、来源、策略、`CLAUDE.md`、README和旧文件不会被一律加盖或补加标记。

## 示例

```
## Wo laeuft der naechtliche Backup-Job?

**Kontext:** Ich beobachte wiederholte Ausfälle auf dem Laptop, weil das Gerät nachts
schläft. Ich schlage vor, den Job auf den Mac Studio umzuziehen, der rund um die Uhr läuft.

**Laptop (Status quo)**
+ Keine Netzwerkabhaengigkeit
- Job faellt regelmaessig aus, wenn das Geraet schlaeft
- Kein zentraler Log-Ueberblick

**Mac Studio**
+ Laeuft 24/7, keine Ausfaelle durch Schlafmodus
+ Zentrale Logs an einem Ort
- Braucht funktionierendes Tailscale/SSH als Voraussetzung

**Talking Points:**
- "Der Ausfall ist kein Bug im Skript, sondern eine Standortfrage."
- "Tailscale laeuft schon fuer andere Jobs stabil -- kein neues Risiko."

**Empfehlung:** Mac Studio -- einzige Option ohne den bekannten Schlafmodus-
Ausfall, und die Abhaengigkeit (Tailscale) ist bereits im Betrieb bewaehrt.

**Vollanalyse:** `.SYNC/MAC_STUDIO_COMPUTE_HANDOFF.md`, Abschnitt "Backup-Jobs" (Ticket T-20260620-42)
```

## 变更日志

### 1.2.0 (2026-09-18)
- 为易懂的决策文本确立风格规则（T-20260913-883789445，用户指示2026-09-13）：
  - 可见文本（标题、背景、谈话要点）中不出现工单编号、D编号或内部路径。
  - 背景和建议以自然的口语化第一人称书写。
  - 技术性的工单和路径引用严格限定在结尾的完整分析行中。

### 1.1.0 (2026-09-09)
- P-018为重要的新保存decision-shot增加会话标记，并设定了狭窄的来源优先级和排除项。

### 1.0.0 (2026-08-24)
- 初始版本。
