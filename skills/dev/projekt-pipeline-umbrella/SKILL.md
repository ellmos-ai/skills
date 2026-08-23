---
name: projekt-pipeline-umbrella
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: >
  Meta-/Umbrella-Skill für die Familie „Projekt-/Pipeline-Aufbau & -Umbau". Kennt alle Skills für
  Anlegen, Aufnehmen, Umbauen und Analysieren von Projekten und Pipelines und leitet zum passenden
  weiter. Nutze diesen Skill, wenn unklar ist, ob etwas neu angelegt (Greenfield) oder umgebaut
  (Bestand) werden soll bzw. ob es um ein einzelnes Projekt oder eine ganze Pipeline geht. Auch
  auslösen bei „neues Projekt/Pipeline anlegen", „bestehendes umbauen", „Projekt aufnehmen",
  „Ordnerstruktur renovieren", „welcher Bootstrapper passt".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [projekt, pipeline, bootstrap, umbau, umbrella, meta, routing]
language: de
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [project-bootstrapper, pipeline-bootstrapper, project-onboarding, pipeline-optimizer, docs-analysis, dev-cycle]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/projekt-pipeline-umbrella/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="projekt-pipeline-umbrella banner">
# Projekt-/Pipeline-Aufbau & -Umbau — Umbrella

## Zweck

Einstiegspunkt für die Familie „Projekt-/Pipeline-Aufbau & -Umbau". Die Mitglieder sortieren sich
entlang zweier Achsen: **Greenfield vs. Bestand** und **Projekt-Ebene vs. Pipeline-Ebene**. Diese
Umbrella verhindert die häufige Verwechslung „bootstrap" vs. „optimize" vs. „onboard".

## Mitglieder & Routing

| Skill | Wofür | Wann diesen statt der anderen |
|-------|-------|-------------------------------|
| `/project-bootstrapper` | NEUES Projekt **in** bestehender Pipeline anlegen | Greenfield, Projekt-Ebene |
| `/pipeline-bootstrapper` | KOMPLETT NEUE Top-Level-Pipeline anlegen | Greenfield, Pipeline-Ebene (selten) |
| `/project-onboarding` | bestehendes Projekt aufnehmen/erfassen | Bestand, Projekt-Ebene |
| `/pipeline-optimizer` | bestehende Pipeline/Struktur renovieren (6-Schritte-Verfahren) | Bestand, Umbau |
| `/docs-analysis` | Anforderungs-/Konzeptdocs gegen aktuellen Code prüfen | Bestand, Analyse (kein Umbau) |
| `/dev-cycle` | 8-Phasen-Entwicklungsrahmen für das eigentliche Bauen | quer: das WIE der Entwicklung |

> Routing-Regel: **neu + Projekt** → `/project-bootstrapper` · **neu + Pipeline** →
> `/pipeline-bootstrapper` · **Bestand aufnehmen** → `/project-onboarding` · **Bestand umbauen** →
> `/pipeline-optimizer` · **nur prüfen** → `/docs-analysis` · **bauen** → `/dev-cycle`.

## Gut gekoppelte Kombinationen

- `/project-onboarding` (zuerst: Bestand erfassen) → `/pipeline-optimizer` (danach: gezielt umbauen) —
  erst verstehen, dann renovieren (deckt das 6-Schritte-Prinzip „erst lesen, dann schreiben").
- `/docs-analysis` (Lücken finden) → `/dev-cycle` (Lücken schließen).
- `/project-bootstrapper` (Gerüst) → `/dev-cycle` (Inhalt entwickeln).

## Gemeinsame Konventionen

- Bestehende Pipeline-Konventionen (Registry, Templates, CLAUDE.md) immer zuerst lesen — keine
  Parallel-Standards anlegen.
- Greenfield-Skills legen an, Bestand-Skills renovieren — nicht vermischen.
- Live-Dateien der Einzelskills vor Anwendung lesen.

## Changelog

### 0.1.0 (2026-06-17)
- Initiale Version. Erzeugt vom Audit-Modus (3c1) für die Familie Projekt-/Pipeline.
