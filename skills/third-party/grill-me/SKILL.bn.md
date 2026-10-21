---
name: grill-me
description: "একটি নিরলস সাক্ষাৎকার যা কোনও পরিকল্পনা বা নকশাকে ধারালো করে তোলে। ব্যবহারকারী যখন বলেন \"grill me\", \"grill mich\", \"grill mich zu diesem Plan\", আমাকে জেরা করো, এই পরিকল্পনা নিয়ে আমাকে জেরা করো, অথবা স্পষ্টভাবে /grill-me আহ্বান করেন তখন ব্যবহার করুন। সাধারণ \"review this\", \"poke holes\", \"stress-test\", \"devil's advocate\" বা \"critique\" ধরনের বাক্যাংশে (বাংলায়: এটি পর্যালোচনা করো, ত্রুটি খোঁজো, চাপ-পরীক্ষা করো, বিপক্ষ যুক্তি দাও, সমালোচনা করো) এটি সক্রিয় হয় না -- ইতিমধ্যে লেখা কোনও artifact (code, PR, paper) পর্যালোচনার জন্য এর পরিবর্তে code-review, 3agenten-review, 7phasen-review বা caveman-review ব্যবহার করুন; grill-me নির্মাণের আগে এখনও খোলা পরিকল্পনা বা ধারণাকে যাচাই করে।"
disable-model-invocation: true
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: bn
translated_from_sha256: 6074974f754dbd47e47fe7abbf10df62f7177cddba8d2fe20e6c581d9935d2b1
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:49.872870+00:00"
---
<img src="banner.png" width="100%" alt="grill-me banner">

Skill টুলটিকে "grilling" দিয়ে কল করুন।

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
