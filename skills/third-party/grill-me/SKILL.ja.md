---
name: grill-me
description: "計画や設計を鋭くするための容赦ない質問インタビュー。ユーザーが「grill me」「grill mich」「grill mich zu diesem Plan」「グリルして」「私を質問攻めにして」と言った場合、または /grill-me を明示的に呼び出した場合に使用する。一般的な「review this」「poke holes」「stress-test」「devil's advocate」「critique」「レビューして」「穴を探して」「ストレステスト」「悪魔の代弁者」「批評して」といった表現では発動しない。すでに書かれた成果物(コード、PR、論文)のレビューには、代わりに code-review、3agenten-review、7phasen-review、または caveman-review を使用すること。grill-me は、まだ構築前の未完成の計画やアイデアを問いただすためのものである。"
disable-model-invocation: true
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: ja
translated_from_sha256: 6074974f754dbd47e47fe7abbf10df62f7177cddba8d2fe20e6c581d9935d2b1
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:49.872870+00:00"
---
<img src="banner.png" width="100%" alt="grill-me banner">

Skillツールを「grilling」で呼び出してください。

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
