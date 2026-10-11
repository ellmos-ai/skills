---
name: model-strategy
version: 3.1.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-10-11
description: Rollenbasierte Multi-Modell-Strategie. Modellkatalog liegt in einer lokalen Konfigurationsdatei statt im Skill-Text -- Rollen (Denker/Entscheider, Dauer-Worker, Entwurfsgenerator, Reviewer/Abnahme, Eskalation), Reasoning-Effort als eigene Achse, Abnahmepflicht für Entwurfsmodelle, Anbieterwechsel für unabhängige Reviews, Kontingente, Delegationsablauf und Kosten/Qualität kleiner Worker.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [model-switching, orchestration, multi-model, cost-optimization, routing, cross-agent, advisor, roles]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/ing-strategie.md', 'origin_version': '2.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="model-strategy banner">

# Model-Switching Strategie

> Rollenbasierte Multi-Modell-Strategie: Konfiguration statt Textkatalog, Rollen statt starrer
> Score-Tabelle, Abnahmepflicht für Entwürfe, Anbieterwechsel für unabhängige Reviews.

---

## 0. Konfiguration

**Modelle gehören nicht in diesen Text.** Welche konkreten Modelle, Provider und Aufrufwege
gerade existieren, ändert sich schneller als ein Skill sinnvoll gepflegt werden kann — und ist
pro Nutzer verschieden. Dieser Skill beschreibt deshalb nur **Rollen und Prinzipien**; der
tatsächliche Katalog lebt in einer Konfigurationsdatei im Skill-Ordner.

### Ladereihenfolge

1. **Lokale Datei** im Skill-Ordner: `models.local.json` oder `models.private.json` (beide
   Namensmuster sind in der `.gitignore` dieser Bibliothek bereits als privat erfasst,
   `skills/**/*.local.*` bzw. `skills/**/*.private.*` — nie veröffentlichen, nie committen).
   Wenn vorhanden, ist das der maßgebliche Katalog.
2. **Beispieldatei** `models.example.json` im selben Ordner — neutrale Platzhalter-Vorlage, die
   das Schema zeigt. Dient nur als Vorlage zum Anlegen der eigenen lokalen Datei, nicht als
   Katalog für echte Läufe.
3. **Live-Erhebung**, wenn beide Dateien fehlen oder unvollständig sind: welche Modelle bietet
   die aktuelle Runtime tatsächlich an (z. B. das `model`-Enum eines nativen Subagenten-Werkzeugs,
   `codex debug models --bundled`, eine App-eigene Modellliste)? Ein geratenes Modell ist
   schlechter als ein kurz erhobenes.

**Bei Widerspruch gilt die Live-Messung.** Eine Konfigurationsdatei kann veraltet sein (ein
Modell wurde abgeschaltet, umbenannt oder ersetzt); eine frische Messung an der Runtime selbst
schlägt jede Textquelle, inklusive der eigenen lokalen Konfiguration. Widerspruch kurz benennen
und die Konfigurationsdatei danach aktualisieren, statt ihn stillschweigend zu übergehen.

**`deprecated: true` heißt: nie einsetzen.** Ein als `deprecated` markierter Katalogeintrag
bleibt aus Erkennungs-/Historiengründen stehen (damit ein Agent eine alte Erwähnung einordnen
kann), wird aber für keine neue Aufgabe mehr gewählt — auch nicht als Fallback.

### Schema (siehe `models.example.json`)

Jeder Katalogeintrag trägt: `id`, `provider`, `invoke` (Aufrufmuster, keine echten Pfade im
Beispiel), `effort_levels`, `roles` (siehe Abschnitt 1), `strengths`, `weaknesses`, `guardrails`
(Zuverlässigkeits-Einschränkungen wie „nur Entwurf", „nicht selbst ins Dateisystem schreiben",
„enge Abnahme" — siehe Abschnitt 3), `budget_hint` (Verweis auf den Skill `budgetierung`),
`verified` (Verfügbarkeit in der eigenen Runtime belegt, siehe Abschnitt 5) und `deprecated`.

---

## 1. Rollen statt starrer Modell-Hierarchie

Eine Modellwahl beantwortet zuerst **welche Rolle** eine Aufgabe braucht, danach erst welches
konkrete Modell diese Rolle aktuell am besten/günstigsten füllt. Rollen sind stabiler als
Modellnamen — ein Modell wird ausgetauscht, die Rolle bleibt.

| Rolle | Frage | Typisches Merkmal |
|---|---|---|
| **Denker/Entscheider** | Architektur, Strategie, mehrdeutige Anforderungen, Abwägung von Alternativen | teurer, wird gezielt statt durchgehend eingesetzt |
| **Dauer-Worker** | laufende Umsetzung über viele Schritte: Implementierung, Debugging, Standardaufgaben | güns­tig genug, um durchgehend zu laufen |
| **Entwurfsgenerator** | schnelle erste Fassung (Design, Text, Code, Struktur, Übersetzung) | schnell, aber grundsätzlich mit Abnahmepflicht (Abschnitt 3) |
| **Reviewer/Abnahme** | prüft Ergebnisse anderer Modelle | wirkt am stärksten bei einem anderen Anbieter als der Ersteller (Abschnitt 4) |
| **Eskalation** | wird nur für den einzelnen schwierigsten Schritt hinzugezogen | nie für den ganzen Lauf, immer kurz begründet |

Ein Modell kann mehrere Rollen tragen (z. B. gleichzeitig Dauer-Worker und gelegentlicher
Reviewer). Welche Modelle welche Rollen aktuell füllen, steht in der Konfiguration
(Abschnitt 0), nicht hier. Zur kleinsten Worker-Klasse (Kosten pro Auftrag, Qualität
je Aufgabentyp) siehe Abschnitt 7.

### Grobe Schwierigkeits-Orientierung (keine feste Tabelle)

Eine Score-Rechnung über feste Dimensionen (Klarheit, Komplexität, Kreativität, Kontext,
Kritikalität) kann als **grobe Orientierung** dienen, um zwischen Dauer-Worker und
Denker/Eskalation zu unterscheiden — sie ist kein verbindlicher Mechanismus, der ein Modell
automatisch bestimmt:

```
SCORE = (10 - KLARHEIT) + KOMPLEXITAET + KREATIVITAET + KONTEXT + KRITIKALITAET   (je Dimension 0-10)
```

Niedriger Score → Dauer-Worker oder sogar ein günstiges/token-freies lokales Modell reicht.
Hoher Score (durchgehend widersprüchliche Anforderungen, mathematische Beweisführung, Statistik
mit weitreichenden Konsequenzen) → Denker/Eskalation, meist mit anschließendem Review. Dazwischen
liegt der breite Normalfall des Dauer-Workers. Die konkrete Schwelle, ab der eskaliert wird,
hängt vom aktuellen Katalog ab (manche Nutzer haben nur zwei, andere sechs Rollen-Füllungen) und
gehört deshalb nicht in eine feste Tabelle in diesem Text.

---

## 2. Reasoning-Effort als eigene Achse

Reasoning-Effort (z. B. `low`/`medium`/`high`/`xhigh`/`max`, oder eine feinere/andere Staffelung
je Anbieter) ist eine **von der Modell-/Rollenwahl unabhängige Achse**: Erst ein fachlich
geeignetes, live verfügbares Modell für die Rolle wählen, dann seine Denktiefe passend zur
Schwierigkeit staffeln.

- Niedrige Stufen für Routine und gut definierte Teilaufgaben.
- Hohe Stufen für Wissenschaft, Beweisführung, Architekturentscheidungen mit Tragweite.
- Eine Breitenroute (parallele, klar getrennte Teilaufgaben statt mehr Tiefe in einem Strang)
  nur, wenn die aktuelle Runtime dafür einen eigenen Modus anbietet und die ohnehin geltende
  Bestätigungs-/Kostenregel für größere oder schwer kalkulierbare Fan-outs erfüllt ist.

**Keine Effort-Stufe erweitert Schreib-, Kosten-, Freigabe- oder Publikationsrechte.**
Delegationen bleiben innerhalb der bestehenden Autorität (siehe Abschnitt 5). Ist eine Stufe in
der aktuellen Runtime nicht verfügbar, wird das benannt und auf eine belegt verfügbare Stufe
ausgewichen — nicht stillschweigend das billigere Verhalten als Erfolg gemeldet.

Lang laufende oder rechenintensive Einzelschritte gehören — unabhängig von der Effort-Stufe —
auf den dafür vorgesehenen Compute-Host, nicht auf die lokale interaktive Maschine; die Schwelle
dafür ist eine Umgebungsregel, keine Modellstrategie-Regel.

---

## 3. Abnahmepflicht für Entwurfsmodelle

Modelle in der Rolle **Entwurfsgenerator** liefern grundsätzlich einen Entwurf, keine fertige
Lieferung — unabhängig davon, wie gut der erste Eindruck ist. Das ist keine pauschale Abwertung
eines einzelnen Modells, sondern eine Eigenschaft der Rolle: schnelle erste Fassungen sind
wertvoll, weil sie schnell sind, und genau deshalb fehleranfälliger.

Daraus folgen drei feste Regeln, unabhängig vom konkreten Modell:

1. **Jeder Entwurf wird vor Übernahme geprüft** — durch ein Dauer-Worker- oder Reviewer-Modell,
   nie durch bloßes Vertrauen in die Entwurfsqualität.
2. **Ein Entwurfsmodell schreibt bevorzugt nicht selbst in das Zielsystem** (Zieldateisystem,
   Produktionsdatenbank, veröffentlichter Ort). Es liefert das Ergebnis zurück; ein geprüftes
   Modell setzt es ein. Diese Guardrail steht konkret im jeweiligen Katalogeintrag
   (`guardrails`), weil sie je Werkzeug unterschiedlich technisch umgesetzt wird.
3. **Fachlich enge Bereiche** (z. B. LaTeX, Rechts- oder Zahlentexte, sicherheitsrelevanter Code)
   bekommen eine **engere** Abnahme als allgemeiner Text, auch wenn das Entwurfsmodell dort
   erfahrungsgemäß gut abschneidet.

---

## 4. Anbieterwechsel für unabhängige Reviews

Ein Review ist am aussagekräftigsten, wenn Ersteller und Prüfer **nicht denselben Anbieter und
nicht dasselbe Modell** nutzen — sonst teilen sie möglicherweise dieselben blinden Flecken.

- **Review-Muster:**

  | Muster | Wie es funktioniert | Wann einsetzen |
  |---|---|---|
  | **Session-Advisor** | Nutzer setzt einen Reviewer in der laufenden Session, Agent ruft ihn gezielt | Standard bei Beweis/Architektur |
  | **Orchestrator-als-Reviewer** | das stärkere/koordinierende Modell reviewt den Output eines Worker-Subagenten | Orchestrator ist ohnehin leistungsfähiger als der Worker |
  | **Gegen-Agent / Anbieterwechsel** | Modell A (Anbieter 1) arbeitet, Modell B (Anbieter 2) prüft adversarial | unabhängige Verifikation, zwei Perspektiven, höchste Aussagekraft |
  | **Empfehlung statt Eigenausführung** | Agent empfiehlt explizit: „diese Aufgabe mit Rolle Eskalation + Review bearbeiten" | aktuelle Session ist für den Schritt zu schwach |

- **Wann Review einsetzen:** mathematische Beweisführung, Architekturentscheidungen mit
  langfristigen Konsequenzen, statistische Methodik/Studiendesign, komplexe Bugs nach mehreren
  erfolglosen Debug-Zyklen, jeder Entwurf aus Abschnitt 3.
- **Wann kein Review nötig ist:** Routine-Code, Content, Formatierung; gut definierte,
  unkritische Aufgaben im Rahmen eines bereits geprüften Vorgehens.
- **Dokumentierte Schwächen bleiben in der Konfiguration, nicht hier** — z. B. „Modell X ist für
  mathematische Reviews ungeeignet" gehört als `weaknesses`-Eintrag in den Katalog, weil er sich
  mit dem Modell ändert, nicht mit dem Skill.

---

## 5. Rechte hängen am Auftrag, nicht am Modell

Es gibt bewusst **keine Berechtigungsmatrix nach Modellname** (welches Modell darf löschen,
welches Systembefehle ausführen). Eine solche Matrix suggeriert, Rechte seien eine Eigenschaft
des Modells — sie sind eine Eigenschaft des **Auftrags und der erteilten Autorität**:

- Was ein Agent lesen, schreiben, löschen oder ausführen darf, ergibt sich aus der aktuellen
  Runtime-Sandbox, dem Scope des Auftrags und einer etwaigen Nutzerfreigabe — nicht daraus, ob
  gerade ein teures oder ein günstiges Modell antwortet.
- Guardrails im Katalog (`guardrails`-Feld) sind **Zuverlässigkeits-Hinweise**, keine
  Rechteerweiterung oder -beschränkung: „nur Entwurf" sagt, wie sehr dem Ergebnis zu trauen ist,
  nicht, was technisch erlaubt wäre.
- Eine Delegation (an einen Subagenten, einen externen Agenten, ein anderes Modell) bleibt
  innerhalb der Autorität des delegierenden Laufs. Sie erweitert nichts.

### Eskalation und De-Eskalation (Muster, nicht Modellnamen)

- **Nach oben (Rolle wechselt zu Denker/Eskalation):** Architektur-Entscheidung gefordert,
  mehrere Systeme müssen integriert werden, Anforderungen widersprüchlich/unklar, strategische
  Planung nötig, kritischer Bug nach mehreren erfolglosen Zyklen.
- **Lateral (andere Rolle, gleiche Ebene):** fachfremde Recherche, unabhängiges Review,
  Spezialwerkzeug eines anderen Anbieters.
- **Nach unten (De-Eskalation):** Konzept ist definiert → Dauer-Worker übernimmt Umsetzung;
  Aufgabe ist trivial/repetitiv → ein günstigeres Modell übernimmt; reine Textaufgabe ohne
  Werkzeugzugriff → ein lokales/token-freies Modell übernimmt, falls im Bestand verfügbar und
  belegt (`verified: true` im Katalog).

### Transparenzregel bei Modellwechsel

**Ein stiller Modellwechsel gegenüber der konfigurierten Besetzung ist zu melden.** Wählt eine
Runtime aus eigenem Antrieb (Kontingent, Verfügbarkeit, interner Default) ein anderes Modell als
in `models.local.json`/`models.private.json` festgelegt, ist das kein Fehler, aber es gehört
transparent benannt — nicht stillschweigend als Erfolg der geplanten Strategie gemeldet. Das
gilt unabhängig davon, welche zwei Modelle konkret betroffen sind; frühere Fassungen dieses
Skills nannten hier ein bestimmtes Modellpaar als Präzedenzfall — die Regel ist seither bewusst
neutral gehalten, weil sie nicht an einem einzelnen Modellwechsel hängen soll.

---

## 6. Kontingente, Ablauf und Rollenzuschnitt — Verweise statt Doppelpflege

Dieser Skill beantwortet **welche Rolle** und **mit welcher Sorgfalt (Effort, Review)**. Zwei
benachbarte Fragen werden bewusst nicht hier beantwortet, um Doppelpflege zu vermeiden:

- **„Wie oft darf ich ein teures/knappes Modell einsetzen?"** → Skill `budgetierung`: Aushandlung
  von Kontingenten je Zeitfenster, laufendes Konto, Puzzleteil-Vorverfahren vor Eskalation.
  `budget_hint` im Katalog verweist genau hierhin.
- **„Wie zerlege ich die Aufgabe, delegiere ich Arbeitspakete und nehme ich Ergebnisse ab?"** →
  Skill `orchestrator` (Protokoll zum Zerlegen, Beauftragen, Abnehmen) bzw. Skill
  `choose-your-orchestrator` (wenn die passende Orchestrierungsform selbst erst ausgehandelt
  werden muss — Session-Vertrag für Modellslots, Parallelität, Spawn-Tiefe, Schreibgrenzen,
  Abnahme, Eskalation).

---

## 7. Kleine Worker (Haiku-Klasse): Qualität und Kosten pro Auftrag

Messung 2026-10 (Haiku 5.5, `claude-haiku-5-5`; Familie damals Fable 5.1, Opus 5.5, Sonnet 5.5,
Haiku 5.5; rund 30 Einsätze, gegen Sonnet 5.5 verglichen). Preise je Mio. Tokens (Stand 2026-10-06):
Haiku 5.5 $0,10/$0,50 (bis 100k Prompt), Sonnet 5.5 $2/$10, Opus 5.5 $4/$20 — pro Token ≈ 1/20
Sonnet, 1/40 Opus. Preise und Befunde veralten mit den Modellen: bei Abweichung gilt die frische
Messung (Abschnitt 0).

**Effizienz-Falle: billig pro Token ≠ billig pro Auftrag.** Ein Haiku-Subagent im Claude-Code-Harness
kostet ~180–360k Tokens je Auftrag, auch für eine 193-Zeilen-Datei. Die Grundlast (~45–65k Tokens
je Turn) stammt aus dem Harness (Skill-/Agenten-/MCP-Listen, Start-Hooks), nicht aus der
Projekt-`CLAUDE.md` (Wiederholung nach Kürzung der Regeldatei: 186k → 182k). Gegenmittel:

- **Bündeln:** mehrere Teilaufgaben je Worker, damit die Grundlast nur einmal anfällt; nie ein
  Subagent je Dokument.
- **Naiver Headless-Worker** für Massenaufgaben mit fester Eingabe: `claude -p --model haiku
  --strict-mcp-config --mcp-config '{"mcpServers":{}}' --disable-slash-commands --tools Read,Write`
  → gemessen $0,018 je README-Übersetzung (gleiches Tokenprofil: Sonnet ≈ $0,35, Opus ≈ $0,66).
  `--bare` (ohne `CLAUDE.md` und Hooks) spart weiter, braucht aber einen API-Key. Bei sehr großen
  Mengen API/Batch statt Subagent.
- **Ergebnis als Datei plus Meldung von 3–5 Zeilen**, wenige Tool-Aufrufe.

**Qualität je Aufgabentyp (gemessen):**

| Aufgabentyp | Befund |
|---|---|
| Treueprüfung alt → neu (Prüfschwarm) | sehr gut; fand 2 kritische Fehler, die Autor und Prüfskript übersahen; ~6 % Fehlalarme |
| Einzeldatei-Code-Review | gut; 8 echte Funde gegen 6 des Vergleichsmodells, in einer zweiten Datei 4 Zusatzfunde; jeder Fund braucht Gegenprüfung |
| Übersetzung (z. B. READMEs DE→EN) | gut (~9/10); vollständige Parität; Fachbegriffe schwanken zwischen Läufen → Glossar; UI-Labels/Platzhalter brauchen Kontext |
| Doku↔Code-Abgleich | gut; keine Fehlalarme in Stichproben |
| Dubletten-Kartierung | brauchbar; ~85–90 % Recall gegen das Vergleichsmodell, ~1 Fehlalarm je Abschnitt |
| Kleiner, klar spezifizierter Fix mit Test | gut |
| Mechanik (Tests im Worktree, Rebase, PR, Lagebild) | gut; meldet Flakiness und Blockaden ehrlich, umgeht keine Guards |

**Empfehlungen:**

1. Massenübersetzungen (Docs, READMEs, i18n-Strings): sehr geeignet, mit Glossar-Datei, 1:1-Paritätsregel und Stichprobe durch ein stärkeres Modell; viele Dokumente je Worker bündeln oder den naiven Headless-Worker bzw. die Batch-API nutzen — nie ein Subagent je Dokument.
2. Prüfschwärme (Treue alt→neu, Doku↔Code, Vorher/Nachher, Link-/Pfad-Existenz): der beste Einsatz — unabhängiger Zweitleser, der findet, was dem Autor entgeht.
3. Dokumentationsbasis aktualisieren im Muster *kleines Modell kartiert → Dauer-Worker schreibt → kleines Modell prüft → Denker nimmt ab*; normative Texte nie allein vom kleinen Modell umschreiben lassen.
4. Code-Review-Vorprüfung je Datei und kleine, klar spezifizierte Fixes mit Test.
5. Mechanik: Testläufe, Readbacks, Log-Auswertung, Lagebilder per `git grep`.
6. **Nicht** für Architektur-, Merge- und Sicherheitsentscheidungen, normative Regeldateien und große dateiübergreifende Synthesen.
7. Effizienzregeln: Aufgaben je Worker bündeln, Ergebnis als Datei plus 3–5-Zeilen-Meldung, wenige Tool-Aufrufe; Ergebnisse nie ungeprüft übernehmen (Abschnitt 3 gilt auch hier).

**Einsatzregel:** Das Modell ist ein Entwurfs- und Prüfwerkzeug (Rolle *Entwurfsgenerator* bzw.
Zweitleser im Prüfschwarm, Abschnitt 1) — keine Abnahme-Instanz und kein Standard-Dauer-Worker.
Produktivarbeit läuft über den Dauer-Worker der Konfiguration; die kleine Klasse nur auf
ausdrücklichen Auftrag des Nutzers. Massenaufgaben mit fester Eingabe laufen bevorzugt über die
API (Batch, ≈ $0,001 je README), nicht als Subagent im Harness.

---

## Changelog

### 3.1.0 (2026-10-11) — Kleine Worker (Haiku-Klasse) gemessen
- Neuer Abschnitt 7: Haiku 5.5 als Worker, Messung 2026-10 (Qualität je Aufgabentyp, Preise, Empfehlungen)
- Effizienz-Falle dokumentiert: Subagent ~180–360k Tokens je Auftrag (Harness-Grundlast ~45–65k je
  Turn); Gegenmittel Bündeln, naiver Headless-Worker ($0,018 je README-Übersetzung), API/Batch für
  Massenaufgaben
- Einsatzregel: kleine Klasse nur auf ausdrücklichen Auftrag, Produktivarbeit über den Dauer-Worker
- Schema-Liste in Abschnitt 0 um `verified` ergänzt (Feld war in `models.example.json` und
  Abschnitt 5 bereits in Gebrauch)

### 3.0.0 (2026-10-03) — Breaking: Modellkatalog ausgelagert
- Modellkatalog aus dem Skill-Text entfernt und in `models.example.json` (getrackt, neutral)
  plus eine lokale, nicht veröffentlichte Konfigurationsdatei (`models.local.json` /
  `models.private.json`, bereits über `.gitignore` als privat erfasst) verlagert
- Ladereihenfolge dokumentiert: lokale Datei → Beispieldatei → Live-Erhebung; bei Widerspruch
  gewinnt die Live-Messung; `deprecated: true` wird nie eingesetzt
- Starre Level-1-bis-4-Modellhierarchie und feste Score→Modell-Tabelle ersetzt durch fünf Rollen
  (Denker/Entscheider, Dauer-Worker, Entwurfsgenerator, Reviewer/Abnahme, Eskalation); Score
  bleibt nur noch als grobe Orientierung
- Abnahmepflicht für Entwurfsmodelle als eigener Abschnitt (Prüfpflicht, keine
  Direktschreibrechte ins Zielsystem, engere Abnahme in fachlich engen Bereichen)
- Anbieterwechsel für unabhängige Reviews als Prinzip statt fester Modellpaar-Empfehlung
- Berechtigungsmatrix nach Modellname entfernt — Rechte hängen am Auftrag/der Autorität, nicht
  am Modell; Guardrails sind Zuverlässigkeits-Hinweise, keine Rechteklausel
- Konkreter Companion-1.0.4-Aufrufweg, feste Ollama/Haiku-Eskalationskette und die
  Fable/Opus-4.8-Präzedenzregel entfernt bzw. in eine neutrale „stiller Modellwechsel ist zu
  melden"-Regel überführt
- Kontingente an den Skill `budgetierung`, Delegationsablauf/Rollenzuschnitt an `orchestrator`
  und `choose-your-orchestrator` verwiesen statt doppelt gepflegt

### 2.2.0 (2026-09-02)
- Reasoning-Effort als orthogonale Achse zur Modellwahl ergänzt (`xhigh`, gezieltes `max`,
  breitenorientiertes `ultracode`)
- Lokale Compute-Schwelle sowie Runtime-, Kosten- und Autoritätsgrenzen klargestellt

### 2.1.0 (2026-07-02)
- PRÄZEDENZ-REGEL: ein bestimmtes Modell ersetzt ein anderes in allen Level-4-/Reviewer-/
  Beweis-Empfehlungen (User-Entscheid; inzwischen mit 3.0.0 neutralisiert)
- Stiller-Modellwechsel-Warnung ergänzt

### 2.0.0 (2026-06-12)
- Cross-Agent-Delegation: externe Agenten und ein lokales Modell als Routing-Ziele
- Advisor-Pairing: 4 Muster (Session-Advisor, Orchestrator-als-Reviewer, Gegen-Agent,
  User-Empfehlung)
- Erreichbarkeits-Matrix: Subagent-startbar vs. User-only dokumentiert
- Laterale Eskalation zu externen Agenten (Recherche, Review)
- Score-Schwellwerte erweitert

### 1.0.0 (2026-03-15)
- Portiert aus BACH v3.8.0 (ing-strategie v2.0.0)

---

*Portiert aus BACH v3.8.0 | Rollenbasiert seit 3.0.0*
