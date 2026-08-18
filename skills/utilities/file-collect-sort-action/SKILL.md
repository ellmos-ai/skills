---
name: file-collect-sort-action
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-18
updated: 2026-08-18
description: >
  Erkennt Nutzeraufträge der Form "hole aus einem Ordner immer bestimmte Dateien und sammle
  sie an einem Ziel" und richtet dafür das Modul file-collect-sort-action (CLI fcsa) ein —
  ein konfigurationsgetriebener Agent, der Ordner scannt, Dateien per Schablone kategorisiert
  und gestufte Aktionen anwendet (move/copy/duplicate-check/delete/OCR/place-information).
  Nutze diesen Skill bei Sätzen wie "hole aus <Ordner> immer <Dateiart> und sammle sie in
  <Ziel>", "sortiere den Ordner X automatisch nach ...", "sammle eingehende Dateien aus ...
  in ...", "räume diesen Ordner regelbasiert auf" oder "verschiebe alle <Dateiart> aus <Ordner>
  automatisch". Richtet IMMER zuerst einen Dry-Run ein und schaltet erst nach ausdrücklichem
  Nutzer-Go scharf; Löschen bleibt grundsätzlich im _trash-Modus.

# Kompatibilitaet
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: utilities
tags: [dateien, sortierung, automatisierung, config-driven, ordner-ueberwachung, duplikate, ocr]
language: de
status: active

# Abhaengigkeiten
dependencies:
  tools: [fcsa]
  services: []
  protocols: []
  python: []
  modules: [file-collect-sort-action]

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# File Collect Sort Action

> Der Nutzer hat dieses Modul bewusst passiv geparkt, bis ein konkreter Auftrag es braucht
> (Ticket T-20260818-916568570, User wörtlich: *"ich werde irgendwann mal sagen hole aus dem
> ordner immer die und die dateien und sammle sie dort -> dann erkennst du den skill zu
> unserem modul und richtest das ein"*). Dieser Skill IST die Erkennung, auf die er wartet.

## Wann dieser Skill greift

Trigger sind Nutzersätze, die ein wiederkehrendes **Einsammeln nach Regel** beschreiben —
nicht ein einmaliges "verschiebe diese eine Datei":

- "Hole aus `<Ordner>` immer `<Dateiart>` und sammle sie in `<Ziel>`"
- "Sortiere den Ordner `<X>` automatisch nach `<Kriterium>`"
- "Sammle eingehende Dateien aus `<Quelle>` in `<Ziel>`"
- "Räum diesen Ordner regelbasiert auf" / "verschiebe alle `<Dateiart>` aus `<Ordner>` automatisch"
- Jede Variante, die **Quelle**, **Erkennungsmerkmal** (Dateiart/Namensmuster/Inhalt) und
  **Ziel** benennt und impliziert, dass das **wiederholt** passieren soll (nicht nur jetzt einmal)

**Nicht** dieser Skill: eine einzelne, einmalige Datei verschieben (das macht ein Agent direkt,
ohne Konfigurationsschicht) — `dokument-ingest` (beantwortet "womit lese ich den *Inhalt*",
nicht "wohin gehört die *Datei*") — inkrementelles Text-Indizieren ohne Dateien zu bewegen
(`gardener`).

## Was das Modul kann (Kurzfassung)

`file-collect-sort-action` (Kurzname **f-csa**, CLI **`fcsa`**) ist ein
konfigurationsgetriebener Scan→Kategorisieren→Handeln-Agent mit drei Konfigurationsdateien
und einem Verarbeitungsgedächtnis:

| Datei | Rolle |
|---|---|
| `config.json` | `scan_paths` (Positivliste), Format-Ein-/Ausschluss, Duplikaterkennungsregeln, Sicherheitsgatter (`allow_hard_delete`) |
| `categories-definitions.json` | Erkennungsschablonen je Kategorie (Dateiname/Endung/Inhalt), Checks/Gates, `default_target`, `default_actions` + `default_stepping` |
| `action-rules.json` | Aktionsparameter je Kategorie (move/copy-Ziele, Duplikatmodus, Löschmodus, OCR-Backend, Platzierungsreihenfolge) |
| `processing-csa.json` | wird **in jeden gescannten Ordner** geschrieben — bekannte Dateien, ihre Kategorie, angewandte Aktionen, wirksamer Einstellungsabdruck (Fingerprint) |

Bekannte Aktions-IDs: `duplicate_check`, `move`, `copy`, `delete`, `ocr_extract`,
`place_information`. Stepping-Semantik: `default_stepping: true` = Aktionen laufen links nach
rechts wie aufgelistet, eine doppelt aufgeführte Aktions-ID läuft **doppelt**; `false` = Menge
(Duplikate kollabieren auf eine Ausführung).

## Sicherheitsmodell — beim Einrichten IMMER einhalten

- **Dry-Run ist Pflicht vor jedem ersten Scharfbetrieb**, je Scan-Pfad. `fcsa run` (ohne
  `--dry-run`) verweigert ohne protokollierten Dry-Run für genau diesen Pfad.
- **Eine Einstellungsänderung entwaffnet die Bestätigung neu** (Fingerprint über alle drei
  Config-Dateien) — nach jeder Config-Anpassung braucht der nächste Scharflauf wieder einen
  frischen Dry-Run.
- **Löschen ist fail-closed.** `delete` verschiebt immer in `trash_dir`, außer *sowohl*
  `action-rules.json` (`delete.hard_delete: true`) *als auch* `config.json`
  (`allow_hard_delete: true`) stimmen ausdrücklich zu. **Für diesen Skill gilt zusätzlich:**
  hartes Löschen niemals ohne separate, ausdrückliche Nutzerfreigabe aktivieren — Default bleibt
  `_trash`.
- **`scan_paths` ist eine explizite Positivliste**, jeder andere Pfad wirft
  `PathNotAllowedError`; Pfade mit `.PRIVAT`- oder `CREDENTIALS`-Segment werden beim Laden
  abgewiesen.
- **Dry-Run ist Byte-für-Byte folgenlos** für den gescannten Ordner: `processing-csa.json`
  wird ausschließlich bei einem Scharfbetrieb geschrieben, nie bei einem Dry-Run.

## Ablauf: vom Trigger-Satz zur eingerichteten Automatisierung

1. **Auftrag strukturieren.** Aus dem Nutzersatz Quelle, Erkennungsmerkmal(e) und Ziel(e)
   herausziehen. Bei Unklarheit gezielt nachfragen (Dateiart? Unterordner mit einbeziehen?
   Was bei Namenskollision im Ziel — skip/overwrite/rename/quarantine?).
2. **Modul lokalisieren.** Klon: `C:\_Local_DEV\repos\file-collect-sort-action` (Repo
   `ellmos-ai/file-collect-sort-action`, privat). CLI: `fcsa` (`pip install -e .` im Klon, falls
   noch nicht installiert). OneDrive-Spiegel (Plan D, git-los):
   `.AI/.MODULES/.TOOLS/file-collect-sort-action/`.
3. **Config-Ordner anlegen.** `fcsa init <config-dir>` — schreibt `scan_paths` zunächst auf
   einen frischen `inbox/`-Ordner **innerhalb** des Config-Ordners selbst, niemals automatisch
   auf einen echten Nutzerordner. Beispiel-Templates dafür: `fcsa/_examples/*.example.json`
   im Modul.
4. **Config auf den echten Auftrag zuschneiden.** `scan_paths` auf den genannten Quellordner
   setzen, in `categories-definitions.json` die Erkennungsschablone(n) für die genannte
   Dateiart eintragen (`default_target` = genanntes Ziel), in `action-rules.json` die
   passenden Aktionen (typischerweise `move`, ggf. `duplicate_check` davor) konfigurieren.
   `state_dir`/`trash_dir` dürfen NICHT innerhalb eines `scan_path` liegen (das Modul weist
   das ab — sonst Selbstfütterungs-Schleife).
5. **Immer zuerst Dry-Run vorlegen:** `fcsa run --config-dir <config-dir> --dry-run` — Ergebnis
   dem Nutzer zeigen (was würde wohin verschoben, was als Duplikat erkannt).
6. **Scharfschaltung nur nach explizitem Nutzer-Go.** Erst dann `fcsa run --config-dir
   <config-dir>` (ohne `--dry-run`). `fcsa status --config-dir <config-dir>` zeigt danach den
   Stand.
7. **Schrittweise erweitern** (User: "und dann erweitert sich das mit der Zeit"): weitere
   Kategorien/Ordner nachtragen, statt eine neue Einrichtung zu beginnen — die drei
   Config-Dateien sind additiv pflegbar. Jede Erweiterung braucht wegen des
   Einstellungsabdrucks wieder einen Dry-Run vor dem nächsten Scharflauf.

## Grenzen / bekannte offene Punkte (Stand Ticket T-20260818-916568570)

- Modul ist Durchgang 1, Status "development" — Kernpipeline, CLI und Sicherheitsgatter sind
  fertig und getestet (63/63 Tests), aber **noch nie gegen einen echten Nutzerordner
  scharfgeschaltet**. Die erste Scharfschaltung ist bewusst dieser Skill-Einsatz.
  Repo-Sichtbarkeit ist "private" — keine Veröffentlichung ohne eigenen `repo-publish-check`.
- Zwei Lesarten von Spezifikationslücken sind dokumentiert (`CHANGELOG.md`/`TODO.md` im
  Modul): `default_stepping: false` kollabiert eine doppelt gelistete Aktion auf **eine**
  Ausführung; `duplicate_check` mit Ergebnis `skip` bricht die **gesamte** restliche
  Aktionskette für die Datei ab (nicht nur move/copy). Bei Bedarf mit dem Nutzer klären, bevor
  eine Config sich darauf verlässt.
- OCR ist ein steckbares Backend (`none`/`command`) — keine eigene OCR-Engine gebündelt. Für
  echte OCR-Extraktion `ellmos-filecommander` `fc_ocr` über den `command`-Backend-Typ anbinden.

## Herkunft

Modul gebaut in Ticket T-20260818-916568570 (Durchgang 1, fcsa-worker), auf Wunsch
des Nutzers bewusst passiv geparkt (PARKED/until-trigger) bis genau der oben beschriebene
Trigger auftritt. Dieser Skill setzt exakt diesen Park-Vermerk um.

## Changelog

### 1.0.0 (2026-08-18)
- Initiale Version. Trigger-Erkennung für "sammle/sortiere Dateien automatisch"-Aufträge,
  Einrichtungs-Ablauf mit Dry-Run-Pflicht und Scharfschaltung nur nach Nutzer-Go dokumentiert.
