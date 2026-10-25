---
name: plugin-system
version: 1.0.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: "نظام إضافات عام لتطبيقات Python. اكتشاف تلقائي، والتحقق من الصحة، وتحمّل الأعطال. بلا أي تبعيات (مكتبة Python القياسية فقط)."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [plugin, framework, extensibility, cli, architecture]
language: ar
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/plugins', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: a2fea4a34859b7d2e08c4205a368e948ecacdb744e6d80b5d0246271076f3c70
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:03.139962+00:00"
---
<img src="banner.png" width="100%" alt="plugin-system banner">

# نظام الإضافات

نظام إضافات متحمل للأعطال لتطبيقات سطر أوامر Python.
لا يمكن لإضافة معطوبة أن توقف بقية التطبيق أبدًا.

## الميزات الأساسية

- **الاكتشاف التلقائي:** يعثر على الإضافات تلقائيًا داخل مجلد
- **التحقق:** يفحص `name` و`version` و`execute()` في كل صنف إضافة
- **تحمل الأعطال:** تُسجَّل الإضافات المعطوبة في السجل ولا تُحمَّل
- **بلا تبعيات:** مكتبة Python القياسية فقط

## الملفات

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

## البدء السريع

### 1. إنشاء إضافة

```python
from plugin_system import PluginBase

class MeinPlugin(PluginBase):
    name = "MeinPlugin"
    version = "1.0.0"

    def execute(self, *args, **kwargs):
        return {"status": "ok", "message": "Hallo!"}
```

### 2. استخدام PluginManager

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

### 3. الدمج في تطبيقك الخاص

```python
class MeineApp:
    def __init__(self):
        self.plugins = PluginManager("./plugins")
        self.plugins.discover_plugins()

    def run_command(self, command, **params):
        success, result = self.plugins.execute_plugin(command, **params)
        return result if success else None
```

## واجهة الإضافة

يجب أن تقوم كل إضافة بما يلي:

| المتطلب | التفاصيل |
|---------|----------|
| الوراثة من `PluginBase` | `from plugin_system import PluginBase` |
| تعيين `name` | سمة صنف، غير فارغة |
| تعيين `version` | سمة صنف، بالترقيم الدلالي للإصدارات |
| تنفيذ `execute()` | `*args, **kwargs` اختيارية |

## تحمل الأعطال

| نوع العطل | السلوك |
|-----------|--------|
| SyntaxError في الإضافة | تُتخطى الإضافة وتُحمَّل البقية |
| سمات مفقودة | تُوسَم الإضافة بأنها `is_valid=False` |
| استثناء في `execute()` | يعيد `(False, error_message)` |
| لا توجد إضافة في المجلد | قائمة فارغة، دون تعطل |

## سجل التغييرات

### 1.0.0 (2026-03-12)
- ترحيل من MODULAR_AGENTS/plugins إلى مكتبة المهارات
- PluginBase ABC + PluginManager
- 3 إضافات توضيحية (Hello وCalculator وSystemInfo)
- أكثر من 16 اختبار وحدة
- عرض توضيحي لسطر الأوامر باستخدام argparse
