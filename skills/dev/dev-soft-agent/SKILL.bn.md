---
name: dev-soft-agent
version: 0.1.0
type: agent
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: "স্বয়ংক্রিয় সফটওয়্যার উন্নয়ন পাইপলাইন। প্রকল্প স্ক্যান করে, কাজের অগ্রাধিকার নির্ধারণ করে, কোড বিশ্লেষণ করে এবং উন্নয়ন লুপ পরিচালনা করে। শূন্য নির্ভরতা (শুধুমাত্র Python স্ট্যান্ডার্ড লাইব্রেরি)।"
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [development, code-analysis, task-management, automation, pipeline]
language: bn
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/devSoftAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
translated_from_sha256: b4da2d8980df2043e035914acdea3c2074e576a37a180765638d10aed37bc8aa
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.795701+00:00"
---
<img src="banner.png" width="100%" alt="dev-soft-agent banner">

# Dev Soft Agent

স্বয়ংক্রিয় সফটওয়্যার উন্নয়ন পাইপলাইন। BACH-এর ATI-Agent থেকে নিষ্কাশিত, এবং সম্পূর্ণ স্বতন্ত্রভাবে শুধুমাত্র Python স্ট্যান্ডার্ড লাইব্রেরি দিয়ে চলে।

## উপাদানসমূহ

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

## Python লাইব্রেরি হিসেবে ব্যবহার

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

## CLI হিসেবে ব্যবহার

```bash
cd scripts
python -m devSoftAgent scan ~/projects
python -m devSoftAgent select
python -m devSoftAgent analyze /pfad/zum/projekt
python -m devSoftAgent tasks /pfad/zum/projekt
python -m devSoftAgent session --project mein-projekt
python -m devSoftAgent status
```

## নামকরণ নিয়ম (প্রকল্প শ্রেণীবিভাগ)

প্রকল্পগুলোকে তাদের ফোল্ডারের নামের ভিত্তিতে শ্রেণীবদ্ধ করা হয়:

| প্রিফিক্স | লেবেল | ওজন | অর্থ |
|--------|-------|-----------|---------|
| `RDY` | Ready | 1.0 | সর্বোচ্চ অগ্রাধিকার |
| `RDY_FAST` | Fast Ready | 0.5 | দ্রুত সম্পন্নযোগ্য |
| `FAST` | Fast | 0.33 | ছোট কাজ |
| `DEV` | Development | 0.17 | উন্নয়নাধীন |
| `REL` | Released | 0.0 | সম্পন্ন, কোনো কাজ নেই |
| `ARC` | Archived | 0.0 | আর্কাইভ করা |

ওজন এলোমেলো নির্বাচনের সম্ভাব্যতা নির্ধারণ করে।

## AUFGABEN.txt ফরম্যাট

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

## নীতিসমূহ (Policies)

স্বয়ংক্রিয়ভাবে কোডের বিরুদ্ধে পরীক্ষা করা যায় এমন গুণগত মানের নীতি:

- **NamingPolicy:** মডিউল/ফাংশনের জন্য snake_case, ক্লাসের জন্য PascalCase
- **EncodingPolicy:** UTF-8 বাধ্যতামূলক করা, BOM শনাক্ত করা, CRLF চিহ্নিত করা
- **PathPolicy:** হার্ডকোড করা পরম (absolute) পাথ শনাক্ত ও রিপোর্ট করা

## Changelog

### 0.1.0 (2026-03-12)
- MODULAR_AGENTS/devSoftAgent থেকে Skillbibliothek-এ মাইগ্রেশন
- প্রকল্প স্ক্যানার, টাস্ক ইঞ্জিন, কোড অ্যানালাইজার, DevLoop
- ৩টি নীতি (Naming, Encoding, Paths)
- ৩টি প্রম্পট টেমপ্লেট (Task, Review, Analysis)
