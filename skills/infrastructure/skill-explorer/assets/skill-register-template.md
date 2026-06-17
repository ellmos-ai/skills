---
name: skill-register
version: 0.1.0
type: skill
author: {{author}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
description: >
  Inhaltsverzeichnis aller lokalen Skills unter ~/.claude/skills/. Aktiviert sich bei „welche Skills
  habe ich", „Skill-Liste", „Skill-Register", oder wenn kein Skill direkt passt und ein Überblick
  nötig ist. Verweist auf die Live-Datei jedes Skills (echte Anleitung steht dort, nicht hier).

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, index, register, discovery, meta]
language: de
status: active

dependencies:
  tools: []
  services: []
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-register/"
  origin_version: "0.1.0"
---

# Skill-Register

> NUR anlegen, wenn auf dem System KEIN Register existiert. Auf bestehenden Systemen stattdessen
> `code-skill-index` + `<skill register: index>` + `.USR/the family map` erweitern.

Bridge zur lokalen Skill-Sammlung. Liefert nur die Liste — der echte Inhalt liegt in den Live-Dateien
`~/.claude/skills/<name>/SKILL.md`.

## Pflichtablauf

Wenn ein Wunsch zu einem gelisteten Skill passt: zuerst die Live-Datei lesen (Beschreibungen hier sind
Momentaufnahmen), dann der Anleitung folgen.

## Index (nach Familie)

<!-- Generiert/aktualisiert aus inventory_skills.py. Pro Familie eine Tabelle. -->

### Familie: {{Familie}}
| Skill | Pfad | Kurzbeschreibung |
|-------|------|------------------|
| `{{skill}}` | `~/.claude/skills/{{skill}}/SKILL.md` | {{kurz}} |

## Aktualisierung

Bei Bestandsänderung neu erzeugen via `inventory_skills.py` (aus `skill-explorer`) und diese Tabellen
ersetzen. Pflege automatisierbar über den Subskill `skill-register-care` (siehe `skill-explorer`).
