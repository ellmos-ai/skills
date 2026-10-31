---
name: decision-draw
version: 1.1.0
type: skill
author: Lukas Geiger + agy
created: 2026-09-13
updated: 2026-09-18
description: "将分散的未决决策汇总为一个连贯的、以散文呈现的整体概念，基于所有推荐方案。展示各子系统在实施后如何具体协同运作，而不是迫使用户逐一回答数十个孤立的问题。用户可以整体接受该图景，或给出有针对性的修正；修正会自动转化为单项决策，并通过 decision-briefing 第4阶段回写到登记册中。在以下情况使用此技能：“如果我们同意所有内容，整体会是什么样子”、“给我画出整体图景”、“决策的整体概念”、“decision draw”、/decision-draw、“这些系统之后如何协同”。若要讨论每个要点的备选方案，请勿使用此技能，那是 decision-briefing 的职责；若要查看依赖关系图，请勿使用，那是 decision-path 的职责；若要为包括紧密相关组在内的结构化单个模块提供选项及优缺点，请勿使用，那是 decision-shot 的职责；若要推导单个决策，请勿使用，那是 decide 的职责。"
visibility: public
language: zh
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [entscheidung, konzeptbild, gesamtabnahme, buendelung, zusammenspiel, ruecktransfer, workflow]
status: active
dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, decision-path, decision-shot, decision-avatar]
provenance:
  origin: "custom"
  decision_ref: "T-20260913-107991667 (Ticket-Master, Nutzerauftrag 2026-09-13)"
translated_from_sha256: da661fa325502ab0dfae6d6655d70650457d6ac1ff27ca5f0ce6289c375ef2c8
translator: "claude-haiku-5-5"
translated_at: "2026-10-16T00:57:09.230238+00:00"
---
<img src="banner.png" width="100%" alt="decision-draw banner">

# decision-draw — 整体图景与捆绑决策的验收

> 当有五到十项决策待定时，人们很容易在众多选项的细节中迷失，失去对正在形成的系统的整体把握。decision-draw 描述的不是备选方案，而是运作良好的整体：如果所有推荐都被采纳，各系统将如何协同工作？用户可以整体接受这一图景，也可以有针对性地修正。

---

## 何时使用

- 多项相互关联的决策（来自 [decision-briefing](../decision-briefing/SKILL.md) 或决策模板）不应被当作冗长的单项问题清单逐一处理。
- 用户希望在决定之前看到各组件在实施后于日常中如何真正协同。
- 从依赖图（[decision-path](../decision-path/SKILL.md)）中识别出一组紧密耦合的决策，可以作为一个功能单元进行验收。
- 触发词：`/decision-draw`、“如果我们同意所有内容，整体会是什么样子”、“给我画出整体图景”、“决策的整体概念”、“decision draw”、“之后这些系统如何协同”、“用于整体验收的图景”。
- **不要**使用的情况：
  - 当用户想逐个问题权衡各选项，并通过字母（A/B/C）进行选择时——这由 [decision-briefing](../decision-briefing/SKILL.md) 负责。
  - 仅在终端中进行因果与阻塞分析时——这由 [decision-path](../decision-path/SKILL.md) 负责。
  - 针对单个问题或紧密相关组，以5部分结构模块（背景、各选项优缺点、推荐）进行孤立的选项权衡时——这由 [decision-shot](../decision-shot/SKILL.md) 负责。
  - 针对单个开放性基本问题进行方法论推导时——这由 [decide](../decide/SKILL.md) 负责。

---

## 决策系列中的界定

| 技能 | 用户体验与重点 | 对选项的态度 | 验收形式 |
|---|---|---|---|
| `decision-briefing` | **拆分**为单个问题 | 展示所有选项 A/B/C/D | 字母代码（`1A 2C 3B`） |
| `decision-path` | **梳理**因果关系 | 在图中评估选项 | 终端中的诊断（ASCII） |
| `decision-draw` | **连贯的目标图景**（捆绑相互关联的决策） | 仅描述**推荐的方案**（备选方案已链接） | 整体验收或修正语句 |
| `decision-shot` | **结构化的单个模块**（用于单个问题或紧密组） | 展示带 2–4 条优缺点的选项 | 执行决策 / 单项验收 |
| `decide` | **深入研究**单一案例 | 评估矩阵（标准） | 分析性建议 |

> **核心规则：**
> `decision-draw` **只描述推荐的方案**。被否决的备选方案并未消失——它们记录在 [decision-briefing](../decision-briefing/SKILL.md)、[decision-shot](../decision-shot/SKILL.md) 或链接的工单中，并在当前 decision-draw 文档的头部提供链接（是链接，而非仅在标题中提及）。若没有这一引用，图景会剥夺用户的选择权，而非帮助他们做出选择。

---

## 强制性文风规则：用户文本不使用代号和编号

> **标准用户指令（反馈 2026-09-13 / 工单 T-20260913-883789445）：**
> *“decision draws 对我来说太技术化了，必须不带编号，这些你在后台知道，或用于撰写文本时使用 [...]。”*

1. **可见的用户文本中不出现技术代号：**
   在面向人的可见正文（捆绑、概念、协同、实施、询问）中，**不**出现内部代号（如 `BH-A`、`MD-A`、`HA-A`、`PRA`）、工单编号（`T-2026...`）、D 编号（`D-2026...`）、相对路径、Git 哈希或测量数值。
2. **每项 2–4 句日常语言，使用第一人称：**
   捆绑中的每一项按以下三段式表述：
   - *现状：* 当前的初始情况是什么？
   - *“我来做……”：* 我具体计划做什么 / 我的行动建议是什么？
   - *回退：* 如果失败会怎样，或者用户之后决定什么？
   *（示例：“Hermes 只支持英文任务。我会向 Hermes 提交 Issue，同时我们自己做一个临时方案。目前有一些无法使用的旧会话。我会尝试让它们重新可用。如果不行，我会给你一个随机抽取的 10 个会话样本并加以总结——这样你可以决定是否值得抢救。”）*
3. **用于定位的通俗标题：**
   每一项都有一个易懂的德语标题（例如 *“模型后端作为独立核心”*、*“Mac 上的安全部署密钥”*）。用户可以通过该标题进行交互，或给出整体验收。
4. **技术对应关系仅出现在附录中：**
   通俗标题、内部代号、工单 ID 与登记册状态之间的对应关系**仅**体现在文档末尾的一张附录表格中。自动解析器和登记册回写程序只在那里读取。

---

## 强制结构（八个部分）

一份完整的 `decision-draw` 无例外地遵循以下结构：

### 1. 捆绑与范围（通俗表述）
用日常语言概述所捆绑的各项（第一人称，每点 2–4 句，正文中不含 ID/代号）。

### 2. 概念
期望目标状态，以连贯的散文段落呈现：
- 若所有推荐都按此方式实施，将出现怎样的系统格局或工作流程？
- 不做选项对比，不出现“也可以”之类的并列虚拟语气。
- 使用清晰、准确的陈述语气：系统在目标状态下如此运作。

### 3. 协同
本技能的功能核心：
- 已决定的部分在实施**之后**实际上如何相互衔接？
- 优先沿具体的端到端流程进行描述，而非仅列出组件清单。
- 使数据流、接口和职责清晰可见。

### 4. 实施
具体的落地顺序：
- 在实践中实际发生什么？
- 直接采用 [decision-path](../decision-path/SKILL.md) 中的边与依赖逻辑。
- 独立的工作线如实呈现为并行（不编造人为的因果链；一个捆绑可以由多条并行线组成）。只有在存在经证实的依赖或期限时才主张先后顺序。
- 指明关卡、迁移步骤和检查点。

### 5. 此图景未涵盖的内容
防止虚假完整感：
- 哪些边缘问题、未决点或 🔴 置信度被有意排除？
- 与相邻系统的接口边界在哪里？
- 一幅隐瞒其边界的图景会制造虚假的安全感。

### 6. 验收
与用户的互动：
- 用户整体审阅该图景。
- 回应方式 1：**明确的整体验收**（“可以”、“验收通过”、“按此实施”）。只有在此情况下，捆绑中的所有项才被记为已决定。
- 回应方式 2：**通过通俗标题或日常语言进行修正**（“Mac 部署时最好不要自动重启”、“先暂缓 VersicherungsManager”）。这会被拆分为单项决策；所有未修正的项保持开放。

### 7. 回写
将用户修正系统地转化为单项决议：
- **不自动并入：** 只有在明确整体验收的情况下，未改动的项才会被记录。部分修正**不是**整体验收！
- **修正时的隔离：** 若出现修正，将其拆分为单项决策；捆绑中的其余各项严格保持**开放**（在来源登记册/模板中），直到用户确认修订后的整体图景，或逐一确认剩余项。
- **强制回写表：** 每一条修正反馈都必须生成一张结构化的分析表，包含四列（原始修正、受影响代号、连锁状态、未决歧义）。
- **仅通过第 4 阶段写入：** `decision-draw` **没有**自己的登记册写入通道。记账**仅**通过 [decision-briefing](../decision-briefing/SKILL.md) 第 4 阶段的标准流程完成。

### 8. 附录：技术参考表（仅供记账与审计）
文档末尾的紧凑表格，包含：
`| Klartext-Titel | Internes Kürzel / ID | Ticket-Referenz | Unterstellte Empfehlung | Konfidenz | Link / Details |`

---

## 示例（试点摘录：Ticket-Master 2026-09-13 — BACH 与系统集群）

```markdown
# DECISION-DRAW: BACH-Kernverbund & Betriebsintegrität

## 1. Bündel und Umfang

- **Modell-Backend als eigenes Herzstück:** Die Modellzuteilung ist aktuell eng mit dem Monolithen verzahnt. Ich lagere das Backend als eigenständiges Kernmodul aus, damit Rechte und Budgets unabhängig geprüft werden. Scheitert ein externer Dienst, schaltet das System automatisch auf das lokale Reservemodell zurück.
- **Sichere Deploy-Schlüssel auf dem Mac:** Auf dem Mac laufen Dauerprozesse, die bei harten Updates unsauber abbrechen können. Ich richte einen lesenden Schlüssel und ein Meldeskript ein, das Aktualisierungen anzeigt, ohne laufende Dienste abzuschießen. Sollte ein Dienst dennoch hängen, meldet der Watcher das direkt an die Betriebsübersicht.
- **Einheitliche Konfigurations-Sollwerte:** Die beiden Hauptrechner nutzen teilweise unterschiedliche Spracheinstellungen. Ich gleiche die Konfigurationen über das gemeinsame Sync-Verzeichnis an, lasse dem Laptop aber ausreichend Spielraum für mobile Tests.
- **Feste Zeitzone im VersicherungsManager:** Datumsberechnungen bei Fristen hängen bisher vom Betriebssystem ab. Ich verankere eine feste Zeitzone in den Anwendungseinstellungen, damit Fristen überall auf die Minute genau übereinstimmen.
- **Öffentliche Bereitstellung der USMC-Dokumentation:** Die Modul-Dokumentation ist im Webauftritt noch als privat markiert und löst Prüfwarnungen aus. Ich korrigiere die Sichtbarkeit auf öffentlich, damit der nächtliche Seiten-Bau ohne Fehler durchläuft.

---

## 2. Konzept

Wir etablieren ein sauberes, entkoppeltes Multi-Host-System, bei dem das Modell-Backend
als eigenständiges Kernmodul `agents-heart` betrieben wird. Rechte und Budgets liegen
strukturiert in einer SQLite-Datenbank, während Zuteilungsentscheidungen zweistufig
fallen: BACH ermittelt fachlich fundiert die Kandidatenmenge, clutch wählt darin
preis- und kapazitätsoptimal das finale Modell.

Auf dem Mac Studio laufen die 24/7-Dienste geschützt und stabil über einen read-only
Deploy-Key; Updates ziehen automatisch ein, benachrichtigen den Operator bei laufenden
Diensten aber sanft, statt Hintergrundprozesse hart abzuschießen. Konfigurationen
dürfen dort bewusst hostspezifisch auf Leistung abgestimmt sein, während app-weite
Einstellungen (wie Zeitzonen im VersicherungsManager nach dem bewährten routinika-Muster)
deterministisch fest verdrahtet sind. USMC bleibt der kanonische öffentliche
Memory-Baustein und behält seinen festen Platz im Webauftritt.

---

## 3. Zusammenspiel

Die fünf Posten bilden keine serielle Kausalkette, sondern stellen modular entkoppelte Bausteine der täglichen Betriebsintegrität dar, die im Gesamtsystem parallel ineinandergreifen:

- **Kernarchitektur & Modell-Routing (`BH-A`):** Das Modul `agents-heart` entkoppelt die Modellzuteilung. Trifft eine Aufgabe ein, ermittelt BACH fachbezogen die Kandidatenmenge und clutch wählt kosten- und kapazitätsoptimal das Modell.
- **Host-Konfiguration & Deploy-Integrität (`CF-A`, `MD-A`):** Während auf dem Laptop und der Workstation konsistente Reasoning-Stufen gelten (`CF-A`; hostabhängige Modelle bleiben transparent), betreibt der Mac Studio seine persistenten Hintergrundprozesse unter validierten Einstellungen. Bei Aktualisierungen zieht der Mac den Code via Read-only Deploy-Key (`MD-A`); der GUI-Server startet neu, während langlebige 24/7-Dienste den Update-Bedarf sanft an das Dashboard melden.
- **Domänen-Persistenz & Fristen (`VM-A`):** Applikationen wie der VersicherungsManager schreiben Fristen und Deadlines gegen eine app-weite `settings`-Tabelle nach routinika-Muster. Zeitrechnungen und Deadline-Projektionen operieren über alle Profile hinweg deterministisch auf derselben IANA-Zeitzone.
- **Öffentlicher Auftritt (`PD-A`):** Der nächtliche Seiten-Builder validiert den Zustand der Repositories. USMC wird mit korrigierter `public`-Deklaration fehlerfrei publiziert, ohne Warnungen in den Sicherheits-Gates auszulösen.

---

## 4. Umsetzung

Da die Vorlage für diese fünf Posten im Abhängigkeitsgraphen ([decision-path](../decision-path/SKILL.md)) keine serielle Kette vorgibt, erfolgt die Umsetzung ehrlich in vier voneinander unabhängigen, parallelen Arbeitssträngen (Ausweg a: parallele Stränge statt erfundener Kausalität). Eine sequenzielle Reihenfolge gilt nur dort, wo externe Fristen oder interne Schritte belegt sind:

- **Strang A (Termingebunden — Frist 2026-09-14):**
  1. USMC-Metadaten auf `public` nachziehen (`PD-A`); Draft-PR #2 verwerfen. Duldet wegen des nächtlichen Builder-Laufs keinen Aufschub, ist technisch jedoch von allen anderen Strängen unabhängig.
- **Strang B (Host-Konfiguration & Mac-Deploy — parallel ausführbar):**
  1. B1: Sollwerte in `.SYNC` festschreiben (`CF-A`), Reasoning-Stufe `high` für beide Hosts synchronisieren.
  2. B2 (unabhängig von B1): Read-only Deploy-Key auf Mac Studio hinterlegen und Pull-and-Report-Skript einrichten (`MD-A`).
- **Strang C (Domänen-Datenbank — parallel ausführbar):**
  1. Migration der app-weiten `settings`-Tabelle im VersicherungsManager nach routinika-Vorbild implementieren (`VM-A`), um die saubere Basis für den nachgelagerten Publisher-Bau zu schaffen.
- **Strang D (Architektur-Herauslösung — interner Mehrstufenplan):**
  1. D1: SQLite-Schema für Rollen und Budgets in `agents-heart` anlegen (`BH-A` E1).
  2. D2: Backend-Katalog als Python-Modul ausgründen (`BH-A` E3) und clutch-Seam für Zuteilung binden (`BH-A` E2).
  3. D3: Modul `agents-heart` final herauslösen und anbinden (`BH-A` E5, E6).

---

## 5. Was dieses Bild nicht abdeckt

- **Task-Claiming Race Condition:** Der Integritätsfehler bei doppeltem Task-Claim läuft
  in einem separaten Hotfix-Ticket und ist nicht Teil dieser Freigabe.
- **Cockpit-Frontend:** Das Monitoring-Cockpit (`BH-A` E4) wird bewusst noch nicht gebaut,
  solange das Backend nicht produktiv meldet.
- **Sichtbarkeitsschaltung nach außen:** Reine Bereitstellung von Code schaltet keine
  neuen Repos public; die finale Freigabe bleibt dem Nutzer vorbehalten.

---

## 6. Abnahme

Du kannst diesen Systemverbund als Ganzes abnehmen oder in Alltagssprache korrigieren:

- **Ausdrückliche Gesamtabnahme:** „Passt so, genau so umsetzen.“ (Nur dies führt zur Verbuchung aller Posten).
- **Korrektur-Beispiele:**
  - *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“* (Mehrfachtreffer)
  - *„BH-A E5 lieber ocean-heart nennen statt agents-heart.“*
  - *„VM-A erst mal vertagen, der Publisher hat noch Zeit.“*

---

## 7. Rücktransfer

Wird das Gesamtbild abgenommen oder korrigiert, übersetzt der Skill die Rückmeldung:

### Fall A: Ausdrückliche Gesamtabnahme
Nimmt der Nutzer das Gesamtbild ausdrücklich als Ganzes ab (z. B. *„Passt so, genau so umsetzen“*):
- Alle fünf Posten (`BH-A: 1A/2A/3A/4B/5A/6A`, `MD-A: A1`, `CF-A: 1C/2B/3B`, `VM-A: A`, `PD-A: A`) werden als GETROFFEN an [decision-briefing](../decision-briefing/SKILL.md) Phase 4 übergeben.
- Phase 4 übernimmt die Eintragung ins Register `DECIDED-AND-DONE.md` und aktualisiert die fünf Quelltickets.

### Fall B: Teilkorrektur mit Mehrfachtreffer
Gibt der Nutzer eine inhaltliche Korrektur ein, z. B.:
> *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“*

**1. Strukturierte Rücktransfer-Tabelle:**

| Originalkorrektur (Wortlaut des Nutzers) | Betroffene Kürzel | Domino-Status (welche abhängigen Knoten kippen dadurch) | Offene Mehrdeutigkeiten |
|---|---|---|---|
| *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“* | `MD-A`, `CF-A` *(Mehrfachtreffer: 1 Aussage bewegt 2 Posten)* | **`MD-A`:** Kippt von A1 auf A2. Erfordert SSH-Write-Key auf Mac Studio, Push-Rechte im GitHub-Repo `bach` und Sicherheitsprüfung des LaunchAgents.<br>**`CF-A`:** Gruppe 1 kippt von C auf A (Laptop-Claude-Desktop wird restriktiver). Gruppe 2 kippt von B auf A (`codex.model` wird starr angeglichen). Gruppe 3 bleibt B (`high`), da bereits synchron. | **`CF-A` Gruppe 1:** Nutzer verlangt Angleichung an Workstation (1=A) — Rückfrage nötig, ob die bisher bewusste Freizügigkeit auf dem Laptop wirklich entzogen werden soll.<br>**`MD-A`:** Unklar, ob Write-Key für alle Repos oder nur für `bach` gelten soll. |

**2. Status der unberührten Posten (Schutz vor ungefragtem Mitbuchen):**
- Die unveränderten Posten `BH-A`, `VM-A` und `PD-A` werden **nicht** gebucht!
- Sie verbleiben im Status **OFFEN** (`PENDING`) in der Vorlage bzw. im Register `TO-DECIDE-USER.txt`.
- Eine Teilkorrektur ist **keine** Gesamtabnahme. Erst wenn das nach Korrektur aktualisierte Gesamtbild vom Nutzer als Ganzes abgenommen wird oder die verbleibenden Punkte einzeln bestätigt werden, dürfen sie verbucht werden.

**3. Buchungsweg:**
- `decision-draw` besitzt keinen eigenen Schreibmechanismus.
- Übergeben wird an **[decision-briefing](../decision-briefing/SKILL.md) Phase 4** nur, was die Tabelle als eindeutig ausweist: `CF-A` Gruppe 2 = A und Gruppe 3 = B.
- **Nicht** übergeben werden `MD-A` und `CF-A` Gruppe 1 — für beide steht in der Spalte *Offene Mehrdeutigkeiten* eine Rückfrage. Eine Mehrdeutigkeit, die man vor der Buchung klären wollte, darf man nicht in derselben Runde als geklärt verbuchen.
- Phase 4 trägt die eindeutigen Teile mit Begründung in Ticket `T-20260913-947070291.txt` ein und aktualisiert `DECIDED-AND-DONE.md`. Ticket `T-20260913-799464688.txt` (`MD-A`) bleibt offen, bis die Rückfrage beantwortet ist.

---

## 8. Anhang: Technische Referenztabelle (nur für Buchung & Audit)

| Klartext-Titel | Internes Kürzel | Ticket / Quelle | Unterstellte Empfehlung | Konfidenz | Link / Details |
|---|---|---|---|---|---|
| Modell-Backend als eigenes Herzstück | `BH-A` | `T-20260913-896336887` | 1A / 2A / 3A / 4B / 5A / 6A | 🟢 | `docs/MODELL-BACKEND-KONZEPT_2026-09-13.md` |
| Sichere Deploy-Schlüssel auf dem Mac | `MD-A` | `T-20260913-799464688` | A1 + Skript (nur Melden für 24/7) | 🟢 | Ticket `T-20260913-799464688.txt` |
| Einheitliche Konfigurations-Sollwerte | `CF-A` | `T-20260913-947070291` | 1C (begründet) / 2B (hostabh.) / 3B (high) | 🟢 / 🟡 | Ticket `T-20260913-947070291.<HOST>.txt` |
| Feste Zeitzone im VersicherungsManager | `VM-A` | `T-20260906-496406575` | A (app-weite settings wie routinika) | 🟢 | Ticket `T-20260906-496406575.<HOST>.txt` |
| Öffentliche Bereitstellung der USMC-Dokumentation | `PD-A` | `T-20260913-609930207` | A (auf public nachziehen, Status quo) | 🟢 | Ticket `T-20260913-609930207.txt` |
```

---

## 实践规则

1. **概念中不使用虚拟语气：** 按照已经实现的方式描述整个系统。用户想要的是对结果的清晰认识，而非理论上的可能性。
2. **因果先于时序：** *实施*部分的顺序遵循 [decision-path](../decision-path/SKILL.md) 依赖图的层级。独立的线索如实呈现为并行，不会被扭曲成人为的因果链。
3. **回写中的明确连锁检查：** 不得在未检查依赖节点是否在图中失效或受到影响的情况下，孤立地记录用户的修正。
4. **部分修正时不自动并入：** 只有在明确整体验收时才记录未改动的项。每次部分修正时，所有未受影响的项都严格保持开放，直到整体图景被重新批准或各项被逐一确认。
5. **仅通过第 4 阶段写入：** `decision-draw` 没有自己的登记册写入通道。记账无一例外地通过 [decision-briefing](../decision-briefing/SKILL.md) 第 4 阶段完成。
6. **遵守登记册约定：** 记账始终遵循决策登记册的规则（不重新编号 ID、唯一的记账代码、规范目标 `DECIDED-AND-DONE.md`）。
7. **用户文本不含技术编号和代号：** 面向人的可见正文中不出现 ID、代号、路径或工单编号。每一项都以易懂的第一人称表述；所有标识符移入附录表格。

---

## 会话溯源

当 Decision-Draw 作为长期概念文档保存时，它以以下内容结尾：

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

- 来源优先级：明确的运行时/CLI 声明，其次是权威的提供方环境或钩子，否则为 `unbekannt`。
- 子代理继承父会话的会话 ID。
- 纯聊天模板不附加标记。

---

## 更新日志

### 1.1.0 (2026-09-18)
- 面向用户的决策文本风格规则已确立（T-20260913-883789445，用户指令 2026-09-13）：
  - 可见用户文本中不出现技术代号、工单/D 编号、路径或测量数值。
  - 每项使用 2–4 句第一人称日常语言（现状、“我来做……”、回退）。
  - 用于识别和验收的通俗易懂的标题。
  - 技术对应关系（代号、工单 ID、登记册状态）严格移入结尾附录表（第 8 节）。

### 1.0.1 (2026-09-13)
- 审核后的修订：
  - 收紧回写约定：部分修正不自动并入；未受影响的项在整体验收前严格保持开放。
  - 引入四列强制回写表（原始修正、受影响代号、连锁状态、未决歧义）。
  - 示例中演示了多重命中（一次用户修正同时影响 `MD-A` 和 `CF-A`）。
  - 在约定和示例中确立了仅通过 `decision-briefing` 第 4 阶段写入的途径。
  - 修正示例中的因果链错误：独立的项如实呈现为四条并行工作线（方案 a）。
  - 通过输出格式（带优缺点的结构化单个模块与带整体验收的连贯目标图景）明确了与 `decision-shot` 的界定。

### 1.0.0 (2026-09-13)
- 基于用户需求 T-20260913-107991667 的初始版本。
- 七部分强制结构（捆绑、概念、协同、实施、边界、验收、回写）。
- 捆绑逻辑基于 `decision-path`，并通过回写桥接到 `decision-briefing` 第 4 阶段。
