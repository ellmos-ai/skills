# Scaffold-Report — agent-config-sync (0.1.0)

> Stand: 2026-06-20. Kurzbericht zum Design + Scaffold. Enthaelt KEINE echten Pfade.

## Gap-Analyse `mcp-config-sync`

- **Kann:** MCP-Server spiegeln, aber NUR Claude Code <-> Claude Desktop, NUR ein Rechner,
  ein OS-Skript pro Plattform, Master-Datei als einzige Quelle.
- **Fehlt:** weitere Agent-Tools (Codex/Gemini/Kimi/Cursor/Cline/Windsurf/Copilot);
  Skills-Sync (nur als Reference dokumentiert, nicht ausgefuehrt); deklarative Registry
  (welche Tools syncen wie); regelbasierte Richtung (pull vs. verteilen) statt 1 fixer Pfad.
- **Fehlt:** Lernmechanismus fuer veraltete/unbekannte Config-Orte; Multi-System-Modell.
- **Empfehlung:** neuer uebergreifender Skill `agent-config-sync`, der `mcp-config-sync`
  als Registry-Beziehung `claude-pair` (pull, scope mcp) umschliesst. Altskill vorerst als
  Legacy behalten, nach `--apply`-Reife `deprecated` markieren.

## Modellierung

- **Registry** (Steuerebene, lokal): `host`, `tools{installed,role}`, `relations[]` mit
  `mode` (pull/push/bidirectional), `source`, `scope` (mcp/skills/both). Teilmengen erlaubt
  ueber `role` (hub/member/leaf). `host`-Feld macht es multi-system-faehig (Default: ein Host).
- **Config** (publizierbar): je Anbieter `mcp.path/format/key/merge` + `skills.path/kind`
  + `notes`/`sources`/`updated`. Unverifizierte Eintraege als `UNVERIFIED` markiert.
- **Cache** (lokal): aufgeloeste reale Pfade + `exists` + `resolved_via` + `last_verified`.
- **Lernmechanismus:** fehlender Pfad → Systemsuche (FileCommander/Glob); unbekannter
  Anbieter → WebSearch; Format-Unsicherheit → WebSearch + Context7; Treffer aktualisieren
  `config.json` (mit `sources`+`updated`).

## Privacy

- Publizierbar: SKILL.md, CONFIG.md, config.json, REGISTRY.md, registry.example.json,
  CACHE.md, cache.example.json, scripts/, references/, dieser Report (nur Platzhalter).
- Lokal/gitignored: `registry.json`, `cache.json` (in `.SKILLS/.gitignore` ergaenzt).
- Verifiziert: keine echten Pfade/Hosts/IPs in publizierbaren Dateien (Author-Frontmatter
  konsistent mit allen anderen Skills).

## Offene Punkte (Implementierungs-Stufe)

1. `--apply` implementieren: format-erhaltendes block-replace pro Provider, JSON↔TOML
   (Codex `mcp_servers`), Backup+Verify. Bewaehrte OS-Skripte von `mcp-config-sync` als
   Schreib-Backend uebernehmen.
2. Skills-Sync real: Verzeichnis-Abgleich + Bridge fuer Apps ohne direkten Skill-Pfad.
3. UNVERIFIED-Anbieter (Gemini/Kimi/Cline/Windsurf/Copilot) per Lernmechanismus belegen.
4. Konflikt-Eskalation bei `bidirectional` ausgestalten.
5. Tests (frische Subagenten) + Multi-System-Transport ueber `~/OneDrive/.SYNC/`.
6. Nach Reife: `mcp-config-sync` auf `deprecated` + Verweis; ggf. via `skill_sync.py` deployen
   (User-Entscheid).
