---
name: nulcleaner
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Находит и удаляет зарезервированные файлы NUL в Windows, созданные при использовании /dev/null в Git Bash. В автономном режиме (headless) или с GUI.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [windows, nul, cleanup, git-bash, filesystem]
language: ru
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/nulcleaner.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="nulcleaner banner">

> **Русский** — Официальная русская версия `nulcleaner`.

# nulcleaner - Windows NUL File Cleanup (Русский)

## Проблема

При использовании `/dev/null` в командах Git Bash в Windows (например, `> /dev/null`) вместо перенаправления в никуда в текущем каталоге создается **реальный файл с именем `nul`**. Windows резервирует "NUL" в качестве имени устройства, поэтому такие файлы нельзя удалить обычным способом.

Этот инструмент находит и удаляет такие файлы NUL с использованием расширенного пути UNC (`\\?\`).

---

## Режимы

| Режим | Описание |
|------|-------------|
| `scan` | Рекурсивное сканирование каталога на наличие файлов NUL |
| `delete` | Поиск и удаление файлов NUL |
| `gui` | Графический интерфейс с выбором файлов |

---

## Использование CLI

```bash
# Только сканирование (показывает найденные файлы NUL) (Русский)
python nulcleaner.py scan /path/to/directory

# Сканирование и удаление (Русский)
python nulcleaner.py delete /path/to/directory

# Запуск режима GUI (Русский)
python nulcleaner.py gui
```

---

## Автономный API (для интеграции)

Инструмент также предоставляет Python API для автономной работы (headless):

```python
from nulcleaner import clean_nul_files_headless

result = clean_nul_files_headless("/path/to/directory", verbose=True)
print(f"Found: {result['found']}, Deleted: {result['deleted']}")
```

**Возвращаемое значение:** `{'found': int, 'deleted': int, 'errors': list}`

---

## Технические детали

- Использует расширенный путь UNC (`\\?\`) для удаления зарезервированных имен файлов Windows
- Рекурсивное сканирование с помощью `os.walk()`
- Графический интерфейс на tkinter (без внешних зависимостей)
- Работает только в Windows (где возникает проблема)

---

## Предотвращение

Лучше полностью избегать использования `/dev/null` в Git Bash. Вместо этого:
- Просто опускайте вывод
- Используйте `2>&1` для перенаправления stderr
- Обращайте внимание на совместимость с Windows в шелл-скриптах