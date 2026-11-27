---
name: encoding-fix
version: 1.0.1
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-11-22
description: "Utilisez cette compétence lorsque des fichiers sont corrompus par un mauvais encodage de caractères (par ex. 'réparer le mojibake', 'accents cassés', 'UTF-8 doublement encodé', /encoding-fix). Corrige les erreurs cp1252, Latin-1 et UTF-8 double/triple encodé sans dépendances ; ne PAS utiliser pour de simples conversions de format sans altération d'encodage."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [encoding, utf-8, mojibake, windows, cp1252, text-repair]
language: fr
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "bach"
  origin_path: "system/tools/encoding_fix.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="encoding-fix banner">

> **Français** — Version française officielle de la compétence `encoding-fix`.

# Encoding Fix — Correction d'encodage

Répare le mojibake (UTF-8 doublement ou triplement encodé) causé par une mauvaise interprétation Windows cp1252/Latin-1. Zéro dépendance — uniquement la bibliothèque standard Python.

## Problème typique

```
"ü" (U+00FC) → UTF-8 \xc3\xbc → lu comme cp1252 → "Ã¼"
```

## Utilisation

### En tant que bibliothèque
```python
from encoding_fix import sanitize_outbound

clean = sanitize_outbound("WÃ¼rge")  # → "Würge"
```

### Sortie de sous-processus
```python
from encoding_fix import sanitize_subprocess_output

text = sanitize_subprocess_output(process.stdout)
```

### CLI
```bash
python encoding_fix.py "WÃ¼rge"    # Vérifier une chaîne isolée
python encoding_fix.py              # Auto-test
```

## Fonctionnalités

- **Idempotent :** Un texte correctement encodé n'est pas modifié
- **Jusqu'à 3 passes :** Répare aussi les chaînes triplement encodées
- **Décodeur de sous-processus :** Repli UTF-8/cp1252 pour les sorties de processus
- **Zéro dépendance :** Uniquement la bibliothèque standard Python

## Journal des modifications

### 1.0.1 (2026-11-22)
- Indication de langue corrigée

### 1.0.0 (2026-03-12)
- Porté depuis BACH `system/tools/encoding_fix.py`
