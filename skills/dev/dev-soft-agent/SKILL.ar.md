---
name: dev-soft-agent
version: 0.1.0
type: agent
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: "أداة آلية لخط أنابيب تطوير البرمجيات. تفحص المشاريع، وتحدد أولويات المهام، وتحلل الشيفرة، وتنسق حلقات التطوير. بلا أي تبعيات (مكتبة Python القياسية فقط)."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [development, code-analysis, task-management, automation, pipeline]
language: ar
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/devSoftAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: b4da2d8980df2043e035914acdea3c2074e576a37a180765638d10aed37bc8aa
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.143674+00:00"
---
<img src="banner.png" width="100%" alt="dev-soft-agent banner">

# Dev Soft Agent

خط أنابيب آلي لتطوير البرمجيات. مستخرج من وكيل ATI الخاص بـ BACH، ويعمل بشكل كامل كأداة مستقلة باستخدام مكتبة Python القياسية فقط.

## المكونات

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

## الاستخدام كمكتبة Python

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

## الاستخدام كواجهة سطر الأوامر (CLI)

```bash
cd scripts
python -m devSoftAgent scan ~/projects
python -m devSoftAgent select
python -m devSoftAgent analyze /pfad/zum/projekt
python -m devSoftAgent tasks /pfad/zum/projekt
python -m devSoftAgent session --project mein-projekt
python -m devSoftAgent status
```

## اتفاقية التسمية (تصنيف المشاريع)

يُصنَّف المشروع استنادًا إلى اسم مجلده:

| البادئة | التسمية | الوزن | المعنى |
|--------|-------|---------|-----------|
| `RDY` | Ready | 1.0 | أعلى أولوية |
| `RDY_FAST` | Fast Ready | 0.5 | يمكن إنجازه بسرعة |
| `FAST` | Fast | 0.33 | مهمة صغيرة |
| `DEV` | Development | 0.17 | قيد التطوير |
| `REL` | Released | 0.0 | منجز، لا يوجد عمل |
| `ARC` | Archived | 0.0 | مؤرشف |

يحدد الوزن احتمالية الاختيار عند الاختيار العشوائي.

## تنسيق ملف AUFGABEN.txt

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

## السياسات

سياسات الجودة التي يمكن فحص الشيفرة بها تلقائيًا:

- **NamingPolicy:** snake_case للوحدات والدوال، وPascalCase للأصناف
- **EncodingPolicy:** فرض ترميز UTF-8، واكتشاف BOM، وتمييز CRLF
- **PathPolicy:** اكتشاف المسارات المطلقة المكتوبة يدويًا في الشيفرة والإبلاغ عنها

## سجل التغييرات

### 0.1.0 (2026-03-12)
- ترحيل من MODULAR_AGENTS/devSoftAgent إلى مكتبة المهارات
- ماسح المشاريع، ومحرك المهام، ومحلل الشيفرة، وDevLoop
- 3 سياسات (التسمية، والترميز، والمسارات)
- 3 قوالب توجيهية (المهام، والمراجعة، والتحليل)
