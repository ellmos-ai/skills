---
name: project-onboarding
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Стандартная процедура онбординга новых программных проектов: анализ функций, проверка качества кода, чек-лист и создание задач.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [onboarding, project, intake, analysis, checklist, code-review]
language: ru
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/projekt-aufnahme.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **Русский** — Официальная русская версия `project-onboarding`.


# Стандартная процедура онбординга для новых программных проектов (Русский)

**Версия:** 1.0
**Дата:** 2026-03-12

---

## Обзор и назначение

Эта процедура определяет шаги, которые необходимо выполнить для недавно обнаруженных папок с программным обеспечением перед их добавлением в систему управления задачами.

```
+─────────────────────────────────────────────────────+
|           STANDARD ONBOARDING PROCEDURE              |
+─────────────────────────────────────────────────────+
|  1. Create feature analysis                          |
|  2. Code quality review (standard tests)             |
|  3. Create TASKS.txt                                 |
|  4. Add to task management                           |
+─────────────────────────────────────────────────────+
```

---

## Фаза 1: Анализ функций

**Назначение:** Понять инструмент, его функции и статус разработки.

**Создать файл:** `Feature_Analysis_<ToolName>.md`

### Шаблон

```markdown
# Feature Analysis: <ToolName> (Deutsch)

## Brief Description
A short sentence describing what the tool does.

---

## Highlights

| Feature | Description |
|---------|-------------|
| **Feature 1** | Description |
| **Feature 2** | Description |

---

## Development Stage Assessment

### Current Status: **<Status> (<X>%)**

Possible statuses:
- Prototype (0-30%)
- Alpha (30-60%)
- Beta (60-85%)
- Production Ready (85-95%)
- Release (95-100%)

| Category | Rating (1-5) | Details |
|----------|:------------:|---------|
| **Functionality** | 3 | |
| **UI/UX** | 3 | |
| **Stability** | 3 | |
| **Documentation** | 3 | |

---

## Recommended Extensions

### Priority: High
1. ...

### Priority: Medium
2. ...

### Priority: Low
3. ...

---

## Technical Details

Framework:      <Framework>
File size:      <X> lines of Python
Main file:      <main.py>

---

*Analysis created: <Date>*
```

---

## Фаза 2: Проверка качества кода

**Назначение:** Обеспечить техническое качество, выявить известные проблемы.

### Рекомендуемые проверки

| Тест | Инструмент | Описание |
|------|------------|----------|
| **Кодировка** | Проверка кодировки (например, `chardet`, `file`) | Обеспечить UTF-8 |
| **Анализ методов** | Линтер (например, `pylint`, `flake8`) | Найти крупные методы |
| **Отступы** | Форматировщик (например, `black`, `autopep8`) | Проверить согласованность |
| **Импорты** | Проверка импортов (например, `isort`, `pylint`) | Найти неиспользуемые импорты |

### Контрольные точки

- [ ] Все файлы .py закодированы в UTF-8?
- [ ] Нет неоправданно больших методов (>100 строк)?
- [ ] Согласованные отступы (пробелы или табуляция)?
- [ ] Неиспользуемые импорты удалены?
- [ ] Присутствуют ли docstring?

### Документирование результатов

Записать проблемы в TASKS.txt в разделе "QUALITY REVIEW".

---

## Фаза 3: Создание TASKS.txt

**Назначение:** Фиксация открытых задач в структурированном формате.

**Создать файл:** `TASKS.txt` в папке проекта

### Шаблон

```
TASKS - <ToolName> V<Version>
==============================
Status: <Status>
Date: <Date>

OPEN TASKS:
[ ] <Task 1> - Effort: <LOW|MEDIUM|HIGH>
[ ] <Task 2> - Effort: <LOW|MEDIUM|HIGH>

---
DONE (Archive):
- <Completed task> (<Version>, <Date>)
```

### Значения статусов

| Статус | Значение |
|--------|----------|
| NEWLY DISCOVERED | Еще не проанализировано |
| ANALYSIS NEEDED | Выполняется анализ функций |
| QUALITY REVIEW | Выполняются тесты кода |
| VALIDATED & READY | Готово к разработке функций |
| MVP | Минимально жизнеспособный продукт |
| BUILD ONLY | Требуется только сборка |
| BLOCKED | Ожидание тестирования/решения пользователя |

---

## Фаза 4: Интеграция с системой управления задачами

После завершения фаз 1-3:

1. **Перенос задач:** Создать записи из TASKS.txt в качестве задач/issue
2. **Проверка:** Все ли задачи правильно категоризированы?
3. **Категоризация:** Назначить проекту соответствующую категорию (отдельный инструмент, пакет, библиотека и т. д.)

### Автоматические задачи онбординга

Для новых проектов создайте следующие стандартные задачи:

| Задача | Описание | Трудоемкость |
|--------|----------|--------------|
| onb_1 | Создать анализ функций | средняя |
| onb_2 | Проверка качества кода | низкая |
| onb_3 | Создать TASKS.txt | низкая |

Задачи имеют зависимости: onb_2 зависит от onb_1, onb_3 зависит от onb_2.

---

## Быстрый чек-лист

```
[ ] 1. Feature_Analysis_<Name>.md created
[ ] 2. Code quality review completed (linter, encoding, imports)
[ ] 3. TASKS.txt created with status
[ ] 4. Tasks added to task management
```

---

## Пример и применение

```bash
# 1. Feature analysis (Deutsch)
# -> Create Feature_Analysis_MyTool.md (see template) (Deutsch)

# 2. Code quality (Deutsch)
pylint MyTool/main.py
flake8 MyTool/main.py
file -i MyTool/main.py  # Check encoding

# 3. TASKS.txt (Deutsch)
# -> Create in tool folder with status "QUALITY REVIEW" (Deutsch)

# 4. Create tasks (Deutsch)
# -> Capture TASKS.txt entries as issues/tickets (Deutsch)
```

---

*Создано: 2026-01-10 | Перенесено: 2026-03-12*
