---
name: bilingual-doc-sync
version: 1.5.1
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-10-15
description: "Manter sincronizadas as versões linguísticas paralelas de um documento (artigo DE/EN, README + README_de, SKILL.md + SKILL.en.md, textos de site): completar a versão ausente, verificar a paridade das seções e corrigir divergências, com uma regra clara de idioma-guia e retransferência controlada quando a versão secundária resolver algo melhor. Use esta skill em perguntas como „DE e EN estão sincronizados?\", „atualize a versão em inglês/alemão\", „a tradução está desatualizada\", em artigos, READMEs ou skills bilíngues, ou como verificação periódica sobre um conjunto de documentos. Inclui também a auditoria de expansão: avaliar se um projeto/documento MERECE OUTROS idiomas (aptidão para i18n conforme o público-alvo, preparação técnica, sem tradução em massa às cegas)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: utilities
tags: [übersetzung, zweisprachig, synchronisation, paper, readme, i18n, dokumentation]
language: pt
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: [markdown-it-py]

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: cc96429f6f5663a7890b76c0958f3c19c1856fccbd65cd0505a75f831260d65d
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:40:39.337351+00:00"
---
<img src="banner.png" width="100%" alt="bilingual-doc-sync banner">
# Bilingual-Doc-Sync — manter versões linguísticas paralelas sincronizadas

## Finalidade

Documentos bilíngues divergem aos poucos: a versão ativamente editada cresce, a outra
fica desatualizada, até que "tradução" só seja verdadeira no nome. Esta skill transforma
a verificação de sincronização em um procedimento definido, com uma decisão prévia
decisiva: **qual versão é a guia?** Sem uma regra de idioma-guia, cada divergência vira
uma decisão caso a caso e a verificação não pode ser repetida.

## Procedimento

### 0. Reconhecer conteúdo monolíngue (ANTES de qualquer comparação)

Divergência nem sempre significa "desatualizado". Às vezes é **conteúdo novo e real que,
até agora, existe apenas em uma versão** (uma contribuição externa/PR em um idioma que não
é o guia, uma alteração que chegou primeiro à versão secundária, ou perda de conteúdo
causada por uma reescrita do histórico etc.). O procedimento original conhecia apenas
"inserir em EN ou DE e depois distribuir para todos", sem nenhum caso em que algo existe
só em uma versão. Caso de referência: `ellmos-ai/skills` PR #1 inseriu um link de
descoberta em chinês apenas em README.md; uma reescrita posterior do histórico o removeu
novamente, porque nenhum passo verificou se existia conteúdo que não está em nenhuma outra
versão (T-20260926-967984806).

- **Verificar, não presumir:** antes da comparação propriamente dita (passo 3), gere um
  diff em relação ao último estado sincronizado conhecido (ou diretamente em relação às
  outras versões) e procure, de forma direcionada, conteúdo que é novo em UMA versão e não
  tem contrapartida em NENHUMA outra, e não apenas seções do idioma-guia que faltam.
- **Ferramenta:** `scripts/check_language_parity.py <datei1> <datei2> [...]` extrai links Markdown E HTML
  (`[text](url)`, `<a href="url">`, `<img src="url">`) de todas as versões
  fornecidas (os links permanecem inalterados após a tradução e, por isso, são um
  indicador robusto e independente do idioma) e reporta cada link que não aparece em TODAS
  as versões, com saída 1. Saída 0 significa: nenhum desvio de subconjunto de links foi
  encontrado. Isso não é prova de paridade completa, mas é um teste rápido e direcionado do
  passo 0 antes da comparação manual. Links dentro de um bloco `<!-- lang-only: <code> -->` são
  verificados apenas contra arquivos cujo código de idioma está indicado na marcação
  (reconhecido pelo nome do arquivo, por exemplo `README_zh.md` → `zh`,
  `README.md` → `en`); nesse caso, eles NÃO contam como "ausente nas
  outras versões". Além disso, o script filtra por padrão URLs de badge `shields.io`
  com texto de rótulo codificado, pois ali muitas vezes está diretamente na URL o rótulo
  traduzido. Isso não é perda real de conteúdo, mas uma variação de tradução esperada;
  `--include-badges` desativa esse filtro. Arquivos não legíveis como UTF-8 e argumentos
  ausentes terminam com saída 2 e uma mensagem de erro, não com um traceback.
- **Decisão ao encontrar algo:** conteúdo monolíngue NUNCA é descartado silenciosamente.
  Há três saídas, sem exclusão silenciosa:
  (a) **traduzir e incorporar em TODAS as versões**: o caso normal para conteúdo de
  relevância geral;
  (b) **limitar deliberadamente a um ou mais idiomas** ("lang-only"), quando o conteúdo vale
  apenas para esse público-alvo (caso de referência T-20260926-967984806: um link de
  descoberta em chinês não é relevante para leitores de DE/ES/JA/RU, e uma tradução em
  todas as seis versões teria sido incorreta; correção do usuário após a primeira versão
  deste passo). Marcação: **`<!-- lang-only: <code>[,<code>...] --> … <!-- /lang-only -->`** (comentário HTML, invisível em renderizadores
  Markdown; para vários idiomas de destino, separados por vírgula, por exemplo
  `zh,ja`). Não se conhece um padrão consolidado da indústria para este caso
  restrito (P-009 verificado); comentários HTML são a opção mais portátil e invisível na
  renderização do Markdown. Conteúdo marcado **não é traduzido nem reportado como ausente**
  durante a comparação;
  (c) **escalar como conflito**, quando não estiver claro se o conteúdo ainda é desejado
  (por exemplo, se parece contraditório em relação à versão guia): perguntar ao usuário ou
  à cadeia de decisão.
  Em todos os três casos vale: nunca remover sem comentário da versão em que o conteúdo
  está, apenas porque as outras não o têm.

### 1. Verificar o estoque

- Existem todas as versões linguísticas (ou todas as duas)? Se uma estiver completamente
  ausente → **completar** (tradução integral da versão guia, não uma reescrita livre).
- Verificar a convenção de nomes (por exemplo, `DOKUMENT.md` + `DOKUMENT.en.md`
  ou os sufixos `_de`/`_en`) e alinhar os desvios:
  a localizabilidade é metade da sincronização.

### 2. Esclarecer o idioma-guia (antes de qualquer comparação)

- O idioma-guia é a versão em que o trabalho de conteúdo é feito (em artigos, muitas vezes
  EN; em documentação local, muitas vezes o idioma materno). Ele prevalece em caso de
  contradição.
- **Exceção de retransferência:** se a versão secundária resolver algo comprovadamente
  melhor (formulação mais clara, erro corrigido), isso é INCORPORADO à versão guia:
  primeiro retransfira, depois sincronize normalmente. Verifique a correção técnica antes
  de adotar uma formulação "mais bonita".

### 3. Verificar a paridade

Primeiro a estrutura, depois o conteúdo:

1. **Comparação de estrutura:** lado a lado, as seções e títulos das duas versões. Seções
   ausentes, adicionais ou reordenadas são as divergências grosseiras.
2. **Amostragem por seção** da estrutura coincidente: afirmações, números, referências e
   exemplos são idênticos? Particularmente sujeitos a divergência: changelogs, tabelas,
   valores numéricos, listas de literatura/links e as seções editadas por último.
3. **Verificar invariantes não traduzíveis:** blocos de código, identificadores, fórmulas e
   caminhos devem ser IDÊNTICOS nas duas versões (código nunca é traduzido).

### 4. Corrigir

- Resolver as divergências na direção da versão guia (ou após a retransferência).
- Respeitar a tipografia da língua-alvo (em alemão, umlauts reais ä ö ü ß, sem substituição
  por ae/oe/ue; convenções de aspas).
- Atualizar os metadados: números de versão, campos de data, entradas de changelog em
  AMBAS as versões (o próprio changelog é o ponto de divergência mais frequente).

### 5. Documentar

Registrar o resultado (o que estava divergente, o que foi incorporado, o que foi
retransferido). Como execução periódica sobre um conjunto de documentos: combinar com a
estrutura de rotação (`rotation-check`), um documento (ou par de documentos) por
execução, usando o registro como memória.

## Extensão: auditoria de expansão (deveriam existir MAIS idiomas?)

Além de manter sincronizadas as versões existentes, faz parte do cuidado com os idiomas
a pergunta sobre se um documento/projeto MERECE outros idiomas:

1. **Avaliar a aptidão** em vez de traduzir às cegas: público-alvo, utilidade internacional,
   presença em lojas/web, mobilidade do conteúdo. Nem todo documento interno precisa de
   inglês; nem todo app precisa de cinco idiomas.
2. **Verificar a preparação técnica:** o alvo está preparado para arquivos de idioma ou
   versões paralelas (estrutura i18n, convenção de nomes)? Se não estiver, ESSA é a primeira
   tarefa, não a tradução.
3. **Documentar o resultado, sem traduzir em massa imediatamente:** tarefas de tradução
   concretas vão para o arquivo TODO local do projeto; "nenhum idioma adicional faz sentido"
   é um resultado válido e que deve ser registrado.
4. **QA das versões criadas:** verificar por amostragem as traduções geradas automaticamente
   contra a versão guia (seção 3), antes de considerá-las "disponíveis".

## Exemplo

```text
Auftrag: „Prüf, ob das Paper in DE und EN synchron ist."

1. Bestand: paper_en.tex (führend) + paper_de.tex vorhanden.
2. Gliederung: DE fehlt der neue Abschnitt 4.2 (letzte EN-Revision); DE hat einen
   besseren Beweis-Absatz in 3.1.
3. Rücktransfer: 3.1-Formulierung fachlich geprüft → in EN übernommen.
4. Nachziehen: 4.2 nach DE übersetzt; Zahlen in Tabelle 2 abgeglichen (DE hatte
   veraltete Werte); Literaturverzeichnis identisch gemacht.
5. Registry-Eintrag: „paper-X | 2026-07-03 | de-en-sync | 3 Divergenzen behoben,
   1 Rücktransfer | nächster Check nach nächster EN-Revision".
```

## Red Flags

| Pensamento | Realidade |
| --- | --- |
| „Eu simplesmente traduzo as diferenças de novo" | Primeiro esclareça o idioma-guia e a questão da retransferência, senão a solução melhor será sobrescrita. |
| „A estrutura confere, então está sincronizado" | Números, changelogs e referências divergem primeiro: a amostragem em profundidade é obrigatória. |
| „Eu também traduzo os comentários do código" | Blocos de código e identificadores permanecem idênticos nas duas versões (em inglês). |
| „Sincronizo todos os documentos de uma vez" | Um par por execução (estrutura de rotação) mantém a comparação verificável. |

## Traduções em série autorizadas

Quando há um pedido explícito para um estoque linguístico inteiro, `scripts/worldset.py`
apoia o procedimento com a Claude Message Batches API. A unidade de trabalho é fonte ×
idioma × SHA-256. O script exige apenas Python 3.10 ou mais recente, além de
`pip install -r scripts/requirements.txt`. A lista de idiomas é adotada explicitamente da convenção vigente de
cada projeto; os códigos integrados são DE, EN, ES, ZH, JA, RU, FR, HI, AR, BN e PT.

```bash
python scripts/worldset.py scan --root /path/to/checkout --kind skills --out /private/run/plan.json
python scripts/worldset.py submit --projection /private/run/plan.json --receipt /private/run/batch.json --limit 20
python scripts/worldset.py collect --receipt /private/run/batch.json --out /private/run/results
```

`--kind readme` planeja, em vez disso, versões linguísticas de README. README.md é, por
padrão, em inglês; um idioma-guia diferente deve ser declarado explicitamente com
`<!-- source-language: de -->`. Antes disso, verifique o estoque quanto a nomes de arquivo
alternativos já estabelecidos.

`retry-plan --receipt ... --results ... --out ...` cria, a partir de falhas de gate concluídas, exatamente uma tentativa
de correção. Falhas repetidas permanecem para revisão. Para cada idioma, `submit --glossary <json>`
pode usar um objeto de terminologia; suas entradas são fornecidas ao respectivo especialista
linguístico.

A chave de API vem de `ANTHROPIC_API_KEY` ou `--key-file`; seu valor não é gravado
nem em receipts nem em traduções. Use apenas o saldo existente explicitamente liberado,
nunca recarregue automaticamente. O script encerra o trabalho na nuvem quando não há saldo.
Um adaptador de modelo local precisa de liberação e verificação de recursos próprias.

A projeção é um snapshot da entrada, não uma segunda fila de tarefas. O ID do batch do
provedor é o handle de execução; batches em andamento são consultados, não reenviados.
Um receipt sem ID de batch após uma falha de transporte deve ser conciliado com a lista de
batches do provedor. Não repita envios às cegas. Modelos e glossários são dados não
confiáveis.

As saídas ficam exclusivamente em `raw/` e, após verificações estruturais e
linguísticas aprovadas, em `candidates/`. Mesmo candidatos aprovados precisam de uma
amostragem linguística independente; verificações mecânicas não comprovam a qualidade da
tradução. Versões linguísticas existentes sem hash de fonte são preservadas, pois podem conter
complementos independentes. `--include-stale` replaneja apenas traduções desatualizadas
previamente marcadas com hash. Antes da incorporação, verifique novamente o hash da fonte, o
estado-alvo e os locks; depois, execute os gates regulares de repositório, privacidade, commit
e deployment. Execução em segundo plano somente pelo scheduler já responsável, com seu contrato
de claim e de recursos.

### Verificação linguística separada por API

Na varredura, vale o idioma de origem declarado; na falta dele, o alemão padrão para skills
próprias. Para fontes estrangeiras em inglês, \`--source-language en\` deve ser indicado
explicitamente; \`--kind skills-flat\` oferece suporte a uma biblioteca plana de skills.
\`--source-languages\` carrega, em bibliotecas mistas, um mapeamento JSON verificado de
caminho relativo da fonte para código de idioma. O arquivo de origem é preservado; versões
alemãs ausentes são então criadas como \`SKILL.de.md\`. Pastas de idioma antigas já existentes,
como \`EN/SKILL.md\` ou \`fr/SKILL.md\`, contam como versões preservadas e não são
complementadas por arquivos concorrentes.

`scripts/worldset_review.py` prepara candidatos aprovados para uma verificação linguística
independente. O tradutor continua sendo o Haiku; o modelo de verificação é indicado
separadamente. Use primeiro uma amostra controlada com exemplos já verificados e só então
defina o escopo adicional de verificação com base na taxa de erro.

```bash
python scripts/worldset_review.py prepare --translation-receipt batch.json --results-dir staging --out review-plan.json
python scripts/worldset_review.py submit --projection review-plan.json --receipt review-batch.json --model claude-sonnet-5-5
python scripts/worldset_review.py collect --receipt review-batch.json --out review-results
```

A verificação lê integralmente cada fonte e cada versão selecionadas. Sua decisão está
vinculada ao hash da fonte, ao hash do candidato, aos caminhos, ao idioma e ao modelo de
verificação efetivamente observado. Erros de significado e gatilhos locais ausentes bloqueiam
a incorporação, mesmo com uma pontuação geral alta. Devido à taxa de erro no piloto, o
verificador automático exige no mínimo 4,5 de 5 pontos. Cada achado nomeado exige,
adicionalmente, uma revisão explícita do operador: \`operator_reviewed: true\`, \`operator\` e
\`operator_notes\` no registro de revisão vinculado por hash. Mesmo alterações de significado
avaliadas como pequenas não podem passar automaticamente. Respostas de verificação com
erros ou truncadas permanecem retidas. Os `reviews-<batch-id>.json` gerados são entradas para
`worldset.py apply`; a verificação linguística não escreve destinos. Um veredito automático
não substitui a aceitação final específica do projeto.

`retry-plan` permite uma execução de correção. Para `max_tokens`, seu limite de
saída é elevado de forma direcionada para pelo menos 64.000; após um limite já esgotado de
128.000, é necessário dividir o trabalho. A liberação dos custos da API e a proibição de
recarga automática de saldo continuam válidas. Dados brutos e contratos de proteção congelados
de batches concluídos devem ser preservados. Novas regras de parser não podem substituir
retroativamente atribuições de marcadores antigas. Em URLs nuas sem delimitador para o texto
seguinte, o limite pode ser ambíguo; esses casos permanecem retidos para verificação de formato.
Links Markdown explícitos ou delimitadores eliminam essa ambiguidade.

## Correções semânticas direcionadas

`scripts/worldset_repair.py` trabalha com candidatos completos que passam nas verificações mecânicas,
mas cuja verificação linguística ou revisão do operador encontrou erros concretos. A entrada
contém o batch original e seu ID, a fonte completa e a versão candidata, seus hashes, o modelo
de tradução efetivamente observado, o registro de revisão independente completo e os
`repair_feedback` concretos. Para fontes separadas, prepare cada estoque com seu próprio
`--repository-root`.

```bash
python scripts/worldset_repair.py --repository-root repo prepare --cases repair-cases.json --out repair-plan.json
python scripts/worldset_repair.py --repository-root repo submit --projection repair-plan.json --receipt repair-batch.json
python scripts/worldset_repair.py --repository-root repo collect --receipt repair-batch.json --out repair-staging
```

A tarefa de reparo vincula fonte, candidato, revisão completa e feedback a um novo ID. Antes
da chamada à API, a fonte atual e o destino ainda ausente devem coincidir. O batch nativo
permanece como único handle de execução; um receipt reservado após um envio com resultado
incerto não pode ser reenviado. A chave de API permanece no host executor. Com hosts diferentes,
use uma cópia da fonte armazenada separadamente e verificada por hash como raiz de entrada; ela
não substitui a nova verificação da fonte real no momento do apply.

O Haiku entrega no máximo 16 substituições únicas e não sobrepostas. Código, links, idioma e
proveniência permanecem protegidos; apenas o timestamp no frontmatter é ajustado pelo collector.
Após a última alteração, as verificações mecânicas completas são executadas novamente. Versões
de destino existentes e candidatos de README sem frontmatter YAML estão excluídos deste caminho
de reparo; esse limite já é verificado antes do envio.

O resultado permanece em `review_required`. Depois, com `worldset_review.py`, deve ser feita
uma nova verificação linguística independente e completa, resolvendo também todos os achados.
A revisão anterior não é uma liberação do candidato reparado. Só então vale o contrato de apply
existente, com nova varredura de locks, verificação do hash da fonte e criação atômica.

## Skills relacionadas

- `rotation-check` — estrutura para a execução periódica sobre um conjunto de documentos.
- `workflow-extract` — se esta verificação deve ser configurada como automação permanente.

## Changelog

### 1.5.1 (2026-10-15)
- Processar metadados de thinking regulares ao lado do texto JSON de reparo; recusar blocos
  de ferramenta, tipos de resposta desconhecidos e respostas sem texto JSON.
- Regressão protegida com respostas reais armazenadas do provedor e seleção unívoca de módulo
  no processo de teste.

### 1.5.0 (2026-10-15)
- Correções semânticas limitadas adicionadas, com vínculo completo à fonte, ao candidato, à
  revisão e ao feedback, receipts nativos e nova verificação linguística independente; as
  verificações explícitas continuam ativas também sob Python otimizado.

### 1.4.0 (2026-10-15)
- Idiomas de origem declarados ou explícitos, bibliotecas planas e pastas de idioma antigas
  já existentes foram considerados na varredura, inclusive versões alemãs de fontes em inglês.

### 1.3.1 (2026-10-15)
- Verificação linguística de API separada, vinculada por hash, adicionada; spans de código
  protegidos com base no parser CommonMark, atribuição de URLs e parágrafos verificada e
  execuções de correção limitadas possibilitadas após o esgotamento do limite de saída.

### 1.3.0 (2026-10-15)
- Traduções em série autorizadas adicionadas, com projeções de entrada imutáveis, handles
  nativos de batch, áreas protegidas de código/links, proveniência por hash de fonte e
  candidatos de verificação separados.

### 1.2.2 (2026-09-26)
- `scripts/check_language_parity.py`: regra de prefixo para códigos lang-only: um código base (por exemplo
  `zh`) agora também cobre suas variantes regionais (`zh-cn`,
  `zh-tw`); o inverso não vale.
- A verificação fail-closed de um código lang-only agora compara com TODOS os arquivos README
  do diretório, não apenas com o subconjunto passado; uma chamada com apenas duas de seis
  versões, portanto, não gera mais alarme falso. Um código válido sem arquivo NESTA chamada
  agora gera apenas uma observação (sem saída 1); um código realmente desconhecido (erro de
  digitação como `cn` em vez de `zh`) continua com saída 1.

### 1.2.1 (2026-09-26)
- `scripts/check_language_parity.py`: um código lang-only que não corresponde a nenhuma das versões
  linguísticas passadas (por exemplo, o erro de digitação `cn` em vez de
  `zh`) agora é reportado de forma fail-closed como achado, em vez de dispensar
  silenciosamente o link.
- Nomes de arquivo com código de região agora são reconhecidos como idioma:
  `README_zh-CN.md` e `README_zh_CN.md` resultam ambos em `zh-cn`.

### 1.2.0 (2026-09-26)
- Passo 0 „Reconhecer conteúdo monolíngue" adicionado (T-20260926-967984806): a divergência
  pode ser conteúdo novo ainda não propagado, e não desatualização; três saídas (traduzir e
  incluir em todas / marcar como lang-only / escalar como conflito), nunca exclusão silenciosa.
  Nova marcação `<!-- lang-only: <code> -->` para conteúdo deliberadamente restrito a um público-alvo.
- `scripts/check_language_parity.py` + `scripts/test_check_language_parity.py` adicionados: encontra links que aparecem apenas em
  um subconjunto das versões linguísticas (links Markdown e HTML), respeita a marcação
  lang-only, filtra o ruído de badges shields.io e captura arquivos não UTF-8 com saída 2 em
  vez de traceback.

### 1.1.0 (2026-07-03)
- Auditoria de expansão adicionada (avaliar aptidão para i18n, preparação técnica, QA para
  versões criadas), integrada em vez de ser uma skill separada i18n-coverage-audit
  (decisão de deduplicação).

### 1.0.0 (2026-07-03)
- Versão inicial. Abstraída do Codex-Automation
  „research-paper-de-en-synchronisationscheck" e generalizada para quaisquer versões
  linguísticas paralelas mantidas em conjunto (artigos, READMEs, skills, textos de site).
