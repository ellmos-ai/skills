---
name: skill-family-care
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: "Skill de maintenance qui maintient les familles de skills à jour, sans lancer l'audit complet du skill-explorer. Utilisez ce skill lorsqu'un nouveau skill doit être rattaché à la bonne famille, lorsqu'un routeur d'en-tête de famille doit être mis à jour après un changement de famille, ou lorsqu'un routeur orphelin doit être supprimé. Déclenchez-le également pour « maintenir les familles », « rattacher un nouveau skill à une famille », « mettre à jour les routeurs », « définir/supprimer les en-têtes de famille »."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, familien, pflege, routing, meta]
language: fr
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [skill-explorer, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-family-care/"
  origin_version: "0.1.0"
translated_from_sha256: b4d39973bb0e97c3190c0f821fe0a351a0f338cdfd1ea6fff26d44d1ca476c21
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:32:13.529594+00:00"
---
<img src="banner.png" width="100%" alt="skill-family-care banner">
# Maintenance des familles de skills

## Objectif

Maintient à jour les **familles** de skills, sans l'exécution complète de l'audit de `skill-explorer`. Extrait selon le principe de l'installateur (sous-skill léger plutôt que monolithe). Référence les scripts de `skill-explorer`, sans les copier.

## Sources (ne pas dupliquer)

- **Liste des familles :** `<USER_HOME>\OneDrive\.USR\SKILL-MAP.md` (carte canonique des familles et du routage).
- **Inventaire (état actuel) :** `skill-explorer/scripts/inventory_skills.py`.
- **Définir/supprimer les routeurs :** `skill-explorer/scripts/inject_family_header.py`.
- **Configuration (familles liées) :** `~/.claude/skills/skill-explorer/config.json`.

## Tâches

### A — Rattacher un nouveau skill à une famille
1. Refaire l'inventaire :
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
2. Choisir la famille appropriée dans `SKILL-MAP.md` (axes : phase/largeur/rigidité/effet/matière première).
3. Inscrire le skill comme membre dans `config.json` (`families[<fam>].members`) et dans `SKILL-MAP.md`.

### B — Mettre à jour le routeur d'en-tête après un changement de famille
```bash
PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inject_family_header.py \
    --family <Familie> --skills s1,s2,s3 --router "<Wegweiser>" --inventory ~/.skill-inventory.json
```
- Idempotent : un bloc existant de la même famille est remplacé.
- Seuls les skills `editable`/`source=user` sont modifiés (contrôle dans le script).

### C — Supprimer un routeur orphelin
Même script avec `--remove` (`--router` non nécessaire).

## Règles absolues

- **Inspection ≠ modification :** seuls les skills propres à l'utilisateur reçoivent un en-tête. Ne jamais toucher aux plugins ni aux skills externes.
- Après chaque modification, mettre à jour `config.json` (`families[*].linked`, `updated`).
- Ne jamais copier de contenu de la carte des familles dans les skills individuels — uniquement le bloc de renvoi.

## Journal des modifications

### 0.1.0 (2026-06-17)
- Version initiale. Générée par le mode audit (P1).
