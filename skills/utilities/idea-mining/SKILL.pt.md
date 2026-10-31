---
name: idea-mining
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-09-27
description: "Fluxo de trabalho de mineração de ideias para problemas pesados e travados (provas, questões de pesquisa, problemas persistentes de design/arquitetura): preencher um repositório de ideias com oito técnicas de mineração (reconhecimento, analogia de disciplina distante, alegoria cotidiana, desconforto estético, reenquadramento de conto de fadas, pesquisa na web/literatura, projetos irmãos, varredura do acervo existente), depois filtrar contra o que já foi tentado, escolher uma ideia e segui-la até a substância. Use esta skill quando um problema continua travado após várias tentativas, quando são necessárias \"novas ideias para X\", diante de \"estamos andando em círculos\", ou para ciclos periódicos de inovação sobre um projeto. Para coleta ampla e livre de ideias sem um problema travado, use brainstorm (SCAMPER, Six Hats etc.)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: utilities
tags: [ideen, kreativität, forschung, beweis, analogie, allegorie, recherche, innovation]
language: pt
status: active
visibility: public

dependencies:
  tools: []
  services: [websearch]
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 384a11073e2a67f6171fab75a7288288928b6baef43b284b947186597cd5e29d
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.906820+00:00"
---
<img src="banner.png" width="100%" alt="idea-mining banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.


> **English Translation** — Official English version of `idea-mining`.



# Idea-Mining — minerar ideias, filtrar, levar uma até o fim (Português)

## Visão geral e objetivo

Em problemas difíceis, a geração de ideias raramente fracassa por falta de intuições, mas por três
motivos: as intuições não são **registradas**, não são verificadas contra o **que já foi
tentado** (repete-se os mesmos becos sem saída), e nenhuma é consistentemente **levada até o
fim**. Este fluxo separa rigidamente as três fases: primeiro minerar de forma divergente (sem
avaliação), depois filtrar (contra a documentação do projeto), depois explorar substancialmente UMA ideia.

Origem: destilado de uma execução produtiva de automação de pesquisa sobre problemas matemáticos
abertos; funciona igualmente para bloqueios de arquitetura, design e conceito.

## Fase A — Preencher o repositório de ideias (divergente, sem avaliação)

Gravar todos os achados em um arquivo `IDEENSPEICHER.md` na pasta do projeto (tópicos +
2–3 frases, anotar fonte/gatilho). Percorrer as oito técnicas em sequência — elas visam
espaços associativos diferentes, por isso, em problemas realmente travados, não pular nenhuma
(em bloqueios mais leves ou com pouco tempo, basta um subconjunto justificado, mas no mínimo
uma técnica suave entre 3–5 mais a pesquisa):

1. **Reconhecimento:** Isto me soa familiar? Já vi esta estrutura em outro contexto?
2. **Disciplina distante:** Existe um problema/fórmula semelhante em uma disciplina bem distante
   (física↔economia, biologia↔informática, …)? Onde exatamente está a conexão?
3. **Alegoria cotidiana:** Contar o problema em uma alegoria próxima da natureza (ondas,
   areia, correnteza, crescimento …). Eficaz: deixar um **subagente não contaminado** inventar a
   alegoria e depois observar aonde ela leva — a própria visão já está deformada pelo problema.
4. **Desconforto / sapo→príncipe:** O que me incomoda no estado atual, o que acho feio? O que
   precisaria mudar para que eu o achasse de repente belo? O desconforto estético costuma apontar
   para a representação escolhida de forma equivocada.
5. **Reenquadramento de conto de fadas:** Contar o problema como um conto: quem é o herói, quem
   são os vilões, quais perigos espreitam, o que poderia ajudar o herói? A atribuição de papéis
   força uma estrutura causal que permanece invisível no formalismo.
6. **Pesquisa:** Vasculhar web, bases especializadas, servidores de preprints, fóruns
   (Reddit/ResearchGate/GitHub) em busca de publicações, scripts e abordagens novas. Carregar as
   fontes relevantes em uma pasta `_sources/` e ler buscando inovações — com preprints,
   manter o senso crítico.
7. **Projetos irmãos:** Verificar projetos próprios relacionados quanto a ideias de solução
   transferíveis de volta (subproblemas já resolvidos lá, ferramentas já construídas lá).
8. **Varredura do acervo:** Percorrer todo o acervo próprio de projetos (pipeline) em busca de
   abordagens que possam servir para ESTE problema.

## Fase B — Filtro (contra o que já foi tentado)

Cruzar o repositório de ideias com a documentação do projeto: notas de prova, proof-notes, logs de
decisão, TODO/DONE, repositórios de ideias anteriores. **Elimina-se o que está documentado como
já tentado e concluído** — não o que apenas "parece improvável" (a avaliação por atratividade
vem só na Fase C). Os sobreviventes vão para `IDEENSPEICHER_FILTERED.md`.

Pré-requisito é uma documentação de tentativas mantida em dia — se não existir, o primeiro passo é
criá-la (senão, toda execução futura produz repetições).

## Fase C — Escolher e levar adiante

1. Explorar brevemente de uma a três ideias do filtrado (um parágrafo cada: qual seria o primeiro
   passo concreto, qual o sinal de sucesso?).
2. Escolher **uma** — a de maior atração. A atração é aqui um critério legítimo: em problemas
   difíceis, só carrega uma ideia que se *quer* seguir.
3. Levar a escolha até o fim ou pelo menos até um avanço substancial — não pular para a próxima
   ideia no primeiro obstáculo (isso seria comportamento da Fase A dentro da Fase C).

## Fase D — Documentar

- Registrar os aprendizados na documentação do projeto (nota de prova, log de decisão, ADR) —
  **inclusive os fracassos**, pois eles são o filtro da próxima execução.
- Devolver as ideias de follow-up abertas para `IDEENSPEICHER.md` ou para o TODO.
- Relatório curto: minerado (quantidade) | filtrado (sobreviventes) | explorado | resultado | próximo passo.

## Fase E — Semeadura (retorno opcional para fora)

A técnica 7 traz ideias DOS projetos irmãos — a Fase E inverte o sentido: se a exploração produziu
algo transferível (método, ferramenta, padrão de solução), percorrer brevemente o acervo próprio
de projetos: quem se beneficiaria disso?

- **Semear com precisão, não espalhar:** no máximo ~3 projetos destinatários recebem diretamente
  uma entrada de TODO concreta (o que assumir, onde está, por que se encaixa); outros candidatos
  ficam apenas como lista priorizada no próprio projeto.
- Motivo do limite: espalhar amplamente gera, em muitos projetos, tarefas vagas que ninguém
  assume — três sementes precisas superam dez difusas.

## Como execução periódica

O fluxo é adequado como automação recorrente sobre um projeto fixo (rodada de inovação). Para
isso, combinar com o arcabouço de rotação (skill `rotation-check`): o registro impede que as
mesmas ideias sejam "redescobertas" várias vezes — o repositório de ideias e a documentação de
tentativas são aqui a memória.

## Exemplo e aplicação

```text
Problem: Ein Konvergenzbeweis steckt seit Wochen an einer Abschätzung fest.

A) Schürfen → IDEENSPEICHER.md: u. a. (2) ähnliche Struktur in der Warteschlangen-
   theorie?; (3) Subagent-Allegorie „Sand rieselt durch immer feinere Siebe" →
   Idee: Abschätzung stufenweise statt global; (6) Preprint von 2026 mit neuem
   Lemma, nach _sources/ geladen; (7) Nachbarprojekt hat ein numerisches
   Prüfscript, das sich rücktransferieren lässt.
B) Filter gegen BEWEISNOTIZ.md: „globale Abschätzung verschärfen" wurde 2× versucht
   und dokumentiert verworfen → raus. 3 Ideen überleben → IDEENSPEICHER_FILTERED.md.
C) Prime-Wahl: die Sieb-Idee (stärkste Anziehung) — bis zu einem Teilresultat
   durchgezogen.
D) BEWEISNOTIZ.md aktualisiert (auch der Fehlschlag von Idee 2), Kurzbericht.
```

## Sinais de alerta

| Pensamento | Realidade |
| --- | --- |
| "As técnicas 3–5 são firula" | As técnicas suaves geram as ideias que a pesquisa não consegue gerar — elas atingem outros espaços associativos. |
| "Eu já avalio enquanto coleto" | Avaliar na Fase A mata o rendimento divergente. Primeiro registrar, depois filtrar. |
| "O filtro demora demais, eu já me lembro" | A memória suaviza fracassos — só a documentação conta. |
| "A ideia emperrou, pego a próxima" | Na Fase C leva-se até o fim; voltar à Fase A só com um motivo documentado. |

## Skills relacionadas

- `brainstorm` — métodos criativos amplos (SCAMPER, Six Hats) sem pipeline de filtro/exploração.
- `think` / `decide` — análise e decisão de escolha, utilizáveis dentro da Fase C.
- `rotation-check` — arcabouço para uso periódico.
- `swarm-operations` — subagentes não contaminados para a técnica 3 e para exploração paralela.

## Registro de alterações

### 1.1.0 (2026-07-03)
- Fase E "Semeadura": retorno opcional de resultados transferíveis para projetos irmãos
  (no máx. ~3 destinatários diretos) — integrado em vez de ser uma skill própria
  cross-project-transfer (decisão de deduplicação).

### 1.0.0 (2026-07-03)
- Versão inicial. Abstraída da automação do Codex "ultra-deep-idea-search-single-project"
  (repositório de ideias → filtro → escolha da principal → exploração) e generalizada de forma
  neutra quanto ao usuário.
