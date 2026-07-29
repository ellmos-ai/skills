---
language: es
---

> **Español** — [Español] Documentación completa traducida al español para la habilidad `decision-avatar`.



> **English Translation** — Official English version of `decision-avatar`.


# Decision Avatar

## Zweck

Dieser Skill bildet keine Person nach. Er stellt ein überprüfbares Verfahren
bereit, um bei wiederkehrenden Entscheidungstypen eine wahrscheinliche Präferenz
aus echten, autorisierten Belegen abzuleiten.

Nutze ihn nur, wenn ein lokales Entscheidungsprofil vorhanden und dessen Nutzung
für die aktuelle Aufgabe zulässig ist. Ohne Profil liefert der Skill keine
stellvertretende Entscheidung.

Die Nutzung gilt nur dann als autorisiert, wenn Auftrag, geltende Agentenregel
oder Profilmetadaten den aktuellen Zweck ausdrücklich erlauben. Bloße
Erreichbarkeit einer Profildatei ist keine Einwilligung.

## Kernprinzipien

1. **Beleg vor Vermutung.** Direkte Aussagen und bestätigte Entscheidungen wiegen
   stärker als abgeleitete Muster.
2. **Vorhersage ist keine Aussage der Person.** Agentenausgaben dürfen nicht als
   neue Primärbelege in das Profil zurückfließen.
3. **Entscheiden ist nicht Ausführen.** Eine Empfehlung kann bestimmt sein, obwohl
   ihre Umsetzung zusätzliche Autorität braucht.
4. **Stille Zustimmung ist kein Feedback.** Ausbleibender Widerspruch bestätigt
   keine Vorhersage.
5. **Profile bleiben lokal und privat.** Keine personenbezogenen Daten, Secrets
   oder sensiblen Inhalte in geteilte Skill-Dateien übernehmen.

## Portables Profilmodell

Die Dateinamen sind frei konfigurierbar; benötigt werden nur diese Rollen:

| Rolle | Inhalt |
|---|---|
| Methodik | Evidenzstufen, Datenschutz und Kalibrierungsregeln |
| Belegte Präferenzen | direkte Aussagen und bestätigte Entscheidungen |
| Hypothesen | abgeleitete Regeln mit Konfidenz und Quellen |
| Aktionen | aufgrund einer Vorhersage getroffene Handlungen |
| Feedback | Bestätigung, Korrektur oder Ablehnung durch die Person |

Projektbezogene, aktuellere Entscheidungen haben Vorrang vor allgemeinen
Präferenzen.

Jeder verwertete Beleg sollte mindestens enthalten:

```text
Quellen-ID:
Datum:
Entscheidungstyp und Gültigkeitsbereich:
Status: bestätigt/korrigiert/widerrufen
Gültig bis: <optional>
```

Widerrufene, abgelaufene oder außerhalb ihres Gültigkeitsbereichs liegende Belege
nicht verwenden. Bei widersprüchlichen bestätigten Belegen gewinnt zunächst der
spezifischere und danach der aktuellere. Bleibt der Konflikt bestehen, Konfidenz
auf „niedrig“ setzen und eskalieren.

## Entscheidungsloop

### 0. Lokale Vorrangregel prüfen

Gibt es für das aktuelle Projekt oder den konkreten Entscheidungstyp eine
bestätigte Regel, nutze diese und dokumentiere ihre Quelle.

### 1. Echte Evidenz suchen

Nur Belege verwenden, die nach der lokalen Methodik zulässig sind. Aufgabenlisten,
Agentenprotokolle, frühere Avatar-Antworten und Argumente der aktuellen Sitzung
sind keine Aussagen der Person.

### 2. Vorhersage bilden

Ergebnis stets mit Begründung und einer von drei Stufen ausgeben:

- **hoch:** mehrere direkte, konsistente und einschlägige Belege,
- **mittel:** plausibles Muster mit begrenzter oder indirekter Evidenz,
- **niedrig:** neuartige Lage, widersprüchliche Belege oder kein belastbares
  Muster.

Folgenreiche Entscheidungen sind nicht automatisch „niedrig“. Konfidenz misst
die Evidenz für die Präferenz, nicht die Reichweite der späteren Ausführung.

### 3. Modus trennen

| Modus | Ergebnis | Seiteneffekt |
|---|---|---|
| Vorhersagen | wahrscheinliche Position + Belege + Konfidenz | keiner |
| Entscheiden | konkrete Wahl + Begründung + Konfidenz | keiner |
| Handeln | autorisierte, sichere Umsetzung + Aktionsprotokoll | möglich |

Im Handlungsmodus gelten zusätzlich die Autoritäts- und Sicherheitsregeln der
Runtime. Niedrige Konfidenz oder fehlende Ausführungsbefugnis führt zur
Eskalation, nicht zur stillen Ausführung.

### 4. Feedback kalibrieren

Nach echtem Feedback:

1. Vorhersage als bestätigt, korrigiert oder abgelehnt markieren.
2. Optional eine Bewertungsskala erfassen.
3. Unterschied zwischen Richtungsfehler und Zuschnittfehler festhalten.
4. Hypothese und Konfidenz anpassen.
5. Nur echte Rückmeldung in die belegten Präferenzen übernehmen.

## Ausgabeformat

```text
Entscheidungstyp:
Modus:
Wahrscheinliche Präferenz:
Konfidenz:
Zulässige Belege:
Gegenbelege oder Unsicherheit:
Ausführung autorisiert: ja/nein
Nächster Schritt:
```

In Ausgaben nur redigierte Quellen-IDs und die für die Entscheidung notwendige
Belegzusammenfassung nennen. Keine privaten Aussagen, absoluten Profilpfade oder
sensiblen Rohdaten wiedergeben.

## Grenzen

- Keine Diagnostik oder Behauptung über innere Zustände einer Person.
- Keine Nutzung eines Profils außerhalb seines erlaubten Zwecks.
- Keine automatische Übernahme von Agentenannahmen als Personenwissen.
- Keine Ausführung allein aufgrund einer Vorhersage, wenn dafür neue Autorität
  erforderlich wäre.

## Registro de Cambios

### 1.0.0 (2026-07-28)
- Feedback-Präkognition, Konfidenzkalibrierung und Provenienztrennung aus einer
  persönlichen Avatar-Konfiguration als eigenständiges, portables Protokoll
  extrahiert.
- Autorisierung, Beleglebenszyklus, Konfliktauflösung und redigierte Ausgabe
  operationalisiert.