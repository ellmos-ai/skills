---
name: paveman
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-19
updated: 2026-08-19
description: >
  Erkennt Auftraege, eine Regel- oder Gedaechtnisdatei zu kuerzen ("kuerze meine CLAUDE.md",
  "MEMORY.md ist zu lang", "komprimiere die Doku, ohne Technik anzutasten", "diese Regeldatei
  wird ueber die Zeichengrenze abgeschnitten") und richtet dafuer das Modul paveman ein — ein
  deterministisches, modellfreies CLI-Tool zum Kuerzen von Prosa in Markdown-/Textdateien mit
  Trockenlauf als Default, Rollback und striktem Schutz-Validator fuer Pfade/Ueberschriften/
  Code. Nutze diesen Skill bei Saetzen wie "kuerze <Datei>", "diese Datei ist zu lang/wird
  abgeschnitten", "shrink this rule file", "komprimiere ohne Inhalt zu veraendern", oder wenn
  eine Regel-/Gedaechtnisdatei erkennbar an eine Zeichen-/Zeilengrenze stoesst.

# Kompatibilitaet
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: utilities
tags: [kuerzen, kompression, regeldatei, gedaechtnis, deterministisch, dry-run, rollback, dokumentation]
language: de
status: active

# Abhaengigkeiten
dependencies:
  tools: [paveman]
  services: []
  protocols: []
  python: []
  modules: [paveman]

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Paveman — Regel-/Gedaechtnisdateien deterministisch kuerzen

> Dünner Skill-Wrapper um das bereits installierte Modul `paveman`
> (`C:\_Local_DEV\repos\paveman`, pip-installiert am 2026-08-19, Ticket T-20260819-213392123).
> Dieser Skill ist die Erkennung, die dem Modul bisher fehlte — das gleiche Muster wie
> `file-collect-sort-action` fuer `fcsa`: das Werkzeug konnte schon alles, aber kein Skill
> wusste, WANN es zu greifen hatte.

## Wann dieser Skill greift

Trigger sind Nutzersaetze, die eine **bestehende Regel-, Konventions- oder Gedaechtnisdatei**
kuerzen wollen, OHNE ihren fachlichen Inhalt zu veraendern:

- "Kuerze `<Datei>`" / "diese Datei ist zu lang" / "wird bei X Zeichen/Zeilen abgeschnitten"
- "Komprimiere die Doku, ohne Technik/Code anzutasten"
- "MEMORY.md/CLAUDE.md ist zu voll geworden"
- "Mach diese Regeldatei knapper, aber lass die Bedeutung unveraendert"
- Jede Variante, die **Kuerzen einer bestehenden Datei** meint, nicht **neues Schreiben** und
  nicht **Uebersetzen** (siehe Abgrenzung unten)

**Nicht** dieser Skill:
- **`knappform`** — aendert, WIE das Modell selbst in der laufenden Konversation SPRICHT
  (LLM-Kommunikationsstil, modellbasiert, kein Dateizugriff). `paveman` aendert stattdessen den
  INHALT einer bestehenden DATEI (deterministisch, ohne Modellaufruf). Beide koennen
  nebeneinander bestehen — verwechselt werden sie leicht wegen der aehnlichen Namensherkunft
  (beide von `caveman` abgeleitet), sind aber technisch und funktional getrennt.
- **`bilingual-doc-sync`** — zieht FEHLENDE SPRACHFASSUNGEN nach (Uebersetzung). `paveman`
  kuerzt EINE Fassung, uebersetzt nichts.
- **`llm-text-hygiene`** — entfernt KI-Spuren/Chat-Reste aus Texten. Anderer Zweck als Kuerzen.
- Neuen Inhalt schreiben/erfinden — `paveman` kuerzt nur, was schon da ist.

## Was das Modul kann (Kurzfassung)

`paveman` (CLI-Befehl `paveman`, Python-Paket, pip-installiert, MIT, Clean-Room-Eigenbau ohne
BSL-Code) ist ein **regelbasierter, deterministischer** Prosa-Kuerzer fuer Markdown-/Textdateien
— kein Modellaufruf, keine Tokens, nichts verlaesst die Maschine.

| Flag | Wirkung |
|---|---|
| *(kein Flag)* | **Trockenlauf (Default).** Zeigt Diff + Zeichenersparnis, schreibt nichts. |
| `--apply` | Schreibt wirklich (Backup wird vorher automatisch angelegt). |
| `--rollback` | Stellt die letzte Sicherung wieder her. |
| `--locker` | Pfade/Ueberschriftentext nur als Warnung statt als Fehler (weicher Modus). |
| `--kontext N` | Diff-Kontextzeilen. |

**Schutz-Validator laeuft bei jedem Aufruf:** Code-Bloecke, Pfade und Ueberschriften werden
NIE veraendert — Standard-Modus behandelt eine Abweichung als **Fehler und verweigert das
Schreiben**, nicht nur als Warnung (staerker als die Referenz, gegen die `paveman` gebaut wurde).

## Ablauf — IMMER in dieser Reihenfolge

1. **Erst Trockenlauf, ohne Ausnahme.** `paveman <Datei>` (kein `--apply`) — Ergebnis dem Nutzer
   zeigen: Zeichenersparnis, Diff, Validator-Status ("OK" oder die konkrete Fehlermeldung).
2. **Erst nach ausdruecklichem Nutzer-Go schreiben.** `paveman <Datei> --apply` — niemals von
   selbst aus dem Trockenlauf heraus anwenden, auch wenn das Ergebnis harmlos aussieht.
3. **`--rollback` aktiv erwaehnen**, bevor `--apply` laeuft — der Nutzer soll wissen, dass ein
   Fehlgriff sofort rueckholbar ist (`paveman <Datei> --rollback`), nicht erst danach suchen.
4. **Validator-Fehler ernst nehmen.** Meldet der Schutz-Validator eine Abweichung (Pfad/
   Ueberschrift veraendert), NICHT mit `--locker` umgehen, um den Fehler verschwinden zu lassen —
   erst pruefen, ob die Abweichung echt unschaedlich ist. `--locker` ist eine bewusste
   Nutzerentscheidung, kein Standardweg um eine Fehlermeldung loszuwerden.
5. **Kuratierte Inhalte respektieren.** `paveman` ist regelbasiert und kann nicht wissen, ob ein
   Abschnitt bewusst so formuliert ist — bei Unsicherheit den Trockenlauf-Diff genau pruefen,
   bevor `--apply` empfohlen wird.

## Voraussetzung — Modul-Installationsstatus pruefen

`paveman` muss auf dem jeweiligen Host als CLI verfuegbar sein (`which paveman` bzw.
`paveman --help`). Auf **ASUS-GEI ist es installiert** (editable pip-install aus
`C:\_Local_DEV\repos\paveman`, 26/26 Tests gruen, Stand 2026-08-19). Auf einem Host, wo der
Befehl fehlt: aus dem bestehenden Repo installieren (`pip install -e .` im Repo-Root) — **kein
neues Repo/Modul anlegen**, das bestehende Modul nachziehen. Fehlt das Repo auf diesem Host
ganz, das als eigenen Punkt melden statt den Skill blind auszufuehren.

## Beispiele

```
User: "Kuerze meine ~/CLAUDE.md, sie wird beim Sessionstart abgeschnitten."

→ `paveman C:\Users\User\CLAUDE.md` (Trockenlauf)
→ Ergebnis: "12.400 -> 9.800 Zeichen (-21 %), Validator: OK — alles Geschuetzte unveraendert."
  Diff dem Nutzer zeigen.
→ Nutzer bestaetigt.
→ `paveman C:\Users\User\CLAUDE.md --apply` (Backup automatisch angelegt)
→ Kurz erwaehnt: "Bei Bedarf --rollback stellt den vorherigen Stand wieder her."
```

```
User: "MEMORY.md ist zu voll, kuerz die mal."

→ Trockenlauf zuerst: "893 -> 893 Zeichen, keine Regel griff — Text ist bereits knapp."
→ Kein Mehrwert durch --apply — das dem Nutzer ehrlich melden statt trotzdem zu schreiben.
```

## Changelog

### 1.0.0 (2026-08-19)
- Erstversion als Mini-Anhang zu T-20260819-213392123 (paveman-Modul war bereits installiert
  und funktionsgeprueft, hatte aber noch keinen Skill, der WANN/WIE erkennt — gleiches Muster
  wie `file-collect-sort-action` fuer `fcsa`). Abgrenzung zu `knappform` (LLM-Kommunikationsstil
  vs. deterministisches Datei-Kuerzen), `bilingual-doc-sync` (Uebersetzung statt Kuerzen) und
  `llm-text-hygiene` (KI-Spuren statt Laenge).
