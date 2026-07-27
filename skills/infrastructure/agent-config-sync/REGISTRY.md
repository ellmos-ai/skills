# REGISTRY — User-Auswahl statt Anbieter-Default

`registry.example.json` ist neutral und enthält keine aktive Relation. Die
lokale `registry.json` dokumentiert eine konkrete User-Entscheidung.

## Endpoint-Auswahl

Eine Relation kann `members` explizit nennen oder einen Selektor verwenden:

```json
"selection": {
  "providers": ["anthropic", "openai"],
  "app_classes": ["cli"],
  "members": []
}
```

`"*"` wählt alle katalogisierten Werte der Achse. Vor Apply werden nur lokal
erkannte und vom User bestätigte Mitglieder in die aktive Registry übernommen.

## Truth

Für MCP/Skills kann `source` einen Endpoint bezeichnen. Für Regeln sind auch
eine oder mehrere Dateien zulässig:

```json
"truth": {
  "sources": [
    "<HOME>/AGENTS.md",
    "<PROJECT>/AGENTS.md"
  ],
  "strategy": "ordered-overlay"
}
```

Zulässige Strategien müssen vom User gewählt werden:

- `copy`: eine Quelle unverändert kopieren,
- `redirect`: Ziel verweist auf die Truth,
- `ordered-overlay`: mehrere Quellen in festgelegter Reihenfolge,
- `generated-loader`: kleine Bootstrap-Datei lädt mehrere Quellen.

Leere `source`/`truth.sources` bedeuten keine Autorisierung. Plan und Apply
bleiben dann blockiert.
