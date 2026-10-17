---
name: reissverschluss-merge
version: 1.0.0
type: skill
language: pt
visibility: public
author: Claude (extrahiert aus einer Live-Merge-Session, Multi-Repo-PR-Abarbeitung)
created: 2026-08-07
provenance:
  origin: live-session-extraction
  extracted: 2026-08-07
  method: skill-extractor
updated: 2026-08-07
description: "Procedimento de fecho éclair (em inglês: zipper merge) para merges com alto número de conflitos: quando dois ramos divergentes ou um PR e o seu ramo de destino trazem AMBAS as alterações valiosas que aparentam ser inconciliáveis, não se escolhe um lado de forma global; em vez disso, compara-se secção por secção, adota-se em cada caso a versão melhor segundo uma tabela de decisão (Escolher/Porquê), faz-se commit por secção e só no fim se faz push. Último nível de escalada: reconstruir em vez de fazer merge — apenas assumir a intenção/funcionalidade do ramo e reconstruí-la sobre o estado atual. Usar quando surgirem: \"Merge-Konflikt\", \"divergente Branches\", \"main vs. master\", \"konfliktreicher PR\", \"zipper merge\", \"Reißverschluss\", \"beide Seiten haben Recht\", \"PR ist zu alt zum Mergen\"."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
aliases:
  - zipper-merge
  - zipper-verfahren
  - reissverschluss
tags: [git, merge, konflikt, pull-request, branch, rebase, dev-workflow]
translated_from_sha256: 6a31c500a8da2c6d19255bf7601125cf9f2fed39f9387fa0c8e45b11260468ee
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.592432+00:00"
---
<img src="banner.png" width="100%" alt="reissverschluss-merge banner">

# Merge em fecho éclair (zipper merge)

## Quando usar este procedimento

Dois ramos do mesmo repositório estão **fortemente divergentes** e **ambos têm valor** —
tipicamente: `main` vs. `master` após manutenção paralela, um PR antigo contra um
ramo de destino que avançou, dois estados de agentes/equipas com correções próprias.
Um merge normal ou eliminaria um dos lados ("ours"/"theirs") ou
produziria um emaranhado de conflitos impossível de desfazer. O procedimento de fecho éclair resolve isto
ao fazer os dentes de ambos os lados **engrenar secção por secção**:
em cada secção vence a versão comprovadamente melhor — ou uma mistura fundamentada.

**Não é necessário** em conflitos triviais (um lado claramente desatualizado,
poucos hunks): nesse caso faz-se merge normal. O procedimento compensa a partir do ponto em que
é preciso ponderar seriamente várias ficheiros/secções.

## Fase 0 — Visão geral e escolha da base

1. **Analisar ambos os lados por completo** (não apenas os marcadores de conflito):
   `git log --oneline A..B` e `B..A`, `git diff A...B --stat`, depois ler os
   ficheiros divergentes de ambas as versões.
2. **Escolher a base — pela realidade, não pela data.** A base passa a ser o ramo que
   coincide com a **realidade publicada**: estado do registo (npm/PyPI/…),
   versão implementada, CI verde, tags de release. Um ramo com data mais recente,
   mas sem correspondência com o mundo exterior, é material, não base.
3. **Verificar a consistência de ambos os lados** — muitas vezes AMBOS são internamente
   inconsistentes (por exemplo, a base tem a versão X sem changelog correspondente, a outra
   mantém o changelog, mas fica atrás na versão). Estes achados pertencem à
   tabela, não devem ser varridos para debaixo do tapete.

## Fase 1 — Tabela de decisão (o núcleo)

Para cada secção divergente (ficheiro, bloco, campo — tão fina quanto necessário) uma
linha:

| Secção | Escolher | Porquê |
|---|---|---|
| `package.json` → version | Base | coincide com o registo |
| Bloco `overrides` | Outro lado | contém atualizações de segurança que faltam na base |
| ↳ nele a entrada `X` | **misturar** | adotar a entrada do outro lado, mas elevá-la para a versão mais recente da base |
| Changelog `[Unreleased]` | **misturar** | unir ambos os blocos, remover duplicados |

Regras:

- **Factos em vez de suposições.** Cada célula "Porquê" apoia-se em algo verificável:
  consulta ao registo, execução de testes, base de dados de advisories, instalação
  isolada de teste do ficheiro controverso. Quem adivinha faz merge de suposições.
- **"Misturar" é um veredicto legítimo** — o fecho éclair pode deixar os dois dentes
  engrenar dentro de uma mesma secção.
- **Descartar é um veredicto legítimo** — o que não se sustenta em nenhum dos lados
  (badge morto, funcionalidade meio introduzida) é eliminado. O estado intermédio
  ("funcionalidade meio integrada") é a pior variante: ou entra completamente ou sai completamente.
- A tabela concluída é o **documento contratual** da implementação — em caso de mudança de
  sessão ou passagem de testemunho, basta para continuar mecanicamente.

## Fase 2 — Implementação: commit por secção, push só no fim

1. Iniciar na base um merge real: `git merge <gegenseite>`
   (intencionalmente SEM `-X ours/theirs` — os conflitos devem ficar visíveis de propósito).
2. Resolver os conflitos **secção por secção** exatamente segundo a tabela.
3. **Um commit por secção lógica** (ou, se houver um único merge-commit:
   um passo de resolução documentado por secção na mensagem de commit).
   Cada mensagem de commit indica o veredicto da tabela ("overrides: lado oposto +
   vitest elevado para o estado da base"). Assim, cada dente do fecho éclair
   continua rastreável e reversível individualmente.
4. **Testes após a implementação** (suite, build, instalabilidade) — primeiro verdes,
   depois seguir.
5. **Push só no fim** — o histórico local pode ser reorganizado durante o procedimento;
   o remoto vê apenas o resultado final.
6. **Fechar a divergência sem apagar:** fazer avançar o ramo derrotado por fast-forward
   até ao resultado (`git checkout <gegenseite> &&
   git merge --ff-only <basis>`). Ambos os nomes apontam depois para o mesmo
   estado; nenhum histórico se perde.

## Caminho de escalada — reconstruir em vez de fazer merge (último nível)

Quando o fecho éclair já não funciona, **não se faz merge, reconstrói-se**:
destila-se a **intenção/funcionalidade** do ramo/PR
(O QUE queria alcançar — não COMO) e implementa-se de novo sobre o estado atual.
O ramo/PR antigo é fechado com referência à reconstrução.

Gatilhos para a escalada (basta um):

- O outro lado está **comprovadamente defeituoso** (por exemplo, nunca foi instalável,
  o build falha) — então nunca houve um estado funcional para fazer merge.
- O volume de conflitos ≫ substância: a alteração é pequena, mas dispersa por centenas
  de linhas deslocadas (ondas de renomeação/formatação pelo meio).
- O histórico está envenenado (por exemplo, o mesmo número de versão atribuído em ambos os lados
  a conteúdos **diferentes** — um merge herdaria a mentira).
- O PR é tão antigo que o seu contexto (APIs, estrutura) já não existe.

Procedimento: registar a intenção em 2–5 frases (a partir da descrição do PR, commits,
substância do diff) → reimplementar sobre o estado atual → testes → no PR/ramo
antigo, documentar O QUE foi assumido e O QUE foi deliberadamente deixado de fora, depois fechar.
Mencionar a autoria da ideia na mensagem de commit/texto do PR.

## Armadilhas (da sessão de origem, pagas caro)

- **Bloco de changelog duplicado `[Unreleased]`** é o ponto crítico mais frequente em ramos
  mantidos em paralelo — unir sempre, nunca descartar um sem aviso.
- **Ambos os lados atribuem o mesmo número de versão a conteúdos diferentes:**
  antes do merge, esclarecer qual número o registo conhece; o outro lado
  recebe uma correção no changelog unificado.
- **Um merge é uma oportunidade de auditoria:** ao ler secção por secção, surgem
  coisas que nenhum dos ramos viu (advisories abertos, links mortos, pins inconsistentes).
  Levar esses achados, mas como commits próprios — não misturados
  com as decisões do fecho éclair.
- **Aceitar "porque é mais recente":** a data não é argumento. Cada aceitação precisa
  de um motivo verificável.
- **Reflexo do force-push:** o procedimento dispensa force-push (merge +
  fast-forward). Se um force parecer necessário, a escolha da base está quase sempre errada.

## Sinais de alerta

| Pensamento | Realidade |
|---|---|
| "Fico simplesmente com o lado mais recente" | Data ≠ qualidade. Construir a tabela. |
| "Resolvo os conflitos de uma vez" | Um commit único torna cada decisão individual irrevisável. |
| "Faço push entretanto" | Fechos éclair meio prontos no remoto confundem qualquer leitor. Push só no fim. |
| "Merge resulta sempre de alguma forma" | Com um lado defeituoso ou histórico envenenado, reconstruir é mais honesto e mais rápido. |
| "A tabela é exagero" | Sem tabela, após o terceiro ficheiro esquece-se porque a secção 1 foi decidida assim. |

## Skills relacionadas

- `bugfix-protocol` — se o merge revelar um defeito real, continuar aí.
- `skill-extractor` — origem desta skill (destilado de sessão ao vivo).
- `human-loop-audit` — partilha apenas a imagem do fecho éclair, mas não tem nada a ver com merges do Git
  (procedimento interativo de teste de apps/GUI com o utilizador).

## Changelog

### 1.0.0 (2026-08-07)
- Versão inicial. Extraída de uma sessão de merge ao vivo de 2026-08-06
  (unificação main/master de vários repositórios com tabela de decisão, descoberta de um
  lado nunca instalável, conclusão por fast-forward; caso de escalada
  "assumir a intenção, reconstruir").
