---
name: batch-file-ops
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Пакетные операции с файлами (удаление, перемещение, копирование, список) с использованием масок glob. CLI-инструмент для эффективной работы с файловой системой. Без зависимостей.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [batch, file-ops, glob, cli, filesystem, cleanup]
language: ru
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/batch_file_ops.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="batch-file-ops banner">

> **Русский** — Официальная русская версия `batch-file-ops`.


# batch_file_ops - Пакетные операции с файлами (Русский)

CLI-инструмент для эффективных пакетных операций с файлами с использованием масок glob.
Поддерживает: delete, move, copy, list. Нулевые зависимости (только стандартная библиотека Python).

---

## Действия

| Действие | Описание |
|----------|----------|
| `delete` | Удалить файлы, соответствующие маске |
| `move` | Переместить файлы, соответствующие маске |
| `copy` | Скопировать файлы, соответствующие маске |
| `list` | Вывести список файлов, соответствующих маске |

## Использование CLI

```bash
python batch_file_ops.py <action> <source> [<target>] --pattern "<glob>" [--dry-run] [--recursive]
```

### Аргументы

| Аргумент | Описание |
|----------|----------|
| `action` | `delete`, `move`, `copy` или `list` |
| `source` | Исходный каталог |
| `target` | Целевой каталог (только для `move` и `copy`) |
| `--pattern`, `-p` | Маска glob (например, `*.py`, `TOOLS_*.py`) — По умолчанию: `*` |
| `--dry-run`, `-n` | Только предварительный просмотр, без изменений |
| `--recursive`, `-r` | Рекурсивный поиск в подкаталогах |

---

## Примеры и использование

```bash
# Вывести список всех файлов Python в каталоге
python batch_file_ops.py list /path/to/directory --pattern "*.py"

# Удалить все файлы .tmp (сначала выполните пробный запуск dry-run!)
python batch_file_ops.py delete /path/to/directory --pattern "*.tmp" --dry-run
python batch_file_ops.py delete /path/to/directory --pattern "*.tmp"

# Переместить файлы
python batch_file_ops.py move /source /target --pattern "*.txt"

# Скопировать файлы (рекурсивно)
python batch_file_ops.py copy /source /target --pattern "*.md" --recursive

# Примеры масок
python batch_file_ops.py delete /path --pattern "TOOLS_*.py"
python batch_file_ops.py list /path --pattern "backup_202?-*"
```

---

## Примечания

- **Сначала пробный запуск (Dry-run):** Всегда сначала используйте `--dry-run` при выполнении `delete` и `move`
- **Маски Glob:** Используется Python `pathlib.glob()` / `pathlib.rglob()`
- **Совместимость с Windows:** Автоматическая кодировка вывода UTF-8
- **Только файлы:** Каталоги пропускаются (обрабатываются только файлы)
