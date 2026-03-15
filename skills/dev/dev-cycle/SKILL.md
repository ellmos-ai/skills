---
name: dev-zyklus
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  8-Phasen Entwicklungszyklus: Feature-Wuensche, Ist-Stand, funktionale
  Planung, Frontend, Backend-Planung, Backend-Code, Tests, Usecases.
  Iteratives Framework fuer systematische Softwareentwicklung.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: dev
tags: [entwicklung, dev-cycle, phasen, workflow, systematisch, iterativ]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/workflows/dev-zyklus.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Entwicklungszyklus (Dev-Zyklus)

> **Ziel:** Strukturierter Ablauf von Feature-Wunsch bis validiertem System.
> Jede Entwicklung durchlaeuft diese 8 Phasen.

---

## Uebersicht

```
  ┌──────────────────────────────────────────────────────────────────┐
  │                    ENTWICKLUNGSZYKLUS                            │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                  │
  │  Phase 1   Feature-Wuensche (Anforderungen funktional)           │
  │     │                                                            │
  │     v                                                            │
  │  Phase 2   Ist-Stand pruefen (Was gibt es schon?)                │
  │     │                                                            │
  │     v                                                            │
  │  Phase 3   Funktionale Planung                                   │
  │            (Workflows, Agenten, Experten, Skills, Services)      │
  │     │                                                            │
  │     v                                                            │
  │  Phase 4   Functional Frontend implementieren                    │
  │            (Skill-Dateien, Workflow-Markdown, Agent-Profile)      │
  │     │                                                            │
  │     v                                                            │
  │  Phase 5   Backend planen und ausrichten                         │
  │            (CLI-Handler, DB-Schema, API-Endpoints)               │
  │     │                                                            │
  │     v                                                            │
  │  Phase 6   Backend-Aufgaben umsetzen                             │
  │            (Python-Code, Tools, DB-Migrationen)                  │
  │     │                                                            │
  │     v                                                            │
  │  Phase 7   Technische Tests und Bugfixes                         │
  │            (B/O/E-Tests, Bugfix-Protokoll)                       │
  │     │                                                            │
  │     v                                                            │
  │  Phase 8   Funktions- und Featuretest: USECASES                  │
  │            (End-to-End Validierung aus Nutzersicht)               │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘

  Grundprinzipien durchgaengig:
  - Funktionale Beschreibung zuerst (vor Code)
  - CLI First (alles ueber Terminal steuerbar)
  - Klare Trennung von User-Daten und System-Daten
```

---

## Phase 1: Feature-Wuensche (Anforderungen funktional)

**Was:** Funktionale Anforderungen sammeln und formulieren.

**Eingabe:**
- User-Wuensche, Ideen, Probleme
- Partner-Vorschlaege (LLM-Assistenten)
- Erkenntnisse aus Usecases (Rueckkopplung!)

**Ergebnis:**
- Tasks im Task-System (z.B. als Issue, Ticket oder TODO-Liste)
- Anforderung beschreibt WAS gewuenscht ist, nicht WIE

**Regeln:**
- Anforderungen immer funktional formulieren ("User kann X tun")
- Nicht technisch ("Implementiere REST-Endpoint fuer X")
- Usecases als Anforderungsquelle nutzen (Phase 8 -> Phase 1)

---

## Phase 2: Ist-Stand pruefen

**Was:** Vorhandene Funktionalitaet inventarisieren.

**Checkliste:**
```
  [ ] Bestehende Tools/Skripte durchsuchen
  [ ] Dokumentation/Hilfe zum Thema pruefen
  [ ] Vorhandene Skills/Agenten/Services pruefen
  [ ] DB-Schema pruefen (falls relevant)
  [ ] Usecases pruefen - wurde etwas Aehnliches getestet?
```

**Ergebnis:**
- Dokumentation was existiert, was fehlt, was erweitert werden muss
- Vermeidung von Duplikaten

---

## Phase 3: Funktionale Planung

**Was:** Auf der funktionalen Ebene planen - NICHT sofort Code schreiben.

**Planungs-Ebenen:**

| Ebene | Frage | Artefakt |
|-------|-------|----------|
| Workflow | WANN/WIE wird koordiniert? | workflows/*.md |
| Agent | WER fuehrt aus? | agents/*.txt |
| Experte | WER hat Fachwissen? | experts/*/ |
| Skill | WAS wird getan? | skills/*.md |
| Service | WIE wird es technisch getan? | services/*/ |

**Regeln:**
- Erst funktional denken, dann technisch
- Workflows beschreiben Ablaeufe, keine Implementierungsdetails
- Jeder Agent braucht ein klares Profil
- Services muessen ohne User-Daten funktionieren

---

## Phase 4: Functional Frontend implementieren

**Was:** Skill-Dateien, Workflow-Markdown, Agent-Profile erstellen.

Das "Frontend" ist hier die funktionale Beschreibungsebene:
- Workflow-Dateien (.md)
- Agent-Profile (.txt)
- Experten-Wissen
- Service-Beschreibungen
- Help-Dateien

**Ergebnis:**
- Alle funktionalen Beschreibungen existieren
- Ein LLM-Partner koennte den Workflow lesen und verstehen
- Die funktionale Ebene ist komplett dokumentiert

---

## Phase 5: Backend planen und ausrichten

**Was:** Technische Architektur auf das funktionale Frontend ausrichten.

**Planungs-Bereiche:**

| Bereich | Frage | Ort |
|---------|-------|-----|
| CLI-Handler | Welche Befehle? | handlers/*.py |
| DB-Schema | Welche Tabellen/Spalten? | schema/*.sql |
| API-Endpoints | Welche GUI-Endpunkte? | server.py |
| Tools | Welche Python-Scripts? | tools/*.py |

**Ergebnis:**
- Technischer Plan der sich am funktionalen Frontend orientiert
- DB-Schema-Entwurf
- CLI-Befehlsstruktur

---

## Phase 6: Backend-Aufgaben umsetzen

**Was:** Python-Code schreiben, DB-Migrationen, CLI-Handler.

**Checkliste (pro Aufgabe):**
```
  [ ] Funktioniert ohne User-Daten (leere DB)?
  [ ] CLI-Befehl vorhanden?
  [ ] Input kann aus Dateien/Ordnern kommen?
  [ ] Output geht in strukturierte DB?
  [ ] Scan/Import ist wiederholbar (idempotent)?
  [ ] Kein Hardcoded-Pfad?
  [ ] Tool registriert und dokumentiert?
  [ ] Help-Datei erstellt?
```

---

## Phase 7: Technische Tests und Bugfixes

**Was:** Technische Korrektheit sicherstellen.

**Test-Typen (B/O/E):**

| Typ | Perspektive | Beschreibung |
|-----|-------------|--------------|
| B-Tests | Extern/Automatisiert | Automatisierte Tests, CI/CD |
| O-Tests | Funktional (Input->Output) | Manuelle Funktionspruefung |
| E-Tests | Subjektiv/Erfahrung | UX-Bewertung, Ergonomie |

**Bei Bugs:**
- Bugfix-Protokoll anwenden
- 20-Minuten-Regel beachten (nach 20 Min. Ansatz wechseln)
- Lessons Learned dokumentieren

---

## Phase 8: Funktions- und Featuretest - USECASES

**Was:** End-to-End Validierung aus Nutzersicht.

**Usecases sind BEIDES:**
1. **Feature-Hinweisgeber** - Was ist gewuenscht? Was soll moeglich sein?
2. **Test-Szenarien** - Funktioniert es wirklich von A bis Z?

**Usecase-Format:**
```
  USECASE_NNN: Kurztitel

  VORBEDINGUNG: Was muss vorhanden sein?
  EINGABE:      Was gibt der User ein / welche Daten?
  ERWARTUNG:    Was soll herauskommen?
  PRUEFT:       Welche Komponenten werden getestet?
```

**Rueckkopplung:**
- Fehlgeschlagene Usecases -> neue Tasks in Phase 1
- Erfolgreiche Usecases -> validierte Features
- Neue Usecase-Ideen -> als Task erfassen

---

## Zusammenfassung: Der Kreislauf

```
  Phase 8 (Usecases)
       │
       │ Neue Anforderungen / Bugs
       v
  Phase 1 (Feature-Wuensche)  -->  Phase 2 (Ist-Stand)
       ^                                    │
       │                                    v
  Phase 7 (Tests/Bugs)         Phase 3 (Funktionale Planung)
       ^                                    │
       │                                    v
  Phase 6 (Backend Code)       Phase 4 (Functional Frontend)
       ^                                    │
       │                                    v
       └──────────────────── Phase 5 (Backend Planung)
```

Der Zyklus ist ein Kreislauf: Usecases validieren Features und
generieren gleichzeitig neue Anforderungen.

---

*Erstellt: 2026-01-28 | Portiert: 2026-03-12*
