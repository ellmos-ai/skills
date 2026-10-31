---
name: rescue-intake
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: >
  Aufnahme eines Rettungsfalls für einen Laptop oder PC mit Verdacht auf Schadsoftware oder
  Fehlfunktion: Eigentum und Einwilligung bestätigen, den Betriebsmodus wählen (A: sammeln
  und auf einem sauberen Rechner auswerten, B: Agent vor Ort, nur aus einem Live-Boot),
  verhindern, dass echte Konten auf dem Zielrechner angemeldet werden, und festlegen, was
  anonymisiert wird, bevor Belege zu einem Cloud-Agenten gehen. Immer als Erstes nutzen,
  bevor irgendetwas auf dem Zielgerät läuft.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [incident-response, endpoint, intake, consent, malware, rescue, privacy, defensive]
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
  origin_path: "skills/infrastructure/rescue-intake/"
  origin_version: "1.0.0"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# rescue-intake (Deutsch)

Erster Schritt jedes Rettungsfalls. Rein defensiv: Es geht darum, ein **eigenes oder
ausdrücklich freigegebenes** Gerät wieder in einen verlässlichen Zustand zu bringen. Der
Skill erlaubt weder Zugriff auf fremde Geräte noch Angriffs- oder Umgehungsmaßnahmen.
Danach folgt `endpoint-triage`; Bereinigung und Härtung regeln `malware-cleanup-guide` und
`os-hardening-baseline`, die Dokumentation `incident-notes`.

## 1. Eigentum und Einwilligung (Pflicht vor dem Start)

Frage und halte schriftlich fest (Antworten in `intake.md`, Vorlage unten):

- Wem gehört das Gerät? Ist diese Person erreichbar und einverstanden?
- Ist es **privat**, oder verwaltet eine Firma, Schule oder Behörde das Gerät? Dann nicht
  anfassen, solange deren IT nicht zugestimmt hat; Meldung an sie ist der richtige Weg.
- Gehört es einer anderen Person (Familie, Freunde)? Nur mit deren ausdrücklicher
  Zustimmung und nachdem ihr erklärt wurde, welche Daten angesehen werden. Bei Geräten
  Minderjähriger zählt die Zustimmung der Sorgeberechtigten.
- Bestehen Zweifel am Eigentum oder an der Einwilligung (Gerät „gefunden", Gerät einer
  Ex-Partnerin, Gerät mit fremdem Konto): **abbrechen.** Der Skill hilft nicht, fremde
  Geräte zu untersuchen.

Erklärung an die Eigentümerin oder den Eigentümer, bevor es losgeht: Auswertungen enthalten
persönliche Daten (Programme, Verbindungen, Kontonamen, Dateipfade). Was gesammelt wird,
wo es liegt und wann es gelöscht wird, wird vorher gesagt.

## 2. Ziel und Lage

Was ist passiert, seit wann, was wurde zuletzt getan (Programm installiert, Link geöffnet,
Anhang, Anruf, Fernwartung)? Gibt es Hinweise auf abgeflossene Zugangsdaten oder Geld?
Falls ja: **Zugangsdaten werden später von einem sauberen Gerät aus geändert**, nicht vom
Zielgerät (siehe `malware-cleanup-guide`). Läuft Datenverschlüsselung mit Lösegeldforderung:
Gerät vom Netz trennen, nicht zahlen, nicht weiterarbeiten, Fall an
`malware-cleanup-guide` übergeben.

## 3. Modus wählen

| Modus | Was läuft wo | Wann |
|---|---|---|
| **A: Sammeln und auswerten (Standard)** | Auf dem Zielrechner läuft nur ein **schreibgeschütztes Sammelskript**, das ausschließlich in einen Fallordner auf dem Wechselmedium schreibt. Die Auswertung durch Agenten geschieht auf einem **sauberen Rechner.** | Verdacht auf Infektion; Zustand des Geräts unklar |
| **B: Agent vor Ort** | Der Agent läuft auf dem Zielrechner, **nur aus einem vom Wechselmedium gebooteten Live-System**, das die interne Platte höchstens lesend einbindet. | Offline-Prüfung der Platte; Gerät bootet nicht mehr |

Regeln für beide Modi:

- **Keine Anmeldung echter Konten auf dem Zielrechner.** Weder Agenten-Konten (Claude,
  Codex, Gemini …) noch E-Mail, Cloud, Bank, Passwortmanager. Ein womöglich kompromittiertes
  Gerät sieht jede Eingabe und jeden Sitzungstoken. Wird dennoch eine Anmeldung gebraucht,
  nur mit einem eigens angelegten, eng begrenzten, kurzlebigen Zugang, der danach widerrufen
  wird -- Modus B aus einem Live-System ist der Normalfall dafür.
- Im Zweifel Modus A. Ein Agent „vor Ort" auf dem laufenden, unsauberen System ist kein
  vorgesehener Modus.
- Das Wechselmedium bekommt keine Zugangsdaten und wird danach als potenziell berührt
  behandelt (nicht an einem sauberen Rechner einfach starten, sondern ansehen und scannen).

## 4. Belege und Datenschutz

- Belege (Sammelordner, Logs) bleiben zunächst lokal auf dem Wechselmedium bzw. dem sauberen
  Rechner.
- **Vor der Übergabe an einen Cloud-Agenten anonymisieren:** Benutzernamen, Rechnername,
  E-Mail-Adressen, Kontonamen, interne und öffentliche IP-Adressen, Seriennummern, Pfade mit
  Namen, Tokens und Schlüssel ersetzen (konsistente Platzhalter, damit Zusammenhänge
  erhalten bleiben). Die Ersetzungstabelle bleibt lokal. Kein Anonymisierer ist perfekt:
  Ergebnis vor dem Senden stichprobenartig lesen.
- Dateien selbst (verdächtige Programme) werden nicht ungefragt zu Online-Diensten
  hochgeladen; Hashwerte genügen meist für eine Recherche.
- Aufbewahrung: Fallordner erhalten, bis die Eigentümerin oder der Eigentümer zustimmt, ihn
  zu löschen. Das Wechselmedium mit Auswertungen verschlüsseln oder wegschließen.

## 5. Vorlage `intake.md`

```text
Fall-ID:            <z. B. fall-20261031-01>
Datum/Uhrzeit UTC:  <gemessen, nicht geschätzt>
Eigentümer/in:      <Name oder Kürzel>      Einwilligung: ja / nein   (wie belegt: ...)
Gerät:              <Typ, Betriebssystem, Baujahr>   Verwaltet von Dritten: nein / ja -> Stopp
Anlass/Symptome:    ...
Zuletzt getan:      ...
Verdacht auf abgeflossene Zugangsdaten/Geld: nein / ja (welche Dienste: ...)
Modus:              A / B   Begründung: ...
Echte Konten auf dem Zielgerät angemeldet: nein (Soll)
Anonymisierung vor Cloud-Agenten: ja / nein / nicht nötig
Nächster Schritt:   endpoint-triage
```

## Abbruch

Stopp und Rückfrage, wenn: Eigentum oder Einwilligung unklar, Gerät von Dritten verwaltet,
der Auftrag verlangt, Zugangsdaten anderer Personen zu beschaffen, Konten zu übernehmen
oder Schutzmechanismen eines Geräts zu umgehen, das nicht der Person gehört. Solche
Aufträge sind nicht Gegenstand dieses Skills.
