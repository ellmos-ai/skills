---
name: plugin-system
version: 1.0.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: "Python अनुप्रयोगों के लिए सामान्य प्लगइन सिस्टम। ऑटो-डिस्कवरी, सत्यापन, दोष सहिष्णुता। शून्य निर्भरताएँ (केवल Python stdlib)।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [plugin, framework, extensibility, cli, architecture]
language: hi
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/plugins', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: a2fea4a34859b7d2e08c4205a368e948ecacdb744e6d80b5d0246271076f3c70
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T12:49:09.130463+00:00"
---
<img src="banner.png" width="100%" alt="plugin-system banner">

# प्लगइन सिस्टम

Python CLI अनुप्रयोगों के लिए दोष-सहिष्णु प्लगइन सिस्टम।
एक दोषपूर्ण प्लगइन एप्लिकेशन के बाकी हिस्से को कभी नहीं रोकता।

## मुख्य विशेषताएँ

- **ऑटो-डिस्कवरी:** किसी डायरेक्टरी में प्लगइन्स को स्वचालित रूप से खोजता है
- **सत्यापन:** हर प्लगइन क्लास पर `name`, `version`, `execute()` की जाँच करता है
- **दोष सहिष्णुता:** दोषपूर्ण प्लगइन्स लॉग किए जाते हैं लेकिन लोड नहीं किए जाते
- **शून्य निर्भरताएँ:** केवल Python मानक लाइब्रेरी

## फ़ाइलें

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

## त्वरित प्रारंभ

### 1. प्लगइन बनाएँ

```python
from plugin_system import PluginBase

class MeinPlugin(PluginBase):
    name = "MeinPlugin"
    version = "1.0.0"

    def execute(self, *args, **kwargs):
        return {"status": "ok", "message": "Hallo!"}
```

### 2. PluginManager का उपयोग करें

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

### 3. अपने ऐप में एकीकृत करें

```python
class MeineApp:
    def __init__(self):
        self.plugins = PluginManager("./plugins")
        self.plugins.discover_plugins()

    def run_command(self, command, **params):
        success, result = self.plugins.execute_plugin(command, **params)
        return result if success else None
```

## प्लगइन इंटरफ़ेस

हर प्लगइन को:

| आवश्यकता | विवरण |
|----------|-------|
| `PluginBase` से इनहेरिट करना होगा | `from plugin_system import PluginBase` |
| `name` सेट करना होगा | क्लास एट्रिब्यूट, खाली नहीं |
| `version` सेट करना होगा | क्लास एट्रिब्यूट, Semantic Versioning |
| `execute()` लागू करना होगा | कोई भी `*args, **kwargs` |

## दोष सहिष्णुता

| दोष का प्रकार | व्यवहार |
|---------------|---------|
| प्लगइन में SyntaxError | प्लगइन छोड़ दिया जाता है, बाकी लोड होता है |
| गायब एट्रिब्यूट | प्लगइन को `is_valid=False` के रूप में चिह्नित किया जाता है |
| `execute()` में अपवाद | `(False, error_message)` लौटाता है |
| डायरेक्टरी में कोई प्लगइन नहीं | खाली सूची, कोई क्रैश नहीं |

## चेंजलॉग

### 1.0.0 (2026-03-12)
- MODULAR_AGENTS/plugins से Skillbibliothek में माइग्रेशन
- PluginBase ABC + PluginManager
- 3 उदाहरण प्लगइन्स (Hello, Calculator, SystemInfo)
- 16+ यूनिट टेस्ट
- argparse के साथ CLI डेमो
