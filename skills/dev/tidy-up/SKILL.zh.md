---
name: tidy-up
version: 1.1.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-08-19
updated: 2026-08-19
description: "对项目文件夹（包括子文件夹）执行一次性的任务求解、文档撰写和维护流程，即会话此前已在其中工作的那个文件夹——不做系统级全盘扫描。处理未完成的平凡/自主登记项，依据实测的现状更新文档（既在项目内，也在项目所在的流水线根目录中），并按\"回收站原则\"清理零散文件和临时文件。在以下情况使用此技能：/tidy-up、\"整理一下项目\"、\"在继续之前先收拾干净\"、项目工作会话结束时，或作为 /work-autonomous + /goal 内的到期自主任务。"
# Kompatibilitaet
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: dev
tags: [hygiene, maintenance, cleanup, documentation, tasksolver, writer, maintainer, autonomy, goal, work-autonomous, ticket-master]
language: zh
status: active
visibility: public

# Abhaengigkeiten
dependencies:
  tools: []
  services: []
  protocols: [work-autonomous, bilingual-doc-sync]
  python: []

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 27510ce60a4dd2defe9ee4686aeae6378ce8aea2f2376b98163d1d1340960233
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.906820+00:00"
---
<img src="banner.png" width="100%" alt="tidy-up banner">

# 整理（Tidy Up）— 针对当前项目文件夹的任务求解、撰写与维护流程

## 目的

在项目工作会话结束时，通常会留下一些零碎事项：已完成却从未勾选的待办项；仍显示旧状态而非实测状态的 README；一些已无人需要的测试文件。`tidy-up` 是一次**一次性、自我限定的流程**，正是针对**一个**项目文件夹补齐这些事项——即会话此前已在其中工作的那个文件夹。它不是持续循环，也不是系统级全盘扫描。

该流程由三个角色组成，模型依次自行承担：

1. **TASKSOLVER（任务求解）** — 解决项目登记中开放的、平凡/可自主完成的事项，或将其正确归档。
2. **WRITER（撰写）** — 将文档更新为实测的现状，既在项目内，也在项目所在流水线的根目录中。
3. **MAINTAINER（维护）** — 卫生性工作：按回收站原则收集零散文件/临时文件，维护登记/目录，并将遗留事项归档，而不只是在聊天中提及。

**在构建本技能之前的实测结果：** 截至 2026-08-19，本库中**不存在**名为 `tasksolver`/`writer`/`maintainer` 的独立技能或角色——既不作为技能名称，也未在其他技能中作为已记录的角色出现（全文搜索 `skills/**/SKILL.md`，除一个不相关的名称 `privat-mail-writer` 外无匹配）。因此，三个角色直接定义在下方各节中，而非由外部编排。若日后出现独立的 `tasksolver`/`writer`/`maintainer` 技能，`tidy-up` 将通过引用调用它们，而不是继续复制其逻辑（每次修改本技能时都需进行此项检查）。

## 范围 — 什么算作"当前项目文件夹"？

- 会话在本上下文中工作过的项目文件夹，**包括其所有子文件夹**。不跨入相邻项目，也不对整个流水线乃至 `.TOPICS/` 进行扫描。
- **一项明确的例外：** 文档/登记更新可额外涉及项目所在流水线的**根目录层级**（例如，在流水线级概览表中为该项目更新一行状态）——但仅限于涉及该项目的那一行/那一节，不得重新整理整个流水线根目录。
- 若"当前项目文件夹"不明确（例如会话在多个文件夹中工作），则取最接近的共同项目根目录（即 README/TODO/CLAUDE.md 所在之处）——拿不准时，宁可范围收窄，也不要过宽。

## 角色 1 — TASKSOLVER（任务求解）

目标：使项目登记（`TODO.md`/`AUFGABEN.txt` 或类似的本地约定）达到正确、最新的状态。

1. 定位项目登记（本地约定优先于新建文件——参见全局规则中的"遗留任务应归档，而不是仅提及"）。
2. 逐项评估每个开放事项：
   - **已完成**（例如已被刚结束的会话完成）→ 标记为已完成，或按照本地的已完成约定移入 `DONE.md`。
   - **平凡且可自主解决**（无需用户决定/批准/数据/硬件/会话，参见 `work-autonomous` 中的界限表）→ 现在解决，然后归档为已完成。
   - **非平凡或不可自主完成** → 不做改动，但保持其正确归档（若存在更合适的归档位置，则不要任其无声地停留——例如，某项早就应进入 `USER/*` 工单类别）。
3. 不得虚构新任务——`tidy-up` 只处理已有的遗留事项，不会制造新的议程。

## 角色 2 — WRITER（撰写）

目标：文档反映**实测**的现状，而非记忆中或期望中的状态。

1. 在项目内：将 README/CHANGELOG/状态行与实际的代码/文件夹情况进行核对（例如，所提及的文件是否仍然存在，所写的版本号是否正确，"进行中"标记是否早已完成）。
2. 在流水线根目录中：若那里存在登记/状态表格列出了该项目（例如 `.TOPICS/<Pipeline>/ROADMAP.md`、`STATUS.md`，或流水线 README 中的项目表），则仅更新对应**该项目**的那一行/那一节。
3. **绝不替换经过精选与维护的内容，只实测并更新。** 表格、变更日志或精心撰写的段落在形式和语气上保持不变——只修正事实（数字、状态、文件名、版本）。若不确定某一节是否经过精选与维护，宁可补充一条注释，也不要覆盖既有措辞。
4. 若局部更新即可满足需要，则不要从零重写。
5. **翻译补齐**（2026-08-19 补充，用户实时提出需求）：若项目缺少根据 **策略 P-006**（`.SYNC/_policies/library/P-006_sprachstufen.md`）在其层级下必须具备的语言版本，或现有版本明显过时，则由 WRITER 步骤予以补齐。P-006 简述如下：**核心集（DE+EN）为每个已发布的仓库/已编目对象的必备项**（仓库：`README.md` EN + `README_de.md`；技能：`SKILL.md` DE + `SKILL.en.md`）；完整集/全球集（ES/ZH/JA/RU，或再加 FR/HI/AR/BN/PT）是目标状态，但**逐步**补齐，不会由 `tidy-up` 在一次行动中完成。**工具：现有技能 `bilingual-doc-sync` 通过编排（调用）使用，其逻辑不会被复制**——它已涵盖"补齐缺失版本"、章节对等性检查及差异修正。`tidy-up` 仅为其提供触发信号（对当前项目文件夹，指明哪个对象、P-006 要求而缺失的哪种必备语言），而翻译质量、结构对等性和主语言规则仍由 `bilingual-doc-sync` 负责。**与 P-006 相同的限制：** 仅翻译到实测的现状，不虚构内容，使用真正的变音符号/元音变音，尊重仓库冷却期（上次提交后 <24 小时）及活动锁——若遇到这些情况，则保持该项未翻译，并将其作为开放事项归档（角色 3），而不是强行完成。

## 角色 3 — MAINTAINER（维护）

目标：进行卫生性维护，同时确保不丢失任何内容。

1. **收集零散文件/临时文件**（脚本残留、`*.tmp`、重复副本、遗忘的调试输出）——遵循回收站原则：移入本地 `_archive/` 文件夹（若不存在则创建，并在 `.gitignore` 中登记），**绝不直接删除**。对于来源或用途不明的文件：主动查明其用途（读取文件），而不是未读就清理——参见"外部改动事后认证"约定。
2. **登记/目录维护：** 若项目是更大型目录/注册表的一部分（技能注册表、模块清单、流水线概览），检查该项目的条目是否仍然准确——不要重建整个注册表，只处理这一条。
3. **将遗留事项归档，而不是在聊天中提及：** 本次流程结束时仍未解决的事项（无法自主完成的项目、已发现但未修复的缺陷、有意推迟的事项），按照"遗留任务应归档，而不是仅提及"规则进行归档——主要在本地发现处归档（项目的 TODO.md/AUFGABEN.txt 约定），否则集中归档（`ticket-master`/`TASKPLAN`），每项均附上背景（是什么、为何未完成、下一步）。
4. **尊重锁：** 每次修改前，检查项目文件夹中是否存在活动的 `LOCK.txt`/`LOCK.<scope>.txt`/`LOCK.user.*`。`LOCK.user.*` 会完全停止 `tidy-up` 对相关区域的操作——不得绕过，也不得对被锁定的区域进行部分整理。
5. **提交与推送仅依照各项目的仓库约定** — 在规划区与开发区分离的情况下，应在经授权的本地项目克隆中进行修改，而不是在规划副本或投影副本中进行。若项目如此规定，则自身修改依照全局约定"立即自行提交并推送"处理。

## 自我限定

`tidy-up` 是**一次流程，而非循环**。角色 3 完成后，本技能以简短摘要结束（已解决什么、已更新什么、已清理什么、已归档哪些遗留事项），并返回调用它的会话。若之后不久在同一项目中再次调用 `/tidy-up` 是允许的，但未必有意义——参见下方的到期判定标准。

## 与 work-autonomous 的关系

`tidy-up` 运行**计为 `work-autonomous` 第 1 层意义上可自主执行的任务**（正常、可见的工作——只要存在到期的 `tidy-up` 运行，就无需切换到代价高昂的第 2 层穷尽性检查）。实际含义是：若 `/work-autonomous` 与 `/tidy-up` 在 `/goal` 内一同使用，则只有当到期的 `tidy-up` 事项也已完成（前提是这些事项可自主执行，参见 `work-autonomous` 中的界限表）后，该目标才视为完成；需要用户决定的 `tidy-up` 事项，与任何其他依赖 `USER/*` 的任务一样，不计为自主完成。

**到期判定标准**（何时一次 `tidy-up` 运行"到期"？）：

1. 会话在本上下文中已在某一具体项目文件夹中工作（而非仅做研究/阅读且无任何修改——那样则无可整理之物）。
2. 自该项目上一次记录的 `tidy-up` 运行以来，冷却期已过（默认：每个项目每次会话结束运行 1 次——若自上次运行后没有新的修改，则同一会话内不得重复运行）。
3. 没有活动的 `LOCK.user.*` 阻塞该项目文件夹（参见角色 3，第 4 点）。

记录上一次运行（沿用 `work-autonomous` 中的防护模式，但有意更精简——`tidy-up` 不需要四步链条，只需为每个项目保存一个时间戳）：

```bash
usmc --agent <agent> note "tidy-up: project=<projekt-pfad-oder-slug> at=<ISO-Zeit> result=<done|nothing-to-do>" \
  --type context --priority 2 --tags "tidy-up-log,<projekt-slug>"
```

开始新运行前，读取当天记录（`usmc --agent <agent> working --limit 20`，按 `tidy-up-log,<projekt-slug>` 过滤），以检查判定标准第 2 条。

若存在某个 `/goal` 结构（若已存在或即将构建——`work-autonomous` 本身不调用 `/goal`，参见其中"有意不内置 `/goal`"一节），它对该到期判定标准的读取方式，与读取 `work-autonomous` 自身的终止信号相同：若某个 `tidy-up` 运行已到期且可自主执行，则目标尚未完成——无论 `work-autonomous` 自身的四步链条是否已报告"已耗尽"。

在 `work-autonomous` 技能本身中，与之对应的最小侵入式补充条目（第 1 层，新来源"当前项目到期的 tidy-up 运行"）是本次扩展的一部分——参见其中的变更日志条目。

## 相关技能

- **`work-autonomous`** — 见上文；`tidy-up` 是 `work-autonomous` 第 1 层处理的来源之一，并非其穷尽性检查的替代。
- **`bilingual-doc-sync`** — 由角色 2（WRITER）为翻译补齐进行编排（见该处），而非复制。`tidy-up` 仅决定根据 P-006 缺少什么，`bilingual-doc-sync` 决定如何翻译/同步。
- **`bugsweep`** — 带升级加倍机制的系统性缺陷搜寻。目的不同（查找缺陷，而非维护登记/文档/卫生）——若存在交叉（缺陷搜寻的发现进入登记），`tidy-up` 仅负责登记维护，不负责缺陷搜寻本身。
- **`dev-cycle`** — 新功能开发的 8 阶段框架。`tidy-up` 不是开发框架，而是在已完成工作之后进行的收尾/卫生流程。
- **`folder-flattening`** — 重组嵌套的文件夹层级。`tidy-up` 在既有结构内整理文件，不修改结构本身。

## 示例

```
User: "/tidy-up"
(Session hat gerade am autorisierten lokalen Checkout von `beispiel-projekt` gearbeitet)

→ TASKSOLVER: TODO.md gelesen — 2 Punkte bereits durch die Sitzung erledigt (nach DONE.md
  verschoben), 1 trivialer Punkt ("README-Tippfehler in Zeile 12") autonom geloest, 1 Punkt
  braucht Nutzerentscheidung (unveraendert stehen gelassen).
→ WRITER: README-Versionsangabe war 1.2.0, tatsaechlich 1.3.0 (package.json) — korrigiert.
  Pipeline-Root-Statustabelle: Zeile fuer "beispiel-projekt" von "in Arbeit" auf "aktiv" gesetzt.
→ MAINTAINER: 3 Debug-Skripte im Projektroot gefunden, nach _archive/ verschoben (Zweck geprueft:
  einmalige Testskripte, nicht mehr referenziert). Skill-Registry-Eintrag geprueft: stimmt.
  1 offener Punkt (Nutzerentscheidung) in AUFGABEN.txt belassen, dort bereits korrekt einsortiert.
→ USMC-Log geschrieben: tidy-up: project=beispiel-projekt at=2026-08-19T14:30 result=done
→ Zusammenfassung an Nutzer: 3 geloest, 2 Doku-Stellen aktualisiert, 3 Dateien archiviert, 1 Punkt
  offen (Nutzerentscheidung noetig).
```

```
Kombiniert mit /goal + /work-autonomous:

/goal "Projekt X fertigstellen" mit /work-autonomous + /tidy-up als Bedingungen
→ work-autonomous Ebene 1 findet: ACTIONABLE-Ticket erledigt, dann kein weiteres Ticket mehr,
  ABER tidy-up-Faelligkeitskriterium erfuellt (Session hat an Projekt X gearbeitet, kein
  protokollierter Lauf seit Sitzungsbeginn, kein LOCK.user aktiv) → tidy-up-Durchlauf ausgefuehrt.
→ Erst NACHDEM tidy-up "done" meldet UND work-autonomous Ebene 2 "exhausted" meldet, gilt das
  Goal als abgeschlossen.
```

## 变更日志

### 1.1.0 (2026-08-19)
- 根据工单 T-20260819-461890468 中实时补充的一项附加要求（用户原话："bis zu einer uebersetzung nachzuziehen die noch nicht existiert soll auch zum skill gehoeren"，即"在某个尚不存在的翻译被补齐之前，也应属于本技能"）进行的补充：角色 2（WRITER）新增第五点，依据**策略 P-006**（语言层级：核心集 DE+EN 为必备，完整/全球集逐步补齐）进行翻译补齐。工具为已存在的技能 `bilingual-doc-sync`——通过编排使用，而非复制。已补充 Frontmatter 依赖项及"相关技能"条目。

### 1.0.0 (2026-08-19)
- 源自工单 T-20260819-461890468 的初始版本。在全库全文搜索确认不存在独立的 `tasksolver`/`writer`/`maintainer` 技能之后（否则应编排而非复制），将三个角色（任务求解/撰写/维护）定义为本技能中的各节。范围限定为当前项目文件夹及流水线根目录状态行。目标集成：`tidy-up` 运行计为 `work-autonomous` 第 1 层来源，并配备独立的、精简的 USMC 到期记录（不同于 `work-autonomous` 本身的四步防护——对 `tidy-up` 而言结构过于简单）。已在 `work-autonomous` 1.3.0 中补充对应的最小侵入式条目（见其变更日志）。
