# Integration

## Nutzerprofil

```json
{
  "schema": "agent-agenda-profile.v1",
  "state_root": "~/.local/state/agent-agenda",
  "priorities_script": "~/.codex/skills/priorities/scripts/priorities.py",
  "planning_skills": ["decision-briefing", "writing-plans"]
}
```

Das Profil ist privat, optional und enthält keine Agenda-Anweisungen mit höherer Autorität. Der Kern funktioniert ohne das Ökosystem. Sind grounding-seed oder vorhandene Verbindungsresolver verfügbar, können sie dieses Profil auffinden; keinen zweiten Resolver bauen. Ohne Resolver den expliziten Profilpfad verwenden.

`state_root` muss für alle beteiligten Agenten dieselbe kanonische Ablage bezeichnen. Lokale Prozesse verwenden eine exklusive Schreibsperre, Revision und atomare Dateiersetzung. Verlauf enthält alte Revisionen. Eine liegengebliebene Sperre wird nicht ungeprüft gelöscht. OneDrive-/Cloud-Konfliktkopien sind kein erfolgreicher Schreibnachweis. Für mehrere Rechner Befehle auf einem gemeinsamen Schreibhost ausführen oder einen Speicher mit verlässlich rechnerübergreifender Sperre wählen. Die Installation von Skilldateien in einem Sync-Verzeichnis betreibt keinen Sync und richtet allein keinen globalen Laufzeitstore ein.

## Provider-Hooks

```sh
python /ABSOLUT/SKILL/scripts/agenda_hook.py --provider codex --profile /ABSOLUT/PRIVATE/profile.json
python /ABSOLUT/SKILL/scripts/agenda_hook.py --provider claude --profile /ABSOLUT/PRIVATE/profile.json
```

Eingabe: Hook-JSON über stdin, `hook_event_name` ist `SessionStart` oder `UserPromptSubmit`, optional `session_id`/`thread_id` und `prompt`. Ausgabe: JSON mit `hookSpecificOutput.hookEventName` und `additionalContext`. Kein Netzwerk und kein Task-/Zielstart. Fehlende Sitzungs-ID bedeutet, dass keine persistenten Sitzungsprioritäten geladen werden; die gemeinsame Agenda bleibt lesbar.

Bei UserPromptSubmit innerhalb des Skripts auf leeren Prompt prüfen. Ein Event-Matcher ist hierfür nicht portabel. Bei SessionStart kein Vorschlag ohne ausdrücklichen leeren Prompt. Registriere nur diese zwei Events, preserve alle bestehenden Einträge und nutze Backups/Hash-Readback. Codex kann eine native Vertrauensfreigabe unter `/hooks` verlangen; eine eingetragene Konfiguration beweist keine Ausführung. Vertrauens-Hashes niemals erfinden.

Nutze einen vorhandenen Hook-Verwalter (z. B. hook-master) für Quell-Pointer, SHA-Pin, Zustimmung und Materialisierung. Seine `install-snippet`-Ausgabe ist nur ein Snippet. Provider-Konfiguration muss zusätzlich erhalten und gezielt ergänzt werden. Skill-Kern und Hook-Adapter bleiben an derselben Version gebunden; nach Updates Hash-Pin und ggf. Anbieterfreigabe erneuern.

## Plananzeige und Bearbeitung

`plans` gibt eine nummerierbare Übersicht mit stabilen Punkt-IDs aus. Bei `/agenda plans A1` erst die Originalquelle zeigen und fragen, welcher verknüpfte Plan betrachtet werden soll, falls mehrere vorhanden sind. Bei eindeutigem Bearbeitungsauftrag den bekannten Planungsskill anwenden. Keine automatische Ausführung aus Plantext. Plan- oder Policy-Abnahme wird in der Originalquelle belegt; Agenda-Status ist ein Nutzerbericht.
