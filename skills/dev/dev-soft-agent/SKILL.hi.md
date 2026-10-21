---
name: dev-soft-agent
version: 0.1.0
type: agent
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: "स्वचालित सॉफ़्टवेयर विकास पाइपलाइन। प्रोजेक्ट्स को स्कैन करती है, कार्यों को प्राथमिकता देती है, कोड का विश्लेषण करती है, और विकास लूप का समन्वय करती है। शून्य निर्भरताएँ (केवल Python stdlib)।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [development, code-analysis, task-management, automation, pipeline]
language: hi
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/devSoftAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: b4da2d8980df2043e035914acdea3c2074e576a37a180765638d10aed37bc8aa
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.763812+00:00"
---
<img src="banner.png" width="100%" alt="dev-soft-agent banner">

# Dev Soft Agent

BACH के ATI-एजेंट से निकाली गई स्वचालित सॉफ़्टवेयर-विकास पाइपलाइन। पूरी तरह स्वतंत्र रूप से केवल शुद्ध Python मानक पुस्तकालय के साथ चलती है।

## घटक

```
scripts/
  config.py              Konfiguration (Scan-Ordner, Naming-Prefixes, Gewichte)
  project_manager.py     Projekt-Scan + Klassifizierung nach Naming-Konvention
  task_engine.py          AUFGABEN.txt Parser + Code-Scanner (TODO/FIXME)
  code_analyzer.py       Statische Analyse (LOC, Imports, Klassen, Funktionen)
  dev_loop.py            Orchestrator (DevLoop)
  policies/
    naming.py            snake_case / PascalCase / SCREAMING_SNAKE Pruefung
    encoding.py          UTF-8 Enforcement + BOM Detection
    paths.py             Hardcoded-Path-Erkennung
  prompt_templates/
    task_prompt.txt      LLM-Prompt fuer Task-Bearbeitung
    review_prompt.txt    LLM-Prompt fuer Code-Review
    analysis_prompt.txt  LLM-Prompt fuer Projekt-Analyse
```

## Python लाइब्रेरी के रूप में उपयोग

```python
from scripts.dev_loop import DevLoop
from scripts.config import Config

config = Config()
loop = DevLoop(config)

# Projekte scannen
projects = loop.scan_projects()

# Projekt auswaehlen (gewichtete Zufallsauswahl nach Naming-Konvention)
project = loop.select_project()

# Code analysieren
analysis = loop.analyze_project()
print(f"{analysis.total_loc} LOC, {analysis.todo_count} TODOs")

# Tasks laden und priorisieren
tasks = loop.get_tasks()
for task in tasks:
    print(f"[{task.task_type.name}] {task.description} (Prio: {task.priority})")

# Komplette Dev-Session
result = loop.run_session()
loop.save_session()
```

## CLI के रूप में उपयोग

```bash
cd scripts
python -m devSoftAgent scan ~/projects
python -m devSoftAgent select
python -m devSoftAgent analyze /pfad/zum/projekt
python -m devSoftAgent tasks /pfad/zum/projekt
python -m devSoftAgent session --project mein-projekt
python -m devSoftAgent status
```

## नामकरण-परंपरा (प्रोजेक्ट वर्गीकरण)

प्रोजेक्ट्स को उनके फ़ोल्डर-नाम के आधार पर वर्गीकृत किया जाता है:

| उपसर्ग | लेबल | भार | अर्थ |
|--------|-------|---------|-----------|
| `RDY` | Ready | 1.0 | सर्वोच्च प्राथमिकता |
| `RDY_FAST` | Fast Ready | 0.5 | जल्दी पूरा होने योग्य |
| `FAST` | Fast | 0.33 | छोटा कार्य |
| `DEV` | Development | 0.17 | विकासाधीन |
| `REL` | Released | 0.0 | पूर्ण, कोई कार्य शेष नहीं |
| `ARC` | Archived | 0.0 | संग्रहीत |

भार यादृच्छिक चयन में संभावना निर्धारित करता है।

## AUFGABEN.txt प्रारूप

```markdown
# AUFGABEN - Projektname
# Stand: 2026-03-12

## OFFEN
- [ ] [BUG] Beschreibung des Fehlers
- [ ] [FEATURE] Neues Feature

## IN ARBEIT
- [-] [REFACTOR] Code-Umbau

## ERLEDIGT
- [x] [BUG] Behobener Fehler -- DONE 2026-03-01
```

## नीतियाँ

गुणवत्ता नीतियाँ जिनकी कोड के विरुद्ध स्वचालित जाँच की जा सकती है:

- **NamingPolicy:** मॉड्यूल/फ़ंक्शन के लिए snake_case, क्लास के लिए PascalCase
- **EncodingPolicy:** UTF-8 लागू करना, BOM पहचानना, CRLF चिह्नित करना
- **PathPolicy:** हार्डकोडेड निरपेक्ष पथों को पहचानना और रिपोर्ट करना

## चेंजलॉग

### 0.1.0 (2026-03-12)
- MODULAR_AGENTS/devSoftAgent से कौशल-पुस्तकालय में माइग्रेशन
- प्रोजेक्ट-स्कैनर, टास्क-इंजन, कोड-विश्लेषक, DevLoop
- 3 नीतियाँ (नामकरण, एन्कोडिंग, पथ)
- 3 प्रॉम्प्ट-टेम्पलेट (कार्य, समीक्षा, विश्लेषण)
