---
name: academic-study-learn
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-06-20
updated: 2026-06-20
description: >
  Einsetzen, wenn Lerninhalte aus Studienmaterialien (Skripte, Bücher, PDFs,
  Vorlesungsfolien) strukturiert erarbeitet, zusammengefasst oder durch
  Retrieval-Practice gefestigt werden sollen. Leitet durch einen vollständigen
  Lernzyklus: Lernziel, Kernideen, Glossar, Transfer und Selbsttest.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: education
tags: [lernen, lernziele, retrieval, glossar, zusammenfassung, studium, didaktik]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Academic Study Learn

## Übersicht

Begleite das quellenbasierte Lernen mit einem fünfstufigen Lernzyklus. Der Skill
ist institution- und fachunabhängig: er funktioniert mit jedem Studienmaterial,
das als Datei, Texteingabe oder per Webzugang verfügbar ist.

## Konfiguration

| Platzhalter | Bedeutung |
|---|---|
| `<MODUL_PREFIX>` | Kürzel für Modulbezeichnungen (z. B. MM, MF, MO) |
| `<LMS>` | Lernmanagementsystem (z. B. ILIAS, Canvas, Stud.IP) |
| `<INDEX_DATEI>` | Lokale Indexdatei des Studienordners (z. B. LLM_INDEX.md) |

## Lernzyklus (5 Phasen)

### 1. Lernziel klären

- Was soll nach dieser Einheit können, verstanden oder angewendet werden?
- Ziel in einem Satz formulieren und am Ende der Einheit prüfen.

### 2. Kernideen extrahieren (3–7)

- Wichtigste Konzepte, Theorien oder Verfahren aus dem Material herausarbeiten.
- Jede Kernidee in 2–4 Sätzen erklären.
- Verbindungen zwischen den Kernideen benennen.

### 3. Glossar anlegen

- Fachbegriffe mit Kurzdefinition und — wenn vorhanden — Quellenangabe auflisten.
- Nur Begriffe aufnehmen, die für das Lernziel relevant sind.

### 4. Transfer und Anwendung

- Mindestens ein Beispiel oder eine Anwendung aus dem eigenen Kontext formulieren.
- Unterschiede zwischen ähnlichen Konzepten herausarbeiten.
- Offene Fragen und Unklarheiten explizit benennen.

### 5. Retrieval Practice (5–10 Fragen)

- Fragen ohne Blick ins Material beantworten lassen.
- Antworten mit dem Quellmaterial abgleichen.
- Lücken und Irrtümer als Grundlage für die nächste Wiederholung notieren.

## Quellen und Materialzugang

- Lokale Modulordner nach Schema `<MODUL_PREFIX><Nummer>` prüfen (z. B.
  `<MODUL_PREFIX>1`, `<MODUL_PREFIX>2`).
- Bei Online-Materialien (Skripte, Aufgaben, Literaturlisten) `<LMS>` oder die
  offizielle Hochschulwebseite nutzen, wenn ein Connector oder Browser-Zugang
  verfügbar ist.
- `<INDEX_DATEI>` als Einstieg verwenden, wenn ein lokaler Studienordner vorliegt.
- Optional: Uni-Mails nach relevanten Hinweisen zu Pflichtlektüre oder Aufgaben
  durchsuchen, wenn ein Mail-Connector verfügbar ist.

## Qualitätskriterien

- Kernideen sind in eigenen Worten formuliert, nicht wörtlich kopiert.
- Retrieval-Fragen decken verschiedene kognitive Niveaus ab: Wiedererkennen,
  Verstehen, Anwenden.
- Offene Fragen und Unsicherheiten sind explizit markiert, nicht weggelassen.
- Quellennachweise sind vollständig (Dokument, Kapitel oder Seitenzahl).

## Hinweise

- Der Skill eignet sich für jedes Fach und jeden Materialtyp (Text, Tabelle,
  Code, Diagramm).
- Für Prüfungsvorbereitung und Selbsttests den Skill `academic-study-test`
  nutzen.
- Für Semesterplanung und Fristen den Skill `academic-study-control` nutzen.
