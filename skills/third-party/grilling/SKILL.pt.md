---
name: grilling
description: "Interrogue o usuário de forma implacável sobre um plano, decisão ou ideia. Use quando o usuário quiser testar seu raciocínio sob pressão, ou usar qualquer expressão de gatilho com \"grill\" -- incluindo gatilhos em português, como \"me interrogue sobre este plano\" ou \"destrinche meu plano no modo grill\", e versões em alemão como \"grill mich\", \"grill mich zu diesem Plan\" ou \"zerpflück meinen Plan im Grill-Modus\". Ponto de entrada para o comando /grill-me; também pode ser invocado diretamente."
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: pt
translated_from_sha256: 7f0fe16de62ea366d79b723cbf52cd65c3f237415352cfa870ba0b12cf4fef53
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="grilling banner">

Entreviste o usuário de forma implacável até chegar a um entendimento compartilhado. Mapeie isto como uma **árvore de design**: cada decisão se ramifica nas decisões que dela dependem.

Percorra a árvore em **rodadas**. A **fronteira** é o conjunto de todas as decisões cujos pré-requisitos já estão resolvidos: as perguntas que você pode fazer _agora_ sem adivinhar respostas que ainda não ouviu. Pergunte toda a fronteira em uma só rodada: numere cada pergunta e forneça sua resposta recomendada. Em seguida, aguarde as respostas do usuário antes da próxima rodada.

Formate uma rodada da seguinte forma:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Cada rodada, com as respostas do usuário, remodela a árvore: decisões resolvidas empurram a fronteira para fora e desbloqueiam perguntas que dependiam delas. Recalcule a fronteira e faça a próxima rodada. Uma pergunta cuja resposta depende de outra pergunta ainda aberta nesta rodada pertence a uma rodada _posterior_, não a esta.

Descobrir _fatos_ é sua tarefa, nunca a do usuário. Quando uma pergunta da fronteira exigir um fato do ambiente (sistema de arquivos, ferramentas etc.), delegue a um sub-agente para encontrá-lo; não peça ao usuário nada que você mesmo possa consultar. Não bloqueie por causa disso: uma exploração em andamento é um pré-requisito não resolvido, então apenas as perguntas que dependem dela aguardam o relatório do sub-agente; faça as demais perguntas da fronteira agora. As _decisões_ são do usuário: apresente-as a ele e aguarde.

A sessão termina quando a fronteira estiver vazia: cada ramo da árvore de design foi visitado, sem nada deixado em suposição silenciosa. Não aja com base no resultado da sessão até que o usuário confirme que chegaram a um entendimento compartilhado.

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
