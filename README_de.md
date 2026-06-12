# ellmos skills

[Englische Version](README.md) | [Maschinenlesbarer Kontext](llms.txt)

**Portierbare KI-Skillbibliothek für Claude-Code-artige `SKILL.md`-Workflows, Codex-kompatible Agenten-Setups, BACH und andere lokal-first LLM-Agentenlaufzeiten.**

Dieses Repository ist der wiederverwendbare Skill-Katalog des ellmos-Ökosystems. Es enthält eigenständige Prozess-Skills, Entwicklungs-Workflows, Forschungshelfer, therapieorientierte Methoden, Infrastruktur-Playbooks und Utility-Werkzeuge im Anthropic-kompatiblen `SKILL.md`-Format. Jeder Skill trägt seine Metadaten direkt im YAML-Frontmatter, sodass Laufzeiten Herkunft, Kompatibilität und Abhängigkeiten ohne zentrale Registry prüfen können.

## Einstieg

| Bedarf | Datei oder Befehl |
|---|---|
| Alle öffentlichen Skills ansehen | [`skills/`](skills/) |
| Das `SKILL.md`-Schema verstehen | [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md) |
| Skills lokal auflisten | `python catalog.py list` |
| Nach Kategorie filtern | `python catalog.py list --category dev` |
| Herkunft und Sync-Status prüfen | `python catalog.py sync-status` |
| Neues Skill-Gerüst erzeugen | `python catalog.py create "mein-skill" --category utilities --type skill` |
| Drift zur lokalen Skill-Installation prüfen | `python skill_sync.py status` |
| Skills in `~/.claude/skills/` deployen | `python skill_sync.py deploy [skill ...] [--dry-run]` |
| Öffentliche Änderungen nachvollziehen | [`CHANGELOG.md`](CHANGELOG.md) |
| Kompakte Projektkarte für LLMs lesen | [`llms.txt`](llms.txt) |

## Katalogstand

Der aktuelle öffentliche Katalog enthält 43 Laufzeit-Skills:

| Kategorie | Anzahl | Fokus |
|---|---:|---|
| `dev` | 10 | Entwicklungsprotokolle, Debugging, Bug-Sweeps, Pipeline-Renovierung, Migration, Dokumentation, Plugin-Systeme |
| `infrastructure` | 2 | Portables KI-Setup, Betriebssystem-Unterstützung, MCP-Config-Sync zwischen Agent-Apps |
| `research` | 1 | Unterstützung für Forschungsagenten-Workflows |
| `therapy` | 19 | Deutschsprachige Psychoedukation und Gesprächsführungs-Methoden |
| `utilities` | 10 | Batch-Operationen, Denkrahmen, Dokumenten-Chunking, Encoding-Reparatur, YouTube-Transkripte |
| `web` | 1 | Protokoll zum Lesen und Auswerten von Webinhalten |

## Repository-Struktur

```text
skills/
  <kategorie>/
    <skill-name>/
      SKILL.md              # Definition, Frontmatter, Nutzungsablauf
      scripts/              # Optional ausführbare Hilfsprogramme
      references/           # Optional unterstützende Dokumente
  _templates/               # Vorlagen für neue Skills
docs/
  CONVENTIONS.md            # Frontmatter-Spezifikation
catalog.py                  # CLI für Liste, Filter, Sync-Status, Anlage
skill_sync.py               # Deploy-/Drift-Tool: Repo (Quelle) -> ~/.claude/skills
llms.txt                    # Kompakte Projektkarte für LLM-Crawler
```

## Skill-Metadaten

Jede `SKILL.md` deklariert, ob sie eigenständig läuft, ob sie BACH-kompatibel ist und woher sie stammt:

```yaml
standalone: true
bach_compatible: true
bach_origin: true
provenance:
  origin: "bach"
  origin_path: "system/skills/therapie/"
  origin_version: "1.0.0"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
```

Unterstützte Skill-Typen sind `skill`, `agent`, `expert`, `service`, `protocol` und `tool`.

## Suchkontext

Dieses Repository ist relevant für Suchbegriffe wie:

- `ellmos skills`
- `ellmos-ai/skills`
- `agent skill library`
- `SKILL.md catalog`
- `portable AI skills`
- `Claude Code SKILL.md library`
- `Codex skills library`
- `Claude Code and Codex skills`
- `local-first LLM agent skills`
- `BACH skill catalog`
- `Anthropic-compatible skills`

Der Name ist bewusst generisch. Für Verlinkungen und Verzeichnisse sollte deshalb der kanonische Repository-String `ellmos-ai/skills` verwendet werden. Es handelt sich um einen wiederverwendbaren Skill-Katalog, nicht um einen MCP-Server, einen gehosteten SaaS-Marktplatz, ein Prompt-Pack oder einen privaten Skill-Installer.

## Verwandte ellmos-Projekte

| Projekt | Rolle |
|---|---|
| [BACH](https://github.com/ellmos-ai/bach) | Vollständiges textbasiertes LLM-Betriebssystem |
| [Rinnsal](https://github.com/ellmos-ai/rinnsal) | Leichte lokal-first LLM-Agenteninfrastruktur |
| [USMC](https://github.com/ellmos-ai/usmc) | Gemeinsamer Speicherbaustein für Agentensysteme |
| [Gardener](https://github.com/ellmos-ai/gardener) | Datenbankbasierter Betriebssystem-Gegenpart |
| [MarbleRun / llmauto](https://github.com/ellmos-ai/MarbleRun) | Framework zur Ausführung von LLM-Ketten |

## Lizenz

MIT License. Siehe [LICENSE](LICENSE).

## Haftung

Dieses Projekt ist eine unentgeltliche Open-Source-Schenkung im Sinne der §§ 516 ff. BGB. Die Haftung des Urhebers ist gemäß § 521 BGB auf Vorsatz und grobe Fahrlässigkeit beschränkt. Nutzung auf eigenes Risiko. Es gibt keine Wartungszusage, keine Verfügbarkeitsgarantie, keine Gewähr für Fehlerfreiheit und keine Zusicherung der Eignung für einen bestimmten Zweck.
