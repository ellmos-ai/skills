---
name: dev-cycle
version: 1.2.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-08-22
description: "8-Phasen-Entwicklungszyklus: Feature-Anforderungen, Ist-Zustand, funktionale Planung, Frontend, Backend-Planung, Backend-Code, Tests, Use Cases. Iteratives Framework für systematische Softwareentwicklung."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [development, dev-cycle, phases, workflow, systematic, iterative]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/dev-zyklus.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 3d82b648971c28906aeabf5b953a28ac162897503581e5cb5a6af8d9f0b1ae8f
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:52:38.401999+00:00"
---
<img src="banner.png" width="100%" alt="dev-cycle banner">

> **Deutsch** — Offizielle Deutsch-Version / Offizielles Dokument auf Deutsch.


# Entwicklungszyklus (Dev Cycle) (Deutsch)

> **Ziel:** Strukturierter Prozess von der Feature-Anforderung bis zum validierten System.
> Jede Entwicklung durchläuft diese 8 Phasen.

> 📐 **Beilage:** `SCHALTPLAN-SOFTWAREENTWICKLUNG.html` —
> menschlich lesbarer „Schaltplan der Softwareentwicklung" (HTML, im Browser öffnen):
> recherchierte Gesamtkarte aus Phasen, Regelkreisen, Rollen, Prozessketten und Test-Gates
> (Webrecherche 08/2026), in die sich dieser 8-Phasen-Zyklus einordnet.

---

## Übersicht & Zweck

```
  +--------------------------------------------------------------+
  |                    DEVELOPMENT CYCLE                           |
  +--------------------------------------------------------------+
  |                                                                |
  |  Phase 1   Feature Requests (functional requirements)          |
  |     |                                                          |
  |     v                                                          |
  |  Phase 2   Check Current State (What already exists?)          |
  |     |                                                          |
  |     v                                                          |
  |  Phase 3   Functional Planning                                 |
  |            (Workflows, Agents, Experts, Skills, Services)      |
  |     |                                                          |
  |     v                                                          |
  |  Phase 4   Implement Functional Frontend                       |
  |            (Skill files, workflow markdown, agent profiles)     |
  |     |                                                          |
  |     v                                                          |
  |  Phase 5   Plan and Align Backend                              |
  |            (CLI handlers, DB schema, API endpoints)            |
  |     |                                                          |
  |     v                                                          |
  |  Phase 6   Implement Backend Tasks                             |
  |            (Python code, tools, DB migrations)                 |
  |     |                                                          |
  |     v                                                          |
  |  Phase 7   Test Execution, Review Gate and Bugfixes           |
  |            (B/O/E tests, bugfix protocol, code review)          |
  |     |                                                          |
  |     v                                                          |
  |  Phase 8   Functional and Feature Test: USE CASES              |
  |            (End-to-end validation from user perspective)        |
  |                                                                |
  +--------------------------------------------------------------+

  Core principles throughout:
  - Functional description first (before code)
  - CLI First (everything controllable via terminal)
  - Clear separation of user data and system data
  - Shift-Left: tests are DESIGNED early (phases 1/3/5) and WRITTEN
    with the code (phase 6) - phase 7 only EXECUTES them
```

---

## Phase 1: Feature-Anforderungen (funktionale Anforderungen)

**Was:** Funktionale Anforderungen sammeln und formulieren.

**Input:**
- Wünsche, Ideen und Probleme der Nutzer
- Anregungen von Partnern (LLM-Assistenten)
- Erkenntnisse aus Use Cases (Feedback-Schleife!)

**Output:**
- Aufgaben im Aufgabensystem (z. B. als Issue, Ticket oder TODO-Liste)
- Anforderungen beschreiben WAS gewünscht ist, nicht WIE
- Jede Anforderung enthält prüfbare Abnahmekriterien (Shift-Left: Sie werden
  zu den Use Cases der Phase 8 und zur Abnahmecheckliste)

**Regeln:**
- Anforderungen immer funktional formulieren („Nutzer kann X tun")
- Nicht technisch formulieren („REST-Endpoint für X implementieren")
- Use Cases als Anforderungsquelle nutzen (Phase 8 -> Phase 1)

---

## Phase 2: Ist-Zustand prüfen

**Was:** Vorhandene Funktionalität inventarisieren.

**Checkliste:**
```
  [ ] Search existing tools/scripts
  [ ] Check documentation/help on the topic
  [ ] Check existing skills/agents/services
  [ ] Check DB schema (if relevant)
  [ ] Check use cases - has something similar been tested?
```

**Output:**
- Dokumentation, was vorhanden ist, was fehlt und was erweitert werden muss
- Vermeidung von Duplikaten

---

## Phase 3: Funktionale Planung

**Was:** Auf funktionaler Ebene planen – NICHT sofort Code schreiben.

**Planungsebenen:**

| Ebene | Frage | Artefakt |
|-------|-------|----------|
| Workflow | WANN/WIE wird koordiniert? | workflows/*.md |
| Agent | WER führt aus? | agents/*.txt |
| Experte | WER hat Fachwissen? | experts/*/ |
| Skill | WAS wird getan? | skills/*.md |
| Service | WIE wird es technisch umgesetzt? | services/*/ |

**Regeln:**
- Zuerst funktional denken, dann technisch
- Shift-Left: Für jede Planungsebene auch deren PRÜFUNG planen — Anforderung →
  Abnahmekriterium, Service/Schnittstelle → Integrationstest, Unit → Unit-Test
  (Auswahl von Teststufe und Technik: [software-testing](../software-testing/SKILL.md))
- Workflows beschreiben Abläufe, keine Implementierungsdetails
- Jeder Agent braucht ein klares Profil
- Services müssen ohne Nutzerdaten funktionieren

---

## Phase 4: Funktionales Frontend umsetzen

**Was:** Skill-Dateien, Workflow-Markdown und Agenten-Profile erstellen.

Das „Frontend" ist hier die funktionale Beschreibungsschicht:
- Workflow-Dateien (.md)
- Agenten-Profile (.txt)
- Expertenwissen
- Service-Beschreibungen
- Hilfedateien

**Output:**
- Alle funktionalen Beschreibungen liegen vor
- Ein LLM-Partner könnte den Workflow lesen und verstehen
- Die funktionale Schicht ist vollständig dokumentiert

---

## Phase 5: Backend planen und abstimmen

**Was:** Technische Architektur auf das funktionale Frontend abstimmen.

**Planungsbereiche:**

| Bereich | Frage | Ort |
|---------|-------|-----|
| CLI-Handler | Welche Befehle? | handlers/*.py |
| DB-Schema | Welche Tabellen/Spalten? | schema/*.sql |
| API-Endpunkte | Welche GUI-Endpunkte? | server.py |
| Tools | Welche Python-Skripte? | tools/*.py |

**Output:**
- Technischer Plan, abgestimmt auf das funktionale Frontend
- DB-Schema-Entwurf
- CLI-Befehlsstruktur

---

## Phase 6: Backend-Aufgaben umsetzen

**Was:** Python-Code, DB-Migrationen und CLI-Handler schreiben.

**Checkliste (pro Aufgabe):**
```
  [ ] Unit tests written (TDD: test before code) and green locally?
  [ ] Works without user data (empty DB)?
  [ ] CLI command available?
  [ ] Input can come from files/folders?
  [ ] Output goes to structured DB?
  [ ] Scan/import is repeatable (idempotent)?
  [ ] No hardcoded path?
  [ ] Tool registered and documented?
  [ ] Help file created?
```

---

## Phase 7: Testausführung, Review-Gate und Bugfixes

**Was:** Technische Korrektheit sicherstellen. Tests wurden in den Phasen 1/3/5 ENTWORFEN und
in Phase 6 GESCHRIEBEN (Shift-Left) — Phase 7 FÜHRT sie in gestuften, blockierenden Gates aus:
schnelle Tests bei jedem Commit, aufwendige Tests (vollständige Regression, E2E, Last) nachts
oder vor dem Release. Gate-Zuordnung und Testauswahl: [software-testing](../software-testing/SKILL.md).

**Testarten (B/O/E):**

| Art | Perspektive | Beschreibung |
|-----|-------------|--------------|
| B-Tests | Extern/Automatisiert | Automatisierte Tests, CI/CD |
| O-Tests | Funktional (Eingabe->Ausgabe) | Manuelle funktionale Überprüfung |
| E-Tests | Subjektiv/Erleben | UX-Bewertung, Ergonomie |

**Review-Gate (vor Phase 8):**
- Code-Review durch ein zweites Paar Augen (Peer, Reviewer-Agent oder Berater)
- Nichts gelangt unüberprüft in die Use-Case-Validierung
- Review-Ergebnisse fließen als Änderungsanfragen zurück in Phase 6

**Bei Bugs:**
- Bugfix-Protokoll anwenden
- Die 20-Minuten-Regel beachten (Ansatz nach 20 Minuten wechseln)
- Erkenntnisse dokumentieren (Lessons Learned)

---

## Phase 8: Funktions- und Feature-Test – USE CASES

**Was:** End-to-End-Validierung aus Nutzersicht.

**Use Cases dienen BEIDEN Zwecken:**
1. **Feature-Indikatoren** – Was wird gewünscht? Was sollte möglich sein?
2. **Testszenarien** – Funktioniert es tatsächlich von A bis Z?

**Use-Case-Format:**
```
  USECASE_NNN: Short Title

  PRECONDITION: What must be in place?
  INPUT:        What does the user enter / what data?
  EXPECTED:     What should the result be?
  TESTS:        Which components are tested?
```

**Feedback-Schleife:**
- Fehlgeschlagene Use Cases -> neue Aufgaben in Phase 1
- Erfolgreiche Use Cases -> validierte Features
- Neue Use-Case-Ideen -> als Aufgaben erfassen

---

## Zusammenfassung: Der Zyklus

```
  Phase 8 (Use Cases)
       |
       | New requirements / bugs
       v
  Phase 1 (Feature Requests)  -->  Phase 2 (Current State)
       ^                                    |
       |                                    v
  Phase 7 (Tests/Bugs)         Phase 3 (Functional Planning)
       ^                                    |
       |                                    v
  Phase 6 (Backend Code)       Phase 4 (Functional Frontend)
       ^                                    |
       |                                    v
       +──────────────────── Phase 5 (Backend Planning)
```

Der Zyklus ist eine Schleife: Use Cases validieren Features und erzeugen gleichzeitig
neue Anforderungen.

---

## Regelkreise (Control Loops)

Der 8-Phasen-Zyklus ist die ÄUSSERE Regelschleife. Innerhalb davon laufen schnellere
Schleifen parallel — je weiter innen eine Schleife liegt, desto kürzer ihr Takt und desto
günstiger die Behebung:

| Schleife | Takt | Ort im Zyklus |
|----------|------|---------------|
| TDD (Rot–Grün–Refactor) | Sekunden–Minuten | innerhalb Phase 6 |
| Testausführung / CI-Gates | < 10 Min. pro Commit | Phase 7 → Phase 6 bei Rot |
| Review-Gate (4-Augen) | Stunden | zwischen Phase 7 und Phase 8 |
| Bugfix-Schleife | Stunden | Phase 7 → Phase 6 (Bugfix-Protokoll) |
| Use-Case-Schleife | pro Zyklus | Phase 8 → Phase 1 |
| Betriebs-Feedback | kontinuierlich | Monitoring/Vorfälle → Phase 1 |

Faustregel: Die Zeit von Commit bis Rückmeldung unter 10 Minuten halten — eine langsame
Schleife wird umgangen. Visuelle Karte aller Schleifen mit Taktzeiten: beiliegend
`SCHALTPLAN-SOFTWAREENTWICKLUNG.html`, Blatt BL-2.

---

## Phasenspezifische Skills

| Phase | Spezialisierter Skill | Auslöser |
|-------|----------------------|----------|
| Phasen 1-3 | Projekt-Bootstrapper (falls verfügbar) | Neues Projekt anlegen (Greenfield) |
| Phase 2 | [project-onboarding](../project-onboarding/SKILL.en.md) | Ein bestehendes Projekt übernehmen |
| Phasen 2-3 | [docs-analysis](../docs-analysis/SKILL.en.md) | Anforderungsdokumente gegen Code prüfen |
| Phasen 5-6 | [pipeline-optimizer](../pipeline-optimizer/SKILL.en.md) | Bestehende Strukturen sanieren |
| Phase 7 | [bugfix-protocol](../bugfix-protocol/SKILL.en.md) | Systematisches 6-Phasen-Debugging |
| Phasen 7-8 | [bugsweep](../bugsweep/SKILL.en.md) | Konvergierende Bug-Suche vor einem Release |
| Phasen 1, 3, 7 | [software-testing](../software-testing/SKILL.md) | Teststufen, Testarten und Testentwurfstechniken wählen; CI/CD-Gate-Zuordnung |
| Nach Phase 8 | [github-repo-care](../github-repo-care/SKILL.en.md) | Release: Repository veröffentlichen und pflegen |

Falls deine Skill-Sammlung einen Skill-Index hat, durchsuche ihn nach weiteren phasenspezifischen Skills.

---

## Änderungsprotokoll

### 1.2.0 (2026-08-22)
- Shift-Left verankert (Rechercheabgleich mit Beilage-Schaltplan): Abnahmekriterien als
  Phase-1-Output, Testentwurf je Planungsebene in Phase 3, Unit-Tests (TDD) als erster
  Punkt der Phase-6-Checkliste; Phase 7 umbenannt in „Testausführung, Review-Gate und
  Bugfixes" — Tests werden dort ausgeführt, nicht erst geschrieben
- Review-Gate (4-Augen-Prinzip) als expliziter Schritt vor Phase 8
- Neuer Abschnitt „Regelkreise (Control Loops)" mit Taktzeiten (TDD, CI, Review,
  Bugfix, Use-Case, Betrieb)
- Phasen-Skill-Tabelle erweitert: software-testing (Phasen 1/3/7), github-repo-care
  (nach Phase 8); Verweise auf software-testing in Phase 3 und Phase 7

### 1.1.1 (2026-08-22)
- Beilage `SCHALTPLAN-SOFTWAREENTWICKLUNG.html` (menschlich lesbare Gesamtkarte: Phasen,
  Regelkreise, Rollen, Prozessketten, Test-Gates — Synthese einer Webrecherche 08/2026)
  plus Verweis im Kopf der Datei

### 1.1.0 (2026-06-13)
- Neue Tabelle „Phasenspezifische Skills" mit Verweisen auf project-onboarding, docs-analysis, pipeline-optimizer, bugfix-protocol und bugsweep

### 1.0.0 (2026-03-12)
- Von BACH portiert (dev-zyklus v1.0.0)

---

*Erstellt: 2026-01-28 | Portiert: 2026-03-12*
