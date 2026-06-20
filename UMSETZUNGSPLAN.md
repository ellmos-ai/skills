# Umsetzungsplan: `.SKILLS` versionieren und standardisieren

Stand: 2026-06-19

Ziel dieses Plans ist eine nicht-destruktive Umsetzung der Versionierungsstrategie für `.SKILLS`, Prompts, Workflows und Agenten. Nicht-destruktiv heißt hier: bestehende Skills werden zuerst nur gelesen, klassifiziert, gespiegelt und geprüft. Keine Datei wird verschoben, überschrieben, gelöscht oder automatisch deployed, bevor die Registry, Fork-Logik, Privacy-Gates und Dry-Runs stabil sind.

## Leitprinzipien

- Lesen vor Schreiben.
- Schattenmodus vor Produktivmodus.
- Dry-Run vor echter Änderung.
- Additive Dateien vor Umbau bestehender Dateien.
- Keine Auto-Korrektur an Skill-Inhalten in den ersten Etappen.
- Keine Mass Moves, keine Mass Renames, keine Deletes.
- Persönliche Forks werden nie automatisch in neutrale Skills zurückgeschrieben.
- Fremdskills behalten Herkunft, Lizenz, Upstream-Pfad und lokale Abweichungen.
- Deployment-Ziele wie `~/.claude/skills`, BACH oder PromptBoard werden erst nach Drift-Bericht berührt.
- ProSync- und ProFiler-Logik wird modular genutzt, aber der neue Kern bleibt ohne unnötige PDF-, OCR- oder GUI-Abhängigkeiten.

## Nicht-Ziele der ersten Umsetzung

- Keine Reorganisation des bestehenden `skills/`-Baums.
- Keine automatische SemVer-Erhöhung.
- Keine automatischen Git-Tags.
- Kein BACH-Import in Produktivdaten.
- Kein Deployment nach `~/.claude/skills` ohne Dry-Run.
- Kein Rückschreiben von persönlichen Lukas-Anpassungen in nutzerneutrale Skills.
- Kein direkter Import fremder Skills ohne Herkunfts- und Lizenzklassifikation.
- Keine Löschung alter Versionen, auch wenn sie redundant wirken.

## Etappe 0: Freeze und Sicherheitsrahmen

Zweck: Ausgangslage stabilisieren, ohne Inhalte zu ändern.

Aktionen:

- Bestehende Konzeptdateien als aktuelle Planungsgrundlage markieren:
  - `BACH-VERSIONIERUNG-BEISPIEL.md`
  - `WEITERE-VERSIONIERUNGS-RESSOURCEN.md`
  - `STANDARDISIERUNGS-VERSIONIERUNGS-KONZEPT.md`
- Vor jeder späteren Änderung in `.SKILLS` auf `LOCK*.txt` prüfen.
- Keine bestehenden Skill-Dateien anfassen.
- Entscheidung festhalten: `.SKILLS` bleibt Quelle der Wahrheit; Deployments sind abgeleitet.

Artefakt:

- Dieser Umsetzungsplan.

Abschlusskriterium:

- Plan liegt vor, ohne bestehende Dateien umzubauen.

## Etappe 1: Read-only Inventur

Zweck: Den aktuellen Bestand verstehen, ohne Registry oder Skills zu verändern.

Aktionen:

- Alle `skills/**/SKILL.md` lesen.
- Frontmatter extrahieren.
- Vorhandene Felder erfassen: `name`, `version`, `type`, `standalone`, `anthropic_compatible`, `bach_compatible`, `bach_origin`, `provenance`, `status`, `language`.
- Datei-Hash je `SKILL.md` berechnen.
- Dateibaum erfassen: `scripts/`, `references/`, `assets/`, `tests/`.
- Auffälligkeiten nur berichten, nicht reparieren.

Artefakt:

```text
.SKILLS/_reports/inventory-readonly-YYYYMMDD.json
.SKILLS/_reports/inventory-readonly-YYYYMMDD.md
```

Nicht-destruktive Garantie:

- Es wird nur unter `_reports/` geschrieben.
- Keine Skill-Datei wird verändert.

Abschlusskriterium:

- Bestand ist maschinenlesbar erfasst.
- Fehlende oder uneinheitliche Frontmatter-Felder sind sichtbar.

## Etappe 2: Herkunft und Neutralität klassifizieren

Zweck: Eigene/Fremdskills und neutrale/persönliche Varianten unterscheiden.

Klassen:

- `own-neutral`
- `own-personal-fork`
- `foreign-neutral`
- `foreign-local-fork`
- `foreign-personal-fork`

Aktionen:

- Bestehende `provenance`-Felder auswerten.
- Hinweise auf Fremdherkunft sammeln: externe Repo-URLs, Anthropic-Beispiele, Community-Hinweise, Plugin-Pfade.
- Hinweise auf Personalisierung sammeln: lokale Pfade, Lukas-spezifische Angaben, private Zielsysteme, lokale Agenten- oder Maschinenbezüge.
- Nur Vorschläge erzeugen, keine Klassifikation direkt ins Frontmatter schreiben.

Artefakt:

```text
.SKILLS/_reports/ownership-classification-proposed-YYYYMMDD.csv
.SKILLS/_reports/ownership-classification-proposed-YYYYMMDD.md
```

Nicht-destruktive Garantie:

- Klassifikation ist zunächst ein Vorschlag.
- Persönliche Forks werden nicht aus neutralen Skills erzeugt und nicht zurückgemergt.

Abschlusskriterium:

- Jede bestehende Komponente hat mindestens eine vorgeschlagene Klasse oder einen `needs-review`-Status.

## Etappe 3: Registry-Schema im Entwurf

Zweck: Schema entwerfen, ohne produktive Registry zu aktivieren.

Aktionen:

- JSON-Schemas als Entwurf anlegen:
  - `schemas/component-v1.schema.json`
  - `schemas/skill-v1.schema.json`
  - `schemas/prompt-v1.schema.json`
  - `schemas/workflow-v1.schema.json`
  - `schemas/agent-v1.schema.json`
- Schema-Felder aus dem Konzept übernehmen:
  - Identität
  - Version
  - Provenance
  - Ownership
  - Branch
  - Fork
  - Privacy
  - Compatibility
  - Hash

Artefakt:

```text
.SKILLS/schemas/*.schema.json
```

Nicht-destruktive Garantie:

- Neue Dateien sind additiv.
- Keine vorhandene Registry wird ersetzt.

Abschlusskriterium:

- Schema kann ein Beispiel aus Etappe 1 validieren.

## Etappe 4: Schatten-Registry erzeugen

Zweck: Registry testen, ohne sie als Quelle der Wahrheit zu deklarieren.

Aktionen:

- Aus Inventur und Klassifikationsvorschlag eine Schatten-Registry erzeugen.
- Komponenten nur spiegeln, nicht korrigieren.
- Konflikte markieren:
  - gleicher `name`, verschiedene Pfade
  - gleiche Datei, fehlende Version
  - Fremdherkunft unklar
  - Personalisierung unklar
  - `standalone: true`, aber BACH-Abhängigkeit erkennbar

Artefakt:

```text
.SKILLS/registry/_draft/components.proposed.json
.SKILLS/registry/_draft/forks.proposed.json
.SKILLS/registry/_draft/branches.proposed.json
.SKILLS/registry/_draft/deployments.proposed.json
.SKILLS/registry/_draft/releases.proposed.json
```

Nicht-destruktive Garantie:

- Nur `_draft/` wird geschrieben.
- Produktive Registry-Dateien bleiben unangetastet oder existieren noch nicht.

Abschlusskriterium:

- Schatten-Registry kann vollständig neu erzeugt werden.
- Manuelles Löschen von `_draft/` würde keine Skill-Daten verlieren.

## Etappe 5: `versionctl` read-only Prototyp ✅ IMPLEMENTIERT 2026-06-20

Zweck: Tooling starten, aber nur lesend.

Kommandos:

```text
versionctl scan --dry-run
versionctl status --dry-run
versionctl classify --dry-run
versionctl validate --dry-run
```

Aktionen:

- Ein schlankes CLI anlegen, bevorzugt in einem neuen Toolbereich, nicht mitten in bestehenden Skills.
- Nur lesen und Reports schreiben.
- Keine `bump`, `release`, `deploy` oder `export`-Schreiboperationen.

Artefakt:

```text
.SKILLS/tools/versionctl/
.SKILLS/_reports/versionctl-status-YYYYMMDD.md
```

Nicht-destruktive Garantie:

- Alle Kommandos sind standardmäßig Dry-Run.
- Jeder Schreibpfad liegt unter `_reports/` oder `registry/_draft/`.

Abschlusskriterium:

- `versionctl scan --dry-run` reproduziert die Inventur aus Etappe 1.

## Etappe 6: Templates additiv einführen ✅ IMPLEMENTIERT 2026-06-20

Zweck: Neue Komponentenarten ermöglichen, ohne bestehende Skills umzubauen.

Aktionen:

- Templates anlegen:
  - `templates/PROMPT.md`
  - `templates/WORKFLOW.md`
  - `templates/AGENT.md`
  - `templates/SKILL.md` als erweiterte `.SKILLS`-Variante
- Keine bestehenden Komponenten automatisch auf die Templates migrieren.

Artefakt:

```text
.SKILLS/templates/PROMPT.md
.SKILLS/templates/WORKFLOW.md
.SKILLS/templates/AGENT.md
.SKILLS/templates/SKILL.md
```

Nicht-destruktive Garantie:

- Nur neue Template-Dateien.
- Keine Änderung an `skills/**/SKILL.md`.

Abschlusskriterium:

- Neue Komponenten können nach Template erstellt werden.
- Bestehende Komponenten bleiben unverändert.

## Etappe 7: Fork-Modell im Schattenmodus

Zweck: Forks sichtbar machen, ohne Forks automatisch zu erzeugen.

Aktionen:

- `.sync-hold` als Deployment-Fork-Kandidat auswerten.
- Persönliche Fork-Kandidaten erkennen, aber nicht verschieben.
- Fremdskill-Forks erkennen, aber nicht umbenennen.
- Rückfluss-Kandidaten markieren:
  - Änderung aus personalisiertem Fork könnte neutralisiert werden.
  - Änderung enthält persönliche Details und bleibt privat.

Artefakt:

```text
.SKILLS/registry/_draft/forks.proposed.json
.SKILLS/_reports/fork-review-YYYYMMDD.md
```

Nicht-destruktive Garantie:

- Keine Fork-Dateien werden automatisch kopiert.
- Kein persönlicher Fork wird in einen neutralen Skill gemergt.

Abschlusskriterium:

- Fork-Beziehungen sind als Vorschlag sichtbar.

## Etappe 8: Produktive Registry minimal aktivieren ✅ IMPLEMENTIERT 2026-06-20

Zweck: Von Entwurf zu minimaler Quelle wechseln, aber weiterhin ohne Inhaltsänderung.

Aktionen:

- Nach Review die leeren/minimalen produktiven Registry-Dateien anlegen:
  - `registry/components.json`
  - `registry/forks.json`
  - `registry/branches.json`
  - `registry/releases.json`
  - `registry/deployments.json`
- Nur bestätigte Datensätze aus `_draft/` übernehmen.
- Jede Übernahme in einem Report festhalten.

Artefakt:

```text
.SKILLS/registry/components.json
.SKILLS/registry/forks.json
.SKILLS/registry/branches.json
.SKILLS/registry/releases.json
.SKILLS/registry/deployments.json
```

Nicht-destruktive Garantie:

- Registry wird additiv angelegt.
- Bestehende Skill-Inhalte bleiben unverändert.

Abschlusskriterium:

- Registry kann gegen Dateisystem geprüft werden.
- Abweichungen werden berichtet, nicht repariert.

## Etappe 9: `versionctl status` und Drift-Berichte

Zweck: Änderungen erkennen, ohne sie zu korrigieren.

Kommandos:

```text
versionctl status
versionctl diff <component>
versionctl validate
```

Aktionen:

- Registry-Hash gegen Dateisystem vergleichen.
- Fehlende Registry-Einträge melden.
- Geänderte Skill-Dateien melden.
- Unklare Herkunft und Neutralität melden.
- Changelog-/SemVer-Hinweise geben.

Artefakt:

```text
.SKILLS/_reports/drift-YYYYMMDD.md
```

Nicht-destruktive Garantie:

- Keine Auto-Fixes.
- Keine Versionserhöhung.
- Keine Dateiüberschreibung.

Abschlusskriterium:

- Drift ist transparent.
- Der Bericht kann manuell reviewed werden.

## Etappe 10: Schreiboperationen nur an Testkomponenten

Zweck: Schreiblogik testen, ohne echte Skills zu riskieren.

Aktionen:

- Einen klar markierten Testbereich nutzen:

```text
.SKILLS/_sandbox/versionctl-test/
```

- Dort Testkomponenten anlegen.
- `versionctl bump`, `versionctl fork create` und `versionctl release --dry-run` nur gegen Sandbox-Komponenten testen.

Nicht-destruktive Garantie:

- Kein echter Skill wird verändert.
- Sandbox ist klar getrennt und kann später archiviert werden.

Abschlusskriterium:

- Schreiboperationen funktionieren nur im erlaubten Testbereich.

## Etappe 11: Deployment-Dry-Runs

Zweck: Deployment-Verhalten prüfen, ohne Ziele zu überschreiben.

Kommandos:

```text
versionctl deploy claude --dry-run
versionctl deploy bach --dry-run
versionctl deploy promptboard --dry-run
```

Aktionen:

- Zielzustand lesen.
- Geplante Kopien auflisten.
- Konflikte und `.sync-hold` markieren.
- Persönliche Forks besonders schützen.
- Keine Datei ins Ziel kopieren.

Artefakt:

```text
.SKILLS/_reports/deploy-dry-run-claude-YYYYMMDD.md
.SKILLS/_reports/deploy-dry-run-bach-YYYYMMDD.md
.SKILLS/_reports/deploy-dry-run-promptboard-YYYYMMDD.md
```

Nicht-destruktive Garantie:

- Kein Ziel wird geschrieben.
- Kein Deployment löscht Dateien.

Abschlusskriterium:

- Deployment-Plan ist nachvollziehbar und blockiert persönliche/fremde Konflikte.

## Etappe 12: ProSync-Integration als Bibliothek

Zweck: Deployment-Mechanik robuster machen, ohne ProSync monolithisch einzubauen.

Aktionen:

- Nur neutrale Sync-/Report-Bausteine identifizieren.
- Keine GUI- oder Tray-Abhängigkeit in `versionctl`.
- Keine echten Syncs in der ersten Integration.
- Reportformat definieren: Quelle, Ziel, Modus, geplante Aktion, Blocker, Ergebnis.

Nicht-destruktive Garantie:

- ProSync wird zunächst nur als Konzept-/Bibliotheksquelle genutzt.
- Keine ProSync-Profile werden produktiv verändert.

Abschlusskriterium:

- `versionctl deploy --dry-run` kann ProSync-artige Reports erzeugen.

## Etappe 13: ProFiler-Integration als Index-Kern

Zweck: Hashing, Index und Review robuster machen, ohne schwere Module zu importieren.

Aktionen:

- Neutrale ProFiler-Bausteine übernehmen oder neu kapseln:
  - SHA-256
  - SQLite-Index
  - Versionseinträge
  - Labels
  - Soft-Delete-ähnliche Statusfelder für Registry-Einträge
- PDF-, OCR-, Redaction- und GUI-nahe Teile ausdrücklich nicht in den Kern aufnehmen.

Nicht-destruktive Garantie:

- Der Index ist rebuildable Cache, nicht einzige Wahrheit.
- Registry und Dateien bleiben führend.

Abschlusskriterium:

- Index kann gelöscht und aus `.SKILLS` plus Registry neu aufgebaut werden.

## Etappe 14: Export-Adapter nur ausgehend

Zweck: Andere Tools anbinden, ohne fremde Daten ungeprüft in `.SKILLS` zu schreiben.

Aktionen:

- Exporte bauen:
  - Anthropic Skill-Format
  - PromptBoard LibraryItem
  - ProfiPrompt Prompt-Versionen
  - ExplorerPro/ProSync redigierte Profile
  - BACH-kompatible Exportvorschau
- Import bleibt zunächst deaktiviert oder report-only.

Nicht-destruktive Garantie:

- Exporte schreiben in `_exports/`.
- Keine fremden Daten werden automatisch in `.SKILLS` importiert.

Abschlusskriterium:

- Export-Artefakte sind prüfbar und enthalten keine privaten Daten.

## Etappe 15: Erste kontrollierte echte Änderung

Zweck: Nach allen Dry-Runs eine kleine echte Änderung unter Kontrolle durchführen.

Voraussetzung:

- Registry validiert.
- Drift-Bericht grün oder bekannte Abweichungen dokumentiert.
- Privacy-Gate grün.
- Fork-Klasse klar.
- Backup oder Git-Commit vorhanden.

Erlaubte erste echte Änderung:

- Eine neue Template-Komponente anlegen.
- Oder eine Sandbox-Komponente releasen.
- Oder einen einzelnen, nutzerneutralen Skill nur um Registry-Metadaten ergänzen, wenn vorher manuell freigegeben.

Nicht erlaubt:

- Massenmigration.
- Deployment echter Skills.
- Auto-Bump vieler Versionen.
- Rückmerge persönlicher Forks.

Abschlusskriterium:

- Eine echte Änderung wurde vollständig nachvollziehbar, reversibel und klein durchgeführt.

## Etappe 16: Governance verbindlich machen

Zweck: Erst nach Praxistest Regeln scharf stellen.

Aktionen:

- Detailregeln für Rückfluss von persönlichen Forks definieren.
- Detailregeln für Fremdskills und Lizenzfelder definieren.
- Release-Gates finalisieren.
- `versionctl`-Kommandos für echte Schreiboperationen hinter klare Flags setzen:

```text
--apply
--confirm <component-id>
--allow-personal
--allow-foreign
```

Nicht-destruktive Garantie:

- Default bleibt read-only oder dry-run.
- Schreiboperationen brauchen explizite Flags.

Abschlusskriterium:

- Governance ist dokumentiert und in Tooling gespiegelt.

## Reihenfolge als Kurzliste

1. Plan und Freeze.
2. Read-only Inventur.
3. Herkunft und Neutralität klassifizieren.
4. Schemas entwerfen.
5. Schatten-Registry erzeugen.
6. `versionctl` read-only bauen.
7. Templates additiv anlegen.
8. Fork-Modell im Schattenmodus.
9. Produktive Registry minimal aktivieren.
10. Drift-Berichte.
11. Sandbox-Schreibtests.
12. Deployment-Dry-Runs.
13. ProSync als Deployment-Bibliothek anbinden.
14. ProFiler als Index-Kern anbinden.
15. Export-Adapter nur ausgehend.
16. Erste kontrollierte echte Änderung.
17. Governance verbindlich machen.

## Abbruchkriterien

Eine Etappe wird gestoppt, wenn:

- ein aktiver Lock gefunden wird,
- ein Tool mehr als `_reports/`, `_draft/`, `_sandbox/` oder `_exports/` schreiben will,
- persönliche Daten in einem öffentlichen Export auftauchen,
- ein Fremdskill ohne Herkunft/Lizenzklasse produktiv registriert werden soll,
- ein persönlicher Fork ohne Review in einen neutralen Skill zurückfließen soll,
- ein Deployment-Ziel ohne Dry-Run verändert würde,
- ein BACH-Import produktiv statt als Vorschau laufen würde.

## Erfolgskriterium der Gesamtumsetzung

Die Umsetzung ist erfolgreich, wenn `.SKILLS` Folgendes kann:

- Bestand vollständig inventarisieren.
- Eigene und fremde Skills unterscheiden.
- Nutzerneutrale und persönliche Forks unterscheiden.
- Hash- und SemVer-Drift anzeigen.
- Fork-Beziehungen sichtbar machen.
- Releases mit Changelog und Registry-Eintrag vorbereiten.
- Deployments zuerst als Dry-Run planen.
- ProSync für sichere Rollouts und ProFiler für Index/Review nutzen, ohne unnötige schwere Module in den Kern zu ziehen.
- Alles standardisieren, ohne bestehende Skills zu beschädigen.
