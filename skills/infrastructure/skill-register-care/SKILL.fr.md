---
name: skill-register-care
version: 0.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-09-20
description: "Skill de maintenance qui garde le registre à trois volets cohérent (catalogues par catégorie code-skill-index, index des Skills, carte SKILL-MAP des familles et du routage). Utilise ce skill pour une vérification de dérive entre l'inventaire réel des Skills et le registre documenté : signaler les entrées manquantes ou en trop, corriger les compteurs, définir la date d'état. Se déclenche aussi pour « Maintenir le registre des Skills », « Mettre à jour l'index », « Vérifier la dérive du registre », « quels Skills manquent dans la carte »."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, register, index, drift, pflege, meta]
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
  origin_path: "~/.claude/skills/skill-register-care/"
  origin_version: "0.2.0"
translated_from_sha256: 6a187b857227bb33edb71c82f4b992a376877192b746a6eea17458e9819cae46
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T20:52:38.401999+00:00"
---
<img src="banner.png" width="100%" alt="skill-register-care banner">
# Skill-Register-Care

## Objectif

Garde le **registre** exempt de dérive. Le registre se compose de trois artefacts imbriqués : ne jamais en créer un quatrième, toujours étendre ces trois-là :

| Artefact | Rôle | Maintenance |
|---|---|---|
| `~/.claude/skills/code-skill-index/references/catalog-*.md` | Catalogues par catégorie | géré à la main, travail manuel |
| `<USER_HOME>/OneDrive/.SYNC/CLAUDE-CODE-SKILLS.md` | Index inter-systèmes (unique vue des Skills pour Claude Desktop) | **automatisé**, voir ci-dessous |
| `<USER_HOME>/OneDrive/.USR/SKILL-MAP.md` | Carte des familles et du routage | géré à la main, travail manuel |

## Automatisé : l'index inter-systèmes

L'index n'est **plus** complété à la main : cela l'avait laissé à l'arrêt pendant trois mois (état au 21.06. face à 152 Skills réels au 20.09.2026 ; 81 manquaient). À la place :

```bash
PYTHONIOENCODING=utf-8 python "<USER_HOME>/OneDrive/.SYNC/scripts/skill_index_care.py" --check
PYTHONIOENCODING=utf-8 python "<USER_HOME>/OneDrive/.SYNC/scripts/skill_index_care.py" --apply
```

Il s'exécute de toute façon comme **étape 2b du `/sync` quotidien** ; ici, manuellement uniquement lorsque des Skills viennent d'être créés ou déployés et que l'index doit être à jour immédiatement. L'exécution est additive et idempotente : les descriptions courtes sélectionnées sont conservées, les Skills manquants sont classés par catégorie de bibliothèque, les entrées sans `SKILL.md` en service sont **marquées au lieu d'être supprimées**.

## Procédure de vérification de dérive (les deux registres gérés à la main)

1. **Relever l'état réel :**
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
   Seuls les Skills `source=user` sont pertinents pour le registre (les plugins et externes restent exclus).
2. **Lire l'état attendu :** les trois artefacts du registre.
3. **Établir l'écart :**
   - **Manquant** (dans l'inventaire, absent du registre) → ajouter.
   - **Orphelin** (dans le registre, plus dans l'inventaire) → **vérifier d'abord, juger ensuite.**
     Un dossier de Skill dont le `SKILL.md` a été renommé en `CONTENT.md` est *désenregistré* : volontairement non chargé comme Skill, mais contenu présent et accessible via `code-skill-index`. L'inventaire ne le compte pas ; il ne doit pas pour autant être supprimé. Le marquer. Ne le retirer réellement que si le dossier a disparu.
   - **Écart de compteur** (p. ex. « 18 Skills » ne correspond plus) → corriger le nombre.
4. **Ajouter :** pour chaque nouveau Skill, une ligne dans le `catalog-<kategorie>.md` approprié, une ligne dans l'index des Skills (+ date d'en-tête) et, si la famille est nouvelle ou modifiée, une section dans `SKILL-MAP.md`.
5. **Date d'état** : dans tous les fichiers touchés, la mettre à la date du jour.

## Extrait utilitaire (lister les Skills user manquants)

```bash
PYTHONIOENCODING=utf-8 python -c "
import json
inv=json.load(open('<USER_HOME>/.skill-inventory.json',encoding='utf-8'))
print('\n'.join(s['dir'] for s in inv['skills'] if s['source']=='user'))
"
```
Comparer la sortie avec les artefacts du registre (manuellement ou via grep).

## Règles impératives

- **Pas de quatrième registre** : étendre uniquement les trois.
- Seuls les Skills écrits par l'utilisateur appartiennent au registre ; les Skills tiers suivent le chemin externe.
- Ne pas deviner la date : mettre la date du jour.
- Ne **pas** tenir l'index inter-systèmes **à la main** ; lancer `skill_index_care.py`. Quiconque y ajoute manuellement des lignes prépare la prochaine dérive silencieuse.

## Journal des modifications

### 0.2.0 (2026-09-20)
- L'index inter-systèmes `CLAUDE-CODE-SKILLS.md` a été migré vers `.SYNC/scripts/skill_index_care.py` (additif, marquant, idempotent) et intégré comme étape 2b dans le `/sync` quotidien. Raison : l'index était à l'arrêt depuis le 2026-06-21 ; 81 Skills locaux manquaient, 15 entrées pointaient sans marquage vers des procédures désenregistrées, et une vers un dossier sans `SKILL.md`.
- « Orphelin » précisé : les Skills désenregistrés (`CONTENT.md` au lieu de `SKILL.md`) sont marqués, non supprimés ; sinon, lors du rattrapage, 15 entrées gérées à la main auraient été effacées.

### 0.1.0 (2026-06-17)
- Version initiale. Générée par le mode Audit (P2). Raison : lors de l'audit du 2026-06-17, environ 10 Skills user manquaient dans la SKILL-MAP (swarm-operations, model-strategy, agents-bridge, mcp-config-sync, system-onboarding, update-cli-docs, migrate-rename, plugin-system, ainsi que les familles Thérapie et Game-Dev).
