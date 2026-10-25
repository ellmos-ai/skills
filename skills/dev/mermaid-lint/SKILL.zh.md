---
name: mermaid-lint
version: 1.0.0
type: tool
author: Lukas Geiger + Claude
created: 2026-09-20
updated: 2026-09-20
aliases: [mermaid, mermaid-fehler, diagramm-render-fehler, unable-to-render-rich-display, schaltplan-fehler]
description: "查找并修复 GitHub 无法渲染的 Mermaid 图表（\"Unable to render rich display\"）。使用真实的 Mermaid 解析器逐个检查每个 ```mermaid 代码块，无需浏览器；随后在线上的 GitHub 页面中核实结果。"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [mermaid, markdown, github, readme, diagramm, lint, dokumentation]
language: zh
status: active
visibility: public
dependencies: {'tools': ['node', 'git'], 'services': ['GitHub'], 'protocols': [], 'python': [], 'npm': ['mermaid', 'jsdom', 'playwright-core']}
translated_from_sha256: a1286c3571792da726aea23967c12360cb0daadb8d3d0bce2208ff27fc14bce9
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="mermaid-lint banner">

# mermaid-lint

一个语法有误的 Mermaid 图表在 GitHub 上不会显示图形，而是显示方框
**"Unable to render rich display"**。本地不易察觉，因为没有任何工具检查这些代码块。本技能填补了这一空白。

## 适用场景

- README 或文档在 GitHub 上显示渲染错误，而不是图表。
- 发布或发行前，文档中包含图表。
- 每次修改涉及 Mermaid 代码块的 Markdown 之后。
- 跨多个仓库全面检查，当不清楚哪些地方存在问题时。

## 两个工具

### 1. `mermaid_lint.mjs` —— 无浏览器的语法检查

```
node mermaid_lint.mjs <repo-pfad> [...] [--json]
node mermaid_lint.mjs --from <liste.txt> [--json]
```

递归查找所有 `.md` 文件，提取每个 ```mermaid 代码块，并交由 `mermaid.parse()` 处理——**与 GitHub 在浏览器中使用的解析器相同**。
退出码 0 = 所有代码块均可解析，退出码 1 = 至少一个代码块有误。输出会给出文件、代码块编号、行号以及原始解析错误信息。

`--from <datei>` 读取一个路径列表，每行一个。请使用它，而不是传入大量参数：
带反斜杠的 Windows 路径会在 Bash shell 中被悄悄破坏
（`D:\code\my-repo` 会变成 `D:codemy-repo`）。请使用正斜杠书写路径。

单个进程即可处理数百个仓库，因为 Mermaid 只需加载一次。
无需 Puppeteer，也无需下载 Chromium。

### 2. `readback.mjs` —— 在线页面的验证

```
node readback.mjs <github-url> [...]
```

在已安装的 Edge 中打开页面（不下载浏览器），并统计真实的渲染错误。每个页面的判定结果为 `OK`、`DEFEKT`、`UNKLAR` 或 `KEIN-MERMAID`。

## 导致本技能必要性的三个陷阱

**GitHub 在沙箱化的 iframe 中渲染 Mermaid**，来源于 `viewscreen.githubusercontent.com`。
主页面看不到其中的内容。如果只检查 `document.body.innerText` 或 `msedge --dump-dom`，即使在确实有问题的页面上，也会报告**每个**页面零错误。因此 `readback.mjs` 会检查所有 frame。

**单次 DEFEKT 结果并不可靠。** 加载过程中，GitHub 会短暂显示一个看起来像渲染错误的占位符。2026-09-20 的测量显示：同一页面先报告了 `ERR=1`，随后两次报告 `ERR=0`。`readback.mjs` 会自动重复否定结果；`OK` 则从不重复。

**`mermaid.parse()` 需要 DOM**，否则会在 `DOMPurify.addHook` 处失败，并把有效的流程图误报为有问题。`mermaid_lint.mjs` 会预先提供一个 jsdom 窗口。即便如此，若仍残留环境错误，它会单独归入 `envIssues`，并且**不**计为语法错误。

## 始终用负对照检验

在相信绿色结果之前，先让工具检查一个你知道有问题的版本——例如修复前的提交：

```
node readback.mjs "https://github.com/<org>/<repo>/blob/<alter-sha>/README.md"
```

如果它也报告 `OK`，说明你的回读没有测到任何东西。上面的 iframe 陷阱正是这样被发现的。

## 常见错误原因及最小侵入式修复

| 解析错误中的症状 | 原因 | 修复 |
|---|---|---|
| `Expecting '+', '-', '()', 'ACTOR', got 'loop'` | 参与者名称与保留字相同：`loop`、`alt`、`opt`、`par`、`end`、`critical`、`break`、`rect`、`note` | 声明别名：`participant L as Loop`，消息中使用 `L`。**显示名称保持不变**——不要重命名。 |
| 流程图中的 `got 'PS'` | 节点标签中含圆括号 | 为标签加引号：`A["Start (hier)"]` |
| `Lexical error ... Unrecognized text` | 标签中含反引号或冒号 | 为标签加引号，去掉反引号 |
| `Expecting 'SEMI', 'NEWLINE', 'EOF'` 出现在 `graph`/`flowchart` 中 | `Note:` 仅在时序图和类图中可用 | 将提示文字移出代码块，作为其下方的 Markdown 行，以保证信息可见 |
| 时序图中的 `Expecting 'SOLID_OPEN_ARROW' ... got 'NEWLINE'` | 消息文本中含 **HTML 实体**（`&lambda;`、`&Delta;`、`&ge;`）。此处括号和 `=` 本身没有问题——但实体结尾的 `;` 会被词法分析器当作语句结束符，其后的内容都变成新语句。 | 用字面字符替换实体（λ、Δ、≥），其余文本保持不变。括号可以保留。数值及其写法绝不修改。 |
| 时序消息中的分号 | 被读取为语句结束 | 替换为 ` - ` |

在**带引号的流程图标签**中，实体没有问题——该规则仅适用于时序消息。`mermaid_lint.mjs` 会将此类实体作为单独的 `[WARN]` 行报告（JSON 中的字段为 `warnings`），与解析错误并列：解析器只会报告 `got 'NEWLINE'`，而不说明原因。

**原则：** 最小侵入。在可能的范围内，保持布局、节点 ID、顺序和可见文本不变。在科研类仓库中，这一点尤其适用于数值及其写法。对于英德双语版本（EN/DE）的一致性，两个版本的结构应保持一致。

## 跨多个仓库的流程

1. 通过 `gh repo list <org> --limit 200 --json name,isArchived,isPrivate,defaultBranchRef` 生成清单。
2. 克隆仓库并**拉取远程最新状态**，认真对待分歧。在过时的克隆上检查，测到的是错误的状态。如果 `git pull --ff-only` 失败，应对照 `origin` 而不是工作区进行检查：`git archive origin/<branch> | tar -x -C <tempdir>`，然后检查临时目录。
3. **不同组织中同名的仓库**（典型如 `.github`）不得映射到同一个克隆——否则会把同一个仓库检查九遍。遇到名称重复时，应平铺克隆到 `<org>__<repo>` 下，并检查新拉取的状态。
4. 每次修改前检查锁（克隆中的 `lock_scan.py`、`LOCK*.txt` **以及** OneDrive 项目路径），设置自己的锁，推送后再移除。**要读取锁的范围，而不只是检查其是否存在：** 已过期的 `expires_after` 锁 `LOCK.team.*` 可以忽略；`LOCK.user.zenodo-upload.txt` 仅锁定外部 Zenodo 写入操作，并明确允许文档修改。相反，`LOCK.user.until-winners-announcement.txt`（评审中）会阻止任何推送——此时只做只读检查，并把发现的问题记录为工单。
5. 修复，检查直至全部通过，提交，`git pull --rebase`，推送。
6. 进行带负对照的回读。只有这样才算完成。

## 安装

```
npm install mermaid jsdom playwright-core
```

可放在脚本文件夹中，也可全局安装；`playwright-core` 使用已安装的 Edge（`channel: 'msedge'`），不会下载自己的浏览器。仅回读需要它——语法检查无需它即可运行。

## 相关内容

- GithubBot 中的 `_tools/lint_mermaid.py`：较早的基于正则表达式的 linter，带有 `--fix`。它会自动修复已知模式，但**不认识保留字**，无法替代本技能。推荐顺序：先用 `mermaid_lint.mjs` 进行诊断，然后视情况用 `lint_mermaid.py --fix` 处理批量模式，最后再次检查。
- `github-repo-care`：仓库维护与发布的总体流程文档。
