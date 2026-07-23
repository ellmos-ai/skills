# Privat-Mail-Writer - Usecases

Diese Datei ist die Usecase-Registry. Neue wiederkehrende Mailaufgaben hier ergänzen, damit spätere Entwürfe konsistent bleiben.

## Usecase-Regeln

Ein Usecase beschreibt eine wiederkehrende Mailabsicht, nicht einen einzelnen Fall. Usecases knapp halten und nach folgendem Muster pflegen:

- `id`: stabile Kennung
- `name`: sprechender Name
- `trigger`: typische Userformulierungen
- `ziel`: was die Mail erreichen soll
- `pflichtangaben`: Fakten, die vor einem finalen Entwurf nötig sind
- `optionale_angaben`: Details, die den Entwurf verbessern
- `stil`: Länge, Ton und Direktheit
- `standardform`: Bausteinfolge oder Vorlage
- `rückfragen`: kurze Nachfragen, wenn Pflichtangaben fehlen

Neue Usecases nur anlegen, wenn die Aufgabe wahrscheinlich wiederkommt. Bei einem Einzelfall direkt entwerfen.

---

## UC-001 - Offizielle Absage eines Termins

**Trigger**

- "Termin offiziell absagen"
- "ich kann den Termin nicht wahrnehmen"
- "schreib eine kurze Absage"
- "freundlich und knapp absagen"
- "offiziellen Termin absagen"

**Ziel**

Einen vereinbarten oder angebotenen Termin höflich, klar und kurz absagen. Die Absage soll freundlich wirken, aber nicht lang erklären.

**Pflichtangaben**

- Empfänger oder Anredeform
- Terminbezug: Datum, Uhrzeit, Anlass oder Betreff
- Soll ein Ersatztermin angeboten oder erbeten werden?

**Optionale Angaben**

- knapper Grund, falls der User ihn ausdrücklich nennen will
- gewünschte Grußformel
- formeller oder halbformeller Ton

**Stil**

- kurz, freundlich, offiziell
- 3 bis 5 Sätze im Mailkörper
- keine langen Begründungen
- klare Absage im ersten oder zweiten Satz
- Bedauern nur einmal ausdrücken

**Standardform**

```text
Betreff: Absage des Termins am [Datum]

[Anrede],

vielen Dank für die Einladung / die Terminvereinbarung.
Leider muss ich den Termin am [Datum] absagen.
[Optional: Einen Ersatztermin können wir gerne abstimmen. / Ich melde mich wegen eines neuen Termins.]

Mit freundlichen Grüßen
[Signatur]
```

**Rückfragen**

- "Soll ich einen Ersatztermin anbieten oder nur absagen?"
- "Soll ein Grund genannt werden oder soll die Absage neutral bleiben?"

**Sehr kurze Variante**

```text
Betreff: Absage des Termins am [Datum]

[Anrede],

leider muss ich den Termin am [Datum] absagen.
Vielen Dank für Ihr Verständnis.

Mit freundlichen Grüßen
[Signatur]
```
