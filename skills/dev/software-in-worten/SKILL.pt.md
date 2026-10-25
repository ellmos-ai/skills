---
name: software-in-worten
version: 1.0.0
type: method
author: ellmos (aus einem Entwurfsgespräch von Lukas Geiger, 2026-08-02)
created: 2026-08-02
updated: 2026-08-23
description: "Traduz entre interface de utilizador e texto — em ambas as direções. A partir de uma interface descrita, obtém-se uma skill; a partir de uma skill, obtém-se uma interface. Usar quando se está a desenhar uma aplicação e o fluxo ainda não está claro, quando uma ferramenta existente deve ser disponibilizada como skill, quando a interface e o acesso do agente divergem, ou quando uma skill fica demasiado longa e ninguém sabe porquê."
category: dev
tags: [design, ui, skills, methodik, uebersetzung, entwurf]
language: pt
status: stable
visibility: public
standalone: true
translated_from_sha256: e9250c36688fcdb950c1914daefd7ecfaf80e7ed56db0d4d287d2db69d3b9c63
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T12:49:12.834436+00:00"
---
<img src="banner.png" width="100%" alt="software-in-worten banner">

# Software em palavras

## A ideia

As pessoas desenham **visualmente**: *Como quero operar isto?* Os agentes leem **texto**.
Enquanto ambos surgem separadamente, divergem — a interface pode fazer algo que a skill
não conhece, e vice-versa.

Mas ambos são o mesmo, apenas em estados de agregação diferentes. Existe uma
tradução, e quem a conhece trabalha nas duas direções:

> **Desenhar uma interface a partir de palavras. E trazer uma interface de volta para palavras.**

---

## A tabela de tradução

| Na interface | O que significa | Em texto |
|---|---|---|
| **Cursor do rato** | *posso escolher* — o espaço do possível | o conjunto de opções nesse ponto |
| **Marcar** | *quero isto* | uma seleção, um valor |
| **Clique** | *decido-me, quero ir para lá* | **o prompt** — a resposta do utilizador |
| **Campo, interruptor, definição** | uma decisão que permanece | **Config** |
| **Definições de todo o software** | decisões válidas em todo o lado | **Policies** |
| **Formulário, máscara de entrada** | um conjunto de decisões relacionadas | **Template** |
| **Botão que inicia algo** | *agora acontece algo* | uma **Skill** ou **Workflow** é acionada |
| **O que decorre a seguir** | a sequência de passos | instruções na skill — ou um **script** |
| **Indicador de progresso** | *está a decorrer, e até onde* | mensagens de estado no fluxo |
| **Mensagem de sucesso, vista de resultados** | *isto resultou* | a devolução — na interface apenas apresentada de forma mais agradável |
| **Projeto** | um estado de trabalho delimitado | uma **pasta** — e, por estar ela própria numa pasta, parte do software |
| **Vista, separador, área** | um estado em que se está neste momento | um passo na árvore de fluxo |

**A linha central é o clique.** Um clique é apenas aquilo que um utilizador diria numa
conversa — só que mais depressa. **O clique é o prompt.** E a um prompt segue-se uma
reação: uma nova pergunta, uma nova vista, um novo estado.

---

## O fluxo é uma árvore

Cada aplicação é uma sequência de decisões, entre as quais algo acontece:

```
Voraussetzungen geklärt?   →  Referenzen · Kandidatenliste · Nummern · Reihenfolge
        ↓
Einverständnis des Nutzers →  START
        ↓
Will er mitlesen?          →  ja: Mitleseansicht öffnen
Will er Zwischenmeldungen? →  ja: bei jedem Ereignis melden (durch, abgelehnt, Status)
        ↓
        [ AUSFÜHRUNG — oft ausgelagert an andere Software ]
        ↓
Rückgabe kommt zurück      →  auswerten
        ↓
Was will er wissen?        →  das Ergebnis in seinen Begriffen:
                              „bestellt bei X, 40 Minuten, 30 Euro"
```

**Três partes, sempre as mesmas:**

1. **Decisões** — se-então, até estar reunido tudo o que é necessário
2. **Execução** — frequentemente nem sequer na própria ferramenta, mas externalizada
3. **Retorno** — o resultado de volta ao ser humano, na sua linguagem

A terceira parte é a mais subestimada no desenho. **A comunicação passa pelos sentidos** —
como texto, como imagem, como som. Uma interface molda isso; uma skill descreve *o que*
é comunicado e *quando*.

---

## O nível intermédio: o blueprint

Entre "descrito" e "construído" falta um degrau. Chama-se **blueprint** e é
**texto cuja disposição corresponde à imagem** — um ecrã que se pode ler:

```
 Worauf hast du Hunger?   [ Burger                        ]
 Wohin liefern?           [ Dorfstraße 1, 16321 Bernau    ]
 Höchstbetrag             [ 35 ] €   ⓘ Endbetrag an der Haustür
 Modus                    (•) Lieferung  ( ) Tisch  ( ) Abholung

 Kandidaten (ziehen zum Umsortieren)            ↻ neu suchen
 ┌────────────────────────────────────────────────────┐
 │ ≡ 1  Burger House Dorfstadt      ★ Favorit   offen │
 │ ≡ 2  Pizzeria Roma                            offen │
 └────────────────────────────────────────────────────┘

 [ Trockenlauf ansehen ]   [ Wirklich anrufen → 4 Anrufe, ~0,20 € ]
```

**Porque é que este degrau traz tanto:**

Um blueprint é **simultaneamente legível e visível**. A pessoa reencontra a sua imagem, o
agente vê campos, tipos e ordem. Surge em minutos, não custa nada e pode ser corrigido na
conversa — ao contrário de uma interface construída.

**E a partir do blueprint, a skill sai quase por si:**

> **O que deve o agente poder fazer, saber e executar — e em que ordem —
> para preencher este blueprint?**

Cada campo torna-se uma pergunta. A disposição torna-se a ordem. O que já vem preenchido
não é perguntado. O que aparece como botão torna-se um passo. Depois acrescenta-se o que o
agente ainda precisa de saber — conhecimento de domínio, limites, armadilhas.

**Três degraus, portanto:** descrição → **blueprint** → skill *(e daí igualmente bem para
uma interface construída)*.

### Um campo vazio é uma pergunta — e a pergunta tem um propósito

`[ 35 ] €` parece um número. Mas é um **pedido de dados a uma pessoa**, e tem uma
razão que quase nunca é dita:

> **Precisamos deste valor máximo porque é a condição sob a qual se encomenda de todo.**

O campo carrega, portanto, três coisas ao mesmo tempo: **o que** deve lá entrar, **porque**
é necessário, e **onde** atua mais tarde. Numa interface isso está no layout e no texto de
ajuda. No texto tem de ser escrito — caso contrário perde-se.

**Por isso, sob cada blueprint deve existir uma legenda de campos:**

| | |
|---|---|
| **Pergunta** | como uma pessoa seria questionada |
| **Tipo** | número, texto, seleção, lista, lista ordenada, data … |
| **Finalidade** | para que o valor será usado depois — *"critério de paragem na cascata"* |
| **Pré-condição** | o que tem de existir para que o campo faça sentido |
| **Pós-condição** | o que vale depois de ser preenchido |
| **Se vazio** | aceitar em silêncio · definir predefinição · perguntar de novo · bloquear |
| **Se errado** | mensagem, pergunta de retorno, sugestão de correção |

**As duas últimas linhas são as que mais facilmente se esquecem** — e as que mais
problemas causam em funcionamento. *"Preço indiferente"* é uma resposta válida e deve estar
prevista como tal, não como erro.

### O campo é aberto — a pergunta restringe

Um campo vazio é **tudo e nada**, como uma janela de contexto vazia: um convite a escrever
seja o que for. Mas o quê?

**A restrição não vem do campo, mas daquilo que o rodeia** — normalmente do texto ligado
antes, acima ou ao lado:

> *"Qual é o máximo que pode custar?"*

Esta pergunta restringe **semântica e pragmaticamente**. O próprio campo continua a admitir
tudo — e se alguém usar essa liberdade, **perde o seu propósito**. Por isso entram as
condições do campo: *apenas números*. Não porque "trinta e cinco" fosse incompreensível,
mas porque é mais difícil de processar e demora mais a escrever.

**Daqui resulta a direção de trabalho: a partir da pergunta derivam-se as regras do campo,
não o inverso.** Quem define primeiro o tipo de dados já se esqueceu da pergunta.

E a pergunta costuma também transportar a **finalidade** — por isso, nas pessoas, aparece
muitas vezes um ícone de informação ao lado:

> *"Não aceitamos uma oferta acima deste preço."*

Isto não é cortesia, mas o significado real do campo: **uma preferência do utilizador que
mais tarde atua como uma barreira rígida.**

### A fronteira de controlo — e porque tudo tem de ser transmitido

De um campo decorre uma cadeia:

```
Feld „Höchstbetrag"
   → der Wert wird später gebraucht        (Zweck)
   → für eine Prüfung                       (Gate)
   → also muss der Gegenwert erhoben werden (neue Frage, an anderer Stelle)
   → diese Frage stellt niemand von uns     (sie steht im Prompt)
```

**É aqui que passa a linha decisiva: com o prompt, sai da nossa camada de controlo.** Depois
já não há acesso — nem insistência, nem intervenção, nem segunda oportunidade.

Por isso **tudo** o que do outro lado for necessário tem de ser transmitido:

- **o próprio valor** — 35 €
- **a instrução para obter a contrapartida** — perguntar pelo preço
- **o que vale se for superior** — recusar, agradecer, terminar com cortesia
- **o que vale se não for indicado nenhum** — não estimar, recusar
- **o que vale se o interlocutor não quiser falar com uma máquina** — pedir um telefonema
  pessoal de retorno e devolver o número como valor

O último ponto mostra a direção em que menos se pensa ao desenhar: **também o caso excecional
tem de devolver um valor**, caso contrário não chega nada à pessoa além de "não resultou".

### O prompt é uma skill gerada

Com isto fica claro o que é, de facto, um prompt:

> **Um prompt é uma skill que a interface acabou de montar** — a partir das decisões, cliques
> e valores desta única execução. Personalizada, adaptada à finalidade, e obrigada a
> exprimir tudo o que se pretende **em linguagem**.

Uma skill escrita de forma fixa diz como se faz *sempre*. Um prompt diz como deve correr
*desta vez*. Ambos têm a mesma forma — um permanece, o outro surge no momento e depois desaparece.

**Na prática:** quem trata a construção do prompt como montagem de blocos de texto constrói
prompts fracos. Quem a trata como *geração de skills* — com finalidade, regras, limites,
exceções e valores de retorno — constrói bons.

### Esperar não é não fazer nada, é não saber

Depois do envio, a pessoa entregou o controlo. O que precisa agora não é paciência, mas
**informação**: *o que está a acontecer neste momento? Onde estamos?*

O agente recebe isso de qualquer forma — pergunta pelo progresso. **A pessoa não vê nada
disso enquanto ninguém o traduzir.** Para isso existem as barras de progresso, os registos
em curso e as linhas de estado: não são enfeites, mas a tradução de um fluxo de dados em
algo que quem espera consegue suportar.

### O retorno é um prompt de volta

A mensagem de sucesso não é um fecho, mas uma **entrega de volta**:

> *"Este é o resultado do teu pedido."*

Só assim a pessoa pode avaliar e agir. E é precisamente por isso que tem de ser completa:
*"Encomendado — mas três pizzas em vez de uma. Ainda bem que o número de retorno está aí,
ligo eu próprio."*

**Sem um retorno utilizável, ninguém consegue continuar o processamento.** Uma mensagem que
diz apenas "resultou" não fecha o ciclo.

### Análise de perguntas e campos

Para **cada** elemento de um blueprint — campo, botão, seleção, apresentação — as mesmas
perguntas:

| | |
|---|---|
| **O que se pretende, e para quê?** | a intenção por trás do elemento |
| **O que acontece ao enviar?** | processado de imediato, ou apenas guardado? |
| **Onde e quando é o valor voltado a necessitar?** | o ponto onde atua |
| **Durante quanto tempo tem de ser mantido?** | para além do clique? para além da execução? |
| **O que deve acontecer-lhe?** | verificar, transmitir, apresentar, descartar |

O valor máximo, por exemplo, **não** é necessário de imediato. É guardado, transportado e
só atua na conversa — por isso é preciso um sítio onde fique e um ponto em que passe para o prompt.

### As bifurcações determinam o algoritmo de perguntas

Uma seleção raramente é apenas um valor. Muitas vezes é um **interruptor** que reorganiza
todo o resto do fluxo:

| Modo | Primeira pergunta na conversa | O que desaparece | O que surge |
|---|---|---|---|
| **Entrega** | *"Entregam aqui?"* — um não termina logo a chamada | — | Morada de entrega |
| **Recolha** | desaparece | a pergunta da entrega | Hora de recolha |
| **Mesa** | *"Têm aberto, e há mesa livre às X?"* | toda a verificação de preço | Número de pessoas, crianças, pedido de lugar, período |

**A ordem na conversa segue a força de exclusão, não a curiosidade.** Quem não entrega não
precisa de ser questionado sobre a comida — a condição mais dura vem primeiro, porque leva
mais rapidamente ao candidato seguinte.

E: **muita coisa permanece igual através dos interruptores.** O valor máximo vale para
entrega e para recolha, e a lista de candidatos também. Só o algoritmo de perguntas muda.

### O círculo

```
Problem  →  Use Case  →  Wille        „Ich bin auf dem Land und habe Hunger"
   ↓
was ich will, wird zu Bedingungen     5 Personen · 19 Uhr · Italiener · nicht der eine
   ↓
Bedingungen brauchen Daten            → daraus ergeben sich die FELDER
   ↓
Felder + Entscheidungen               → daraus wird der PROMPT (der erzeugte Skill)
   ↓
                [ Ausführung jenseits der Kontrollgrenze ]
   ↓
Rückgabe empfangen und speichern      → nur, was vorher mitgegeben wurde, kommt zurück
   ↓
übersetzen in Sicht- und Hörbares     → MELDUNG an den Menschen
   ↓
er bewertet und entscheidet neu       → zurück nach oben
```

**O caso de uso fundamenta os dados, e os dados fundamentam os campos.** Quem começa pelos
campos inventa formulários. Quem começa pela intenção recebe-os de graça.

### Entre dois blueprints está a causalidade

Um blueprint é um **arranjo estático**. Vários em sequência ainda não formam um fluxo —
entre eles acontece algo, e **esse entre é a verdadeira lógica**: o que sucede quando aqui
se clica? Que verificação corre? O que é guardado? O que é desencadeado?

Três formas de tornar visível esse plano temporal:

1. **Anotação na imagem** — setas e pequenas notas entre os blueprints
2. **Pares antes/depois** — o mesmo excerto em dois estados, "antes do clique" e "depois do clique"
3. **Escrita** — pré e pós-condições como texto sob a imagem

A terceira forma é a que mais longe chega, porque é executável. As duas primeiras ajudam a
pessoa a compreender.

### Do campo deriva o modelo de dados

Quem descreve um campo "adicionar contacto" já decidiu que existem destinatários, que serão
guardados e quais os dados que lhes pertencem. **A tabela de dados segue os campos, não o inverso.**

Por isso compensa tornar a legenda de campos completa antes de desenhar qualquer esquema:
cada campo com tipo e finalidade é uma coluna, cada grupo repetível é uma tabela, cada
relação entre campos é uma referência.

## Direção 1: Das palavras para a interface

**Quando primeiro se descreveu o fluxo.**

1. **Recolher decisões.** Cada ponto em que algo fica definido. Ordenar:
   - **Obrigatória** — sem isto não se avança → **campo obrigatório**
   - **Deduzível** — pode vir do contexto ou do existente → **campo pré-preenchido** com
     possibilidade de correção
   - **Opcional** — melhora o resultado → **secção recolhida**
   - **Barreira** — irreversível, custa dinheiro, chega a pessoas → **passo de confirmação**
2. **Agrupar o que pertence em conjunto** → uma máscara, um template.
3. **Cortar a árvore em vistas.** Um estado = uma vista.
4. **Desenhar os retornos.** O que é comunicado e quando? Progresso, estado intermédio,
   resultado.
5. **Fixar uma vez o que vale em todo o lado** — cor, tipografia, disposição, movimento.
   São as policies da interface.

**O ganho:** um formulário que nasce de uma conversa é quase sempre mais enxuto do que um
desenhado na prancheta. Ao formular, percebe-se qual pergunta é supérflua.

## Direção 2: Da interface para as palavras

**Quando a aplicação já existe ou está descrita.**

1. **Formular cada clique como pergunta.** O que é que este botão, de facto, pergunta ao utilizador?
2. **Cada campo como entrada de Config** — com valor predefinido, tipo e texto de ajuda.
3. **Cada vista como passo** no fluxo.
4. **Cada mensagem como retorno** — o que é reportado, com que palavras?
5. **Verificar o que a interface sabe implicitamente** — ordens, bloqueios, dependências que
   não estão escritos em lado nenhum, apenas no layout. **É a parte que mais facilmente se perde
   ao traduzir.**

### Porque é esta direção mais difícil — e como a percorrer na mesma

A direção 1 é fácil, a direção 2 parece pesada. Há uma razão:

> **Uma skill é tempo. Um ecrã é superfície.**
> Primeiro isto, depois aquilo — contra tudo visível ao mesmo tempo.

Não se traduz, portanto, linha a linha, mas **corta-se um fluxo em superfícies**. A aresta de
corte é sempre a mesma:

**Um ecrã surge onde o fluxo espera por uma pessoa.**

Tudo o que se passa entre dois pontos de espera corre por si — isso **não** se torna ecrã,
quando muito uma indicação de progresso. Quem constrói uma vista para cada passo constrói
uma prisão de cliques.

**E as cadeias se-então?** Nem todas se tornam visíveis. Quatro casos:

| Tipo de condição | O que dela resulta |
|---|---|
| **A pessoa a define** ("no máximo 35 €") | um **campo** — antes do início |
| **O sistema a verifica** ("preço acima do limite") | um **resultado** — depois, com justificação |
| **Altera o que a pessoa vê** ("sem resultados") | um **estado** do mesmo ecrã, não um novo |
| **É pura mecânica** (repetições, tempos limite, verificação de formato) | **nada** — permanece invisível |

**O quarto caso é o mais frequente.** A maioria das ramificações de um script nunca pertence
a um ecrã. Quem as mostra assim mesmo confunde diagrama de fluxo com interface.

**Na prática, em quatro passos:**

1. **Marcar os pontos de espera** — cada sítio onde uma pessoa decide, confirma ou introduz algo.
   São os ecrãs, e costumam ser surpreendentemente poucos.
2. **Recolher para trás** — o que tem de ser conhecido antes deste ponto de espera? Esses
   valores são os campos do ecrã.
3. **Recolher para a frente** — o que acontece depois, e o que dali a pessoa deve saber?
   Isso é o retorno.
4. **Deixar o resto de fora** — tudo o que não é entrada nem comunicação fica invisível.

---

## O gradiente: skill ↔ script

```
weit von der Software                                    nah an der Software
   Skill trägt alles                                    Skript trägt alles
        │                                                       │
   ausführlicher Text          ────────────►         knappe Bedienungsanleitung
   jeder Schritt erklärt                             „ruf dies auf, dann jenes"
   funktioniert ohne Werkzeug                        funktioniert nur mit Werkzeug
```

**Quanto mais automatizado está um processo, menos a skill tem de explicar.** Torna-se mais
curta e concreta — a certa altura é pouco mais do que uma instrução de uso para os scripts:
*quando usar esta ferramenta, o que se lhe dá, como se reconhece que resultou.*

Duas conclusões inversas que ajudam no dia a dia:

- **Se uma skill fica demasiado longa, falta um script.** O comprimento é um sinal: o que se
  repete e é mecânico deve ser automatizado.
- **Se um script se torna incompreensível, falta uma skill.** Uma ferramenta sem texto por
  cima só é utilizável por quem a construiu.

---

## A moeda comum

**Cada definição existe em triplicado** — como valor de Config, como pergunta na skill, como
campo na interface. Para que não divirjam, a representação é descrita **uma única vez** e
lida pelos três:

```yaml
field: sample.method
label: "Ziehungsverfahren"                       # Oberfläche
question: "Wie soll gezogen werden — zufällig, geschichtet oder alle?"   # Skill
type: choice
options: [random, stratified, census]
default: random
help: "Geschichtet nur, wenn die Merkmale in der Grundlage stehen."
locked: false        # true = nicht abschaltbar, erscheint in keiner Oberfläche
```

**O que é `locked` não aparece em lado nenhum como opção.** Algumas coisas não são
definições, mas parte da estrutura.

---

## Quando é útil esta skill

- Uma aplicação está a ser desenhada e o fluxo ainda não está claro → **direção 1**
- Uma ferramenta existente deve tornar-se utilizável por agentes → **direção 2**
- A interface e o acesso do agente divergem → introduzir a **moeda comum**
- Uma skill fica demasiado longa e ninguém sabe porquê → verificar o **gradiente**
- Uma conversa de desenho deve ser registada antes de se perder → tabela + árvore

## Relacionado

`condition` traduz condições, momentos e sequências em barreiras verificáveis
(`/if`, `/when`, `/after`, `/and`, `/or`) — o mesmo movimento para o caso especial do controlo de fluxo.
`skill-extractor` extrai skills a partir de históricos de conversas. `plugin-system` torna
os scripts próprios descobríveis.
