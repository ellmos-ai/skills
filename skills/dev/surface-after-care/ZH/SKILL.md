---
language: zh
---

> **中文** — `surface-after-care` 官方中文版本。

# Surface After Care — 已发布 Repo 的定期维护例行流程

## 本 Skill 的适用场景

适用于**已公开发布**且需要定期复查的 Code Repository。它是轻量级维护阶段：包含所有仅需在 Repository 本身内部决策的事项，无需盘点外部 Repository 或发起法律审查。

与相关 Skill 的区别：

| 场景 | Skill |
|---|---|
| Repo 首次公开发布 | `github-repo-care` |
| Repo 已公开，定期例行维护 | **本 Skill** |
| 额外法律检查 + 跨所有 Org 交叉引用 + 应用 i18n | `full-after-care`（别名 `deep-after-care`） |
| 在公开发布前仅进行法律/隐私/许可证检查 | `repo-publish-check` |
| 保持多语言版本内容同步 | `bilingual-doc-sync` |
| 在多个 Repo 之间公平轮换分配此维护例行流程 | `rotation-check` |

## 核心理念

已发布的 Repo 容易在两个方向上产生偏差：**文档描述的软件版本落后于 Repo 中的实际代码**，以及**积累了从未打算向外界展示的文件**。这两者通常都不会引发灾难，但都会失去你最想吸引的用户——一部分用户因为安装指南不再适用而放弃，另一部分用户因为在根目录下看到 `AUFGABEN.txt` 和 `Plan.txt` 而觉得这里只是某人的私密草稿堆。

本流程旨在清理这两类问题。它被设计为可反复执行的例行流程：每年执行 4 次半小时的维护，远胜过一次大规模的大扫除。

## 执行步骤

步骤顺序并非随意排列。步骤 0 位于最前，因为它决定了后续所有步骤的范围。步骤 2 必须在任何推送更改的操作之前运行——否则你就会把改进推送到尚未清理干净的状态之上。步骤 1 纯属服务端操作，不会造成干扰。

### 0. 盘点分发渠道

**在修改任何内容之前：弄清楚该项目究竟部署在哪些地方。** GitHub Repo 很少是唯一的分发渠道。如果 npm 包页面继续显示带有错误安装指令的旧版本，那么修改后的 README 作用有限——而那里恰恰是大多数用户落脚的地方，因为包注册表在搜索引擎中的排名通常高于 Repo。

```bash
# Manifeste verraten die Kanäle (Deutsch)
cat package.json pyproject.toml setup.py Cargo.toml 2>/dev/null | rg -n "name|version|keywords|repository|homepage"
rg -n "npmjs.com|pypi.org|marketplace|registry|crates.io|hub.docker|zenodo|doi" README* docs/ .github/ 2>/dev/null

# Veröffentlichten Stand der Kanäle abfragen (nur was zutrifft) (Deutsch)
npm view <paket> version description keywords 2>/dev/null
pip index versions <paket> 2>/dev/null
gh release list --repo ORG/REPO --limit 5
```

典型渠道：npm, PyPI, Crates, Docker Hub, MCP Registry, 插件/Skill 目录, VS Code 或浏览器 Marketplace, App Store, Zenodo/DOI, 项目网站, 组织 Profile, `llms.txt`, 其他 Host 上的镜像 Repo。

在执行日志中记录查找到的列表。从现在起，该列表即为**目标集合**：后续步骤中的每项更改最终都要与该列表进行比对（见“所有渠道的一致性”）。如果你发现某个渠道已无人维护且指向失效状态，这是一个独立发现——要么更新它，要么主动撤回，绝不要放任不管。

### 1. 设置 Topics

Topics 是 GitHub 内部最重要的搜索入口，且几乎没有任何成本。

```bash
gh repo view ORG/REPO --json nameWithOwner,description,repositoryTopics,homepageUrl,visibility
gh repo edit ORG/REPO --add-topic <topic> --add-topic <topic>
```

目标是从三个维度设定大约 5–12 个 Topic：**它是什么** (`cli`, `mcp-server`, `python-library`)，**关于什么** (`file-management`, `tax`, `note-taking`)，以及**如何工作** (`local-first`, `offline`, `privacy`)。请参考同类项目中实际使用的 Topic——凭空捏造的 Topic 无法吸引用户。同时检查 Description 和 Homepage，它们在同一视图中展示。

Topics 在步骤 0 的其他渠道中都有对应项：`package.json` 中的 `keywords`，`pyproject.toml` 中的 `keywords`/`classifiers`，Marketplace 和 Store 中的分类与标签。请保持内容一致——它们代表同一个决策，只是体现在多个地方。

### 2a. 隐私检查关卡 (Privacy Gate) — 始终运行

无论例行维护看起来多么无害，此步骤绝不能省略。检查应在**被追踪的 (tracked)** 文件集中进行，而不是在可见的工作树中，因为这正是“看起来干净”与“实际干净”的区别所在。

```bash
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|/home/[a-z]|s[k]-[A-Za-z0-9]{16}|gh[p]_|gh[o]_|AKIA[0-9A-Z]{16}|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|BEGIN [A-Z ]*PRIVATE KEY" $(git ls-files)
rg -n "\x{C3}\x{83}|\x{C2}\x{A0}|\x{FFFD}" $(git ls-files -- '*.md' '*.txt' '*.json')
```

在匹配模式中补充**你自有的内部存储位置名称**——Pipeline 文件夹、主题目录、私有工作区：

```bash
rg -n "\.SOFTWARE|\.RESEARCH|_control-center|<weitere eigene Ordnernamen>" $(git ls-files)
```

此类引用并非 Secret，不会触发警报，因此很容易漏网——但对外部读者而言它们是**无法解析的**（“从 .SOFTWARE-Pipeline 重新传输”对陌生人毫无意义），并且暴露了内部结构。应当替换或删除它们，而不是仅仅容忍。仅搜索 `C:\Users\...` 和 Token 模式的检查保证找不到它们。

找到了内容？发现的**类型**决定了后续处理方式——请参阅“Force-Push 规则”一节。一旦某个 Secret 被 Commit 过了，它就已失效：仅从 `HEAD` 中删除是不够的，必须进行轮换 (Rotate)。

### 2b. 检查文档的发布意图

这是本次维护的核心所在。逐一检查被追踪的 `.md`, `.txt` 和 `.json` 文件，并询问每个文件：**它是否曾打算向外界公开？**

```bash
git ls-files -- '*.md' '*.txt' '*.json' | sort
```

不要凭文件名猜度——简要查看文件内容。一个 `PLAN.md` 可能是公开的 Roadmap，而听起来无害的 `notes.md` 却可能包含内部定价策略。分为三类：

**属于 Repo** — README, LICENSE, CHANGELOG, SECURITY, CONTRIBUTING, `docs/`, API 参考, 示例配置, 真正的 Roadmap, 清单文件 (`package.json`, `pyproject.toml`), Lockfile, CI 配置。

**不属于 Repo 但非敏感内容** — 本流程的常见情况。任务和规划文件 (`AUFGABEN.txt`, `Plan.txt`, `TODO-intern.md`)，Session 笔记与 Handover 文件 (`HANDOFF`, `BRIEFING`, `_handoff/`)，内部 Pipeline 的状态文件，开发日志，`_archive/`，带本地路径的 Registry 和 Index JSON，中间状态与生成的 Artifact，Agent 工作文件。此类文件没有危险，但会造成混乱并给人一种未完工现场的感觉。处理方式：补充到 `.gitignore`，执行 `git rm --cached <file>` 并**正常 Push**。

**不属于 Repo 且属于敏感内容** — 凭据 (Credentials)、个人数据、客户数据、内部测算、定价与谈判策略、未发布的商业计划、合同草案、任何具有商业竞争价值的内容。此处仅靠普通的 Commit 是不够的，请参阅 Force-Push 规则。

对于 `.json` 文件值得二次检查： Manifest 和 Lockfile 予以保留，但本地配置、任务/Registry 文件、导出 Dump 以及任何带有绝对路径或 Host 密件的内容都是典型的随带搭乘客。

如果你删除了一个别人可能会寻找的文件（例如 Roadmap），请在 Commit 或 README 中简要说明该信息现在存放在何处——否则看起来会像是退步。

### 3. Banner

Banner 很大程度上决定了读者是否会开始阅读。检查 README 中是否存在 Banner 且是否作为首个元素引入。

如果缺失，有三种途径——按以下顺序选择最为合理：

1. **Agent 的图像生成器**（例如 agy；其中的词语“generate”是生成真实 PNG 的触发词），当视觉图像比排版更合适时使用。
2. **Codex**，当 Banner 应当由代码生成且存在可供模仿的样式模版时使用。
3. **自行创建为 SVG**，当 Banner 主要是文字标识 (Wordmark) 加设计语言时——这往往是最快且最可控的方案，且 SVG 以后依然易于修改。

如果项目属于某个项目群，请保持系列一致性：相同的基色、相同的审美、相同的文字标识处理方式。一个脱离风格的 Banner 比没有 Banner 效果更差。通常尺寸为 1200x300；PNG 放入 Repo，SVG 源码存放在旁边。

### 4. 根据真实状态核对描述

这里是产生最大价值的地方。README 中作出了各种声明——请去核实它们，而不是盲目相信：

- README/Badge 中的**版本号** vs. `pyproject.toml`/`package.json`/`__version__` 以及最新的 Release Tag。如果有多个版本号载体，全部检查，不要只查一个。
- **安装路径**实际演练一遍，至少在脑海中演练：指定的名称下是否存在该包？命令和 Flag 是否正确？
- **Feature 列表** vs. 代码：提到的功能是否都在？新功能是否在列表中缺失？
- **数字**（Tool 数量、支持的格式、测试覆盖率）在源头核对计数，而不是直接顺延之前的数字。README 中的数字会静悄悄地过时。
- **截图** vs. 当前 UI。
- **Requirements**（Python/Node 版本、依赖项）vs. Manifest。
- 指向相关项目、文档和 Registry 的**链接**：它们是否依然有效？

**修改适用于所有渠道，而不仅仅是发现问题的那个渠道。** 如果某个事实陈述被证明是错误的——尤其是当委托人对其进行了更正时——那么相同的陈述极有可能也存在于其他地方：组织 Profile 中、`llms.txt` 中、第二语言版本中、相关项目的 README 中。在打勾确认前请专门搜索：

```bash
gh search code "<prägnante Formulierung>" --owner ORG
```

否则你只纠正了一处而留下了三处——直到下一个 Repo 轮到维护时才会注意到这种矛盾。这不仅浪费时间，还会损害对文档的信任：看到同一件事有两种矛盾描述的人，哪一个都不会相信。

随后在表达较弱的地方改进**排版呈现**：长选项列表改为表格形式更易读；代码块需要添加语言 Tag；结构或流程概览用 Mermaid 图表或 ASCII 树比文字描述更易快速理解；首屏高度应当展示用途、安装和使用示例，而不是 Badge 和前情提要。如果 README 超过约 400 行，将细节迁移至 `docs/` 并建立链接。

**README 的语言规则：** 标准配置是**英文 `README.md`** 加上**德文第二版本**。例外情况：应用的领域本身就是德语区（德国法律、德国税务或资助体系、德语目标受众）或者目前仅存在德文版本——此时德语保持为主语言。对于项目已支持的每种其他语言，都应包含对应的 README 版本。请遵循 Repo 中已使用的命名约定（`README_de.md`, `README.de.md`, `docs/README.de.md`），不要在旁边另创第二种规范。在 Header 中对各语言版本进行互链。

### 6. 补全缺失的标准语言

补全**标准语言**中缺失的 README：德语、英语、西班牙语、简体中文、日语、俄语。其目的是扩大受众覆盖面，因此这主要适用于面向用户的项目——对于一个纯英文受众的开发者库而言，俄文 README 没有任何收益，只会增加维护负担。请理智决策并将决策记录在执行日志中，以便下一轮维护时不再重新讨论。

新版本应当**填充内容，而不是建立后留空**——包含“TODO: translate”的 Stub 比完全没有文件更糟糕，因为它假装了完整性。内容一致性与反向同步由 `bilingual-doc-sync` 处理；当超过两个语言版本时，值得引入该 Skill 进行比对。

### 7. 可见度与推广

思考哪些措施能真正为**该**项目带来用户，并予以实施：

- 项目在技术上归属的 **Registry**：包注册表 (npm, PyPI)、MCP Registry、插件/Skill 目录、Marketplace。
- **精选列表**（`awesome-*` 和主题收录集），前提是确实符合入选标准。向一个项目不符合条件的列表提交 PR 会损害声誉。
- **自有渠道**：组织 Profile、`llms.txt`、项目网站、生态系统 README、相关自有 Repo 的引用。
- **Release Notes** 作为契机：没有宣导新特性的 Release 是不会被关注到的。

**审批关卡 (Approval Gate)：** 所有面向外部的操作——向外部 Repo 提交 PR、在外部列表中添加条目、发帖、提交申请——都属于**提议并在获得明确批准后方可执行**，除非该渠道存在长期授权。修改自有渠道不需要此关卡。原因很简单：向外部 Repo 提交后又撤回的 PR 是公开可见的，会反映到项目本身。

### 8. 在组织页面上添加条目

首先检查自己的组织：Repo 是否已列在 Profile README (`ORG/.github` → `profile/README.md`) 中、分类是否正确、Description 是否最新？

```bash
gh api user/orgs --jq '.[].login'
```

然后遍历**所有**组织，并针对每个组织回答同一个问题：访问该组织页面的访客是否会从该 Repo 中获益？通常答案是否——此时“不建立链接”是正确的结果，而不是漏洞。如果答案是肯定的（主题相关、共同用户群、补充了当地项目的工具），则添加引用，并用一行文字说明其价值，而不仅仅是列出名称。

Profile 位于独立的 Repo 中 (`ORG/.github`)。那里的修改需要同步维护并 Push——遵照步骤 11 中的 Dirty-Tree 规则。

### 10. Issue 和 Pull Request

```bash
gh issue list --repo ORG/REPO --state open --limit 50
gh pr list --repo ORG/REPO --state open --limit 30
```

深入处理它们，而不是仅仅统计数量：

- **可修复的 Bug**：直接修复——在本轮维护中上下文反正已经加载。附带测试并引用 Issue 编号的小型清晰修复。
- **已解决的 Issue**：予以关闭，并附带一句说明解决途径的话。
- **不明确的报告**：需要针对性的追问（版本、操作系统、复现步骤）。
- **PR**：认真阅读 Diff，运行测试，然后 Merge 或附带理由予以回复。一个搁置数月未回复的 PR 比礼貌拒绝消耗更多好感。
- **Stale 情况**：予以解决，而不是继续拖延。

**审批关卡：** 公开评论、带理由的关闭以及 Merge 外部贡献均属于对外沟通——在执行前提交审查，除非存在长期授权。自己 Repo 中的纯代码修复不受此限。

### 11. Commit, Push 与验证

本轮维护并不止于完成修改，而是止于将修改**推送出去**。工作树中堆满未 Push 的改进是最糟糕的结果：下一次 Session——可能是另一个 Agent 或另一台设备——必须首先适应一个陌生的、半成品的状态，而在公共渠道上没有任何改善。

在 Push 之前简要验证可测试的内容：运行测试和 Smoke Check，在修改文档时检查链接和渲染视图。然后按**主题拆分为独立的 Commit**，而不是把所有东西一股脑扔进一个大 Commit 中——清理、文档更新和 Bug 修复是三件不同的事，以后如果有人想撤销其中一项会对此心存感激：

```bash
git add .gitignore && git rm --cached <interne dateien>
git commit -m "chore: interne Arbeitsdateien aus dem Repo nehmen"
git commit -am "docs: README auf aktuellen Stand (Version, Toolzahl, Screenshots)"
git commit -am "fix: <Issue-Nummer> ..."

git pull --rebase        # bei divergiertem Branch, vor dem Push
git push
```

随后进行验证而不是盲目假设：渲染视图中的 Remote README、CI 运行状态、Release 和 Tag 状态。

```bash
gh run list --repo ORG/REPO --limit 3
gh repo view ORG/REPO --json description,repositoryTopics,url
```

**如果 CI 变红，即便你的 Commit 只动了文档**，根本原因也几乎绝非出自你的修改。最常见的情况——在这组 Repo 家族中一天内**遇到过三次**——是**未 Pin 版本的 Linter 且没有锁定规则集**。在怀疑你的 Commit 之前，请**首先**检查这一点。

其机制为：如果 Workflow 在未 Pin 依赖（`ruff>=0.12` 或完全没有版本）的情况下运行 `ruff check`（或 flake8, eslint…），且缺乏显式的规则选择（`[tool.ruff.lint] select = [...]`，若缺少 `pyproject.toml` 则缺少独立的 `ruff.toml`），那么 Linter 将遵循**每次全新安装**的版本的默认规则。新发布的 Linter 版本会改变这一默认设置，导致未修改的代码库变红。败露的迹象：

- 项目此前从未有过的规则代码 (`UP045`, `UP006`, `BLE001`, `RUF100`, `DTZ005`, `N999`…)，有时多达三位数。
- 失败往往呈现**跨平台分裂**：带有缓存旧版本的 Runner 保持绿色，全新 Runner 变为红色。
- 有时某条规则会举报无法修复的内容（`N999` 举报包名本身）——这是它从未是标准规范的铁证。

修复方案：锁定此前为绿色的规则集——`select = ["E4","E7","E9","F"]` 是 ruff 的经典默认项。如果不存在 `pyproject.toml`，请创建一个 `ruff.toml`。针对**新** Linter 版本本身进行验证（安装、在无配置下复现发现的问题、在有配置下确保通过 "passed"）。新规则作为**Task**进入项目——显式采纳是一种决策，而不是工具更新的副作用。这是一个真实的、重复出现的发现：如果不 Pin 版本，在下一次 Linter 发布时，**每一个**如此配置的 Repo 的 CI 都会再次崩溃。

两种**不**推送的情况：当项目适用发布或提交冻结期时，或者当状态明确为未完成时。两者都是需要合理理由的例外——正常情况是：Commit 并 Push。

在发布冻结期间，例行维护不会被中断，而是**重定向**：在独立的分支（`judging-hold/...`, `freeze/...`）上进行本地 Commit，保持 Main 分支在已提交状态下不受触动，在执行日志中注明冻结原因，并在解冻后追平。关键在于保持一致：被冻结的不止是 `git push`，还有**所有远程可见的变更**——Topic、Description、Homepage、Release 以及 Issue/PR 操作同样会改变已发布的项目。

如果存在该 Repo 的其他 Clone（第二台设备、部署副本、镜像），请在 Push 后立即追平它们。一个落后 10 个 Commit 的 Clone 会在下一次排错时基于一个已不存在的状态给出诊断。

#### 对其他 Repo 的修改 — Dirty-Tree 例外

本轮维护会定期在被维护 Repo **之外**产生修改：组织 Profile 中的一行文字（步骤 8），或者稍后在深度维护中相关 Repo 里的反向引用。此类修改同样需要 Commit 并 Push——未发布的反向引用等于不存在。

在动用外部 Repo 之前，简要检查其状态：

```bash
git -C <pfad> status --porcelain
```

**干净的工作树 (Clean)** → 进行修改，在**独立的、主题明确的 Commit** (`docs: link <projekt>`) 中 Commit 并 Push。不要与被维护 Repo 的 Commit 混在一起：那是另一个具有独立历史和读者的 Repo。

**Dirty，但外部修改在其他文件中** → 你自己的修改依然可以干净地完成。**按路径精确 Stage 并仅 Commit 你自己的文件**，以便未核实的外部工作不会被随带提交：

```bash
git -C <pfad> add README.md
git -C <pfad> commit -m "docs: link <projekt>"     # nur der gestagte Pfad
```

但是**不要 Push**。该 Commit 在本地是无害的；Push 则不一定：你不知道另一个工作状态最终走向何方——也许它正在被 Amend、Rebase 或重新切分，而你的 Push 会强迫对方去处理冲突。本地 Commit 保护了你的工作而不会强加于任何人；稍后轮到该 Repo 的维护流程会发现它并一并带走。

**Dirty 且恰好在你需要修改的文件中** → 不要动。此时你必须基于外部的中间状态进行构建并共同 Commit；首先去理解它所花的成本高于这一条引用的价值。

**目标 Repo 中存在激活的 Lock (`LOCK*.txt`)** → **首先阅读 Lock 内容，而不是一律视为一刀切的禁令。** Lock 会描述其自身的适用范围，而该范围通常比“完全不能动”要窄。典型情况：

- **编辑 Lock**（“当前有人在此工作”）→ 什么都不要动，包括辅助文件。
- **纯发布/Push Lock**（提交、评审、冻结）→ 本地工作依然允许，仅远程接触被禁止。在独立分支上工作并在本地 Commit；**省略远程生效的步骤**——不仅是 Push，Topics、Description、Homepage、Release 以及 Issue/PR 操作也一律省略，因为它们同样会改变已发布的项目。

将仅限制 Push 的 Lock 误读为全面禁令会白白损失整个维护流程的本地部分而没有任何安全收益。反之，仅不执行 Push 却依然修改 Metadata 也是不够的。如有疑问，引用 Lock 内容并提问。

#### 诉求绝不能丢失

如果修改由于上述任何原因而**未**执行，它将转移到目标 Repo 的任务列表中——根据当地存在的文件选择 `AUFGABEN.txt`, `TODO.md` 或 `TODO.txt`。包含日期、期望修改和原因的条目：

```markdown
- [ ] [2026-07-24, after-care] Rückverweis auf <projekt> im README ergänzen
      (übersprungen: README hatte uncommittete Fremdänderungen)
```

这就是“推迟”与“遗忘”的区别：任务列表位于该 Repo 下一位维护者无论如何都会查看的地方——比写在另一个例行流程的日志里可靠得多。如果不存在任务列表，不要新建；在自己例行流程日志里的待办事项就足够了。

在**存在激活的 Lock 时，连这一点也不适用**——此时文件不能动，记录留在自己的例行流程日志中。在这两种情况下都要在日志中予以记录，以便轮换机制了解该待办事项。

最后，处理步骤 0 中的渠道——见下一节。

## 所有分发渠道的一致性

在例行流程结束时，对照步骤 0 的列表检查：**用户能看到的每项修改都必须到达用户寻找它的每一个渠道。** 一个 npm 页面讲述着不同故事的 Repo 比只有一个渠道的 Repo 处境更差。

关键机制：**包注册表展示的是上一次 Publish 时的 README，而不是当前的 Repo 状态。** npm 或 PyPI 上的 README 更正在发布新版本之前是不可见的。如果更正包含实质内容（错误的安装、错误的版本、过时的 Feature 列表），则必须配合一次 Patch Release——否则该 Fix 将毫无效果。

| 渠道 | 那里维护的内容 | 如何到达 |
|---|---|---|
| npm | README, `description`, `keywords`, Repository 链接 | 仅通过 `npm publish`（Patch 版本）；Metadata 来自 `package.json` |
| PyPI | README (`long_description`), Classifiers, 项目 URL | 仅通过重新上传；Metadata 来自 `pyproject.toml` |
| MCP-Registry / 插件目录 | Description, 版本, Tool 列表, 入门文档 | 根据 Registry 不同，更新 Manifest 或重新提交 |
| Marketplace / Store | Description, 截图, 分类, 语言版本 | 通过对应的管理界面；截图在那些地方老化得特别快 |
| Docker Hub / Container-Registry | Description, Tag, 使用示例 | Repository Description 加新 Tag |
| Zenodo / DOI | Metadata, 作者, 版本 | Metadata 可直接编辑，内容更新需新版本 |
| 网站 / Org Profile / `llms.txt` | 简要 Description, 链接, 定位 | 可直接编辑——成本最低的渠道，因此绝不要忘记 |

在提升版本号时，**所有版本号载体**必须同时更新：Manifest, 代码常量, README Badge, Changelog, Release Tag, `llms.txt`。半提升的版本状态比全盘皆旧的状态更难诊断。

如果某个渠道上的更新目前无法进行或不合理（例如仅为了纠正错别字而发布 Release），请在执行日志中记录，以免下一轮维护将其误认为疏忽。

## Force-Push 规则

标准规则是**不进行 Force-Push**。事后将内部规划文件设为 Ignore 并不构成重写历史的理由：代价很高，每个 Clone 和 Fork 都会损坏，打开的 PR 会变得不可用——而收益很低，因为内容是无害的。标准做法：

```bash
git rm --cached <datei>            # aus dem Tracking, bleibt lokal erhalten
# .gitignore ergänzen (Deutsch)
git commit -m "chore: interne Arbeitsdateien aus dem Repo nehmen"
git push
```

仅在发生**真实泄露 (Leak)** 时，重写历史（并由此使用 `--force-with-lease` 进行 Push）才是合理的：凭据和密钥、个人数据或客户数据，以及具有真实商业竞争价值的文件——内部测算、定价策略、未公开的计划、合同细节。在此情况下：

1. **首先轮换**受影响的 Secret——此时历史已经被复制、Fork 并在 Cache 中了。轮换才起作用，删除仅是表面功夫。
2. 清理历史（`git filter-repo` 或 BFG），使用 `--force-with-lease` 推送。
3. 检查 Fork 和 Cache；必要时就孤立对象联系 GitHub Support。
4. 在执行日志中记录过程：内容、时间、进行了何种轮换。

在“非敏感”与“敏感”之间存在疑问时：按敏感处理并提交审查。两者的成本是不对称的。

## 发现应转化为 Task，而非仅仅是日志行

维护流程定期会发现超出其在同一轮中能够或应当修复的内容：缺失的语言版本、现代化滞后、未曾进行的发布。**此类发现应当在发现的时刻转化为 Task**——否则它们会悬挂在已结束流程的日志里，而项目的下一位维护者不会去那里查看。

Task 属于**项目文件夹本地的 Task 系统**——属于下一位在此项目上工作的人会查看的地方。通常是项目文件夹中的 `AUFGABEN.txt` 或 `TODO.md`，而该文件夹往往**不在 Git Clone 中**，而是在规划存放的目录里。Clone 包含代码，项目文件夹包含管理；在下一次 `git clean` 时消失的 Clone 内条目不是 Task。

注意三件事：

1. **将内部 Task 列表与公开 Roadmap 区分开。** 一个 `TODO.md` 可能是维护良好的公开 Roadmap——此时它不是存放内部后续工作的地方。在追加内容前先看一眼：如果那里有形如“Public roadmap”的标题，请写在旁边的内部文件 (`AUFGABEN.txt`) 中并标记为内部。
2. **检查现有条目，而不是重复创建。** 往往发现的问题已经写在那里了。此时不要新建，而是进行**丰富**——用本次运行中的实证证据（“已确认：`--help` 输出完全为德语”）。带新鲜证据的已知事项比旁边的第二个条目更有价值。
3. **记录已完成事项。** 本轮流程修复的内容应作为带 Commit Hash 的已打勾事项附上。这向下一轮维护解释了为何某个发现消失了，并防止其再次被“发现”。

表述 Task 时使其在没有本次运行上下文的情况下也能被理解：发现了什么、为什么重要、下一步是什么。“i18n 不完整”不是 Task；“目录仅包含 `status.title`，es/zh/ja/ru 为空——先将 CLI 字符串提取到目录中，然后填满所有六种语言”才是 Task。

## 执行日志

将结果记录在 `_after-care/LOG.md` 中（该文件夹应列入 `.gitignore`——它是 Pipeline 材料，不是 Repo 内容，完全符合步骤 2b 的规则）。每一轮占一行，包含日期、阶段和明确的决策：

```markdown
## 2026-07-24 — surface
- Flächen: GitHub, npm (<paket>), MCP-Registry, Org-Profil, llms.txt
- Topics: +local-first, +mcp-server; keywords in package.json angeglichen
- Entfernt: AUFGABEN.txt, _handoff/ (gitignored, kein Force-Push nötig)
- README: Version 0.9 -> 1.2 korrigiert, Toolzahl 23 -> 26 nachgezählt
- Sprachen: EN + DE gepflegt; ES/ZH/JA/RU bewusst nicht (entwicklernahes Publikum)
- Issues: #12 gefixt, #7 geschlossen (erledigt), #15 Rückfrage gestellt
- Push: 3 Commits, CI grün; npm-Republish 1.2.1 wegen README-Korrektur
- Offen: Store-Screenshots veraltet, brauchen neuen Build
```

日志避免了下一轮重复作出相同的决策，并且是跨多个 Repo 进行轮换维护（`rotation-check`）的基础。

## 常见错误

| 错误 | 纠正措施 |
|---|---|
| 只查看了工作树，没有查看 `git ls-files` | 始终检查被追踪的文件集——问题出在那里 |
| 隐私关卡仅针对路径和 Token | 同时搜索自有的 Pipeline/文件夹名称——它们不会触发警报，容易漏网 |
| 删除内部文件时重写了历史 | 对于非敏感文件，`git rm --cached` + 普通 Push 就足够了 |
| 从 `HEAD` 中删除了 Secret 即认为已解决 | 轮换 Secret；其他一切都只是表面功夫 |
| 仅凭文件名对文件进行分类 | 简要查看内部内容——文件名无法可靠反映意图 |
| README 中的数字直接顺延而不是重新计数 | 在源头计数（Tool 列表、测试运行、Manifest） |
| 将新语言版本建立为简陋的空 Stub | 填充内容或不建立——Stub 虚假地假装了完整性 |
| 在现有规范旁引入了第二种 README 命名约定 | 沿用现有的命名约定 |
| 未经批准向外部列表提交了 PR | 外部沟通需先提交审查；仅自有渠道可自由操作 |
| 仅统计 Issue 数量而未深入处理 | 修复、关闭或针对性追问——每一个案例都有明确状态 |
| 擅自以异样风格生成了 Banner | 遵循生态系统的设计语言系列 |
| 纠正了 Repo 中的 README，但 npm/PyPI 页面仍显示旧版 | Registry 页面来自上一次 Publish——补上 Patch Release |
| 仅在 Manifest 中提升了版本号 | 所有版本号载体同时提升：Manifest, 代码, Badge, Changelog, Tag, `llms.txt` |
| 更改已完成，但留着未 Push | Commit 和 Push 属于例行流程的一部分；仅冻结期构成例外理由 |
| 所有东西合并在一个 Commit 中 | 区分清理、文档和修复——否则无法单独撤销任何一项 |
| 文档 Commit 后 CI 变红，怀疑是自己的问题 | 未 Pin 的 Linter 在缺乏 `select` 时遵循新版本的默认值——锁定规则集 |
| 仅在发现问题的地点纠正了错误声明 | 组织范围内搜索该表述——它通常也存在于 Org Profile、`llms.txt` 和第二语言版本中 |
| 在 Dirty 的第三方 Repo 中使用了 `commit -a` | 按路径精确 Stage 并 Commit，不要 Push——第三方工作保持不动 |
| 在 Clean 的 Org Profile Repo 中作了修改但未 Push | Clean 的第三方 Repo 获得独立的 Commit **以及**独立的 Push |
| 跳过的修改仅记录在自己的日志中 | 额外写入目标 Repo 的 Task 列表中（如果存在） |
| 发现仅写在执行日志中 | 转化为文件夹本地 Task 系统中的 Task——以后没人看旧日志 |
| 内部后续工作挂在公开 Roadmap 上 | 先查看内容；“Public roadmap”意味着使用旁边的内部文件 |
| 将已知发现重复创建为新条目 | 用本次运行的实证证据丰富现有条目 |
| 在编辑冻结期间将 TODO 行写入被冻结的 Repo | 编辑冻结适用于整个项目——那里什么都不要动 |
| 将 Push 冻结误读为全面禁令并完全跳过了 Repo | 阅读 Lock：如果仅限制发布，本地维护在独立分支上继续 |
| 在 Push 冻结下虽未 Push 但修改了 Topic 或 Description | Metadata 在远程同样可见——在发布冻结下同样省略 |

## 最终检查清单

- [ ] 已确认分发渠道并在执行日志中记录。
- [ ] 已设置并检查 Topics, Description 和 Homepage。
- [ ] 已在被追踪的文件集上运行隐私关卡，并处理了发现的问题。
- [ ] 已检查 `.md`/`.txt`/`.json` 的发布意图，忽略了内部文件。
- [ ] 无真实泄露绝不 Force-Push；若有泄露已执行轮换。
- [ ] Banner 存在且已在 README 中引入。
- [ ] 版本、Feature、数字、截图、链接已根据真实状态进行核对。
- [ ] 已改进呈现效果（表格、图表、首屏高度）。
- [ ] README 语言矩阵完整；关于其他语言的决策已记录。
- [ ] 已实施可见度措施或已提交审批。
- [ ] 已检查自有 Org Profile 中的条目，已放置合理的第三方 Org 引用。
- [ ] 对第三方 Repo 的修改：Clean → Commit 并 Push；Dirty → 本地 Commit；
      未执行 → 已写入目标 Repo 的任务列表。
- [ ] Issue 和 PR 已处理至明确状态。
- [ ] 已创建独立的 Commit 并 Push，CI 和远程视图已验证。
- [ ] 所有分发渠道已保持同一状态（必要时进行 Patch Release）。
- [ ] 未解决的发现已作为 Task 写入文件夹本地 Task 系统。
- [ ] 执行日志已写入 `_after-care/LOG.md`。

## 变更日志

### 1.6.0 (2026-07-24)
- 补充规则：实质内容的纠正适用于所有渠道。经验教训——
  用户做出的澄清在第 1 轮中于 Hub 内进行了纠正，但不知不觉中还在组织 Profile（EN, DE, `llms.txt`）
  中存在 5 处，直到 9 轮之后才被注意到。

### 1.5.0 (2026-07-24)
- 在一天内模式出现 3 次后加严了 Linter 诊断
  (n8n-workflow-manager ruff 0.15, clirec + swarm-ai ruff 0.16)：“首先检查”，具体的
  败露规则代码，平台分裂，在缺少 `pyproject.toml` 时将 `ruff.toml` 作为 Fix，
  针对新 Linter 版本本身进行验证。

### 1.4.0 (2026-07-24)
- 补充诊断：如果 CI 在纯文档 Commit 后变红，最常见的原因是未 Pin 的 Linter 且缺乏
  锁定规则集——新工具发布改变了默认值并使未修改的代码变红。Fix：锁定规则集，新规则作为 Task。
  连续出现两次（n8n-workflow-manager 搭配 ruff 0.15，clirec 搭配 0.16）。

### 1.3.0 (2026-07-24)
- 新增“发现应转化为 Task”一节：本轮未能自行修复的内容，在发现的时刻转化为项目文件夹
  本地 Task 系统中的一个条目——存放在下一位维护者查看的地方，而不是已结束流程的日志里。
  包含内部列表与公开 Roadmap 的区分、丰富而非重复、带 Commit 的已完成事项。

### 1.2.0 (2026-07-24)
- 隐私关卡额外搜索自有内部存储位置的名称。它们不是 Secret，因此不会触发警报，
  能够穿透仅针对路径和 Token 的关卡——但对读者而言依然无法解析，并且暴露了自有的结构。

### 1.1.0 (2026-07-24)
- 审读 Lock 而不是一律视为一刀切禁令：纯发布/Push Lock 将维护流程重定向至本地分支，
  而不是终止流程。同时明确在如此 Lock 下 Metadata、Release 以及 Issue/PR 操作
  也一律省略——它们与 Push 一样在远程可见。

### 1.0.0 (2026-07-24)
- 初始版本。Repo 后续维护阶段 1，衍生自 `github-repo-care`。
