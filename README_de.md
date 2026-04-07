# Skills Library

**🇬🇧 [English Version](README.md)**

**Standalone-Skillbibliothek** -- portierbare KI-Skills im Anthropic-kompatiblen Format.

Skills können eigenständig (standalone) oder als Teil eines größeren Systems (z.B. BACH) genutzt werden. Die Herkunft, der Sync-Status und die Abhängigkeiten sind **direkt in jeder SKILL.md** im YAML-Frontmatter hinterlegt -- keine zentrale Steuerdatei nötig.

## Struktur

```
skills/
  <kategorie>/
    <skill-name>/
      SKILL.md              # Definition + Provenance + Abhängigkeiten
      scripts/              # Optional: ausführbarer Code
      references/           # Optional: Referenzdokumente
  _templates/               # Vorlagen für neue Skills
  _examples/                # Beispiel-Skills
docs/
  CONVENTIONS.md            # Frontmatter-Spezifikation
catalog.py                  # CLI: Katalog, Sync-Status, Suche
```

## Skill-Typen

| Typ | Beschreibung |
|-----|-------------|
| `skill` | Allgemeine Fähigkeit (Standard) |
| `agent` | Orchestriert andere Skills/Experten |
| `expert` | Tiefes Domänenwissen |
| `service` | Hintergrunddienst |
| `protocol` | Ablauf-/Workflow-Anleitung |
| `tool` | Ausführbares Werkzeug (mit Script) |

## Standalone vs. System-gebunden

Jede SKILL.md deklariert über Frontmatter-Felder, ob sie eigenständig funktioniert:

```yaml
standalone: true             # Funktioniert ohne externes System
bach_compatible: true        # Kann in BACH geladen werden
bach_origin: true            # Stammt aus BACH
```

Details: [docs/CONVENTIONS.md](docs/CONVENTIONS.md)

## Schnellstart

```bash
# Katalog anzeigen
python catalog.py list

# Skill nach Kategorie filtern
python catalog.py list --category productivity

# Sync-Status prüfen (welche Skills sind veraltet?)
python catalog.py sync-status

# Neuen Skill aus Template erstellen
python catalog.py create "mein-skill" --category productivity --type skill
```

## Provenance-System

Jeder Skill trägt seine Herkunft in sich:

```yaml
provenance:
  origin: "bach"                          # bach | custom | community
  origin_path: "system/skills/therapie/"  # Quellpfad im Ursprungssystem
  origin_version: "1.0.0"                # Version beim Export
  last_sync_from_origin: "2026-03-12"    # Letzter Import
  last_sync_to_origin: null              # Letzter Rückfluss
  local_changes_since_sync: false        # Lokale Änderungen?
```

So ist jederzeit nachvollziehbar: Woher kommt der Skill? Auf welchem Stand ist er? Wurde er lokal verändert?

## Lizenz

MIT License -- siehe [LICENSE](LICENSE)
