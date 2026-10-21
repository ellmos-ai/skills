---
name: plugin-system
version: 1.0.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: "Sistema genérico de plugins para aplicações Python. Descoberta automática, validação, tolerância a falhas. Zero dependências (apenas biblioteca padrão do Python)."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [plugin, framework, extensibility, cli, architecture]
language: pt
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/plugins', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: a2fea4a34859b7d2e08c4205a368e948ecacdb744e6d80b5d0246271076f3c70
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.388379+00:00"
---
<img src="banner.png" width="100%" alt="plugin-system banner">

# Sistema de Plugins

Sistema de plugins tolerante a falhas para aplicações CLI em Python.
Um plugin defeituoso nunca interrompe o restante da aplicação.

## Funcionalidades principais

- **Descoberta automática:** Encontra plugins automaticamente em um diretório
- **Validação:** Verifica `name`, `version`, `execute()` em cada classe de plugin
- **Tolerância a falhas:** Plugins defeituosos são registrados em log, mas não carregados
- **Zero dependências:** Apenas a biblioteca padrão do Python

## Arquivos

```
scripts/
  plugin_system.py       Kern: PluginBase (ABC) + PluginManager
  cli_demo.py            Demo-CLI mit argparse
  test_plugin_system.py  16+ Unit-Tests
examples/
  hello.py               Hello-World Plugin
  calculator.py          Rechner-Plugin
  systeminfo.py          System-Info Plugin
```

## Início rápido

### 1. Criar um plugin

```python
from plugin_system import PluginBase

class MeinPlugin(PluginBase):
    name = "MeinPlugin"
    version = "1.0.0"

    def execute(self, *args, **kwargs):
        return {"status": "ok", "message": "Hallo!"}
```

### 2. Usar o PluginManager

```python
from plugin_system import PluginManager

manager = PluginManager(plugins_dir="./meine_plugins")
plugins = manager.discover_plugins()

# Alle Plugins auflisten
manager.list_plugins()

# Plugin ausfuehren
success, result = manager.execute_plugin("MeinPlugin", param="wert")
if success:
    print(result)
```

### 3. Integrar à sua própria aplicação

```python
class MeineApp:
    def __init__(self):
        self.plugins = PluginManager("./plugins")
        self.plugins.discover_plugins()

    def run_command(self, command, **params):
        success, result = self.plugins.execute_plugin(command, **params)
        return result if success else None
```

## Interface de plugin

Cada plugin deve:

| Requisito | Detalhes |
|-----------|----------|
| Herdar de `PluginBase` | `from plugin_system import PluginBase` |
| Definir `name` | Atributo de classe, não vazio |
| Definir `version` | Atributo de classe, Versionamento Semântico |
| Implementar `execute()` | Qualquer `*args, **kwargs` |

## Tolerância a falhas

| Tipo de falha | Comportamento |
|---------------|---------------|
| SyntaxError no plugin | O plugin é ignorado, o restante é carregado |
| Atributos ausentes | O plugin é marcado como `is_valid=False` |
| Exceção em `execute()` | Retorna `(False, error_message)` |
| Nenhum plugin no diretório | Lista vazia, sem falhas |

## Changelog

### 1.0.0 (2026-03-12)
- Migração de MODULAR_AGENTS/plugins para a biblioteca de skills
- PluginBase ABC + PluginManager
- 3 plugins de exemplo (Hello, Calculator, SystemInfo)
- 16+ testes unitários
- Demonstração de CLI com argparse
