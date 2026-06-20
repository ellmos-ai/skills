---
name: academic-study-control
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-06-20
updated: 2026-06-20
description: >
  Einsetzen, wenn Studienverwaltung, Semesterplanung, Modulpriorisierung,
  Fristen, Prüfungsanmeldungen oder institutionelle Mails geprüft, geplant
  oder in Erinnerungen überführt werden sollen. Koordiniert Webrecherche,
  lokale Statusdateien und optionale Kalender- und Mail-Integration.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: education
tags: [studium, semester, fristen, pruefung, planung, kalender, mail, hochschule]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Academic Study Control

## Übersicht

Steuere Studium und Fristen mit Quellenprüfung, Datenschutz und realistischer
Planung. Dieser Skill ist institution- und LMS-neutral: Platzhalter (in spitzen
Klammern) werden in der ersten Nutzung durch den Agent an den konkreten Kontext
angepasst.

## Konfiguration

| Platzhalter | Beispielwert | Bedeutung |
|---|---|---|
| `<HOCHSCHULE>` | Universität A, TU Berlin | Offizieller Name der Hochschule |
| `<LMS>` | ILIAS, Canvas, Stud.IP | Lernmanagementsystem |
| `<MODUL_PREFIX>` | MM, MF, MO | Kürzel für Modulbezeichnungen |
| `<STATUS_DATEI>` | STATE.md, SEMESTER.md | Lokale Statusdatei der Studierenden |
| `<INDEX_DATEI>` | LLM_INDEX.md, INDEX.md | Lokale Indexdatei |
| `<KALENDER>` | Google Calendar, iCal | Kalenderanwendung (optional) |
| `<MAIL>` | Gmail, Outlook, Thunderbird | Mailprogramm oder -connector (optional) |

## Ablauf

1. **Ziel klären:** Semesterplan, Wochenplan, Prüfungsanmeldung, Rückmeldung,
   Fristencheck, Mailcheck, Modulwechsel oder Erinnerungen.
2. **Lokale Lage prüfen:** `<STATUS_DATEI>`, `<INDEX_DATEI>`, relevante
   Modulordner, vorhandene Pläne und Originaldokumente der Hochschule.
3. **Aktuelle institutionelle Lage live prüfen:** offizielle Webseiten der
   `<HOCHSCHULE>`, Prüfungsamt, `<LMS>`-Ankündigungen und — sofern verfügbar
   und beauftragt — institutionelle Mails.
4. **Zeitbezug absolut notieren:** heutiges Datum, Semester, Fristdatum, Quelle,
   Abrufdatum.
5. **Entscheidung oder Plan ableiten** — nicht nur Links oder Informationen
   sammeln.

## Recherche

- Für aktuelle Informationen immer Webrecherche oder Originaldokumente nutzen.
  Termine, Prüfungsformen, Rückmeldezeiträume, Gebühren und Ankündigungen
  ändern sich regelmäßig.
- Bevorzugte Quellen: offizielle Seiten der `<HOCHSCHULE>`, Fakultätsseiten,
  Prüfungsamt, Modulhandbuch, Prüfungsportal, `<LMS>` und offizielle
  Hochschulmails.
- Bei Loginbedarf Computer-Use oder Browser-Steuerung einsetzen, aber
  Authentifizierung beim Nutzenden lassen. Niemals Credentials, MFA-Codes oder
  Sessiondaten speichern.
- `<MAIL>` nur nutzen, wenn ein passender Connector oder explizit bereitgestellte
  Mailinhalte verfügbar sind. Suche eng formulieren (Absender der Hochschule,
  Modulcodes, Prüfungsamt, Rückmeldung, Fristbegriffe).
- Quellenkonflikte offen markieren und die offiziellere oder neuere Quelle
  bevorzugen.

## Planen

Baue Planungen mit Puffer:

1. Pflichttermine und harte Fristen zuerst.
2. Prüfungs- und Abgabentermine rückwärts planen.
3. Module nach Aufwand, Risiko, Vorwissen und Prüfungsnähe priorisieren.
4. Pro Woche realistische Lernblöcke setzen, inklusive Wiederholung und freier
   Puffer.
5. Planänderungen begründen: was fällt weg, was rückt vor, welches Risiko
   entsteht.
6. Ergebnis in einer kompakten Tabelle ausgeben:
   `Datum | Aufgabe | Quelle | Status | Nächster Schritt`.

## Erinnerungen und Kalender (optional)

Wird nur genutzt, wenn der `<KALENDER>`-Connector verfügbar ist und explizit
beauftragt wurde:

- Erstelle Erinnerungen mit Vorwarnzeiten: harte Frist, 7 Tage vorher, 2 Tage
  vorher und am Vortag (anpassbar).
- Änderungen im Kalender vor dem Schreiben knapp bestätigen lassen, sofern die
  Handlung nicht eindeutig beauftragt ist.
- Keine Frist übernehmen, bevor sie aus offizieller Quelle oder lokalem
  Originaldokument bestätigt wurde.

## Mail- und Portalcheck (optional)

Bei Aufträgen wie „prüf mal Hochschulmails" oder ähnlichem:

1. Institutionelle Mails nach relevanten neuen Nachrichten durchsuchen.
2. Offizielle Terminseiten und Modul-/Prüfungsseiten prüfen.
3. `<LMS>` nur bei Bedarf und mit Nutzenden-Login öffnen.
4. Änderungen als Delta ausgeben: neu, geändert, unverändert, unklar.
5. Nächste Aktionen nennen: anmelden, herunterladen, nachfragen, planen,
   erinnern.

## Datenschutz

- Immatrikulationsnummern, Bescheinigungen, Mailvolltexte, Gesundheitsdaten
  und Prüfungsdaten nicht unnötig ausgeben.
- Bei Dateischreibungen zuerst fragen, wenn sensible Inhalte in neue
  Planungsdateien übernommen würden.
- In Antworten genügen abstrahierte Angaben: „Rückmeldefrist endet am …" —
  keine kompletten Mail- oder Dokumentzitate.

## Offene Punkte

- `author`-Feld folgt der `.SKILLS`-Konvention (Repo-Autorenschaft); der Wert
  enthält einen Eigennamen, ist aber für die Repo-Öffentlichkeit intendiert.
- Tool-Integrationen (`<MAIL>`, `<KALENDER>`) sind bewusst optional — der Skill
  funktioniert vollständig auch ohne sie.
