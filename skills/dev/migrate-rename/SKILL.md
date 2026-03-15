---
name: migrate-rename
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: >
  Evolutionaere Datei-Umbenennung mit Wrapper-Dateien. Ermoeglicht Umbenennungen ohne harte Brueche — Verweise werden organisch durch Nutzung aktualisiert.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: dev
tags: [migration, umbenennung, wrapper, evolutionaer, refactoring]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/skills/workflows/migrate-rename.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-15"
  last_sync_to_origin: null
  local_changes_since_sync: true
---

# Datei-Umbenennung mit Wrapper (Evolutionaere Migration)

> Ermoeglicht Datei-Umbenennungen OHNE harte Brueche. Verweise werden organisch durch taegliche Nutzung aktualisiert.

---

## Prinzip: Evolutionaere Migration

```
VORHER:                          NACHHER:
alte_datei.md                    neue_datei.md (umbenannt)
   |                                |
   +-- Verweis A                    +-- alte_datei.md (Wrapper)
   +-- Verweis B                           |
   +-- Verweis C                           +-- Log-Tabelle
                                           +-- Anleitung
                                           +-- Link zu neue_datei.md
```

Wer den alten Pfad aufruft:
1. Landet bei der Wrapper-Datei
2. Traegt sich ins Log ein
3. Korrigiert den Verweis der ihn herschickte
4. Geht zur eigentlichen Datei

---

## Schritt-fuer-Schritt

### 1. Datei umbenennen

```bash
mv alte_datei.md neue_datei.md
```

### 2. Wrapper-Datei erstellen

Erstelle `alte_datei.md` mit folgendem Inhalt:

```markdown
# ALTE_DATEI.md - UMGELEITET

**Status:** Diese Datei wurde umbenannt zu `neue_datei.md`

---

## Migration-Log

| Datum | Wer | Herkunft | Verweis korrigiert? |
|-------|-----|----------|---------------------|
| YYYY-MM-DD | [Name] | Initiale Migration | n/a (Wrapper erstellt) |

---

## Anleitung

1. **Log-Eintrag hinterlassen** (oben in Tabelle)
2. **Herkunft pruefen**: Was hat dich hierher geschickt?
3. **Verweis korrigieren**: Aendere `alte_datei.md` -> `neue_datei.md`
4. **Zur eigentlichen Datei gehen**: [neue_datei.md](neue_datei.md)

---

**Zieldatei:** [neue_datei.md](neue_datei.md)
```

### 3. Kritische Verweise sofort korrigieren
- Help-Dateien (primaere Dokumentation)
- System-Prompt Referenzen
- CLI-Code der den Pfad direkt verwendet

### 4. Uebrige Verweise evolutionaer migrieren
Der Rest wird automatisch korrigiert bei Nutzung.

---

## Wann Wrapper-Methode verwenden?

**JA - Wrapper sinnvoll:**
- Viele potenzielle Verweise
- Datei wird von verschiedenen Partnern/Tools referenziert
- Keine kritische System-Datei

**NEIN - Direkt alle aendern:**
- Wenige, bekannte Verweise
- Kritische System-Dateien (config, DB-Schema)
- Performance-kritische Pfade

---

## Cleanup

Nach ca. 30 Tagen oder wenn Log zeigt dass keine neuen Eintraege:
1. Wrapper-Datei nach `_archive/deprecated/` verschieben
2. Oder komplett loeschen (wenn keine Eintraege mehr)

---

## Changelog

### 1.0.0 (2026-03-15)
- Portiert aus BACH v3.8.0

---

*Portiert aus BACH v3.8.0 | Standalone-Version*
