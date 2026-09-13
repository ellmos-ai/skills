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

## Deterministische Stationen (Claude Code)

Vor einer inhaltlichen Bewertung kann `scripts/segment_stations.py` ein Claude-Code-JSONL
in Stationen zwischen harten Berichtspunkten zerlegen:

```bash
python scripts/segment_stations.py <transkript.jsonl> --output <stationen.json>
```

Harte Grenzen sind `stop_hook_summary`, `compact_boundary`, ein Wechsel zwischen zwei
nichtleeren Session-IDs und das Dateiende. Mit `--gap-seconds <sekunden>` können zusätzlich
Zeitlücken als Grenze dienen. Datensätze ohne Session-ID lösen bewusst keinen Wechsel aus,
weil Claude Code solche Metadatensätze innerhalb einer laufenden Session einstreut.

Die Ausgabe enthält nur Zeilenbereiche, Zeitpunkte, Record-Typen, Session-/Turn-IDs und den
Grenztyp. Chattext, Toolparameter und absolute Quellpfade werden nicht kopiert. Damit ist S1
deterministisch und datensparsam; Aufgabe, Werkzeugkette, Endzustand und Anschlussklassifikation
gehören in die nachgelagerte Stationsbewertung.

## Erntewert einer Stationsfolge (S3)

`scripts/score_stations.py` baut auf der Segmentierung auf und bewertet **Stationsfolgen**:

```bash
python scripts/score_stations.py <transkript.jsonl> [weitere.jsonl ...] \
    [--min-score 5] [--gap-seconds 1800] [--candidates-only] [--output <scored.json>]
```

Ablauf: segmentieren → harte Signale je Station sammeln (Werkzeugnamen, `is_error`,
`tool_use_error`, `isApiError`, Unterbrüche, Mensch-Turns) → Anschlussprompt klassifizieren →
Folgen bilden → Score.

**Folgengrenze:** Richtungsänderung (`RA`) oder ein harter Neustartmarker — Sessionwechsel,
Compact, Zeitlücke. Ein Startprompt wird **nicht** aus dem Wortlaut geraten; er ist von einer
gewöhnlichen Anweisung sprachlich nicht zu trennen. Stattdessen trennt die Zeitlücke: Default
1800 s, `--gap-seconds 0` schaltet sie ab. Der Wert ist eine Kalibrierschraube — ohne ihn fallen
lange Sessions zu wenigen Folgen mit 30+ Stationen zusammen (gemessen: 137 Stationen ergaben
6 Folgen ohne, 17 Folgen mit Zeitlücke).

**Score-Bestandteile** (jeder Beitrag steht als Klartextbegründung in `score_reasons`):

| Beitrag | Bedingung |
| --- | --- |
| +2 je Korrektur (max. +6) | Anschlusstyp `KO` — teuer erworbenes Wissen |
| +3 | Folge endet mit Bestätigung (`BE`) |
| +2 | Werkzeugkette ≥3 Schritte |
| +2 | gleiche Kettensignatur in ≥2 Sessions |
| +1 | Fehlersignal mit folgender Korrektur — belegter Fallstrick |
| −4 | Folge endet mit Richtungsänderung (`RA`) — Sackgasse |

**Ausgabe ist inhaltsfrei** wie bei S1: Labels, Zähler, Werkzeugnamen, Station-/Session-IDs,
Zeitpunkte. Nachrichtentext wird nur zum Klassifizieren gelesen, nie kopiert.

**Die Klassifikation ist ein Vorfilter, kein Klassifikator.** Marker greifen auf Wortgrenzen
(sonst liest „weitere" als Bestätigung „weiter"); alles Uneindeutige bleibt `unknown`. Das Feld
`classified_ratio` weist den tatsächlich klassifizierten Anteil aus; unter 0,5 setzt die Ausgabe
eine Warnung und die Rangfolge gilt als nicht belastbar. Auf realen Transkripten liegt der Anteil
bei etwa 0,5 — die obersten Kandidaten also nachklassifizieren, bevor geerntet wird.

## Datenreduktion vor Bulk-Extraktion

Reihenfolge der Reduktionsstufen (jede Stufe verkleinert um eine Größenordnung):

1. **Vorhandene Kollektoren nutzen:** Existiert bereits ein Prompt-Kollektor/-Listener oder
   ein Studien-Datensatz (nur User-Prompts, bereits extrahiert), damit starten statt roh zu
   parsen.
2. **Stationen + Bewertung:** Erst mit `segment_stations.py` harte Abschnitte bilden, mit
   `score_stations.py --candidates-only` auf die lohnenden Folgen eindampfen, dann
   nur User-Turns + Tool-Call-Namen extrahieren (Script, kein LLM).
3. **Subagenten-Map:** Pro Session-Bündel ein Subagent, der Kandidaten-Destillate liefert
   (Auslöser, Ablauf, Begründung, Fallstricke, Beleg) — Rohtext bleibt beim Subagenten.
4. **Reduce:** Destillate clustern und mergen; Häufigkeit über Sessions zählen.

Faustgröße pro Map-Subagent: so viele Sessions, wie nach Stufe 2 bequem in einen Kontext
passen (grob <50k Tokens Reduktat).
