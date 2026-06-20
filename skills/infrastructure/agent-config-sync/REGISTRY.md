# REGISTRY — was syncen welche Tools wie?

> Das **Template** (`registry.example.json`) ist publizierbar. Die mit echten Pfaden/Hosts
> gefuellte **reale Instanz** (`registry.json`) ist LOKAL und wird per `.gitignore`
> ausgeschlossen.

Die Registry ist die **Steuerebene**: sie deklariert pro System, welche Agent-Tools
installiert sind, welche davon synchronisieren sollen und in welcher Beziehung
(Gruppen/Paare), mit welchem Modus und welchem Scope.

## Struktur (`registry.json`)

```jsonc
{
  "host": "<HOST>",                 // dieses System (z.B. LAPTOP / WORKSTATION / MAC)
  "tools": {                         // welche Anbieter sind HIER installiert?
    "<provider-id>": { "installed": true, "role": "hub|member|leaf" }
  },
  "relations": [                     // wie wird gesynct?
    {
      "name": "claude-pair",
      "members": ["claude-code", "claude-desktop"],
      "mode": "pull",               // pull | push | bidirectional
      "source": "claude-code",      // bei pull/push: der Master/Quell-Provider
      "scope": "mcp"                // mcp | skills | both
    }
  ]
}
```

### Felder

| Feld | Bedeutung |
|---|---|
| `host` | Identifier dieses Systems (real in `registry.json`, Platzhalter im Template) |
| `tools.<id>.installed` | ist der Anbieter hier vorhanden? |
| `tools.<id>.role` | `hub` (zentrale Quelle), `member` (nimmt teil), `leaf` (nur Empfaenger) |
| `relations[].mode` | `pull` (Ziele holen vom `source`), `push` (`source` verteilt an Ziele), `bidirectional` (Union, Konflikt → eskalieren) |
| `relations[].source` | der Master-Provider bei `pull`/`push` |
| `relations[].scope` | `mcp` \| `skills` \| `both` |

## Modellierung „braucht jedes System alles?"

- **Nein, Teilmengen sind erlaubt.** `role` und `relations` druecken aus, dass z.B. ein
  Laptop nur eine Teilmenge der MCP-Server fuehrt oder ein bestimmtes Tool nur Empfaenger
  (`leaf`) ist.
- **Multi-System-fähig, aber per Default single-host.** Das Feld `host` erlaubt spaeter
  System-uebergreifende Registries (Laptop/Workstation/Mac); die mitgelieferte reale
  Instanz fuellt nur DIESES System. System-uebergreifender Transport laeuft ueber
  `~/OneDrive/.SYNC/` (siehe `agents-bridge`, Achse 2) — dieser Skill regelt den
  Tool-Abgleich, nicht den Datei-Transport zwischen Rechnern.

## Beispiel-Beziehungen (siehe `registry.example.json`)

1. **claude-pair** (`pull`, scope `mcp`): Claude Code ist Hub, Claude Desktop zieht dessen
   MCP-Stand — exakt der Fall, den der Legacy-Skill `mcp-config-sync` abdeckte.
2. **cli-mcp-fanout** (`push`, scope `mcp`): Claude Code verteilt einen kuratierten
   MCP-Satz an Codex (TOML) und weitere CLIs.
3. **skills-hub** (`push`, scope `skills`): `<HOME>/.claude/skills/` ist die Skill-Quelle,
   andere Tools bekommen Redirect/Bridge (kein hartes Kopieren).
