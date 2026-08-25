# Companion-Worker — Scaffold + Verifikation

Bauweg für eine **ad-hoc benannte, wiederverwendete Instanz** für eine
begrenzte Aufgabenserie (z. B. eine Ticket-Kette) — kein dauerhafter
Registry-Eintrag, kein neuer Rollen-Name über die Serie hinaus.

## Primärquelle des Musters

`_control-center/_TICKETS/README.md`, Abschnitt „Leitprinzip
(Kontext-Ökonomie)": „Der TICKET-MASTER ist ein dünner, langlebiger **Router**
und hält seinen Kontext klein. Ausführung + Verifikation werden ausgelagert;
Subagenten melden kompakt zurück (Hash + 1 Zeile). Für Ticket-Serien einen
**Companion-Subagenten** wiederverwenden (per `SendMessage`, ad-hoc benannt,
bei Domänenwechsel/Größe rotieren), statt jede Kleinigkeit inline zu lösen."

Namensgeber ist die Analogie zu `companion-for-agy` (ConPTY-Wrapper, der
Gemini/Antigravity als externen Companion-Prozess anspricht) — hier aber
ökosystem-intern: ein per `Agent`-Tool gestarteter, benannter Worker, der über
`SendMessage` für eine ganze Themenserie wiederangesprochen wird, statt für
jede Einzelaufgabe neu zu starten.

**Gelebtes Beispiel:** Diese Sitzung selbst. Der Worker `skillcreator-bau`
wurde für eine Kette zusammenhängender Tickets rund um Marketplace-Sichtung,
Registry-Pflege und Eigenbau-Skills wiederverwendet (mehrere `SendMessage`-
Runden von `team-lead`, ein durchgehender Name, kompakte Rückmeldungen je
Ticket) — kein neuer Worker pro Einzelticket.

## Scaffold-Fragen

1. **Themenklammer:** Was hält die Serie zusammen (ein Projekt, eine
   Ticket-ID-Familie, ein Marketplace-Themenblock)? Ohne erkennbare Klammer
   lieber Einzelaufgabe statt Companion-Worker.
2. **Name:** kurz, thematisch, kein Rollenname aus der Subagenten-Registry
   (Verwechslungsgefahr vermeiden — ein Companion-Worker ist KEIN dauerhafter
   Subagent).
3. **Rotationskriterium vorab festlegen:** Domänenwechsel oder Kontextgröße
   (siehe Primärquelle oben) — wann wird dieser Worker beendet und ein neuer
   für die nächste Themenserie gestartet? Nicht erst entscheiden, wenn der
   Kontext schon zu groß ist.
4. **Modellwahl:** wie bei nativen Subagenten NICHT hier entscheiden — an
   `model-strategy` delegieren (siehe `model-staffing-and-messaging.md`).
   Ein Companion-Worker erbt **nicht automatisch** das Modell des
   Orchestrators.
5. **Beauftragungsform:** „verweisen statt wiederholen" — zentrale Regeln aus
   `CLAUDE.md`/Projekt-Dokumenten NICHT im Auftrag nacherzählen (der Worker
   erbt sie ohnehin per Kontext); nur das Aufgabenspezifische mitgeben:
   gemessene Ausgangswerte, Kausalketten dieses Systems, Scope-Grenzen,
   Abbruchbedingungen, Begründungen für Festlegungen (siehe
   `model-staffing-and-messaging.md`).

## Verifikations-Checkliste

**Kritische Punkte:**
- Kein erkennbares Rotationskriterium — der Worker droht, Themen zu
  vermischen, bis der Kontext unbrauchbar wird.
- Auftrag wiederholt zentrale Regeln statt nur das Aufgabenspezifische zu
  nennen (Verdünnungseffekt — das Wichtige geht im Bekannten unter).
- Modellwahl nicht begründet.

**Warnungen:**
- Name kollidiert stilistisch mit einer dauerhaften Subagenten-Rolle
  (Verwechslungsgefahr).
- Keine kompakte Rückmeldeform vereinbart (Hash + 1 Zeile o. ä.) — der
  Orchestrator-Kontext wächst unnötig durch lange Statusberichte.

**Bestandene Prüfungen:**
- Klare Themenklammer, klares Rotationskriterium.
- Auftrag verweist statt nachzuerzählen; Begründungen sind mitgegeben, nicht
  nur Schlussfolgerungen (Nachvollziehbarkeit für den Worker, siehe
  `~/CLAUDE.md` Abschnitt „Agenten beauftragen: verweisen statt wiederholen").
- Modellwahl über `model-strategy` begründet.
