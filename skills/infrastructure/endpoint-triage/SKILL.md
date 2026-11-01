---
name: endpoint-triage
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: >
  Schreibgeschützter Sammel- und Auswertungsplan für Laptops und PCs (Windows, macOS,
  Linux) bei Verdacht auf Schadsoftware, Persistenz oder Fehlkonfiguration: was gesammelt
  wird, wie die Sammelskripte sicher laufen, wie die Ausgabe auf einem sauberen Rechner
  gelesen wird (Prozesse, Autostarts, Dienste, Netzverbindungen, Konten, Patchstand) und wie
  Beobachtung von Deutung getrennt bleibt. Standard ist Diagnose ohne jede Änderung am
  Zielgerät.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [incident-response, endpoint, triage, persistence, autostart, malware, windows, macos, linux, defensive, read-only]
language: de
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [rescue-intake]
  python: []

provenance:
  origin: custom
  origin_path: "skills/infrastructure/endpoint-triage/"
  origin_version: "1.0.0"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="endpoint-triage banner">

# endpoint-triage (Deutsch)

Sammelplan und Leseanleitung für ein Gerät, dem etwas nicht geheuer ist. Voraussetzung:
`rescue-intake` ist abgeschlossen (Eigentum, Einwilligung, Modus). Der Skill ist rein
defensiv und **ändert nichts am Zielgerät.** Was danach getan wird, regelt
`malware-cleanup-guide`; die Fallnotizen führt `incident-notes`.

## Grundsätze

1. **Schreibgeschützt.** Gesammelt wird nur lesend. Schreiben darf allein der Fallordner,
   und der liegt auf dem Wechselmedium, nicht auf der Platte des Zielgeräts.
2. **Sammeln vor Ort, Auswerten woanders (Modus A).** Die Ausgabe wird auf einem sauberen
   Rechner gelesen. Auf dem Zielgerät werden keine Agenten-Konten angemeldet.
3. **Misstrauen gegenüber dem Messgerät.** Auf einem kompromittierten System können
   Betriebssystemwerkzeuge (Prozessliste, Netzstatus) manipulierte Ausgaben liefern. Eine
   saubere Ausgabe ist deshalb nur ein schwacher Beleg für „sauber". Die belastbarere
   Sicht liefert die Offline-Prüfung der Platte aus einem Live-System (Modus B).
4. **Beobachtung ist nicht Deutung.** Jeder Befund wird als `Beobachtung` (was die Ausgabe
   zeigt) und `Deutung` (was das bedeuten könnte, mit Sicherheitsgrad) getrennt notiert.
5. **Keine Dateien in Online-Dienste.** Nur Hashwerte werden nachgeschlagen, und auch das
   erst nach dem Anonymisieren der Begleitdaten (siehe `rescue-intake`).

## Sammeln

Die Sammelskripte des Rettungspakets (`collect_win.ps1`, `collect_mac.sh`,
`collect_linux.sh`) schreiben je eine Textdatei pro Themenblock in einen Fallordner und
legen eine `INDEX.sha256` mit den Prüfsummen an. Den Fallordner **immer ausdrücklich auf
das Wechselmedium legen** (Argument `-Case` bzw. erstes Argument), da der Standard relativ
zum aktuellen Verzeichnis ist. Vor dem Start den Skriptinhalt lesen und der Eigentümerin
oder dem Eigentümer zeigen.

| Betriebssystem | Wird gesammelt |
|---|---|
| Windows | Systemversion und letzter Start, Prozesse (mit Pfad), Startbefehle, Run-Schlüssel (`HKLM`/`HKCU`), Dienste, geplante Aufgaben, TCP-Verbindungen, lokale Konten, installierte Software, Hotfixes, Defender-Status |
| macOS | Version, Kernel, Prozesse, Netzverbindungen (`lsof -i`), launchd-Liste, Launch-Agents/-Daemons (Systemebene und Benutzer), SIP-, Gatekeeper-, FileVault-Status, Konten, letzte Anmeldungen, Laufwerke |
| Linux | Kernel und Distribution, Prozesse, Netzverbindungen und lauschende Ports, systemd-Dienste und -Timer, `/etc/passwd`, letzte Anmeldungen, System-Cron, geladene Kernelmodule, Laufwerke und Mounts, zuletzt installierte Pakete (dpkg) |

**Bekannte Lücken** der Standardskripte (bei Verdacht ergänzend und weiterhin
schreibgeschützt abfragen, die Zusatzabfrage im Fallprotokoll vermerken):

- Windows: Autostart-Ordner der Benutzer, WMI-Ereignisabonnements, Browser-Erweiterungen,
  `hosts`-Datei und DNS-Einstellungen, Ereignisprotokolle (Anmeldungen, Dienstinstallationen).
- macOS: Anmeldeobjekte, Konfigurationsprofile, Browser-Erweiterungen, Benutzer-Cron.
- Linux: Benutzer-Crontabs, `authorized_keys`, Shell-Startdateien, Inhalt der
  systemd-Unit-Dateien, `ld.so.preload`, Paketmanager-Quellen.

## Auswerten (auf dem sauberen Rechner)

Zuerst `INDEX.sha256` gegen die Dateien prüfen. Dann je Themenblock:

- **Prozesse und Autostarts:** Einträge, die aus beschreibbaren Benutzerpfaden starten
  (Temp, Downloads, AppData, `/tmp`, Benutzer-LaunchAgents), mit zufällig wirkenden Namen,
  ohne erkennbaren Herausgeber oder mit Namen, die Systemprozesse nachahmen
  (Schreibweisen-Varianten), sind zu prüfen. Merke: **auffällig ist nicht gleich bösartig.**
- **Dienste, geplante Aufgaben, Timer, Cron, launchd:** neu hinzugekommene, unbekannte oder
  nach Zeitplan aufrufende Einträge; Persistenz zeigt sich oft hier.
- **Netzverbindungen:** unerwartete lauschende Ports, dauerhafte Verbindungen zu fremden
  Adressen, Verbindungen eines Prozesses, der nichts Vernetztes tun sollte. Die Zuordnung
  Prozess zu Verbindung über die Prozess-ID.
- **Konten und Anmeldungen:** unbekannte lokale Konten, kürzlich angelegte Konten,
  Anmeldungen zu ungewohnten Zeiten.
- **Schutzeinstellungen:** Defender oder Schutzfunktionen abgeschaltet, SIP, Gatekeeper
  oder FileVault aus, fehlende Updates (Patchstand). Installierte Software gegen aktuelle
  Herstellerhinweise gleichen: `security-tech-stack-check`.
- **Zeitleiste:** Wann beginnt das Auffällige (Installationsdatum, Startzeit, erster Eintrag)
  im Verhältnis zu dem, was die Eigentümerin oder der Eigentümer zuletzt getan hat?

Ergebnis je Befund: Kennung, Beobachtung, Deutung mit Sicherheitsgrad
(`gesichert`/`wahrscheinlich`/`unklar`), Quelle (Datei im Fallordner), empfohlene
Prüfung. Offene Fragen bleiben ausdrücklich offen; „nichts gefunden" heißt nur, dass die
Sammlung nichts zeigt, nicht dass das Gerät sauber ist.

## Übergabe

- Befunde gehen in `incident-notes`.
- Weiteres Vorgehen (isolieren, sichern, bereinigen oder neu aufsetzen):
  `malware-cleanup-guide`.
- Konfigurationsmängel, die nichts mit einem Vorfall zu tun haben, gehen in
  `os-hardening-baseline`.

## Nicht Gegenstand

Keine Beschaffung von Zugangsdaten, kein Umgehen von Schutzmaßnahmen, keine Untersuchung
fremder Geräte ohne Einwilligung, keine Änderungen am Zielgerät in diesem Skill.
