# branch-header.example.md — Frontmatter-Vorlage für einen Branch-Skill

Dieses Template zeigt das vollständige `provenance`-Frontmatter für einen Branch-Skill.
`{{...}}`-Platzhalter durch echte Werte ersetzen (analog zu den anderen Vorlagen in `assets/`).
Den Block in der kopierten `SKILL.md` in den `provenance:`-Abschnitt eintragen (alte Felder ersetzen).

---

```yaml
---
name: {{original-skill-name}}-fork
version: {{version-des-originals-zum-branch-zeitpunkt}}
type: skill
author: {{bearbeiter}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
description: >
  Branch von {{original-skill-name}}. {{Kurzbeschreibung der Anpassung.}}

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: {{kategorie}}
tags: [{{tags-des-originals}}, branch, fork]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "branch"
  branched_from: "{{original-skill-name}}"
  branch_source_path: "{{~/.claude/plugins/.../skills/original-skill-name/}}"
  origin_repo: "{{repo des originals oder null}}"
  origin_version: "{{version des originals zum branch-zeitpunkt oder null}}"
  branch_date: "{{YYYY-MM-DD}}"
  branch_author: "{{bearbeiter}}"
  branch_reason: "{{grund der anpassung}}"
  last_sync_from_origin: null
---
```

---

**Einsatz:**
1. Original-Verzeichnis vollständig kopieren (inkl. `LICENSE`): `cp -r <quelle>/ <ziel>-fork/`
2. Obigen Block in die kopierte `SKILL.md` eintragen (alten `provenance:`-Abschnitt ersetzen).
3. Nur die Kopie bearbeiten — das Original nie anfassen.
4. Original für die Runtime deregistrieren (`SKILL.md` → `CONTENT.md`) oder Router auf Branch
   zeigen, damit kein Kollisions-Paar entsteht.
5. Branch in `config.json` unter `branches` vermerken (→ `assets/config.example.json`).

Vollständige Anleitung: `references/skill-branching.md`.
