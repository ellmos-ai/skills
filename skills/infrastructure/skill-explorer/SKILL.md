---
name: skill-explorer
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: >
  Verwaltet die eigene Skill-Landschaft: sichtet und vergleicht vorhandene Skills (Audit-Modus),
  recherchiert im Web nach neuen Skills/Plugins (Explore-Modus) und ist zugleich der Installer, der
  schlanke Subskills erzeugt (Skill-Finder, Familien-Umbrella, Pflege-Skills) statt einen Monolithen zu
  laden. Nutze diesen Skill bei „Skills vergleichen/auditieren", „welche Skills sind doppelt",
  „Skill-Familien bilden", „Skills aufräumen/konsolidieren", „Skill-Register pflegen", „Skills/Plugins
  für Thema X finden", „neue Skills installieren", „Skill-Marktplatz durchsuchen", oder bei
  `/skill-explorer`. Liefert pro Familie einen Teilbericht und eine global durchnummerierte
  Entscheidungsliste; installiert/deinstalliert nur nach Sicherheitsprüfung und expliziter Freigabe.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, audit, cluster, recherche, install, security, installer, meta, workflow, branch, fork]
language: de
status: active

dependencies:
  tools: [git]
  services: [websearch]
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-explorer/"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# Skill-Explorer — Skill-Landschaft verwalten (Audit · Explore · Installer)

## Zweck

Mit wachsendem Skill-Bestand entstehen Duplikate, ungenutzte Ressourcen und unklare „welcher Skill
statt welchem"-Situationen — und es gibt draußen ständig neue Skills/Plugins. `skill-explorer`
bündelt drei Rollen in einem Werkzeug:

| Rolle | Was sie tut | Detail |
| --- | --- | --- |
| **Audit-Modus** (nach innen) | alle Skills sichten, in Familien clustern, Fähigkeiten/Abhängigkeiten/Ressourcen erheben, pro Familie Teilbericht + nummerierte Empfehlungen | `references/audit-mode.md` |
| **Explore-Modus** (nach außen) | im Web (Web/GitHub/Reddit, zweisprachig) nach neuen Skills/Plugins zu einem Thema recherchieren, vergleichen, gated installieren | `references/explore-mode.md` |
| **Installer** | schlanke Subskills *erzeugen* statt Monolith — Skill-Finder, Familien-Umbrella, Pflege-Skills | unten + `references/family-care.md` |

Aufruf: `/skill-explorer` (Audit als Default) bzw. „… für Thema X finden" (Explore). Beide Modi teilen
Taxonomie (`references/clustering.md`), Berichtsformat (`references/report-format.md`) und das
Nummerierungsschema, damit der User mit einer einzigen Zahlenliste antworten kann.

## Installer-Prinzip & Persistenz

Statt selbst monolithisch zu wachsen, *generiert* `skill-explorer` bei Bedarf schlanke, einzeln
ladbare Subskills — so muss nie ein überlanger Einzel-Skill geladen werden:

- **Skill-Finder** ([F]) — aktiver Finder/Router analog einem „using-superpowers"-Türsteher, der vor
  jeder Aufgabe das Register liest und zur passenden Familie routet (`references/skill-finder.md`,
  Vorlage `assets/skill-finder-template.md`).
- **Familien-Umbrella** (c1) — Meta-Skill, der eine ganze Familie kennt (`assets/family-umbrella-template.md`).
- **Pflege-Skills** ([P1] Familien, [P2] Register) — halten Familien/Register aktuell (`references/family-care.md`).

Entscheidungen werden in `~/.claude/skills/skill-explorer/config.json` persistiert
(`references/config.md`, Vorlage `assets/config.example.json`): beim Start lesen (bekannte
Familien/Router/erzeugte Subskills), nach Ausführung aktualisieren — so legt ein Re-Run nichts doppelt an.

## Branch-Mechanismus (Drittanbieter anpassen)

Ein read-only-Skill (Plugin, importierter Drittanbieter) kann angepasst werden, ohne das Original zu
verändern: Das Original-Verzeichnis wird vollständig kopiert (**Branch**); anschließend wird nur die
Kopie bearbeitet. Der Branch trägt vier Pflichtangaben: Verweis aufs Original, Branch-Datum,
Bearbeiter und Grund. Sobald der Branch das Original ablöst, wird das Original für die Runtime
deregistriert (`SKILL.md` → `CONTENT.md`) oder der Familien-Router auf den Branch gezeigt, damit
zwei nahezu identische Skills nicht kollidieren. Drittanbieter-Branches bleiben **privat** — sie
gehen nicht in die öffentliche `.AI/.SKILLS`-Library. Detail: `references/skill-branching.md`.

## Ablauf

1. **Modus wählen:** Bestand sichten/aufräumen → Audit-Modus. Von außen suchen/installieren →
   Explore-Modus. (Explore kann auf einen vorherigen Audit/`config.json` aufsetzen.)
2. **Audit-Modus** (`references/audit-mode.md`): Inventar (Skript) → Familien-Cluster → Teilberichte →
   **eine global durchnummerierte Entscheidungsliste** (a/b/c1/c2/c3, plus R/F/P1/P2).
3. **Explore-Modus** (`references/explore-mode.md`): zweisprachige Mehrquellen-Recherche → 3 Kategorien
   je Kandidat → Wirkungs-Simulation → nummerierte Install/Remove-Empfehlungen.
4. **Ausführen** nur nach Zahlen-Bestätigung des Users; Skill-Erzeugung/-Änderung registrieren und
   `config.json` aktualisieren.

## Eiserne Regeln

- **Survey ≠ Mutation:** alles clustern, aber nur **user-eigene** Skills editieren; Plugin-/Drittanbieter-
  Skills sind read-only (nie Header/Löschung). Wer ein Drittanbieter-Skill anpassen will, erzeugt
  stattdessen einen **Branch** (Fork-Kopie) — das Original bleibt unangetastet, die Anpassung erfolgt
  ausschließlich an der Kopie (→ `references/skill-branching.md`).
- **Register erweitern, nicht duplizieren:** existiert ein Skill-Register (Index + Familien-Map +
  Index-Skill), dieses erweitern statt ein viertes anzulegen.
- **Sicherheit primär manuell:** vor jeder Installation liest das Modell den Skill selbst und urteilt;
  `scripts/scan_skill_security.py` ist nur unterstützende Triage mit bekannten Grenzen. Nie auto-install.
- **Registrierung nach Herkunft:** user-authored → Library; Drittanbieter → externer Pfad, **nicht** Library.

## Orchestrierung (modell-neutral)

Familien-Teilberichte bzw. Quellen/Sprachen sind unabhängige Arbeitspfade. Wenn die Plattform
günstigere Subagenten bietet als der Orchestrator selbst, je Familie/Quelle einen Subagenten
beauftragen und als Orchestrator nur konsolidieren/prüfen (Spezialist-Schwarm). Sonst sequenziell selbst.

## Ressourcen

- **Modi:** `references/audit-mode.md`, `references/explore-mode.md`
- **Geteilt:** `references/clustering.md`, `references/report-format.md`, `references/config.md`
- **Audit:** `references/family-care.md`, `references/skill-finder.md`
- **Explore:** `references/research-method.md`, `references/integration-sim.md`, `references/install-uninstall.md`
- **Branch:** `references/skill-branching.md`
- **Skripte:** `scripts/inventory_skills.py` (Inventar), `scripts/inject_family_header.py` (Header-Router),
  `scripts/scan_skill_security.py` (Security-Triage)
- **Vorlagen:** `assets/family-umbrella-template.md`, `assets/skill-finder-template.md`,
  `assets/skill-register-template.md`, `assets/config.example.json`, `assets/branch-header.example.md`

## Changelog

### 1.1.0 (2026-06-17)
- Branch-Mechanismus ergänzt: Drittanbieter-/read-only-Skills können per Fork-Kopie (Branch)
  angepasst werden — mit Verweis aufs Original, Datum, Bearbeiter und Grund; Original bleibt
  unangetastet. Eiserne Regel „Survey ≠ Mutation" um Branch-Ausweg erweitert. Neuer Abschnitt
  `## Branch-Mechanismus`. Neu: `references/skill-branching.md`, `assets/branch-header.example.md`.

### 1.0.0 (2026-06-17)
- Initiale Version. Vereint Bestands-Audit (Familien-Clustering, nummerierte Entscheidungen) und
  Web-Recherche (gated Install mit Security-Triage) in einem Installer, der schlanke Subskills erzeugt.
