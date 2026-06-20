# BACH-Versionierung: Skills, Workflows, Agenten und Prompts

Stand: 2026-06-18

## Kurzfazit

| Bereich | Hat BACH Versionierung? | Einschätzung |
|---|---|---|
| Skills | Ja | Explizite SemVer im YAML-Header, DB-Sync mit `version`, Versionscheck lokal vs. zentral über `bach skills version <name>`. |
| Workflows | Teilweise ja | Workflows sind als `type: workflow` in der Skills-Struktur versionierbar und über `bach skills version <workflow-name>` prüfbar. Zusätzlich gibt es Workflow-TÜV/Lifecycle, aber keine eigene Inhalts-Historie. |
| Agenten | Teilweise | Agenten/Experten müssen `version` im `SKILL.md`-Frontmatter haben; Templates nennen einen Agenten-Versionscheck. Praktisch wirkt Agenten-Versionierung eher wie Metadaten/Registry-Sync, nicht wie eine eigene Änderungshistorie. |
| Prompts | Ja, am stärksten | Das Prompt-System hat eigene Tabellen `prompt_templates` und `prompt_versions`; `bach prompt update` speichert alte Texte automatisch als Version. In dieser Instanz sind aktuell aber keine Prompt-Templates angelegt. |

## Vorgehen

Ich habe mit dem BACH-Start-Skill gearbeitet und BACH per CLI gestartet:

```powershell
python bach.py skills version bach
python bach.py --startup --partner=Codex --mode=silent
```

Danach habe ich die relevanten Hilfedateien und Handler über BACH gelesen bzw. gesucht:

```powershell
python bach.py help search
python bach.py help skills
python bach.py help workflow
python bach.py help agents
python bach.py help prompt
python bach.py help tuev
python bach.py search "skills version" --limit 15
python bach.py search "workflow version" --limit 15
python bach.py search "agent version" --limit 15
python bach.py search "prompt version" --limit 15
python bach.py skills hierarchy workflow
python bach.py skills show skill-md-aenderung
python bach.py skills version skill-md-aenderung
python bach.py prompt list
python bach.py agent list
python bach.py tuev status
```

Auffälligkeit: `bach skills version bach` löste in der BACH-Registry auf `system/skills/workflows/system/claude-bach-vernetzung.md` v1.0.0 auf, während der geladene Codex-BACH-Skill selbst v3.8.0 ist. Das sieht nach Namens-/Registry-Kollision aus, nicht nach einem Beleg gegen die Versionierungslogik.

## Skill-Versionierung

BACH hat eine klare Skill-Versionierung.

Belege:

- `docs/help/skills.txt` beschreibt das Versionscheck-Prinzip: immer die neueste Version verwenden, lokal oder zentral; Befehl `bach --skills version <name>`.
- Der Standard-Header verlangt `version: X.Y.Z` und erlaubt Typen wie `skill`, `agent`, `expert`, `service`, `connector`, `partner`, `os`, `workflow`.
- Die Skills-Tabelle synchronisiert `name`, `type`, `path`, `content_hash`, `is_active`, `version`.
- `hub/skills.py` implementiert `version` als Operation, liest YAML-Frontmatter, vergleicht lokale und zentrale Versionen aus `data/skill_sources.json` und meldet, ob lokal/zentral neuer ist.

Konkretes Beispiel:

```text
python bach.py skills version skill-md-aenderung

LOKAL:   v1.0.1
ZENTRAL: (nicht registriert)
[OK] Version aktuell: v1.0.1
```

Bewertung: Ja. Das ist die sauberste allgemeine Komponenten-Versionierung in BACH.

## Workflow-Versionierung

BACH hat Workflow-Versionierung, aber sie läuft überwiegend über das Skills-System.

Belege:

- `docs/help/workflow.txt` sagt: Workflows liegen in `skills/workflows/` und werden in der `skills`-Tabelle als `type='workflow'` automatisch synchronisiert.
- `skills/_templates/TEMPLATE_WORKFLOW.md` enthält `version: 1.0.0`, `type: workflow` und einen Versionshinweis.
- `python bach.py skills hierarchy workflow` listete 31 Workflow-Items.
- `skills/workflows/skill-md-aenderung.md` ist selbst ein versionierter Workflow mit `version: 1.0.1`.
- Dieser Workflow beschreibt SemVer-Regeln: Patch, Minor, Major; danach `version:` hochzählen und `updated:` setzen.

Zusätzlich gibt es `bach tuev`:

- `docs/help/tuev.txt` beschreibt Workflow-Qualitätssicherung, Gültigkeit, Usecases, Scores und `bach tuev renew`.
- `python bach.py tuev status` zeigte 29 Workflows im OK-Zustand.

Wichtig: TÜV ist Lifecycle-/Qualitäts-Tracking, keine Inhaltsversionierung. Eine echte Historie alter Workflow-Texte wie bei Prompts habe ich nicht gefunden.

Bewertung: Teilweise ja. Workflows sind versionierte Komponenten im Skills-System; zusätzlich gibt es TÜV. Für vollständige Workflow-Historie bräuchte BACH aber eine eigene `workflow_versions`-Tabelle oder Nutzung des allgemeinen Distribution-/Upgrade-Systems.

## Agenten-Versionierung

BACH hat Agenten-Versionen als Metadaten, aber keine klar belegte eigene Agenten-Historie.

Belege:

- `docs/help/agents.txt` sagt, jeder Agent und Experte muss eine `SKILL.md` haben; das Frontmatter muss mindestens `name`, `version`, `type`, `description` enthalten.
- `skills/_templates/TEMPLATE_AGENT.md` enthält `version: 1.0.0`, `type: agent` und den Hinweis `bach agents version [agent-name]`.
- `hub/agents.py` liest bei Experten ein `Version:`-Feld und schreibt es in `bach_experts.version`.
- `docs/help/agents.txt` beschreibt Agenten primär als Kombination aus Persona, Skill und Session; Skills sind portierbar/exportierbar, Personas/Agents dagegen BACH-spezifisch.

Praktischer Befund:

- `python bach.py agent list` zeigt Agenten und Experten, aber keine Versionen.
- `python bach.py agent info ati` fiel in dieser CLI-Nutzung auf die Agentenliste zurück.
- In den Help-/Handler-Funden habe ich keinen Agenten-spezifischen Versionshistorienmechanismus analog zu `prompt_versions` gefunden.

Bewertung: Teilweise. Agenten sind versionierbar im Sinne von `SKILL.md`-/Registry-Metadaten. Eine robuste Agenten-Versionierung mit History, Diff oder Rollback ist nicht erkennbar.

## Prompt-Versionierung

BACH hat eine eigene Prompt-Versionierung.

Belege:

- `docs/help/prompt.txt` nennt als Ressourcen `hub/prompt.py`, `prompt_templates`, `prompt_boards`, `prompt_versions`.
- Die Doku sagt ausdrücklich: Jede Änderung erzeugt eine neue Version.
- `bach prompt get <id>` zeigt die Versionshistorie.
- `hub/prompt.py` liest `prompt_versions` bei `get`.
- Bei `update` bestimmt `hub/prompt.py` die nächste `version_number`, speichert den alten Text in `prompt_versions` und aktualisiert danach `prompt_templates`.

Beispielablauf:

```powershell
python bach.py prompt add "Zusammenfassung" "Fasse den folgenden Text zusammen:" --category schreiben
python bach.py prompt update "Zusammenfassung" "Fasse den folgenden Text prägnant zusammen:"
python bach.py prompt get "Zusammenfassung"
```

Praktischer Befund:

```text
python bach.py prompt list
Keine Prompt-Templates gefunden.
```

Bewertung: Ja, konzeptionell und technisch. Aktuell ist die Tabelle in dieser Instanz offenbar leer, aber der Handler ist vorhanden.

## Gesamtantwort

Ja, BACH hat Versionierung, aber nicht überall auf derselben Reifestufe:

1. Skills: voll vorhanden.
2. Workflows: vorhanden als versionierte `type: workflow`-Komponenten plus TÜV-Lifecycle; keine eigene Text-Historie.
3. Agenten: Version als Pflicht-Metadatum vorhanden; eigene History/Version-CLI nicht belastbar belegt.
4. Prompts: eigene echte Versionshistorie vorhanden; aktuell nur ohne angelegte Templates.

Wenn BACH konsistenter werden soll, wäre die naheliegende Vereinheitlichung:

```text
component_versions
  id
  component_type      skill | workflow | agent | expert | prompt
  component_name
  version
  content_hash
  content_snapshot
  created_at
  created_by
  source_path
```

Dann könnten Skills, Workflows und Agenten dieselbe Historienlogik bekommen, die Prompts bereits besitzen.

## Quellen im BACH-Baum

- `system/docs/help/skills.txt`
- `system/docs/help/workflow.txt`
- `system/docs/help/agents.txt`
- `system/docs/help/prompt.txt`
- `system/docs/help/tuev.txt`
- `system/skills/_templates/TEMPLATE_AGENT.md`
- `system/skills/_templates/TEMPLATE_WORKFLOW.md`
- `system/skills/workflows/skill-md-aenderung.md`
- `system/hub/skills.py`
- `system/hub/agents.py`
- `system/hub/prompt.py`
