---
name: worksheet-generator
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-07-23
updated: 2026-07-23
description: >
  Zeigt auf das eigenstaendige Modul worksheet-generator: erzeugt
  individualisierte Arbeitsblaetter und Uebungsmaterial fuer paedagogische
  und therapeutische Fachkraefte aus einem Foerderziel (Freitext + optionale
  ICF-Codes), Niveau und Alter -- optional angereichert durch einen Scan
  vorhandenen Materials. Nutze diesen Skill, wenn ein Arbeitsblatt,
  Uebungsblatt oder Foerdermaterial erstellt werden soll. Kein
  Klienten-/Personenbezug (nur Ziel/Niveau/Alter). ICF-Referenz ist
  bring-your-own -- mit klarer Grenze: Material-Generator, kein
  Therapieprogramm, erzeugte Blaetter vor Einsatz fachlich pruefen.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

provenance:
  origin: "external"
  origin_repo: "https://github.com/ellmos-ai/worksheet-generator"
  origin_path: "SKILL.md, worksheet_generator/ (Python-Modul), _tools/icf_fetch.py"
  origin_version: null
  last_sync_from_origin: "2026-07-23"
  last_sync_to_origin: null
  local_changes_since_sync: false

category: education
tags: [foerdermaterial, arbeitsblatt, icf, paedagogik, wrapper, pointer-skill]
language: de
status: active
---

# worksheet-generator -- Verweis-Skill

Dieser Skill ist ein **schlanker Verweis (Wrapper)** auf das eigenstaendige,
oeffentliche Modul-Repository
[`ellmos-ai/worksheet-generator`](https://github.com/ellmos-ai/worksheet-generator)
(MIT-Lizenz, public). Der eigentliche Skill lebt dort -- dieses Repository
verlinkt und dokumentiert nur die Installation.

## Was das Modul tut

`worksheet-generator` erzeugt aus einem Foerderziel (Freitext + optionale
ICF-Codes), Niveau und Alter ein strukturiertes Arbeitsblatt-JSON, das
anschliessend nach Markdown, HTML oder DOCX gerendert wird:

- **Deterministisch und offline** -- kein LLM-, kein Netzwerkzugriff im
  Generator selbst; themenspezifische Platzhalter sind als `(ANZUPASSEN)`
  markiert, die inhaltliche Feinausarbeitung obliegt dem aufrufenden
  LLM-Agenten.
- **Material-Ordner-Scan:** `config.json` (`material_dirs`) kann vorhandenes
  Material (txt/md/docx) einbeziehen, sowie bereits recherchierte
  Stichpunkte direkt als konkrete Aufgaben-Prompts uebernehmen.
- **Renderer:** Markdown und HTML immer verfuegbar, DOCX optional (braucht
  `python-docx`); PDF/PowerPoint/Canva nur als externe Delegation.
- **Kein Klienten-/Personenbezug:** Steuerung ausschliesslich ueber
  Foerderziel/Niveau/Alter -- niemals ueber Namen oder Diagnosen.

## ICF-Referenz: bring-your-own (wichtig)

Das Modul enthaelt **keine** ICF-Kurztitel oder -Volltexte -- nur amtliche
ICF-Codes als neutrale Bezeichner (die MIT-Lizenz des Repos erstreckt sich
NICHT auf ICF-Inhalte, WHO-/BfArM-Lizenz gilt separat). Das mitgelieferte
Fetch-Skript `_tools/icf_fetch.py` erzeugt lokal eine gitignorte
`icf_local.json` (Code + Kurztitel, Quelle + Abrufdatum im Dateikopf):

- **Modus A** (kein Netzwerkzugriff): eigene CSV/JSON-Quelldatei einlesen.
- **Modus B** (Live-Abfrage): WHO-ICD-11-API mit eigener Registrierung
  (`icd.who.int/icdapi`, eigene `WHO_ICD_CLIENT_ID`/`_SECRET`).

## Grenzen (wichtig)

- **Material-Generator, kein Therapieprogramm und kein Heilversprechen.**
  Ersetzt keine fachliche Einschaetzung durch qualifizierte
  paedagogische/therapeutische Fachkraefte.
- **Erzeugte Arbeitsblaetter vor dem Einsatz fachlich pruefen und
  anpassen** -- das Modul liefert Rohmaterial, keine einsatzfertigen
  Unterlagen.
- Kein Klienten-/Personenbezug: fuer Berichte oder Klientendaten ist dieses
  Modul nicht zustaendig.

## Installation (generisch, ohne lokale Konkretpfade)

1. Modul klonen:
   ```bash
   git clone https://github.com/ellmos-ai/worksheet-generator.git <klon-pfad>
   ```
2. Keine Pflicht-Abhaengigkeiten (reine Python-Stdlib, Python >= 3.10).
   Optional fuer den DOCX-Renderer:
   ```bash
   pip install python-docx
   ```
3. `<klon-pfad>/SKILL.md` in die eigene Skill-Umgebung uebernehmen (z. B.
   `~/.claude/skills/worksheet-generator/`). KEINE realen lokalen Pfade oder
   Hostnamen in eine versionierte Skill-Umgebung committen.
4. Lokale Overrides (`material_dirs`, `icf_source`, ...) gehoeren in
   `config.local.json` (gitignored) -- Vorlage: `config.local.example.json`.
5. ICF-Referenz laden: `python <klon-pfad>/_tools/icf_fetch.py --source
   <pfad>` (Modus A) oder mit eigener WHO-Registrierung (Modus B, siehe
   oben).
6. Details zu CLI, Schema und Renderern: siehe README des Modul-Repos.

## Herkunft dieses Verweis-Skills

Dieser Wrapper wurde am 2026-07-23 als Showcase-Eintrag fuer das
`ellmos-ai/skills`-Repository angelegt. Es findet **keine
Code-Duplikation** statt -- Pflege und Versionierung bleiben allein im
Modul-Repo `ellmos-ai/worksheet-generator`.

## Changelog

### 0.1.0 (2026-07-23)
- Initialer Verweis-Skill auf `ellmos-ai/worksheet-generator`.
