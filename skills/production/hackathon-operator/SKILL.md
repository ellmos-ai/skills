---
name: hackathon-operator
version: 1.0.0
type: workflow
author: ellmos (erstellt von Kimi K3 aus der Roshambo-Prozessanalyse)
created: 2026-07-31
description: >
  Führt einen Hackathon end-to-end als Operator: von der Ausschreibung über Analyse,
  Ideenfindung, Bau, Beweisführung, Medienproduktion bis zur Einreichung — mit
  Zwischenstandsspeicher (STATE.md), aus dem jede Phase wieder aufgenommen werden
  kann. Der Nutzer ist human-in-the-loop: Richtungsvorgaben, Abnahmen und alle
  unumkehrbaren Aktionen (Public, Upload, Submit) bleiben beim Menschen.
category: production
tags: [hackathon, workflow, operator, devpost, automation, state-machine]
language: de
status: stable
visibility: private-only
provenance:
  origin: roshambo-hackathon-2026-07
  notes: Host/systemgebunden (USMC, open-compute, OneDrive-Pfade, DevPost-Regime) — nicht pushen
---

<img src="banner.png" width="100%" alt="hackathon-operator banner">

# Hackathon-Operator

## Zweck

Einen kompletten Hackathon als Operator führen. Grundlage: die empirische Analyse
`.HACKATHONS/_analysis/PROZESS-ANALYSE-roshambo-2026-07.md` — dort steht, was 2026-07
wirklich passiert ist (inkl. Fallen). Dieser Skill ist die verdichtete,
wiederholbare Form davon.

## Aktivierung

- „Neuer Hackathon: <link/text>" → Phase 0
- „Nimm Hackathon-Projekt <name> wieder auf" → STATE.md lesen, an `phase` weitermachen
- Jeder Prompt des Nutzers wird erst gegen die Prompt-Taxonomie (§6) klassifiziert.

## Projekt-Anlage (einmalig, Phase 0)

```
.HACKATHONS/<jahr>-<name>/
├── STATE.md            ← DER Zwischenstand (Pflicht, wird nach jedem Schritt fortgeschrieben)
├── BRIEF.md            ← Ausschreibungstext (Link/Volltext/Scrape)
├── REQUIREMENTS.md     ← Anforderungsanalyse aus BRIEF
├── IDEENSPEICHER.md    ← Phase A: unbewertet sammeln; Phase B: Abgleich mit REQUIREMENTS
├── DECISIONS.md        ← Nutzer-Entscheidungen mit Datum (Anker-Fakten!)
├── LINKS.md            ← Pflicht-Linkverzeichnis (wird laufend gepflegt)
├── _analysis/          ← Portfolio-Analyse, Feld-Scrapes
├── _evidence/          ← Beweisprotokolle (EVIDENCE-*.md-Äquivalent)
└── _media/             ← Video, Thumbnails, Audio, Boards
```

Baubereich lokal (nicht OneDrive): `C:\_Local_DEV\repos\<name>` bzw.
`C:\_Local_DEV\_<name>-assets\`. OneDrive = Konzepte/State, lokal = Bau/Render.

## STATE.md — Format (Herzstück)

```yaml
project: roshambo
phase: 7                # aktuelle Phase (0-9, siehe unten)
mode: interactive       # silent | interactive | auto (Nutzer konfiguriert pro Projekt)
operator: kimi-k3       # wer gerade operiert (Operator-Wechsel = Normalfall!)
gates:                  # unumkehrbare Aktionen — NUR nach ausdrücklicher Nutzer-Freigabe
  repo_public: done 2026-07-31
  video_upload: done 2026-07-31 (durch Nutzer)
  submitted: done 2026-07-31 (durch Nutzer)
anchors:                # einmal gesagte, dauerhaft geltende Regeln des Nutzers
  - "Keine erfundenen Zahlen; was nicht gemessen ist, bleibt Platzhalter"
  - "Der Himmel ist erfunden — nie als Astronomie ausgeben"
  - "Absenden immer durch den Nutzer"
decisions_ref: DECISIONS.md
artifacts:              # was existiert wo (Pfade), mit Abnahme-Status
  video_final: {path: ..., approved: true}
open:                   # offene Punkte, nächste Schritte
  - "YouTube-Neuupload nach Jitter-Fix → Link nachtragen"
history:                # eine Zeile pro abgeschlossener Aktion (append-only)
  - "2026-07-31T02Z phase 5→6: Video 2 final, 178s"
```

**Regeln:**
1. Nach JEDER abgeschlossenen Aktion: STATE.md fortschreiben + USMC-Notiz (eine Zeile).
2. Wiederaufnahme = STATE.md lesen, `history` verifizieren (nicht blind vertrauen:
   Existenz/Integrität der Artefakte prüfen, z. B. ffprobe bei Videos).
3. Gates sind die EINZIGEN Punkte, an denen der Operator pausieren MUSS.
4. Operator-Wechsel: neuer Operator liest STATE.md + DECISIONS.md + letzte 3
   history-Zeilen und schreibt sich als `operator` ein. Kein Mund-zu-Mund-Briefing nötig.

## Die Phasen

**Phase 0 — Intake.** BRIEF anlegen (Link/Text/Scrape), Projektstruktur, STATE.md
initialisieren. Frist + Bewertungskriterien prominent in REQUIREMENTS.md.

**Phase 1 — Analyse.** REQUIREMENTS.md (Pflicht/Kann, Werkzeug-Anforderungen mit
Beleg-Pflicht). Portfolio-Analyse: eigene Repos/Module/frühere Hackathons als
Baukasten (`_analysis/portfolio.md`). DevPost-Standardfelder scrapen, wenn möglich.

**Phase 2 — Ideen.** Kreativ-Skills anwenden (idea-mining/idea-crafting/brainstorming):
Phase A divergent ohne Bewertung. Phase B: jede Idee gegen REQUIREMENTS prüfen.
**Drei Ideen antesten** (kleinster echter Test: Schema, 30-Sekunden-Demo, Technik-Risiko)
→ dem Nutzer als Vergleich vorlegen. GATE: Nutzer wählt.

**Phase 3 — Konzept & Plan.** Nutzer-Input in DECISIONS.md. Umsetzungsplan mit
Evidence-Disziplin von Tag 1 (Protokolle wörtlich, keine Glättung; Zählregeln VOR
dem Lauf committen). Architektur-Diagramm früh.

**Phase 4 — Bau.** Code in Trennung: Kern → Dry-Tests → volle Tests, jeweils mit
Rückkopplung zum Plan und Review-Schleifen. Bugs sofort fixen, auch spät.

**Phase 5 — Abnahme & Beweis.** Große Tests MIT Beweisführung: gutes Logging,
reproduzierbare Kernprobe für Juroren ohne Zugänge (z. B. 30-Sekunden-Dry-Run),
Feldversuch mit echten Bedingungen. Beweis zeigt auch eigene Fehler.
GATE: Nutzer sieht Auswertung, Freigabe „Beweis steht".

**Phase 6 — Medienproduktion.** Repos fertig (README aktuell? Text gegen Verlauf
prüfen, Privacy/Lizenz/Topics, Cross-Links). Narration: Gesamtgeschichte mit
Spannungsbogen und echtem Anker. 3 Thumbnail-Entwürfe → GATE Nutzer wählt.
Storyboard → GATE Story-Abnahme. Video bauen (Skills: HyperFrames/ai-media-editor/
Simulation-aus-Daten) + Voiceover → Korrekturschleifen mit Zeitcode-Feedback.
Kompositionsauftrag: Musik passend zur Videostory — Sinnabschnitte als
Wechselindikator, Stimmungsbogen (music-composer-Skill, Storyline-JSON).
Zwei Varianten (geduckt/ungeduckt) → GATE Nutzer wählt. YouTube-Titel/Beschreibung
als Dateien + Play-Thumbnail.

**Phase 7 — Einreichung.** DevPost-Entwurf aus gescrapten Feldern (Listen statt
Markdown-Tabellen!). Modus-abhängig:
- *interactive:* Nutzer lädt Video hoch + reicht ein; Link zurück an Operator.
- *auto:* Operator nutzt open-compute (Nutzer-Browser) für Upload + Formular.
Danach: Link überall nachtragen (READMEs, DevPost, LINKS.md), letzte Überarbeitungen,
GATE Nutzer: Public-Schaltung + Absenden. Einreichung ist bis Frist anpassbar.

**Phase 8 — Abschluss.** Abschlussberichte (USMC + _evidence/), Lessons in die
Analyse-Datei der Pipeline zurückspielen, Ideen-Reste in IDEENSPEICHER.

**Phase 9 — Post-Submission (optional).** Postanalyse, Ausblicke, Nebenprodukte
hardenen (z. B. entstandene Skills/Werkzeuge in ihre Heimat-Repos).

## Modi (pro Projekt in STATE.md)

- **silent:** Operator arbeitet, meldet nur an Gates und bei Blockern.
- **interactive (Default):** Jedes fertige Artefakt wird dem Nutzer GEÖFFNET
  (Video, Thumbnail, Dateien, Repo-Seiten) — er muss nicht nachfragen.
- **auto:** Wie interactive, plus open-compute für outward actions (YouTube-Upload,
  DevPost-Formular). Gates bleiben Gates: Public/Submit nur auf Freigabe.

## Prompt-Taxonomie (§6 der Analyse)

Jeder Nutzer-Prompt wird klassifiziert als: Auftrag / Richtungs-Korrektur /
Qualitäts-Feedback (kurz, mit Zeitcode) / Entscheidungs-Freigabe (Gate) /
Meta-Steuerung (Modus, State-Regeln) / Anker-Fakt (→ DECISIONS.md + STATE.anchors) /
Kreativ-Impuls (→ IDEENSPEICHER, nicht sofort bauen) / Abnahme (→ Gate frei).
Richtungs-Korrekturen dürfen nie teuer sein: Artefakte immer wiederverwendbar halten
(Daten > Inszenierung, Boards/Clips modular).

## Fallen (aus der Analyse, immer prüfen)

- ffmpeg `fade=in` schwärzt alles vor dem Startpunkt → Testframes nach jedem Eingriff.
- OneDrive: Shell-Writes gehen im Sync verloren; CRLF bricht Suchen →
  FileCommander-MCP / zeilenbasierte Edits.
- Fremdlauf-Timeout → IMMER Integrität prüfen (ffprobe), nicht nur Dateiexistenz.
- Reproduktions-Behauptungen selbst ausführen, nie aus Doku abschreiben.
- Teilnehmer-/Zahlen-Claims gegen die Daten prüfen, nicht aus Erinnerung.
- Markdown-Tabellen auf DevPost → Listen.

## Querverweise

- Analyse: `.HACKATHONS/_analysis/PROZESS-ANALYSE-roshambo-2026-07.md`
- Musik: `music-composer` Skill (Storyline-JSON → Score)
- Video: HyperFrames-Skills, ai-media-editor
- GUI-Automation (auto-Modus): open-compute (`oc capture/do`, SKILL.md im Modul)
- State-Backend: USMC (`usmc note`)
