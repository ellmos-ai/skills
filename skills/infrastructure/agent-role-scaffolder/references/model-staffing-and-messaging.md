# Modellstaffelung + Team-/Messaging-Konventionen

Beide Bauwege (nativer Subagent, Companion-Worker) teilen dieselben zwei
Anschlussstellen an den restlichen Bestand. Diese Datei dupliziert die
dortigen Inhalte nicht, sondern bündelt nur den Verweis + die Faustregeln,
die beim Scaffolden am häufigsten übersehen werden.

## Modellstaffelung — an `model-strategy` delegieren

**Nicht selbst entscheiden.** Der Skill `model-strategy` (dev/model-strategy)
liefert score-basierte Modellauswahl, Cross-Agent-Delegation (Gemini, Codex,
Ollama), Advisor-Pairing, Eskalationstrigger und eine Berechtigungsmatrix.
Zugrundeliegendes Routing-Werkzeug: `clutch`
(`.MODULES/.ORCHESTRATION/clutch`, providerneutrale Orchestrierungs-Engine
mit Auto-Learning, Provider Anthropic/Gemini/OpenAI/Ollama/Kimi).

**Belegte Faustregel** (Memory-Fact `feedback-subagenten-modellstaffelung`,
User-bestätigt 2026-08-19): Subagenten erben **nicht pauschal** das
Hauptmodell des Orchestrators — `clutch`/`model-strategy` befragen und das
Feld MODELL-ROUTING (im Ticket-Template) ehrlich ausfüllen, nicht als Formalie
leer lassen.

## Team-/Messaging-Konventionen

- **`SendMessage`** ist der einzige Weg, mit einem anderen Agenten zu
  kommunizieren — reiner Text-Output ist für andere Agenten unsichtbar.
  Antworten kommen automatisch an; kein Postfach-Polling nötig.
- **Ticket-Claim per Dateiname:** `T-YYYYMMDD-NNNNNNNNN.txt` = unclaimed,
  `T-YYYYMMDD-NNNNNNNNN.<HOST>.txt` = geclaimt. Rename ist auf NTFS/OneDrive
  atomar; bei Konfliktkopie hat ein System gewonnen (siehe
  `_control-center/_TICKETS/README.md`).
- **„Verweisen statt wiederholen"** (`~/CLAUDE.md`, gleichnamiger Abschnitt):
  Ein Auftrag an einen Subagenten/Companion-Worker erzählt zentrale Regeln
  NICHT nach (die erbt er ohnehin aus `CLAUDE.md`/Kontext) — er trägt nur,
  was der Worker sonst nicht wissen kann: gemessene Ausgangswerte,
  Kausalketten dieses Systems, Scope-Grenzen, Abbruchbedingungen, und vor
  allem die **Begründung** hinter einer Festlegung (nicht nur das Ergebnis —
  ein Worker, der die Begründung kennt, kann sie im Zweifel korrekt
  anwenden statt sie blind zu befolgen).
- **Kompakte Rückmeldung:** Bei Ticket-Serien meldet ein Companion-Worker
  knapp zurück (Hash/ID + 1 Zeile), damit der Orchestrator-Kontext nicht
  durch Statusberichte wächst, die er selbst nachschlagen kann.
- **Nachtrag-Konvention:** Trifft neue Information nach `SOLVED` ein, wird sie
  als datierter `NACHTRAG`-Block im `VERLAUF` angehängt statt den Status
  zurückzunehmen — belegt in mehreren Fällen dieser Sitzung selbst.
