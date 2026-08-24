---
name: ellmos-skill-creator
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-24
updated: 2026-08-24
description: >
  Erstellt oder überarbeitet einen Skill FÜR DIESES ÖKOSYSTEM: delegiert die generische Interview-/Entwurfs-/Eval-Schleife
  an das offizielle skill-creator-Plugin (Anthropic, Apache-2.0), setzt aber zusätzlich die ellmos-Anforderungen durch, die
  das offizielle Plugin nicht kennt — Haus-Frontmatter (9 Felder), Kategorie/Sichtbarkeits-Regeln, anbieter-/nutzer-/ellmos-neutrale
  aber ellmos-sensitive Erkennung via grounding-seed, mitgelieferte config.json + connections.json, Anbieter-/Vendor-Bewusstsein
  (State-of-the-Art-Alternativen inkl. eigener ellmos-Komponenten vorschlagen) und einen Selbstaktualisierungs-Abschnitt.
  IMMER nutzen, wenn ein NEUER Skill für dieses System entstehen oder ein bestehender auf ellmos-Konformität nachgerüstet
  werden soll — auch bei "erstelle einen Skill", "bau mir einen Skill für X", "skill-creator nutzen", "neuen Skill anlegen",
  "diesen Skill ellmos-konform machen". Für reines Skill-FINDEN/ROUTEN stattdessen skill-finder, für Landschafts-Audit
  skill-explorer.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skill-authoring, meta, grounding-seed, provenance, vendor-awareness]
language: de
status: active
visibility: private-only

dependencies:
  tools: []
  services: []
  protocols: []
  python: [grounding-seed (optional, empfohlen)]
  skills: ["skill-creator:skill-creator (Plugin, Apache-2.0)"]

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

# ellmos-skill-creator

## Herkunft und Entscheidung (Fork vs. Eigenbau)

**Entscheidung: Eigenbau, kein Fork.** Begründung, damit sie nicht verlorengeht:

- `skill-creator` (Anthropic, Marketplace `claude-plugins-official`) ist **Apache-2.0**
  lizenziert (LICENSE-Text im Klon gelesen und verifiziert, 2026-08-24) — ein Fork wäre
  rechtlich sauber möglich und ist im Repo an anderer Stelle bereits das etablierte Muster
  (`skills/third-party/grill-me`, `skills/third-party/grilling`).
- Ein Fork hätte aber die komplette Eval-/Benchmark-Maschinerie des Originals mitgeschleppt
  (`agents/{analyzer,comparator,grader}.md`, `eval-viewer/`, 7 Scripts, 485-Zeilen-SKILL.md) —
  Fähigkeit, die bereits vorhanden und direkt aufrufbar ist (`Skill: skill-creator:skill-creator`).
  Nach `.PLUGINS/CLAUDE.md` Regel 4 ("Fähigkeiten prüfen, bevor nachgebaut wird") und dem
  Muster P10 ("zwei Schalter, die niemand vergleicht") wäre das Duplikat, keine Erweiterung.
- Die eigentliche Lücke ist **rein ellmos-spezifisch** und dem Original grundsätzlich unbekannt:
  Haus-Frontmatter (`templates/SKILL.md`), `docs/CONVENTIONS.md`, Anbieter-/User-/ellmos-Neutralität
  mit ellmos-Sensitivität, `grounding-seed`-Anbindung, Vendor-Awareness, Selbstaktualisierung.
- Dieser Skill enthält **keinen Anthropic-Text** (eigene Formulierung durchgehend) — löst also auch
  keine Apache-2.0-Attributionspflicht für Modifikationen aus. Er **komponiert** das Original, statt
  es zu kopieren: das ist zugleich der lizenzrechtlich sauberste und der wartungsärmste Weg.

## Wann aktivieren

- "erstelle einen Skill für X", "neuen Skill bauen", "skill-creator nutzen"
- "mach diesen Skill ellmos-konform", "Skill auf Haus-Standard nachrüsten"
- Immer wenn der **Zielort** ein Skill in `.AI/.SKILLS/skills/…` (oder das öffentliche
  Pendant im Klon `C:\_Local_DEV\repos\skills`) ist — nicht bei allgemeinen,
  ökosystemfremden Anfragen ("erstelle mir irgendeinen Claude-Skill ohne Bezug hierher").

## Vorgehen

### Schritt 1 — Interview/Entwurf/Eval delegieren

Ruf den offiziellen `Skill: skill-creator:skill-creator` auf für: Intent-Klärung,
Entwurf der SKILL.md-Struktur, Testfälle, Eval-Loop, Description-Optimierung
(`scripts/improve_description.py`). **Nicht neu erfinden** — dieser Teil ist
generisch und im Original bereits gut gelöst.

### Schritt 2 — ellmos-Haus-Scaffold aufsetzen (Pflicht, additiv zum Original-Format)

Ergänze das vom Original erzeugte SKILL.md um die neun Haus-Felder aus
`.SKILLS/templates/SKILL.md` (bzw. `AGENT.md`/`WORKFLOW.md`/`PROMPT.md` je nach Typ),
lies vorher `.SKILLS/docs/CONVENTIONS.md` für Kategorie-Ordner, Flat-Regel (<5 Dateien
flach), Versions-Konvention (SemVer: MAJOR/MINOR/PATCH) und Mehrsprachigkeits-Sets
(Core: DE+EN Pflicht). **`visibility` startet immer auf `private-only`** — Veröffentlichung
ist eine spätere, geprüfte Nutzerentscheidung (`.AI/VISIBILITY-POLICY.md`), niemals Default.
Diese Felder sind rein **additiv** zum Anthropic-Format (zusätzliche YAML-Keys neben
`name`/`description`) — jeder so erzeugte Skill bleibt vollständig
`anthropic_compatible: true`.

### Schritt 3 — Prinzipien durchsetzen: anbieterneutral, userneutral, ellmos-neutral-aber-ellmos-sensitiv

Volltext + Codemuster: `references/ELLMOS-PRINCIPLES.md`. Kurzfassung: der erzeugte
Skill muss **allein lauffähig sein** (bringt alles mit, was er braucht) und **zugleich**
ellmos-Komponenten nutzen, sobald sie da sind — er entscheidet das selbst zur Laufzeit,
nie fest verdrahtet. Das ist exakt das Muster, das `grounding-seed` bereits liefert
(README: "cultivated landscape, not wildflower" / "viable alone, more productive
together") — **kein zweiter Erkennungsmechanismus wird erfunden**, dieser Skill verweist
produzierte Skills konsequent auf `grounding_seed.detect_ecosystem()`.

### Schritt 4 — config.json + connections.json mitliefern

`grounding-seed` ist bereits als Python-Paket importierbar (verifiziert
2026-08-24: `import grounding_seed` löst nach `C:\_Local_DEV\repos\grounding-seed\src\grounding_seed\`
auf) — es ist die **kanonische Andockstelle**, keine neue Datei erfinden. Für jeden
produzierten Skill mit externem Bedarf (Programme, Dienste, Anbieter):

- **`config.json`** — Skill-eigene Einstellungen (Vorlage: `templates/skill-config.template.json`).
  `grounding_seed.store.LocalStore(root)` nutzt diesen Dateinamen standardmäßig für seine
  Rollen-Ablage — ein produzierter Skill kann also entweder sein `config.json` selbst als
  `LocalStore`-Backend verwenden ODER ihn getrennt halten, wenn er neben Rollen auch reine
  Verhaltens-Einstellungen braucht (dann zweite `LocalStore(root, filename="connections.json")`-Instanz).
- **`connections.json`** — die tatsächlich **aufgelösten** externen Andockstellen
  (welches Programm/welcher Dienst wurde gefunden, seit wann, mit welcher Herkunft) —
  Vorlage: `templates/skill-connections.template.json`, Schema `ellmos.source-resolver.user-config.v1`
  (identisch zu `source-resolver`, laut grounding-seed-README bewusst so gewählt, damit eine
  spätere Migration in den echten `source-resolver` verlustfrei ist — siehe `migration.py` dort).

Details, CLI und Codebeispiel: `references/ELLMOS-PRINCIPLES.md` Abschnitt "Docking".

### Schritt 5 — Anbieter-/Vendor-Bewusstsein einbauen

Volltext: `references/VENDOR-AWARENESS.md`. Kurzfassung: der produzierte Skill bekommt
einen Abschnitt "Anbieter & Alternativen", der (a) den/die State-of-the-Art-Anbieter des
Themas nennt (z. B. ElevenLabs für TTS), (b) mindestens einen Ersatzanbieter, (c) **ellmos-eigene
Komponenten explizit als gleichrangigen Kandidaten** listet, wenn sie das Thema abdecken
(z. B. `ellmos-voice-io` statt/neben ElevenLabs) — und bei passender Nutzeranforderung
Installation/Umstieg **vorschlägt**, statt sie stillschweigend vorauszusetzen. Grundlage
für "was ist auf dem System vorhanden": `grounding_seed.scan.scan_resources([...])`
(prüft `shutil.which`) plus `.AI/.MCP/MCP-PROFILE-MANAGEMENT.md` für ellmos-Kandidaten.

### Schritt 6 — Selbstaktualisierung anlegen

Volltext: `references/SELF-UPDATE.md`. Kurzfassung: jeder produzierte Skill bekommt einen
Abschnitt "Selbstaktualisierung", der (a) periodisch eine kurze Web-Recherche vorschlägt,
um bei State-of-the-Art zu bleiben, (b) verwandte Skills/Workflows kennt und neue
Alternativen benennt, die besser passen könnten, (c) eine kleine Lern-JSON mitführt
(Vorlage: `templates/skill-connections.template.json`, Feld `notizen`/`gelernt`), die bei
vorhandener ellmos-Memory-Komponente (USMC/Gardener) ausgelagert werden kann statt lokal
zu wachsen — auch hier: erkennen statt fest verdrahten (`grounding_seed.detect_ecosystem()`).

### Schritt 7 — Registrieren, testen, committen

- Kategorie-Ordner nach `.SKILLS/CLAUDE.md`/`SKILLS-MAP.md` wählen; bei Zweifel `skill-finder`
  oder `controlcenter_find_skill` fragen, ob eine Familie schon existiert.
- `testing/` (privacy_gate + Metadaten-Tests) laufen lassen, bevor committet wird.
- Registry-Dateien (`registry/components.json`, `SKILLS-MAP.md`, `llms.txt`) **nicht von Hand
  editieren** — die werden generiert (`build_public_registry.py`, `build_skills_map.py`,
  `catalog.py`). Läuft im kanonischen Klon gerade eine fremde, uncommittete Session, NICHT
  global regenerieren (mischt fremde und eigene Änderungen in einer Datei) — stattdessen den
  neuen Skill-Ordner isoliert committen und die Registry-Regeneration dem nächsten sauberen
  Lauf (`skill-register-care`) überlassen.
- `git commit -- skills/<kategorie>/<name>/` — nur die eigenen, neuen Pfade.

## Kompatibilität zum Anthropic-Format

Alle Zusatzfelder sind reine YAML-Erweiterungen neben `name`/`description` — ein
Standard-Claude-Code ohne dieses Ökosystem liest weiterhin nur `name`/`description`
und ignoriert den Rest. `config.json`/`connections.json` sind optionale Bundled
Resources (wie in `docs/CONVENTIONS.md` vorgesehen), keine Pflicht-Abhängigkeit —
ein Skill ohne sie funktioniert unverändert.

## Verwandte Skills

- `skill-creator:skill-creator` — generische Interview-/Eval-Schleife (delegiert an, Schritt 1).
- `skill-finder` — Router für vorhandene eigene Skills (VOR dem Bauen prüfen: gibt es das schon?).
- `skill-explorer` — Landschafts-Audit + Web-Recherche nach neuen Skills/Plugins (Meta-Ebene:
  unser Skill-*Bestand*; dieser Skill hier macht stattdessen jeden *einzelnen produzierten*
  Skill selbst anbieterbewusst).
- `skill-family-care`, `skill-register-care` — Pflege nach dem Bauen.
- `grounding-seed` (Modul, `.AI/.MODULES/.CONTROL/grounding-seed`) — die tatsächliche
  Andock-/Selbstversorgungs-Logik, hier nur referenziert, nicht dupliziert.

## Changelog

### 0.1.0 (2026-08-24)
- Erstfassung. Entscheidung Eigenbau statt Fork getroffen und begründet (Ticket
  T-20260824-218233618). Delegiert generische Skill-Erstellung an
  `skill-creator:skill-creator`, ergänzt Haus-Scaffold, ellmos-Prinzipien,
  `grounding-seed`-Anbindung (config.json/connections.json), Vendor-Awareness und
  Selbstaktualisierung.
