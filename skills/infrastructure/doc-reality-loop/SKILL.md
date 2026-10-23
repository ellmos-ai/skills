---
name: doc-reality-loop
version: 0.1.0
type: protocol
author: ellmos contributors
created: 2026-10-23
updated: 2026-10-23
description: >-
  Prüft Tatsachenaussagen in Dokumentation gegen belegte Wirkung und führt
  bestätigte Korrekturen durch einen unabhängigen Review mit erneuter Messung.
standalone: false
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: infrastructure
language: de
status: draft
visibility: public
provenance:
  origin: custom
  origin_path: https://github.com/ellmos-ai/open-ocean
  origin_version: 3f2d4f306f4fc57ad5bb7596d10312c8a8da1cfa
  last_sync_from_origin: 2026-10-23
---

# Dokumentation mit der tatsächlichen Wirkung abgleichen

Dieser Katalogadapter erschließt den gemeinsamen **doc-reality-loop** aus Ocean.
Die Methode wird dort gepflegt. Er benötigt die externen gepinnten Quellen
und die Autorität des jeweiligen Produkts für Messung, Korrektur und Abnahme.

## Quelle auflösen

Lies [source-pin.v1.json](source-pin.v1.json). Ermittle die deutsche oder englische
Workflowdatei und den Vertrag am dort genannten festen Commit. Vergleiche
SHA-256 über die exakten Git-Blobs, bevor du deren Inhalt verwendest; ein
Windows-Checkout kann andere Zeilenenden haben. Bei unerreichbarer Quelle oder
Hashabweichung bleibt der Methodenstand ungeprüft. Keine bewegliche Quelle
`main` als Ersatz verwenden.

## Auftrag ausführen

Führe dann die passende Variante des **vollständig gelesenen** Shared-Workflows
aus: `help`, `root`, `requirements` oder `freshness`. Produktpfade, Register,
Intervalle, Werkzeuge und Befugnisse kommen vom beauftragenden Consumer.
Fehlende Host-/Instanz-/Versions-/Wirkungsbelege bleiben `unknown`.
Die Aufnahme dieses Skills erweitert den Auftrag und seine Schreibrechte nicht.

Der Shared-Vertrag unterscheidet Auslöser, Taskanlage, tatsächliche Ausführung,
Textkorrektur, unabhängigen Review und erneute Messung. Taskstatus und
Dispatchmarker beweisen keine spätere Stufe. Offene Sollanforderungen bleiben
erhalten; Archivierung braucht Leser-/Linkprüfung und Rückweg. Der referenzierte
Prüfer kontrolliert die Form der Belegkette und ersetzt keine Prüfung der Belege.

## Produktadapter

Für BACH gilt zusätzlich dessen Produktadapter unter
`system/skills/workflows/doc-reality-loop-bach.md`, sobald dieser im konkret
verwendeten BACH-Stand integriert und verfügbar ist. Ein fehlender Adapter wird
als offene Integration erfasst. Für andere Consumer gilt ihr eigener belegter
Adapter; dieser Katalogeintrag installiert oder startet keinen Consumer.

English: [SKILL.en.md](SKILL.en.md).

## Anwendungsbeispiel

Auftrag: „Prüfe die Versionsangaben des Handbuchs gegen den bezeichneten Release.“
Lade die gepinnte Methode und wähle freshness. Erfasse jede Versionsaussage
mit Quelle und Leser, vergleiche sie mit dem tatsächlichen Releasebeleg und
melde nicht erreichbare Oberflächen als unknown. Ist nur Analyse beauftragt,
liefere Unterschiede und Korrekturvorschläge; ändere das Handbuch erst nach
entsprechender Autorisierung.

## Changelog

- 0.1.0 (2026-10-23): Zweisprachiger Katalogadapter mit festem Ocean-Quellpin.
