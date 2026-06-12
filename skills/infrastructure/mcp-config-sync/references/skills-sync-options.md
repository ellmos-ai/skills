# User-Skills-Sync zwischen Claude Code und Claude Desktop — Optionen

> Stand: 2026-04-30. Reference-Datei zum Skill `mcp-config-sync`.

## Aktueller Stand

- Claude Code liest `~/.claude/skills/` automatisch
- Claude Desktop liest **nicht** aus `~/.claude/skills/`. Es nutzt einen session-internen Pfad unter `%APPDATA%\Claude\local-agent-mode-sessions\skills-plugin\<id>\<id>\skills\`, der von Anthropic verwaltet wird (Standard-Skills wie `pdf`, `docx`, `xlsx`, `pptx`, `canvas-design`).
- Plugin-Skills (z.B. `nimble:meeting-prep`) erscheinen in beiden Apps, weil sie ueber das Plugin-System geladen werden.

## Optionen, Custom-Skills auch in Claude Desktop nutzbar zu machen

### Option 1 — Bridge-Skill verwenden (empfohlen, sauber)

Einen eigenen **Index-Skill** in Claude Desktop installieren (Drag & Drop oder Skill-Creator-Paketinstallation): ein kleiner Skill, der einen **Index** der Live-Skills mit deren Pfaden enthaelt. Bei jedem Aufruf liest Claude Desktop die Live-Datei am angegebenen Pfad.

Vorteile:
- Funktioniert ohne Junction
- Keine Anthropic-Update-Konflikte
- Kein Doppel-Pflege-Aufwand
- Aktualisierungen am Live-Skill werden automatisch gelesen

### Option 2 — Als Plugin verpacken (sauber, aber Aufwand)

Skill in einen Plugin-Ordner mit `plugin.json` packen, ueber `~/.claude/plugins/` als lokales Plugin ablegen oder in einem eigenen Marketplace-GitHub-Repo bereitstellen. Wird dann von beiden Apps geladen.

Vorteile:
- Native Erkennung in beiden Apps
- Saubere Versionierung

Nachteile:
- Aufwand fuer jeden Skill
- Setup eines lokalen Marketplaces

### Option 3 — Hochladen pro Session (pragmatisch)

Skill-Datei beim Cowork-Start in den Chat ziehen — Claude Desktop nutzt sie fuer die laufende Session.

Vorteile:
- Sofort einsatzbereit, kein Setup

Nachteile:
- Manuell pro Session
- Nur kurzfristig

### Option 4 — Junction setzen (NICHT empfohlen, fragil)

Den session-internen Skills-Pfad per Junction auf `~/.claude/skills/` zeigen lassen.

Risiken:
- Anthropic-Updates ueberschreiben die Junction
- Standard-Skills koennen ueberschrieben werden
- Cowork-Modus haengt am session-internen Layout — Aenderungen am Layout brechen die Junction
- Im Schaden steht Claude Desktop ohne funktionierende Skill-Quelle

**Konkret nicht zu empfehlen, weil:**
- Cowork-Sessions liegen in `%APPDATA%\Claude\local-agent-mode-sessions\<dynamic-id>\<dynamic-id>\skills-plugin\<id>\<id>\skills\` mit dynamischen IDs.
- Eine Junction muesste pro Session neu gesetzt werden.

## Empfehlung

Standardweg ist **Option 1** (Bridge-Skill): einen kleinen Index-Skill anlegen, der die eigenen Live-Skills mit Pfaden auflistet, und diesen in Claude Desktop installieren.
