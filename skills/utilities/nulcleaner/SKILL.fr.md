---
name: nulcleaner
version: 1.0.1
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-11-22
description: "Utilisez cette compétence pour trouver et supprimer les fichiers réservés Windows NUL créés lors de l'utilisation de /dev/null dans Git Bash. Fonctionne en mode headless ou avec interface graphique."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [windows, nul, cleanup, git-bash, filesystem]
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
  origin_path: "system/tools/nulcleaner.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="nulcleaner banner">

> **Français** — Version française officielle de la compétence `nulcleaner`.

# nulcleaner — Nettoyage des fichiers NUL sous Windows

## Le problème

Lorsqu'on utilise `/dev/null` dans des commandes sous Git Bash sur Windows (par ex. `> /dev/null`), au lieu d'une redirection vers le vide, un véritable **fichier nommé `nul`** est créé dans le répertoire courant. Windows réserve « NUL » comme nom de périphérique, si bien que ces fichiers ne peuvent pas être supprimés normalement.

Cet outil détecte et supprime ces fichiers NUL via le chemin UNC étendu (`\\?\`).

---

## Modes

| Mode | Description |
|------|-------------|
| `scan` | Parcourir récursivement un répertoire à la recherche de fichiers NUL |
| `delete` | Détecter et supprimer les fichiers NUL |
| `gui` | Interface graphique avec sélection de fichiers |

---

## Utilisation CLI

```bash
# Uniquement scanner (affiche les fichiers NUL trouvés)
python nulcleaner.py scan /chemin/vers/repertoire

# Scanner et supprimer
python nulcleaner.py delete /chemin/vers/repertoire

# Lancer le mode GUI
python nulcleaner.py gui
```

---

## API headless (pour intégration)

L'outil propose également une API Python pour un fonctionnement sans interface graphique :

```python
from nulcleaner import clean_nul_files_headless

result = clean_nul_files_headless("/chemin/vers/repertoire", verbose=True)
print(f"Trouvés : {result['found']}, Supprimés : {result['deleted']}")
```

**Valeur de retour :** `{'found': int, 'deleted': int, 'errors': list}`

---

## Détails techniques

- Utilise le chemin UNC étendu (`\\?\`) pour supprimer les noms de fichiers réservés sous Windows
- Parcours récursif avec `os.walk()`
- Interface graphique avec `tkinter` (aucune dépendance externe)
- Ne fonctionne que sous Windows (là où survient le problème)

---

## Prévention

Le mieux est d'éviter `/dev/null` dans Git Bash. À la place :
- Simplement omettre la sortie
- Utiliser `2>&1` pour la redirection de `stderr`
- Veiller à la compatibilité Windows dans les scripts shell

## Journal des modifications

### 1.0.1 (2026-11-22)
- Indication de langue corrigée
