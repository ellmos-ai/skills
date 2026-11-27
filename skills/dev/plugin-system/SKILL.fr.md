---
name: plugin-system
version: 1.0.1
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-11-22
description: "À utiliser lorsqu'une application Python doit être dotée d'une architecture de plugins dynamique et tolérante aux pannes avec détection automatique (ex. 'implémenter un système de plugins', 'charger des plugins dynamiquement', 'extensibilité pour outil', /plugin-system). Fournit une architecture modulaire propre et extensible sans dépendances externes. Ne PAS utiliser pour l'audit de sécurité de plugins tiers (utiliser dev/sec-supplychain)."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [plugin, framework, extensibility, cli, architecture]
language: fr
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/plugins', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---


<img src="banner.png" width="100%" alt="plugin-system banner">

> **Français** — Version française officielle de la compétence `plugin-system`.

# Système de Plugins

Système de plugins tolérant aux pannes pour les applications CLI en Python.
Un plugin défectueux n'interrompt jamais le reste de l'application.

## Fonctionnalités clés

- **Découverte automatique (Auto-Discovery) :** détecte automatiquement les plugins dans un répertoire
- **Validation :** vérifie `name`, `version`, `execute()` sur chaque classe de plugin
- **Tolérance aux pannes :** les plugins défectueux sont journalisés mais ne sont pas chargés
- **Zéro dépendance :** uniquement la bibliothèque standard Python

## Fichiers

```
scripts/
  plugin_system.py       Cœur : PluginBase (ABC) + PluginManager
  cli_demo.py            CLI de démonstration avec argparse
  test_plugin_system.py  16+ tests unitaires
examples/
  hello.py               Plugin Hello-World
  calculator.py          Plugin calculatrice
  systeminfo.py          Plugin informations système
```

## Démarrage rapide

### 1. Créer un plugin

```python
from plugin_system import PluginBase

class MonPlugin(PluginBase):
    name = "MonPlugin"
    version = "1.0.0"

    def execute(self, *args, **kwargs):
        return {"status": "ok", "message": "Bonjour !"}
```

### 2. Utiliser PluginManager

```python
from plugin_system import PluginManager

manager = PluginManager(plugins_dir="./mes_plugins")
plugins = manager.discover_plugins()

# Lister tous les plugins
manager.list_plugins()

# Exécuter un plugin
success, result = manager.execute_plugin("MonPlugin", param="valeur")
if success:
    print(result)
```

### 3. Intégrer dans votre propre application

```python
class MonApplication:
    def __init__(self):
        self.plugins = PluginManager("./plugins")
        self.plugins.discover_plugins()

    def run_command(self, command, **params):
        success, result = self.plugins.execute_plugin(command, **params)
        return result if success else None
```

## Interface de plugin

Chaque plugin doit :

| Exigence | Détails |
|----------|---------|
| Hériter de `PluginBase` | `from plugin_system import PluginBase` |
| Définir `name` | Attribut de classe, non vide |
| Définir `version` | Attribut de classe, versionnage sémantique |
| Implémenter `execute()` | Accepte `*args, **kwargs` quelconques |

## Tolérance aux pannes

| Type d'erreur | Comportement |
|---------------|--------------|
| `SyntaxError` dans le plugin | Le plugin est ignoré, le reste se charge |
| Attributs manquants | Le plugin est marqué `is_valid=False` |
| Exception dans `execute()` | Retourne `(False, error_message)` |
| Aucun plugin dans le dossier | Liste vide, aucun plantage |

## Journal des modifications

### 1.0.1 (2026-11-22)
- Mention linguistique corrigée.

### 1.0.0 (2026-03-12)
- Migration depuis `MODULAR_AGENTS/plugins` vers la bibliothèque de compétences
- `PluginBase` (ABC) + `PluginManager`
- 3 plugins d'exemple (Hello, Calculator, SystemInfo)
- 16+ tests unitaires
- CLI de démonstration avec `argparse`
