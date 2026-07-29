# System-Inventar

> Reference-Datei zum Skill `agents-bridge`. Wo liegt was, und wie wird es gepflegt?

## Ort

`~/OneDrive/.SYNC/_inventory/`

## Zweck

Fuer jedes System (Workstation / Laptop / Mac) wird festgehalten, was lokal installiert ist. Damit:

- **Re-Installation** auf neuem Geraet kann gegen das Inventar abgeglichen werden — Skript `system-onboarding/scripts/...` liest das Inventar und schlaegt fehlende Tools vor.
- **Spezialisierungen** sind sichtbar (Workstation hat Roblox Studio + MiKTeX + grosse GPU; Laptop ist mobil-optimiert; Mac hat XCode).
- **Backup-Status** pro Ordner ist nachvollziehbar (lokal-only / OneDrive / git / none).
- **Excel-Export** fuer menschliche Uebersicht bei Quartalscheck.

## Datenmodell (SQLite)

```
inventory.db
├── systems        Ein Eintrag pro Rechner
├── software       Installierte Tools/Apps pro System
├── skills         User-Skills pro System (claude-code, codex)
├── mcps           MCP-Server pro System pro App
├── plugins        Plugins/Extensions pro System pro App
├── connectors     Auth-basierte Connectors
├── agents         Persona-Agenten (BACH, custom)
├── pipelines      Multi-Step-Workflows
└── folders        Wichtige Ordner mit Backup-Status
```

Vollschema: `~/OneDrive/.SYNC/_inventory/scripts/schema.sql`.

## Workflow

1. **Initial-Erfassung pro System** (einmalig pro neuem Rechner):
   ```
   ~/OneDrive/.SYNC/_inventory/scripts/build-inventory.py
   ```
   Erzeugt `inventory.db` aus den JSON-Seed-Dateien in `systems/<name>/`.

2. **Update bei Aenderung** (z.B. neuer Skill installiert, neuer MCP konfiguriert):
   ```
   ~/OneDrive/.SYNC/_inventory/scripts/update-inventory.ps1   # Windows
   ~/OneDrive/.SYNC/_inventory/scripts/update-inventory.sh    # Mac
   ```
   Liest live vom System, schreibt in die JSON-Seed-Datei des aktuellen Systems.

3. **Excel-Export** (fuer Quartal-Check):
   ```
   ~/OneDrive/.SYNC/_inventory/scripts/export-xlsx.py
   ```
   Erzeugt `inventory.xlsx` mit einem Sheet pro Tabelle.

4. **Suche** (fuer schnelle Antworten):
   ```
   ~/OneDrive/.SYNC/_inventory/scripts/query.ps1 "skill:therapy"
   ~/OneDrive/.SYNC/_inventory/scripts/query.ps1 "system:workstation mcp:context7"
   ```

## Wichtig

- **JSON-Seeds sind die Quelle** der Wahrheit. Die DB ist materialisiert und kann jederzeit neu gebaut werden.
- **Kein Auto-Discovery ueber alle Systeme** — jedes System pflegt nur seinen eigenen Slot. Cross-System-Sicht entsteht durch das gemeinsame `_inventory/` im OneDrive-SYNC.
- **Keine Credentials** in den JSON-Seeds. Nur Existenz-Information ("hat Tool X"), nicht Auth-Daten.

## Bezug zum AGENTS-BRIDGE-Skill

Dieser Skill (AGENTS-BRIDGE) hilft fremden Tools/IDEs, die kanonischen Regeln zu finden. Wenn ein Tool registriert wird, gehoert es ins Inventar — Tabelle `software` mit category `ide` oder `agent`. Das Inventar ist also das Datenmodell, AGENTS-BRIDGE die Bedienoberflaeche fuer "wie binde ich Tool X an".
