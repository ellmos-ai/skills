---
name: grilling
description: "对某个计划、决定或想法对用户进行不留情面的追问。当用户希望对其思路进行压力测试，或使用任何\"grill\"触发短语时使用——包括德语的，例如\"grill mich\"、\"grill mich zu diesem Plan\"或\"zerpflück meinen Plan im Grill-Modus\"。中文触发短语包括“拷问我”、“就这个计划拷问我”和“用拷问模式彻底挑战我的计划”。作为 /grill-me 命令的入口点；也可直接调用。"
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: zh
translated_from_sha256: 7f0fe16de62ea366d79b723cbf52cd65c3f237415352cfa870ba0b12cf4fef53
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.160760+00:00"
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

<!--
Vendored from mattpocock/skills (skills/productivity/grilling/SKILL.md, MIT
License, Copyright (c) 2026 Matt Pocock -- see LICENSE next to this file).

Modification vs. upstream: the `description` field was extended with German
trigger phrases ("grill mich"). The `category` and `language` fields and this
comment were added; all are local convention (recommended, not one of the
nine house fields), not upstream content, and `language: en` reflects that
the vendored body is unmodified English. The body (the design tree / frontier
/ rounds method) is unchanged from upstream.

Adopted 2026-08-24 per Ticket T-20260824-594031458 alongside skills/third-
party/grill-me/ (the thin, explicit-only entry point that calls this skill).
-->
