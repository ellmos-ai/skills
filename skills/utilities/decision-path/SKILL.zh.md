---
name: decision-path
version: 1.1.0
type: skill
author: Lukas Geiger + agy
created: 2026-09-13
updated: 2026-09-18
description: "根据一组未决和已决的决策，为终端生成结构化的 ASCII 依赖图（最多 100 列）。依据五项固定标准评估节点：合理性、推荐、符合用户习惯（方向与 decision-avatar 置信度分开评估）、相互契合和相互矛盾；边携带关系类型与证据状态。毫不留情地揭示阻塞项、解锁关系、先后顺序以及相互矛盾的推荐。当用户提出以下类似表述时使用此技能：\"哪些决策相互依赖\"、\"决策的依赖图\"、\"可视化决策路径\"、\"检查决策之间的矛盾\"、\"决议的先后顺序\"、/decision-path。不要用于先盘点决策，那是 decision-briefing 的工作；不要用于将推荐的整体方案汇总以供验收，那是 decision-draw 的工作；不要用于包含选项与利弊的紧凑五段式单块，那是 decision-shot 的工作；不要用于基于框架的单一案例权衡，那是 decide 的工作。"
visibility: public
language: zh
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [entscheidung, abhaengigkeiten, ascii-graph, decision-path, visualisierung, routing, widerspruchs-erkennung]
status: active
dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, decision-draw, decision-shot, decision-avatar]
provenance:
  origin: "custom"
  decision_ref: "T-20260913-107991667 (Ticket-Master, Nutzerauftrag 2026-09-13)"
translated_from_sha256: 68422f7ca7043f158883734f79aadf21f8830b6238588a896255dccd8abc952a
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:40:39.337351+00:00"
---
<img src="banner.png" width="100%" alt="decision-path banner">

# decision-path：未决策决策的 ASCII 依赖图

> 决策不会在真空中做出。单独看似合理的决定，往往会阻塞后续工作、需要尚未完成的前置步骤，或者绕过既有的保护约定。decision-path 在终端中清晰呈现因果关系、先后顺序与相互矛盾之处。

---

## 何时使用

- 需要对一批未决策决策进行结构化整理（来自 [decision-briefing](../decision-briefing/SKILL.md) 第一阶段、会话上下文或决策模板）。
- 需要厘清哪些决策可以立即自由决定（根节点），哪些依赖前置条件或外部阻塞项。
- 需要概览哪些推荐彼此协调，以及哪些决议在逻辑或组织上相互冲突。
- 触发词：`/decision-path`、"哪些决策相互依赖"、"决策的依赖图"、"可视化决策路径"、"ASCII 决策树"、"决策之间的矛盾"、"检查因果关系"。
- **不要**用于以下情况：
  - 首次采集和盘点未决问题，这由 [decision-briefing](../decision-briefing/SKILL.md) 第一阶段负责。
  - 将推荐的方案整合为一个连贯的整体图景以供验收，这由 [decision-draw](../decision-draw/SKILL.md) 负责。
  - 包含选项与每个选项利弊的紧凑五段式单块，这由 [decision-shot](../decision-shot/SKILL.md) 负责。
  - 对单个复杂问题进行方法论上的推导（加权评分、情景分析），这由 [decide](../decide/SKILL.md) 负责。

---

## 决策技能家族中的分工

| 技能 | 任务 | 输入 | 输出 |
|---|---|---|---|
| `decide` | 以方法论推导**单个**决策 | 标准、选项 | 评估矩阵、单项决策 |
| `decision-briefing` | 将**大量**未决决策拆解为带选项的单个问题 | 未决事项清单 | 编号的 A/B/C/D 简报、粗略标记、登记 |
| `decision-path` | **验证并可视化大量决策之间的因果关系与矛盾** | 来自简报/登记册的粗略标记 | 带 5 项节点评估和边状态的 ASCII 依赖图 |
| `decision-draw` | 将推荐**整合为一个整体图景**供整体验收 | `decision-path` 的打包结果 | 方案、协同效应（仅推荐方案）、回传 |
| `decision-shot` | 将**已完成的分析**压缩为要点（1 个决策或一组紧密相关的决策） | 1 个已分析的问题或一组问题 | 含选项、利弊和完整分析链接的五段式简要版 |
| `decision-avatar` | 提供**用户偏好建模** | 上下文、既往决议 | 置信度评估 🟢 / 🟡 / 🔴 |

### 与 decision-briefing 的约定与职责划分

`decision-briefing` 第一阶段在读入时已粗略识别依赖关系与先后顺序（例如来自"之后自动："等信号词、阻塞项或工单引用）。`decision-path` 不会悄悄地重新推导这一结构，而是直接基于这些粗略标记继续工作：

1. **decision-briefing 提供粗略标记：** 它提供未决决策的原始清单，以及其初步的关联信号。
2. **decision-path 验证、评估并可视化：** 它依据实际证据状态检验这些信号，区分已确认的边与推测的边，为每个节点给出五项评估，并毫不留情地揭示门控冲突。
3. **差异反馈：** 如果 `decision-path` 发现简报中缺失或记录不完整的依赖关系，它绝不会悄悄接受，而是以修正说明的形式反馈给简报。

---

## 每个节点的五项评估（以及边的证据状态）

五个维度 `[S E U Z W]` 评估的是**节点**（系统语境中待决或已决的决策）。边携带其语义关系类型（例如解锁、阻塞、以…为前提）以及证据状态（已证实与推测）。

图中每个节点都带有一行紧凑的评估，恰好包含五个维度：

```
[S+ E:<Option> U<Richtung><Konfidenz> Z+ W-]
```

1. **合理性（`S`）**：技术与架构上的可行性：
   - `S+`：方案稳健，解决真实问题，避免不必要的复杂性。
   - `S~`：部分合理，但存在维护或流程风险。
   - `S-`：治标不治本的方案、盲目行动或已知的错误方向（例如在错误的环节设置过滤器）。

2. **推荐（`E`）**：具体的、基于事实的行动建议：
   - `E:<Option>`：明确的选项（例如 `E:A`、`E:B`、`E:klaeren`、`E:Schritt1`）。
   - `E-`：无法给出推荐（例如事实缺失或确属根本性问题）。

3. **符合用户习惯（`U`）**：与用户的工作方式和规则的一致程度（通过 `decision-avatar`）：
   分别编码**方向**（该选项是否符合工作方式？）与**证据可靠性/置信度**：
   - **方向（"U" 之后的第一个字符）：**
     - `+`：符合用户习惯，即与历史上已证实的决策、指导原则（`CLAUDE.md`，即政策）或用户明确表达的偏好一致。
     - `~`：中立 / 开放，即无法证明存在明显的偏好方向。
     - `-`：不符合用户习惯，即与用户惯常的工作方式或既往模式相悖。
   - **证据可靠性 / 置信度（第二个字符）：**
     - 在 ASCII 图中仅使用 ASCII 字符：
       - `!`：高 / 已证实（在正文中：🟢 已证实）。
       - `~`：中 / 合理推断（在正文中：🟡 需要价值判断，需用户权衡）。
       - `?`：低 / 未经证实（在正文中：🔴 新领域，根本性问题）。**升级处理，而非猜测！**
   - *示例：* `U+!`（符合用户习惯且已证实）、`U+~`（符合用户习惯，但属于权衡问题）、`U-!`（已证实但不符合用户习惯）、`U~?`（开放、无既定指引，需升级处理）。

4. **相互契合（`Z`）**：与相邻节点在风格和架构上的柔性契合度：
   - `Z+`：在风格和架构上无缝契合，形成无摩擦的一致整体。
   - `Z~`：风格上略有摩擦或存在组织上的额外开销，但功能上可以兼容。
   - `Z-`：在系统整体中明显摩擦（例如配置泛滥、耦合不清、范式断裂），但尚未违反任何硬性规则。

5. **相互矛盾（`W`）**：明确的矛盾以及规则/门控违反（**最重要的输出——警报！**）：
   - `W-`：与其他推荐、具有约束力的指导原则以及生效中的保护门控不存在矛盾。
   - `W+`：**硬性冲突 / 警报！** 推翻另一项推荐、违反具有约束力的政策（`CLAUDE.md`，P-00x），或无视生效中的保护门控。冲突节点必须始终在 `WIDERSPRUECHE` 一节中列出，并附上原因与化解路径。

---

## 边的类型与推导规则

依赖关系**严格从源文本推导**，绝不凭空推测。边携带其关系类型与证据状态：

| 文本中的信号 | 边的类型 | 记法 | 含义 |
|---|---|---|---|
| "之后自动：…"、"放行"、"使…成为可能" | 解锁 | `+-->` | 只有源决策完成后，目标决策才能执行（已证实） |
| "阻塞"、"阻止"、"保护门控生效" | 阻塞 | `=>` | 只要源问题未解决，目标即被阻塞 |
| "以…为前提"、"需要先行"、"前置条件" | 以…为前提 | `-->` | 目标在时间顺序和逻辑上需要源决策 |
| "后续决策"、"之后的第 2 步" | 先后顺序 | `-->` | 完成后的逻辑后续步骤 |
| "已被测量证伪"、"已过时"、"失效" | 作废 | `--X-->` | 源端的认识使目标事项失去意义 |
| 相同 D-ID、工单 ID 或相同系统，但无文本依据 | 推测 | `?-->` | 合理的关联，但缺乏明确的因果证据（未经证实） |

> **未经证实的边的规则：**
> 凡文本中没有明确因果依据的，边一律标记为推测（`?-->`），绝不作为既定事实。凡完全没有证据显示关联的，节点保持相互独立并列呈现。

---

## ASCII 图的格式要求

1. **等宽且适合终端：** 最大行宽 **100 列**。不使用会在终端中换行的宽表格。
2. **字符集与纯净性：** 纯 ASCII。在图形代码块内不得出现表情符号（🟢🟡🔴）；置信度在其中仅通过 ASCII 字符（`!`、`~`、`?`）编码。
3. **节点标识：** 仅使用已有的简称（`PD-A`、`MD-A`、`BH-A`、`VM-A`、`QR-A`、`CL-A`、`MO-A`、`D-001`、`732597768`）。绝不发明新的人造标识！若缺少简称，则使用事项编号。内部后续步骤以无编号的注释 `(...)` 形式标注在边上。
4. **层级结构：**
   - `EBENE 0 - haengt an nichts`：根节点、未被阻塞的决策、外部杠杆。
   - `EBENE 1 - haengt an genau einer`：直接的后续决策。
   - `EBENE 2 - haengt an mehreren / tiefe Kette`：多重依赖或下游节点。
   - `WIDERSPRUECHE`：硬性矛盾、门控冲突以及不一致的推荐（`W+`）。
   - `LEGENDE`：每张图的必备组成部分。图中使用的每个结构符号（`|`、`=Option`、`(...)`、边的箭头）都必须在图例中列出并加以说明。
5. **可选的 Mermaid 投影：** 如果无需额外成本，可在需要时附加一个额外的代码围栏（`mermaid`）。ASCII 图始终是具有约束力的主要输出。

---

## 示例（试点节选：Ticket-Master 2026-09-13）

来自 Ticket-Master 决策模板的真实节选（`732597768`、`MO-A`、`CL-A`、`QR-A`、`387521104`、`CL-B`）：

```
====================================================================================================
DECISION-PATH: ABHAENGIGKEITSGRAPH (Pilot Ticket-Master 2026-09-13)
====================================================================================================

EBENE 0 - haengt an nichts (Wurzelentscheidungen & externe Blocker)
  [732597768] GitHub-Billing klaeren                        [S+ E:klaeren U+! Z+ W-]
      |  schaltet frei
      +--> [MO-A] Welle 2 freigeben                         [S+ E:A       U+~ Z+ W-]

  [CL-A] clutch Admin-Merge PR #6 & PR #8                   [S+ E:A       U+! Z+ W-]
      |  blockiert durch: [Gate "1 Approving Review" (Self-Approval unmoeglich)]
      --> (Folgeentscheidung: Branchschutz auf 0 oder Bot anpassen)

  [QR-A] Queue-Rename Junction (_TICKETS -> TICKETS)        [S+ E:B       U+! Z+ W-]
      +--> [387521104] Nachtfenster faehrt                  (belegt: nur unter B)

  [CL-B] Review-Gate-Pilot: Mac-Signierschluessel           [S+ E:Schritt1 U+~ Z+ W-]
      --> (Folgeschritte 2-4: Modell-Automatisierung nach Schluessel-Bereitstellung)

EBENE 1 - haengt an genau einer Vorbedingung
  [MO-A] Welle 2 freigeben                                  [S+ E:A       U+~ Z+ W-]
      |  setzt voraus: [732597768] (Billing geklaert, Remote-CI-Gates wieder aktiv)
      |  setzt voraus: [Gate PRIVATE.txt "gruenes Remote-CI"]
      --> (Folgeschritt: Sichtbarkeit schalten bleibt reine Nutzerhandlung)

EBENE 2 - haengt an mehreren / tiefe Kette
  [387521104] Nachtfenster Migration autonom fahren         [S+ E:B       U+! Z+ W-]
      |  setzt voraus: [QR-A]=B (NTFS-Junction gesetzt)
      |  setzt voraus: (Junction auf dem zweiten Host per Transfer-Ticket gesetzt -
      |                  Ticketnummer in der Vorlage nicht genannt)

----------------------------------------------------------------------------------------------------
WIDERSPRUECHE & GATE-KOLLISIONEN
----------------------------------------------------------------------------------------------------
  [MO-A]=B  X  [Gate PRIVATE.txt "gruenes Remote-CI"]
               Konflikt: Option B wuerde Welle 2 rein auf lokaler Testbasis freigeben,
               obwohl zwei Modulvertraege ausdruecklich gruenes Remote-CI fordern.
               Aufloesung: Empfehlung A erzwingt erst [732597768] (Billing), heilt Kollision.

  [CL-A]=StatusQuo  X  [Gate "1 Approving Review" (Self-Approval unmoeglich)]
               Konflikt: master verlangt 1 Review, einziges Repo-Konto ist lukisch.
               Aufloesung: Empfehlung A (Admin-Merge) bricht Blockade legitim auf.

----------------------------------------------------------------------------------------------------
LEGENDE & BEWERTUNGSSCHLUESSEL
----------------------------------------------------------------------------------------------------
  Kanten & Struktur:
    +-->   schaltet frei (Kausalitaet im Quelltext belegt)
    =>     blockiert / verhindert (Gate oder externer Blocker)
    -->    setzt voraus / Reihenfolge (Vorbedingung oder Folgeschritt)
    ?-->   vermutete Abhaengigkeit (Koppelung plausibel, aber unbelegt)
    --X--> entwertet / ueberholt (macht Zielposten obsolet)
    X      Widerspruch / Kollision (Gate- oder Regelverletzung)
    |      vertikaler Verbindungsstrang / Attribut-Zuordnung
    [ID]   Entscheidungsknoten (Kuerzel oder Postennummer aus Vorlage)
    [Gate]  externes Gate / Regel / Vertrag - KEIN Entscheidungsknoten
    =Opt   spezifische Option eines Knotens (z. B. [MO-A]=B)
    (...)  unnummerierte Kanten-Annotation / Folgeschritt (keine neue ID)

  Knoten-Status [S E U Z W]:
    S: Sinnvoll      (+ tragfaehig / ~ mit Vorbehalt / - ungeeignet)
    E: Empfohlen     (A, B, C, klaeren, Schritt1, - keine Empfehlung)
    U: Usertypisch   (Richtung: + typisch / ~ neutral / - untypisch;
                      Konfidenz: ! gesichert / ~ Abwaegung / ? Eskalation)
                      [! = belegt (Prosa gruen), ~ = Nutzerabwaegung (Prosa gelb),
                       ? = ungesichert / Eskalation (Prosa rot)]
    Z: Zusammenpass. (+ harmoniert stilistisch / ~ Reibung / - Architektur-Bruch)
    W: Widerspruch   (- widerspruchsfrei / + harte Kollision mit Gate oder Regel)
====================================================================================================
```

---

## decision-path 不做的事

1. **不做决策：** 该技能提供对局势的透明梳理。决定权始终在用户手中。
2. **不设计选项：** 该技能不讨论新的方案或标准目录；这些任务属于 [decide](../decide/SKILL.md) 或 [decision-briefing](../decision-briefing/SKILL.md)。
3. **不回写登记册：** 图不修改登记册或工单文件。决策作出后的回写由 [decision-briefing](../decision-briefing/SKILL.md) 第四阶段完成，或通过 [decision-draw](../decision-draw/SKILL.md) 的回传机制完成。
4. **向用户解释时不使用难懂的缩写黑话：** 向用户说明图的结果时，适用强制性的风格规则（T-20260913-883789445）：用第一人称、日常口语写 2–4 句（说明局势、"我会……"、回退方案）。节点标签使用可读的简短标题。技术标识与工单编号移入附录表格。

---

## 会话溯源

当依赖图作为持久的分析产物保存时，文档以以下内容结尾：

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

- 来源优先级：显式的运行时/CLI 信息，其次是权威的提供方环境或钩子，否则为 `unbekannt`。
- 子代理继承父会话的会话 ID。
- 日常聊天和临时终端输出不加标记。

---

## 变更日志

### 1.1.0（2026-09-18）
- 为易懂的决策文本确立风格规则（T-20260913-883789445，2026-09-13 用户指示）：
  - 向用户的说明采用自然的第一人称，避免编号泛滥。
  - 终端图中的节点使用可读的简短标题。
  - 技术归属（工单/D 编号）移至附录表格。

### 1.0.0（2026-09-13）
- 基于用户任务 T-20260913-107991667 的首个版本。
- 每个节点的五项评估键（合理性、推荐、符合用户习惯——方向与置信度分开评估，通过 `decision-avatar`、相互契合、相互矛盾）；边携带关系类型与证据状态。
- 与 `decision-briefing` 的约束性约定：briefing 提供粗略标记，decision-path 验证并可视化；差异时反馈。
- 通过输出格式（包含选项与利弊的紧凑五段式）与 `decision-shot` 明确划界。
- 修正因果结构：CL-A 位于批准门控而非计费环节；删除了发明的标识，改用无编号的边注释。
- 统一的 ASCII 规格（最多 100 列），边记法统一为 `--X-->`，并提供完整的结构图例和不含表情符号的图形代码。
