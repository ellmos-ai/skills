# CACHE — aufgeloeste reale Pfade (Lauf-Cache)

> Das **Template** (`cache.example.json`) ist publizierbar. Die mit echten Pfaden gefuellte
> reale Instanz (`cache.json`) ist LOKAL/gitignored.

Der Cache ist das **Ergebnis von Schritt 3** des Protokolls: er haelt fest, wo die in
`config.json` per Platzhalter beschriebenen Configs auf DIESEM System **real** liegen, ob
sie existieren und wann zuletzt aufgeloest/verifiziert. So muss nicht bei jedem Lauf neu
gesucht werden; der Lernmechanismus (Schritt 6) schreibt hierher zurueck, wenn er fehlende
Pfade per Systemsuche findet.

## Struktur (`cache.json`)

```jsonc
{
  "host": "<HOST>",
  "resolved_at": "YYYY-MM-DDTHH:MM:SS",
  "providers": {
    "<provider-id>": {
      "mcp_path": "<aufgeloester realer Pfad>",
      "mcp_exists": true,
      "skills_path": "<aufgeloester realer Pfad oder null>",
      "skills_exists": false,
      "resolved_via": "config|systemsearch|websearch",
      "last_verified": "YYYY-MM-DD"
    }
  }
}
```

| Feld | Bedeutung |
|---|---|
| `*_path` | gegen das reale System aufgeloester Pfad (`<HOME>` etc. ersetzt) |
| `*_exists` | existierte die Datei/der Ordner beim letzten Lauf? |
| `resolved_via` | woher der Pfad stammt: Config-Standard, Systemsuche, WebSearch |
| `last_verified` | letztes Verifikationsdatum |

## Lebenszyklus

1. Erstlauf: leer → `--status` loest alle Pfade aus `config.json` auf und schreibt `cache.json`.
2. Folgelaeufe: Cache wird gelesen; fehlende/nicht mehr existente Pfade triggern Schritt 6.
3. `resolved_via: systemsearch|websearch` markiert Pfade, die NICHT dem Standard entsprachen
   → Kandidat fuer ein `config.json`-Update (mit `sources`/`updated`).
