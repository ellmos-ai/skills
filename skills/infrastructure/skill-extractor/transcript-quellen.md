# Transcript-Quellen — wo Chatverläufe liegen und wie man sie liest

Fundorte und Parsing-Hinweise für die gängigen Agenten-Harnesses. Pfade sind Defaults —
bei abweichender Installation zuerst mit einer Dateisuche verifizieren.

## Fundorte

| Agent | Ort (Default) | Format |
| --- | --- | --- |
| Claude Code | `~/.claude/projects/<projekt-slug>/*.jsonl` | JSONL, ein Event pro Zeile |
| Codex CLI/Desktop | `~/.codex/sessions/` bzw. App-Datenverzeichnis | JSONL/SQLite je nach Version |
| Kimi Code | `~/.kimi-code/session_index.jsonl` → `<sessionDir>/agents/main/wire.jsonl` | JSONL |
| Gemini/Antigravity | `~/.gemini/` (Brain-/Session-Verzeichnisse) | versionsabhängig |
| Generischer Export | vom User bereitgestellte `.md`/`.txt`/`.json`-Exporte | frei |

Der `<projekt-slug>` bei Claude Code ist der Arbeitsverzeichnis-Pfad mit `-` statt
Trennzeichen (z. B. `C--Users-name-projekt`).

## Parsing-Hinweise (JSONL)

- **Nie ganze Dateien in den Kontext laden** — Transkripte erreichen leicht sechsstellige
  Token-Zahlen. Gezielt filtern (grep/jq/Python), dann nur Treffer lesen.
- **User-Turns tragen das meiste Signal** für die Extraktion: Aufträge, Korrekturen,
  Richtungswechsel. Bei Claude Code: Zeilen mit `"type":"user"`; echte Mensch-Eingaben von
  Tool-Results unterscheiden (Tool-Results haben `tool_use_id`/`toolUseResult`-Felder).
  Bei Kimi: `type=="turn.prompt"` und `origin.kind=="user"`.
- **Korrekturschleifen finden:** User-Turns, die kurz nach einem Assistant-Turn folgen und
  Negationen/Imperative enthalten („nein", „nicht so", „stattdessen", „falsch", „immer",
  „nie", „merk dir") — das sind die wertvollsten Stellen.
- **Werkzeugketten rekonstruieren:** Abfolge der Tool-Calls des Assistant extrahieren
  (Tool-Name + Kurzparameter reichen), um funktionierende Abläufe nachzuzeichnen.
- **Zeitliche Ordnung wahren:** Sessions chronologisch verarbeiten; spätere Sessions
  enthalten oft die korrigierte Endfassung eines Ablaufs aus früheren.

## Datenreduktion vor Bulk-Extraktion

Reihenfolge der Reduktionsstufen (jede Stufe verkleinert um eine Größenordnung):

1. **Vorhandene Kollektoren nutzen:** Existiert bereits ein Prompt-Kollektor/-Listener oder
   ein Studien-Datensatz (nur User-Prompts, bereits extrahiert), damit starten statt roh zu
   parsen.
2. **Feld-Filter:** Nur User-Turns + Tool-Call-Namen extrahieren (Script, kein LLM).
3. **Subagenten-Map:** Pro Session-Bündel ein Subagent, der Kandidaten-Destillate liefert
   (Auslöser, Ablauf, Begründung, Fallstricke, Beleg) — Rohtext bleibt beim Subagenten.
4. **Reduce:** Destillate clustern und mergen; Häufigkeit über Sessions zählen.

Faustgröße pro Map-Subagent: so viele Sessions, wie nach Stufe 2 bequem in einen Kontext
passen (grob <50k Tokens Reduktat).
