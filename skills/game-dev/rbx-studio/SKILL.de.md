---
name: rbx-studio
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "Roblox Studio für die Spielentwicklung betreiben: der visuelle Editor, in dem die 3D-Szene gebaut, getestet und veröffentlicht wird. Verwende diesen Skill für: Studio-Grundlagen (Explorer, Workspace, Play-Test, Speichern des Places als .rbxl), das Zusammenspiel mit Rojo (Connect, Modus Szene vs. Code), KI-Steuerung von Studio über den Roblox-Studio-MCP (execute_luau, insert_from_creator_store, generate_material, screen_capture, Play/Stop, Lesen der Konsole), den vollständigen Asset-Pipeline-Workflow (Creator Store → bereinigen → Kit → Szene → .rbxl → Rojo erweckt sie zum Leben) und vor allem die VERPFLICHTENDE Malware-Prüfung für Marktplatz-Assets. Löse diesen Skill auch aus bei „ein Asset aus dem Store einbetten“, „Studio MCP funktioniert nicht“, „studios: []“, „Material generieren“, „Szene speichern“, „ist dieses Roblox-Asset sicher“, „Skripte verschwinden nach Play“."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [roblox, studio, mcp, assets, creator-store, malware, luau, gamedev]
language: de
status: active
visibility: public
dependencies: {'tools': ['rojo'], 'services': ['roblox-studio-mcp'], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/rbx-studio/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: 9d0fca2a40692abba63ce104ab8f69627490f5cd4adf2ead8a6da3ad00f4d7b2
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:52:38.401999+00:00"
---
<img src="banner.png" width="100%" alt="rbx-studio banner">

> **Deutsch** — Offizielle deutsche Version / Offizielles Dokument auf Deutsch.


> **Note:** Nicht mit der Roblox Corporation verbunden; „Roblox“ ist eine Marke ihrer Inhaber. „rbx“ ist die gebräuchliche Abkürzung in der Community.



# Roblox Studio — Editor, Test, Assets, MCP (Deutsch)

## Übersicht & Zweck

Roblox Studio ist der offizielle Editor: Baue die 3D-Szene, teste das Spiel im Spielmodus,
füge Assets aus dem Creator Store ein und veröffentliche den Place. In einem Rojo-Workflow
verwaltet Studio die **Szene** (Workspace, Terrain, platzierte Modelle) und das **Testen**;
der **Code** kommt über Rojo aus dem Dateisystem (siehe Skill `/rojo`).

Dieser Skill behandelt: Studio-Grundlagen, die klare Trennung von Szenen- und Codearbeit,
die KI-Steuerung über den Roblox-Studio-MCP sowie den Asset-Workflow einschließlich der
**verpflichtenden Malware-Prüfung** für jedes Marktplatz-Asset.

## Grundlagen

- **Explorer**: Baum aller Instanzen (Workspace, ServerScriptService, ReplicatedStorage, …).
  Ist Rojo aktiv, werden die zugeordneten Bereiche live aus dem Dateisystem befüllt.
- **Play-Test**: Der grüne Play-Button (oder F5) startet eine lokale Server- und Client-Sitzung.
  Prüfe nach jedem Start die **Output-Konsole auf Fehler**. Das ist der wichtigste Debugging-Reflex.
- **Place speichern**: File → Save As → `.rbxl` (binär) oder `.rbxlx` (XML, diff-fähig).
  Der gespeicherte Place enthält die **Szene**. Der Code liegt im Dateisystem, nicht im Place.

## Der kritische Workflow: Szenenmodus vs. Codemodus

Beim Connect überschreibt Rojo alle zugeordneten Skriptbereiche mit dem Inhalt des Dateisystems.
Die `Workspace` (3D-Szene) ist **nicht** zugeordnet und bleibt unverändert. Daraus folgt die
wichtigste Regel der täglichen Arbeit: Beide Modi niemals vermischen.

**Modus A: Szene bearbeiten (Rojo AUS):**
1. Stoppe den Rojo-Server (`taskkill //F //IM rojo.exe` oder Strg+C).
2. Öffne den Place in Studio, platziere Assets, baue die Welt, ordne sie an.
3. File → Save → Die `.rbxl` enthält nun die neue Szene.

**Modus B: Code testen (Rojo AN):**
1. Öffne denselben Place in Studio.
2. Starte `rojo serve` → im Rojo-Plugin von Studio → Connect.
3. Drücke Play und teste. Rojo synchronisiert die Skripte; der Workspace stammt aus der `.rbxl`.
4. Solange Rojo läuft, **nicht** speichern (sonst friert der Rojo-Zustand in der `.rbxl` ein).

So können Szenenarbeit (Studio) und Codearbeit (Editor + Rojo) parallel und
konfliktfrei laufen: Artists bauen Szenen, Entwickler schreiben Code.

## Roblox-Studio-MCP: KI steuert Studio

Der Roblox-Studio-MCP erlaubt Claude, Gemini und Codex, eine **laufende** Studio-Instanz
direkt zu steuern: Code ausführen, inspizieren, Play/Stop, die Konsole lesen und Assets einfügen. Er
ersetzt Rojo **nicht**, sondern ergänzt es: Rojo für dauerhafte Codeänderungen, MCP für Inspektion,
Tests, Asset-Einfügung und Materialgenerierung.

```
Editor + Rojo  ──(persistenter Code-Sync)──►  Studio (laufend)  ◄──(Inspektion/Test/Insert)──  MCP ◄── KI
```

### Verfügbare MCP-Tools (typisch)

| Tool | Zweck |
| --- | --- |
| `list_roblox_studios` / `set_active_studio` | offene Instanzen auflisten / die aktive auswählen |
| `search_game_tree` / `inspect_instance` | die Hierarchie durchsuchen / Eigenschaften lesen |
| `execute_luau` | Luau-Code direkt in Studio ausführen |
| `script_read` / `script_grep` / `script_search` | Skripte analysieren |
| `multi_edit` | mehrere Instanzen/Skripte stapelweise ändern |
| `start_stop_play` | Play/Stop steuern |
| `get_console_output` | das Output-Log lesen |
| `screen_capture` | Screenshot der Szene |
| `insert_from_creator_store` | ein Asset aus dem Creator Store einfügen |
| `generate_material` | ein KI-Material/eine KI-Textur (MaterialVariant) generieren |
| `character_navigation` / `user_keyboard_input` / `user_mouse_input` | Eingaben simulieren |

### Einrichtung (benutzerneutral)

Der MCP läuft als Server, der mit Studio ausgeliefert wird. Er wird oft über einen schlanken
JSON-Filter-Wrapper angebunden. Dieser entfernt Nicht-JSON-Banner, die manche Clients sonst nicht parsen können:

- MCP-Batchdatei (Windows): `%LOCALAPPDATA%\Roblox\mcp.bat`
- optionaler Wrapper: `<your roblox-mcp wrapper>`
  (falls auf diesem System vorhanden; von Claude/Codex/Gemini gemeinsam genutzt)
- Client-Konfigurationen: `~/.claude/mcp.json` · `~/.codex/config.toml` · `~/.gemini/antigravity/mcp_config.json`

Beispieleintrag (`~/.claude/mcp.json`):
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
| `studios: []` oder `Not connected to WS host` | nicht sofort „kaputt“: sende `initialize` → warte 2–3 s → `list_roblox_studios`; andernfalls Studio neu starten |
| `Error: connection closed: initialized request` | Studio ist überhaupt nicht geöffnet: Studio starten, Place laden, erneut versuchen |
| über MCP geschriebene Skripte nach Play/Stop verschwunden | MCP-Änderungen am Code sind nicht dauerhaft: für bleibende Codeänderungen **Rojo** verwenden |
| Wert über `require()` in der Plugin-VM ist falsch | die Plugin-VM hat ihren eigenen require-Cache; zur Überprüfung `.Source` direkt lesen oder nach Play das Server-Log prüfen |

## Asset-Pipeline (Creator Store → Spiel)

Zuerst Greybox (Gameplay), später Assets (vor der Veröffentlichung). Die bewährte Abfolge:

```
STORE DURCHSUCHEN   → z. B. "medieval" → mehrere Kandidaten laden
AUSSORTIEREN        → stilfremde/hässliche raus, 5–8 passende behalten
BEREINIGEN          → ALLE Scripts entfernen (Malware!), nur Geometrie/Meshes behalten
KIT / SET BAUEN     → aus Basis-Assets Varianten ableiten (gleiche Materials/Proportionen)
SZENE BAUEN (Studio)→ Assets zur Kulisse zusammensetzen (Dorf, Arena, Park)
ALS .RBXL SPEICHERN → die Kulisse ist die "Bühne"
ROJO BELEBT ES      → Scripts/Gameplay/HUD kommen per Rojo dazu; Workspace bleibt unangetastet
```

**Variantentechnik („modulares Kit“):** Nimm ein gutes Basis-Asset und leite daraus eine ganze
Reihe ab (Haus → Turm, Scheune, Schmiede, Ruine). Alle teilen Materialien, Farben und
Proportionen, was ein einheitliches Erscheinungsbild mit minimalem Aufwand ergibt, so wie es professionelle Studios tun.

**Asset-Quellen (Priorität):** Creator Store (kostenlos, sehr groß, **Malware-Prüfung verpflichtend**) →
KI-Materialien (`generate_material`) → eigene Meshes (Blender → .fbx) → gekaufte Asset-Packs.

## VERPFLICHTEND: Malware-Prüfung für Marktplatz-Assets

Assets aus dem Creator Store können verschleierte bösartige Skripte enthalten (Backdoors, Remote Code,
Bot-Netz-Hooks). Prüfe **jedes** importierte Asset vor der Verwendung und entferne alle Skripte.
Behalte nur Geometrie und Meshes.

- Musterreferenz: [`references/malware-patterns.md`](references/malware-patterns.md): die 8
  bekannten Verschleierungsmuster (umgekehrte Attribut-Nutzlast, gefälschtes Systemskript, Remote
  `require()`, `loadstring`, `string.char`, `getfenv/setfenv`, versteckte Values, verzögerte Ausführung).
- Scanner: [`scripts/scan_asset_malware.luau`](scripts/scan_asset_malware.luau). Führe ihn in Studio über
  `execute_luau` aus (oder über die Command Bar). Er prüft eine Instanz gegen alle Muster und meldet Funde.

**Sofortige Warnsignale:** ein großes Skript in einem reinen Dekorationsmodell · umgekehrte Strings in
Attributen · `require(<number>)` · `loadstring` · `HttpService` in einem Asset, das keine
Netzwerkkommunikation benötigt. Im Zweifel: Skript löschen. Dokumentiere Funde (z. B. `_malware_reports/YYYY-MM-DD_*.md`
in der Referenz-Pipeline).

## Wichtige Luau-/Studio-Fallstricke (Auszug)

Die häufigsten, die in Studio tatsächlich Probleme machen. Die vollständige Liste führt der Skill `/rbx-dev`:

- `Model.Position` existiert nicht → `model:GetPivot().Position`.
- `tick()` ist veraltet → `os.clock()` / `workspace:GetServerTimeNow()`.
- `SetPrimaryPartCFrame()` ist veraltet → `model:PivotTo(cf)`.
- DataStore-Aufrufe **immer** in `pcall` ausführen.
- Baseplate und prozedurale Bodenfläche auf gleicher Höhe → Z-Fighting (Flackern): Entferne die Baseplate
  oder hebe den Boden um +0,1 Studs an.
- Behalte das Part-Budget im Blick (ca. 50–80 Parts pro prozedural erzeugtem Raum).

## Weiterführende Literatur

- Schwester-Skills: `/rojo` (Synchronisation, Projekteinrichtung), `/game-design` (Rollen, Workflows, GDD),
  Meta-Skill `/rbx-dev` (Architekturmuster und alle Luau-Lektionen).
- Engine-/Creator-Dokumentation: Context7 MCP (`/websites/create_roblox_reference_engine`,
  `/roblox/creator-docs`) oder <https://create.roblox.com/docs>.
- Referenz-Pipeline (falls vorhanden): `<your Roblox project pipeline>`
  (`ROBLOX_MCP_FAQ.md`, `ASSET_PIPELINE.md`, `_malware_reports/PATTERNS.md`).

## Änderungsprotokoll

### 1.0.0 (2026-06-17)
- Erstversion. Destilliert aus der Pipeline `.ROBLOX` (ROBLOX_MCP_FAQ, ASSET_PIPELINE,
  PATTERNS, LESSONS_LEARNED), benutzerneutral verfasst.
