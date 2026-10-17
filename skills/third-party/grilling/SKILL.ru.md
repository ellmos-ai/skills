---
name: grilling
description: "Безжалостно допрашивать пользователя о плане, решении или идее. Использовать, когда пользователь хочет проверить свои рассуждения на прочность или использует любую фразу-триггер с «grill», включая немецкие, например «grill mich», «grill mich zu diesem Plan» или «zerpflück meinen Plan im Grill-Modus». Точка входа для команды /grill-me; может также вызываться напрямую."
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: ru
translated_from_sha256: 7f0fe16de62ea366d79b723cbf52cd65c3f237415352cfa870ba0b12cf4fef53
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.248639+00:00"
---
<img src="banner.png" width="100%" alt="grilling banner">

Допрашивайте пользователя безжалостно, пока не достигнете общего понимания. Представьте это как **дерево проектирования**: каждое решение ветвится на решения, которые от него зависят.

Обходите дерево **раундами**. **Фронтир** — это все решения, предпосылки которых уже определены: вопросы, которые можно задать _прямо сейчас_, не угадывая ответов, которых вы ещё не услышали. Задайте весь фронтир за один раунд: пронумеруйте вопросы и укажите свой рекомендуемый ответ. Затем дождитесь ответов пользователя перед следующим раундом.

Оформляйте раунд так:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Каждый раунд, ответы пользователя перестраивают дерево: определённые решения расширяют фронтир и открывают вопросы, которые от них зависели. Пересчитайте фронтир и задайте следующий раунд. Вопрос, ответ на который зависит от другого вопроса, ещё открытого в этом раунде, относится к _более позднему_ раунду, а не к этому.

Поиск _фактов_ — ваша задача, а не пользователя. Когда для вопроса фронтира нужен факт из окружения (файловая система, инструменты и т. п.), запустите подагента, чтобы его найти; не спрашивайте пользователя о том, что можете выяснить сами. Не блокируйтесь на этом: выполняющееся исследование — это неопределённая предпосылка, поэтому ждать отчёта подагента нужно только вопросам, которые от него зависят; остальной фронтир задайте сейчас. _Решения_ принадлежат пользователю: выносите каждое на его рассмотрение и ждите.

Сессия завершена, когда фронтир пуст: каждая ветвь дерева проектирования пройдена, ничего не принято молча на веру. Не действуйте, пока пользователь не подтвердит, что вы достигли общего понимания.

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
