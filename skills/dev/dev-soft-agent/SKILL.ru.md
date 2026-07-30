---
name: dev-soft-agent
version: 0.1.0
type: agent
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: Автоматизированный пайплайн разработки программного обеспечения. Сканирует проекты, расставляет приоритеты задач, анализирует код и оркестрирует циклы разработки. Ноль зависимостей (только стандартная библиотека Python).
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [development, code-analysis, task-management, automation, pipeline]
language: ru
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/devSoftAgent', 'origin_version': '0.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="dev-soft-agent banner">
> **Русский** — Официальная русская версия `dev-soft-agent`.

# Dev Soft Agent (Русский)

Автоматизированный пайплайн разработки программного обеспечения. Извлечен из агента ATI платформы BACH,
работает полностью автономно, используя исключительно стандартную библиотеку Python.

## Компоненты

```
scripts/
  config.py              Конфигурация (папки сканирования, префиксы наименований, веса)
  project_manager.py     Сканирование проектов + классификация по соглашению о именовании
  task_engine.py          Парсер TASKS.txt + сканер кода (TODO/FIXME)
  code_analyzer.py       Статический анализ (LOC, импорты, классы, функции)
  dev_loop.py            Оркестратор (DevLoop)
  policies/
    naming.py            Валидация snake_case / PascalCase / SCREAMING_SNAKE
    encoding.py          Обеспечение UTF-8 + обнаружение BOM
    paths.py             Обнаружение жестко зашитых путей (hardcoded paths)
  prompt_templates/
    task_prompt.txt      Промпт LLM для обработки задач
    review_prompt.txt    Промпт LLM для ревью кода
    analysis_prompt.txt  Промпт LLM для анализа проекта
```

## Использование в качестве библиотеки Python

```python
from scripts.dev_loop import DevLoop
from scripts.config import Config

config = Config()
loop = DevLoop(config)

# Сканирование проектов (Русский)
projects = loop.scan_projects()

# Выбор проекта (взвешенный случайный выбор по соглашению об именовании) (Русский)
project = loop.select_project()

# Анализ кода (Русский)
analysis = loop.analyze_project()
print(f"{analysis.total_loc} LOC, {analysis.todo_count} TODOs")

# Загрузка и приоритезация задач (Русский)
tasks = loop.get_tasks()
for task in tasks:
    print(f"[{task.task_type.name}] {task.description} (Prio: {task.priority})")

# Завершение сессии разработки (Русский)
result = loop.run_session()
loop.save_session()
```

## Использование через CLI

```bash
cd scripts
python -m devSoftAgent scan ~/projects
python -m devSoftAgent select
python -m devSoftAgent analyze /path/to/project
python -m devSoftAgent tasks /path/to/project
python -m devSoftAgent session --project my-project
python -m devSoftAgent status
```

## Соглашение об именовании (Классификация проектов)

Проекты классифицируются на основе имени их папки:

| Префикс | Метка | Вес | Значение |
|---------|-------|-----|----------|
| `RDY` | Ready (Готов) | 1.0 | Наивысший приоритет |
| `RDY_FAST` | Fast Ready | 0.5 | Быстрое завершение |
| `FAST` | Fast | 0.33 | Небольшая задача |
| `DEV` | Development | 0.17 | В разработке |
| `REL` | Released | 0.0 | Выпущен, работа не требуется |
| `ARC` | Archived | 0.0 | Заархивирован |

Вес определяет вероятность при случайном выборе.

## Формат TASKS.txt

```markdown
# TASKS - ИмяПроекта (Русский)
# По состоянию на: 2026-03-12 (Русский)

## OPEN
- [ ] [BUG] Описание ошибки
- [ ] [FEATURE] Новая функция

## IN PROGRESS
- [-] [REFACTOR] Реструктуризация кода

## DONE
- [x] [BUG] Исправленная ошибка -- DONE 2026-03-01
```

## Политики (Policies)

Политики качества, которые можно автоматически проверять в коде:

- **NamingPolicy:** snake_case для модулей/функций, PascalCase для классов
- **EncodingPolicy:** Принудительный UTF-8, обнаружение BOM, флаг CRLF
- **PathPolicy:** Обнаружение и отчет о жестко зашитых абсолютных путях

## Журнал изменений

### 0.1.0 (2026-03-12)
- Миграция из MODULAR_AGENTS/devSoftAgent в библиотеку навыков
- Сканер проектов, движок задач, анализатор кода, DevLoop
- 3 политики (именование, кодировка, пути)
- 3 шаблона промптов (задача, ревью, анализ)