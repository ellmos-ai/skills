---
name: cloud-communication-protocols
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-01
updated: 2026-08-25
language: de
visibility: public
standalone: true
anthropic_compatible: true
category: infrastructure
tags: [ping-pong, agent-beam, listeners, cross-machine, sync-yard, coordination]
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
description: Dach-Skill für Cloud-gestützte Kommunikationsprotokolle zwischen Agenten auf unterschiedlichen Maschinen (Ping-Pong, agent-beam, Listener und künftige Protokolle). Nutzen, wenn Arbeit über Maschinen hinweg per gemeinsamem Sync-Ordner oder Message-Yard koordiniert wird.
---

<img src="banner.png" width="100%" alt="cloud-communication-protocols banner">

# cloud-communication-protocols

Familie von Protokollen, die zwei oder mehr Agenten auf unterschiedlichen
Maschinen über einen gemeinsamen, cloud-synchronisierten Ordner (den "Yard")
statt über einen direkten Kanal koordinieren lässt. Dieser Skill ist das
**Dach**: er sammelt die Protokolle, benennt, welches bewiesen ist, und
sperrt die, die noch Konzept sind.

## Wann nutzen

- Arbeit erstreckt sich über zwei oder mehr Maschinen (Verifikation,
  gespiegelte Setups, Piloten) und es gibt keinen direkten
  Agent-zu-Agent-Kanal.
- Ein gemeinsames Vokabular für Aufträge, Antworten, Takt und Eskalation
  über diese Maschinen hinweg wird gebraucht.

## Protokolle dieser Familie

### 1. Ping-Pong (bewiesen, Basisprotokoll)

Zwei oder mehr Worker mit versetzten geplanten Scans überbrücken die
Cloud-Sync-Latenz: jede Seite scannt den Yard nach an sie adressierten
Aufträgen, führt aus, hinterlässt die Antwort und kann Folgeaufträge für
die andere Seite ausstellen.

Kernregeln: nur im eigenen Slot schreiben, Belege für jede Aktion,
Idempotenz, keine Geheimnisse im Yard (nur öffentliche Schlüssel/
Fingerprints/Pfade), kooperative Fehler-Deltas, Readback-über-Log-Verifikation.

**Takt: adaptive Poll-Frequenz.** Die Taktsteuerung ist nicht Teil der
Payload-Regeln des Basisprotokolls, aber jede Implementierung braucht sie —
ein fester Poll-Intervall flutet entweder einen leeren Yard oder verpasst
frische Arbeit. Zwei Mechanismen gelten und müssen beide behandelt werden,
nicht implizit bleiben:

- **A — Selbstjustierend (Standard, keine Operator-Eingabe; das
  `cooldown`/Backoff-Muster).** Neuer Auftrag gefunden → direkt auf das
  schnellste Intervall springen (z. B. 15 min). Leerer Lauf → auf einer
  Leiter abkühlen: 4 aufeinanderfolgende leere Läufe → 30 min, 2 weitere →
  1 h, danach jede weitere leere Serie verdoppeln (2 h, 4 h, 8 h) bis zu
  einem harten Deckel (24 h, niemals höher). Den Leerlauf-Zähler und das
  aktuelle Intervall in einer kleinen State-Datei beim Worker persistieren
  (nicht im Konversationsgedächtnis), damit sie Neustarts überlebt; ein
  Taktwechsel bedeutet, den alten geplanten Job zu löschen und einen neuen
  im neuen Intervall anzulegen, Zähler übernommen. Vollständiges
  Referenzschema, State-Datei-Schema und weitere Loop-Typen (Burst,
  Wake-Assist): Begleit-Skill **`cron-tuner`**.
- **B — Peer-instruiertes Override.** Jede Seite darf den Takt der anderen
  Seite explizit im Auftragstext setzen — `CADENCE: match 15m`, um auf ein
  engeres Fenster zu synchronisieren, oder `CADENCE: pause 1h → 2h after 3
  empty`, um eine Seite mit planbarer Kopf-runter-Arbeit zu verlangsamen.
  Wer den Takt eines Peers ändert, bestätigt das neue Intervall im nächsten
  Delta (Readback gilt auch für Uhren).

Beide Mechanismen ändern nur die Reaktionszeit, niemals die
Basisprotokoll-Regeln (Slot-Disziplin, Belege, keine Geheimnisse). Ein
gegenseitiger `WAKE: <Grund>`-Kanal erlaubt Scans außerhalb des Zyklus als
Hinweis, niemals als Autorität; nach dem Lesen löschen.

Vollständige Spezifikation und Referenzbelege:
`dev-bricks/system-gap-master` → `docs/communications-protocols-skill.md`.

### 2. agent-beam (Konzept, gesperrt)

Für dringende Arbeit: ein Paket aus Prompt + Starter-Skript wird im
Ziel-Slot abgelegt, und ein Watcher auf der Zielmaschine startet damit
einen lokalen Agentenlauf — der Agent "landet" mit Auftrag und Starter und
beginnt sofort.

Gesperrt: benötigt einen signierten Starter-Vertrauensvertrag, einen
Quarantäne-/Review-Schritt und ausdrückliche Operator-Freigabe vor jeder
Aktivierung.

### 3. Listener / Ear-to-Ear-Listening (Konzept, gesperrt)

Watcher beobachten Trigger im Yard (Datei-Ankünfte, Flag-Dateien,
Registry-Änderungen) und starten Agenten auf der anderen Maschine.
"Ear-to-Ear": der Listener des einen Hosts beobachtet den Posteingang des
anderen Hosts.

Gesperrt: Debouncing-Regeln, Trigger-Whitelists je Slot und ein
Sicherheitsvertrag werden zuerst benötigt.

## Gemeinsame Invarianten (alle Protokolle)

- Der Yard ist Transport, niemals Arbeitsbereich und niemals
  Geheimnis-Speicher.
- Jede Aktion hinterlässt einen verifizierbaren Beleg; "erledigt" ohne
  Artefakt ist nicht erledigt.
- Fehlerbehandlung ist kooperativ: Fehler-Deltas mit Hypothese und
  Gegentest, Zweitmeinungen willkommen.
- Abwesenheit eines Partners wird über die Vakanz-Regel der Plattform
  behandelt (z. B. 48 h), nicht über Eskalation.

## Neue Protokolle hinzufügen

Neue Protokolle treten dieser Familie als Unterkapitel in
`communications-protocols-skill.md` bei (zuerst Konzept, mit eigenem
Sicherheitsvertrag und Belegen vor "bewiesen"). Hier mit je einer Zeile
listen: Name, Zustand (Konzept/Pilot/bewiesen), Zweck.
