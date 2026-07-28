---
name: store-welle-usertest
version: 1.0.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-07-23
updated: 2026-07-28
description: >
  Führt einen Windows-Store-Wellentest mit dem User durch: Release-Apps
  nacheinander öffnen, Live-Feedback verlustfrei in die jeweilige Aufgabenliste
  übernehmen, ein nummeriertes Asset-Review vorbereiten, Submission-Sheets
  erstellen und nach der Einreichung Store-IDs zurückschreiben. Nutzen bei
  Store-Wellentests, gemeinsamen App-Reviews und Microsoft-Store-Einreichungen.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [windows-store, user-test, release, msix, submission, wave]
language: de
status: active

dependencies:
  tools: [powershell]
  services: [Microsoft Partner Center]
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: "session://store-wave-user-test/2026-07-23"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-07-23"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Store-Wellen-Testzyklus mit dem User

## Zweck und Rollenverteilung

Behandle die Zeit des Users als seriellen Engpass jeder Store-Welle: Nur der
User kann final testen, Verbesserungen ansagen und im Partner Center
einreichen. Bereite alle anderen Schritte so vor, dass pro App nur der
eigentliche Test und die nötigen Entscheidungen offenbleiben. Übernimm dabei
die Rolle des Cockpits: öffnen, protokollieren, vorbereiten und zurückschreiben.

## Konfiguration

Ermittle die konkreten Pfade aus der lokalen Projekt- oder Pipeline-Dokumentation.
Nutze diese generischen Bezeichnungen:

| Zweck | Generischer Ort |
|---|---|
| Wellen-Liste | `<workspace>/STORE-WELLE-<N>_*.txt` |
| Pipeline-Registry | `<software-pipeline>/WINDOWS_STORE_PIPELINE.md` und `releases.json` |
| Projekt-Feedback | `AUFGABEN.txt` oder die lokale Aufgabenquelle des Projekts |
| Review-Dokument | `<software-pipeline>/_STORE/WELLE<N>_ASSETS_REVIEW.html` |
| Submission-Sheet | `<project>/releases/windowsstore/SUBMISSION-SHEET.md` |
| Lock-Regel | Projektlokale Lock-Policy; vorhandene fremde Locks immer beachten |

Verwende in Cloud-Sync-Ordnern das dafür vorgesehene Dateiwerkzeug. Freie
rekursive Shell-Scans können dort timeouten oder an Cloud-Locks scheitern.

## Phase A — Apps sequenziell mit dem User testen

1. Übernimm die App-Reihenfolge aus der Wellen-Liste.
2. Prüfe vor jeder Änderung die projektlokale Lock-Policy. Setze einen eigenen
   eng begrenzten Lock, wenn die Policy dies verlangt, und entferne ihn nach
   Abschluss dieses Projektscopes.
3. Löse den kanonischen Release-Pfad auf und öffne ausschließlich die
   Release-EXE, die dem einzureichenden Paket entspricht. Starte weder einen
   Quelllauf noch einen ungeprüften Dev-Build.
4. Verifiziere nach dem Start Prozess-ID und Executable-Pfad. Melde dem User
   erst danach, dass die App geöffnet ist.
5. Übernimm diktiertes Feedback sofort und bedeutungstreu in die Aufgabenquelle
   des Projekts. Nutze einen datierten Block
   `[WELLE-<N>-USERTEST YYYY-MM-DD]` mit nummerierten Punkten `U1`, `U2`, ...
6. Stelle nur bei echter Mehrdeutigkeit eine Rückfrage. Sammle Feedback nicht
   ausschließlich im Chat.
7. Schließe den Projektscope sauber und fahre mit der nächsten App fort.
8. Setze gefundene Punkte in getrennten Projektläufen um. Der User testet
   anschließend nur die Fixes erneut.

## Phase B — Asset-Review vorbereiten

Erstelle selbst oder mit einem ausdrücklich verfügbaren, eng begrenzten Worker
eine HTML-Datei mit Icons und Store-Screenshots der Welle:

- Nummeriere Icons als `I{App-Nr}.{lfd}` und Screenshots als
  `S{App-Nr}.{lfd}`. Die App-Nummer folgt der Wellen-Liste.
- Zeige Nummer, Vorschau und vollständigen Quellpfad.
- Suche nur in den dokumentierten Asset-Orten des Projekts, beispielsweise
  `store_assets/`, `releases/windowsstore/screenshots/` oder
  `README/screenshots/store/`.
- Bette unterstützte Bilder per `file:///` ein. Liste nicht darstellbare
  `.ico`-Dateien nur mit Nummer und Pfad.
- Markiere fehlende Assets sichtbar und schließe mit einer Übersichtstabelle.
- Öffne das fertige Dokument für den User.
- Übernimm Korrekturansagen wie „I9.1 tauschen“ in die Aufgabenquelle der
  betroffenen App.

Wenn kein Worker verfügbar oder erlaubt ist, führe diese Phase sequenziell im
Hauptlauf aus.

## Phase C — Submission-Sheets erstellen

Erstelle pro App ein `SUBMISSION-SHEET.md` in der Reihenfolge des Microsoft
Partner Center:

1. App-Name und Reservierung
2. Pricing und Availability
3. Properties und Kategorie
4. Age Ratings beziehungsweise IARC-Stichpunkte
5. Paketpfad und Version
6. Store Listing Deutsch
7. Store Listing Englisch
8. Support- und Privacy-URLs
9. Notes for Certification

Übernimm Angaben ausschließlich aus vorhandenen Projektquellen. Erfinde keine
Store-Texte, Altersfreigaben, URLs oder Produkteigenschaften. Markiere fehlende
Angaben mit `FEHLT`. Ergänze im Kopf das Feld `STORE-ID: ________`.

## Phase D — Einreichung und Rückschreibung

1. Öffne für die Einreichung das Submission-Sheet der jeweiligen App.
2. Lasse den User die Felder im Partner Center eintragen.
3. Nimm die vergebene Store-ID entgegen.
4. Schreibe die ID in alle kanonischen Projektflächen zurück, typischerweise:
   - `SUBMISSION-SHEET.md`,
   - `store_package.json`, sofern das Schema ein Feld vorsieht,
   - die Pipeline-Registry mit Status `EINGEREICHT`,
   - die Wellen-Liste.
5. Lies die aktualisierten Werte zurück und melde die konkreten Ziele.

## Sicherheits- und Qualitätsgates

- Teste den tatsächlichen Release-Stand, nicht einen bequemeren Quellstart.
- Prüfe unbekannte Frozen-EXEs vor dem Start auf Laufzeit-Installationen oder
  Selbstaufrufe über `sys.executable`. In einer PyInstaller-EXE kann ein
  pip-Fallback sonst dieselbe EXE rekursiv neu starten.
- Wenn sich eine App unkontrolliert vervielfältigt, ermittle zuerst den exakten
  Executable-Pfad und die zugehörigen PIDs. Beende nur diese Prozesse in einem
  begrenzten Retry-Zyklus. Beende keine Prozesse allein anhand eines
  mehrdeutigen Namens und keine fremden Prozesse.
- Beachte fremde Locks. Entferne nur den eigenen Lock.
- Nutze einen optionalen Worker nur für einen klar begrenzten Scope. Die
  Hauptinstanz behält Integration und Endkontrolle.
- Verifiziere alle geschriebenen Store-IDs und Statuswerte per Readback.

## Trigger-Beispiele

- „Wir machen jetzt Welle 2 – öffne mir die Apps nacheinander.“
- „Ich teste die Store-Apps, nimm meine Punkte auf.“
- „Zeig mir alle Icons und Screenshots der Welle zum Prüfen.“
- „Bereite die Submission-Sheets für die nächste Store-Welle vor.“

## Verwandte Skills

- `bugsweep` und `bugfix-protocol` für die Umsetzung gefundener Fehler
- ein lokaler Desktop- oder Release-Runner zum kontrollierten Öffnen der Apps
- `workflow-extract`, wenn aus dem wiederholten Ablauf eine Automation werden soll

## Changelog

### 1.0.0 (2026-07-28)

- Session-Ablauf als portablen Store-Wellen-Testzyklus zertifiziert.
- Frontmatter, Provenance, Privacy-Gate und Prozesssicherheit ergänzt.
- Parallel-Worker als optionalen, eng begrenzten Ausführungsweg formuliert.
