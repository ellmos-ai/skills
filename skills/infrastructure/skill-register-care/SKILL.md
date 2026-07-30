---
name: skill-register-care
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: >
  Pflege-Skill, der das dreiteilige Skill-Register konsistent hält (code-skill-index-Kataloge,
  Skill-Index, SKILL-MAP Family-/Routing-Map). Nutze diesen Skill für einen Drift-Check zwischen dem
  realen Skill-Inventar und dem dokumentierten Register: fehlende oder zu viele Einträge melden, Counts
  korrigieren, Stand-Datum setzen. Auch auslösen bei „Skill-Register pflegen", „Index aktualisieren",
  „Register-Drift prüfen", „welche Skills fehlen in der Map".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, register, index, drift, pflege, meta]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: [skill-explorer, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-register-care/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="skill-register-care banner">
# Skill-Register-Care

## Zweck

Hält das **Register** drift-frei. Das Register besteht aus drei verzahnten Artefakten — niemals ein
viertes anlegen, immer diese drei erweitern:

- `~/.claude/skills/code-skill-index/references/catalog-*.md` (Kategorie-Kataloge)
- der Skill-Index (Master-Liste)
- `<USER_HOME>\OneDrive\.USR\SKILL-MAP.md` (Family-/Routing-Map)

## Drift-Check-Prozedur

1. **Ist-Stand erheben:**
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
   Nur `source=user`-Skills sind register-relevant (Plugin/extern bleiben außen vor).
2. **Soll-Stand lesen:** die drei Register-Artefakte.
3. **Differenz bilden:**
   - **Fehlend** (im Inventar, nicht im Register) → nachtragen.
   - **Verwaist** (im Register, nicht mehr im Inventar) → markieren/entfernen.
   - **Count-Abweichung** (z. B. „18 Skills" stimmt nicht mehr) → Zahl korrigieren.
4. **Nachtragen:** je neuer Skill eine Zeile im passenden `catalog-<kategorie>.md`, eine Zeile im
   Skill-Index (+ Kopf-Datum) und — falls neue/geänderte Familie — ein Abschnitt in `SKILL-MAP.md`.
5. **Stand-Datum** in allen berührten Dateien auf das aktuelle Datum setzen.

## Hilfs-Snippet (fehlende user-Skills auflisten)

```bash
PYTHONIOENCODING=utf-8 python -c "
import json
inv=json.load(open('<USER_HOME>/.skill-inventory.json',encoding='utf-8'))
print('\n'.join(s['dir'] for s in inv['skills'] if s['source']=='user'))
"
```
Die Ausgabe gegen die Register-Artefakte abgleichen (manuell oder per grep).

## Eiserne Regeln

- **Kein viertes Register** — nur die drei erweitern.
- Nur user-authored Skills gehören ins Register; Drittanbieter folgen dem externen Pfad.
- Datum nicht raten — aktuelles Datum setzen.

## Changelog

### 0.1.0 (2026-06-17)
- Initiale Version. Erzeugt vom Audit-Modus (P2). Anlass: beim Audit 2026-06-17 fehlten ~10 user-Skills
  in der SKILL-MAP (swarm-operations, model-strategy, agents-bridge, mcp-config-sync, system-onboarding,
  update-cli-docs, migrate-rename, plugin-system + Therapie- und Game-Dev-Familie).
