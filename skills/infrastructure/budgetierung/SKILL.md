---
name: budgetierung
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-10-03
updated: 2026-10-03
description: >
  Kontokonzept für den budgetierten Einsatz teurer oder knapper Modelle (Advisor,
  Reviewer, Spezialmodelle, Dauer-Worker) in längeren Agentenläufen. Beginnt mit
  einer gemeinsamen Aushandlung zwischen Nutzer und Modell über verfügbare Modelle,
  Rollen und Kontingente je Zeitfenster, führt ein Konto über jeden Einsatz, setzt
  vor jeder Eskalation ein Puzzleteil-Vorverfahren und erlaubt Anpassungen mitten im
  Lauf. Verwenden bei "Budget", "Kontingent", "Konto führen", "nur einmal pro Stunde",
  "Reviewer sparsam einsetzen", "Fable/Codex/Sol/Astra/Luna/Advisor nur begrenzt",
  "/budgetierung", und immer dann, wenn ein Operator-, Forschungs- oder
  Automationslauf mehrere Modelle mit unterschiedlichen Kosten kombinieren soll —
  auch wenn der Nutzer das Wort Budget nicht nennt, aber Einsatzgrenzen für Modelle
  vorgibt.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [budget, kontingent, modellwahl, eskalation, reviewer, advisor, operator, konto]
language: de
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Budgetierung — Modellkontingente aushandeln, führen, anpassen

## Wozu

Lange Agentenläufe kombinieren heute oft mehrere Modelle mit sehr unterschiedlichem Preis und
unterschiedlicher Verfügbarkeit: einen Hauptagenten, der denkt und entscheidet, billige
Dauer-Worker für die Ausführung und wenige teure Spezialisten für Reviews, Audits oder
Durchbrüche. Ohne Absprache passieren zwei Fehler: Die teuren Modelle werden für Routine
verbrannt, oder sie werden aus falscher Vorsicht nie benutzt. Das Konto macht den Einsatz
**sichtbar und verhandelbar**: Was erlaubt ist, steht vorher fest, jeder Einsatz wird
gebucht, und der Nutzer kann jederzeit nachsteuern.

Modelle, Preise und Kontingente ändern sich ständig, weil neue Modelle erscheinen, Abos sich ändern
und Projekte unterschiedlich wichtig sind. Deshalb enthält dieser Skill **keine festen Zahlen**,
sondern ein Verfahren, um sie pro Einsatz und Projekt gemeinsam festzulegen.

## Phase 1 — Aushandlung zu Beginn

Bevor Arbeit delegiert wird, das Budget mit dem Nutzer klären. Was er schon vorgegeben hat,
nicht erneut abfragen; nur Lücken schließen und das Ergebnis einmal kurz bestätigen lassen.

1. **Bestand erheben:** Welche Modelle und Zugänge sind auf diesem Host tatsächlich aufrufbar?
   Prüfen statt raten: Konfigurationsdateien, Modelllisten der CLIs, verfügbare Subagent-Typen.
   Modellnamen exakt so notieren, wie sie aufgerufen werden.
2. **Rollen vorschlagen:** Jedes Modell bekommt eine Rolle:
   - *Denker/Entscheider* (Hauptagent),
   - *Dauer-Worker* (Ausführung, ohne oder mit weitem Budget),
   - *Reviewer/Auditor* (unabhängige Prüfung, idealerweise ein anderer Anbieter als der Autor),
   - *Eskalation* (hochkomplexe Teilprobleme, Durchbruchsversuche),
   - *Advisor/Berater* (Kurskorrektur des Hauptagenten).
3. **Kontingente festlegen:** Je Ressource ein Budget und ein Zeitfenster, z. B. „2 Anfragen je
   Stunde“ oder „dauerhaft, ohne Grenze“. Ausdrücklich klären:
   - **Verfall oder Ansparen?** Ungenutzte Einheiten verfallen in der Regel; das so festhalten.
   - **Gemeinsame oder getrennte Töpfe?** Teilen sich z. B. zwei Modelle eine Einheit („Fable
     *oder* Astra“)?
   - **Zählt der Advisor mit?** Advisor-Aufrufe sind teuer und leicht zu vergessen; ob sie ein
     eigenes Kontingent haben, zum Topf gehören oder extrabudgetär sind, steht im Konto.
   - **Aufwandsstufe:** Bei Modellen mit Reasoning-Stufen gehört die Stufe zum Budget
     (xhigh ≠ low).
4. **Vorverfahren vereinbaren** (Phase 3), sofern der Nutzer nichts anderes will.
5. **Konto anlegen** (Phase 2) und dem Nutzer den Pfad nennen.

Kurzform der Rückfrage, wenn Angaben fehlen: eine Frage mit Vorschlag statt offener Liste,
z. B. „Vorschlag: Sonnet als Dauer-Worker, Codex-Review 1×/Stunde, Advisor nur auf Anfrage —
passt das?“.

## Phase 2 — Das Konto

Eine Markdown-Datei im Projekt, z. B. `_operator/KONTINGENT.md` oder am Ort, den die
Projektkonventionen vorsehen. Vorlage: [references/konto-vorlage.md](references/konto-vorlage.md).

Das Konto enthält:
- **Regelblock:** die ausgehandelten Kontingente als Tabelle (Ressource | exakter Aufruf/Modellname
  | Budget je Fenster | Verfall ja/nein).
- **Änderungsprotokoll der Regeln:** Jede Anpassung durch den Nutzer wird datiert ergänzt, nicht
  überschrieben. So bleibt nachvollziehbar, unter welcher Regel eine frühere Buchung stand.
- **Buchungstabelle:** eine Zeile je Einsatz einer budgetierten Ressource mit Nr., tatsächlicher
  Startzeit, **tatsächlich gelaufenem Modell**, Zweck, durchlaufenem Vorverfahren, Ergebnispfad
  und frühestem nächsten Fenster.

Wichtig:
- **Tatsächliches Modell buchen, nicht das gemeinte.** CLIs fallen ohne ausdrückliche
  Modellangabe auf ihr Default-Modell zurück. Deshalb das Modell immer explizit setzen und im
  Zweifel aus Konfiguration oder Antwort belegen. Stellt sich nachträglich heraus, dass ein
  anderes Modell lief, die Buchung **umklassifizieren** und den Fehler vermerken.
- **Startzeit aus einem Beleg** (Zeitstempeldatei, Log), nicht geschätzt.
- **Extrabudgetäre Einsätze** (vom Nutzer ausgelöst oder ausdrücklich freigestellt) trotzdem
  eintragen, mit dem Vermerk „keine Einheit gebucht“, damit das Bild vollständig bleibt.
- Unbegrenzte Dauer-Worker brauchen keine Einzelbuchung. Es genügt eine Zeile, dass sie laufen
  und woran.

## Phase 3 — Vorverfahren vor jeder Eskalation

Teure Einheiten sind für Ausnahmen da. Bevor eine gebucht wird:

1. **Puzzleteil definieren:** Was genau fehlt? Welche Eigenschaften müsste die Lösung, die
   Quelle oder das Prüfergebnis haben? Schriftlich, ein paar Zeilen.
2. **Billig suchen:** Web, Fachdatenbanken, Projektbestand, mit Dauer-Workern.
3. **Ideenwerkzeuge:** z. B. `/idea-mining`, dann `/skill-finder`, falls es einen Skill für die
   Aufgabe gibt.
4. **Erst dann buchen**, und im Konto vermerken, welche Schritte durchlaufen wurden.
   Passt ein Schritt sachlich nicht (z. B. Ideensuche, wenn eine *Prüfung* gesucht ist), das
   begründet vermerken, statt ihn pro forma auszuführen.

Ein verfallendes Kontingent ist **kein Grund**, es zu verbrauchen. Umgekehrt ist falsche
Sparsamkeit auch ein Fehler: Wenn eine unabhängige Abnahme für den nächsten Schritt nötig ist
(z. B. Claim-Register mit Anbieterwechsel), ist das genau der Ausnahmefall, für den das Budget
existiert.

## Phase 4 — Anpassungen im Lauf

Der Nutzer kann Regeln jederzeit ändern: neue Modelle, mehr oder weniger Einheiten, ein
Advisor, der ab sofort mitzählt. Dann:
- die neue Regel datiert in den Regelblock übernehmen und die alte stehen lassen,
- prüfen, ob bisherige Buchungen unter der neuen Regel anders einzuordnen sind, und das vermerken,
- prüfen, ob es für die neue Ressource eine passende offene Aufgabe gibt, und sie dann einsetzen.
  Gibt es keine, darf sie ungenutzt bleiben, bis Bedarf entsteht: Ein Kontingent ist ein Rahmen,
  kein Auftrag. Der Nutzer kann den Bedarf überschätzt haben, und Beschäftigung um ihrer selbst
  willen kostet ebenfalls,
- dem Nutzer in einem Satz bestätigen, was jetzt gilt.

Schlägt das Modell selbst eine Anpassung vor (z. B. weil eine Ressource dauerhaft ungenutzt bleibt
oder ein Engpass auftritt), formuliert es das als Vorschlag mit Begründung. Die Entscheidung
trifft der Nutzer.

## Phase 5 — Abschluss

Am Ende eines Laufs oder Blocks im Bericht an den Nutzer eine Zeile zum Verbrauch: welche
Einheiten genutzt wurden, wofür und mit welchem Ergebnis, was ungenutzt verfiel. Das Konto bleibt im Projekt
liegen; eine Folgesitzung liest es zuerst.

## Beispiel

Der Nutzer sagt: „Arbeite als Operator, nutze Sonnet-Worker, Fable oder Codex nur einmal pro Stunde
und führe ein Konto.“ Später: „Sol darf zweimal pro Stunde reviewen, Luna dauerhaft, der Advisor
bekommt ein Extrakontingent.“

→ Phase 1 bestätigt kurz die Rollen, Phase 2 legt das Konto mit der ersten Regel an. Bei der
zweiten Nachricht ergänzt Phase 4 den Regelblock und stellt fest, dass zwei frühere „Codex“-Audits
ohne Modellangabe tatsächlich über das Default-Modell liefen. Die Buchungen werden deshalb
umklassifiziert. Für Luna gibt es gerade eine passende offene Explorationsaufgabe, also wird sie
eingesetzt; ohne eine solche Aufgabe bliebe sie ungenutzt.

## Verwandte Skills

- `operator` — Rollenmodell Operator/Worker, in das dieses Konto eingebettet wird.
- `model-strategy` — wann welches Modell sachlich passt; dieser Skill regelt, *wie viel* davon.
- `idea-mining`, `skill-finder` — Bausteine des Vorverfahrens.
- `advisor-skill` — selektive Beratung; deren Aufrufe gehören ins Konto.
- `orchestrator` — Arbeitspakete, Profile (Parallelität), Abnahme.
- `choose-your-orchestrator` — Session-Vertrag, in dessen Budgetslots dieses Konto
  eingetragen wird.

## Changelog

### 1.0.0 (2026-10-03)
- Initiale Version: Aushandlung, Konto, Vorverfahren, Lauf-Anpassungen, Abschluss.
