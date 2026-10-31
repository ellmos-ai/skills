---
name: grilling
description: "围绕某个计划、决定或想法持续追问用户。当用户想压力测试自己的思路、说“grill me”或“grill-me”（旧命令 /grill-me 已由 /grilling 替代），或使用其他含“grill”的触发短语时使用；这也包括德语短语“grill mich”“grill mich zu diesem Plan”“zerpflück meinen Plan im Grill-Modus”和中文短语“拷问我”“就这个计划拷问我”“用拷问模式彻底挑战我的计划”。规划会话结束后，如果用户询问是否还有未解决事项，也使用此技能。"
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: zh
translated_from_sha256: 5d1b8c01ac7dc1437fe7c47e90506f755b22bdd9df0555a5f556e96921337a3b
translator: "claude-haiku-5-5 + Codex GPT-6 (Luna)"
translated_at: "2026-10-25T11:15:53+00:00"
---
<img src="banner.png" width="100%" alt="grilling banner">

毫不留情地追问用户，直至双方达成共同理解。将其映射为一棵**设计树**：每个决策都会分支出依赖于它的子决策。

以**轮次**推进树的遍历。**前沿**是指所有前置条件已经确定的决策：即你现在就能提出、无需猜测尚未听到的答案的问题。在一轮中提出整个前沿：为每个问题编号并给出你推荐的答案。然后等待用户回答，再进入下一轮。

一轮的格式如下：

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

用户每一轮的回答都会重塑这棵树：已确定的决策将前沿向外推进，并解锁依赖它们的问题。重新计算前沿，然后提出下一轮问题。如果某个问题的答案取决于本轮中仍未解决的另一个问题，则它属于**后续**轮次，而不是本轮。

查找*事实*是你的工作，而不是用户的。当某个前沿问题需要来自环境（文件系统、工具等）的事实时，派遣子代理去查找；不要询问用户你自己就能查到的任何信息。不要因此阻塞：一个正在运行的探索是尚未确定的前置条件，因此只有依赖它的后续问题才需要等待子代理报告；现在就提出前沿中的其余问题。*决策*属于用户：将每个决策交给用户并等待其回答。

当前沿为空时，会话即告结束：设计树的每个分支都已被访问，且没有任何内容被悄悄假定。在用户确认你们已达成共同理解之前，不要据此采取行动。

## 本地补充规则

这些规则扩展原有方法，但不改变它。

1. **从已有记录开始构建决策树。** 第一轮前，阅读计划以及项目记录决策的位置，收集所有仍处于开放、提议或未确认状态的事项。不要重新询问已经决定的事项；引用已有记录即可。
2. **在进入下一轮前记录每个回答。** 将每个回答写入项目决策记录，标记为已决定，并附上日期和来源。只留在聊天中的回答会在下次上下文重置后丢失。
3. **遇到打断时暂停，不要重启。** 如果用户要求先做其他事，就先完成它，再从剩余的开放问题继续。已经解决的问题仍视为已解决。
4. **每条建议都给出一个理由。** 说明推荐的答案以及支撑它的那一条事实或规则。用户确认之前，建议不构成决定。
5. **展示你核实过的事实。** 如果问题依赖于从环境中查到的事实，说明发现了什么以及来源在哪里，让用户依据证据作决定。
6. **使用用户的语言提问。** 问题和建议都使用用户的语言；标识符保持原样。
7. **用决策清单收尾。** 当前沿为空时，列出已经决定的事项和有意保留为未决的事项，然后请用户确认双方是否达成共同理解。

<!--
Vendored from mattpocock/skills (skills/productivity/grilling/SKILL.md, MIT
License, Copyright (c) 2026 Matt Pocock -- see LICENSE next to this file).

Improved fork. Modifications vs. upstream:
- `description`: German trigger phrases ("grill mich"), the "grill me" /
  "grill-me" phrases, and the end-of-planning trigger were added.
- `category`, `language` and this comment were added (local convention).
- "Local additions" (rules 1-7) were appended after the upstream body. The
  upstream body above that heading is unchanged, so a resync only needs to
  replace that part.

Adopted 2026-08-24 per Ticket T-20260824-594031458, together with the thin
entry point skills/third-party/grill-me/ (upstream
skills/productivity/grill-me, `disable-model-invocation: true`, body
"Call the Skill tool with grilling"). On 2026-10-25 grill-me was removed at
the user's request: one skill instead of two, the phrase triggers moved into
this description. The native /grill-me command no longer exists; /grilling
replaces it. The description only adds semantic matching and registers no
alias command. Rules 1-7 come from a planning session of the same day.
-->
