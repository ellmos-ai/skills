---
name: roblox-studio
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: >
  Bedienung von Roblox Studio für die Spieleentwicklung — der visuelle Editor, in dem die 3D-Szene
  gebaut, getestet und veröffentlicht wird. Nutze diesen Skill für: Studio-Grundbedienung (Explorer,
  Workspace, Play-Test, Place als .rbxl speichern), das Zusammenspiel mit Rojo (Connect, Szene-vs-Code-
  Modus), die KI-Steuerung von Studio per Roblox-Studio-MCP (execute_luau, insert_from_creator_store,
  generate_material, screen_capture, Play/Stop, Console lesen), den kompletten Asset-Pipeline-Workflow
  (Creator Store → bereinigen → Kit → Szene → .rbxl → Rojo belebt) und vor allem den PFLICHT-Malware-Scan
  für Marketplace-Assets. Auch auslösen bei "Asset aus dem Store einbauen", "Studio MCP geht nicht",
  "studios: []", "Material generieren", "Szene speichern", "ist dieses Roblox-Asset sicher", "Scripts
  verschwinden nach Play".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: game-dev
tags: [roblox, studio, mcp, assets, creator-store, malware, luau, gamedev]
language: de
status: active

dependencies:
  tools: [rojo]
  services: [roblox-studio-mcp]
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/roblox-studio/"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Roblox Studio — Editor, Test, Assets, MCP

## Zweck

Roblox Studio ist der offizielle Editor: 3D-Szene bauen, das Spiel im Play-Modus testen,
Assets aus dem Creator Store einfügen und den Place veröffentlichen. In einem Rojo-Workflow
übernimmt Studio die **Szene** (Workspace, Terrain, platzierte Modelle) und das **Testen** —
der **Code** kommt per Rojo aus dem Dateisystem (siehe Skill `/rojo`).

Dieser Skill deckt ab: Studio-Grundbedienung, die saubere Trennung von Szene- und Code-Arbeit,
die KI-Steuerung über das Roblox-Studio-MCP und den Asset-Workflow inklusive des
**Pflicht-Malware-Scans** für jedes Marketplace-Asset.

## Grundbedienung

- **Explorer** — Baum aller Instanzen (Workspace, ServerScriptService, ReplicatedStorage, …).
  Bei aktivem Rojo werden die gemappten Bereiche live aus dem Dateisystem befüllt.
- **Play-Test** — grüner Play-Button (oder F5) startet eine lokale Server+Client-Session.
  Nach jedem Start **die Output-Console auf Fehler prüfen** — der wichtigste Debug-Reflex.
- **Place speichern** — File → Save As → `.rbxl` (binär) oder `.rbxlx` (XML, diffbar).
  Der gespeicherte Place enthält die **Szene**. Code lebt im Dateisystem, nicht im Place.

## Der kritische Workflow: Szene-Modus vs. Code-Modus

Rojo überschreibt beim Connect alle gemappten Skript-Bereiche mit dem Dateisystem-Inhalt.
Der `Workspace` (3D-Szene) wird **nicht** gemappt und bleibt erhalten. Daraus folgt die
wichtigste Regel der täglichen Arbeit — niemals beide Modi vermischen:

**Modus A — Szene bearbeiten (Rojo AUS):**
1. Rojo-Server stoppen (`taskkill //F //IM rojo.exe` bzw. Ctrl+C).
2. Place in Studio öffnen, Assets platzieren, Welt bauen, anordnen.
3. File → Save → die `.rbxl` hat jetzt die neue Szene.

**Modus B — Code testen (Rojo AN):**
1. Denselben Place in Studio öffnen.
2. `rojo serve` starten → in Studio Rojo-Plugin → Connect.
3. Play drücken und testen. Rojo synct die Scripts; der Workspace kommt aus der `.rbxl`.
4. Während Rojo läuft **nicht** speichern (sonst friert der Rojo-Zustand in die `.rbxl` ein).

So können Szenen-Arbeit (Studio) und Code-Arbeit (Editor + Rojo) parallel und konfliktfrei
laufen — Künstler bauen Szenen, Entwickler schreiben Code.

## Roblox-Studio-MCP — KI steuert Studio

Das Roblox-Studio-MCP erlaubt Claude/Gemini/Codex, eine **laufende** Studio-Instanz direkt zu
steuern: Code ausführen, inspizieren, Play/Stop, Console lesen, Assets einfügen. Es ersetzt
Rojo **nicht** — es ergänzt es: Rojo für persistente Code-Änderungen, MCP für Inspektion,
Tests, Asset-Insertion und Materialerzeugung.

```
Editor + Rojo  ──(persistenter Code-Sync)──►  Studio (laufend)  ◄──(Inspektion/Test/Insert)──  MCP ◄── KI
```

### Verfügbare MCP-Tools (typisch)

| Tool | Zweck |
| --- | --- |
| `list_roblox_studios` / `set_active_studio` | offene Instanzen auflisten / aktive wählen |
| `search_game_tree` / `inspect_instance` | Hierarchie durchsuchen / Properties auslesen |
| `execute_luau` | Luau-Code direkt in Studio ausführen |
| `script_read` / `script_grep` / `script_search` | Scripts analysieren |
| `multi_edit` | mehrere Instanzen/Scripts gebündelt ändern |
| `start_stop_play` | Play/Stop steuern |
| `get_console_output` | Output-Log lesen |
| `screen_capture` | Screenshot der Szene |
| `insert_from_creator_store` | Asset aus dem Creator Store einfügen |
| `generate_material` | KI-Material/Textur erzeugen (MaterialVariant) |
| `character_navigation` / `user_keyboard_input` / `user_mouse_input` | Eingabe simulieren |

### Setup (nutzerneutral)

Das MCP läuft als von Studio mitgelieferter Server, oft über einen schmalen JSON-Filter-Wrapper
angebunden (filtert Nicht-JSON-Banner heraus, den manche Clients sonst nicht parsen):

- MCP-Batch (Windows): `%LOCALAPPDATA%\Roblox\mcp.bat`
- optionaler Wrapper: `<your roblox-mcp wrapper>`
  (falls auf diesem System vorhanden; teilen sich Claude/Codex/Gemini)
- Client-Configs: `~/.claude/mcp.json` · `~/.codex/config.toml` · `~/.gemini/antigravity/mcp_config.json`

Beispiel-Eintrag (`~/.claude/mcp.json`):
```json
{
  "mcpServers": {
    "Roblox_Studio": {
      "command": "node",
      "args": ["<your roblox-mcp wrapper>",
               "cmd.exe", "/c", "%LOCALAPPDATA%\\Roblox\\mcp.bat"]
    }
  }
}
```

### Häufige MCP-Probleme

| Symptom | Bedeutung / Lösung |
| --- | --- |
| `studios: []` oder `Not connected to WS host` | nicht sofort "kaputt": `initialize` senden → 2–3 s warten → `list_roblox_studios`; sonst Studio neu starten |
| `Error: connection closed: initialized request` | Studio ist gar nicht offen — Studio starten, Place laden, erneut versuchen |
| per MCP geschriebene Scripts weg nach Play/Stop | MCP-Edits am Code sind nicht persistent — für bleibende Code-Änderungen **Rojo** nutzen |
| Wert per `require()` im Plugin-VM stimmt nicht | Plugin-VM hat eigenen require-Cache — zur Verifikation `.Source` direkt lesen oder Server-Log nach Play prüfen |

## Asset-Pipeline (Creator Store → Spiel)

Greybox zuerst (Gameplay), Assets später (vor Release). Der bewährte Ablauf:

```
STORE DURCHSUCHEN   → z. B. "medieval" → mehrere Kandidaten laden
AUSSORTIEREN        → stilfremde/hässliche raus, 5–8 passende behalten
BEREINIGEN          → ALLE Scripts entfernen (Malware!), nur Geometrie/Meshes behalten
KIT / SET BAUEN     → aus Basis-Assets Varianten ableiten (gleiche Materials/Proportionen)
SZENE BAUEN (Studio)→ Assets zur Kulisse zusammensetzen (Dorf, Arena, Park)
ALS .RBXL SPEICHERN → die Kulisse ist die "Bühne"
ROJO BELEBT ES      → Scripts/Gameplay/HUD kommen per Rojo dazu; Workspace bleibt unangetastet
```

**Varianten-Technik ("Modular Kit"):** Ein gutes Basis-Asset nehmen und daraus ein ganzes
Set ableiten (Haus → Turm, Scheune, Schmiede, Ruine). Alle teilen Materials, Farben und
Proportionen → konsistenter Look mit minimalem Aufwand, wie es Profi-Studios tun.

**Asset-Quellen (Priorität):** Creator Store (gratis, riesig, **Malware-Check Pflicht**) →
KI-Materials (`generate_material`) → eigene Meshes (Blender → .fbx) → gekaufte Asset-Packs.

## PFLICHT: Malware-Scan für Marketplace-Assets

Creator-Store-Assets können obfuskierte Schad-Scripts enthalten (Backdoors, Remote-Code,
Bot-Netzwerk-Hooks). **Jedes** importierte Asset vor der Nutzung scannen und alle Scripts
entfernen — behalte nur Geometrie/Meshes.

- Muster-Referenz: [`references/malware-patterns.md`](references/malware-patterns.md) — die 8
  bekannten Obfuskationsmuster (reversed Attribute-Payload, fake System-Script, remote
  `require()`, `loadstring`, `string.char`, `getfenv/setfenv`, hidden Values, delayed execution).
- Scanner: [`scripts/scan_asset_malware.luau`](scripts/scan_asset_malware.luau) — in Studio per
  `execute_luau` (oder Command Bar) ausführen; prüft eine Instanz auf alle Muster und meldet Funde.

**Red Flags sofort:** großes Script in einem reinen Deko-Modell · reversed Strings in
Attributen · `require(<Zahl>)` · `loadstring` · `HttpService` in einem Asset, das keine Netzwerk
braucht. Im Zweifel: Script löschen. Funde dokumentieren (z. B. `_malware_reports/YYYY-MM-DD_*.md`
in der Referenz-Pipeline).

## Wichtige Luau-/Studio-Fallstricke (Auszug)

Die häufigsten, die in Studio beißen — die vollständige Liste hält der Skill `/roblox-dev`:

- `Model.Position` existiert nicht → `model:GetPivot().Position`.
- `tick()` ist deprecated → `os.clock()` / `workspace:GetServerTimeNow()`.
- `SetPrimaryPartCFrame()` deprecated → `model:PivotTo(cf)`.
- DataStore-Calls **immer** in `pcall`.
- Baseplate + prozeduraler Boden auf gleicher Höhe → Z-Fighting (Flackern): Baseplate entfernen
  oder Boden +0.1 Studs anheben.
- Part-Budget im Blick behalten (~50–80 Parts pro prozedural generiertem Raum).

## Weiterführend

- Schwesterskills: `/rojo` (Sync, Projekt-Setup), `/game-design` (Rollen, Workflows, GDD),
  Metaskill `/roblox-dev` (Architektur-Pattern + alle Luau-Lessons).
- Engine-/Creator-Doku: Context7 MCP (`/websites/create_roblox_reference_engine`,
  `/roblox/creator-docs`) oder <https://create.roblox.com/docs>.
- Referenz-Pipeline (falls vorhanden): `<your Roblox project pipeline>`
  (`ROBLOX_MCP_FAQ.md`, `ASSET_PIPELINE.md`, `_malware_reports/PATTERNS.md`).

## Changelog

### 1.0.0 (2026-06-17)
- Initiale Version. Destilliert aus der `.ROBLOX`-Pipeline (ROBLOX_MCP_FAQ, ASSET_PIPELINE,
  PATTERNS, LESSONS_LEARNED), nutzerneutral gefasst.
