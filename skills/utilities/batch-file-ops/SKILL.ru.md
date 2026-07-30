---
name: batch-file-ops
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Пакетные операции с файлами (удаление, перемещение, копирование, список) с помощью шаблонов glob. CLI-инструмент для эффективных операций с файловой системой. Без зависимостей.

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

CLI-инструмент для эффективных пакетных операций над файлами с использованием шаблонов glob.
Поддерживает: delete, move, copy, list. Без зависимостей (только стандартная библиотека Python).

---

## Действия

| Действие | Описание |
|----------|----------|
| `delete` | Удалить файлы, соответствующие шаблону |
| `move` | Переместить файлы, соответствующие шаблону |
| `copy` | Копировать файлы, соответствующие шаблону |
| `list` | Вывести список файлов, соответствующих шаблону |

## Использование CLI

```bash
python batch_file_ops.py <action> <source> [<target>] --pattern "<glob>" [--dry-run] [--recursive]
```

### Аргументы

| Аргумент | Описание |
|----------|----------|
| `action` | `delete`, `move`, `copy` или `list` |
| `source` | Исходная директория |
| `target` | Целевая директория (только для `move` и `copy`) |
| `--pattern`, `-p` | Шаблон glob (например, `*.py`, `TOOLS_*.py`) - По умолчанию: `*` |
| `--dry-run`, `-n` | Только предварительный просмотр, без изменений |
| `--recursive`, `-r` | Рекурсивный поиск в поддиректориях |

---

## Примеры и использование

```bash
# Список всех файлов Python в директории (Русский)
python batch_file_ops.py list /path/to/directory --pattern "*.py"

# Удалить все файлы .tmp (сначала запустите с --dry-run!) (Русский)
python batch_file_ops.py delete /path/to/directory --pattern "*.tmp" --dry-run
python batch_file_ops.py delete /path/to/directory --pattern "*.tmp"

# Переместить файлы (Русский)
python batch_file_ops.py move /source /target --pattern "*.txt"

# Копировать файлы (рекурсивно) (Русский)
python batch_file_ops.py copy /source /target --pattern "*.md" --recursive

# Примеры шаблонов (Русский)
python batch_file_ops.py delete /path --pattern "TOOLS_*.py"
python batch_file_ops.py list /path --pattern "backup_202?-*"
```

---

## Примечания

- **Сначала Dry-run:** Всегда сначала используйте `--dry-run` для `delete` и `move`
- **Шаблоны Glob:** Используется Python `pathlib.glob()` / `pathlib.rglob()`
- **Совместимость с Windows:** Автоматическая кодировка вывода UTF-8
- **Только файлы:** Директории пропускаются (обрабатываются только файлы)