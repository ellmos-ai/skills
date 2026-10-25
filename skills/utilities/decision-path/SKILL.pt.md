---
name: decision-path
version: 1.1.0
type: skill
author: Lukas Geiger + agy
created: 2026-09-13
updated: 2026-09-18
description: "Gera, a partir de um estoque de decisões em aberto e de decisões já tomadas, um grafo de dependências em ASCII estruturado (no máximo 100 colunas) para o terminal. Avalia os nós segundo cinco critérios fixos: sensato, recomendado, típico do usuário (direção e confiança do decision-avatar separadas), compatível e contraditório; as arestas trazem o tipo de relação e o status de comprovação. Expõe sem piedade bloqueios, liberações, sequências e recomendações contraditórias. Use esta skill em casos como “quais decisões dependem umas das outras”, “grafo de dependências das decisões”, “visualizar o caminho de decisão”, “verificar contradições entre decisões”, “ordem das decisões” ou /decision-path. NÃO use para inventariar decisões primeiro: isso faz o decision-briefing. NÃO use para reunir o conceito geral recomendado para aprovação: isso faz o decision-draw. NÃO use para blocos individuais compactos de cinco partes com opções e prós/contras: isso faz o decision-shot. NÃO use para a análise de um caso isolado com frameworks: isso faz o decide."
visibility: public
language: pt
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [entscheidung, abhaengigkeiten, ascii-graph, decision-path, visualisierung, routing, widerspruchs-erkennung]
status: active
dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, decision-draw, decision-shot, decision-avatar]
provenance:
  origin: "custom"
  decision_ref: "T-20260913-107991667 (Ticket-Master, Nutzerauftrag 2026-09-13)"
translated_from_sha256: 68422f7ca7043f158883734f79aadf21f8830b6238588a896255dccd8abc952a
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:40:39.337351+00:00"
---
<img src="banner.png" width="100%" alt="decision-path banner">

# decision-path — Grafo ASCII de dependências de decisões em aberto

> As decisões não são tomadas no vácuo. O que, isoladamente, parece razoável
> muitas vezes bloqueia trabalhos seguintes, exige pré-etapas inacabadas ou
> contorna contratos de proteção existentes. O decision-path torna visíveis, de
> forma transparente no terminal, as causalidades, as sequências e as contradições.

---

## Quando usar

- Um estoque de decisões em aberto (proveniente do [decision-briefing](../decision-briefing/SKILL.md) Fase 1, de um contexto de sessão ou de um documento de decisão) deve ser estruturado.
- Deve-se esclarecer quais decisões podem ser tomadas de imediato sem restrições (nós-raiz) e quais dependem de pré-condições ou de bloqueadores externos.
- É necessária uma visão geral de quais recomendações se harmonizam entre si e onde duas deliberações se contradizem lógica ou organizacionalmente.
- Palavras-gatilho: `/decision-path`, “quais decisões dependem umas das outras”, “grafo de dependências das decisões”, “visualizar o caminho de decisão”, “árvore de decisão ASCII”, “contradições entre decisões”, “verificar causalidades”.
- **Não** usar:
  - Para o primeiro levantamento e inventário de questões em aberto: isso faz o [decision-briefing](../decision-briefing/SKILL.md) Fase 1.
  - Para reunir as variantes recomendadas em um quadro coerente para aprovação: isso faz o [decision-draw](../decision-draw/SKILL.md).
  - Para blocos individuais compactos de cinco partes com opções e prós/contras por opção: isso faz o [decision-shot](../decision-shot/SKILL.md).
  - Para a elaboração metódica de uma única questão complexa (Weighted Scoring, cenários): isso faz o [decide](../decide/SKILL.md).

---

## Delimitação na família de decisões

| Skill | Tarefa | Entrada | Saída |
|---|---|---|---|
| `decide` | Elabora **uma única** decisão metodicamente | Critérios, opções | Matriz de avaliação, decisão individual |
| `decision-briefing` | **Decompõe muitas** decisões em aberto em questões individuais com opções | Lista de pontos em aberto | Briefing numerado A/B/C/D, marcações preliminares, registro |
| `decision-path` | **Valida e visualiza causalidades e contradições** em muitas decisões | Marcações preliminares do briefing / registro | Grafo de dependências ASCII com 5 avaliações por nó e status das arestas |
| `decision-draw` | **Reúne recomendações em um quadro geral** para aprovação como um todo | Pacote da `decision-path` | Conceito, interação (apenas a variante recomendada), retransferência |
| `decision-shot` | Condensa **análises concluídas** à essência (1 decisão ou um pacote restrito) | 1 questão analisada ou um grupo | Resumo de cinco partes com opções, prós/contras e link para a análise completa |
| `decision-avatar` | Fornece a **modelagem das preferências do usuário** | Contexto, deliberações anteriores | Avaliação de confiança 🟢 / 🟡 / 🔴 |

### Contrato e competência em relação ao decision-briefing

O `decision-briefing` Fase 1 já identifica, ao ser lido, dependências e sequências de forma preliminar (por exemplo, a partir de palavras-sinal como “Depois automaticamente:”, bloqueadores ou referências a tickets). O `decision-path` não deduz essa estrutura uma segunda vez de forma silenciosa, mas se apoia diretamente nessas marcações preliminares:

1. **O decision-briefing fornece as marcações preliminares:** ele disponibiliza o inventário bruto das decisões em aberto e os primeiros sinais de vinculação.
2. **O decision-path valida, avalia e visualiza:** ele verifica os sinais contra o estado real de comprovação, separa arestas comprovadas de presumidas, atribui as cinco avaliações por nó e expõe sem piedade as colisões com gates.
3. **Retorno em caso de divergências:** se o `decision-path` encontrar uma dependência que falte no briefing ou que tenha sido registrada de forma incompleta, ele nunca a assume em silêncio, mas a devolve ao briefing como nota de correção.

---

## As cinco avaliações por nó (e status de comprovação das arestas)

As cinco dimensões `[S E U Z W]` avaliam os **nós** (as decisões pendentes ou já tomadas no contexto sistêmico). As arestas trazem seu tipo de relação semântica (por exemplo, liberadora, bloqueadora, pressuposta) e seu status de comprovação (comprovado vs. presumido).

Cada nó do grafo traz uma linha de avaliação compacta com exatamente cinco dimensões:

```
[S+ E:<Option> U<Richtung><Konfidenz> Z+ W-]
```

1. **sensato (`S`)** — Viabilidade técnica e arquitetônica:
   - `S+`: A solução é robusta, resolve um problema real e evita complexidade desnecessária.
   - `S~`: Parcialmente sensata, mas traz riscos de manutenção ou de processo.
   - `S-`: Solução aparente, ativismo ou caminho sabidamente equivocado (por exemplo, filtro aplicado na alavanca errada).

2. **recomendado (`E`)** — A recomendação de ação concreta e baseada em fatos:
   - `E:<Option>`: Opção clara (por exemplo, `E:A`, `E:B`, `E:klaeren`, `E:Schritt1`).
   - `E-`: Nenhuma recomendação possível (por exemplo, por falta de fatos ou diante de uma questão de princípio genuína).

3. **típico do usuário (`U`)** — Correspondência com o modo de trabalho e as regras do usuário (via `decision-avatar`):
   Codifica **direção** (a opção combina com o modo de trabalho?) e **comprovação / confiança** separadamente:
   - **Direção (primeiro caractere após U):**
     - `+`: Típico do usuário — corresponde a decisões historicamente comprovadas, diretrizes (`CLAUDE.md`, políticas) ou preferências explícitas do usuário.
     - `~`: Neutra / em aberto — nenhuma direção de preferência pronunciada pode ser comprovada.
     - `-`: Atípica — rompe com o modo de trabalho habitual ou com os padrões anteriores do usuário.
   - **Comprovação / confiança (segundo caractere):**
     - No grafo ASCII, puramente ASCII:
       - `!`: Alta / comprovada (em prosa: 🟢 comprovado).
       - `~`: Média / plausível (em prosa: 🟡 decisão de avaliação, é necessária ponderação do usuário).
       - `?`: Baixa / não comprovada (em prosa: 🔴 território inexplorado, questão de princípio). **Escalar em vez de adivinhar!**
   - *Exemplos:* `U+!` (típica do usuário e comprovada), `U+~` (típica do usuário, mas questão de ponderação), `U-!` (comprovada e atípica), `U~?` (em aberto, sem orientação → escalação).

4. **compatível (`Z`)** — Encaixe suave, estilístico e arquitetônico com os vizinhos:
   - `Z+`: Combina sem atrito, estilística e arquitetonicamente; forma um todo coerente sem fricção.
   - `Z~`: Leve atrito estilístico ou esforço organizacional extra, mas funcionalmente compatível.
   - `Z-`: Causa atrito perceptível no conjunto do sistema (por exemplo, proliferação de configurações, acoplamento inadequado, quebra de paradigma), mas ainda não viola nenhuma regra rígida.

5. **contraditório (`W`)** — Contradição rígida e violação de regra ou gate (**saída mais importante — alarme!**):
   - `W-`: Livre de contradição em relação a outras recomendações, diretrizes vinculantes e gates de proteção ativos.
   - `W+`: **Colisão grave / Alarme!** Anula outra recomendação, viola uma política vinculante (`CLAUDE.md`, P-00x) ou desrespeita um gate de proteção ativo. Nós em colisão devem sempre ser listados, obrigatoriamente, na seção `WIDERSPRUECHE`, com causa e caminho de resolução.

---

## Tipos de aresta e regras de derivação

As dependências são derivadas **estritamente dos textos-fonte**, nunca inventadas de forma especulativa. As arestas trazem seu tipo de relação e seu status de comprovação:

| Sinal no texto | Tipo de aresta | Notação | Significado |
|---|---|---|---|
| “Depois automaticamente: …”, “libera”, “possibilita” | Libera | `+-->` | A decisão de destino só se torna executável por meio da decisão de origem (comprovado) |
| “bloqueia”, “impede”, “gate de proteção se aplica” | Bloqueia | `=>` | O destino fica bloqueado enquanto a origem não for resolvida |
| “pressupõe”, “exige antes”, “pré-condição” | Pressupõe | `-->` | O destino exige, cronológica e logicamente, a decisão de origem |
| “Decisão subsequente”, “passo 2 depois” | Sequência | `-->` | Passo lógico seguinte à conclusão |
| “está refutado por medição”, “superado”, “sem efeito” | Invalida | `--X-->` | O conhecimento da origem torna obsoleto o item de destino |
| Mesmo D-ID, mesmo ID de ticket ou mesmo sistema sem comprovação textual | Presumido | `?-->` | Vinculação plausível, sem prova causal explícita (não comprovada) |

> **Regra para arestas não comprovadas:**
> Quando não houver comprovação causal explícita no texto, a aresta é marcada como presumida (`?-->`) — jamais como fato comprovado. Quando nenhuma relação estiver comprovada, os nós ficam lado a lado, independentes.

---

## Requisitos de formato para o grafo ASCII

1. **Monoespaçado e adequado ao terminal:** largura máxima de linha de **100 colunas**. Nada de tabelas largas que quebrem no terminal.
2. **Conjunto de caracteres e pureza:** ASCII puro. Dentro do bloco de código do grafo não podem aparecer emojis (🟢🟡🔴); as confianças são codificadas ali exclusivamente por caracteres ASCII (`!`, `~`, `?`).
3. **IDs de nós:** somente as siglas existentes (`PD-A`, `MD-A`, `BH-A`, `VM-A`, `QR-A`, `CL-A`, `MO-A`, `D-001`, `732597768`). Nunca inventar novos IDs artificiais! Se faltar uma sigla, vale o número do item. Etapas internas subsequentes são registradas como anotações não numeradas `(...)` junto à aresta.
4. **Estrutura em níveis:**
   - `EBENE 0 - haengt an nichts`: Nós-raiz, decisões não bloqueadas, alavancas externas.
   - `EBENE 1 - haengt an genau einer`: Decisões subsequentes diretas.
   - `EBENE 2 - haengt an mehreren / tiefe Kette`: Nós com dependência múltipla ou posteriores.
   - `WIDERSPRUECHE`: Contradições rígidas, colisões com gates e recomendações inconsistentes (`W+`).
   - `LEGENDE`: Componente obrigatório de todo grafo. Cada caractere estrutural usado no grafo (`|`, `=Option`, `(...)`, setas das arestas) deve constar da legenda e ser explicado.
5. **Projeção Mermaid opcional:** pode ser anexada, se necessário, como bloco de código adicional (`mermaid`), quando isso não exigir esforço extra. O grafo ASCII continua sendo a saída primária e vinculante.

---

## Exemplo (trecho piloto: Ticket-Master 2026-09-13)

Trecho real do documento de decisões do Ticket-Master (`732597768`, `MO-A`, `CL-A`, `QR-A`, `387521104`, `CL-B`):

```
====================================================================================================
DECISION-PATH: ABHAENGIGKEITSGRAPH (Pilot Ticket-Master 2026-09-13)
====================================================================================================

EBENE 0 - haengt an nichts (Wurzelentscheidungen & externe Blocker)
  [732597768] GitHub-Billing klaeren                        [S+ E:klaeren U+! Z+ W-]
      |  schaltet frei
      +--> [MO-A] Welle 2 freigeben                         [S+ E:A       U+~ Z+ W-]

  [CL-A] clutch Admin-Merge PR #6 & PR #8                   [S+ E:A       U+! Z+ W-]
      |  blockiert durch: [Gate "1 Approving Review" (Self-Approval unmoeglich)]
      --> (Folgeentscheidung: Branchschutz auf 0 oder Bot anpassen)

  [QR-A] Queue-Rename Junction (_TICKETS -> TICKETS)        [S+ E:B       U+! Z+ W-]
      +--> [387521104] Nachtfenster faehrt                  (belegt: nur unter B)

  [CL-B] Review-Gate-Pilot: Mac-Signierschluessel           [S+ E:Schritt1 U+~ Z+ W-]
      --> (Folgeschritte 2-4: Modell-Automatisierung nach Schluessel-Bereitstellung)

EBENE 1 - haengt an genau einer Vorbedingung
  [MO-A] Welle 2 freigeben                                  [S+ E:A       U+~ Z+ W-]
      |  setzt voraus: [732597768] (Billing geklaert, Remote-CI-Gates wieder aktiv)
      |  setzt voraus: [Gate PRIVATE.txt "gruenes Remote-CI"]
      --> (Folgeschritt: Sichtbarkeit schalten bleibt reine Nutzerhandlung)

EBENE 2 - haengt an mehreren / tiefe Kette
  [387521104] Nachtfenster Migration autonom fahren         [S+ E:B       U+! Z+ W-]
      |  setzt voraus: [QR-A]=B (NTFS-Junction gesetzt)
      |  setzt voraus: (Junction auf dem zweiten Host per Transfer-Ticket gesetzt -
      |                  Ticketnummer in der Vorlage nicht genannt)

----------------------------------------------------------------------------------------------------
WIDERSPRUECHE & GATE-KOLLISIONEN
----------------------------------------------------------------------------------------------------
  [MO-A]=B  X  [Gate PRIVATE.txt "gruenes Remote-CI"]
               Konflikt: Option B wuerde Welle 2 rein auf lokaler Testbasis freigeben,
               obwohl zwei Modulvertraege ausdruecklich gruenes Remote-CI fordern.
               Aufloesung: Empfehlung A erzwingt erst [732597768] (Billing), heilt Kollision.

  [CL-A]=StatusQuo  X  [Gate "1 Approving Review" (Self-Approval unmoeglich)]
               Konflikt: master verlangt 1 Review, einziges Repo-Konto ist lukisch.
               Aufloesung: Empfehlung A (Admin-Merge) bricht Blockade legitim auf.

----------------------------------------------------------------------------------------------------
LEGENDE & BEWERTUNGSSCHLUESSEL
----------------------------------------------------------------------------------------------------
  Kanten & Struktur:
    +-->   schaltet frei (Kausalitaet im Quelltext belegt)
    =>     blockiert / verhindert (Gate oder externer Blocker)
    -->    setzt voraus / Reihenfolge (Vorbedingung oder Folgeschritt)
    ?-->   vermutete Abhaengigkeit (Koppelung plausibel, aber unbelegt)
    --X--> entwertet / ueberholt (macht Zielposten obsolet)
    X      Widerspruch / Kollision (Gate- oder Regelverletzung)
    |      vertikaler Verbindungsstrang / Attribut-Zuordnung
    [ID]   Entscheidungsknoten (Kuerzel oder Postennummer aus Vorlage)
    [Gate]  externes Gate / Regel / Vertrag - KEIN Entscheidungsknoten
    =Opt   spezifische Option eines Knotens (z. B. [MO-A]=B)
    (...)  unnummerierte Kanten-Annotation / Folgeschritt (keine neue ID)

  Knoten-Status [S E U Z W]:
    S: Sinnvoll      (+ tragfaehig / ~ mit Vorbehalt / - ungeeignet)
    E: Empfohlen     (A, B, C, klaeren, Schritt1, - keine Empfehlung)
    U: Usertypisch   (Richtung: + typisch / ~ neutral / - untypisch;
                      Konfidenz: ! gesichert / ~ Abwaegung / ? Eskalation)
                      [! = belegt (Prosa gruen), ~ = Nutzerabwaegung (Prosa gelb),
                       ? = ungesichert / Eskalation (Prosa rot)]
    Z: Zusammenpass. (+ harmoniert stilistisch / ~ Reibung / - Architektur-Bruch)
    W: Widerspruch   (- widerspruchsfrei / + harte Kollision mit Gate oder Regel)
====================================================================================================
```

---

## O que o decision-path NÃO faz

1. **Não toma decisões:** a skill entrega um mapeamento transparente da situação. A autoridade decisória permanece com o usuário.
2. **Não elabora opções:** a skill não discute variantes novas nem catálogos de critérios; isso é tarefa do [decide](../decide/SKILL.md) ou do [decision-briefing](../decision-briefing/SKILL.md).
3. **Não reescreve no registro:** o grafo não modifica arquivos de registro ou de tickets. A gravação de volta, após a decisão, cabe à Fase 4 do [decision-briefing](../decision-briefing/SKILL.md) ou ao mecanismo de retransferência do [decision-draw](../decision-draw/SKILL.md).
4. **Nada de siglas crípticas no texto corrido ao usuário:** quando os resultados do grafo forem explicados ao usuário, vale a regra de estilo vinculante (T-20260913-883789445): 2 a 4 frases em linguagem cotidiana, em primeira pessoa (situação, “Eu faço …”, alternativa de recuo). Os rótulos dos nós usam títulos curtos legíveis. Identificadores técnicos e números de tickets vão para uma tabela em anexo.

---

## Proveniência da sessão

Se o grafo de dependências for salvo como artefato de análise persistente, o documento termina com:

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

- Prioridade das fontes: indicação explícita de runtime/CLI; depois, ambiente ou hook autoritativo do provedor; caso contrário, `unbekannt`.
- Subagentes herdam o ID de sessão da sessão-pai.
- Conversas rotineiras e saídas temporárias do terminal não recebem carimbo.

---

## Changelog

### 1.1.0 (2026-09-18)
- Regra de estilo para textos de decisão compreensíveis ancorada (T-20260913-883789445, instrução do usuário de 2026-09-13):
  - Explicações ao usuário em primeira pessoa natural, sem avalanche de números.
  - Títulos curtos legíveis para os nós no grafo do terminal.
  - Vinculação técnica (números de ticket/D) transferida para uma tabela em anexo.

### 1.0.0 (2026-09-13)
- Versão inicial com base na solicitação do usuário T-20260913-107991667.
- Chave de avaliação de cinco partes por nó (sensato, recomendado, típico do usuário com direção e confiança separadas via `decision-avatar`, compatível, contraditório); as arestas trazem tipo de relação e status de comprovação.
- Contrato vinculante com `decision-briefing`: o briefing fornece marcações preliminares, o decision-path valida e visualiza; retorno em caso de divergências.
- Delimitação clara em relação ao `decision-shot` pelo formato de saída (blocos compactos de cinco partes com opções e prós/contras).
- Correção da estrutura causal: CL-A no gate de aprovação em vez de faturamento; eliminação de IDs inventados em favor de anotações de aresta não numeradas.
- Especificação ASCII consistente (máx. 100 colunas) com notação de aresta uniforme `--X-->`, legenda estrutural completa e código de grafo sem emojis.
