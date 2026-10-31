---
name: decision-briefing
version: 1.2.0
type: skill
author: Lukas Geiger
created: 2026-06-13
updated: 2026-09-18
description: "Use sempre que várias decisões estiverem pendentes ou tiverem se acumulado — seja dentro de um tema, projeto ou documento, seja ao longo de uma sessão: inventariá-las, apresentar um briefing numerado com opções A/B/C/D e uma recomendação marcada, aceitar respostas por letras (inclusive em lotes), registrar os resultados e reescrevê-los nos documentos de origem."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [entscheidung, briefing, batch, decision-session, priorisierung, workflow]
language: pt
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/_experts/decision-briefing/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-13', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 5eb5eb50aed074ac83c743e1ed9d5f9cf5fc817c0c46bd1c9aae9992cd9870d0
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.485190+00:00"
---
<img src="banner.png" width="100%" alt="decision-briefing banner">

# Decision-Briefing — Trabalhar de forma estruturada com muitas decisões de um tema

> De uma montanha de decisões em aberto surge um briefing numerado com recomendações, que o usuário pode responder de forma rápida por letras — individualmente ou em lote.

---

## Quando usar?

**Sempre que houver várias decisões pendentes** — independentemente do tema. Situações típicas:

- Em uma área/tema se acumularam muitas decisões em aberto
- Um documento (plano, lista de TODOs, conceito) contém vários pontos não decididos
- Na conversa surgiram, uma após a outra, várias perguntas de decisão
- O agente tem várias perguntas de esclarecimento para o usuário — em vez de fazê-las uma a uma, reúne-as em um briefing
- O usuário quer "dar conta" dos pontos em aberto de forma rápida e fundamentada

**Palavras-gatilho:** decisões em aberto, sessão de decisões, briefing, resolver pendências, repassar, decidimos tudo isso agora

**Delimitação:** [decide](../decide/SKILL.md) fornece frameworks para UMA pergunta. `decision-briefing` coordena o trabalho com VÁRIAS decisões de um tema — e recorre a `decide` em casos individuais complexos. Se uma decisão já foi tomada/analisada e deve ser apenas repassada em forma executiva curta (prós/contras, pontos de discussão, recomendação, link para a análise completa), a apresentação fica a cargo de [decision-shot](../decision-shot/SKILL.md) — não é uma habilidade concorrente, mas o formato de saída posterior.

---

## UX central

O núcleo é o formato de briefing. Cada decisão é apresentada de modo que a resposta possa ser rápida e sem carga cognitiva desnecessária:

- **Título em linguagem clara e descritiva** para cada ponto (ex.: *"Suporte ao idioma do Hermes"*, *"Recuperação de sessões de trabalho antigas"*)
- **Linguagem cotidiana em primeira pessoa (tríade):**
  1. *Situação:* qual é a situação / o problema?
  2. *Eu faço ...:* o que pretendo ou recomendo fazer concretamente?
  3. *Plano B:* o que acontece em caso de falha ou o que o usuário decide depois?
- **Sem códigos técnicos no texto da pergunta:** sem números de tickets (`T-...`), identificadores D, hashes do Git ou caminhos de arquivos no texto visível ao usuário.
- **Opções como letras** A/B/C/D (2–4 opções, formuladas de forma clara e compreensível)
- **Recomendação destacada** em primeira pessoa (ex.: `→ Ich empfehle Option A, weil ich damit ...`)
- **Tabela de referência técnica apenas no anexo:** números estáveis (`[E01]`, `[E02]`), IDs de tickets e registros de destino são mantidos no fim, em uma tabela compacta.

**Formatos de resposta do usuário:**

```
Per Buchstabe:   "E01: A"  oder  "1A"
Batch:           "1A 2C 3B"
Per Klartext:    "Bei der Hermes-Sprachunterstützung Option A"
Vertiefen:       "E02: mehr Info"  oder  "2?"
Vertagen:        "E03: später"
Gesamtabnahme:   "Passt so, alle Empfehlungen umsetzen"
```

---

## Fluxo de trabalho (4 fases)

```
Thema + vorliegende Entscheidungen
     |
     v
Phase 1: ERFASSEN & INVENTARISIEREN
     |
     v
Phase 2: BRIEFING AUFBEREITEN
     |
     v
Phase 3: DECISION-SESSION
     |
     v
Phase 4: PROTOKOLL & RÜCKSCHREIBEN
```

### Fase 1: Levantar e inventariar

Fontes: o que o usuário menciona, um documento disponível ou o contexto da conversa. Nenhuma varredura de todo o sistema — apenas o que estiver disponível.

1. Listar todas as decisões em aberto (1 linha cada: título curto)
2. Identificar e unir **duplicatas** (mesma pergunta formulada várias vezes)
3. Marcar **dependências** ("E04 depende de E01")
4. Definir a **ordem**: bloqueadores primeiro (decisões das quais outras dependem), depois por urgência
5. Mostrar brevemente a lista ao usuário para confirmação ("Tenho todas? Falta algo?")

### Fase 2: Preparar o briefing

Para cada decisão:

```
[E01] <Sprechender Klartext-Titel>
  Lage: <1 Satz: Was ist die Situation?>
  Handlung: <1-2 Sätze in Ich-Form: Was schlage ich vor zu tun?>
  Rückfall: <1 Satz: Was passiert bei Fehlschlag oder als nächster Schritt?>
  A) <Option in Alltagssprache>
  B) <Option in Alltagssprache>
  → Meine Empfehlung: A — <Begründung in Ich-Form>
```

Ao final do briefing:
```
### Technische Referenztabelle (nur für Buchung & Audit)
| Nummer | Klartext-Titel | Empfehlung | Ticket-ID / D-Nummer | Quelle / Pfad |
|---|---|---|---|---|
| E01 | Hermes-Sprachunterstützung | A | T-20260913-989062143 | hermes-agent |
```

Regras para boas opções:

- As opções devem ser mutuamente exclusivas e cobrir o espectro
- Se necessário, incluir uma opção "manter o status quo" ou "adiar"
- A recomendação deve ser justificada de forma transparente — nunca de maneira velada ou sugestiva
- Havendo base factual incerta: esclarecer antes (ou marcar como pergunta em aberto), não adivinhar

### Fase 3: Sessão de decisão

1. Apresentar o briefing — individualmente (uma decisão por mensagem) ou em lote (todas de uma vez); com mais de 5 decisões, em blocos de 3–5
2. Receber e confirmar as respostas por letras
3. Em caso de resposta "mais informações": aprofundar a decisão (caixa de ferramentas de métodos abaixo)
4. Em casos individuais complexos (muitos critérios, grande alcance): escalar para a habilidade [decide](../decide/SKILL.md) (Weighted Scoring, Scenario Analysis)
5. Decisões adiadas devem ser explicitamente mantidas como abertas — não deixá-las cair em silêncio

### Fase 4: Registro e reescrita

1. **Criar tabela de resultados**:

```
| Nr.  | Entscheidung        | Gewählt | Status   |
|------|---------------------|----------|----------|
| E01  | <Kurztitel>         | A        | getroffen|
| E02  | <Kurztitel>         | C        | getroffen|
| E03  | <Kurztitel>         | —        | vertagt  |
```

2. Inserir as decisões tomadas nos **documentos de origem/arquivos de TODO** — no local em que a pergunta aberta aparece, por exemplo:

```
ENTSCHEIDUNG: <Frage>
  → GETROFFEN 2026-06-13: Option A (<Kurzfassung>)
  → Nächste Aktion: <falls die Entscheidung eine Folgeaktion impliziert>
```

3. **Manter explicitamente como aberto o que foi adiado** (no documento de origem ou na lista de TODOs), para que reapareça no próximo briefing

---

## Exemplo de briefing (fictício)

Tema: relançamento do site de uma associação — 3 decisões em aberto do plano de projeto.

```
[E01] Welches System für die neue Website?
  Kontext: Aktuelle Seite ist handgepflegtes HTML; 2 Personen sollen künftig Inhalte pflegen.
  A) Static-Site-Generator (schnell, sicher, Pflege via Git)
  B) Klassisches CMS mit Admin-Oberfläche
  C) Website-Baukasten (gehostet)
  → Empfehlung: B — zwei nicht-technische Redakteure brauchen eine Oberfläche, kein Git.

[E02] Wie wird gehostet?
  Kontext: Budget ~10 EUR/Monat, kein eigener Admin im Verein.
  A) Shared Hosting beim bestehenden Anbieter
  B) Eigener kleiner VPS
  C) Managed Hosting passend zum gewählten System
  → Empfehlung: C — am wenigsten Wartungsaufwand ohne Admin; Konsequenz: hängt von E01 ab.

[E03] Wann geht die neue Seite live?
  Kontext: Inhalte sind zu 60% migriert; Vereinsjubiläum in 3 Monaten.
  A) Sofort als Soft-Launch (Rest nachziehen)
  B) Nach vollständiger Inhaltsmigration
  C) Zum Jubilaeum als Stichtag
  → Empfehlung: A — umkehrbar und liefert früh Feedback; finale Inhalte folgen.
```

O usuário responde em lote: **"1B 2C 3A"** → tabela de resultados; em seguida, as três decisões são registradas como TOMADAS no plano de projeto.

---

## Caixa de ferramentas de métodos (para "mais informações" e aprofundamento)

| Método | Quando | Descrição breve |
|---------|------|------------------|
| **Matriz de prós/contras** | 2–3 opções, comparação rápida | Avaliar todas as opções lado a lado |
| **Análise de utilidade** | Vários critérios | Critérios ponderados, pontos por opção (quantitativo quando possível) |
| **Pensamento de segunda ordem** | Alcance incerto | Quais são as consequências das consequências? |
| **Pré-mortem** | Decisão arriscada | "Deu errado — por quê?" Encontrar fragilidades antecipadamente |
| **Método 10/10/10** | Distorção emocional/temporal | Como a decisão se apresenta em 10 minutos / 10 meses / 10 anos? |

---

## Princípios de trabalho

- **Não impor decisões:** fornecer informações, justificar a recomendação de forma transparente — quem decide é o usuário
- **Detecção de vieses:** apontar erros de raciocínio quando se tornarem visíveis (viés de confirmação, falácia do custo afundado)
- **Considerar reversibilidade:** decidir rapidamente as decisões reversíveis, tratar as definitivas com mais profundidade
- **Considerar pressão de tempo:** decisões rápidas exigem métodos mais simples — nem toda pergunta merece uma análise de utilidade

### Proveniência da sessão em artefatos gerados

Se esta habilidade criar um briefing, relatório, handoff ou recibo novo e importante,
armazenado de forma duradoura, o artefato termina com exatamente uma linha:

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

- Prioridade das fontes: indicação explícita de runtime/CLI, depois ambiente ou hook autoritativo do provedor; caso contrário, `unbekannt`. Nunca adivinhar valores.
- Um subagente usa o ID da sessão de sua sessão-mãe.
- Conversas rotineiras, documentos de origem consultados, políticas, `CLAUDE.md`, READMEs e decisões apenas reescritas não recebem carimbo genérico. Arquivos antigos não são carimbados às cegas.

---

## Delimitação e sinergias

| Função | `decide` | `decision-briefing` |
|---|---|---|
| Estruturar uma decisão individual com um framework | ✓ | — |
| Inventariar muitas decisões de um tema | — | ✓ |
| Briefing numerado com opções A/B/C | — | ✓ |
| Respostas em lote ("1A 2C 3B") | — | ✓ |
| Reescrita nos documentos de origem | — | ✓ |
| Repassar uma análise pronta de uma pergunta única como forma curta | — | — (ver [decision-shot](../decision-shot/SKILL.md)) |

**Sinergia:** em casos individuais complexos dentro de uma sessão, `decision-briefing` aplica os frameworks de `decide` (Weighted Scoring, Scenario Analysis). Para o processo de pensamento maior que vem antes (análise → ideias → decisão), ver [structured-thinking](../structured-thinking/SKILL.md).

---

## Changelog

### 1.2.0 (2026-09-18)
- Regra de estilo para textos de decisão compreensíveis ancorada (T-20260913-883789445, instrução do usuário de 2026-09-13):
  - Sem números de tickets crípticos, identificadores D ou caminhos no texto visível da pergunta.
  - Tríade em primeira pessoa (situação, "Eu faço …", plano B) para contexto e recomendação.
  - Título descritivo em linguagem clara para cada ponto de decisão; formatos de resposta ampliados com linguagem clara e aceitação geral.
  - Mapeamento técnico (identificadores, IDs de tickets, caminhos de registro) transferido para a tabela de anexo ao fim do briefing.

### 1.1.0 (2026-09-09)
- P-018 acrescenta proveniência da sessão para briefings, relatórios, handoffs e recibos novos e importantes; prioridade das fontes, sessão-mãe para subagentes e exclusões restritas estão definidas.

### 1.0.0 (2026-06-13)
- Portado do especialista BACH `decision-briefing` v1.0.0; componente de varredura (scanner.py, sources.json, varreduras de marcadores) removido intencionalmente — o levantamento é feito de forma leve a partir do contexto disponível

---

*Portado de BACH | Versão standalone sem scanner*

**Veja também:** [decide](../decide/SKILL.md) (frameworks para uma única decisão) | [structured-thinking](../structured-thinking/SKILL.md) (análise → ideias → decisão como meta-fluxo de trabalho) | [decision-shot](../decision-shot/SKILL.md) (apresentar uma análise pronta como forma executiva curta com link para a versão completa)
