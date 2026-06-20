---
name: academic-study-test
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-06-20
updated: 2026-06-20
description: >
  Einsetzen, wenn Prüfungsvorbereitung, Selbsttests, Klausur- oder
  Prüfungssimulationen, schriftliche Hausarbeiten oder Fehlerdiagnosen
  durchgeführt werden sollen. Bietet fünf Modi und ein Rubrik-basiertes
  Bewertungssystem mit strikter Abgrenzung zu laufenden Prüfungen.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: education
tags: [pruefung, klausur, selbsttest, simulation, rubrik, bewertung, feedback, studium]
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

# Academic Study Test

## Übersicht

Unterstütze die Prüfungsvorbereitung mit strukturierten Selbsttests, realistischen
Simulationen und diagnostischem Feedback. Der Skill ist fach- und
institutions-neutral und kann mit beliebigen Lernmaterialien eingesetzt werden.

## Konfiguration

| Platzhalter | Bedeutung |
|---|---|
| `<MODUL_PREFIX>` | Kürzel für Modulbezeichnungen (z. B. MM, MF, MO) |
| `<AUFGABENTYP>` | Art der Abgabe (z. B. Hausarbeit, Portfolio, Seminararbeit) |
| `<LMS>` | Lernmanagementsystem (z. B. ILIAS, Canvas, Stud.IP) |

## Modi

### Modus 1 — Schnelltest (5–10 Minuten)

- 5 gezielte Fragen zum gewählten Thema oder Modul.
- Sofortfeedback nach jeder Antwort.
- Empfehlung: für tägliche Wiederholung und Lernstandskontrolle.

### Modus 2 — Klausurblock (60–90 Minuten)

- Vollständige Klausursimulation nach dem Zeitrahmen und Format der Zielprüfung.
- Alle Fragen werden zuerst beantwortet, dann gemeinsam ausgewertet.
- Bewertung nach Rubrik (siehe unten), Gesamtpunktzahl und Stärken/Lücken-Profil.

### Modus 3 — Mündliche Prüfung

- Simuliertes Prüfungsgespräch: offene Fragen, Nachfragen, Einwände.
- Rückmeldung zu Inhalt, Argumentation und Kommunikationsstil.
- Eignet sich für Bachelor-/Masterprüfungen, Referate und Kolloquien.

### Modus 4 — `<AUFGABENTYP>`-Training

- Bearbeitung von Übungsaufgaben im Format der abzugebenden Aufgabe.
- Qualitätsprüfung nach Inhalt, Struktur, Quellenbezug und formalen Vorgaben.
- Rückmeldung mit konkreten Verbesserungsvorschlägen.

### Modus 5 — Fehlerdiagnose

- Analyse von Fehlern aus früheren Tests, Korrekturen oder Abgaben.
- Muster identifizieren: Konzeptlücken, Flüchtigkeitsfehler, Missverständnisse.
- Priorisierte Wiederholungsempfehlung.

## Bewertungsrubrik

| Kriterium | 0 Punkte | 1 Punkt | 2 Punkte |
|---|---|---|---|
| Inhaltliche Korrektheit | Fehlerhaft | Teilweise korrekt | Vollständig korrekt |
| Vollständigkeit | Wesentliches fehlt | Lücken vorhanden | Vollständig |
| Begründung | Keine Begründung | Angedeutet | Nachvollziehbar begründet |
| Fachsprache | Nicht verwendet | Teilweise | Durchgängig korrekt |
| Struktur | Unklar | Erkennbar | Klar und folgerichtig |

Maximalpunktzahl: 10 Punkte. Bewertungsskala: 9–10 = sehr gut, 7–8 = gut,
5–6 = befriedigend, 3–4 = ausreichend, 0–2 = nicht bestanden.

## Materialzugang

- Lokale Modulordner nach Schema `<MODUL_PREFIX><Nummer>` nutzen.
- Bei Online-Materialien `<LMS>` oder Hochschulwebseite verwenden.
- Optional: institutionelle Mails nach Aufgabenstellungen oder Korrekturen
  durchsuchen, wenn Mail-Connector verfügbar ist.

## Ethik und Grenzen

Dieser Skill dient ausschließlich der Vorbereitung und Übung.

**Absolutes Verbot:**
- Keine Unterstützung während laufender Prüfungen, Klausuren oder
  abzugebender `<AUFGABENTYP>`-Abgaben.
- Kein Formulieren von Antworten, die ohne Kennzeichnung als eigene Leistung
  eingereicht werden.
- Keine Umgehung von Prüfungsordnungen oder Hochschulrichtlinien.

Im Zweifel: Aufgabe als „zu prüfen" markieren, bis Klärung erfolgt ist.

## Hinweise

- Für quellenbasiertes Lernen und Vertiefung den Skill `academic-study-learn`
  nutzen.
- Für Semesterplanung und Fristen den Skill `academic-study-control` nutzen.
