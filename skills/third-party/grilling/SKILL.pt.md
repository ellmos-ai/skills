---
name: grilling
description: "Interrogue o usuário sem trégua sobre um plano, uma decisão ou uma ideia. Use esta skill quando ele quiser testar seu raciocínio, disser “grill me” ou “grill-me” (o antigo comando /grill-me foi substituído por /grilling), ou usar outra expressão de gatilho com “grill”, incluindo as expressões em português “me interrogue sobre este plano” e “destrinche meu plano no modo grill” e as alemãs “grill mich”, “grill mich zu diesem Plan” e “zerpflück meinen Plan im Grill-Modus”. Use-a também quando uma sessão de planejamento terminar e o usuário perguntar se ainda há algo em aberto."
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: pt
translated_from_sha256: 5d1b8c01ac7dc1437fe7c47e90506f755b22bdd9df0555a5f556e96921337a3b
translator: "claude-haiku-5-5 + Codex GPT-6 (Luna)"
translated_at: "2026-10-25T11:15:53+00:00"
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

## Adições locais

Estas regras ampliam o método original, sem alterá-lo.

1. **Comece pelo que já está registrado.** Antes da primeira rodada, leia o plano e o local onde o projeto registra suas decisões. Reúna todos os pontos ainda abertos, propostos ou não confirmados. Não pergunte de novo o que já foi decidido; cite o registro.
2. **Registre cada resposta antes da rodada seguinte.** Anote cada resposta no registro de decisões do projeto como decidida, com data e fonte. Uma resposta que só existe no chat se perde na próxima redefinição de contexto.
3. **Pause em vez de recomeçar quando houver uma interrupção.** Se o usuário pedir outra coisa primeiro, faça isso e depois retome os pontos ainda abertos. O que já foi resolvido continua resolvido.
4. **Dê um motivo para cada recomendação.** Apresente a resposta recomendada e o único fato ou regra que a fundamenta. Uma recomendação só se torna decisão quando o usuário a confirma.
5. **Mostre os fatos que verificou.** Quando uma pergunta depender de um fato consultado no ambiente, informe o resultado e onde o encontrou, para que o usuário decida com base nas evidências.
6. **Faça perguntas no idioma do usuário.** Perguntas e recomendações devem acompanhar o idioma do usuário; identificadores permanecem inalterados.
7. **Encerre com um registro.** Quando a fronteira estiver vazia, liste o que foi decidido e o que foi deixado em aberto de propósito, e peça confirmação de que chegaram a um entendimento compartilhado.

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
