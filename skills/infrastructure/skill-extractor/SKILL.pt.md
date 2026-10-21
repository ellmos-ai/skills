---
name: skill-extractor
version: 1.3.1
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-09-14
description: "Extrai de um histórico de chat (sessão atual ou arquivos de transcrição) uma skill reutilizável — ou melhora uma skill existente muito semelhante, em vez de criar uma duplicata. Use esta skill com expressões como „transforme isso em uma skill\", „devemos registrar isso como skill\", „extraia skills deste/destes históricos de chat antigos\", „torne este modo de trabalho reutilizável\", ou com `/skill-extract`. Também cobre execuções em lote sobre muitas transcrições antigas (com redução de dados por meio de subagentes). Para AUTOMATIZAÇÕES recorrentes (Cron/Schedule/Loop), use a skill irmã workflow-extract."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [skills, extraction, transcript, chatverlauf, meta, dedup, neutralisierung, workflow]
language: pt
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'None', 'origin_version': 'None', 'origin_repo': 'github.com/ellmos-ai/skills', 'last_sync_from_origin': 'None', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
translated_from_sha256: ab3eadf82194e539e4f617d67bc24b0375427d88167e6ff359baf8bf8476fcdc
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:49.872870+00:00"
---
<img src="banner.png" width="100%" alt="skill-extractor banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

> **English Translation** — Official English version of `skill-extractor`.

# Skill-Extractor — extrair skills de históricos de chat (Português)

## Visão geral e finalidade

Modos de trabalho valiosos surgem durante as sessões: um problema foi resolvido com esforço, o usuário
fez várias correções, e ao final existe um fluxo funcional — e, na próxima vez, o agente começa
novamente do zero. Esta skill destila de um histórico de chat aquilo que vale a pena conservar e
transforma isso em uma skill segundo as convenções da biblioteca local de skills. Princípio central:
**estender antes de criar** — se existir uma skill muito semelhante, ela é melhorada em vez de se criar
uma duplicata.

Delimitação: o resultado aqui é uma **skill acionável** (capacidade/procedimento que um agente carrega
quando necessário). Se o histórico deve se tornar uma **automação autônoma** (prompt recorrente, Cron,
Schedule), use a skill irmã `workflow-extract`.

## Fluxo

### 1. Determinar a fonte

Três formas de entrada:

| Fonte | Acesso |
| --- | --- |
| **Sessão atual** | Usar diretamente o contexto da conversa — nenhum arquivo necessário |
| **Transcrições individuais** | Ler os arquivos; locais e parsing: `transcript-quellen.md` |
| **Lote (muitos históricos antigos)** | Primeiro redução de dados por meio de subagentes, depois extração: seção „Modo lote" |

Para JSONL do Claude Code, use primeiro `scripts/segment_stations.py`. O script forma estações determinísticas
entre pontos de relatório, sem copiar texto do chat ou parâmetros de ferramentas para a saída.
Marcadores, opções e formato de saída estão em `transcript-quellen.md`.

### 2. Encontrar o que vale a extração

Nem toda sessão contém uma skill. Procure estes sinais — eles mostram onde há conhecimento adquirido
a um custo alto e que será necessário novamente:

- **Repetição:** o mesmo fluxo ocorreu ≥2 vezes (nesta ou em várias sessões).
- **Ciclos de correção:** o usuário ajustou o agente várias vezes até acertar — a versão final é o
  destilado, as correções são as justificativas („por que assim").
- **Marcadores explícitos:** „guarde isso", „é assim que fazemos sempre", „da próxima vez já assim".
- **Cadeias de ferramentas:** uma sequência não óbvia de ferramentas/comandos que funcionou (incluindo
  os becos sem saída a evitar).
- **Regras de decisão:** critérios segundo os quais foi escolhida uma alternativa.

Para cada candidato, registre: gatilho (quando se precisa disso), fluxo (passos), justificativas (por
que assim e não de outra forma), armadilhas (o que deu errado), forma do resultado.

**Com transcrições JSONL, não conduza a busca manualmente.** `scripts/score_stations.py` pega as estações do
passo 1 e entrega, em vez de locais no texto corrido, uma **lista de candidatos avaliada**:

```bash
python scripts/score_stations.py <transkript.jsonl> [weitere.jsonl ...] --candidates-only
```

A avaliação repousa sobre uma única observação: **a resposta seguinte é o rótulo.** Uma estação é julgada pelo que
a pessoa diz em seguida — se confirma, o procedimento era viável; se corrige, faltava uma regra; se muda
a direção, a abordagem estava errada. Assim, os sinais enumerados acima tornam-se contáveis, e não apenas
perceptíveis:

| Sinal da lista acima | equivalente automático |
| --- | --- |
| Ciclos de correção | tipo de resposta `KO`, ponderado com limite |
| Repetição | mesma assinatura de cadeia de ferramentas em ≥2 sessões |
| Cadeias de ferramentas | comprimento da cadeia ≥3 passos |
| Becos sem saída | tipo de resposta `RA` — desconto de pontos, ainda assim vale a leitura como armadilha |
| Armadilhas | `is_error` seguido de correção (erro sem correção não conta) |

Uma **sequência de estações** é a unidade, não a estação isolada — uma skill corresponde a uma seção
trabalhada por completo, não a um ponto de relatório.

**Os limites da automação também devem ser lidos.** O tipo de resposta surge de um pré-filtro determinístico
por lista de palavras; o que não for inequívoco permanece `unknown` em vez de ser adivinhado.
Perguntas inequívocas são reconhecidas como `NT`: com ponto de interrogação, com poucos
inícios claros de pergunta como „você pode …" („kannst du …“) ou „devemos …" („sollen wir …“) e em complementos como „mais uma coisa sobre …" („noch etwas zu …“).
Declarações de estado vagas, sem pergunta, correção ou pedido identificáveis, permanecem deliberadamente
`unknown`. Se `classified_ratio` estiver abaixo de 0,5, a saída informa por si mesma que a
ordem não se sustenta — então reclassifique as respostas dos candidatos principais antes de colher. Um score é
uma recomendação de leitura, não uma decisão de seleção: o passo 3 continua obrigatório.

**Nem toda resposta é um prompt.** Turnos vazios e envelopes de máquina (notificação de tarefa, mensagem de
teammate, comando slash puro) não têm tipo de prompt e são indicados como `empty` ou
`non_prompt` — eles **não** entram no denominador de `classified_ratio`. Em três transcrições reais,
isso correspondia a 127 de 246 respostas; contá-los como classificação fracassada reduziu o indicador de 0,64
para 0,45 e teria colocado um modelo sobre entradas nas quais não há nada a reconhecer.

**Etapa opcional de modelo — e por que raramente é necessária.** `--classifier-cmd "<befehl>"` encaminha os
`unknown` restantes a um comando externo (lista JSON na entrada padrão, lista JSON com rótulos
do mesmo comprimento na saída padrão; tudo fora dos sete tipos permanece `unknown`). Propositalmente
um **comando em vez de um adaptador de provedor**: esta biblioteca é neutra quanto ao usuário e não contém
nenhum endpoint de modelo. `follow_up_source` e o bloco `classification` indicam quais rótulos vêm do
modelo.

> **Proteção de dados:** esta é a única etapa em que texto de prompt sai do processo. O pré-filtro lê o
> texto apenas localmente e emite exclusivamente rótulos; um comando classificador pode repassá-lo
> livremente. Por isso a etapa vem **desligada** por padrão.
>
> **Medido antes de ligá-la** (60 respostas abertas, 57 rotuladas à mão, Gemini 3.7 Flash):
> **70,2 % de acertos** — e em **0 %** dos casos o modelo disse honestamente „não sei". Ele sempre adivinha.
> Os erros não estão distribuídos uniformemente: 12 de 17 caíram em `NM`, entre eles 3 de 4
> `KO` atribuídos erroneamente. Justamente `KO` concede os pontos no score — um
> modelo que recolhe correções como `NM` distorce exatamente a ordem para a qual foi chamado.
> Para `--min-score`, este estado **não** é sustentável.

Quem quiser elevar a taxa tem a alavanca mais barata no pré-filtro: prompts de pedido (`ticket:`,
`erstelle`, `starte`, …) capturaram na mesma amostra **14 de 25 SP com 100 % de precisão**,
enquanto o modelo acertou 15 e, ao fazê-lo, corrompeu 17 outros rótulos.

### 3. Portão de deduplicação: estender antes de criar

Antes de escrever qualquer coisa, verifique o panorama existente:

1. Pesquisar as palavras-chave do candidato nos diretórios de skills (pasta de implantação do agente,
   p. ex. `~/.claude/skills/`, e — se existir — a biblioteca curada de skills como fonte da verdade;
   igualmente as skills de plugins registrados).
2. **Ler de fato** as 2–3 skills mais próximas, não apenas comparar nomes.
3. Decidir:

| Resultado | Ação |
| --- | --- |
| O candidato já está essencialmente coberto | **Estender:** incorporar os elementos faltantes à skill existente (nova seção, nova técnica, nova armadilha), aumentar a versão MINOR, entrada no changelog |
| Sobreposição parcial, mas núcleo diferente | **Nova skill** com referência cruzada („Skills relacionadas") às vizinhas — não duplicar conteúdo, apenas remeter |
| Nada comparável | **Nova skill** |

Regra prática: se mais da metade do candidato estiver em uma skill existente, estenda. Um acervo de skills
cheio de quase-gêmeas é pior do que uma skill bem cuidada.

### 4. Neutralizar

A matéria-prima está cheia de detalhes específicos da sessão. Antes de escrever, abstraia segundo as regras
de `neutralisierung.md`: separe a mecânica (de validade geral) da configuração (específica de usuário/sistema),
substitua caminhos/hosts/nomes concretos por marcadores ou por um bloco de configuração claramente
identificado. Objetivo: a skill funciona para outros usuários, outros sistemas, outros projetos.

### 5. Escrever a skill

- **Formato:** respeitar as convenções da biblioteca de destino (frontmatter, esquema de nomes, idioma,
  changelog). Nesta biblioteca: `docs/CONVENTIONS.md` (cabeçalho YAML completo, nome em kebab-case,
  alemão como idioma principal, Versionamento Semântico).
- **Redigir a description de forma „incisiva":** a description é o mecanismo de gatilho. Escreva nela tanto
  O QUE a skill faz quanto QUANDO ela deve entrar em ação (formulações típicas do usuário) — skills tendem a
  ser acionadas com pouca frequência, e não com excesso.
- **Motivo antes do que:** incorpore na skill as justificativas dos ciclos de correção. Uma skill que apenas
  lista passos é aplicada incorretamente no primeiro caso especial; uma que explica o porquê pode ser
  transferida.
- **Documentar as armadilhas:** os becos sem saída da sessão são ouro — inclua-os em uma seção „Red Flags" ou
  „Armadilhas".
- **Manter enxuta:** abaixo de ~300 linhas; transfira o material detalhado para arquivos de referência aos
  quais o SKILL.md remete.

### 6. Wrapper de comando (opcional)

Se a skill for chamada diretamente com frequência, crie um comando slash (no Claude Code: um arquivo Markdown
curto em `~/.claude/commands/<name>.md` que aponta para a skill e repassa os argumentos). Convenção: o comando é uma
entrada fina, o conteúdo vive na skill.

### 7. Registrar e testar

- Colocar na biblioteca (categoria correta) e implantar no ambiente de execução (aqui: `python skill_sync.py deploy <name>` —
  a primeira instalação precisa do nome explícito).
- Teste de gatilho: formular 2–3 prompts realistas que devem acionar a skill e verificar se a description
  funciona.
- Para um ciclo completo de avaliação (casos de teste, comparação com linha de base, otimização da descrição),
  use o `skill-creator`, se instalado — esta skill aqui é o extrator, não o laboratório de testes.
- Manutenção de índice/roteamento: atualize as skills de busca/índice, se existirem
  (aqui: `code-skill-index`, tabela de roteamento `skill-finder`).

## Modo lote: muitos históricos de chat antigos

As transcrições são grandes (frequentemente >100k tokens); nunca carregue todas cruas em um único contexto.
Map-reduce por meio de subagentes (padrão: skill `swarm-operations`, enxame de tarefas):

1. **Inventário:** listar os arquivos de transcrição (locais: `transcript-quellen.md`), agrupar por projeto/
   período. Em acervos muito grandes, reduzir primeiro com coletores/extratores existentes (p. ex., conjuntos
   de dados de listeners de prompts/estudos que contêm apenas prompts do usuário) — prompts do usuário e
   correções carregam a maior parte do sinal.
2. **Map:** para cada lote, um subagente com missão estrita: „Leia estas transcrições, reporte candidatos a
   skill como lista compacta (gatilho, fluxo, justificativas, armadilhas, sessão de referência)" — devolver
   apenas os destilados, nunca texto bruto.
3. **Reduce:** unir as listas de candidatos, agrupar, mesclar duplicatas. A frequência conta: um padrão que
   aparece em 5 sessões é um candidato mais forte do que um truque isolado.
4. **Portão + construção:** para os principais candidatos, percorrer os passos 3–7 do fluxo normal. Antes da
   construção em massa, apresente ao usuário uma lista numerada de candidatos para seleção — a extração em
   lote, do contrário, gera lixo de skills.

## Exemplo e aplicação

```text
User: „Wir haben jetzt dreimal PDF-Rechnungen nach demselben Schema geparst —
mach daraus einen Skill."

1. Quelle: aktuelle Session. Signal: Wiederholung (3×) + Korrektur („Beträge immer
   als Dezimalzahl mit Punkt, nicht Komma").
2. Dedup-Gate: Suche findet `pdf`-Skill (generisch, Erzeugung/Extraktion) — Kern
   überlappt nicht (hier: Rechnungs-Schema + Validierungsregeln) → neuer Skill
   `invoice-parsing` mit Querverweis auf `pdf`.
3. Neutralisieren: konkreter Ablageordner und Firmenname → Konfigurationsblock.
4. Skill schreiben: Schema-Tabelle, die Komma/Punkt-Korrektur als Fallstrick,
   Changelog 1.0.0. Trigger-Test mit „lies diese Rechnung ein".
```

## Red Flags

| Pensamento | Realidade |
| --- | --- |
| „Crio rapidamente uma skill nova" | Portão de deduplicação primeiro — estender antes de criar. |
| „Deixo os caminhos, afinal é para este sistema" | Neutralizar é obrigatório; o concreto pertence a um bloco de configuração. |
| „O histórico é longo, resumo de memória" | Procurar deliberadamente os sinais (correções, marcadores) — a memória suaviza justamente os pontos que tornam a skill valiosa. |
| „Cada sessão gera uma skill" | Sem sinal de repetição/correção/marcador: nenhuma skill. |

## Skills relacionadas

- `workflow-extract` — mesma extração, mas o objetivo é uma automação autônoma.
- `skill-explorer` — auditoria/limpeza do panorama de skills (usa o portão de deduplicação em grande escala).
- `skill-creator` (Plugin) — ciclo de avaliação e otimização de descrição para skills prontas.
- `swarm-operations` — padrão de enxame para o modo lote.

## Registro de alterações

### 1.3.1 (2026-09-14)
- **Pré-filtro NT conservador para respostas humanas abertas:** complementos como „mais uma coisa sobre
  …" e perguntas inequívocas por ponto de interrogação ou com um início claro de pergunta são reconhecidos
  como `NT`. Marcadores específicos que já se aplicavam mantêm a prioridade.
- **Nenhuma precisão aparente em declarações de estado:** frases sem pergunta, correção ou pedido
  identificáveis permanecem `unknown`; a cobertura adicional não inventa um tipo de prompt.

### 1.3.0 (2026-09-13)
- **Respostas que não são prompts deixam de contar como classificação fracassada.**
  `prompt_kind()` separa `empty` (turno vazio), `non_prompt` (envelope de máquina, comando
  slash puro) e `human`; apenas estes últimos entram no denominador de `classified_ratio`. Em três
  transcrições reais, 127 de 246 respostas não eram manifestações — contá-los havia reduzido o indicador de 0,64
  para 0,45 e disparado o aviso „ordem não confiável", sem que o pré-filtro estivesse errado. Efeito colateral:
  textos de máquina eram antes, às vezes, **mal**classificados como `BE`/`KO` por seus marcadores
  de palavra; isso deixa de ocorrer.
- **Prompt de pedido (`SP`) no pré-filtro.** S3 havia medido que um prompt inicial não é
  reconhecível linguisticamente — isso vale para o INÍCIO da sessão, não para o PEDIDO (`ticket:`,
  `erstelle`, `starte`, …). Contra 57 respostas rotuladas à mão: 14 de 25 `SP` com
  100 % de precisão. É verificado **por último**, para que „crie X, mas não assim" continue sendo uma correção.
- **Etapa opcional de modelo `--classifier-cmd`** após o pré-filtro: um comando (JSON entra, JSON sai), não um
  adaptador de provedor — a biblioteca permanece neutra quanto ao usuário. Uma chamada em lote para todos os
  respostas abertas; diferença de comprimento, JSON defeituoso ou saída com erro nunca levam a rótulos deslocados.
  `follow_up_source` e o bloco `classification` indicam a origem de cada rótulo.
- **Medição da etapa de modelo, que depõe contra seu uso amplo** (60 respostas abertas, Gemini 3.7 Flash):
  70,2 % de acertos, 0 % de „unknown" honesto, e 12 de 17 erros caem em `NM` — entre eles 3 de 4
  `KO` deslocados, justamente a classe que sustenta o score. Para uma calibração `--min-score` isso não
  basta; a etapa permanece opt-in e está marcada como transição de proteção de dados.
- Indicador nas mesmas três transcrições: **0,451 → 0,644**, sem chamada de modelo.

### 1.2.0 (2026-09-12)
- Avaliação do valor de colheita de sequências de estações acrescentada (`scripts/score_stations.py`): sinais duros por
  estação, classificação dos anexos segundo os sete tipos de `promptarchaeologie`, score e lista de candidatos. O
  passo 2 „Encontrar o que vale a extração" recebe assim uma lista avaliada em vez de uma busca de sinais no
  texto corrido. A saída permanece sem conteúdo; `classified_ratio` indica até onde a automação se sustenta, em
  vez de simular uma ordem (ticket T-20260831-971906399, S3/S4; decisão do usuário D-20260906-012).
- `station-skill-mask-v1.schema.json`: `$schema`/`$id` restaurados — ambas as chaves haviam sido vítimas de uma expansão
  de variável de shell ao serem criadas (`""` como chave).

### 1.1.0 (2026-08-31)
- Acrescentado segmentador determinístico e economizador de dados de estações para JSONL do Claude Code.

### 1.0.0 (2026-07-03)
- Versão inicial. Surgiu da tarefa de abstrair sistematicamente automações do Codex e históricos de chat
  em skills.
