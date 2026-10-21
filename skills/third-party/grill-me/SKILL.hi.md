---
name: grill-me
description: "एक निर्मम साक्षात्कार जो किसी योजना या डिज़ाइन को धारदार बनाता है। तब उपयोग करें जब उपयोगकर्ता कहे \"grill me\" (मुझसे कड़े सवाल पूछो), \"grill mich\", \"grill mich zu diesem Plan\" (मुझे ग्रिल करो), या स्पष्ट रूप से /grill-me का आह्वान करे। सामान्य \"review this\" (इसकी समीक्षा करो), \"poke holes\" (कमियां निकालो), \"stress-test\" (तनाव-परीक्षण करो), \"devil's advocate\" (विरोधी पक्ष लो) या \"critique\" (आलोचना करो) वाक्यांशों पर यह सक्रिय नहीं होता -- पहले से लिखे गए किसी artifact (कोड, PR, पेपर) की समीक्षा के लिए इसके बजाय code-review, 3agenten-review, 7phasen-review या caveman-review का उपयोग करें; grill-me किसी अभी भी खुली योजना या विचार की जांच उसे बनाए जाने से पहले करता है।"
disable-model-invocation: true
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: hi
translated_from_sha256: 6074974f754dbd47e47fe7abbf10df62f7177cddba8d2fe20e6c581d9935d2b1
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="grill-me banner">

"grilling" के साथ Skill tool को कॉल करें।

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
