---
name: docs-analysis
version: 1.1.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-10-15
description: >
  Prüft Konzept- und Anforderungsdokumente gegen die Umsetzung. Optionaler Modus
  Plankonsolidierung (Dokument-Synopse): führt mehrere Pläne zu einem aktuellen
  Dokument mit offenen Punkten zusammen und archiviert abgeschlossene oder
  abgelöste Inhalte mit folder-organization.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [docs-analysis, requirements, code-review, diff-report, quality-assurance]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/docs-analyse.md', 'origin_version': '1.2.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---
<img src="banner.png" width="100%" alt="docs-analysis banner">

# Dokumenten-Anforderungsanalyse

> Analysiert alle Konzept- und Anforderungsdokumente, prüft deren Anforderungen gegen den aktuellen Code und erstellt einen konsolidierten Differenz-Bericht.

---

## Zweck

Analysiert alle Konzept- und Anforderungsdokumente im ../docs/ Ordner, prüft deren Anforderungen gegen den aktuellen Code und erstellt einen konsolidierten Differenz-Bericht.

---

## Modus wählen

- **Anforderungsanalyse (Standard):** Anforderungen gegen Code prüfen; Ablauf und
  Ausgaben unten verwenden.
- **Plankonsolidierung / Dokument-Synopse:** Bei „mehrere Pläne zusammenführen“,
  „aktueller Plan mit offenen Punkten“ oder „Erledigtes archivieren“ die
  [Plankonsolidierung](references/plan-consolidation.md) lesen und diesem Zweig folgen.
  Er nutzt `folder-organization` für Archivierung und Cut-and-Clue und eignet sich
  auch für Vorhaben ohne Code. Die Prozent-Schwelle und Umbenennung des Standardmodus
  gelten in diesem Zweig nicht.

Die folgenden Abschnitte beschreiben ausschließlich den Standardmodus.

### Namenskonvention des Standardmodus

### Präfix und Suffix
Alle analysierten Dokumente erhalten:
- **Präfix:** `conN_` wobei N = Analyse-Version (1, 2, 3, ...)
- **Suffix:** `_XX` wobei XX = Erfüllungsgrad in Prozent (gerundet auf 10er)

### Archivierungs-Schwelle
- **>= 75% erfüllt:** Dokument wird nach `../docs/_archive/` verschoben
- **< 75% erfüllt:** Dokument bleibt in `../docs/` mit Präfix/Suffix
- **Schwelle konfigurierbar** (Default: 75)

---

## Ablauf

### Phase 1: Dokumente sammeln
- Liste alle *.md und *.txt Dateien in ../docs/ (root)
- Filtere README.txt aus

### Phase 2: Anforderungen extrahieren
Für jedes Dokument:
- Lese Inhalt
- Identifiziere Anforderungen (Checklisten, Tabellen, FEHLT/TODO Marker)
- Kategorisiere: Struktur, Code, API, DB-Schema, CLI, Feature

### Phase 3: Code-Prüfung
Für jede Anforderung:
- Bestimme Prüfmethode (Glob, Grep, Read)
- Führe Prüfung durch
- Markiere als: ERFÜLLT, TEILWEISE, FEHLT

### Phase 4: Bewertung
- Zähle erfüllte vs. offene Anforderungen
- Berechne Erfüllungsgrad (%)
- Entscheide: archivieren (>= 75%) oder belassen (< 75%)

### Phase 5: Ausgabe generieren
- Erstelle ANFORDERUNGSANALYSE.md (Zusammenfassung)
- Erstelle consense_diff.md (nur offene Anforderungen, nach Priorität)

### Phase 6: Versionierung
- Scanne nach höchstem conN_ Präfix
- Neue Version = höchste + 1

### Phase 7: Umbenennen und verschieben
- Dokumente mit neuem Präfix/Suffix versehen
- Archivieren oder belassen

---

## Ausgabe

| Datei | Beschreibung |
|-------|--------------|
| `conN_ANFORDERUNGSANALYSE.md` | Vollständige Analyse (Version N) |
| `consense_diff_N.md` | Konsolidierte offene Anforderungen |
| `_archive/conN_*_XX.*` | Archivierte (>=75%) Dokumente |

---

## Prioritäts-Klassifizierung

| Priorität | Kriterien |
|:----------:|-----------|
| P1 | Kernfunktionalität fehlt, System nicht nutzbar |
| P2 | Wichtiges Feature fehlt, Workaround möglich |
| P3 | Nice-to-have, verbessert UX |
| P4 | Kosmetisch, Dokumentation, Code-Qualität |

---

## Changelog

### 1.1.0 (2026-10-15)
- Optionaler Modus Plankonsolidierung mit folder-organization, Quellenabdeckung und
  belegbasierter Archivierung; Anforderungsanalyse bleibt Standard.

### 1.0.0 (2026-03-15)
- Portiert aus BACH v3.8.0

---

*Portiert aus BACH v3.8.0 | Standalone-Version*
