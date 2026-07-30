---
name: dev
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: Ассистент разработчика (преемник ATI). Предоставляет быстрый обзор проекта с помощью автономного сканирования и маршрутизирует запросы к доступным инструментам разработки: CodeCommander MCP (анализ/рефакторинг/диагностика) и модулю ellmos-code-tools. Чистая маршрутизация инструментов + сканирование, без собственного хранилища.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [dev, coding, projekt-scan, ati, codecommander]
language: ru
status: active
dependencies: {'tools': ['dev_core.py'], 'services': [], 'protocols': [], 'python': ['pathlib'], 'external': ['codecommander-mcp', 'ellmos-code-tools']}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/ati/ + system/agents/entwickler/', 'origin_version': 'n/a', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="dev banner">

> **Русский** — Официальная русская версия `dev`.


# Dev — Ассистент разработчика (ATI) (Русский)

Сначала получает обзор, затем передаёт управление соответствующим инструментам.

## Обзор и назначение

Преемник агента ATI/entwickler из BACH. Две основные задачи:
1. **Сканирование проекта** (автономное/headless, стандартная библиотека): быстрый и экономный по токенам обзор структуры, языков и маркеров сборки проекта — до запуска затратного анализа.
2. **Маршрутизация инструментов:** делегирует задачи существующим инструментам разработки вместо дублирования их функций.

## Триггеры (Triggers)

| Ввод пользователя | Действие |
|---|---|
| "Получи обзор проекта X" | `dev_core.py scan <path>` |
| "Что это за проект / какой стек?" | `dev_core.py scan <path>` |
| "Проанализируй этот файл / сделай рефакторинг" | → CodeCommander MCP |
| "Сгенерируй/проверь код на Python" | → CodeCommander MCP / ellmos-code-tools |

## Ландшафт инструментов (Цели маршрутизации)

- **CodeCommander MCP** (`.AI/.MCP/ellmos-codecommander-mcp`): `cc_analyze_code`, `cc_analyze_methods`, `cc_extract_classes`, `cc_diagnose_imports`, `cc_runtime_import_diagnose`, `cc_generate_python_code`, `cc_check_indentation` и т. д.
- **ellmos-code-tools** (`.AI/.MODULES/ellmos-code-tools`): Инструменты разработки CLI (Structural-Edit, pycutter context, Method-Analyzer).
- **FileCommander MCP**: Операции с файлами и каталогами в больших деревьях.

## Точка входа CLI (dev_core.py)

```bash
python dev_core.py scan .              # current project
python dev_core.py scan /path/project  # structure + languages + markers
```

Определяет, например: Python (pyproject/requirements/setup), Node/TypeScript, Rust, Go, Java, Roblox (Rojo), Docker, репозиторий Git.

## Хранилище (Store)

Без хранилища. Только сканирование + маршрутизация.

## Подход

Мы рекомендуем CodeCommander/ellmos-code-tools в качестве инструментов разработки, но открыты для использования других (например, ruff/pylint/eslint), если пользователь предпочитает их.

## Конфиденциальность

- `dev_core.py` считывает только имена файлов/каталогов (структуру), без содержимого и без загрузки на внешние сервисы.
- Пропускаются: `.git`, `node_modules`, `.venv`, `__pycache__` и т. д.

## Связанные ресурсы

- `assist/AGENTS.md` — Главный маршрутизатор
- `.AI/.MCP/ellmos-codecommander-mcp` · `.AI/.MODULES/ellmos-code-tools`

## История изменений

### 0.1.0 (2026-06-22)
- Начальная версия. Преемник ATI/entwickler: автономное сканирование проекта (стандартная библиотека) + маршрутизация к CodeCommander MCP / ellmos-code-tools. Нейтрален к пользователю, без хранилища.