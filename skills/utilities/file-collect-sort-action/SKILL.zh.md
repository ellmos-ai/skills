---
name: file-collect-sort-action
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-18
updated: 2026-08-18
description: "识别形如\"从某个文件夹中始终获取特定文件并将其收集到某个目标位置\"的用户请求，并为此设置模块 file-collect-sort-action（CLI fcsa）——一个由配置驱动的代理，可扫描文件夹、按模板对文件分类，并应用分级操作（move/copy/duplicate-check/delete/OCR/place-information）。当出现诸如\"从<Ordner>中始终获取<Dateiart>并将它们收集到<Ziel>\"、\"自动按……整理文件夹X\"、\"将来自……的传入文件收集到……\"、\"按规则清理此文件夹\"或\"自动将……中的所有<Dateiart>移动到<Ordner>\"之类的表述时，使用此技能。始终先设置试运行（Dry-Run），仅在用户明确确认\"开始执行\"后才正式启用；删除操作原则上保持在_trash模式。"
# Kompatibilitaet
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: utilities
tags: [dateien, sortierung, automatisierung, config-driven, ordner-ueberwachung, duplikate, ocr]
language: zh
status: active
visibility: public

# Abhaengigkeiten
dependencies:
  tools: [fcsa]
  services: []
  protocols: []
  python: []
  modules: [file-collect-sort-action]

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 844e8b0e6411e463278a6084440cd4915bf241f8ab5a036d1fa25913e18c681f
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T12:34:17.266862+00:00"
---
<img src="banner.png" width="100%" alt="file-collect-sort-action banner">

# File Collect Sort Action

> 用户有意将此模块暂时搁置，直到出现具体任务需要它为止
> （工单 T-20260818-916568570，用户原话："我以后某天会说从那个文件夹里始终获取某些文件并把它们收集到那里——然后你就识别出这个技能属于我们的模块，并进行设置"）。本技能正是其所等待的识别机制。

## 何时启用此技能

触发语句是描述**按规则持续收集**的用户表述，而非一次性的"把这个文件移走"：

- "从`<Ordner>`中始终获取`<Dateiart>`并将它们收集到`<Ziel>`"
- "自动按`<Kriterium>`整理文件夹`<X>`"
- "将来自`<Quelle>`的传入文件收集到`<Ziel>`"
- "按规则清理此文件夹" / "自动将`<Ordner>`中的所有`<Dateiart>`移走"
- 任何同时指明**来源**、**识别特征**（文件类型/命名模式/内容）和**目标**，并暗示该操作需要**重复**进行（而非只做一次）的变体

**不属于**本技能的情况：仅移动单个一次性文件（代理可直接完成，无需配置层）；`dokument-ingest`（回答的是"用什么读取*内容*"，而非"*文件*应放到哪里"）；不移动文件的增量文本索引（`gardener`）。

## 模块功能（简述）

`file-collect-sort-action`（简称 **f-csa**，CLI 为 **`fcsa`**）是一个由配置驱动的"扫描→分类→执行"代理，包含三个配置文件和一个处理记忆：

| 文件 | 作用 |
|---|---|
| `config.json` | `scan_paths`（正向列表）、格式包含/排除、重复检测规则、安全闸门（`allow_hard_delete`） |
| `categories-definitions.json` | 各类别的识别模板（文件名/扩展名/内容）、检查项/闸门、`default_target`、`default_actions` + `default_stepping` |
| `action-rules.json` | 各类别的操作参数（move/copy 目标、重复模式、删除模式、OCR 后端、放置顺序） |
| `processing-csa.json` | **写入每个被扫描的文件夹**——记录已知文件、其类别、已执行的操作、生效的设置指纹（Fingerprint） |

已知操作 ID：`duplicate_check`、`move`、`copy`、`delete`、`ocr_extract`、`place_information`。步进语义：`default_stepping: true` = 操作按列出顺序从左到右执行，重复列出的操作 ID 会**执行两次**；`false` = 集合（重复项合并为一次执行）。

## 安全模型——设置时必须始终遵守

- **每个扫描路径在首次正式运行前必须先做试运行**。`fcsa run`（不带 `--dry-run`）在没有针对该路径的已记录试运行时会拒绝执行。
- **任何设置更改都会使确认失效**（对三个配置文件整体计算指纹）——每次修改配置后，下一次正式运行前都需要重新进行试运行。
- **删除采用失败即关闭（fail-closed）策略。** `delete` 始终移动到 `trash_dir`，除非 *同时* `action-rules.json`（`delete.hard_delete: true`）*和* `config.json`（`allow_hard_delete: true`）明确同意。**针对本技能额外规定：** 未经用户单独、明确授权，绝不启用永久删除——默认保持 `_trash`。
- **`scan_paths` 是显式正向列表**，任何其他路径都会抛出 `PathNotAllowedError`；包含 `.PRIVAT` 或 `CREDENTIALS` 路径段的路径在加载时即被拒绝。
- **试运行对被扫描文件夹是逐字节无副作用的**：`processing-csa.json` 只在正式运行时写入，试运行时从不写入。

## 流程：从触发语句到完成自动化设置

1. **结构化任务。** 从用户语句中提取来源、识别特征和目标。若不明确，有针对性地追问（文件类型？是否包含子文件夹？目标中发生同名冲突时怎么办——skip/overwrite/rename/quarantine？）。
2. **定位模块。** 先用 `fcsa --help` 检查 CLI 是否可用。若缺失，请查找当前系统已授权的模块或包路径；不要臆造本地路径、包名或平行检出副本。安装后，在创建配置之前重新运行 `fcsa --help`。
3. **创建配置文件夹。** `fcsa init <config-dir>`——首先在配置文件夹**内部**的一个全新 `inbox/` 文件夹上写入 `scan_paths`，切勿自动指向真实的用户文件夹。模块中的示例模板：`fcsa/_examples/*.example.json`。
4. **将配置调整为真实任务。** 在 `scan_paths` 中设置为所指定的来源文件夹，在 `categories-definitions.json` 中为所指定的文件类型填写识别模板（`default_target` = 指定目标），在 `action-rules.json` 中配置相应操作（通常为 `move`，必要时前置 `duplicate_check`）。`state_dir`/`trash_dir` 不得位于 `scan_path` 之内（模块会拒绝此类情况，否则会形成自我投喂循环）。
5. **始终先提交试运行：** `fcsa run --config-dir <config-dir> --dry-run`——将结果展示给用户（哪些内容会被移到何处，哪些被识别为重复）。
6. **仅在用户明确确认后正式启用。** 之后才执行 `fcsa run --config-dir
   <config-dir>`（不带 `--dry-run`）。`fcsa status --config-dir <config-dir>` 随后显示当前状态。
7. **逐步扩展**（用户："然后它会随时间逐渐扩展"）：逐步补充更多类别/文件夹，而不是重新开始设置——三个配置文件可增量维护。由于设置指纹的存在，每次扩展后在下一次正式运行前都需要重新进行试运行。

## 限制 / 已知未决事项（以工单 T-20260818-916568570 为准）

- 模块处于第 1 轮，状态为 "development"——核心流水线、CLI 和安全闸门已完成并经过测试（63/63 项测试通过），但**尚未在真实的用户文件夹上正式启用过**。首次正式启用正是本技能的应用场景。仓库可见性为 "private"——未经单独的 `repo-publish-check` 不得发布。
- 规格中的两处缺口存在两种解读（记录于模块内的 `CHANGELOG.md`/`TODO.md`）：`default_stepping: false` 会把重复列出的操作合并为**一次**执行；`duplicate_check` 且结果为 `skip` 时会中止该文件的**整个**剩余操作链（而不仅是 move/copy）。如有需要，在配置依赖这些行为之前与用户确认。
- OCR 是可插拔的后端（`none`/`command`）——未捆绑任何自有的 OCR 引擎。如需真正的 OCR 提取，请通过 `command` 后端类型接入 `ellmos-filecommander` `fc_ocr`。

## 来源

模块在工单 T-20260818-916568570（第 1 轮，fcsa-worker）中构建，应用户要求被有意暂时搁置（PARKED/until-trigger），直至出现上文描述的触发条件。本技能即为执行该搁置备注。

## 更新日志

### 1.0.0 (2026-08-18)
- 初始版本。记录了针对"自动收集/整理文件"任务的触发识别、强制试运行的设置流程，以及仅在用户确认"开始执行"后才正式启用的规则。
