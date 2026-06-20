# Weitere Versionierungs-Ressourcen

Stand: 2026-06-18

Dieser Bericht ergänzt die BACH-Versionierungsanalyse um drei lokale Software-Projekte und öffentliche Referenzen zu Skills, Agenten, Git-Forks, SemVer und Commit-Konventionen. Ziel ist nicht nur zu prüfen, ob irgendwo Versionierung existiert, sondern welche Bausteine wir für eine saubere Versionierung von `.SKILLS`, Prompts, Workflows und Agenten übernehmen sollten.

## Kurzfazit

| Quelle | Befund | Übernahme für `.SKILLS` |
|---|---|---|
| ProfiPrompt | Stärkstes lokales Modell für Prompt-Versionierung: Prompts besitzen mehrere Versionen, Boards können auf konkrete Versionen zeigen, Exportformat ist stabil versioniert. | Prompt-Versionen und referenzierbare Prompt-Version-IDs als Vorbild. |
| PromptBoard | Einheitliches Item-Modell für `PROMPT`, `SKILL`, `WORKFLOW`, `ROLLE`, `AGENT`; bewusst leichtgewichtig und ohne eigene Versionshistorie. | Gemeinsame Komponenten-Typologie und Materialisierung nach Markdown. |
| ExplorerPro | Workspace-Export mit `schema_version`, Privatsphäre-Grenzen und stabiler v1-Kompatibilität; Prompt-Sammlung ohne Versionshistorie. | Export-/Privacy-Grenze und Schema-Stabilität für Skill-Pakete. |
| ProFiler | SQLite-Index mit `files`, `versions`, SHA-256-Hashes, Version-Labels, Collections, Soft-Delete und Such-/Review-UI. | Stärkste lokale Basis für Komponenten-Inventar, Hashing, Drift-Erkennung und Versionssicht. |
| ProSync | Sync-/Deployment-Tool mit Profilen, Batch-Läufen, Reports, redigierten Profil-Exports und sicherem Umgang mit SQLite/WAL. | Beste lokale Basis für Deployments, Ziel-Sync, Reports und Rollout-Profile. |
| BACH | Versionierte Distribution-Dateien, Manifest, Integritätssiegel, Instanz-Identity, Prompt-Templates mit Versionen. | Registry, Manifest, Hashes, Restore- und Upgrade-Logik als Governance-Schicht. |
| Anthropic / AgentSkills | Skill als Ordner mit `SKILL.md`, Frontmatter und optionalen `scripts/`, `references/`, `assets/`; progressive disclosure. | `.SKILLS` bleibt Anthropic-kompatibel, erweitert aber intern um Versionierung. |
| Git / SemVer | Forks, Branches, Tags, SemVer und Conventional Commits bilden die externe Release-Sprache. | Git-Historie plus Komponenten-SemVer plus Changelog wird Standard. |

## Untersuchungsmethodik

- BACH wurde über `bach.py` gestartet und die integrierte Suche genutzt.
- BACH-Suche zu `ProfiPrompt version`, `PromptBoard version` und `ExplorerPro version` ergab keine belastbaren Projekttreffer im BACH-Korpus.
- BACH-Suche zu `Versionierung` verwies auf Identity-, Distribution- und Upgrade-Hilfen; diese wurden gelesen.
- Die lokalen Software-Projekte wurden direkt im Workspace untersucht:
  - `.SOFTWARE/LLM/REL_ProfiPrompt`
  - `.SOFTWARE/LLM/REL-PUB_PromptBoard`
  - `.SOFTWARE/DATA/REL-PUB_ExplorerPro_SUITE`
- Ergänzend wurden öffentliche Definitionen und Standards geprüft: Anthropic Skills, Claude Code Subagents, SemVer, Conventional Commits, Git Tags und GitHub Forks.

## ProfiPrompt

ProfiPrompt ist die wichtigste lokale Referenz für Prompt-Versionierung. Das Projekt beschreibt sich selbst als Desktop-Werkzeug zur Verwaltung, Versionierung und Organisation von AI-Prompts. Technisch ist die Versionslogik nicht nur ein Release-Label, sondern ein Teil des Datenmodells.

Wesentliche Befunde:

- `Prompt` enthält eine Liste von `Version`-Objekten.
- `Version` enthält unter anderem `id`, `prompt_id`, `version_number`, `title`, `text`, `result`, `tags`, `created_at`, `updated_at`.
- `BoardItem` kann mit `prompt_id` und `version_id` auf eine konkrete Prompt-Version verweisen.
- `storage.py` nutzt atomare JSON-Schreibvorgänge und enthält `add_version()` sowie `next_version_number()`.
- Das Exportformat `profiprompt-library-v1.json` transportiert Prompts, Versionen, Boards, Board-Items, Tags, Zeitstempel und App-Metadaten.
- Die v1-Regel lautet sinngemäß: bestehende Felder bleiben stabil, Erweiterungen erfolgen additiv.
- Die Web-Companion-Komponente validiert `schema_version`, zählt Versionen, löst Board-Einträge über `version_id` auf und kann die ausgewählte Version kopieren.

Bewertung:

ProfiPrompt löst genau das, was bei Prompts in `.SKILLS` sonst schnell verloren geht: Nicht nur der aktuelle Text zählt, sondern die Beziehung zwischen Prompt, konkreter Version, Board-/Kontextnutzung und Export. Für `.SKILLS` sollte dieses Modell als Prompt-Historienmodell dienen.

Offene Lücke:

Die lokale Release-Lage wirkt nicht vollständig synchron: README und Store-Paket zeigen 1.0.1 bzw. 1.0.1.0, während im Git-Kontext nur ein `v1.0.0`-Tag sichtbar war. Das ist ein gutes Warnsignal: Komponenten-Version, App-Version und Git-Tag müssen künftig gemeinsam geprüft werden.

## PromptBoard

PromptBoard ist die wichtigste lokale Referenz für eine einheitliche Typologie von KI-Artefakten. Es verwaltet wiederverwendbare LLM-Bausteine als Items und kennt die Typen `PROMPT`, `SKILL`, `WORKFLOW`, `ROLLE` und `AGENT`.

Wesentliche Befunde:

- `LibraryItem` besitzt `id`, `item_type`, `name`, `content`, `category`, `tags`, `source`, `created_at`, `updated_at`.
- `library.json` ist lokale Bibliothek, Backup-Format und Austauschformat.
- Das Format ist ausdrücklich eine Datei-Brücke, kein Live-Sync-System.
- Die Doku markiert Team-/Server-Versionierung, Rechte, Releases und Synchronisierung als eigenes späteres Modell.
- Der ProfiPrompt-Adapter importiert aus ProfiPrompt die jeweils letzte Version und markiert sie im Inhalt mit einer Version.
- Der ExplorerPro-Adapter bildet ExplorerPro-Prompts auf PromptBoard-PROMPT-Items ab und exportiert sie roundtrip-fähig zurück.
- `RELEASES.md` und `CHANGELOG.md` dokumentieren App-Releases; sichtbare Tags waren `v1.0.0`, `v1.1.0`, `v1.1.1`.

Bewertung:

PromptBoard ist nicht das Vorbild für tiefe Historisierung, sondern für Vereinheitlichung. Es zeigt, dass Prompts, Skills, Workflows, Rollen und Agenten als eine Komponentenfamilie behandelt werden können. Genau diese Typologie ist für `.SKILLS` wertvoll.

Offene Lücke:

PromptBoard hat bewusst keine vollständige Item-Historie. Für `.SKILLS` reicht das nicht aus, weil das Ziel ausdrücklich lautet: alles versionieren und standardisieren. PromptBoard sollte daher als Materialisierungs- und Import-/Export-Schicht dienen, nicht als finales Versionierungsmodell.

## ExplorerPro

ExplorerPro ist die wichtigste lokale Referenz für sichere Workspace-Exporte. Es hat eine Prompt-Sammlung, aber keine tiefe Prompt-Versionierung.

Wesentliche Befunde:

- Exportformat `explorerpro-workspace-v1.json`.
- Export enthält `schema`, `app`, `export_options`, `settings`, `apps`, `prompts`, `sync_profiles`, `privacy`, `reports`, `path_refs`.
- v1-Kompatibilität: neue Felder optional, unbekannte Felder sollen ignoriert werden, UTF-8.
- Export vermeidet private Inhalte wie Datei-Inhalte, private DBs, Clipboard-Daten und Secrets.
- Prompts enthalten unter anderem `id`, `title`, `content`, `category`, `tags`, `favorite`.
- Die Prompt-Komponente speichert lokal in `~/.explorerpro/prompts.json` und ist laut Code an ProfiPrompt angelehnt.
- App-/Store-Versionen sind im untersuchten Stand konsistent bei 1.0.0 bzw. 1.0.0.0.

Bewertung:

ExplorerPro liefert weniger Versionierungslogik, aber eine wichtige Grenze: Exportformate müssen explizit festlegen, was nicht exportiert wird. Für `.SKILLS` bedeutet das: private Beispiele, lokale Pfade, Secrets, Clipboard-Inhalte, personenbezogene Daten und nicht freigegebene Arbeitskontexte gehören nicht in öffentliche Skill-Releases.

## ProSync und ProFiler

ProSync und ProFiler sind zusätzlich relevant, weil sie nicht nur Referenzprojekte sind, sondern eigene Werkzeuge aus dem lokalen Ökosystem. Daraus kann ein neues `.SKILLS`-Versionierungstool entstehen. Die beste Richtung ist kein monolithischer Merge, sondern ein neues kleines Tool, das ProFiler- und ProSync-Bausteine gezielt nutzt.

### ProFiler als Inventar- und Index-Basis

ProFiler bringt bereits viele Bausteine mit, die ein Versionierungstool braucht:

- SQLite-Index mit `files` und `versions`.
- `content_hash` als SHA-256-Fingerprint.
- `version_index`, `version_label`, `is_deleted`, `deleted_at`, `is_hidden`, `hidden_at`.
- Collections über `collection_items`.
- Suche und Review über Versionseinträge.
- Redigiertes Workspace-Exportformat `profiler-workspace-v1`.
- Privacy-Logik mit Pfad-Redaktion und sicherer Import-/Export-Grenze.

Bewertung:

ProFiler ist die stärkste lokale Quelle für Inventarisierung, Hashing, Drift-Erkennung und Review-Oberfläche. Für `.SKILLS` kann daraus der Kern entstehen, der Komponenten scannt, Hashes bildet, Versionseinträge pflegt und Unterschiede sichtbar macht.

### ProSync als Deployment- und Rollout-Basis

ProSync bringt die passende Seite für Auslieferung und Synchronisation:

- Verbindungsprofile mit Quelle, Ziel, Modus und Zeitplan.
- `prosync-profile-v1` als redigiertes Austauschformat.
- Batch-Sync und Reports.
- Sichere SQLite-/WAL-Behandlung.
- Einzeldatei- und Ordnersynchronisation.
- Importierte Profile werden nicht blind produktiv gemacht, sondern müssen lokal neu gemappt werden.

Bewertung:

ProSync passt als Codebibliothek und Konzeptbasis für Deployments: `.SKILLS` nach `~/.claude/skills`, BACH, PromptBoard, ProfiPrompt oder andere Zielorte. Es sollte nicht das Versionierungsmodell definieren, sondern die geprüften Versionen ausrollen und protokollieren.

### Lizenz- und Modulgrenze

Da ProSync und ProFiler eigene Tools sind, ist die interne Wiederverwendung grundsätzlich möglich. Trotzdem sollte das neue Tool sauber getrennt werden:

- ProSync kann als Bibliotheksbasis für Sync-/Deployment-Code genutzt werden.
- ProFiler kann als Quelle für Index-, Hash-, Versionen-, Review- und Export-Logik dienen.
- Lizenz- und Drittkomponenten-Themen sollten modulweise geprüft werden, besonders bei PDF/OCR/Redaction-nahen Teilen und anderen schweren Drittbibliotheken.
- Für das neue Versionierungstool sollte ein sauberer Kern entstehen, der keine unnötigen PDF-, OCR- oder GUI-Abhängigkeiten importiert.

Empfehlung:

Ein neues Tool, etwa `versionctl` oder `SkillVersioner`, sollte die gemeinsame Logik neu bündeln:

```text
ProFiler-Kernidee: scan -> hash -> index -> diff -> review
ProSync-Kernidee: profile -> deploy -> report -> rollback-sicher arbeiten
.SKILLS-Kernidee: frontmatter -> semver -> registry -> fork/branch/release
```

Dieses Tool sollte zuerst CLI-first gebaut werden. Eine GUI kann später aus ProFiler-Ideen entstehen, aber die Governance muss zuerst maschinenlesbar und testbar sein.

## BACH-Bezüge

BACH bringt eine Governance-Sicht mit, die über einfache Datei-Versionen hinausgeht:

- `system_identity` enthält Instanz-ID, Instanzname, Version, Siegelstatus, Kernel-Hash, Boot-Informationen und Modus.
- Das Distribution-System trennt `KERNEL`, `CORE`, `EXTENSION` und `USER_DATA`.
- `distribution_manifest` ist die Quelle für versionierte Distribution-Dateien.
- Upgrade überschreibt nur versionierte Dateien aus Distribution/Manifest.
- `dist_file_versions` verfolgt versionierte Dateien; User-Daten bleiben unangetastet.
- `distribution_system` nennt explizit Tier-Klassifizierung, Siegel-System, Versionierung mit Quellen-Suffixen, Release-Erstellung, Snapshots und Point-in-Time-Recovery.

Bewertung:

Für `.SKILLS` sollte BACH nicht blind als Runtime-Abhängigkeit übernommen werden. Sein Konzept ist aber stark: Ein Skill-Katalog braucht eine klare Trennung zwischen Kern, Erweiterung, Deployment und privaten User-Daten. Außerdem sollte ein Manifest mit Hashes und Release-Zustand die Brücke zwischen Dateisystem, Registry und Deployment bilden.

## `.SKILLS`-Ausgangslage

Die bestehende `.SKILLS`-Doku ist bereits nah am Ziel:

- Jede `SKILL.md` trägt standardisiertes YAML-Frontmatter.
- Pflichtfelder enthalten `name`, `version`, `type`, `author`, `created`, `updated`, `description`.
- Kompatibilität wird über `standalone`, `anthropic_compatible`, `bach_compatible`, `bach_origin` abgebildet.
- Provenance enthält `origin`, `origin_path`, `origin_version`, `last_sync_from_origin`, `last_sync_to_origin`, `local_changes_since_sync`.
- `skills/` ist Quelle der Wahrheit.
- `~/.claude/skills` ist Deployment-Ziel.
- `skill_sync.py` kennt `status`, `deploy`, `diff` und eine `.sync-hold`-Liste für bewusst abweichende Deployment-Skills.

Bewertung:

`.SKILLS` hat schon ein Provenance- und Sync-Fundament. Was fehlt, ist eine explizite Fork-/Branch-Semantik, ein gemeinsames Komponentenmodell für Prompts/Workflows/Agenten sowie eine Release-Governance, die lokale Tools, BACH-Registry und Anthropic-Kompatibilität verbindet.

Zusatzanforderung: Herkunft und Nutzerneutralität müssen getrennt werden.

Ein Skill kann selbst erstellt oder fremd übernommen sein. Unabhängig davon kann er nutzerneutral oder personalisiert sein. Beide Achsen müssen sichtbar bleiben:

| Achse | Werte | Bedeutung |
|---|---|---|
| Herkunft | `own`, `foreign` | Stammt der Skill aus unserem Ökosystem oder aus einer externen Quelle? |
| Neutralität | `neutral`, `personalized` | Ist der Skill allgemein nutzbar oder auf eine konkrete Person/Umgebung angepasst? |
| Fork-Status | `upstream`, `fork` | Ist es die Basislinie oder eine abgeleitete Variante? |

Wichtig ist damit ein Klassen-Denken:

- `own-neutral`: unser nutzerneutraler Standard-Skill.
- `own-personal-fork`: persönlicher Fork eines eigenen neutralen Skills.
- `foreign-neutral`: importierter Fremdskill als möglichst unveränderte Upstream-Referenz.
- `foreign-local-fork`: lokaler, aber noch nutzerneutraler Fork eines Fremdskills.
- `foreign-personal-fork`: persönlicher Fork eines Fremdskills.

Für `.SKILLS` ist besonders wichtig: Wenn ein persönlicher Fork verbessert wird, darf die Verbesserung nicht automatisch im persönlichen Fork steckenbleiben. Es muss einen Rückfluss-Kanal geben: allgemeine, datenschutzneutrale Verbesserungen werden geprüft und in den nutzerneutralen Skill zurückgeführt; persönliche Details bleiben im Fork.

## Öffentliche Referenzen

Relevante öffentliche Definitionen und Standards:

- Anthropic beschreibt Skills als selbständige Ordner mit `SKILL.md`, Metadaten im Frontmatter und optionalen Ressourcen wie Skripten und Referenzen: [Anthropic Engineering: Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).
- Das Anthropic-Beispiel-Repository zeigt die praktische Skill-Struktur und das minimale Frontmatter mit `name` und `description`: [anthropics/skills](https://github.com/anthropics/skills).
- Die öffentliche Agent Skills Spezifikation formalisiert Ordnerlayout, `SKILL.md`, optionale `scripts/`, `references/`, `assets/` und optionale `metadata.version`: [agentskills.io/specification](https://www.agentskills.io/specification).
- Claude Code Subagents sind separate Agentenkontexte mit eigener Beschreibung, Prompt, Toolauswahl und optionalem Modell: [Claude Code Subagents](https://docs.anthropic.com/en/docs/claude-code/sub-agents).
- Claude Code empfiehlt für wiederverwendbare Befehle zunehmend Skill-basierte Ablage unter `.claude/skills/<name>/SKILL.md`; klassische Markdown-Commands bleiben als Legacy-/Custom-Format relevant: [Claude Code Slash Commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands).
- SemVer definiert MAJOR, MINOR, PATCH, Pre-Releases und Build-Metadaten: [Semantic Versioning 2.0.0](https://semver.org/).
- Conventional Commits verbindet Commit-Typen mit SemVer: `fix` -> PATCH, `feat` -> MINOR, Breaking Changes -> MAJOR: [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
- Git Tags markieren Release-Punkte; annotierte Tags sind für Releases vorzuziehen: [Git Book: Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging).
- GitHub Forks sind unabhängige Kopien mit eigenen Branches, Tags, Issues und Pull Requests: [GitHub Docs: About forks](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks).

## Übernahmematrix

| Bedarf | Beste Quelle | Konkrete Übernahme |
|---|---|---|
| Prompt-Historie | ProfiPrompt | Prompt hat mehrere Versionen; Verwendungen können auf konkrete Versionen zeigen. |
| Gemeinsame Typologie | PromptBoard | `PROMPT`, `SKILL`, `WORKFLOW`, `ROLE`, `AGENT` als Komponentenfamilie. |
| Export-Stabilität | ProfiPrompt, ExplorerPro | `schema_version`, additive v1-Entwicklung, unbekannte Felder ignorieren. |
| Privacy-Grenze | ExplorerPro | Explizite Nicht-Export-Regeln für Secrets, lokale Pfade und private Inhalte. |
| Inventar und Drift | ProFiler | SHA-256, SQLite-Index, Versionseinträge, Labels, Soft-Delete und Review-Sicht. |
| Deployment und Rollout | ProSync | Profile, Batch-Sync, Reports, sichere lokale Zielzuordnung und redigierte Exporte. |
| Registry/Manifest | BACH | Manifest, Hash, dist_type, Upgrade nur für versionierte Dateien. |
| Herkunft und Neutralität | `.SKILLS` | Eigene/Fremdskills und neutrale/persönliche Forks getrennt erfassen. |
| Deployment-Forks | `.SKILLS` | `.sync-hold` zur ersten Fork-Klasse ausbauen. |
| Externe Kompatibilität | Anthropic / AgentSkills | `SKILL.md` bleibt portabler Minimalstandard. |
| Releases | SemVer, Git Tags | Komponenten-SemVer, Changelog, annotierte Tags. |
| Änderungssemantik | Conventional Commits | Commit-Typen steuern Versionsempfehlung. |

## Wichtigste Schlussfolgerung

Das Ziel sollte kein einzelnes Versionsfeld sein. Richtig wäre ein Drei-Schichten-Modell:

1. Git versioniert das Repository, Branches und Forks.
2. Komponenten-SemVer versioniert Skill, Prompt, Workflow oder Agent als fachliches Artefakt.
3. Registry/Manifest versioniert Export, Deployment, Hash, Herkunft und Kompatibilität.

Darüber sollte ein neues, kleines Tool entstehen: `versionctl`/`SkillVersioner`. Es nutzt ProFiler-Logik für Inventar, Hashing und Review, ProSync-Logik für Deployment und Reports, und `.SKILLS`-Semantik für SemVer, Registry, Forks, Branches und Releases.

So bleiben `.SKILLS`, BACH, Anthropic-kompatible Runtimes, PromptBoard, ProfiPrompt, ExplorerPro, ProSync und ProFiler anschlussfähig, ohne dass eines der Systeme alle anderen dominieren muss.
