---
name: orchestrator
version: 1.3.0
type: protocol
author: Claude + Codex
created: 2026-06-17
updated: 2026-08-24
description: Providerneutrales Protokoll zum Zerlegen komplexer Aufgaben, zum Beauftragen unabhängiger Worker und zur evidenzbasierten Abnahme ihrer Ergebnisse.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [orchestrierung, multi-agent, delegation, evidenz, checkpoint, workflow]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'local-agent-skills/orchestrator/', 'origin_version': '1.0.0', 'origin_repo': 'None', 'last_sync_from_origin': '2026-07-28', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="orchestrator banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.


> **English Translation** — Official English version of `orchestrator`.


# Orchestrator (Deutsch)

## Übersicht & Zweck

Nutze diesen Skill, wenn eine Aufgabe aus mindestens zwei weitgehend unabhängigen
Arbeitspaketen besteht und Delegation einen echten Zeit-, Kontext- oder
Qualitätsvorteil bringt. Für kleine, eng gekoppelte Aufgaben arbeite direkt.

Der Skill beschreibt ein Protokoll. Das konkrete Starten, Unterbrechen und
Wiederaufnehmen von Workern erfolgt über die Fähigkeiten der jeweiligen Runtime.

## Autoritätsgrenze

Delegation erweitert keine Berechtigung. Jeder Worker erhält höchstens den Scope
und die Änderungsrechte, die für die Hauptaufgabe bereits gelten. Externe,
irreversible oder anderweitig freigabepflichtige Aktionen bleiben
freigabepflichtig.

## Ablauf

### 1. Lage prüfen

1. Ziel, Erfolgskriterien und Ausschlüsse der Hauptaufgabe festhalten.
2. Projektregeln, Sperren, laufende Änderungen und verfügbare Budgets prüfen.
3. Vor dem Dispatch den aktuellen Lock-, Status- und Diff-Zustand der betroffenen
   Bereiche als Baseline sichern. Nur so lassen sich vorhandene fremde Änderungen
   später zuverlässig von Worker-Änderungen unterscheiden.
4. Nur Arbeitspakete parallelisieren, die unabhängig genug sind.
5. Überschneidende Schreibbereiche trennen oder sequentiell bearbeiten.

### 2. Auftragsvertrag schreiben

Vor jedem Dispatch einen kurzen, prüfbaren Vertrag erstellen:

| Feld | Pflichtinhalt |
|---|---|
| Kennung | stabile ID des Arbeitspakets |
| Ziel | genau ein konkretes Ergebnis |
| Eingaben | relevante Dateien, Daten oder Kontextquellen |
| Positiver Scope | was gelesen oder geändert werden darf |
| Negativer Scope | was ausdrücklich unberührt bleibt |
| Erfolgskriterium | beobachtbare Bedingung für „fertig“ |
| Evidenz | erwarteter Nachweis, etwa Test, Diff oder Fundstelle |
| Rückgabeformat | kompakte, strukturierte Abschlussmeldung |

Ein Worker bekommt nur den Kontext, den er für diesen Vertrag benötigt.

### 3. Ausführen und beobachten

- Fan-out klein halten und nur bei unabhängigem Nutzen vergrößern.
- Ist ein Ressourcenprofil aktiv (siehe unten), richtet sich der Fan-out nach
  dessen `max_parallel_workers`; der Spawn-Vertrag nennt das aktive Profil.
- Fortschritt über Runtime-Status oder einen projektüblichen Checkpoint verfolgen.
- Bei Konflikten, Scope-Ausweitung oder fehlender Autorität stoppen und eskalieren.
- Ein fehlgeschlagener Worker darf unabhängige Arbeitspakete nicht automatisch
  blockieren.

### 4. Ergebnisse abnehmen

Eine Fertigmeldung ist zunächst eine Behauptung. Der Orchestrator prüft selbst:

1. Existiert das behauptete Artefakt oder die genannte Änderung?
2. Gehört es zum vereinbarten Scope?
3. Besteht der vereinbarte Test oder Nachweis aktuell?
4. Wurden fremde Änderungen, Sperren und negative Scopes respektiert?
5. Widersprechen sich Ergebnisse verschiedener Worker?

Erst danach gilt ein Arbeitspaket als abgeschlossen.

### 5. Integrieren und sichern

- Konflikte bewusst auflösen; Ergebnisse nicht blind aneinanderhängen.
- Erforderliche Gesamttests nach der Integration erneut ausführen.
- Offene, fehlgeschlagene und zurückgestellte Pakete klar ausweisen.
- Bei längeren Läufen Ziel, Status, Evidenz und nächsten Schritt in einem
  wiederauffindbaren Checkpoint sichern.

## Ressourcenprofil

Der Skill funktioniert vollständig ohne Konfiguration. Ohne `profiles.json`
und `config.json` im Skill-Ordner gilt exakt das hier dokumentierte
Sparprofil: höchstens 1-2 parallele Worker, ein zweiter Slot nur bei
unabhängigem Nutzen, ein kleineres Modell wenn ein Auftragsvertrag gut
vorbereitet ist. Diese Regel ändert sich durch das Vorhandensein der Dateien
nicht — sie macht sie nur explizit einstellbar.

Beide Dateien sind eine OPTIONALE, nutzereigene Anpassungsschicht. Modellnamen
und Schwellenwerte darin sind Beispiele des jeweiligen Nutzers, keine Vorgabe
des Skills. Der Skill selbst bleibt nutzer-, pfad-, modell- und
providerneutral (siehe Changelog 1.1.0) — Pfade zu persönlichen Werkzeugen
gehören ausschließlich in die lokale `config.json`, nie in diesen Text.

### profiles.json — benannte Ressourcenprofile

| Feld | Bedeutung |
|---|---|
| `max_parallel_workers` | Obergrenze gleichzeitig laufender Worker |
| `default_worker_model` | Modellhinweis für einfache Aufträge, `null` = keine Vorgabe |
| `escalate_model_on` | Auftragsmerkmale, bei denen trotz Sparprofil ein stärkeres Modell gewählt wird |
| `external_agents_count_as_slot` | ob nicht-native Worker (z. B. Codex, agy) gegen `max_parallel_workers` zählen |
| `operating_mode` | einer von `alleine` / `delegation` / `orchestrator`, siehe Betriebsmodus unten |
| `mode_label` | menschenlesbare Bezeichnung des Betriebsmodus (Nutzerwortlaut) |
| `teammate_model_whitelist` | Liste erlaubter Modell-Kennungen für Teammates in diesem Profil; `[]` = unbeschränkt |

Mitgelieferte Profile: `solo` (1 Worker), `spar` (2 Worker, Default), `burst`
(4 Worker). Der Nutzer kann eigene Profile ergänzen oder bestehende anpassen.

### Betriebsmodus (drei explizite Modi) und Teammate-Modell-Whitelist

Ergänzung zu Ticket T-20260824-552689035: der Ressourcenprofil-Achse
(Worker-Anzahl) liegt eine zweite, vom Nutzer benannte Achse zugrunde — WIE
stark der Hauptmodell selbst noch direkt umsetzt statt nur zu koordinieren.
Beide Achsen sind in den mitgelieferten Profilen bereits gekoppelt, damit kein
zusätzlicher Konfigurationspfad nötig wird:

| Profil | `operating_mode` | `mode_label` | Bedeutung |
|---|---|---|---|
| `solo` | `alleine` | Alleine bewältigen | Hauptmodell arbeitet direkt, keine Delegation außer bei echtem Blocker |
| `spar` | `delegation` | Kleinere Delegationen | Hauptmodell arbeitet primär selbst, delegiert klar abgegrenzte, unabhängige Teilpakete |
| `burst` | `orchestrator` | Reiner Orchestrator-Modus | Hauptmodell übernimmt vorrangig Zerlegung, Vertrag, Beobachtung und Abnahme (Ablauf 1–5); die Umsetzung selbst liegt bei den Workern |

Eigene Profile können `operating_mode`/`mode_label` frei setzen — die drei
genannten Werte sind die vom Nutzer vorgegebenen Kategorien, keine
technische Beschränkung.

**Teammate-Modell-Whitelist:** `teammate_model_whitelist` schränkt ein, welche
Modell-Kennungen für in diesem Profil gestartete Teammates zulässig sind.
Leer (`[]`, Default in allen mitgelieferten Profilen) heißt unbeschränkt —
jedes für den Aufrufer verfügbare Modell ist erlaubt. Eine Eskalation über
`escalate_model_on` darf eine gesetzte Whitelist nicht verlassen; passt kein
gelistetes Modell zur Eskalation, gilt die nächstbeste gelistete Alternative
oder — falls keine passt — eine bewusste Rückfrage statt eines stillen
Whitelist-Bruchs. Kein neuer Konfigurationspfad nötig: die Whitelist ist wie
jedes andere Profilfeld über `config.json.overrides` punktuell überschreibbar.

**Tokeneffizienz als Auswahlkriterium:** Ist `default_worker_model` `null`,
wählt der Aufrufer je Auftrag das güns­tigste Modell aus einer gesetzten
Whitelist (bzw. aus allen verfügbaren Modellen ohne Whitelist), das die
Aufgabe nach eigener Einschätzung sicher trägt — Tokeneffizienz geht vor
Rohleistung. Details zur Modellwahl: Skill `model-strategy`. Eskalation nur
bei tatsächlichen Treffern in `escalate_model_on`, nicht vorsorglich.

**Phasen-/aufgabenflexibler Moduswechsel:** `active_profile` (und damit
`operating_mode`) darf und soll innerhalb EINER Session wechseln, wenn sich
die Art der Arbeit ändert — z. B. Recherche-/Planungsphase im Profil `solo`,
anschließende Umsetzungsphase mit mehreren unabhängigen Paketen im Profil
`spar` oder `burst`, danach wieder `solo` für Integration und Abnahme. Der
Wechsel erfolgt über `session_override` (siehe unten) und wird kurz begründet
im Spawn-Vertrag bzw. Checkpoint vermerkt — kein stiller Wechsel ohne
nachvollziehbaren Grund, aber auch kein Verharren im falschen Modus nur weil
er zu Sessionbeginn galt.

### config.json — aktives Profil und Automatik

| Feld | Bedeutung |
|---|---|
| `active_profile` | Name des aktiven Profils aus `profiles.json` |
| `overrides` | punktuelle Feldüberschreibungen für das aktive Profil |
| `session_override` | manuelle Vorgabe für die laufende Session; schlägt jede Automatik |
| `token_tracker` | optionale automatische Profilwahl nach Token-Guthaben |

#### Automatische Profilwahl nach Token-Guthaben (optional)

`config.json.token_tracker` recycelt ein vorhandenes Token-Tracking-Werkzeug
des Nutzers, statt ein eigenes zu bauen:

| Feld | Bedeutung |
|---|---|
| `enabled` | schaltet die Automatik ein/aus |
| `report_path` | Pfad zu einem Statusbericht mit einer Guthaben-Prozent-Zeile |
| `db_path` | alternativ: Pfad zu einer read-only abfragbaren Tracking-DB |
| `auto_downgrade` | `{ "to": <profil>, "when_credit_below_pct": <zahl> }` |
| `auto_upgrade` | `{ "to": <profil>, "when_credit_above_pct": <zahl> }` |
| `on_unreadable` | Verhalten wenn weder Bericht noch DB lesbar sind |

Ablauf: Beim Laden des Skills und vor jedem neuen Worker-Spawn den aktuellen
Guthaben-Stand aus `report_path` oder `db_path` LESEN — kein Prozess-Spawn des
Tracking-Werkzeugs selbst. Zwei getrennte Schwellen (`auto_downgrade` unten,
`auto_upgrade` oben) bilden die Hysterese: im Band dazwischen bleibt das
aktive Profil unverändert, es wird nur beim tatsächlichen Über- oder
Unterschreiten einer Schwelle neu bewertet — kein Flattern bei jedem Tick.

`session_override` (z. B. eine explizite Nutzervorgabe wie „Sparmodus bis
2:10 Uhr") schlägt die Automatik immer. Sind `report_path`/`db_path` gesetzt,
aber nicht lesbar, gilt `on_unreadable`: bei `"assume_critical"` wird das
Sparprofil angenommen und die Nichtlesbarkeit im Spawn-Vertrag vermerkt — nie
stilles Weiterlaufen im teuren Profil.

`config.json` ist eine lokale, nutzereigene Datei (Pfade darin sind
hostspezifisch). Die kanonische Skill-Bibliothek führt nur eine neutrale
Vorlage mit deaktivierter Automatik (`token_tracker.enabled: false`,
Pfade `null`) — echte Pfade trägt jeder Nutzer selbst in seine lokale Kopie
ein.

Zusätzliche Quelle (Ticket T-20260824-552689035): `report_path` kann auch auf
die Statusline-Bridge `~/.claude/state/token_budget.json` zeigen (geschrieben
vom Hook `token_budget_statusline.py`, Feld
`five_hour.used_percentage`) — Format ist dort JSON statt Report-Prosa, beim
Lesen entsprechend behandeln. Für den GARANTIERTEN, hiervon unabhängigen
manuellen Weg (Hook kann still bleiben) siehe die Skills `sparmodus` (Stufe
2, ab ca. 80 % verbraucht) und `notaus` (Stufe 3, ab ca. 90 % verbraucht) —
beide setzen unter anderem `session_override` dieses Skills.

## Minimaler Worker-Prompt

```text
Auftrag: <Kennung und Ziel>
Eingaben: <Quellen>
Du darfst: <positiver Scope>
Du darfst nicht: <negativer Scope>
Fertig, wenn: <prüfbares Kriterium>
Belege mit: <Test, Diff oder Fundstelle>
Antworte als: <Rückgabeformat>
```

## Stop-Bedingungen

Stoppe nur das betroffene Arbeitspaket, wenn sein Scope, seine Autorität oder
seine Evidenz unklar wird. Unabhängige, sichere Pakete dürfen weiterlaufen.

Stoppe die gesamte Delegation, wenn:

- die Teilaufgaben nicht mehr unabhängig sind,
- ein gemeinsamer Schreibbereich nicht sicher getrennt werden kann,
- Regeln, Sperren oder Autorität für den gesamten verbleibenden Scope unklar sind,
- die erwarteten Kosten den erkennbaren Nutzen übersteigen,
- die geforderte Evidenz nicht erzeugt oder geprüft werden kann.

## Änderungsprotokoll

### 1.3.0 (2026-08-24)
- Delta zu Ticket T-20260824-552689035 (Ist-Stand 1.2.0 hatte bereits
  Ressourcenprofile inkl. Token-Automatik — hier nur das Delta gebaut, siehe
  Vorab-Befund im Ticket):
  - `profiles.json`: `operating_mode` + `mode_label` je Profil ergänzt — macht
    die drei vom Nutzer benannten Betriebsmodi ("alleine bewältigen" /
    "kleinere Delegationen" / "reiner Orchestrator-Modus") explizit benennbar,
    ohne die bestehenden Profile `solo`/`spar`/`burst` zu ersetzen.
  - `profiles.json`: `teammate_model_whitelist` je Profil ergänzt (leer =
    unbeschränkt); nutzt den bereits vorhandenen `overrides`-Mechanismus in
    `config.json`, kein neuer Konfigurationspfad nötig.
  - SKILL.md: Abschnitt zum phasen-/aufgabenflexiblen Moduswechsel (Wechsel
    von `active_profile`/`session_override` innerhalb EINER Session je nach
    Arbeitsphase, mit Begründung im Checkpoint) und zur Tokeneffizienz als
    primärem Auswahlkriterium für `default_worker_model` (statt Rohleistung),
    Verweis auf Skill `model-strategy`.
  - Querverweis auf die neuen Skills `sparmodus`/`notaus` und die
    Statusline-Bridge `~/.claude/state/token_budget.json` als zusätzliche
    `report_path`-Quelle ergänzt.
  - Keine Änderung an Ablauf 1–5, Autoritätsgrenze, Stop-Bedingungen oder dem
    dokumentierten Default ohne Config-Dateien.

### 1.2.0 (2026-08-17)
- Ressourcenprofile ergänzt: optionale `profiles.json` (benannte Profile
  `solo`/`spar`/`burst`) und `config.json` (aktives Profil, Overrides,
  Session-Override) im Skill-Ordner.
- Automatische Profilwahl nach Token-Guthaben ergänzt
  (`config.json.token_tracker`) — recycelt ein vorhandenes Tracking-Werkzeug
  des Nutzers, liest nur, startet keinen Prozess; zwei Schwellen bilden eine
  Hysterese; fail-closed (`on_unreadable: assume_critical`) bei
  Nichtlesbarkeit.
- Ohne beide Dateien bleibt das Verhalten unverändert (dokumentierte
  Sparprofil-Werte als Default) — die Neutralität aus 1.1.0 bleibt gewahrt;
  echte Pfade gehören nur in die lokale, nicht kanonische `config.json`.

### 1.1.0 (2026-07-28)
- Nutzer-, Pfad-, Modell- und Providerbindungen entfernt.
- Auftragsvertrag, Autoritätsgrenze, Evidenzabnahme und Checkpoints als
  portable Kernmechanik herausgearbeitet.
- Baseline für fremde Änderungen sowie paketlokale und globale Stopps
  ausdrücklich getrennt.

### 1.0.0 (2026-06-17)
- Lokale Ausgangsfassung.