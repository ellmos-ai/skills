---
name: piggyback-hosting
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-02
updated: 2026-08-07
description: "Padrão de hospedagem para tornar seguro o hosting de uma aplicação construída localmente (banco de dados próprio, chave de API própria, estado em processo) sem construir gestão de usuários. Traço central — o host não armazena nada, o navegador do visitante armazena tudo — de modo que contas por visitante, verificações de acesso e prazos de exclusão deixam de ser necessários, em vez de precisarem ser resolvidos. Use quando uma aplicação construída localmente deve ser hospedada para vários visitantes, em casos como \"torne isso hospedável sem login\", \"não construir contas de usuário\", \"reduzir a política de privacidade de uma ferramenta hospedada\", \"quem é responsável se não armazenamos nada\" ou ao escolher/implementar um modo servidor (`local`, `huckepack-gift`, `huckepack-only-host`, `pay-membership`). Fornece um modelo de plano de fluxo de dados, um modelo de política de privacidade e uma avaliação jurídica preliminar (RGPD/TDDDG/UWG, em alemão) como referências."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [hosting, privacy, gdpr, dsgvo, byok, client-side-storage, deployment, no-login]
language: pt
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
translated_from_sha256: e4e1a66b0d6e62ff17a5a883b8eef0ca1f59b984e64d8d29030b76b4ffbcebda
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.766825+00:00"
---
<img src="banner.png" width="100%" alt="piggyback-hosting banner">

# piggyback-hosting

**Um padrão de hospedagem para aplicações que, desde o início, nunca aceitam
dados de terceiros.**

> Blueprint criado em 2026-08-02 durante a construção de três agentes de chamada.
> Reutilizável para qualquer aplicação projetada para um único usuário local,
> mas que também deva ser hospedável para outros.

## Sobre o nome

Em inglês, este padrão chama-se **piggyback** — "ir de carona" na infraestrutura
alheia já é o termo técnico corrente. O texto corrido em inglês deste skill usa,
portanto, *piggyback*; **"huckepack" é o título de trabalho em alemão** sob o qual
o padrão foi construído e, ao mesmo tempo, o nome do repositório do qual este
skill foi migrado. **Os valores literais de modo permanecem `huckepack-gift` e `huckepack-only-host`**
— são o que é enviado em código e configuração, escritos exatamente assim,
independentemente do idioma do texto que os envolve.

## O problema

Uma aplicação é construída localmente: um banco de dados, uma chave de API, estado
que vive no processo. Na própria máquina, isso está simplesmente correto. Assim que
alguém a hospeda para outras pessoas, cada uma dessas três premissas se torna um
bug — todo visitante compartilha o mesmo estado, o mesmo banco de dados, a mesma
chave. Quem abre a página vê os dados de todos os outros.

A solução habitual é a gestão de usuários: contas, login, verificações de acesso,
prazos de exclusão, uma política de privacidade, um contrato de tratamento de dados.
Muitas vezes, um empreendimento maior do que a própria aplicação.

## A ideia

**O visitante mantém tudo no próprio dispositivo. O host não mantém nada.**

Isso não resolve a gestão de usuários — ela se torna **irrelevante**. Onde não há
dados de terceiros no servidor, não há nada a separar entre visitantes, nada a
excluir conforme um cronograma, e a política de privacidade se reduz ao que o
serviço efetivamente faz.

## Os três modos

| Modo | Chave de API | Dados | Gestão de usuários |
|---|---|---|---|
| **`huckepack-gift`** | do host | no dispositivo do visitante | nenhuma |
| **`huckepack-only-host`** | do visitante | no dispositivo do visitante | nenhuma |
| **`pay-membership`** | do host, cobrada | servidor | necessária |

- **`huckepack-gift`** — o host fornece a própria chave e oferece a execução
  de graça. Um convite sem atrito para experimentar a ferramenta.
- **`huckepack-only-host`** — o visitante traz a própria chave. O host não paga nada
  e não armazena nada.
- **`pay-membership`** — deliberadamente mantido como stub. Aqui volta a ser
  necessário tudo o que os outros dois evitam — contas, cobrança, armazenamento no
  servidor. Um empreendimento próprio, não um interruptor a ser acionado.

Há sempre um padrão **`local`**: quem não configura nada recebe a
aplicação exatamente como funcionava antes, na própria máquina.

## Os blocos de construção

| Bloco | Finalidade |
|---|---|
| Modo como configuração no momento da instalação | uma propriedade do deployment, não da sessão |
| Camada de armazenamento intercambiável | o mesmo banco de dados, em outro lugar |
| SQLite no navegador (WASM + OPFS) | o mesmo esquema, as mesmas consultas, outro local de execução |
| Campo de chave, mascarado | apenas no modo `only-host`, nunca registrado em log |
| Exportação e importação | **não opcionais** — os dados do navegador são voláteis |
| Comprovante como arquivo para download, pasta de destino escolhível | nenhum servidor envolvido na entrega |

O esforço de engenharia real está em tornar a camada de armazenamento
intercambiável: a aplicação grava em SQLite de qualquer forma, mas uma camada
intermediária decide se essa gravação acaba no servidor ou no navegador do visitante
(`sql.js` / a build oficial do SQLite-WASM, persistida por meio do Origin
Private File System). Se o WASM for pesado demais, ordenar as opções de
armazenamento no navegador por peso: SQLite-WASM + OPFS (um banco de dados real,
maior capacidade) > IndexedDB (estruturado, modelo de consulta próprio) >
`localStorage` (adequado apenas para itens pequenos, como idioma e tema).

## O que este padrão não resolve — com franqueza

- **Dados do navegador apagados significa que tudo se perde.** Não existe cópia no
  servidor. Por isso a exportação é uma condição, não um complemento desejável.
- **Não há troca de dispositivo** sem exportação e importação.
- **A chave que vive no navegador** (`only-host`) é menos protegida do que
  uma em servidor. Mas pertence ao visitante, e a alternativa seria entregá-la ao
  host — não é, de forma evidente, a escolha mais segura.
- **A execução continua passando pelo host.** Em serviços que alcançam um terceiro —
  por exemplo, uma ligação telefônica — o host processa os dados desse terceiro,
  independentemente de onde estejam os registros próprios do visitante. Isso não
  torna a política de privacidade supérflua, apenas a torna mais curta.

## O que a verificação jurídica constatou

Uma avaliação jurídica preliminar (`references/RECHT.md`, em alemão — ela examina
normas alemãs e da UE, por isso citá-la em tradução seria menos preciso, não mais
acessível) verificou o padrão contra o RGPD, a TDDDG e a UWG. **Avaliação preliminar
com referências, não aconselhamento jurídico.** Três achados, uma linha cada:

- **O host continua sendo controlador, mesmo que não armazene nada.** O art. 4(7)
  do RGPD vincula a responsabilidade à decisão sobre finalidades e meios, não ao
  armazenamento; o TJUE afirmou isso expressamente (C-683/21). O que se torna
  irrelevante é a **gestão de usuários**, não a responsabilidade.
- **Para a pessoa contatada, nada diminui.** Deveres de informação segundo o art. 14,
  uma ponderação documentada da base legal, um contrato de tratamento de dados com o
  serviço que executa o contato — normalmente, são as seções mais longas de uma
  política de privacidade, e o padrão não as toca.
- **A exceção doméstica ajuda o visitante, não o host.** Ela cobre o uso puramente
  pessoal por uma pessoa natural; um serviço oferecido a outros não é uma atividade
  puramente pessoal. É exatamente aí que começa a hospedagem piggyback.

O ganho está na **extensão das obrigações e no tamanho da superfície de ataque**,
não na sua natureza — o que, ao mesmo tempo, é a afirmação mais honesta sobre o padrão.

## Como aplicar este padrão

1. Ler `references/DATA-FLOW-TEMPLATE.md` e preenchê-lo para a aplicação real, com base em evidências
   (cada linha precisa de um `file:line` ou de "não encontrado"). Isso expõe
   com precisão quais premissas locais se quebram sob hospedagem multiusuário, antes
   de qualquer alteração de código.
2. Decidir quais modos a aplicação realmente precisa — `local` é sempre o
   padrão; `huckepack-gift` e `huckepack-only-host` são os dois que evitam a gestão
   de usuários; `pay-membership` permanece um stub enquanto não houver um motivo
   concreto para contas reais.
3. Tornar a camada de armazenamento intercambiável (o passo central acima), acrescentar
   o campo de chave mascarado para `only-host` e conectar exportação/importação
   antes de entregar qualquer coisa — essa é a rede de segurança para o armazenamento
   volátil do navegador.
4. Preencher `references/PRIVACY-TEMPLATE.md` para o deployment concreto; excluir os blocos que não
   se aplicam, verificar cada indicação de fornecedor contra os contratos atuais e
   obter uma verificação jurídica específica do caso antes de processar dados reais.
   O modelo é um ponto de partida, não uma declaração pronta.
5. Em qualquer instalação que envolva terceiros reais (ligações telefônicas, mensagens
   a pessoas que não se inscreveram por conta própria) ou participantes de pesquisa,
   tratar as recomendações de `references/RECHT.md` como lista de verificação, não como
   liberação — envolver um advogado antes da primeira execução pública.

## Referências

- `references/DATA-FLOW-TEMPLATE.md` — modelo e procedimento para um plano de fluxo de dados: cada
  linha precisa de um arquivo:linha, senão é uma suposição, não um achado.
- `references/PRIVACY-TEMPLATE.md` — política de privacidade modelo com marcadores de substituição
  para uma instalação piggyback.
- `references/RECHT.md` — avaliação jurídica preliminar (em alemão), com referências ao
  RGPD, à TDDDG e à UWG.

Ambos os modelos são **modelos, não aconselhamento jurídico**. Quem hospeda uma
aplicação a adapta e é responsável pelo resultado.

## Origem

Surgido durante a construção de HungryCall, Ringedingeding e ResearchCall — três
agentes de chamada, nos quais uma auditoria de fluxo de dados mostrou que hospedá-los
sem alterações teria sido um incidente de privacidade com nome anexado. Migrado do
repositório independente `huckepack` para esta biblioteca de skills.
