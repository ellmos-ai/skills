---
name: work-autonomous
version: 1.5.1
type: protocol
author: Lukas Geiger + Claude
created: 2026-08-15
updated: 2026-09-09
description: "Condição de encerramento para loops autônomos: continuar trabalhando de forma independente o máximo possível E encerrar um loop somente quando estiver comprovado que não há mais nenhuma tarefa executável de forma autônoma. A mera impressão de \"nada mais a fazer\" NÃO basta — ela aciona uma cadeia de verificação em quatro etapas (think/decide, _CONTROL/_DECISIONS, Gardener/USMC, decision-avatar/BYUM), que precisa primeiro OBTER novas tarefas antes que o loop possa terminar. Cada etapa da cadeia informa found/empty/unavailable em vez de um resultado binário — \"exhausted\" só vale quando TODAS as fontes foram de fato consultáveis; se pelo menos uma fonte estiver unavailable, a skill informa \"blind\" em vez de \"exhausted\" e não afirma nada não verificado. Use esta skill em /work-autonomous, /waafap, \"continue trabalhando de forma autônoma até não haver mais nada a fazer\", como condição de objetivo dentro de um /loop, ou quando for preciso verificar se realmente não resta trabalho autônomo antes de encerrar um loop/uma sessão."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [autonomy, loop, goal, workflow, decision, exhaustion-check, guard, ticket-master]
language: pt
status: active
visibility: public
aliases: [waafap, work-autonomous-as-far-as-possible]

dependencies:
  tools: []
  services: []
  protocols: [think, decide, decision-avatar]
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: a8ee248e73bb81d9af36df2f3e82719bed0f31e89005ab64c35f4e236b15600c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.160760+00:00"
---
<img src="banner.png" width="100%" alt="work-autonomous banner">

# work-autonomous — encerrar o loop somente quando comprovadamente não houver mais tarefas autônomas

## Finalidade

Esta skill faz duas coisas ao mesmo tempo:

1. **Continuar trabalhando de forma autônoma o máximo possível** — trabalho normal de sessão, sem nada de especial.
2. **Encerrar um loop somente quando estiver COMPROVADO** que não existe mais nenhuma tarefa executável de forma autônoma. A suspeita de "não encontro mais nada a fazer" **não** é motivo de encerramento — ela é o **gatilho** de uma cadeia de verificação que primeiro tenta **obter** novas tarefas. Só quando essa cadeia permanece totalmente sem resultado o encerramento passa a estar comprovado.

**Propositalmente sem `/goal` embutido:** A skill é utilizável de forma independente (p. ex. diretamente como chamada `/work-autonomous` dentro de uma sessão normal) e também como condição dentro de uma construção de loop superior: `/loop` normalmente, depois indicar como objetivo apenas esta skill. O objetivo fica então, em substância: *"Encerre o loop quando não houver mais tarefas autônomas — e até lá continue trabalhando de forma autônoma o máximo possível."* A própria skill não invoca nenhuma construção `/goal`; ela apenas fornece o sinal de encerramento inequívoco que tal construção pode ler (ver "Sinal de encerramento" abaixo).

## Modelo operacional — dois níveis

### Nível 1 — Trabalho normal (cada tick)

#### Gate de intake do TICKET-MASTER (prioridade sobre tudo o mais neste nível)

**Relevante somente se algum sistema de tickets (`_TICKETS/`) fizer parte do contexto** — sessões sem sistema de tickets pulam este gate sem qualquer efeito; a skill continua utilizável sem nenhum sistema de tickets (ver "Finalidade" acima). Quando aplicável, verificar primeiro se `INBOX/` — incluindo entradas informais ainda não colocadas no formato de ticket — está totalmente formalizado e triado. Se não estiver, isso conta como trabalho autônomo encontrado (formalizar/triar é trabalho burocrático sem decisão do usuário, ver a distinção abaixo) — executar, o tick termina, o Nível 2 não é atingido, como em qualquer outra fonte do Nível 1.

**Enquanto a INBOX estiver aberta, NÃO podem surgir `NO_WORK`, um sinal de exaustão (`exhausted`/`blind`), um STOP de guarda ou qualquer outro sinal de encerramento.** Somente quando o intake estiver totalmente triado podem ser verificados `ACTIONABLE`, `BLOCKED` desbloqueados e `WAITING` vencidos (abaixo) — e só então, se for o caso, o Nível 2.

*Caso comprovado:* um loop começou a verificação de exaustão logo após concluir `ACTIONABLE`, enquanto continuavam chegando novos tickets `INBOX`, dois deles com prioridade P1. Sem este gate, o loop teria informado `exhausted`/`blind` mesmo com a entrada aberta — exatamente o que o gate impede.

Depois disso, procurar normalmente por mais trabalho executável de forma autônoma (ver a distinção abaixo) e executá-lo: tickets `ACTIONABLE` abertos, tickets `BLOCKED` desbloqueados, tickets `WAITING` vencidos, pontos `TODO.md`/`AUFGABEN.txt` abertos em projetos sem dependência do usuário, verificações rotineiras/de higiene vencidas segundo a política local, trabalho iniciado mas não concluído da última sessão (USMC `working`), **execuções `tidy-up` vencidas do projeto ativo** (complemento 1.3.0, 2026-08-19 — ver a skill `tidy-up`: uma passagem Tasksolver+Writer+Maintainer sobre a pasta do projeto em que a sessão estava trabalhando; a vencibilidade é verificada pelo próprio `tidy-up` por meio de seu log USMC enxuto, ver a seção correspondente "Relação com work-autonomous").

→ **Encontrado e concluído:** informar brevemente o resultado, o tick termina, o loop segue normalmente. O Nível 2 NÃO é atingido — nenhuma das quatro verificações custosas é necessária enquanto houver trabalho visível.

### Nível 2 — Verificação de exaustão (somente com suspeita de "nada mais a fazer")

Só quando o Nível 1 não encontrar mais nada autônomo surge a suspeita. Essa suspeita sozinha não basta. Agora a cadeia a seguir roda **obrigatoriamente**, para **obter** novas tarefas.

#### Autoconhecimento (antes da cadeia, não depois)

Antes de consultar qualquer coisa, a skill declara QUAIS fontes precisa para seu juízo. Quatro necessidades (`grounding_seed.self_knowledge.Need`, se `grounding-seed` estiver instalado — caso contrário, a mesma lista vale como mera declaração, sem vínculo com a biblioteca):

| Papel | Etapa da cadeia | O que está por trás |
|---|---|---|
| `decisions.ledger` | 2 | registro central de decisões |
| `memory.organic` | 3 | Gardener (`find()`/`put()`) |
| `memory.curated` | 3 | USMC (`facts`/`lessons`/`working`/`context`) |
| `user.model` | 4 | decision-avatar / BYUM |

**`/think` + `/decide` (etapa 1) é deliberadamente NÃO uma fonte declarada.** É a própria etapa analítica do modelo, não um sistema externo que poderia estar ou não acessível — ela está sempre "disponível" no sentido desta distinção. Somente as etapas 2–4 podem tornar-se `unavailable`.

Ferramenta opcional e testável para a mera questão de localização (found/unavailable, ainda SEM verificação de conteúdo): `scripts/exhaustion_check.py` nesta pasta da skill. Ela usa `grounding_seed.resolve()` + `status_from_resolution()` para `decisions.ledger`/`user.model` (aí existe um provedor `source-resolver` real), verifica `memory.organic`/`memory.curated` **sempre** diretamente por acessibilidade de CLI (`gardener`/`usmc` no PATH) — para esses dois papéis, até 2026-08-15 ainda não havia nenhum provedor `source-resolver` registrado; consultá-los pelo resolvedor teria informado apenas `unavailable`, independentemente de Gardener/USMC estarem realmente instalados. Funciona de forma idêntica com e sem `grounding-seed` instalado.

**Atualização 2026-08-25 (K3=C, `T-20260825-342866657`):** A lacuna está fechada — `source-resolver` registra agora `memory.organic` (Gardener) e `memory.curated` (USMC) ambos como papel de nível 1, com a mesma verificação de presença por CLI (`shutil.which("gardener")`/`shutil.which("usmc")`) que este script ainda codifica diretamente. Por isso `exhaustion_check.py` NÃO foi reescrito de imediato (nenhuma perda funcional, a verificação atual continua correta) — na próxima execução de manutenção da skill, a etapa 3 pode ser migrada para `source_resolver.resolve("memory.organic"/"memory.curated")`, de forma análoga à etapa 2 (`decisions.ledger`), em vez de manter a verificação de CLI em duplicidade.

#### As quatro etapas da cadeia — cada uma informa found | empty | unavailable

Cada etapa funciona em duas fases: primeiro a **localização** (sei sequer de algum lugar acessível?), depois — somente se localizada — a **verificação de conteúdo** (o modelo realmente lê, com suas próprias ferramentas, se há algo novo ali). Uma fonte que não pôde ser localizada NUNCA é verificada quanto ao conteúdo — ela conta como `unavailable`, não como `empty`.

1. **`/think` + `/decide`** aplicados à pergunta: "Realmente não há mais nenhum trabalho executável de forma autônoma, ou estou deixando algo passar?" — análise estruturada em vez de intuição. Nenhum status found/empty/unavailable (ver acima, nenhuma fonte).
2. **`decisions.ledger`** — localização via `source_resolver.resolve("decisions.ledger")` /
   `grounding_seed.resolve(...)`, se instalado; caso contrário o caminho de fallback conhecido
   (`_control-center/_CONTROL/_DECISIONS/`, cadeia `TO-DECIDE-USER*.txt`, `TO-DECIDE-USER-<HOST>.txt` próprio do host, `DECIDED-AND-DONE.md`). Localizado → ler o conteúdo: foram tomadas decisões recentes que desbloqueiem trabalho antes bloqueado ou aguardando liberação? Achado → `found`. Lido, nada novo → `empty`. Não localizável (resolvedor ausente E caminho de fallback inexistente) → `unavailable`.
3. **`memory.organic` (Gardener) + `memory.curated` (USMC)** — duas fontes separadas, uma etapa da cadeia. Localização: CLI no PATH (`gardener`/`usmc`), ver o autoconhecimento acima. Acessível → ler o conteúdo (`find()`/`recall()` ou `usmc facts|lessons|working|context`): pontos abertos da memória de trabalho, lições com tarefa de acompanhamento pendente, fatos que apontem para trabalho executável que passou despercebido (exatamente onde sessões anteriores deixam pontos inacabados — campo `RESUME:`, entradas `note` abertas). Achado → `found`. Lido, nada novo → `empty`. CLI não está no PATH → `unavailable`.
4. **`user.model` (decision-avatar/BYUM)** — localização como em `decisions.ledger` (resolvedor ou caminho de fallback `_control-center/_CONTROL/_USER-MIND/`). Localizado → verificar o conteúdo: existe um padrão comprovado segundo o qual o usuário gostaria de ver uma determinada ação executada de forma autônoma nesse ponto? Só conta como `found` com confiança suficiente (🟢/🟡) — 🔴 conta como `empty`, não como tarefa ganha, mas como ponto aberto para a etapa "resto que depende só do usuário" abaixo. Não localizável → `unavailable`.

**"Exhausted" só pode ser informado quando TODAS AS QUATRO fontes (etapas 2–4, três etapas, quatro papéis) puderam de fato ser consultadas — ou seja, `found` ou `empty`, nenhuma única `unavailable`.** Isso corresponde a `grounding_seed.self_knowledge.GroundingReport.all_answerable()`. Se pelo menos um papel for `unavailable`, NÃO vale "exhausted", e sim o sinal próprio "blind" (ver o sinal de encerramento abaixo) — o loop encerra mesmo assim (afinal não pode consultar nada), mas não afirma mais ter verificado o que não conseguiu verificar.

Se alguma etapa encontrar trabalho novo → de volta ao Nível 1, executar o trabalho, e definir o estado da guarda (ver abaixo) como "found" em vez de "exhausted"/"blind".

### Caso especial: somente restos dependentes do usuário

Se a cadeia não encontrar mais nenhuma tarefa **autônoma**, mas houver tickets `USER/*` ou pontos `_DECISIONS` não decididos em aberto, isso ainda é uma PARADA para a autonomia — porém não "nada a fazer", e sim "nada *autônomo* a fazer". Esses pontos são apresentados **agrupados** segundo a regra de loop de autonomia a partir de `ticket-master` (um modelo de consolidação único, não pings individuais), e não perguntados um a um. O sinal de encerramento distingue expressamente este caso de ociosidade real.

## Distinção — o que conta como "executável de forma autônoma"?

Referência: categorias `ticket-master` (`.AI/.MODULES/.CONTROL/ticket-master/docs/CATEGORIES.de.md`).

| Caso | Autônomo? | Justificativa |
|---|---|---|
| `INBOX/` inclusive entradas informais, sob TICKET-MASTER (antes da triagem) | **Sim, com prioridade** | Formalizar/triar é trabalho burocrático sem decisão do usuário — vem antes de `ACTIONABLE`/`BLOCKED`/`WAITING` e bloqueia até então qualquer sinal de encerramento (ver o gate de intake acima). |
| ticket `ACTIONABLE` | **Sim** | Sem bloqueio, sem dependência do usuário — por definição. |
| `BLOCKED/*` (host-receipt, foreign-state, lock, quota, dependency) | Não, enquanto o bloqueio não tiver sido **empiricamente** removido | Nova verificação periódica é permitida (loop de autonomia), "existe" não basta como prova — é preciso comprovação. |
| `WAITING/*` (scheduled, review-due, marker) antes do prazo/marcador | Não | Vinculado a prazo. |
| `WAITING/*` após o prazo/marcador | **Sim** | Condição cumprida → passa para `ACTIONABLE`. |
| `USER/*` (decision, data, freigabe, hardware, session) | **Nunca autônomo** | Exige obrigatoriamente decisão/dados/liberação/hardware/sessão do usuário. Apresentar agrupado, ver acima. |
| `PARKED/*` (skip, backlog, until-trigger) | Não, salvo instrução ou gatilho explícito | Deliberadamente adiado, sem nova verificação automática. |
| Pontos `TODO.md`/`AUFGABEN.txt` abertos sem registro de liberação/decisão | **Sim** | Registro de projeto, trabalho normal. |
| Verificações rotineiras/de higiene vencidas (cooldown expirado, sem lock) | **Sim** | Manutenção regular segundo a política local. |
| Áreas bloqueadas por `LOCK.user.*` | **Nunca** | Bloqueio do usuário — somente o usuário o levanta, ver LOCK-SYSTEM. |
| Passos irreversíveis/com efeito externo sem liberação de política (upload no Zenodo, push em branches julgadas/protegidas, decisão de gasto em servidor além do limite do notebook, exclusão definitiva sem pré-visualização) | **Não** | Exige liberação/decisão, mesmo que tecnicamente executável. |
| Sessão que só pode ser iniciada via GUI/login (p. ex. tarefa do Claude Desktop, login interativo, ação física em hardware) | **Nunca** | "Sessão iniciável apenas pelo usuário" — nenhum loop pode assumi-la. |

Regra prática: é autônomo tudo o que pode ser concluído **sem** decisão, liberação, dados, hardware ou sessão do usuário E que não exige nenhum passo irreversível/com efeito externo sem liberação documentada da política.

## Guarda contra loops infinitos (obrigatória)

**Problema:** sem freio, a cadeia de quatro etapas rodaria por completo a cada nova verificação, mesmo que nada tivesse mudado desde a última passagem sem resultado — caro e inútil, sobretudo quando a skill é chamada repetidamente (loop, tarefa agendada, nova chamada manual logo em seguida).

**O estado é persistido no USMC** (estado de processo, neste sistema, pertence a ele, e não a arquivos Markdown):

```bash
# Zustand lesen (nach Tag work-autonomous-guard filtern)
usmc --agent <agent> working --limit 20

# Zustand nach einem Kettendurchlauf schreiben
usmc --agent <agent> note "work-autonomous-guard: result=<exhausted|blind|found> fingerprint=<FP> at=<ISO-Zeit>" \
  --type context --priority 3 --tags "work-autonomous-guard,<projekt-slug>"
```

**A impressão digital é composta de DUAS partes — a situação E a acessibilidade:**

1. **Parte da situação** (como antes): quantidade/IDs de tickets `ACTIONABLE` abertos, mtime da cadeia `_DECISIONS` (`TO-DECIDE-USER*.txt`, `DECIDED-AND-DONE.md`), número de novas entradas USMC `working` desde a última passagem da cadeia.
2. **Parte da acessibilidade (nova, obrigatória desde 1.2.0):** a tupla ordenada dos papéis que a verificação de autoconhecimento acabou de informar como `unavailable` (`exhaustion_check.availability_fingerprint_component()`), por exemplo `("memory.organic",)` ou `()`.

**Por que a segunda parte é obrigatória — "a guarda herda a lacuna":** sem ela, a impressão digital (parte 1) se apoia, entre outras coisas, no mtime da cadeia `_DECISIONS`. Se essa cadeia faltar por completo em um sistema, essa parte da impressão digital fica constante para sempre — um `exhausted`/`blind` definido por engano jamais seria verificado de novo, mesmo que depois `source-resolver` fosse instalado ou `_control-center/_CONTROL/_DECISIONS/` criado. A parte de acessibilidade resolve justamente isso: se muda QUAIS papéis estão unavailable (uma fonte aparece ou desaparece), a impressão digital muda automaticamente — a guarda percebe isso na próxima chamada e refaz a cadeia. Trata-se de "transplante" no sentido da metáfora de grounding (T-20260815-371628859): uma mudança de ambiente dispara uma nova busca, sem que alguém precise redefinir a guarda manualmente.

**Fluxo antes de cada passagem da cadeia:**

```
guard = letzten "work-autonomous-guard"-Eintrag aus USMC lesen
wenn guard existiert
   und guard.result in ("exhausted", "blind")
   und (jetzt - guard.timestamp) < GUARD_INTERVAL   (Default: 15 Minuten)
   und fingerprint(jetzt) == guard.fingerprint:      # Lage- UND Verfügbarkeits-Baustein
       → Kette NICHT erneut fahren.
       → guard.result == "exhausted":
           Melden: "Weiterhin keine autonome Arbeit — unverändert seit {guard.timestamp}.
                    Kein neuer Trigger. STOP (Guard aktiv, exhausted unchanged since …)."
       → guard.result == "blind":
           Melden: "Weiterhin blind (Quellen nicht verfügbar) — unverändert seit {guard.timestamp}.
                    STOP (Guard aktiv, blind unchanged since …)."
sonst:
       → Kette vollständig fahren (Selbstkenntnis-Prüfung + alle vier Kettenschritte).
       → Neuen Guard-Zustand schreiben (timestamp=jetzt, fingerprint=fingerprint(jetzt),
         result=exhausted|blind|found).
       → alle vier Quellen befragbar UND alle empty → exhausted → STOP (belegt).
       → mindestens eine Quelle unavailable → blind → STOP (nicht belegt, nur unerreichbar).
       → mindestens eine Quelle liefert einen Treffer → found → zurück zu Ebene 1, Arbeit erledigen.
```

Uma única passagem totalmente executada da cadeia, em que TODAS AS QUATRO fontes eram consultáveis e NENHUMA delas trouxe achado, basta como prova de "não há mais tarefas autônomas" (exigência do ticket: "só quando TODAS as etapas de uma passagem permanecerem sem resultado" — sem resultado significa aqui expressamente `empty`, não `unavailable`). A guarda não impede a constatação em si, apenas a **repetição inalterada da constatação** em chamadas próximas — e isso separadamente para `exhausted` E para `blind`, nunca misturados.

`GUARD_INTERVAL` é configurável (padrão de 15 minutos) — em ambientes muito estáticos (novos tickets/decisões raros) pode-se escolher um valor maior; em ambientes muito ativos, um valor menor.

## Sinal de encerramento

Cada passagem termina com **uma** linha inequívoca e pesquisável, para que um `/loop` envolvente ou uma futura construção `/goal` possa ler dela se deve continuar:

```
WORK-AUTONOMOUS: CONTINUE                                          — Ebene 1 hat Arbeit erledigt, Loop läuft weiter.
WORK-AUTONOMOUS: STOP (exhausted)                                  — alle vier Quellen befragt, alle empty. Belegt: keine Arbeit mehr.
WORK-AUTONOMOUS: STOP (blind, N/4 Quellen nicht verfuegbar: <rollen>) — mind. eine Quelle unavailable. NICHT belegt — nur nicht prüfbar.
WORK-AUTONOMOUS: STOP (guard, exhausted unchanged since …)         — Guard aktiv, weiterhin exhausted, kein neuer Trigger.
WORK-AUTONOMOUS: STOP (guard, blind unchanged since …)             — Guard aktiv, weiterhin blind, keine Quelle neu verfügbar geworden.
WORK-AUTONOMOUS: STOP (user-only)                                  — nur USER/*-Reste offen, gebündelt vorgelegt.
```

`CONTINUE` é o único sinal em que um laço superior deve disparar outro tick. Todas as variantes `STOP` são o encerramento comprovado — inclusive com a justificativa de qual caso se aplica.

**A diferença entre `exhausted` e `blind` é essencial para o usuário, não cosmética:** `exhausted` significa "verifiquei tudo o que havia para verificar — o trabalho está concluído". `blind` significa "falta-me infraestrutura para sequer verificar — isso não é um estado de trabalho, e sim uma lacuna". Uma construção `/loop`/`/goal` que trate os dois de forma idêntica (o loop encerra de qualquer jeito) não deve INFORMAR os dois ao usuário da mesma forma — do contrário desaparece justamente a informação que T-20260815-205101335 exigiu.

## Relação com outras skills

- **`think`/`decide`** — fornecem a análise/decisão estruturada da etapa 1 da cadeia. São chamadas aqui como componente, não reinventadas.
- **`decision-avatar`** (esta skill, neutra quanto ao usuário) — fornece a etapa 4. Em sistemas com um perfil concreto e autorizado, isso corresponde a `user-model` + `build-your-users-mind`.
- **`orchestrator`** — regula COMO delegar a subagentes e como verificar a comunicação de conclusão deles. `work-autonomous` regula QUANDO se deixa de buscar; ambas são combináveis (o orquestrador pode aparecer como parte do trabalho realizado no Nível 1).
- **`bugsweep`** — um exemplo de outro protocolo de busca autolimitado (escalada por duplicação em vez de cadeia de quatro etapas). `work-autonomous` é mais genérico: verifica não apenas código em busca de bugs, mas toda fonte de trabalho autônomo.
- **Categorias de tickets (`ticket-master`)** — fornecem o vocabulário para "executável de forma autônoma" (ver a tabela de distinção) e o modelo para o loop de autonomia (nova verificação BLOCKED, agrupamento USER, adiantamento por prazo WAITING, parada PARKED).
- **`tidy-up`** (desde 1.3.0) — fornece uma fonte adicional de nível 1: a passagem única Tasksolver+Writer+Maintainer para a pasta de projeto em trabalho. Verifica sua própria vencibilidade (log USMC enxuto, sem a guarda de quatro etapas daqui) — `work-autonomous` o chama apenas como uma das várias fontes de nível 1, sem duplicar sua lógica.

## Exemplo de fluxo

```
Tick 1: ACTIONABLE-Ticket T-... gefunden → erledigt. WORK-AUTONOMOUS: CONTINUE
Tick 2: Kein ACTIONABLE-Ticket mehr, kein offener TODO-Punkt.
        → Ebene 2: Selbstkenntnis + Kette 1–4 läuft.
        → Schritt 2 (decisions.ledger): verortet, DECIDED-AND-DONE.md hat einen neuen Eintrag
          seit 10 Min. → found, daraus resultiert eine neue autonome Aufgabe.
        → Guard: result=found geschrieben. Aufgabe erledigt. WORK-AUTONOMOUS: CONTINUE
Tick 3: Wieder nichts sichtbar. Voll ausgestattetes System (Gardener, USMC, _DECISIONS, BYUM alle da).
        → Ebene 2: alle vier Quellen verortet UND befragt, alle vier empty.
        → Guard: result=exhausted, fingerprint=FP1 (Lage + Verfügbarkeit ()), timestamp=T1.
        → WORK-AUTONOMOUS: STOP (exhausted)
Tick 4 (2 Minuten später, z. B. durch erneuten Loop-Trigger):
        → Guard: result=exhausted, fingerprint(jetzt)==FP1, (jetzt-T1) < 15 Min.
        → Kette NICHT erneut gefahren.
        → WORK-AUTONOMOUS: STOP (guard, exhausted unchanged since T1)

Gegenbeispiel — System OHNE Gardener/USMC (der Kernfall aus T-20260815-205101335):
Tick 1: Nichts sichtbar. Selbstkenntnis-Prüfung: decisions.ledger verortet (leer, empty),
        memory.organic/memory.curated NICHT verortet (CLI fehlt) → unavailable,
        user.model verortet (empty).
        → nicht alle vier Quellen befragbar → KEIN exhausted.
        → Guard: result=blind, fingerprint=FP2 (Verfügbarkeit ("memory.curated","memory.organic")).
        → WORK-AUTONOMOUS: STOP (blind, 2/4 Quellen nicht verfuegbar: memory.organic, memory.curated)
Tick 2 (Nutzer installiert grounding-seed + usmc auf diesem System):
        → Selbstkenntnis-Prüfung: memory.curated jetzt verortet (CLI auf PATH) → Verfügbarkeits-
          Baustein ändert sich zu ("memory.organic",) → fingerprint(jetzt) != FP2.
        → Guard erkennt Änderung, Kette läuft neu (Verpflanzung) — ohne dass jemand den Guard
          manuell zurückgesetzt hätte.
```

## Changelog

### 1.5.1 (2026-09-09)
- T-20260909-282509082: O fallback documentado para `decisions.ledger` e `user.model` acompanha a mudança comprovada do Control Center para `_CONTROL/_DECISIONS` e `_CONTROL/_USER-MIND`. A precedência do resolvedor e o comportamento fail-closed permanecem inalterados.

### 1.5.0 (2026-09-09)
- P-018: Relatórios de trabalho, handoffs e receipts importantes recém-gerados e persistidos terminam com `session: <session-id> | <agent>@<host> | YYYY-MM-DD`. A prioridade das fontes é: indicação explícita de runtime/CLI antes de ambiente/hook autoritativo do provedor antes de `unbekannt`; os valores nunca são inferidos, e os subagentes usam a sessão-pai. Chat de rotina, fontes, políticas, `CLAUDE.md`, READMEs e arquivos antigos ficam fora de qualquer carimbo global ou retroativo.

### 1.4.0 (2026-09-03)
- Complemento mínimo a partir do ticket T-20260902-729068782: novo **gate de intake do TICKET-MASTER** no Nível 1 (prioridade sobre `ACTIONABLE`/`BLOCKED`/`WAITING`) — relevante somente se um sistema de tickets fizer parte do contexto. Enquanto `INBOX/` (inclusive entradas informais) não estiver totalmente triado, nenhum `NO_WORK`/sinal de exaustão/STOP de guarda pode surgir. Caso comprovado: um loop iniciou a verificação de exaustão enquanto `INBOX` ainda mantinha entradas abertas (inclusive dois tickets P1). A cadeia de exaustão de quatro etapas, a guarda e a utilizabilidade sem TICKET-MASTER permanecem inalteradas — o gate atua exclusivamente no Nível 1 e somente sob TICKET-MASTER.
- Nova função auxiliar testada `scripts/exhaustion_check.py::intake_gate_blocks_stop()` + testes de regressão em `tests/test_exhaustion_check.py` (comportamentais: o gate bloqueia com INBOX aberta, libera com INBOX vazia).

### 1.3.0 (2026-08-19)
- Complemento mínimo a partir do ticket T-20260819-461890468 (nova skill `tidy-up`): o Nível 1 ganha uma fonte adicional e independente — "execuções `tidy-up` vencidas do projeto ativo" (passagem Tasksolver+Writer+Maintainer, ver a skill `tidy-up`). Nenhuma nova etapa da cadeia, nenhuma alteração no Nível 2/guarda/sinal de encerramento — `tidy-up` verifica sua própria vencibilidade por meio de um log USMC enxuto e é aqui referenciada apenas como mais uma fonte do Nível 1, análoga às fontes já existentes (tickets, TODO/AUFGABEN, verificações rotineiras, USMC `working`). Assim, os pontos `tidy-up` contam como tarefa autônoma a executar no sentido de uma construção `/goal` que combina `/work-autonomous` + `/tidy-up` (caso de uso central do ticket). Nenhuma intervenção na cadeia de exaustão de quatro etapas nem na guarda — o Nível 2 permanece inalterado.

### 1.2.0 (2026-08-15)
- Retrofit a partir do ticket T-20260815-205101335 (pedido de verificação: "verifique se a solução se sustenta em conjunto com a metáfora de grounding", constatação na skill entregue: ela se sustentava em três pontos, mas NÃO na distinção "consultado e vazio" vs. "não pôde ser consultado" — a cadeia informava `STOP (exhausted)` mesmo em sistemas sem Gardener/USMC/`_DECISIONS`, sem nunca ter verificado. Primeiro caso real de uso de `grounding-seed`, ticket T-20260815-371628859).
- **Autoconhecimento acrescentado:** quatro necessidades declaradas (`decisions.ledger`, `memory.organic`, `memory.curated`, `user.model`) antes da cadeia, em vez de procurar às cegas em quatro locais fixos.
- **Cada etapa da cadeia (2–4) informa found | empty | unavailable** em vez de um resultado binário — em duas fases: primeiro a localização (`grounding-seed`/`source-resolver` para `decisions.ledger`/`user.model`, verificação direta de CLI para `memory.organic`/`memory.curated`, que ainda não têm provedor `source-resolver`), depois a verificação de conteúdo só se a localização tiver sido bem-sucedida.
- **`exhausted` só vale quando as quatro fontes eram de fato consultáveis** (todas found/empty, nenhuma unavailable). Novo sinal distinguível `STOP (blind, N/4 Quellen nicht
  verfuegbar: …)` para o caso em que pelo menos uma fonte não estava acessível — o loop encerra mesmo assim, mas não afirma mais um resultado verificado.
- **Impressão digital da guarda ampliada com uma parte de acessibilidade** (tupla ordenada dos papéis atualmente unavailable). Corrige a constatação de acompanhamento "a guarda herda a lacuna": sem essa parte, um `exhausted`/`blind` definido por engano permanece válido para sempre quando a cadeia `_DECISIONS` falta por completo (a parte anterior da impressão digital fica então constante). Com a parte nova, uma fonte que se torna acessível dispara automaticamente uma nova passagem da cadeia (transplante no sentido da metáfora de grounding).
- Novo script auxiliar testado `scripts/exhaustion_check.py` (+ `tests/test_exhaustion_check.py`, 11 testes, ambos os modos verificados: com e sem `grounding-seed` instalado) — fornece de forma determinística a verificação de autoconhecimento/localização, para que a skill não precise adivinhá-la a cada execução. Permanece opcional: a skill continua sendo essencialmente um protocolo que um modelo segue com suas próprias ferramentas.
- Dependência: `grounding_seed.self_knowledge.assess()`/`status_from_resolution()` a partir de
  `grounding-seed` 0.2.0 — versões anteriores de `grounding-seed` (0.1.0) tinham um erro de categoria
  (`not_found` era convertido erroneamente em `empty`), que embaralharia novamente exatamente a distinção corrigida aqui. Sem `grounding-seed` instalado, o fallback documentado funciona de forma idêntica.

### 1.1.0 (2026-08-15)
- Retrofit de referência a partir do ticket T-20260815-385400870: a etapa 2 (registro de decisões) agora resolve seu local pelo papel `decisions.ledger` (`source_resolver.resolve(...)`, módulo
  `source-resolver`), em vez de codificá-lo diretamente — com fallback documentado para o caminho anterior, caso o resolvedor não esteja instalado. Comportamento funcional inalterado.

### 1.0.0 (2026-08-15)
- Versão inicial a partir do ticket T-20260815-522639345: modelo operacional de dois níveis, cadeia de verificação de quatro etapas, tabela de distinção segundo as categorias `ticket-master`, guarda contra loops infinitos apoiada no USMC e sinal de encerramento inequívoco para construções `/loop`/`/goal`.
