---
name: system-onboarding
version: 1.2.0
type: skill
author: ellmos contributors
created: 2026-05-16
updated: 2026-07-29
description: >
  Anbieterneutrales Onboarding-Protokoll für einen neuen, neu aufgesetzten
  oder ausgetauschten Arbeitsplatzrechner. Es richtet
  Betriebssystemvoraussetzungen, Agentenlaufzeiten, gemeinsame Regelflächen,
  portable Skills, verifizierte Konfiguration und Nachweise nach der
  Installation ein, ohne Zugangsdaten, private Prompts oder
  host-spezifische Konfiguration in ein Repository zu kopieren.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [onboarding, setup, agent-runtimes, windows, macos, verification, sync]
language: de
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: "internal onboarding protocol (sanitized for portable publication)"
  origin_version: "1.2.0"
  last_sync_from_origin: "2026-07-29"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="system-onboarding banner">

# System-Onboarding

Nutze dieses Protokoll, um einen neuen oder neu aufgesetzten Arbeitsplatzrechner
für lokal-first Agentenarbeit einzurichten. Es ist eine Anleitung für Reihenfolge
und Verifikation, kein Installer und keine Quelle für Zugangsdaten. Ermittle
produktspezifische Anweisungen anhand der aktuellen Dokumentation des jeweiligen
Anbieters, bevor du ein Live-System änderst.

## Aktivierung

Verwende den Skill für einen neuen Arbeitsplatzrechner, ein neu installiertes
Betriebssystem, ein Ersatzgerät oder die kontrollierte Wiederherstellung einer
einzelnen Agentenlaufzeit. Ermittle zuerst Betriebssystem, Ziellaufzeit,
zuständige Person, gemeinsame Regelfläche und ob ein vollständiger Neuaufbau
oder eine begrenzte Komponentenreparatur gewünscht ist. Unterstelle nicht, dass
eine von einem Host kopierte Konfiguration auf einem anderen sicher oder
unterstützt ist.

## Geordneter Arbeitsablauf

1. Richte Betriebssystemupdates, Git, authentifizierte Quellcodeverwaltung,
   Python und bei Bedarf die aktuell unterstützte Node.js-LTS-Version ein.
2. Installiere nur die angeforderten Agentenlaufzeiten über deren unterstützte
   Installer. Schließe die nativen Anmeldeabläufe ab, ohne Token in
   Projektdateien abzulegen.
3. Erstelle lokale Konfigurationswurzeln und lade eine ausdrücklich ausgewählte,
   kanonische Regelfläche. Führe Vorlagen zusammen; überschreibe vorhandenen
   lokalen Zustand niemals blind.
4. Installiere portable Skills sowie MCP- oder Plugin-Konfiguration nur über die
   jeweils dokumentierten Bereitstellungsverfahren. Behandle die
   Konfigurationsformate der Anbieter als voneinander verschieden.
5. Richte gemeinsame Synchronisierung erst ein, nachdem die lokale Laufzeit
   funktioniert. Teile bereinigte Verträge und Belege, nicht Zugangsdaten,
   vollständige Prompts oder maschinenlokale Pfade.
6. Stelle Scheduler oder Automationen nur über deren unterstützte native
   Oberfläche wieder her. Bewahre den vorherigen Zustand und lasse neue
   Aufgaben deaktiviert, bis die zuständige Person die Aktivierung freigibt.
7. Führe die passenden Prüfungen nach der Installation aus und schreibe einen
   lokalen Beleg, der Installation, Konfiguration, Scheduler-Registrierung und
   erfolgreiches Ergebnis unterscheidet.

Lies nur die zum Zielsystem passende Referenz:

- [Übersicht](references/overview.md) für Grenzen und Datenablage;
- [Windows-Checkliste](references/windows-checklist.md) für Windows;
- [macOS-Checkliste](references/mac-checklist.md) für macOS; und
- [Prüfung nach der Installation](references/post-install.md) für Verifikation
  und Wiederherstellung.

## Grenzen

- Veröffentliche niemals Zugangsdaten, Wiederherstellungscodes, private Prompts,
  Kontokennungen oder Rohprotokolle in einem gemeinsamen Repository oder
  Synchronisationsordner.
- Halte virtuelle Umgebungen, Abhängigkeits-Caches und große
  Laufzeitartefakte aus cloud-synchronisierten Projektordnern heraus.
- Erkläre eine kopierte Konfiguration nicht zur maßgeblichen Quelle. Der
  Zielhost muss seinen eigenen unterstützten Zustand ermitteln und per Readback
  bestätigen.
- Registriere einen Zeitplan nicht allein deshalb, weil eine Aufgabendatei
  existiert. Native Registrierung und Ergebnisnachweis sind getrennte
  Anforderungen.
- Inventarisiere bei der Reparatur eines bestehenden Hosts dessen aktuellen
  Zustand und Sperren, bevor du Konfiguration änderst.

## Abschlussnachweis

Ein vollständiger Onboarding-Beleg hält Zielbetriebssystem, ausgewählte
Laufzeiten, verifizierte Versionen, geladene kanonische Regelreferenzen,
ausdrücklich bereitgestellte Skills oder Erweiterungen, nicht unterstützte
Fähigkeiten und aufgeschobene Nutzerentscheidungen fest. Ein erfolgreicher
Befehlsabschluss allein belegt weder, dass eine Anwendung ihre neue
Konfiguration geladen hat, noch dass eine geplante Aufgabe ihr beabsichtigtes
Ergebnis erreicht hat.

## Änderungsprotokoll

### 1.2.0 (2026-07-29)

- Die wiederverwendbare Onboarding-Reihenfolge und Plattformreferenzen nach
  Entfernung host-spezifischer Pfade, Kontodetails und privaten
  Betriebsmaterials in den öffentlichen Skill-Katalog portiert.
