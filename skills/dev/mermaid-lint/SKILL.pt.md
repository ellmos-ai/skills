---
name: mermaid-lint
version: 1.0.0
type: tool
author: Lukas Geiger + Claude
created: 2026-09-20
updated: 2026-09-20
aliases: [mermaid, mermaid-fehler, diagramm-render-fehler, unable-to-render-rich-display, schaltplan-fehler]
description: "Encontra e corrige diagramas Mermaid que o GitHub não renderiza (\"Unable to render rich display\"). Verifica cada bloco ```mermaid com o parser real do Mermaid, sem navegador, e depois comprova o resultado na página ao vivo do GitHub."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [mermaid, markdown, github, readme, diagramm, lint, dokumentation]
language: pt
status: active
visibility: public
dependencies: {'tools': ['node', 'git'], 'services': ['GitHub'], 'protocols': [], 'python': [], 'npm': ['mermaid', 'jsdom', 'playwright-core']}
translated_from_sha256: a1286c3571792da726aea23967c12360cb0daadb8d3d0bce2208ff27fc14bce9
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T22:17:49.701000+00:00"
---
<img src="banner.png" width="100%" alt="mermaid-lint banner">

# mermaid-lint

Um diagrama Mermaid com erro de sintaxe mostra no GitHub, em vez da figura, a caixa
**"Unable to render rich display"**. Localmente isso não aparece, porque nenhuma ferramenta
verifica o bloco. Esta skill fecha essa lacuna.

## Quando aplicar

- Um README ou documento mostra no GitHub um erro de renderização em vez de um diagrama.
- Antes de uma publicação ou de um release com diagramas na documentação.
- Após cada alteração de Markdown que toque blocos Mermaid.
- Em vários repositórios de uma vez, quando não está claro onde algo está quebrado.

## As duas ferramentas

### 1. `mermaid_lint.mjs` — verificação de sintaxe sem navegador

```
node mermaid_lint.mjs <repo-pfad> [...] [--json]
node mermaid_lint.mjs --from <liste.txt> [--json]
```

Pesquisa recursivamente todos os arquivos `.md`, extrai cada bloco ```mermaid e o faz
passar pelo `mermaid.parse()` — **o mesmo parser que o GitHub usa no navegador**.
Saída 0 = todos os blocos são analisados sem erros, saída 1 = pelo menos um bloco com defeito. A saída indica arquivo,
número do bloco, linha e a mensagem literal de erro do parser.

`--from <datei>` lê uma lista de caminhos, um por linha. Use isso em vez de muitos argumentos:
caminhos do Windows com barras invertidas são devorados em silêncio pelo shell Bash
(de `D:\code\my-repo` vira `D:codemy-repo`). Escreva os caminhos com barras normais (forward slashes).

Um único processo cobre centenas de repositórios, porque o Mermaid é carregado apenas uma vez.
Nada de Puppeteer, nada de download do Chromium.

### 2. `readback.mjs` — prova na página ao vivo

```
node readback.mjs <github-url> [...]
```

Abre as páginas no Edge já instalado (sem download de navegador) e conta falhas reais
de renderização. Veredito por página: `OK`, `DEFEKT`, `UNKLAR` ou `KEIN-MERMAID`.

## Três armadilhas que tornam esta skill necessária

**O GitHub renderiza o Mermaid em iframes com sandbox** servidos a partir de `viewscreen.githubusercontent.com`.
A página principal não enxerga o conteúdo deles. Quem avalia apenas `document.body.innerText` ou
`msedge --dump-dom` recebe zero erros em **toda** página — inclusive em uma comprovadamente quebrada. Por isso, `readback.mjs` avalia todos os frames.

**Um único achado DEFEKT não é confiável.** Durante o carregamento, o GitHub mostra por instantes um placeholder que parece um erro de renderização. Medido em 2026-09-20:
a mesma página primeiro informou `ERR=1`, depois duas vezes `ERR=0`. Por isso, `readback.mjs` repete automaticamente os achados negativos; um `OK` nunca é repetido.

**`mermaid.parse()` precisa de um DOM**, senão falha em `DOMPurify.addHook` e
marca fluxogramas válidos como quebrados por engano. `mermaid_lint.mjs` prepara antecipadamente
uma janela jsdom. Se ainda sobrar um erro de ambiente, ele aparece separadamente em `envIssues` e **não** é contado como erro de sintaxe.

## Sempre verifique com um controle negativo

Antes de confiar em um resultado verde, faça a ferramenta rodar uma vez sobre um estado que você sabe estar quebrado — por exemplo, o commit anterior à sua correção:

```
node readback.mjs "https://github.com/<org>/<repo>/blob/<alter-sha>/README.md"
```

Se ela também reportar `OK`, seu readback não mede nada. Foi exatamente assim que a armadilha do iframe, descrita acima, foi descoberta.

## Causas frequentes de erro e a correção mínima

| Sintoma na mensagem do parser | Causa | Correção |
|---|---|---|
| `Expecting '+', '-', '()', 'ACTOR', got 'loop'` | O participante tem nome igual a uma palavra reservada: `loop`, `alt`, `opt`, `par`, `end`, `critical`, `break`, `rect`, `note` | Declarar um alias: `participant L as Loop`; as mensagens usam `L`. O **nome exibido permanece** — não renomear. |
| `got 'PS'` em um fluxograma | Parênteses redondos no rótulo do nó | Colocar o rótulo entre aspas: `A["Start (hier)"]` |
| `Lexical error ... Unrecognized text` | Crases ou dois-pontos no rótulo | Colocar o rótulo entre aspas e remover as crases |
| `Expecting 'SEMI', 'NEWLINE', 'EOF'` em `graph`/`flowchart` | `Note:` existe apenas em diagramas de sequência e de classes | Tirar o texto de observação do bloco e colocá-lo como linha Markdown logo abaixo, para que a informação continue visível |
| `Expecting 'SOLID_OPEN_ARROW' ... got 'NEWLINE'` em um diagrama de sequência | **Entidade HTML** no texto da mensagem (`&lambda;`, `&Delta;`, `&ge;`). Aqui não quebram nem os parênteses nem o `=` — o `;` final da entidade é lido pelo lexer como terminador de instrução, e tudo o que vem depois vira uma nova instrução. | Substituir a entidade pelo caractere literal (λ, Δ, ≥), sem alterar o restante do texto. Os parênteses podem permanecer. Nunca alterar valores numéricos nem a sua grafia. |
| Ponto e vírgula em uma mensagem de sequência | é lido como fim de instrução | substituir por ` - ` |

Em **rótulos de fluxograma entre aspas** as entidades não causam problema — a regra vale apenas para mensagens de sequência. `mermaid_lint.mjs` informa essas entidades como uma linha `[WARN]` própria (campo `warnings` no JSON), além do erro do parser: o parser só diz `got 'NEWLINE'` e não informa a causa.

**Princípio:** correção minimamente invasiva. Layout, IDs de nós, ordem e texto visível permanecem, na medida do possível, inalterados. Em repositórios científicos, isso vale especialmente para valores numéricos e sua grafia. Havendo paridade EN/DE, manter as duas versões com a mesma estrutura.

## Fluxo em vários repositórios

1. Inventário com `gh repo list <org> --limit 200 --json name,isArchived,isPrivate,defaultBranchRef`.
2. Clonar **trazendo o estado remoto** e levar as divergências a sério. Um lint em um clone desatualizado mede o estado errado. Se `git pull --ff-only` falhar, verifique contra `origin` em vez de contra a árvore de trabalho:
   `git archive origin/<branch> | tar -x -C <tempdir>` e faça o lint da pasta temporária.
3. **Repositórios com o mesmo nome em organizações diferentes** (tipicamente `.github`) não podem ser mapeados para o mesmo clone — senão você verifica nove vezes o mesmo repositório. Em caso de nome duplicado, clone de forma plana para `<org>__<repo>` e faça o lint do estado novo.
4. Antes de cada alteração, verifique os locks (`lock_scan.py` e `LOCK*.txt` no clone **e** no caminho do projeto no OneDrive), defina o seu próprio lock e remova-o depois do push.
   **Leia o escopo, não apenas a existência:** `LOCK.team.*` com `expires_after` expirado pode ser ignorado; `LOCK.user.zenodo-upload.txt` bloqueia exclusivamente a operação externa de escrita no Zenodo e permite expressamente alterações na documentação. Já um `LOCK.user.until-winners-announcement.txt` (Judging) bloqueia qualquer push — ali, verifique apenas em modo leitura e registre o achado como ticket.
5. Corrigir, fazer lint até ficar verde, commitar, `git pull --rebase`, fazer push.
6. Readback com controle negativo. Só então vale como concluído.

## Instalação

```
npm install mermaid jsdom playwright-core
```

Na pasta dos scripts ou de forma global; `playwright-core` usa o Edge instalado
(`channel: 'msedge'`) e não baixa um navegador próprio. Só é necessário para o readback —
a verificação de sintaxe funciona sem ele.

## Relacionados

- `_tools/lint_mermaid.py` no GithubBot: linter mais antigo, baseado em regex, com `--fix`. Ele corrige automaticamente padrões conhecidos, **mas não conhece palavras reservadas** e não substitui esta skill. Ordem sensata: primeiro `mermaid_lint.mjs` para diagnóstico, depois, se necessário, `lint_mermaid.py --fix` para os padrões em massa, e então faça o lint novamente.
- `github-repo-care`: protocolo geral para manutenção e publicação de repositórios.
