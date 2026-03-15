---
name: ordner-flattening
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: >
  Verschachtelte Ordnerstrukturen in flache, maschinenlesbare Layouts
  umstrukturieren. Bash-basiert mit intelligenter Merge-Logik.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: utilities
tags: [ordner, flattening, filesystem, bash, reorganisation, cleanup]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/workflows/ordner-flattening.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Workflow: Ordner-Flattening

Ziel: Verschachtelte Ordnerstrukturen in eine flache, maschinenlesbare Struktur ueberfuehren.
Vorteil: Nicht mehr durchklicken, sondern per Datenbank (Verzeichnis.db) suchen.
Duplikate sind erlaubt wenn thematisch sinnvoll.

---

## Uebersicht der Phasen

| Phase | Was passiert | Script-Abschnitt |
|-------|-------------|-----------------|
| 1 | Flatten: Alle Unterordner auf eine Ebene ziehen | `phase_flatten` |
| 2 | Kuerzen: Lange Pfad-Namen auf letztes Segment kuerzen, mergen bei Konflikten | `phase_shorten` |
| 3 | Bereinigen: Mehrfach-Unterstriche (`___`) aufloesen, trailing `_` entfernen | `phase_cleanup_underscores` |
| 4 | Gruppieren: Zahlen-Ordner, CD-Ordner, kurze Namen in Sammelordner | `phase_group_problematic` |
| 5 | Tripel-Analyse: Gleitende 3er-Gruppen, kuerzester Name als Merge-Ziel | `phase_tripel_merge` |
| 6 | Medienformat-Merge: Ordner nach Dateityp zusammenfassen (Template) | `phase_media_merge` |
| 7 | Aufraeumen: Leere Ordner loeschen | `phase_cleanup_empty` |

---

## Wichtige Regeln

### Tripel-Analyse Matching
- **Substring**: `Aufklaerung` in `Aufklaerungsbroschueren` -> merge in `Aufklaerung`
- **Plural/Umlaut**: `Raum` = `Raeume`, `Teil` = `Teile`, `Buch` = `Buecher`
- **Erstes-Wort**: `Autismus ADHS` matcht `Autismus Beruf` (gleicher Anfang)

### Mindestlaenge
- Einwort-Name ohne Leerzeichen: **mindestens 8 Zeichen** (verhindert `Hand`, `Haus`, `Form`)
- Mit Leerzeichen (z.B. `ICF Katalog`): **ab 3 Zeichen OK**
- Damit bleiben `ICF`, `ASS Frauen` etc. erlaubt

### Neustart nach Merge
Nach jedem Merge wird die Ordnerliste neu geladen und beim Merge-Ziel neu gestartet.
So sammelt z.B. `Autismus` alle Erweiterungen ein bevor es weitergeht.

---

## Medienformat-Merge (Template-System)

Phase 6 nutzt ein Template-Array `MEDIA_TYPES`. Jeder Eintrag definiert:
- Zielordner (mit `_` Prefix)
- Dateiendungen die zu diesem Typ gehoeren

```bash
MEDIA_TYPES=(
    "_Audio|mp3|m4a|wav|flac|ogg|wma|aac|opus|aiff"
    "_Video|mp4|avi|mkv|mov|wmv|flv|webm|m4v|mpg|mpeg|3gp"
    "_Bilder|jpg|jpeg|png|gif|bmp|tiff|tif|webp|svg|ico|heic|heif|raw|cr2|nef"
    # Erweiterbar:
    # "_Tabellen|xlsx|xls|csv|ods"
    # "_Prasentationen|pptx|ppt|odp"
    # "_Code|py|js|ts|sh|bat|ps1"
    # "_CAD|dwg|dxf|step|stl"
    # "_3D|obj|fbx|blend|gltf|glb"
    # "_Fonts|ttf|otf|woff|woff2"
)
```

Nur Ordner die **ausschliesslich** Dateien eines Typs enthalten werden verschoben.
Ordner mit Unterordnern werden uebersprungen.

### Neuen Medientyp hinzufuegen

Einfach neue Zeile im `MEDIA_TYPES` Array ergaenzen:
```bash
"_Zielordner|ext1|ext2|ext3"
```

---

## Ausfuehrung

```bash
# Kompletter Durchlauf:
cd /pfad/zum/zielverzeichnis
bash ordner_flattening_komplett.sh

# Oder einzelne Phasen:
bash ordner_flattening_komplett.sh --phase flatten
bash ordner_flattening_komplett.sh --phase tripel
bash ordner_flattening_komplett.sh --phase media
bash ordner_flattening_komplett.sh --phase cleanup
```

---

## Erfahrungswerte Session 26.01.2026

- Start: 206 Ordner + 252 lose Dateien, ~5600 verschachtelte Unterordner
- Nach Flatten: ~2200 Ordner auf einer Ebene
- Nach Kuerzen + Bereinigen: ~2005 Ordner
- Nach Gruppieren (Zahlen, CDs): ~2005 -> Sammelordner erstellt
- Nach Tripel v1: ~1561 Ordner
- Nach Tripel v2 (8-Zeichen-Regel): weitere Reduktion
- Medienformat-Phase: Audio/Video/Bilder-Ordner konsolidiert
