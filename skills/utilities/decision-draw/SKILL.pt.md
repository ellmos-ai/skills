---
name: decision-draw
version: 1.1.0
type: skill
author: Lukas Geiger + agy
created: 2026-09-13
updated: 2026-09-18
description: "Consolida decisões abertas agrupadas num ÚNICO conceito global coerente, em forma de prosa, com base em todas as variantes recomendadas. Mostra como os subsistemas se articulam concretamente após a implementação, em vez de obrigar o usuário a responder dezenas de perguntas isoladas. O usuário aceita o quadro como um todo ou dá correções direcionadas, que são traduzidas automaticamente em decisões individuais e reescritas no registro através da Fase 4 de decision-briefing. Use esta skill em \"como fica o todo se concordarmos com tudo\", \"desenhe para mim o quadro geral\", \"conceito global das decisões\", \"decision draw\", /decision-draw, \"como os sistemas se articulam\". NÃO use quando alternativas por ponto individual devem ser discutidas — isso é feito por decision-briefing; NÃO para o grafo de dependências — isso é feito por decision-path; NÃO para blocos individuais estruturados com opções e prós/contras (também para grupos estreitamente relacionados) — isso é feito por decision-shot; NÃO para a derivação de uma única decisão — isso é feito por decide."
visibility: public
language: pt
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [entscheidung, konzeptbild, gesamtabnahme, buendelung, zusammenspiel, ruecktransfer, workflow]
status: active
dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, decision-path, decision-shot, decision-avatar]
provenance:
  origin: "custom"
  decision_ref: "T-20260913-107991667 (Ticket-Master, Nutzerauftrag 2026-09-13)"
translated_from_sha256: da661fa325502ab0dfae6d6655d70650457d6ac1ff27ca5f0ce6289c375ef2c8
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.497907+00:00"
---
<img src="banner.png" width="100%" alt="decision-draw banner">

# decision-draw — Quadro geral e aceitação de decisões agrupadas

> Quando cinco ou dez decisões estão pendentes, é fácil perder de vista o sistema
> que está surgindo no emaranhado de opções. decision-draw não descreve as
> alternativas, mas o todo funcionando: como os sistemas trabalham juntos se todas
> as recomendações forem aceitas? O usuário aceita o quadro como um todo ou faz
> correções direcionadas.

---

## Quando usar

- Várias decisões relacionadas (de [decision-briefing](../decision-briefing/SKILL.md) ou de um modelo de decisão) não devem ser tratadas como um catálogo arrastado de perguntas isoladas.
- O usuário quer ver, antes da deliberação, como os componentes realmente interagem no dia a dia após a implementação.
- Do grafo de dependências ([decision-path](../decision-path/SKILL.md)) foi identificado um conjunto de decisões fortemente acopladas que pode ser aceito como unidade funcional.
- Palavras-gatilho: `/decision-draw`, "como fica o todo se concordarmos com tudo", "desenhe para mim o quadro geral", "conceito global das decisões", "decision draw", "como os sistemas se articulam depois", "imagem para a aceitação geral".
- **Não** usar:
  - Quando o usuário quer ponderar individualmente as opções de cada pergunta e escolher por letra (A/B/C) — isso é feito por [decision-briefing](../decision-briefing/SKILL.md).
  - Para a pura análise de causalidade e bloqueios no terminal — isso é feito por [decision-path](../decision-path/SKILL.md).
  - Para a ponderação isolada de opções em blocos individuais de 5 partes (contexto, prós/contras por opção, recomendação) para perguntas individuais ou grupos estreitamente relacionados — isso é feito por [decision-shot](../decision-shot/SKILL.md).
  - Para a elaboração metódica de uma única questão fundamental em aberto — isso é feito por [decide](../decide/SKILL.md).

---

## Delimitação na família de decisões

| Skill | UX e foco | Postura em relação às opções | Forma de aceitação |
|---|---|---|---|
| `decision-briefing` | **Decompõe** em perguntas individuais | Mostra todas as opções A/B/C/D | Códigos por letra (`1A 2C 3B`) |
| `decision-path` | **Estrutura** causalidades | Avalia opções no grafo | Diagnóstico no terminal (ASCII) |
| `decision-draw` | **Imagem-alvo coerente** (agrupa decisões interligadas) | Descreve **apenas a variante recomendada** (alternativas linkadas) | Aceitação geral ou frase de correção |
| `decision-shot` | **Blocos individuais estruturados** (para perguntas individuais ou grupos estreitos) | Mostra opções com 2–4 prós/contras | Decisão executiva / aceitação individual |
| `decide` | **Elabora** o caso individual | Matriz de avaliação (critérios) | Recomendação analítica |

> **Regra central:**
> `decision-draw` descreve **exclusivamente a variante recomendada**. As alternativas descartadas não desapareceram — estão documentadas em [decision-briefing](../decision-briefing/SKILL.md), [decision-shot](../decision-shot/SKILL.md) ou nos tickets vinculados, e são linkadas no cabeçalho. Um draw sem essa referência tiraria do usuário a escolha, em vez de facilitá-la.

---

## Regra de estilo obrigatória: textos ao usuário sem códigos e números

> **Instrução canônica do usuário (feedback 2026-09-13 / Ticket T-20260913-883789445):**
> *„Die decision draws sind mir zu technisch, das muss ohne Nummer sein, die kennst du im Hintergrund oder nutzt du zur Texterstellung [...].“*

1. **Nenhum código técnico no texto visível ao usuário:**
   No texto corrido visível ao ser humano (pacote, conceito, articulação, implementação, consulta) **não** aparecem códigos internos (como `BH-A`, `MD-A`, `HA-A`, `PRA`), números de ticket (`T-2026...`), números D (`D-2026...`), caminhos relativos, hashes Git ou valores de medição.
2. **2–4 frases de linguagem cotidiana, em primeira pessoa, por item:**
   Cada item do pacote é formulado segundo a tríade:
   - *Situação:* Qual é a situação atual de partida?
   - *„Eu faço …“:* O que planejo concretamente / qual é minha recomendação de ação?
   - *Recuo:* O que acontece se isso falhar, ou o que o usuário decide depois?
   *(Exemplo: „O Hermes só suporta tarefas em inglês. Eu reporto isso ao Hermes como issue e, para nós, construo um workaround. No momento há sessões antigas inutilizáveis. Tento torná-las utilizáveis de novo. Se não funcionar, te entrego uma amostra aleatória de 10 sessões e a resumo — assim você pode decidir se vale a pena resgatá-las.“)*
3. **Títulos em linguagem clara para orientação:**
   Cada item recebe um título compreensível em alemão (por ex. *„Modell-Backend als eigenes Herzstück“*, *„Sichere Deploy-Schlüssel auf dem Mac“*). O usuário interage por esse título ou dá uma aceitação geral.
4. **Atribuição técnica exclusivamente no anexo:**
   A correspondência entre título em linguagem clara, código interno, ID de ticket e estado do registro ocorre **exclusivamente em uma tabela de anexo final** no fim do documento. Só ali atuam os analisadores automatizados e os gravadores de volta no registro.

---

## Estrutura obrigatória (oito partes)

Um `decision-draw` completo segue sem exceção esta estrutura:

### 1. Pacote e escopo (em linguagem clara)
Visão geral dos itens agrupados em linguagem cotidiana (primeira pessoa, 2–4 frases por ponto, sem IDs/códigos no texto).

### 2. Conceito
O estado-alvo pretendido como texto corrido coerente, em prosa:
- Que paisagem de sistemas ou que fluxo de trabalho surge se todas as recomendações forem implementadas exatamente assim?
- Nenhuma contraposição de opções, nenhum lado a lado no subjuntivo („poderia-se também“).
- Indicativo claro e preciso: assim o sistema funciona no estado-alvo.

### 3. Articulação
O núcleo funcional da skill:
- Como as partes decididas se encaixam na prática **depois** da implementação?
- Apresentação preferencialmente ao longo de um fluxo concreto de ponta a ponta, e não apenas uma lista de componentes.
- Torna tangíveis fluxos de dados, interfaces e responsabilidades.

### 4. Implementação
A sequência concreta de realização:
- O que acontece de fato na prática?
- Assume diretamente a lógica de arestas e dependências de [decision-path](../decision-path/SKILL.md).
- Frentes de trabalho independentes são apresentadas honestamente como paralelas (sem inventar cadeias causais artificiais; um pacote pode consistir em várias frentes paralelas). Sequências são afirmadas apenas onde existem dependências ou prazos comprovados.
- Nomeia gates, passos de migração e verificações.

### 5. O que este quadro não cobre
Proteção contra falsa completude:
- Quais questões marginais, pontos em aberto ou confianças 🔴 ficam deliberadamente de fora?
- Onde estão os limites de interface com os sistemas vizinhos?
- Um quadro que oculta suas bordas produz falsa segurança.

### 6. Aceitação
A interação com o usuário:
- O usuário examina o quadro como um todo.
- Possibilidade de resposta 1: **Aceitação geral explícita** („Passt so“, „Abnahme“, „So umsetzen“). Só nesse caso todos os itens do pacote são registrados como decididos.
- Possibilidade de resposta 2: **Correção por título em linguagem clara ou em linguagem cotidiana** („Beim Mac-Deploy lieber kein Auto-Restart“, „VersicherungsManager erst mal vertagen“). Leva à decomposição em decisões individuais; todos os itens não corrigidos permanecem em aberto.

### 7. Transferência de retorno
A tradução sistemática das correções do usuário em deliberações individuais:
- **Nenhuma contabilização automática:** Só com aceitação geral explícita os itens inalterados são lançados. Uma correção parcial **não** é aceitação geral!
- **Isolamento em correções:** Chegando uma correção, ela é decomposta em decisões individuais; todos os demais itens do pacote permanecem estritamente **em aberto** (no registro de origem / no modelo), até que o usuário aceite o quadro ajustado como um todo ou confirme individualmente os itens restantes.
- **Tabela obrigatória da transferência de retorno:** Cada retorno de correção gera obrigatoriamente uma tabela de avaliação estruturada com quatro colunas (correção original, códigos afetados, status de efeito dominó, ambiguidades em aberto).
- **Caminho de escrita exclusivamente pela Fase 4:** `decision-draw` **não** possui caminho próprio de escrita no registro. O lançamento ocorre **exclusivamente** pelo procedimento padronizado da Fase 4 de [decision-briefing](../decision-briefing/SKILL.md).

### 8. Anexo: tabela técnica de referência (somente para lançamento e auditoria)
Tabela compacta no fim do documento com:
`| Klartext-Titel | Internes Kürzel / ID | Ticket-Referenz | Unterstellte Empfehlung | Konfidenz | Link / Details |`

---

## Exemplo (trecho piloto: Ticket-Master 2026-09-13 — BACH e conjunto de sistemas)

```markdown
# DECISION-DRAW: BACH-Kernverbund & Betriebsintegrität

## 1. Bündel und Umfang

- **Modell-Backend als eigenes Herzstück:** Die Modellzuteilung ist aktuell eng mit dem Monolithen verzahnt. Ich lagere das Backend als eigenständiges Kernmodul aus, damit Rechte und Budgets unabhängig geprüft werden. Scheitert ein externer Dienst, schaltet das System automatisch auf das lokale Reservemodell zurück.
- **Sichere Deploy-Schlüssel auf dem Mac:** Auf dem Mac laufen Dauerprozesse, die bei harten Updates unsauber abbrechen können. Ich richte einen lesenden Schlüssel und ein Meldeskript ein, das Aktualisierungen anzeigt, ohne laufende Dienste abzuschießen. Sollte ein Dienst dennoch hängen, meldet der Watcher das direkt an die Betriebsübersicht.
- **Einheitliche Konfigurations-Sollwerte:** Die beiden Hauptrechner nutzen teilweise unterschiedliche Spracheinstellungen. Ich gleiche die Konfigurationen über das gemeinsame Sync-Verzeichnis an, lasse dem Laptop aber ausreichend Spielraum für mobile Tests.
- **Feste Zeitzone im VersicherungsManager:** Datumsberechnungen bei Fristen hängen bisher vom Betriebssystem ab. Ich verankere eine feste Zeitzone in den Anwendungseinstellungen, damit Fristen überall auf die Minute genau übereinstimmen.
- **Öffentliche Bereitstellung der USMC-Dokumentation:** Die Modul-Dokumentation ist im Webauftritt noch als privat markiert und löst Prüfwarnungen aus. Ich korrigiere die Sichtbarkeit auf öffentlich, damit der nächtliche Seiten-Bau ohne Fehler durchläuft.

---

## 2. Konzept

Wir etablieren ein sauberes, entkoppeltes Multi-Host-System, bei dem das Modell-Backend
als eigenständiges Kernmodul `agents-heart` betrieben wird. Rechte und Budgets liegen
strukturiert in einer SQLite-Datenbank, während Zuteilungsentscheidungen zweistufig
fallen: BACH ermittelt fachlich fundiert die Kandidatenmenge, clutch wählt darin
preis- und kapazitätsoptimal das finale Modell.

Auf dem Mac Studio laufen die 24/7-Dienste geschützt und stabil über einen read-only
Deploy-Key; Updates ziehen automatisch ein, benachrichtigen den Operator bei laufenden
Diensten aber sanft, statt Hintergrundprozesse hart abzuschießen. Konfigurationen
dürfen dort bewusst hostspezifisch auf Leistung abgestimmt sein, während app-weite
Einstellungen (wie Zeitzonen im VersicherungsManager nach dem bewährten routinika-Muster)
deterministisch fest verdrahtet sind. USMC bleibt der kanonische öffentliche
Memory-Baustein und behält seinen festen Platz im Webauftritt.

---

## 3. Zusammenspiel

Die fünf Posten bilden keine serielle Kausalkette, sondern stellen modular entkoppelte Bausteine der täglichen Betriebsintegrität dar, die im Gesamtsystem parallel ineinandergreifen:

- **Kernarchitektur & Modell-Routing (`BH-A`):** Das Modul `agents-heart` entkoppelt die Modellzuteilung. Trifft eine Aufgabe ein, ermittelt BACH fachbezogen die Kandidatenmenge und clutch wählt kosten- und kapazitätsoptimal das Modell.
- **Host-Konfiguration & Deploy-Integrität (`CF-A`, `MD-A`):** Während auf dem Laptop und der Workstation konsistente Reasoning-Stufen gelten (`CF-A`; hostabhängige Modelle bleiben transparent), betreibt der Mac Studio seine persistenten Hintergrundprozesse unter validierten Einstellungen. Bei Aktualisierungen zieht der Mac den Code via Read-only Deploy-Key (`MD-A`); der GUI-Server startet neu, während langlebige 24/7-Dienste den Update-Bedarf sanft an das Dashboard melden.
- **Domänen-Persistenz & Fristen (`VM-A`):** Applikationen wie der VersicherungsManager schreiben Fristen und Deadlines gegen eine app-weite `settings`-Tabelle nach routinika-Muster. Zeitrechnungen und Deadline-Projektionen operieren über alle Profile hinweg deterministisch auf derselben IANA-Zeitzone.
- **Öffentlicher Auftritt (`PD-A`):** Der nächtliche Seiten-Builder validiert den Zustand der Repositories. USMC wird mit korrigierter `public`-Deklaration fehlerfrei publiziert, ohne Warnungen in den Sicherheits-Gates auszulösen.

---

## 4. Umsetzung

Da die Vorlage für diese fünf Posten im Abhängigkeitsgraphen ([decision-path](../decision-path/SKILL.md)) keine serielle Kette vorgibt, erfolgt die Umsetzung ehrlich in vier voneinander unabhängigen, parallelen Arbeitssträngen (Ausweg a: parallele Stränge statt erfundener Kausalität). Eine sequenzielle Reihenfolge gilt nur dort, wo externe Fristen oder interne Schritte belegt sind:

- **Strang A (Termingebunden — Frist 2026-09-14):**
  1. USMC-Metadaten auf `public` nachziehen (`PD-A`); Draft-PR #2 verwerfen. Duldet wegen des nächtlichen Builder-Laufs keinen Aufschub, ist technisch jedoch von allen anderen Strängen unabhängig.
- **Strang B (Host-Konfiguration & Mac-Deploy — parallel ausführbar):**
  1. B1: Sollwerte in `.SYNC` festschreiben (`CF-A`), Reasoning-Stufe `high` für beide Hosts synchronisieren.
  2. B2 (unabhängig von B1): Read-only Deploy-Key auf Mac Studio hinterlegen und Pull-and-Report-Skript einrichten (`MD-A`).
- **Strang C (Domänen-Datenbank — parallel ausführbar):**
  1. Migration der app-weiten `settings`-Tabelle im VersicherungsManager nach routinika-Vorbild implementieren (`VM-A`), um die saubere Basis für den nachgelagerten Publisher-Bau zu schaffen.
- **Strang D (Architektur-Herauslösung — interner Mehrstufenplan):**
  1. D1: SQLite-Schema für Rollen und Budgets in `agents-heart` anlegen (`BH-A` E1).
  2. D2: Backend-Katalog als Python-Modul ausgründen (`BH-A` E3) und clutch-Seam für Zuteilung binden (`BH-A` E2).
  3. D3: Modul `agents-heart` final herauslösen und anbinden (`BH-A` E5, E6).

---

## 5. Was dieses Bild nicht abdeckt

- **Task-Claiming Race Condition:** Der Integritätsfehler bei doppeltem Task-Claim läuft
  in einem separaten Hotfix-Ticket und ist nicht Teil dieser Freigabe.
- **Cockpit-Frontend:** Das Monitoring-Cockpit (`BH-A` E4) wird bewusst noch nicht gebaut,
  solange das Backend nicht produktiv meldet.
- **Sichtbarkeitsschaltung nach außen:** Reine Bereitstellung von Code schaltet keine
  neuen Repos public; die finale Freigabe bleibt dem Nutzer vorbehalten.

---

## 6. Abnahme

Du kannst diesen Systemverbund als Ganzes abnehmen oder in Alltagssprache korrigieren:

- **Ausdrückliche Gesamtabnahme:** „Passt so, genau so umsetzen.“ (Nur dies führt zur Verbuchung aller Posten).
- **Korrektur-Beispiele:**
  - *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“* (Mehrfachtreffer)
  - *„BH-A E5 lieber ocean-heart nennen statt agents-heart.“*
  - *„VM-A erst mal vertagen, der Publisher hat noch Zeit.“*

---

## 7. Rücktransfer

Wird das Gesamtbild abgenommen oder korrigiert, übersetzt der Skill die Rückmeldung:

### Fall A: Ausdrückliche Gesamtabnahme
Nimmt der Nutzer das Gesamtbild ausdrücklich als Ganzes ab (z. B. *„Passt so, genau so umsetzen“*):
- Alle fünf Posten (`BH-A: 1A/2A/3A/4B/5A/6A`, `MD-A: A1`, `CF-A: 1C/2B/3B`, `VM-A: A`, `PD-A: A`) werden als GETROFFEN an [decision-briefing](../decision-briefing/SKILL.md) Phase 4 übergeben.
- Phase 4 übernimmt die Eintragung ins Register `DECIDED-AND-DONE.md` und aktualisiert die fünf Quelltickets.

### Fall B: Teilkorrektur mit Mehrfachtreffer
Gibt der Nutzer eine inhaltliche Korrektur ein, z. B.:
> *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“*

**1. Strukturierte Rücktransfer-Tabelle:**

| Originalkorrektur (Wortlaut des Nutzers) | Betroffene Kürzel | Domino-Status (welche abhängigen Knoten kippen dadurch) | Offene Mehrdeutigkeiten |
|---|---|---|---|
| *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“* | `MD-A`, `CF-A` *(Mehrfachtreffer: 1 Aussage bewegt 2 Posten)* | **`MD-A`:** Kippt von A1 auf A2. Erfordert SSH-Write-Key auf Mac Studio, Push-Rechte im GitHub-Repo `bach` und Sicherheitsprüfung des LaunchAgents.<br>**`CF-A`:** Gruppe 1 kippt von C auf A (Laptop-Claude-Desktop wird restriktiver). Gruppe 2 kippt von B auf A (`codex.model` wird starr angeglichen). Gruppe 3 bleibt B (`high`), da bereits synchron. | **`CF-A` Gruppe 1:** Nutzer verlangt Angleichung an Workstation (1=A) — Rückfrage nötig, ob die bisher bewusste Freizügigkeit auf dem Laptop wirklich entzogen werden soll.<br>**`MD-A`:** Unklar, ob Write-Key für alle Repos oder nur für `bach` gelten soll. |

**2. Status der unberührten Posten (Schutz vor ungefragtem Mitbuchen):**
- Die unveränderten Posten `BH-A`, `VM-A` und `PD-A` werden **nicht** gebucht!
- Sie verbleiben im Status **OFFEN** (`PENDING`) in der Vorlage bzw. im Register `TO-DECIDE-USER.txt`.
- Eine Teilkorrektur ist **keine** Gesamtabnahme. Erst wenn das nach Korrektur aktualisierte Gesamtbild vom Nutzer als Ganzes abgenommen wird oder die verbleibenden Punkte einzeln bestätigt werden, dürfen sie verbucht werden.

**3. Buchungsweg:**
- `decision-draw` besitzt keinen eigenen Schreibmechanismus.
- Übergeben wird an **[decision-briefing](../decision-briefing/SKILL.md) Phase 4** nur, was die Tabelle als eindeutig ausweist: `CF-A` Gruppe 2 = A und Gruppe 3 = B.
- **Nicht** übergeben werden `MD-A` und `CF-A` Gruppe 1 — für beide steht in der Spalte *Offene Mehrdeutigkeiten* eine Rückfrage. Eine Mehrdeutigkeit, die man vor der Buchung klären wollte, darf man nicht in derselben Runde als geklärt verbuchen.
- Phase 4 trägt die eindeutigen Teile mit Begründung in Ticket `T-20260913-947070291.txt` ein und aktualisiert `DECIDED-AND-DONE.md`. Ticket `T-20260913-799464688.txt` (`MD-A`) bleibt offen, bis die Rückfrage beantwortet ist.

---

## 8. Anhang: Technische Referenztabelle (nur für Buchung & Audit)

| Klartext-Titel | Internes Kürzel | Ticket / Quelle | Unterstellte Empfehlung | Konfidenz | Link / Details |
|---|---|---|---|---|---|
| Modell-Backend als eigenes Herzstück | `BH-A` | `T-20260913-896336887` | 1A / 2A / 3A / 4B / 5A / 6A | 🟢 | `docs/MODELL-BACKEND-KONZEPT_2026-09-13.md` |
| Sichere Deploy-Schlüssel auf dem Mac | `MD-A` | `T-20260913-799464688` | A1 + Skript (nur Melden für 24/7) | 🟢 | Ticket `T-20260913-799464688.txt` |
| Einheitliche Konfigurations-Sollwerte | `CF-A` | `T-20260913-947070291` | 1C (begründet) / 2B (hostabh.) / 3B (high) | 🟢 / 🟡 | Ticket `T-20260913-947070291.<HOST>.txt` |
| Feste Zeitzone im VersicherungsManager | `VM-A` | `T-20260906-496406575` | A (app-weite settings wie routinika) | 🟢 | Ticket `T-20260906-496406575.<HOST>.txt` |
| Öffentliche Bereitstellung der USMC-Dokumentation | `PD-A` | `T-20260913-609930207` | A (auf public nachziehen, Status quo) | 🟢 | Ticket `T-20260913-609930207.txt` |
```

---

## Regras para a prática

1. **Nenhum subjuntivo no conceito:** Descreva o sistema global como se já estivesse realizado. O usuário quer clareza sobre o resultado, não eventualidades teóricas.
2. **Causalidade antes de cronologia:** A ordem na seção *Implementação* segue os níveis do grafo de dependências de [decision-path](../decision-path/SKILL.md). Fluxos independentes são apresentados honestamente como paralelos e não são torcidos numa cadeia causal artificial.
3. **Verificação explícita de efeito dominó na transferência de retorno:** Uma correção do usuário nunca pode ser lançada isoladamente sem verificar se nós dependentes no grafo são invalidados ou influenciados.
4. **Nenhuma contabilização automática em correções parciais:** Só com aceitação geral explícita são lançados os itens inalterados. Em cada correção parcial, todos os itens não afetados permanecem estritamente em aberto, até que o quadro geral seja novamente liberado ou os itens confirmados individualmente.
5. **Caminho de escrita exclusivamente pela Fase 4:** `decision-draw` não possui caminho próprio de escrita no registro. Os lançamentos ocorrem sem exceção por meio da Fase 4 de [decision-briefing](../decision-briefing/SKILL.md).
6. **Respeitar os contratos do registro:** Os lançamentos sempre seguem as regras do registro de decisões (sem renumeração de IDs, códigos de lançamento inequívocos, destino canônico `DECIDED-AND-DONE.md`).
7. **Textos ao usuário sem números e códigos técnicos:** No texto visível ao ser humano não há IDs, códigos, caminhos ou números de ticket. Cada item é formulado em primeira pessoa compreensível; todas as identificações vão para a tabela de anexo.

---

## Proveniência da sessão

Quando um decision-draw é salvo como documento conceitual permanente, termina com:

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

- Prioridade de fontes: indicação explícita de runtime/CLI, depois ambiente ou hook autoritativo do provedor, caso contrário `unbekannt`.
- Subagentes herdam o ID de sessão da sessão-mãe.
- Modelos puros de chat não recebem carimbo.

---

## Changelog

### 1.1.0 (2026-09-18)
- Regra de estilo para textos de decisão voltados ao usuário ancorada (T-20260913-883789445, instrução do usuário de 2026-09-13):
  - Sem códigos técnicos, números de ticket/D, caminhos ou valores de medição no texto visível ao usuário.
  - 2–4 frases de linguagem cotidiana em primeira pessoa (situação, „Eu faço …“, recuo) por item.
  - Títulos claros e descritivos para identificação e aceitação.
  - Atribuição técnica (códigos, ID de ticket, estado do registro) estritamente transferida para a tabela de anexo final (seção 8).

### 1.0.1 (2026-09-13)
- Revisão posterior:
  - Contrato de transferência de retorno endurecido: nenhuma contabilização automática em correções parciais; itens não afetados permanecem estritamente em aberto até a aceitação geral.
  - Tabela obrigatória da transferência de retorno com 4 colunas (correção original, códigos afetados, status de efeito dominó, ambiguidades em aberto) introduzida.
  - Correspondências múltiplas demonstradas no exemplo (uma correção do usuário move simultaneamente `MD-A` e `CF-A`).
  - Caminho de escrita exclusivo pela Fase 4 de `decision-briefing` ancorado no contrato e no exemplo.
  - Falsa premissa de cadeia causal no exemplo corrigida: itens independentes apresentados honestamente como quatro frentes paralelas (alternativa a).
  - Delimitação em relação a `decision-shot` precisada pelo formato de saída (blocos individuais estruturados com prós/contras vs. imagem-alvo coerente com aceitação geral).

### 1.0.0 (2026-09-13)
- Versão inicial com base na solicitação do usuário T-20260913-107991667.
- Estrutura obrigatória de sete partes (pacote, conceito, articulação, implementação, limites, aceitação, transferência de retorno).
- Lógica de agrupamento com base em `decision-path` e ponte de reescrita para `decision-briefing` Fase 4.
