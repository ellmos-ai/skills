---
name: grill-me
description: "一种毫不松懈、持续追问的访谈方式,用于打磨计划或设计。当用户说“grill me”、“grill mich”、“grill mich zu diesem Plan”、“拷问我”、“对我进行连环追问”,或明确调用 /grill-me 时使用。对于“review this”、“poke holes”、“stress-test”、“devil's advocate”、“critique”、“帮我审查一下”、“挑挑毛病”、“压力测试”、“唱反调”或“批评点评”等泛泛表述,本技能不会触发——若要审查已写好的产出(代码、PR、论文),请改用 code-review、3agenten-review、7phasen-review 或 caveman-review;grill-me 则是在计划或想法尚未落地构建之前对其进行质询。"
disable-model-invocation: true
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: zh
translated_from_sha256: 6074974f754dbd47e47fe7abbf10df62f7177cddba8d2fe20e6c581d9935d2b1
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:49.872870+00:00"
---
<img src="banner.png" width="100%" alt="grill-me banner">

使用 Skill 工具调用 "grilling"。

<!--
Vendored from mattpocock/skills (skills/productivity/grill-me/SKILL.md, MIT
License, Copyright (c) 2026 Matt Pocock -- see LICENSE next to this file).

Modification vs. upstream: the `description` field was extended with German
trigger phrases ("grill mich") and an explicit non-trigger/abgrenzung note
against this library's existing artifact-review skills (code-review,
3agenten-review, 7phasen-review, caveman-review). The `category` and
`language` fields and this comment were added; all are local convention
(recommended, not one of the nine house fields), not upstream content, and
`language: en` reflects that the vendored body is unmodified English.
The body (the single instruction line) and `disable-model-invocation: true`
are unchanged from upstream.

Adopted 2026-08-24 per Ticket T-20260824-594031458: the user asked whether a
"grill me" skill exists; none did locally, and this upstream implementation
(design-tree / frontier / rounds interrogation, see skills/third-party/grilling/)
is the well-known, MIT-licensed original that the term "grill me" refers to
in the current Claude Code skill ecosystem -- adopted rather than
independently re-implemented.
-->
