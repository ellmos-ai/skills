---
name: skill-register-care
version: 0.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-09-20
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
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [skill-explorer, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-register-care/"
  origin_version: "0.2.0"
---

<img src="banner.png" width="100%" alt="skill-register-care banner">
# Skill-Register-Care

## Zweck

Hält das **Register** drift-frei. Das Register besteht aus drei verzahnten Artefakten — niemals ein
viertes anlegen, immer diese drei erweitern:

| Artefakt | Rolle | Pflege |
|---|---|---|
| `~/.claude/skills/code-skill-index/references/catalog-*.md` | Kategorie-Kataloge | kuratiert, Handarbeit |
| `<USER_HOME>/OneDrive/.SYNC/CLAUDE-CODE-SKILLS.md` | Cross-System-Index (einzige Skill-Sicht für Claude Desktop) | **automatisiert**, siehe unten |
| `<USER_HOME>/OneDrive/.USR/SKILL-MAP.md` | Family-/Routing-Map | kuratiert, Handarbeit |

## Automatisiert: der Cross-System-Index

Der Index wird **nicht** mehr von Hand nachgetragen — das hatte ihn drei Monate stillstehen
lassen (Stand 21.06. gegen 152 reale Skills am 20.09.2026; 81 fehlten). Stattdessen:

```bash
PYTHONIOENCODING=utf-8 python "<USER_HOME>/OneDrive/.SYNC/scripts/skill_index_care.py" --check
PYTHONIOENCODING=utf-8 python "<USER_HOME>/OneDrive/.SYNC/scripts/skill_index_care.py" --apply
```

Läuft ohnehin als **Schritt 2b im täglichen `/sync`**; hier manuell nur, wenn gerade Skills
gebaut oder deployt wurden und der Index sofort stimmen soll. Der Lauf ist additiv und
idempotent: kuratierte Kurzbeschreibungen bleiben, fehlende Skills werden nach
Library-Kategorie einsortiert, Einträge ohne aktive `SKILL.md` **markiert statt gelöscht**.

## Drift-Check-Prozedur (die beiden kuratierten Register)

1. **Ist-Stand erheben:**
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
   Nur `source=user`-Skills sind register-relevant (Plugin/extern bleiben außen vor).
2. **Soll-Stand lesen:** die drei Register-Artefakte.
3. **Differenz bilden:**
   - **Fehlend** (im Inventar, nicht im Register) → nachtragen.
   - **Verwaist** (im Register, nicht mehr im Inventar) → **erst nachsehen, dann urteilen.**
     Ein Skill-Ordner, dessen `SKILL.md` zu `CONTENT.md` umbenannt wurde, ist *deregistriert*:
     bewusst nicht mehr als Skill geladen, inhaltlich aber vorhanden und über `code-skill-index`
     auffindbar. Das Inventar zählt ihn nicht, gelöscht gehört er trotzdem nicht — markieren.
     Wirklich entfernen nur, wenn der Ordner weg ist.
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
- Den Cross-System-Index **nicht von Hand** pflegen; `skill_index_care.py` laufen lassen. Wer
  dort manuell Zeilen ergänzt, baut die nächste stille Drift.

## Changelog

### 0.2.0 (2026-09-20)
- Cross-System-Index `CLAUDE-CODE-SKILLS.md` auf `.SYNC/scripts/skill_index_care.py` umgestellt
  (additiv, markierend, idempotent) und als Schritt 2b in den täglichen `/sync` gehängt. Anlass:
  Der Index stand seit 2026-06-21 still — 81 lokale Skills fehlten, 15 Einträge zeigten
  unmarkiert auf deregistrierte Verfahren, einer auf einen Ordner ohne `SKILL.md`.
- „Verwaist" geschärft: deregistrierte Skills (`CONTENT.md` statt `SKILL.md`) werden markiert,
  nicht entfernt — beim Nachzug wären sonst 15 kuratierte Einträge gelöscht worden.

### 0.1.0 (2026-06-17)
- Initiale Version. Erzeugt vom Audit-Modus (P2). Anlass: beim Audit 2026-06-17 fehlten ~10 user-Skills
  in der SKILL-MAP (swarm-operations, model-strategy, agents-bridge, mcp-config-sync, system-onboarding,
  update-cli-docs, migrate-rename, plugin-system + Therapie- und Game-Dev-Familie).
