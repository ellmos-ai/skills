---
name: full-after-care
version: 1.0.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-07-24
updated: 2026-07-24
aliases: [deep-after-care, repo-after-care-full, tiefe-repo-pflege, repo-tiefenpflege]
description: "Ciclo profundo de manutenção para um repositório GitHub publicado (nível 2): inclui a execução completa do surface-after-care e acrescenta três passos custosos — avaliação jurídica preliminar através dos Law-Checkers com nova verificação após um ano (o parecer permanece gitignored no repositório), referências cruzadas a repositórios relacionados em TODAS as organizações, bem como a atualização de todos os idiomas no nível da aplicação, e não apenas na documentação. Use esta skill com \"full after care\", \"deep after care\", \"manutenção profunda do repo\", \"ronda grande\", \"revisar o repo a fundo\", quando um repo não for verificado há muito tempo, antes de releases maiores ou quando a relevância jurídica, as referências cruzadas ou o multilinguismo forem explicitamente o tema. Para a ronda barata e frequentemente repetida, use surface-after-care; para a primeira publicação, github-repo-care."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: dev
tags: [github, repo, maintenance, legal, i18n, cross-linking, organization, documentation]
language: pt
status: active
visibility: public

dependencies:
  tools: [git, gh, rg]
  services: [GitHub]
  protocols: [surface-after-care]
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 8e67a4197360cd22357ce277ef3739471993d730d1781bf4746e3e28d727b394
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.160760+00:00"
---
<img src="banner.png" width="100%" alt="full-after-care banner">
# Full After Care — a ronda profunda (sinônimo: Deep After Care)

## Quando esta skill se aplica

Use-a quando um repo publicado deve ser revisto **a fundo**: não verificado há muito tempo, antes de um release maior, em caso de objetos juridicamente relevantes, ou quando a articulação com os demais projetos próprios está em pauta.

A diferença em relação à ronda barata está no esforço, não no cuidado: o nível 2 ultrapassa os limites do repo individual. Ele consulta fontes externas (situação jurídica), inventaria **todas** as organizações e intervém na própria aplicação (idiomas). Por isso, roda com menos frequência — tipicamente uma vez por repo e por ano, ou por ocasião.

## Procedimento

### Primeiro o nível 1 por completo

Execute **`surface-after-care` por completo** — inclusive o passo 0 (superfícies de distribuição), o gate de privacidade, a intenção de publicação, o banner, a comparação entre estado real e estado desejado, os idiomas do README, a visibilidade, a entrada na organização, issues e PRs, bem como commit, push e paridade das superfícies. Nada disso é repetido ou abreviado aqui.

Os três passos seguintes vêm por cima. Eles geram, por sua vez, alterações na documentação e no código — envie-as no mesmo ritmo descrito no nível 1, em commits separados por tema.

---

### 5. Avaliação jurídica preliminar com nova verificação anual

#### Primeiro: a avaliação chega a ser devida?

Consulte `_after-care/RECHTSCHECK.md` (a pasta é gitignored, veja abaixo). Se nela constar uma data de verificação que está **há menos de um ano**, este passo é **pulado** — também na ronda profunda. Obter novamente uma avaliação recente custa tempo e dinheiro e não traz nada de novo.

Se a data for **mais antiga que um ano** ou o arquivo não existir, faz-se a verificação. O motivo da nova verificação não é que o parecer tenha ficado pior, mas que a **situação jurídica** muda: novos regulamentos, limiares alterados, nova jurisprudência, regras de plataforma modificadas. Um parecer de dois anos pode estar formalmente correto e, na prática, superado.

Fora do ritmo anual, uma reavaliação é devida quando o **objeto** mudou: novas categorias de dados, novo canal de distribuição, novo modelo de negócio, troca de licença, nova dependência com copyleft, extensão para outro espaço jurídico.

#### O repo é juridicamente relevante?

Nem todo projeto precisa disso. Gatilhos incluem, entre outros:

- trata dados pessoais, mesmo que apenas localmente
- acessa serviços, sites ou interfaces de terceiros (termos de uso, scraping)
- fornece informações em campos regulados (direito, medicina, impostos, finanças)
- traz marcas, nomes ou logotipos de terceiros no nome, na documentação ou na UI
- contém dependências com copyleft ou licença pouco clara, ou fornece conteúdos de terceiros
- destina-se a menores, processa pagamentos ou se enquadra em regras de exportação/cripto
- toma decisões automatizadas sobre pessoas ou é classificado como sistema de IA

Se nada disso se aplicar, registre no protocolo de execução que **foi verificado e negado** — caso contrário, a próxima ronda fará a mesma pergunta do zero.

#### Obter a avaliação

Use os Law-Checkers (skill `law-checker`, módulo `law-checker`) e apresente-lhes o caso concreto: o que a aplicação faz, quais dados toca, por quais canais é distribuída, quais licenças a acompanham, a quem se destina. Quanto mais concreto o caso, mais úteis as referências encontradas. O resultado é uma avaliação preliminar com indicações de artigos — **não é aconselhamento jurídico**; havendo risco sério, o resultado é a recomendação de submeter o caso a um advogado, não o veredicto em si.

#### Arquivamento

```
_after-care/
├── LOG.md                    # Laufprotokoll beider Stufen
└── RECHTSCHECK.md            # Datum, Gegenstand, Ergebnis, Auflagen, Wiedervorlage
```

`_after-care/` pertence a `.gitignore`. Isso não é ocultação, mas a mesma regra do passo 2b do nível 1: documentos de trabalho internos não são conteúdo do repo. No caso de um parecer, soma-se que uma análise de risco publicada junto ao código pode ser lida como uma confissão e fornece aos atacantes um mapa. Alternativamente, o arquivamento pode ocorrer fora do repo, em uma pasta própria — o importante é que seja **encontrável** na próxima execução, senão a regra anual não funciona.

Cabeçalho do arquivo, mantido legível por máquina:

```markdown
# Rechtscheck — <Projekt>
geprüft: 2026-07-24
gegenstand: lokale Dateiverwaltung, keine Cloud, keine personenbezogenen Daten Dritter
ergebnis: unbedenklich
auflagen: Hinweis auf MIT-Lizenz der eingebetteten Bibliothek X im README
wiedervorlage: 2027-07-24
```

Do parecer só se tornam **públicas** as **consequências**: uma indicação de licença, uma cláusula de exoneração, uma nota de privacidade, uma descrição mais precisa do que o app faz. Essas alterações pertencem ao repo — a justificativa por trás delas, não.

---

### 9. Referências cruzadas entre todas as organizações

O nível 1 pergunta apenas se o repo consta nas páginas das organizações. O nível 2 vai um degrau mais fundo: **quais repos individuais de todas as organizações próprias estão relacionados a este — e os dois lados sabem disso?**

```bash
gh api user/orgs --jq '.[].login'
for ORG in $(gh api user/orgs --jq '.[].login'); do
  gh repo list "$ORG" --limit 200 --json name,description,updatedAt,isArchived,primaryLanguage
done
```

O ganho não vem de listar, mas de reconhecer relações. Tipos relevantes:

- **usa / é usado por** — dependência técnica real nos dois sentidos
- **pertence à mesma família** — linha de produto comum, prefixo comum, arquitetura comum
- **resolve o mesmo problema de outra forma** — um usuário que chega a um quer muitas vezes conhecer o outro
- **predecessor / sucessor** — projetos substituídos precisam de um indicador, senão os usuários ficam permanentemente numa versão morta
- **componente / composição** — biblioteca e a aplicação que a utiliza

Defina as referências de forma **bidirecional**. Uma via de mão única é o erro mais comum deste passo: acrescenta-se no repo cuidado uma lista de projetos relacionados, e nos projetos relacionados não há nada. Quem chega lá nunca encontra o caminho de volta.

A referência de retorno é de fato definida no repo oposto — segundo a **regra de árvore suja** do passo 11 do nível 1, em resumo: árvore limpa → commit e push próprios; sujo em outros arquivos → commit restrito aos caminhos, sem push; sujo no arquivo-alvo ou bloqueio ativo → não tocar. Se a referência não for definida, ela pertence à lista de tarefas do repo-alvo (`AUFGABEN.txt`/`TODO.md`); em caso de bloqueio, apenas no protocolo próprio. Assim a ronda permanece fechada em si mesma, sem pôr em risco estados de trabalho alheios e sem que a referência se perca.

Formule as referências orientadas ao benefício, não como lista de nomes: "**projeto-b** — lê as exportações geradas por esta ferramenta e transforma-as em relatórios" é útil; "veja também: projeto-b" não.

Repos arquivados e evidentemente mortos não são linkados — exceto como indicação explícita de sucessor no outro sentido.

Este inventário é a parte mais cara da ronda. Quando há muitas organizações e repos a verificar, vale a pena registrar o resultado do inventário de repos no protocolo de execução, para que a próxima ronda profunda de outro repo possa partir dele.

---

### Atualizar todos os idiomas no nível da aplicação

O nível 1 cuida das versões em idioma do README. Aqui trata-se do **produto em si**: textos da interface, mensagens, ajudas, saídas de CLI, mensagens de erro, descrições em lojas e registries.

Primeiro identifique quais idiomas a aplicação já conhece tecnicamente e como os gerencia:

```bash
rg -l "gettext|i18n|locale|translations|LC_MESSAGES|\.po$|messages\.json" --hidden
fd -e po -e pot -e ftl . 2>/dev/null; ls locales/ i18n/ lang/ translations/ 2>/dev/null
```

Depois feche as lacunas, seguindo três perguntas:

1. **Faltam idiomas** que o projeto deveria ter? Idiomas padrão são alemão, inglês, espanhol, chinês simplificado, japonês, russo — em aplicações voltadas ao usuário. Em bibliotecas voltadas a desenvolvedores, apenas o inglês costuma ser a resposta certa; um idioma desnecessário é carga de manutenção permanente, não ganho.
2. **Os idiomas existentes estão completos?** Após cada ciclo de funcionalidades, os idiomas secundários ficam para trás. Chaves novas sem tradução costumam cair no idioma principal em tempo de execução e assim passam despercebidas — por isso compare de forma dirigida contra o idioma principal, em vez de confiar na impressão visual.
3. **A escolha de idioma é alcançável pelo usuário?** Uma tradução completa que ninguém consegue ativar parece inexistente. Há seletor, a escolha é persistida, o idioma do sistema é detectado como padrão?

Atenha-se ao mecanismo de i18n já estabelecido no projeto e não introduza um segundo ao lado. Verifique os resultados na **interface real**, não apenas no arquivo de recursos: strings longas quebram layouts, e suporte a conjuntos de caracteres só aparece na renderização (glifos CJK ausentes aparecem como caixas vazias).

Por fim, inclua as superfícies do passo 0 do nível 1: descrições de loja e de registry têm campos de idioma próprios, que não acompanham automaticamente a tradução do app.

## Protocolo de execução

Acrescente em `_after-care/LOG.md` uma entrada com o nível `full`:

```markdown
## 2026-07-24 — full
- Stufe 1 vollständig gelaufen (siehe Eintrag oben)
- Rechtscheck: fällig (letzter 2025-06-02) -> neu eingeholt, Ergebnis unbedenklich,
  Auflage Lizenzhinweis Bibliothek X umgesetzt, Wiedervorlage 2027-07-24
- Querverweise: 4 Orgas / 38 Repos geprüft, 3 Beziehungen gefunden,
  bidirektional gesetzt; Rückverweis in repo-y offen (dort aktiver Lock)
- Sprachen App-Ebene: ES ergänzt (312 Schlüssel), JA auf Stand gebracht,
  Umschalter war vorhanden aber nicht persistent -> gefixt
```

## Erros comuns

| Erro | Correção |
|---|---|
| Verificação jurídica refeita, embora a última tivesse 3 meses | Ler primeiro a data em `RECHTSCHECK.md` — com menos de um ano, pula-se |
| Verificação jurídica pulada por "nada mudou" | A situação jurídica muda independentemente do projeto; a partir de um ano, verifica-se |
| Parecer commitado no repo | `_after-care/` pertence a `.gitignore`; só as consequências se tornam públicas |
| Relevância jurídica negada sem documentação | Também um "não relevante" é um achado e pertence ao protocolo |
| Referências cruzadas definidas apenas no repo cuidado | Definir de forma bidirecional, senão é uma via de mão única |
| Verificada apenas a própria organização | O nível 2 significa todas as organizações — exatamente o que o distingue do nível 1 |
| Referências como simples lista de nomes | Explicar o benefício numa frase, senão ninguém clica |
| Novo idioma criado, mas inacessível na UI | Verificar seletor, persistência e detecção do idioma do sistema |
| Tradução verificada apenas no arquivo de recursos | Verificar na interface real — quebras de layout e glifos ausentes só aparecem ali |
| Campos de idioma de loja/registry esquecidos | Eles não acompanham a tradução do app |

## Checklist de encerramento

- [ ] `surface-after-care` percorrido por completo (incl. push e paridade das superfícies).
- [ ] Relevância jurídica verificada; resultado documentado — também quando negado.
- [ ] Verificação jurídica devida? Se sim: obtida, exigências implementadas, nova verificação agendada.
- [ ] `_after-care/` em `.gitignore`, parecer não versionado.
- [ ] Todas as organizações inventariadas, relações determinadas.
- [ ] Referências cruzadas definidas de forma bidirecional, commitadas e enviadas nos repos opostos.
- [ ] Repos opostos pulados por árvore suja ou bloqueio anotados como pontos em aberto.
- [ ] Idiomas do app completos, seletor acessível, verificados na interface.
- [ ] Campos de idioma de loja/registry atualizados.
- [ ] Entrada no protocolo de execução com o nível `full` registrada.

## Changelog

### 1.0.0 (2026-07-24)
- Versão inicial. Nível 2 da manutenção pós-publicação de repos, baseado em `surface-after-care`.
