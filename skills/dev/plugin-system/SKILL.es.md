---
name: plugin-system
version: 1.0.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: Sistema de plugins genérico para aplicaciones Python. Detección automática, validación, tolerancia a fallos. Sin dependencias externas (solo biblioteca estándar de Python).
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [plugin, framework, extensibility, cli, architecture]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/plugins', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **Español** — Versión oficial en español de `plugin-system`.


# Plugin System (Español)

Sistema de plugins tolerante a fallos para aplicaciones CLI en Python.
Un plugin defectuoso nunca detiene el resto de la aplicación.

## Características principales

- **Detección automática (Auto-Discovery):** Encuentra automáticamente plugins en un directorio
- **Validación:** Comprueba `name`, `version`, `execute()` en cada clase de plugin
- **Tolerancia a fallos:** Los plugins defectuosos se registran en el log pero no se cargan
- **Sin dependencias externas:** Solo utiliza la biblioteca estándar de Python

## Archivos

```
scripts/
  plugin_system.py       Núcleo: PluginBase (ABC) + PluginManager
  cli_demo.py            CLI de demostración con argparse
  test_plugin_system.py  16+ pruebas unitarias
examples/
  hello.py               Plugin de demostración Hola Mundo
  calculator.py          Plugin de calculadora
  systeminfo.py          Plugin de información del sistema
```

## Inicio rápido

### 1. Crear un plugin

```python
from plugin_system import PluginBase

class MyPlugin(PluginBase):
    name = "MyPlugin"
    version = "1.0.0"

    def execute(self, *args, **kwargs):
        return {"status": "ok", "message": "Hello!"}
```

### 2. Usar PluginManager

```python
from plugin_system import PluginManager

manager = PluginManager(plugins_dir="./my_plugins")
plugins = manager.discover_plugins()

# Listar todos los plugins
manager.list_plugins()

# Ejecutar un plugin
success, result = manager.execute_plugin("MyPlugin", param="value")
if success:
    print(result)
```

### 3. Integrar en tu aplicación

```python
class MyApp:
    def __init__(self):
        self.plugins = PluginManager("./plugins")
        self.plugins.discover_plugins()

    def run_command(self, command, **params):
        success, result = self.plugins.execute_plugin(command, **params)
        return result if success else None
```

## Interfaz de plugin

Todo plugin debe cumplir con lo siguiente:

| Requisito | Detalles |
|-------------|---------|
| Heredar de `PluginBase` | `from plugin_system import PluginBase` |
| Definir `name` | Atributo de clase, no vacío |
| Definir `version` | Atributo de clase, versionado semántico |
| Implementar `execute()` | Acepta `*args, **kwargs` arbitrarios |

## Tolerancia a fallos

| Tipo de error | Comportamiento |
|-----------|----------|
| `SyntaxError` en el plugin | El plugin se omite, el resto se carga |
| Atributos faltantes | El plugin se marca como `is_valid=False` |
| Excepción en `execute()` | Devuelve `(False, error_message)` |
| Ningún plugin en el directorio | Lista vacía, sin caídas del sistema |

## Historial de cambios

### 1.0.0 (2026-03-12)
- Migración desde MODULAR_AGENTS/plugins a la biblioteca de habilidades
- PluginBase ABC + PluginManager
- 3 plugins de ejemplo (Hello, Calculator, SystemInfo)
- Más de 16 pruebas unitarias
- CLI de demostración con argparse