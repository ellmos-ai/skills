---
name: incident-notes
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: >
  Befundprotokoll und Beweiskette für Rettungs- und Vorfallfälle auf Laptops und PCs: wie
  Beobachtungen, Deutungen und durchgeführte Handlungen getrennt, mit gemessener UTC-Zeit
  und Prüfsummen festgehalten werden, wie Geheimnisse geschwärzt werden und wie die
  Eigentümerin oder der Eigentümer eine verständliche Zusammenfassung erhält. Begleitet
  endpoint-triage, malware-cleanup-guide und os-hardening-baseline.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [incident-response, documentation, evidence, chain-of-custody, endpoint, audit-trail, defensive]
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
  origin_path: "skills/infrastructure/incident-notes/"
  origin_version: "1.0.0"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# incident-notes (Deutsch)

Ohne Protokoll ist ein Rettungsfall nicht nachvollziehbar, und niemand kann später sagen, was
am Gerät verändert wurde. Dieser Skill legt fest, **was** festgehalten wird und **wie**. Er
ist defensiv und ersetzt keine rechtliche Beratung: Wenn ein Fall vor Gericht oder
gegenüber einer Versicherung gebraucht werden könnte, vor weiteren Schritten Fachleute
hinzuziehen.

## Der Fallordner

Ein Ordner je Fall, benannt mit der Fall-ID aus `rescue-intake`:

```text
fall-<datum>-<nr>/
  intake.md          Aufnahme (Eigentum, Einwilligung, Modus)
  notes.md           Befundprotokoll (diese Vorlage, laufend)
  actions.md         Handlungsprotokoll (jede Änderung am Gerät)
  evidence/          Sammelausgaben, Abbild-Prüfsummen, INDEX.sha256
  summary.md         Zusammenfassung für die Eigentümerin/den Eigentümer
```

## Regeln

1. **Zeit messen, nicht schätzen.** Jeder Eintrag trägt UTC-Zeit, aus der Systemuhr
   abgelesen. Weicht die Uhr des Zielgeräts ab, die Abweichung einmal notieren.
2. **Beobachtung, Deutung, Handlung trennen.** Was die Ausgabe zeigt, ist eine Beobachtung.
   Was man daraus schließt, ist eine Deutung mit Sicherheitsgrad (`gesichert`,
   `wahrscheinlich`, `unklar`). Was jemand am Gerät getan hat, ist eine Handlung. Mischformen
   erzeugen Scheingewissheit.
3. **Quellenangabe.** Jede Beobachtung nennt die Datei im Fallordner, aus der sie stammt
   (und die Zeile oder den Ausschnitt).
4. **Prüfsummen.** Für Sammelausgaben, Abbilder und Backups die SHA-256-Summe notieren; die
   Summen stehen in `INDEX.sha256` bzw. im Protokoll. Beweismaterial nach der Prüfsumme
   nicht mehr verändern: Arbeitskopien verwenden.
5. **Übergabekette.** Wer hatte wann welches Medium oder Abbild? Eine Zeile je Übergabe
   (Datum UTC, von, an, Medium, Prüfsumme geprüft ja/nein).
6. **Jede Änderung am Gerät ins Handlungsprotokoll,** bevor sie erfolgt (Plan, Zustand
   vorher, Bestätigung der Eigentümerin oder des Eigentümers, Rückweg) und danach
   (Ergebnis, Zustand nachher, Nachprüfung). Nichts wird nachträglich „geschönt": Fehler
   und Rückschritte bleiben stehen.
7. **Geheimnisse nie ins Protokoll.** Passwörter, Schlüssel, Tokens, Sitzungscookies, Karten-
   und Kontonummern werden geschwärzt (`[GESCHWÄRZT]`) oder gar nicht erst aufgenommen. Ist
   ein Geheimnis im Rohmaterial sichtbar, gilt es als abgeflossen und wird erneuert
   (`malware-cleanup-guide`, Schritt 4).
8. **Anonymisieren vor Cloud-Agenten.** Siehe `rescue-intake`; die Ersetzungstabelle bleibt
   lokal und liegt nicht im Protokoll, das weitergegeben wird.
9. **Negativbefunde zählen.** Was geprüft wurde und nichts ergab, steht ebenfalls drin,
   mit dem Hinweis, dass das Ergebnis nur für den geprüften Umfang gilt.

## Vorlage `notes.md`

```text
Fall-ID: ...        Bearbeiter/in/Agent: ...        Modus: A / B
Uhr des Zielgeräts weicht ab um: ... (gemessen UTC <zeit>)

| Nr | UTC | Typ | Inhalt | Quelle/Beleg | Sicherheit |
|----|-----|-----|--------|--------------|------------|
| 1  | ... | Beobachtung | Dienst "X" startet aus Temp-Ordner | evidence/services.txt Z. 41 | gesichert |
| 2  | ... | Deutung | könnte Persistenz sein | Nr. 1 | wahrscheinlich |
| 3  | ... | Handlung | Dienst deaktiviert, Aufgabe notiert | actions.md #3 | -- |

Offene Fragen: ...
Nicht geprüft: ...
```

## Vorlage `actions.md`

```text
#   UTC   Änderung (konkret)   Zustand vorher   Backup/Abbild (Prüfsumme)   Bestätigt durch   Ergebnis   Zustand nachher   Rückweg
```

## `summary.md` für die Eigentümerin oder den Eigentümer

Einfache Sprache, ohne Fachwörter, in dieser Reihenfolge: Was war los (so weit bekannt) ·
Was wurde getan · Was ist jetzt der Zustand · Was bleibt offen oder unsicher · Was ist jetzt
zu tun (Passwörter, Updates, Backups, Beobachtung) · Wo liegen die Unterlagen und wann
werden sie gelöscht. Keine Zusicherung der Art „das Gerät ist sauber"; stattdessen sagen, was
geprüft wurde und was nicht.

## Abschluss

Fall erst schließen, wenn: Handlungsprotokoll vollständig, Prüfsummen notiert, Geheimnisse
geschwärzt, Zusammenfassung übergeben, Aufbewahrung oder Löschung vereinbart, Wechselmedium
als berührt gekennzeichnet.
