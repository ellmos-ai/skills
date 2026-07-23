# Blender MCP und Skill-Quellen Review

Stand: 2026-06-20. Zweck: Quellenlage für Blender-Automation bewerten, ohne fremden Code blind zu übernehmen.

## Bewertete Quellen

| Quelle | Lizenz | Nutzbar? | Entscheidung |
|---|---|---|---|
| `ahujasid/blender-mcp` | MIT | eingeschränkt | Funktionsideen nutzbar, aber wegen Telemetrie-/Consent-Diskussion nicht als Standard übernehmen. Wenn genutzt: `DISABLE_TELEMETRY=true`, Netzwerk-/API-Features auslassen und Addon-Code auditieren. |
| `djeada/blender-mcp-server` | MIT | ja | Gute Referenz für eine nüchterne MCP-Struktur: stdio-Server, TCP-Bridge zum Blender-Addon, Tool-Namensräume, Export/Render/Python-Jobs. Keine direkte Codeübernahme in diesen Skill. |
| `@glutamateapp/blender-mcp-ts` | MIT | ja | TypeScript-MCP-Idee mit SSE und Blender-Socket-Connector. Für lokale ellmos-MCPs ist stdio passender als SSE. |
| `freshtechbro/claudedesignskills` / `blender-web-pipeline` | MIT | ja | Gute Skill-Ideen für GLB/glTF, Batch-Export, Web-Optimierung. Wegen Umfang nicht kopieren; lokale Skills bleiben knapper und allgemeiner. |
| `youichi-uda/blender-mcp-pro` | teils proprietär | nein | Nur als Feature-Idee betrachten; keine Übernahme. |
| `patrykiti/blender-ai-mcp` | Apache-2.0 | nein für Übernahme | Lizenz nicht MIT; nur als Konzeptsignal für production-shaped Blender-MCPs betrachten. |

## Lizenznotiz

In `using-blender`, `build-assets-with-blender` und `blender-use-mcp` wurde kein Quellcode aus externen Repositories vendored oder kopiert. Übernommen wurden nur selbst neu formulierte Workflow-Ideen aus öffentlich sichtbaren MIT-Quellen. Wenn später konkreter Code aus MIT-Repositories übernommen wird, muss die jeweilige MIT-Lizenz mit Copyright-Hinweis im Zielprojekt dokumentiert werden.

## Praktische Schlüsse

- Für robuste Batch-Arbeit zuerst Headless-Blender nutzen; das ist einfacher, auditierbarer und braucht kein Live-Addon.
- Für Live-Szenensteuerung ist ein MCP sinnvoll, aber nur mit klarer Toolbegrenzung, lokalen Ports und ohne Default-Telemetrie.
- `execute Python in Blender` ist mächtig und riskant. Es braucht Pfadgrenzen, Timeouts und eine bewusste Vertrauensentscheidung für jedes Script.
- Für Roblox/Game-Assets ist der wichtigste Erfolgsnachweis nicht ein hübscher Prompt, sondern ein Reimport-JSON plus saubere Manifest-/Pickup-Doku.
