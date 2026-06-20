# Standardisierungs- und Versionierungs-Konzept

Stand: 2026-06-18

Ziel: `.SKILLS` soll von Anfang an so standardisiert werden, dass Prompts, Skills, Workflows und Agenten nachvollziehbar versioniert, geforkt, gebrancht, exportiert, geprüft und wieder zusammengeführt werden können. Das Konzept verbindet das bestehende `.SKILLS`-Frontmatter, BACH-Governance, ProfiPrompt-Versionierung, PromptBoard-Typologie, ExplorerPro-Privacy-Grenzen und öffentliche Anthropic-/Git-Standards.

## Leitentscheidung

`.SKILLS` wird die Quelle der Wahrheit für wiederverwendbare KI-Komponenten. Anthropic-Kompatibilität bleibt der kleinste gemeinsame Nenner, BACH bleibt Governance- und Registry-Vorbild, Git bleibt die technische Historie, und die Komponenten selbst erhalten eigene SemVer-Versionen.

Das bedeutet:

- Jede Komponente hat eine eigene Identität.
- Jede Komponente hat eine eigene SemVer-Version.
- Jede veröffentlichte Version ist über Hash, Git-Commit, Branch, Herkunft und Changelog nachvollziehbar.
- Forks und Branches werden nicht nur in Git gedacht, sondern auch im Komponenten-Frontmatter und in einer Registry sichtbar gemacht.
- Private Deployment-Abweichungen werden als Fork-Klasse behandelt, nicht als unsichtbarer Drift.

## Begriffe

| Begriff | Bedeutung |
|---|---|
| Komponente | Versionierbares KI-Artefakt: Prompt, Skill, Workflow, Agent oder Rolle. |
| Skill | Anthropic-kompatibler Ordner mit `SKILL.md` plus optionalen Skripten, Referenzen und Assets. |
| Prompt | Wiederverwendbarer Eingabetext mit Variablen, Output-Vertrag, Modellhinweisen und Version. |
| Workflow | Mehrschrittiges Verfahren mit Triggern, Rollen, Eingaben, Ausgaben, Gates und Validierung. |
| Agent | Delegierbare Arbeitsidentität mit Beschreibung, Systemprompt, Tool-/Skill-Rechten und Modellhinweisen. |
| Branch | Temporäre oder releasebezogene Entwicklungslinie innerhalb derselben Quelle. |
| Fork | Bewusst divergente Variante mit eigener Lebensdauer, eigenem Zweck und Merge-Policy. |
| Release | Freigegebener Stand einer oder mehrerer Komponenten mit Tag, Changelog, Manifest und Prüfprotokoll. |
| Deployment | Ausgerollte Kopie, zum Beispiel nach `~/.claude/skills`, BACH oder ein anderes Runtime-Ziel. |

## Standardstruktur

Die bestehende `skills/`-Struktur bleibt erhalten. Für Prompts, Workflows und Agenten wird ein analoges Komponentenmodell eingeführt.

```text
.SKILLS/
  skills/<kategorie>/<skill-name>/
    SKILL.md
    scripts/
    references/
    assets/
    tests/

  prompts/<kategorie>/<prompt-name>/
    PROMPT.md
    examples/
    tests/

  workflows/<kategorie>/<workflow-name>/
    WORKFLOW.md
    references/
    tests/

  agents/<kategorie>/<agent-name>/
    AGENT.md
    references/
    tests/

  registry/
    components.json
    forks.json
    branches.json
    releases.json
    deployments.json

  schemas/
    component-v1.schema.json
    skill-v1.schema.json
    prompt-v1.schema.json
    workflow-v1.schema.json
    agent-v1.schema.json
```

Regel: Bestehende Skills werden nicht vorschnell verschoben. Zuerst wird die Registry eingeführt, dann werden neue Komponenten-Typen ergänzt.

## Gemeinsames Komponenten-Frontmatter

Alle Komponenten bekommen ein gemeinsames Kern-Frontmatter. Für `SKILL.md` bleibt die Anthropic-kompatible Minimalform erhalten; die internen Felder werden als kompatible Erweiterung geführt.

```yaml
---
name: beispiel-komponente
type: skill              # skill | prompt | workflow | agent | role | tool | protocol
version: 1.0.0
schema_version: component-v1
status: draft            # draft | active | deprecated | archived
language: de
description: >
  Kurze Beschreibung der Komponente.

compatibility:
  anthropic: true
  bach: true
  promptboard: true
  profiprompt: false
  explorerpro: false

provenance:
  origin: custom          # custom | bach | anthropic | promptboard | profiprompt | explorerpro | community
  origin_path: null
  origin_version: null
  origin_commit: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false

ownership:
  source_kind: own        # own | foreign
  neutrality: neutral    # neutral | personalized
  upstream_component: null
  personalized_for: null # nur in privaten/personalisierten Forks setzen
  sanitization_required: false

versioning:
  stability: experimental # experimental | stable | locked
  api_surface: content    # content | variables | tool-contract | runtime-contract
  changelog_required: true
  released: false
  release_tag: null
  content_hash: null

branch:
  name: main
  base: null
  purpose: stable

fork:
  is_fork: false
  fork_of: null
  fork_reason: null
  divergence_policy: upstream-first
  merge_policy: rebase-or-pr

privacy:
  level: public           # public | internal | private | secret
  contains_personal_data: false
  contains_local_paths: false
  export_allowed: true
---
```

## Typ-spezifische Standards

### Skills

Skills folgen weiter dem bestehenden `.SKILLS`-Standard:

- `SKILL.md` ist Pflicht.
- `name`, `version`, `type`, `author`, `created`, `updated`, `description` bleiben Pflichtfelder.
- `standalone`, `anthropic_compatible`, `bach_compatible`, `bach_origin` bleiben erhalten.
- `provenance.origin_version` dokumentiert den BACH- oder Fremdstand.
- Ein Changelog am Ende der `SKILL.md` ist Pflicht für Releases.
- Keine BACH-Runtime-Imports in `standalone: true` Skills.

Erweiterung:

- `versioning.content_hash` wird bei Release gesetzt.
- `fork` und `branch` werden ergänzt, sobald ein Skill nicht mehr einfach `main` folgt.
- `.sync-hold` wird als Deployment-Fork im Registry-Modell abgebildet.

### Prompts

Prompts orientieren sich an ProfiPrompt:

- Ein Prompt kann mehrere Versionen haben.
- Nutzungen können auf eine konkrete Prompt-Version zeigen.
- Variablen und Output-Vertrag gehören zur öffentlichen Kompatibilitätsfläche.
- Copy-Edits sind PATCH.
- Neue optionale Variablen oder neue Beispiele sind MINOR.
- Entfernte Variablen, geänderter Output-Vertrag oder inkompatible Modellannahmen sind MAJOR.

Empfohlenes `PROMPT.md`:

```yaml
---
name: beispiel-prompt
type: prompt
version: 1.0.0
schema_version: prompt-v1
description: >
  Zweck des Prompts.
variables:
  - name: input
    required: true
    description: Hauptinput.
output_contract:
  format: markdown
  required_sections: []
model_notes:
  preferred_models: []
  temperature: null
versioning:
  history_model: profiprompt-style
  current_version_id: null
---
```

### Workflows

Workflows bekommen eine explizite Ablauf- und Prüfstruktur:

- Trigger: Wann wird der Workflow genutzt?
- Inputs: Welche Informationen sind nötig?
- Steps: Welche Schritte sind in welcher Reihenfolge auszuführen?
- Roles: Welche Agenten/Personas dürfen beteiligt sein?
- Gates: Welche Prüfungen müssen vor Abschluss bestanden sein?
- Outputs: Welche Artefakte entstehen?
- Recovery: Was passiert bei Drift, Konflikt oder fehlenden Inputs?

Versionierung:

- PATCH: Klarstellungen, Tippfehler, kleine Gate-Ergänzungen ohne Verhaltensbruch.
- MINOR: Neue optionale Schritte, neue unterstützte Ziele, neue Prüfroutinen.
- MAJOR: Geänderte Reihenfolge, Pflichtinputs, Zuständigkeiten oder Abschlusskriterien.

### Agenten

Agenten müssen zwei Welten sauber trennen:

- Anthropic/Claude-Code-Subagents: delegierbare Agenten mit Beschreibung, Prompt, Toolauswahl und optionalem Modell.
- BACH-Agenten/Personas: Rollen und Experten in einem größeren Governance-System.

Empfohlenes `AGENT.md`:

```yaml
---
name: beispiel-agent
type: agent
version: 1.0.0
schema_version: agent-v1
description: >
  Delegationsbeschreibung. Diese Beschreibung entscheidet, wann der Agent genutzt wird.
agent:
  prompt: AGENT.md
  tools: []
  model: null
  skills: []
compatibility:
  anthropic_subagent: true
  bach_agent: false
---
```

Versionierung:

- PATCH: Formulierungen ohne geänderte Delegationsgrenze.
- MINOR: Neue Tools, neue Skills, bessere Spezialanweisungen ohne Bruch.
- MAJOR: Geänderte Zuständigkeit, neue Sicherheitsgrenze, anderes Modellprofil oder entfernte Tools.

## Branch-Strategie

Branches sind Entwicklungslinien innerhalb derselben Quelle. Sie sollen kurzlebig, nachvollziehbar und mergebar bleiben.

| Branch | Zweck |
|---|---|
| `main` | Stabiler, freigegebener Stand. |
| `dev/<komponente>` | Aktive Arbeit an einer Komponente. |
| `feature/<thema>` | Neue Fähigkeit oder neue Struktur. |
| `fix/<thema>` | Fehlerkorrektur ohne Bruch. |
| `release/vX.Y.Z` | Release-Vorbereitung, Freeze und Prüfungen. |
| `hotfix/<thema>` | Schnelle Korrektur auf Release-Basis. |
| `experiment/<idee>` | Unsichere Explorationsarbeit mit Ablaufdatum. |

Regeln:

- Jeder Branch hat ein Ziel, eine Baseline und ein Ablaufdatum.
- Kein Release direkt aus `experiment/*`.
- `release/*` darf nur noch Fixes, Doku, Versionen und Prüfergebnisse ändern.
- Branches werden in `registry/branches.json` gespiegelt, wenn sie länger als einen Arbeitstag existieren.

## Herkunft und Nutzerneutralität

Vor jeder Fork-Entscheidung muss klar sein, ob eine Komponente selbst erstellt oder fremd übernommen ist und ob sie nutzerneutral oder personalisiert ist. Diese beiden Achsen dürfen nicht vermischt werden.

| Klasse | Bedeutung | Standard-Verhalten |
|---|---|---|
| `own-neutral` | Unser eigener, nutzerneutraler Skill/Prompt/Workflow/Agent. | Primäre Basislinie, veröffentlichbar nach Privacy-Gate. |
| `own-personal-fork` | Auf Lukas oder eine konkrete lokale Umgebung angepasster Fork eines eigenen neutralen Artefakts. | Privat oder intern; generische Verbesserungen können zurückfließen. |
| `foreign-neutral` | Fremdskill möglichst nah am externen Upstream. | Herkunft, Lizenz, Version und Upstream-Pfad bleiben erhalten. |
| `foreign-local-fork` | Lokaler neutraler Fork eines Fremdskills, z. B. bereinigt oder portiert. | Änderungen getrennt dokumentieren; Rückfluss zum Fremd-Upstream optional. |
| `foreign-personal-fork` | Persönlicher Fork eines Fremdskills. | Nicht veröffentlichen, solange Personalisierung oder lokale Details enthalten sind. |

Grundsatz:

- Der nutzerneutrale Skill ist die stabile Basis.
- Der persönliche Fork darf lokale Pfade, persönliche Präferenzen, Rollenfeinheiten oder Arbeitsweisen enthalten.
- Wenn im persönlichen Fork eine allgemein nützliche Verbesserung entsteht, wird sie nicht blind übernommen, sondern als neutralisierbarer Patch geprüft.
- Wenn ein Fremdskill personalisiert wird, bleibt die Fremdherkunft sichtbar; Personalisierung erzeugt keinen neuen neutralen Ursprung.

Rückfluss-Modell:

```text
own-neutral -> own-personal-fork       # Personalisierung
own-personal-fork -> own-neutral       # nur bereinigte, allgemeine Verbesserung
foreign-neutral -> foreign-local-fork  # Portierung/Bereinigung
foreign-local-fork -> foreign-personal-fork # persönliche Anpassung
```

Das spätere Regelwerk muss daraus genaue Gates ableiten. Für das Konzept reicht die Festlegung: Herkunft, Neutralität und Fork-Beziehung sind Pflichtdimensionen im Registry-Modell.

## Fork-Strategie

Forks sind bewusste, längerlebige Varianten. Ein Fork ist kein Unfall und kein stiller Drift.

Fork-Klassen:

| Fork-Klasse | Beispiel | Merge-Policy |
|---|---|---|
| `deployment` | Skill in `~/.claude/skills` ist lokal angepasst und steht auf `.sync-hold`. | Upstream nur nach Review überschreiben. |
| `private` | Lokale private Variante mit persönlichen Beispielen. | Nie öffentlich exportieren. |
| `public-sanitized` | Öffentliche Fassung ohne private Pfade und personenbezogene Details. | Wird aus interner Fassung generiert oder manuell gepflegt. |
| `own-personal` | Persönlicher Fork eines eigenen neutralen Skills. | Generische Verbesserungen können nach Neutralisierung zurück in `own-neutral`. |
| `foreign-local` | Lokaler Fork eines Fremdskills. | Upstream-Herkunft und lokale Änderungen getrennt dokumentieren. |
| `foreign-personal` | Persönlicher Fork eines Fremdskills. | Kein öffentlicher Export ohne vorherige neutrale Zwischenfassung. |
| `bach-origin` | Aus BACH exportierter Skill mit Provenance. | Upstream-Sync möglich, BACH-Abhängigkeiten prüfen. |
| `anthropic-port` | Kompatibilitätsvariante für Anthropic Skills. | Nur minimale Felder erzwingen. |
| `runtime-adapter` | Variante für PromptBoard, ProfiPrompt, ExplorerPro oder andere Ziele. | Rückführung nur über Adapter-Regeln. |

Pflichtfelder für Forks:

```yaml
fork:
  is_fork: true
  fork_of: skills/dev/beispiel/SKILL.md
  fork_reason: deployment-localization
  divergence_policy: explicit
  merge_policy: pull-request
  privacy_level: internal
  upstream_ref: main
```

## Release-Modell

Jeder Release besteht aus vier Ebenen:

1. Git-Tag, bevorzugt annotiert.
2. Komponenten-Version im Frontmatter.
3. Changelog-Eintrag in der Komponente.
4. Registry-Manifest mit Hash, Pfad, Commit, Branch, Fork und Exportzielen.

Empfohlene Tag-Formate:

```text
skills/v1.4.0
prompt/<name>/v1.2.0
workflow/<name>/v2.0.0
agent/<name>/v1.1.0
catalog/v2026.06.18
```

SemVer-Regeln:

- MAJOR: Inkompatible Änderung an Variablen, Output-Vertrag, Toolvertrag, Ablauf, Zuständigkeit oder Runtime-Kompatibilität.
- MINOR: Neue rückwärtskompatible Funktionalität.
- PATCH: Fehlerkorrektur, Klarstellung, Formatierung, kleinere Qualitätsverbesserung.
- Pre-Releases: `1.2.0-alpha.1`, `1.2.0-rc.1`.
- Build-Metadaten: `1.2.0+bach.3.9.0` nur für Zusatzinformationen, nicht für Sortierung.

Commit-Regeln:

- `fix:` empfiehlt PATCH.
- `feat:` empfiehlt MINOR.
- `BREAKING CHANGE:` oder `!` empfiehlt MAJOR.
- `docs:`, `test:`, `refactor:`, `chore:` ändern die Version nur, wenn sich die Kompatibilitätsfläche ändert.

## Registry-Modell

`registry/components.json` ist der maschinenlesbare Katalog. Er ersetzt nicht das Frontmatter, sondern spiegelt und prüft es.

Minimaler Eintrag:

```json
{
  "id": "skill:dev:beispiel",
  "name": "beispiel",
  "type": "skill",
  "path": "skills/dev/beispiel/SKILL.md",
  "version": "1.0.0",
  "schema_version": "skill-v1",
  "status": "active",
  "content_hash": "sha256:...",
  "git_commit": "...",
  "branch": "main",
  "fork": null,
  "origin": "custom",
  "compatibility": {
    "anthropic": true,
    "bach": false
  },
  "privacy": {
    "level": "public",
    "export_allowed": true
  }
}
```

`registry/forks.json` enthält die Fork-Beziehungen. `registry/branches.json` enthält längerlebige Branches. `registry/releases.json` enthält Release-Bundles. `registry/deployments.json` enthält Deployments nach `~/.claude/skills`, BACH, PromptBoard, ProfiPrompt, ExplorerPro oder andere Ziele.

## Versionierungstool

Für die Umsetzung wird ein neues Tool empfohlen: `versionctl` oder `SkillVersioner`. Es sollte nicht als großer Umbau von ProSync und ProFiler entstehen, sondern als kleiner, testbarer Kern, der passende Bausteine aus beiden Projekten nutzt.

Grundidee:

```text
ProFiler: scan -> hash -> index -> diff -> review
ProSync: profile -> deploy -> report -> safe sync
.SKILLS: frontmatter -> semver -> registry -> fork/branch/release
```

Empfohlene Rollen:

| Quelle | Rolle im neuen Tool |
|---|---|
| ProFiler | Inventar, SQLite-Index, SHA-256, Versionseinträge, Labels, Collections, Soft-Delete, Review-Sicht. |
| ProSync | Deployment-Profile, Ziel-Sync, Batch-Läufe, Reports, sichere lokale Remapping-Logik. |
| `.SKILLS` | Komponentenmodell, Frontmatter, SemVer, Registry, Forks, Branches und Releases. |
| BACH | Manifest-, Dist-Type-, Siegel-, Upgrade- und Restore-Denken. |

Erste CLI-Kommandos:

```text
versionctl scan
versionctl status
versionctl diff <component>
versionctl bump <component> --patch|--minor|--major
versionctl release <component>
versionctl fork create <component>
versionctl branch register <name>
versionctl deploy claude|bach|promptboard
versionctl export anthropic|promptboard|profiprompt|explorerpro|bach
```

Technische Leitlinie:

- CLI zuerst, GUI später.
- Keine PDF-/OCR-/GUI-Abhängigkeiten im Kern.
- SQLite für lokalen Index, JSON für portable Registry.
- Hashes und Frontmatter sind die primäre Wahrheit, nicht Dateinamen.
- Deployment läuft nur aus freigegebenen Registry-Ständen.
- ProSync darf als Codebibliothek für Sync-/Deployment-Mechanik genutzt werden.
- ProFiler darf als eigene Codebasis für Index-/Hash-/Review-Mechanik genutzt werden; lizenz- und drittkomponentensensible Teile werden modulweise getrennt.

Lizenz-/Modulgrenze:

ProSync und ProFiler sind eigene Werkzeuge. Für das neue Tool ist deshalb nicht die interne Wiederverwendung das Problem, sondern die saubere Trennung von Drittkomponenten und schwergewichtigen Spezialmodulen. PDF-, OCR-, Redaction- und GUI-nahe Teile gehören nicht in den Kern. Der Kern sollte nur die neutralen Versionierungsbausteine übernehmen: Hashing, Index, Registry, Diff, Release, Deployment-Profile und Reports.

## BACH-Integration

BACH wird als Governance-Partner behandelt, nicht als Pflicht-Runtime für jeden Skill.

Übernahmen aus BACH:

- Identity: Instanz, Version, Modus, Integritätsstatus.
- Distribution: Trennung von Kern, Erweiterung, User-Daten.
- Manifest: Nur registrierte, versionierte Dateien sind upgrade-/restorefähig.
- Hash/Siegel: Releases sollen prüfbar sein.
- Upgrade-Denken: Deployment überschreibt nur versionierte und freigegebene Dateien.

Vorgeschlagene Zuordnung:

| BACH-Konzept | `.SKILLS`-Konzept |
|---|---|
| `system_identity` | `registry/catalog_identity.json` |
| `distribution_manifest` | `registry/components.json` plus Hashes |
| `dist_file_versions` | `registry/releases.json` und Changelog |
| `dist_type=0/1/2/3` | `core`, `standard`, `extension`, `private` |
| Siegelstatus | Release- und Deployment-Integritätsprüfung |
| `bach upgrade --dry-run` | `versionctl release --dry-run` |

## Export- und Adapter-Modell

`.SKILLS` soll nicht alle Tools ersetzen. Stattdessen werden saubere Adapter definiert.

| Ziel | Export-Regel |
|---|---|
| Anthropic Skills | Nur Skill-Ordner mit `SKILL.md`, optional `scripts/`, `references/`, `assets/`; minimale Felder bleiben gültig. |
| Claude Code Subagents | `AGENT.md` kann nach `.claude/agents/<name>.md` materialisiert werden. |
| PromptBoard | Komponenten werden als `LibraryItem` mit Typ, Name, Content, Tags, Source exportiert. |
| ProfiPrompt | Nur Prompts werden mit Versionen exportiert; Skill-/Agent-Inhalte höchstens als Referenz. |
| ExplorerPro | Nur sichere Prompt-/Workspace-Metadaten, keine Secrets, keine privaten Inhalte. |
| ProSync | Deployment-Profile, Batch-Rollouts und Reports; keine Definition der Komponenten-Version selbst. |
| ProFiler | Lokaler Index, Hashing, Versionsreview und Drift-Analyse; kein schwerer PDF-/OCR-Kern im Versionierungstool. |
| BACH | Nur `bach_compatible: true` Komponenten; BACH-Abhängigkeiten und Provenance müssen explizit sein. |

## Qualitätsgates

Ein Release darf nur erfolgen, wenn diese Gates grün sind:

- Frontmatter ist syntaktisch gültig.
- `version` ist SemVer.
- `updated` ist aktuell.
- Changelog enthält die Version.
- `privacy.export_allowed` passt zum Ziel.
- Keine lokalen privaten Pfade, Secrets oder personenbezogenen Beispiele in öffentlichen Komponenten.
- `standalone: true` Skills enthalten keine verpflichtenden BACH-Imports.
- Tests laufen, wenn `scripts/` oder Tools vorhanden sind.
- Export nach Anthropic-Minimalstruktur funktioniert für Skills.
- Registry-Hash stimmt mit Dateiinhalt überein.
- Bei BACH-kompatiblen Komponenten ist ein BACH-Import-/Dry-Run möglich.
- Bei Deployment-Forks ist `.sync-hold` oder ein Registry-Fork eingetragen.

## Migrationsplan

### Phase 0: Freeze und Inventur

- Keine Massenverschiebung bestehender Skills.
- Aktuelle `.SKILLS`-Regeln als verbindlich markieren.
- Bestehende `.sync-hold`-Einträge als Deployment-Forks erfassen.
- Aktuelle BACH-Kollisionen und Provenance-Lücken dokumentieren.

### Phase 1: Registry einführen

- `registry/components.json` aus bestehenden `SKILL.md`-Frontmattern generieren.
- Hashes und Pfade erfassen.
- Bestehende Skills nach `own-neutral`, `own-personal-fork`, `foreign-neutral`, `foreign-local-fork` und `foreign-personal-fork` klassifizieren.
- `registry/forks.json`, `registry/branches.json`, `registry/releases.json`, `registry/deployments.json` als leere, versionierte Dateien anlegen.
- JSON-Schemas definieren.

### Phase 2: Komponentenmodell erweitern

- `prompts/`, `workflows/`, `agents/` als neue Quellenbereiche einführen.
- Vorlagen für `PROMPT.md`, `WORKFLOW.md`, `AGENT.md` erstellen.
- PromptBoard-Typologie übernehmen, aber um SemVer und Forks erweitern.

### Phase 3: Adapter bauen

- PromptBoard-Export/Import für alle Komponenten-Typen.
- ProfiPrompt-Export/Import für Prompt-Versionen.
- ExplorerPro-Export nur für sichere Prompt-/Workspace-Sicht.
- BACH-Export/Import nur für kompatible Komponenten.

### Phase 4: Release-Tooling

- `versionctl.py` oder Erweiterung von `catalog.py`:
  - `versionctl check`
  - `versionctl scan`
  - `versionctl status`
  - `versionctl diff <component>`
  - `versionctl bump <component> --patch|--minor|--major`
  - `versionctl release <component>`
  - `versionctl fork create`
  - `versionctl branch register`
  - `versionctl deploy claude|bach|promptboard`
  - `versionctl export anthropic|promptboard|profiprompt|explorerpro|bach`

### Phase 5: Governance verbindlich machen

- Keine öffentlichen Releases ohne Registry-Eintrag.
- Keine Deployment-Überschreibung ohne Drift-Bericht.
- Keine Forks ohne Fork-Reason.
- Keine privaten Komponenten in öffentlichen Exporten.
- Keine MAJOR-Änderungen ohne expliziten Breaking-Change-Eintrag.

## Minimaler nächster Schritt

Der pragmatische nächste Schritt ist klein:

1. `registry/` und `schemas/` anlegen.
2. Bestehende Skills aus `skills/` in `registry/components.json` spiegeln.
3. Eigene/Fremdskills und neutrale/persönliche Varianten klassifizieren.
4. `.sync-hold` in `registry/forks.json` überführen.
5. Eine Vorlage für `PROMPT.md`, `WORKFLOW.md` und `AGENT.md` erstellen.
6. Einen schlanken `versionctl`-Prototyp bauen:
   - bestehende Skills scannen
   - SHA-256-Hashes berechnen
   - `registry/components.json` schreiben
   - Drift zwischen Registry und Dateisystem anzeigen
7. `catalog.py` nur dort erweitern, wo es bereits für Skill-Kataloglogik zuständig ist.

Damit entsteht sofort Ordnung, ohne dass bestehende Skills riskant umgebaut werden.

## Entscheidungsregel

Wenn unklar ist, ob eine Änderung als Branch, Fork oder neue Version behandelt wird:

- Gleiche Absicht, kurzfristige Arbeit: Branch.
- Gleiche Komponente, freigegebener neuer Stand: Version.
- Dauerhaft andere Zielgruppe, andere Runtime, private Abweichung oder andere Sicherheitsgrenze: Fork.

Diese Regel verhindert den typischen Mischmasch aus verstecktem Drift, zufälligen Kopien und unklaren Deployment-Ständen.
