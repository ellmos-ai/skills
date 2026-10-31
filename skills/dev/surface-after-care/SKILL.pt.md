---
name: surface-after-care
version: 1.6.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-07-24
updated: 2026-07-24
aliases: [repo-after-care, repo-pflege, after-care, repo-nachpflege, repo-wartung]
description: "Rotina regular de manutenção para um repositório GitHub já publicado (Nível 1, econômico e frequentemente repetível): primeiro identificar todas as superfícies de distribuição do projeto (npm, PyPI, registros, marketplaces, lojas, website) e espelhar as alterações posteriormente para lá; em seguida definir topics, verificar o portão de privacidade, revisar documentos quanto à intenção de publicação e ignorar posteriormente arquivos internos de planejamento, adicionar banner, comparar as afirmações do README com o estado real do código, melhorar a apresentação, completar as versões linguísticas do README, implementar medidas de visibilidade, verificar a entrada na página da organização e resolver issues e pull requests abertos. Use esta skill quando um repositório existente precisar ser mantido, organizado, atualizado, embelezado ou \"revisado mais uma vez\", quando um repositório parecer desatualizado ou desorganizado, em formulações como \"manutenção do repo\", \"after care\", \"pós-manutenção\", \"colocar o repo em dia\", \"organizar e enviar\" ou em rodadas rotativas de qualidade sobre vários repositórios. Para a rodada profunda, incluindo verificação jurídica e referências cruzadas entre organizações, use full-after-care; para a primeira publicação, github-repo-care."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: dev
tags: [github, repo, maintenance, privacy, i18n, documentation, visibility, issues]
language: pt
status: active
visibility: public

dependencies:
  tools: [git, gh, rg]
  services: [GitHub]
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: bc9d83148b0f265a9304d21d1ec9efaea306584890f1516e21dec9b6958a9026
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.065724+00:00"
---
<img src="banner.png" width="100%" alt="surface-after-care banner">
# Surface After Care — a rodada regular de manutenção para um repo publicado

## Quando esta skill se aplica

Use-a para um repositório que **já é público** e deve ser revisado periodicamente. Ela é o nível econômico: tudo o que pode ser decidido no próprio repo, sem inventariar repos alheios nem acionar um parecer jurídico.

Delimitação em relação às skills vizinhas:

| Situação | Skill |
|---|---|
| Repo está sendo publicado pela primeira vez | `github-repo-care` |
| Repo é público, rodada regular de manutenção | **esta skill** |
| Além disso, verificação jurídica + referências cruzadas em todas as organizações + i18n do app | `full-after-care` (alias `deep-after-care`) |
| Apenas verificação jurídica/privacidade/licença antes de tornar público | `repo-publish-check` |
| Manter as versões linguísticas sincronizadas em conteúdo | `bilingual-doc-sync` |
| Distribuição desta rodada por muitos repos, em rotação justa | `rotation-check` |

## Ideia central

Um repo publicado se afasta em duas direções: **a documentação descreve um software mais antigo do que o que está no repo**, e **acumulam-se arquivos que nunca foram destinados a olhos estranhos**. Ambos raramente são dramáticos, mas ambos custam exatamente os usuários que se quer conquistar — um desiste porque o guia de instalação não serve mais, outro porque encontra `AUFGABEN.txt` e `Plan.txt` na raiz e tem a impressão de que alguém trabalha ali só para si mesmo.

Esta rodada limpa ambos. Ela é deliberadamente repetível: melhor meia hora quatro vezes por ano do que uma grande faxina de uma vez.

## Fluxo

A ordem não é arbitrária. O passo 0 vem no início porque determina o escopo de todos os passos seguintes. O passo 2 vem antes de tudo que envia alterações — caso contrário, empurra-se melhorias sobre um estado que ainda precisa ser limpo. O passo 1 é puramente do lado do servidor e não atrapalha.

### 0. Inventariar as superfícies de distribuição

**Antes de alterar qualquer coisa: esclarecer onde este projeto está presente.** O repositório GitHub raramente é a única superfície. Um README corrigido pouco adianta se a página do pacote no npm ainda mostrar a versão antiga com a instrução de instalação errada — e é exatamente lá que cai a maioria dos usuários, porque os registros de pacotes costumam ranquear melhor nos mecanismos de busca do que o repo.

```bash
# Manifeste verraten die Kanäle
cat package.json pyproject.toml setup.py Cargo.toml 2>/dev/null | rg -n "name|version|keywords|repository|homepage"
rg -n "npmjs.com|pypi.org|marketplace|registry|crates.io|hub.docker|zenodo|doi" README* docs/ .github/ 2>/dev/null

# Veröffentlichten Stand der Kanäle abfragen (nur was zutrifft)
npm view <paket> version description keywords 2>/dev/null
pip index versions <paket> 2>/dev/null
gh release list --repo ORG/REPO --limit 5
```

Superfícies típicas: npm, PyPI, Crates, Docker Hub, MCP-Registry, diretórios de plugins/skills, marketplaces de VS Code ou navegador, lojas de apps, Zenodo/DOI, website do projeto, perfil da organização, `llms.txt`, repos espelho em outros hosts.

Registre a lista encontrada no protocolo da rodada. A partir daí ela é o **conjunto-alvo**: cada alteração dos passos seguintes será espelhada nele ao final (veja "Paridade em todas as superfícies"). Se encontrar uma superfície que ninguém mantém mais e que aponta para um estado obsoleto, isso é uma constatação própria — atualizar ou retirar de forma deliberada, mas não deixar como está.

### 1. Definir topics

Os topics são a principal superfície de busca dentro do GitHub e quase não custam nada.

```bash
gh repo view ORG/REPO --json nameWithOwner,description,repositoryTopics,homepageUrl,visibility
gh repo edit ORG/REPO --add-topic <topic> --add-topic <topic>
```

O alvo são cerca de 5–12 topics a partir de três direções: **o que é** (`cli`, `mcp-server`, `python-library`), **do que trata** (`file-management`, `tax`, `note-taking`) e **como funciona** (`local-first`, `offline`, `privacy`). Oriente-se por topics que projetos comparáveis realmente usam — topics inventados não trazem usuários. Revise também description e homepage, pois aparecem na mesma visão.

Os topics têm equivalentes nas outras superfícies do passo 0: `keywords` em `package.json`, `keywords`/`classifiers` em `pyproject.toml`, categorias e tags em marketplaces e lojas. Mantenha-os coerentes em conteúdo — são a mesma decisão, apenas em vários lugares.

### 2a. Portão de privacidade — sempre executado

Este passo nunca é omitido, nem numa rodada aparentemente inofensiva. A busca é feita no conjunto **rastreado**, não na árvore de trabalho visível, pois essa é a diferença entre "parece limpo" e "está limpo".

```bash
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|/home/[a-z]|s[k]-[A-Za-z0-9]{16}|gh[p]_|gh[o]_|AKIA[0-9A-Z]{16}|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|BEGIN [A-Z ]*PRIVATE KEY" $(git ls-files)
rg -n "\x{C3}\x{83}|\x{C2}\x{A0}|\x{FFFD}" $(git ls-files -- '*.md' '*.txt' '*.json')
```

Acrescente ao padrão os **nomes das suas próprias pastas internas** — pastas de pipeline, diretórios temáticos, áreas de trabalho privadas:

```bash
rg -n "\.SOFTWARE|\.RESEARCH|_control-center|<weitere eigene Ordnernamen>" $(git ls-files)
```

Essas referências não são segredos e não disparam alarme, por isso passam — mas são **ininteligíveis** para os leitores ("retransferido do pipeline .SOFTWARE" não diz nada a estranhos) e expõem a estrutura interna. Devem ser substituídas ou removidas, não apenas toleradas. Uma busca que procure só por `C:\Users\…` e padrões de token certamente não as encontra.

Encontrou algo? Então a **natureza** do achado determina o procedimento — veja a seção "Regra do force-push". Um segredo que já foi commitado está queimado: remover de `HEAD` não basta, é preciso rotacioná-lo.

### 2b. Verificar a intenção de publicação dos documentos

É o núcleo desta rodada. Percorra os `.md`, `.txt` e `.json` rastreados e pergunte para cada arquivo: **isso algum dia foi destinado a estranhos?**

```bash
git ls-files -- '*.md' '*.txt' '*.json' | sort
```

Não decida pelo nome do arquivo — abra e veja. Um `PLAN.md` pode ser um roadmap público, e um `notes.md` de nome inofensivo pode ser a estratégia interna de preços. Três categorias:

**Pertence ao repo** — README, LICENSE, CHANGELOG, SECURITY, CONTRIBUTING, `docs/`, referências de API, configs de exemplo, roadmaps reais, manifestos (`package.json`, `pyproject.toml`), lockfiles, configuração de CI.

**Não pertence ao repo, mas é inofensivo** — o caso normal desta rodada. Arquivos de tarefas e planejamento (`AUFGABEN.txt`, `Plan.txt`, `TODO-intern.md`), notas de sessão e passagens de bastão (`HANDOFF`, `BRIEFING`, `_handoff/`), arquivos de status do próprio pipeline, diários de desenvolvimento, `_archive/`, JSONs de registro e índice com caminhos locais, estados intermediários e artefatos gerados, arquivos de trabalho de agentes. Esses arquivos não são perigosos, mas geram desordem e a impressão de um canteiro de obras alheio. Tratamento: acrescentar `.gitignore`, `git rm --cached <datei>` e **enviar normalmente**.

**Não pertence ao repo e é delicado** — credenciais, dados pessoais, dados de clientes, cálculos internos, estratégias de preço e negociação, planos de negócio não publicados, minutas de contrato, tudo o que tenha valor competitivo. Aqui um commit normal não basta; veja a regra do force-push.

Em `.json` vale uma segunda olhada: manifestos e lockfiles ficam, mas configs locais, arquivos de tarefas/registro, exports e tudo com caminhos absolutos ou nomes de host são passageiros clandestinos típicos.

Se você remover um arquivo que alguém possa procurar (um roadmap, por exemplo), mencione brevemente no commit ou no README onde a informação agora está — caso contrário parece um retrocesso.

### 3. Banner

Um banner influencia se alguém chega a começar a ler. Verifique se existe um e se ele está incluído como primeiro elemento no README.

Se faltar, há três caminhos — nesta ordem de sensatez:

1. **Gerador de imagens de um agente** (p. ex. agy; a palavra "gere" (alemão: "generiere") é ali o gatilho para a geração real de PNG), quando um motivo visual combina mais do que tipografia.
2. **Codex**, quando o banner deve surgir a partir de código e existe um modelo de estilo a seguir.
3. **Fazer você mesmo em SVG**, quando o banner é essencialmente uma marca em palavras mais uma linguagem de formas — muitas vezes é a variante mais rápida e mais controlável, e o SVG continua editável depois.

Mantenha a família se o projeto pertence a um grupo: mesma cor-base, mesma estética, mesmo tratamento da marca em palavras. Um banner que foge do conjunto parece pior do que nenhum. Tamanho usual 1200x300; como PNG no repo, com o SVG ao lado como fonte.

### 4. Comparar as afirmações com o estado real

É aqui que surge a maior parte do valor. O README afirma coisas — verifique, em vez de acreditar:

- **Versão** no README/badge contra `pyproject.toml`/`package.json`/`__version__` e contra a última tag de release. Havendo vários portadores de versão, verifique todos, não apenas um.
- **Caminho de instalação** realmente percorrido, pelo menos em modo somente leitura: o pacote existe sob o nome indicado? Os comandos e flags conferem?
- **Lista de funcionalidades** contra o código: está tudo o que é citado, e falta algo novo na lista?
- **Números** (quantidade de ferramentas, formatos suportados, cobertura de testes) contados na fonte, e não copiados adiante. Números no README envelhecem silenciosamente.
- **Capturas de tela** contra a interface atual.
- **Requisitos** (versões de Python/Node, dependências) contra os manifestos.
- **Links** para projetos vizinhos, documentação e registros: ainda funcionam?

**Uma correção vale para todas as superfícies, não só para aquela em que foi notada.** Quando uma afirmação de conteúdo se revela errada — especialmente quando o solicitante a corrige —, a mesma afirmação quase certamente aparece em outro lugar: no perfil da organização, na `llms.txt`, na segunda versão linguística, no README de um projeto vizinho. Procure-a de forma direcionada antes de marcar o item como concluído:

```bash
gh search code "<prägnante Formulierung>" --owner ORG
```

Caso contrário, você corrige um ponto e deixa três de pé — e a contradição só aparece quando o próximo repo entrar na rodada. Isso custa mais do que tempo: prejudica a confiança na documentação. Quem encontra duas descrições da mesma coisa deixa de acreditar em ambas.

Em seguida, melhore a **apresentação** onde ela estiver fraca: listas longas de opções ficam mais legíveis como tabela; blocos de código precisam de tags de linguagem; uma visão de estrutura ou de fluxo é apreendida mais rápido como diagrama Mermaid ou árvore ASCII do que em prosa; a primeira altura de tela deve mostrar finalidade, instalação e um exemplo de uso, não badges e histórico. Se o README passar de ~400 linhas, mova os detalhes para `docs/` e crie links.

**Regra de idioma para READMEs:** o padrão é um **README em inglês `README.md`** mais uma **versão alemã complementar**. Exceção: o domínio de aplicação da ferramenta é ele próprio alemão (direito alemão, sistema fiscal ou de fomento alemão, público-alvo de língua alemã) ou até agora só existe uma versão alemã — então o alemão continua sendo o idioma principal. Para cada outro idioma que o projeto já fala, deve haver uma versão própria do README. Siga a convenção de nomes já usada no repo (`README_de.md`, `README.de.md`, `docs/README.de.md`) e não invente uma segunda ao lado. Linke as versões entre si no cabeçalho.

### 6. Criar os idiomas padrão que faltam

Complete os READMEs que faltam nos **idiomas padrão**: alemão, inglês, espanhol, chinês simplificado, japonês, russo. O objetivo é alcance, por isso isso vale sobretudo para projetos voltados ao usuário final — numa biblioteca voltada a desenvolvedores com público exclusivamente anglófono, um README em russo não traz ganho, apenas mais carga de manutenção. Decida de forma consciente e registre a decisão no protocolo da rodada, para que a próxima não a rediscuta.

Novas versões são **preenchidas, não criadas vazias** — um stub com "TODO: translate" é pior do que nenhum arquivo, porque simula completude. Paridade de conteúdo e reajuste mútuo são regulados por `bilingual-doc-sync`; com mais de duas versões, vale acionar esta skill para a comparação.

### 7. Visibilidade e divulgação

Pense quais medidas trazem usuários para **este** projeto e execute-as:

- **Registros** nos quais o projeto tecnicamente pertence: registros de pacotes (npm, PyPI), MCP-Registry, diretórios de plugins/skills, marketplaces.
- **Listas curadas** (`awesome-*` e coleções temáticas), desde que os critérios de inclusão sejam realmente atendidos. Um PR para uma lista cujos critérios o projeto não cumpre custa reputação.
- **Superfícies próprias**: perfil da organização, `llms.txt`, website do projeto, README do ecossistema, links a partir de repos próprios relacionados.
- **Notas de release** como ocasião: um release sem novidade narrada não é percebido.

**Portão de aprovação:** tudo o que vai para fora — PRs a repos alheios, entradas em listas alheias, posts, submissões — é **proposto e só executado após aprovação expressa**, a menos que exista uma permissão permanente para esse canal. Alterações nas superfícies próprias não precisam desse portão. O motivo é simples: um PR retirado num repo alheio fica visível publicamente e recai sobre o projeto.

### 8. Entrada nas páginas das organizações

Primeiro a própria organização: o repo consta no README do perfil (`ORG/.github` → `profile/README.md`), na seção correta, com descrição atual?

```bash
gh api user/orgs --jq '.[].login'
```

Depois percorra **todas** as organizações e responda para cada uma a uma única pergunta: um visitante dessa página de organização se beneficiaria deste repo? Na maioria das vezes a resposta é não — então "não linkar" é o resultado correto e não uma lacuna. Onde a resposta for sim (proximidade temática, usuários em comum, uma ferramenta que complementa os projetos de lá), coloque o link com uma linha que explique a utilidade, e não apenas o nome.

O perfil fica num repo próprio (`ORG/.github`). Alterações ali são mantidas e enviadas — conforme a regra de árvore suja do passo 11.

### 10. Issues e Pull Requests

```bash
gh issue list --repo ORG/REPO --state open --limit 50
gh pr list --repo ORG/REPO --state open --limit 30
```

Trabalhe-os em vez de apenas contá-los:

- **Bugs corrigíveis** diretamente — nesta rodada o contexto já está carregado. Correções pequenas e bem delimitadas, com teste e referência ao número da issue.
- **Issues já resolvidas** fechadas, com uma frase sobre o que as resolveu.
- **Relatos pouco claros** precisam de uma pergunta direcionada (versão, sistema operacional, passos para reproduzir).
- **PRs**: ler de fato o diff, executar os testes, depois fazer merge ou devolver com justificativa. Um PR que fica meses sem resposta custa mais boa vontade do que uma recusa educada.
- **Casos obsoletos** resolvidos em vez de arrastados.

**Portão de aprovação:** comentários públicos, fechamentos com justificativa e merges de contribuições alheias são comunicação externa — apresente antes de executar, a menos que exista permissão permanente. Correções de código puramente no repo próprio não são afetadas.

### 11. Commit, push, verificação

A rodada não termina com as alterações, mas com elas **publicadas**. Uma árvore de trabalho cheia de melhorias não enviadas é o pior resultado: a próxima sessão — talvez outro agente ou outro dispositivo — precisa primeiro se orientar num estado alheio e meio pronto, e nas superfícies públicas nada melhorou.

Antes do push, assegure o que for verificável: execute testes e smoke tests; em alterações de documentação, confira links e a visualização renderizada. Depois agrupe em **commits temáticos separados**, em vez de jogar tudo num commit único — limpeza, atualização da documentação e correções de bug são três coisas diferentes, e quem quiser desfazer uma delas mais tarde agradecerá:

```bash
git add .gitignore && git rm --cached <interne dateien>
git commit -m "chore: interne Arbeitsdateien aus dem Repo nehmen"
git commit -am "docs: README auf aktuellen Stand (Version, Toolzahl, Screenshots)"
git commit -am "fix: <Issue-Nummer> ..."

git pull --rebase        # bei divergiertem Branch, vor dem Push
git push
```

Depois verifique em vez de presumir: README remoto na visualização renderizada, execução de CI, estado de release e tags.

```bash
gh run list --repo ORG/REPO --limit 3
gh repo view ORG/REPO --json description,repositoryTopics,url
```

**Se a CI estiver vermelha apesar de o seu commit só ter mexido na documentação**, a causa quase nunca é você. O caso de longe mais frequente — nesta família de repos, verificado **três vezes** num único dia — é um **linter sem versão fixada e sem conjunto de regras definido**. Verifique isso **primeiro**, antes de suspeitar de qualquer coisa no seu commit.

O mecanismo: se o workflow `ruff check` (ou flake8, eslint …) roda contra uma dependência não fixada (`ruff>=0.12`, ou sem nenhuma versão) e falta uma seleção explícita de regras (`[tool.ruff.lint] select = [...]`, ou, na ausência de `pyproject.toml`, uma própria `ruff.toml`), então o lint segue o padrão da versão **recém-instalada**. Um novo release do linter desloca esse padrão, e uma base de código inalterada fica vermelha. Os culpados:

- Códigos de regra que o projeto nunca teve (`UP045`, `UP006`, `BLE001`, `RUF100`, `DTZ005`, `N999` …), às vezes na casa das centenas.
- A quebra costuma aparecer **dividida por plataforma**: runners com uma versão mais antiga em cache continuam verdes, os novos ficam vermelhos.
- Às vezes uma regra aponta algo que não se pode corrigir (`N999` o próprio nome do pacote) — sinal seguro de que ela nunca foi padrão.

Correção: fixar o conjunto de regras que antes estava verde — `select = ["E4","E7","E9","F"]` são os padrões clássicos do ruff. Se não existir `pyproject.toml`, crie uma `ruff.toml`. Verifique contra a **nova** versão do linter (instalar, reproduzir os achados sem configuração, confirmar "passed" com a configuração). As novas regras entram no projeto como **tarefa** — adotá-las é uma decisão, não um efeito colateral de uma atualização de ferramenta. Trata-se de um achado real e recorrente: sem o pin, a CI volta a quebrar no próximo release do linter, e isso acontece em **todo** repo configurado dessa forma.

Dois casos em que **não** se envia: quando há um bloqueio de publicação ou submissão para o projeto, ou quando o estado é declaradamente incompleto. Ambos são exceções que devem ser justificadas — o caso normal é: commitar e enviar.

Diante de um bloqueio de publicação, a rodada não é abortada, mas **redirecionada**: commit local em um branch próprio (`judging-hold/…`, `freeze/…`), deixando o branch principal intocado no estado submetido, anotando o motivo do bloqueio no protocolo e recuperando depois do levantamento. O essencial é ser consistente: bloqueado não é só o `git push`, mas **toda alteração visível remotamente** — topics, descrição, homepage, releases, ações em issues e PRs modificam o projeto publicado da mesma forma.

Existindo outros clones do mesmo repo (segundo dispositivo, cópia de deploy, espelho), atualize-os logo após o push. Um clone dez commits atrás produz diagnósticos sobre um estado que já não existe na próxima busca de erro.

#### Alterações em outros repos — exceção de árvore suja

Esta rodada gera regularmente alterações **fora** do repo mantido: uma linha no perfil da organização (passo 8), mais tarde, na rodada profunda, um link de retorno num repo relacionado. Essas alterações também são commitadas e enviadas — um link de retorno não publicado não é um link de retorno.

Antes de mexer num repo alheio, verifique rapidamente o estado dele:

```bash
git -C <pfad> status --porcelain
```

**Árvore de trabalho limpa** → faça a alteração, faça o commit em um **commit próprio e temático** (`docs: link <projekt>`) e envie. Não misture com os commits do repo mantido: é outro repo, com histórico próprio e leitores próprios.

**Suja, mas as alterações alheias estão em outros arquivos** → sua alteração ainda pode ser feita de forma limpa. Faça stage e commit **apenas do seu arquivo, por caminho**, para que trabalho alheio não verificado não entre junto:

```bash
git -C <pfad> add README.md
git -C <pfad> commit -m "docs: link <projekt>"     # nur der gestagte Pfad
```

Mas **não envie**. O commit é localmente inofensivo; um push não necessariamente o é: você não sabe para onde o outro trabalho está caminhando — talvez esteja sendo amendado, rebaseado ou reorganizado, e seu commit o forçaria a lidar com isso. O commit local preserva o seu trabalho sem impor nada a ninguém; a rodada que voltar a esse repo mais tarde o encontrará e o incorporará.

**Suja exatamente no arquivo que você precisaria alterar** → não toque. Você teria de se apoiar num estado intermediário alheio e commitá-lo junto; entendê-lo custaria mais do que vale esse único link.

**Bloqueio ativo (`LOCK*.txt`) no repo-alvo** → **leia primeiro o lock, em vez de tratá-lo como proibição geral.** Um bloqueio descreve o próprio escopo, que muitas vezes é mais estreito do que "nada". Casos típicos:

- **Bloqueio de edição** ("alguém está trabalhando aqui agora") → não toque em nada, nem em arquivos secundários.
- **Bloqueio apenas de publicação/push** (submissão, julgamento, congelamento) → o trabalho local continua permitido; só o contato remoto está bloqueado. Então trabalhe em um branch próprio e commite localmente; **as etapas com efeito remoto são omitidas** — não só o push, mas também topics, descrição, homepage, releases e ações em issues/PRs, pois também modificam o projeto publicado.

Ler um lock que bloqueia apenas o push como proibição total custa toda a parte local da rodada sem ganho de segurança. Inversamente, não basta deixar de fazer o push e mesmo assim alterar metadados. Na dúvida, cite o lock e pergunte.

#### O desejo não pode se perder

Se a alteração **não** for executada por qualquer desses motivos, ela vai para a lista de tarefas do repo-alvo — `AUFGABEN.txt`, `TODO.md` ou `TODO.txt`, conforme o que existir ali. Uma entrada com data, a alteração desejada e o motivo:

```markdown
- [ ] [2026-07-24, after-care] Rückverweis auf <projekt> im README ergänzen
      (übersprungen: README hatte uncommittete Fremdänderungen)
```

Essa é a diferença entre "adiado" e "esquecido": a lista de tarefas fica onde o próximo responsável por esse repo olha de qualquer forma — mais confiável do que uma anotação no protocolo de uma rodada alheia. Se não existir lista de tarefas, não crie uma; então basta o ponto em aberto no próprio protocolo da rodada.

Diante de um **bloqueio ativo**, isso também não se aplica — nesse caso o arquivo não é tocado e a anotação permanece no protocolo da própria rodada. Registre-a nos dois casos também ali, para que a rotação conheça o ponto em aberto.

Por fim, atenda as superfícies do passo 0 — veja a seção seguinte.

## Paridade em todas as superfícies de distribuição

Ao final da rodada, percorra a lista do passo 0: **toda alteração que um usuário veria precisa chegar a cada superfície onde ele a procura.** Um repo cuja página no npm conta outra história está em pior situação do que um com apenas uma superfície.

O mecanismo decisivo: **registros de pacotes exibem o README da última publicação, não o estado atual do repo.** Uma correção no README só aparece no npm ou no PyPI com uma nova versão. Se a correção for relevante do ponto de vista de conteúdo (instalação errada, versão errada, lista de funcionalidades desatualizada), é necessário um release de patch — caso contrário a correção não tem efeito.

| Superfície | O que é mantido ali | Como chega |
|---|---|---|
| npm | README, `description`, `keywords`, link do repositório | Somente com `npm publish` (versão de patch); os metadados vêm de `package.json` |
| PyPI | README (`long_description`), classifiers, URLs do projeto | Somente com novo upload; metadados de `pyproject.toml` |
| MCP-Registry / diretórios de plugins | Descrição, versão, lista de ferramentas, documentação de entrada | Conforme o registro: atualização do manifesto ou nova submissão |
| Marketplace / loja | Descrição, capturas de tela, categorias, versões linguísticas | Pela interface de gestão correspondente; capturas envelhecem ali especialmente rápido |
| Docker Hub / registro de contêineres | Descrição, tags, exemplo de uso | Descrição do repositório mais nova tag |
| Zenodo / DOI | Metadados, autores, versão | Edição in place para metadados, nova versão para conteúdo |
| Website / perfil da org. / `llms.txt` | Descrição curta, link, posicionamento | Editável diretamente — as superfícies mais baratas, por isso nunca esquecê-las |

Quando uma versão é elevada, **todos os portadores de versão** devem mudar juntos: manifesto, constante no código, badge do README, changelog, tag de release, `llms.txt`. Um estado de versão pela metade é mais difícil de diagnosticar do que um uniformemente antigo.

Se uma atualização não for possível ou não fizer sentido em uma superfície (por exemplo, um release só por causa de um erro de digitação), registre isso no protocolo da rodada, para que a próxima não tome a divergência por descuido.

## Regra do force-push

O padrão é **nenhum force-push**. Ignorar arquivos internos de planejamento depois do fato não justifica reescrever o histórico: o custo é alto, cada clone e cada fork se quebra, PRs abertos ficam inutilizáveis — e o ganho é pequeno, porque o conteúdo é inofensivo. Caminho normal:

```bash
git rm --cached <datei>            # aus dem Tracking, bleibt lokal erhalten
# .gitignore ergänzen
git commit -m "chore: interne Arbeitsdateien aus dem Repo nehmen"
git push
```

Reescrever o histórico (e portanto `--force-with-lease`) só se justifica em **vazamentos reais**: credenciais e chaves, dados pessoais ou de clientes, além de documentos com valor competitivo real — cálculos internos, estratégias de preço, planos não publicados, detalhes internos de contratos. Nesse caso:

1. **Rotacionar primeiro** os segredos afetados — o histórico já foi copiado, bifurcado e posto em caches nesse momento. A rotação tem efeito, apagar é apenas cosmético.
2. Limpar o histórico (`git filter-repo` ou BFG) e enviar com `--force-with-lease`.
3. Verificar forks e caches; se necessário, acionar o suporte do GitHub para objetos órfãos.
4. Registrar o procedimento no protocolo da rodada: o quê, quando, qual rotação.

Na dúvida entre "inofensivo" e "delicado": trate como delicado e apresente. Os custos são assimétricos.

## Achados viram tarefas, não apenas linhas de protocolo

Uma rodada de manutenção frequentemente encontra mais do que consegue ou deve corrigir na mesma rodada: uma versão linguística que falta, um atraso de modernização, uma publicação que nunca aconteceu. **Esses achados viram tarefas no momento em que são descobertos** — senão ficam no protocolo de uma execução encerrada, onde o próximo responsável pelo projeto não olha.

A tarefa pertence ao **sistema de tarefas local à pasta do projeto** — onde quem trabalhar no projeto em seguida vai procurar. Normalmente é `AUFGABEN.txt` ou `TODO.md` na pasta do projeto, e ela muitas vezes **não está no clone Git**, mas na área onde o planejamento vive. O clone contém o código; a pasta do projeto contém o controle e o planejamento; uma entrada no clone que desaparece no próximo `git clean` não é uma tarefa.

Três pontos a observar:

1. **Separar lista interna de tarefas do roadmap público.** Um `TODO.md` pode ser um roadmap público mantido — então não é lugar para trabalho interno pendente. Antes de anexar, olhe: se houver um título como "Public roadmap", escreva no arquivo interno ao lado (`AUFGABEN.txt`) e marque-o como interno.
2. **Verificar entradas existentes em vez de duplicar.** Muitas vezes o achado já está lá. Então ele não é criado de novo, mas **enriquecido** — com a evidência empírica desta execução ("confirmado: `--help` emite saídas inteiramente em alemão"). Um ponto conhecido com prova nova vale mais do que uma segunda entrada ao lado.
3. **Registrar o que foi resolvido.** O que a rodada corrigiu entra como item marcado com o hash do commit. Isso explica à próxima rodada por que um achado desapareceu e evita que ela o "redescubra".

Formule a tarefa de modo que ela seja compreensível sem o contexto desta execução: o que foi encontrado, por que importa, qual seria o próximo passo. "i18n incompleto" não é uma tarefa; "o catálogo contém só `status.title`, em es/zh/ja/ru está vazio — primeiro transferir as strings da CLI para o catálogo, depois preencher as seis línguas" é uma tarefa.

## Protocolo da rodada

Registre o resultado em `_after-care/LOG.md` (a pasta pertence à `.gitignore` — é material de pipeline, não conteúdo do repo, exatamente segundo a regra do passo 2b). Uma linha por execução, com data, nível e as decisões tomadas de forma consciente:

```markdown
## 2026-07-24 — surface
- Flächen: GitHub, npm (<paket>), MCP-Registry, Org-Profil, llms.txt
- Topics: +local-first, +mcp-server; keywords in package.json angeglichen
- Entfernt: AUFGABEN.txt, _handoff/ (gitignored, kein Force-Push nötig)
- README: Version 0.9 -> 1.2 korrigiert, Toolzahl 23 -> 26 nachgezählt
- Sprachen: EN + DE gepflegt; ES/ZH/JA/RU bewusst nicht (entwicklernahes Publikum)
- Issues: #12 gefixt, #7 geschlossen (erledigt), #15 Rückfrage gestellt
- Push: 3 Commits, CI grün; npm-Republish 1.2.1 wegen README-Korrektur
- Offen: Store-Screenshots veraltet, brauchen neuen Build
```

O protocolo poupa à próxima rodada tomar de novo as mesmas decisões e serve de base para as rodadas de manutenção rotativas em muitos repos (`rotation-check`).

## Erros frequentes

| Erro | Correção |
|---|---|
| Olhou só a árvore de trabalho, não `git ls-files` | Verificar sempre o conjunto rastreado — é lá que está o problema |
| Portão de privacidade voltado só para caminhos e tokens | Buscar também pelos nomes das próprias pastas de pipeline/internas — não disparam alarme e passam |
| Arquivo interno removido e histórico reescrito por isso | Para arquivos inofensivos basta `git rm --cached` + push normal |
| Segredo removido de `HEAD` e caso dado como encerrado | Rotacionar o segredo; o resto é cosmético |
| Arquivos classificados pelo nome | Abrir rapidamente — o nome não carrega a intenção de forma confiável |
| Números no README atualizados por cópia, não recontados | Contar na fonte (lista de ferramentas, execução de testes, manifesto) |
| Nova versão linguística criada como stub vazio | Preencher ou não criar — um stub simula completude |
| Segunda convenção de nomes de README introduzida ao lado da existente | Adotar a convenção já existente |
| PR a uma lista alheia enviado sem aprovação | Apresentar comunicação externa; só as superfícies próprias são livres |
| Issues contadas em vez de trabalhadas | Corrigir, fechar ou perguntar de forma direcionada — cada caso recebe um estado |
| Banner criado por conta própria em estilo alheio | Respeitar a família de design do ecossistema |
| README corrigido no repo, mas a página do npm/PyPI continua com a versão antiga | As páginas de registro vêm da última publicação — providenciar um release de patch |
| Versão elevada só no manifesto | Todos os portadores de versão juntos: manifesto, código, badge, changelog, tag, `llms.txt` |
| Alterações prontas, mas deixadas sem push | Commitar e enviar faz parte da rodada; só bloqueios justificam exceção |
| Tudo num único commit de conjunto | Separar limpeza, documentação e correções — senão nada é desfeito individualmente |
| CI vermelha após commit de documentação, suspeitando do próprio commit | Linter sem versão fixada e sem `select` segue o padrão da nova versão — fixar o conjunto de regras |
| Afirmação errada corrigida só onde foi notada | Buscar a formulação em toda a organização — normalmente ela também está no perfil, em `llms.txt` e na segunda versão linguística |
| Trabalho feito em repo alheio sujo com `commit -a` | Stage e commit por caminho, sem push — o trabalho alheio fica intocado |
| Alteração feita num repo de perfil limpo, mas sem push | Repos alheios limpos recebem um commit próprio **e** um push próprio |
| Alteração não executada só anotada no protocolo próprio | Também registrar na lista de tarefas do repo-alvo, se existir |
| Achado só anotado no protocolo da rodada | Ele vira tarefa no sistema de tarefas local à pasta — ninguém olha o protocolo depois |
| Trabalho interno pendurado num roadmap público | Olhar antes; "Public roadmap" significa: usar o arquivo interno ao lado |
| Achado conhecido duplicado como nova entrada | Enriquecer o ponto existente com a evidência empírica desta rodada |
| Diante de bloqueio de edição, uma linha TODO escrita no repo bloqueado | Esse bloqueio vale para o projeto inteiro — não tocar em nada ali |
| Bloqueio de push lido como proibição total e o repo inteiro foi pulado | Ler o lock: se bloqueia só a publicação, a rodada local segue num branch próprio |
| Sob bloqueio de push, sem enviar, mas com topics ou descrição alterados | Metadados também são visíveis remotamente — sob bloqueio de publicação eles são omitidos também |

## Checklist de encerramento

- [ ] Superfícies de distribuição identificadas e registradas no protocolo da rodada.
- [ ] Topics, description e homepage definidos e verificados.
- [ ] Portão de privacidade executado sobre o conjunto rastreado; achados tratados.
- [ ] `.md`/`.txt`/`.json` verificados quanto à intenção de publicação; arquivos internos ignorados.
- [ ] Nenhum force-push sem vazamento real; em caso de vazamento, rotação executada.
- [ ] Banner presente e incluído no README.
- [ ] Versão, funcionalidades, números, capturas de tela e links conferidos com o estado real.
- [ ] Apresentação melhorada (tabelas, diagramas, primeira altura de tela).
- [ ] Matriz de idiomas do README completa; decisões sobre outros idiomas documentadas.
- [ ] Medidas de visibilidade executadas ou apresentadas para aprovação.
- [ ] Entrada no próprio perfil da organização verificada; links relevantes para outras organizações definidos.
- [ ] Alterações em repos alheios: limpos → commitados e enviados; sujos → commitados localmente;
      não executadas → registradas na lista de tarefas do repo-alvo.
- [ ] Issues e PRs levados a um estado definido.
- [ ] Commits separados criados, enviados, CI e visualização remota verificadas.
- [ ] Todas as superfícies de distribuição levadas ao mesmo estado (se necessário, release de patch).
- [ ] Achados não corrigidos registrados como tarefas no sistema de tarefas local à pasta.
- [ ] Protocolo da rodada escrito em `_after-care/LOG.md`.

## Changelog

### 1.6.0 (2026-07-24)
- Regra acrescentada: uma correção de conteúdo vale para todas as superfícies. Aprendido empiricamente — um
  esclarecimento do usuário foi corrigido no hub na rodada 1, mas continuou sem ser notado em cinco lugares
  no perfil da organização (EN, DE, `llms.txt`), e só foi notado nove rodadas depois.

### 1.5.0 (2026-07-24)
- Diagnóstico do linter reforçado, depois de o padrão ter ocorrido três vezes num único dia
  (n8n-workflow-manager com ruff 0.15; clirec + swarm-ai com ruff 0.16): "verificar primeiro", os
  códigos de regra típicos do problema, a divisão por plataforma, `ruff.toml` como correção quando
  falta `pyproject.toml`, verificação contra a nova versão do linter.

### 1.4.0 (2026-07-24)
- Diagnóstico acrescentado: quando a CI fica vermelha após um commit puramente de documentação, a causa mais
  frequente é um linter sem versão fixada e sem conjunto de regras definido — um novo release da ferramenta
  desloca o padrão e torna código inalterado vermelho. Correção: fixar o conjunto de regras, novas regras como
  tarefa. Ocorreu duas vezes seguidas (n8n-workflow-manager com ruff 0.15, clirec com 0.16).

### 1.3.0 (2026-07-24)
- Nova seção "Achados viram tarefas": o que a rodada não corrige sozinha vira, no momento da descoberta, uma
  entrada no sistema de tarefas local à pasta do projeto — onde o próximo responsável procura, não no protocolo
  de uma execução encerrada. Inclui a separação entre lista interna e roadmap público, enriquecer em vez de
  duplicar, e o registro do que foi resolvido com commit.

### 1.2.0 (2026-07-24)
- O portão de privacidade passa a buscar também pelos nomes das próprias pastas internas. Não são segredos,
  portanto não disparam alarme e passam por um portão que só busca caminhos e tokens — mas permanecem
  ininteligíveis para os leitores e expõem a estrutura interna.

### 1.1.0 (2026-07-24)
- Bloqueios passam a ser lidos em vez de tratados como proibição geral: um bloqueio puro de publicação/push
  redireciona a rodada para um branch local, em vez de interrompê-la. Ao mesmo tempo, fica claro que sob esse
  bloqueio também saem metadados, releases e ações em issues/PRs — são tão visíveis remotamente quanto um push.

### 1.0.0 (2026-07-24)
- Versão inicial. Nível 1 da manutenção de repositórios, derivado de `github-repo-care`.
