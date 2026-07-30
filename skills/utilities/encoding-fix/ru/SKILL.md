---
name: encoding-fix
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Восстановление текста (mojibake) при двойном/тройном кодировании UTF-8. Исправляет неверную интерпретацию Windows cp1252/Latin-1. Нуль зависимостей.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [encoding, utf-8, mojibake, windows, cp1252, text-repair]
language: ru
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/encoding_fix.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

> **Русский** — Официальная русская версия `encoding-fix`.


# Encoding Fix (Русский)

Исправляет mojibake (двойное/тройное кодирование UTF-8), вызванное ошибочной интерпретацией Windows cp1252/Latin-1. Нуль зависимостей — только стандартная библиотека Python.

## Типичная проблема

```
"ue" (U+00FC) -> UTF-8 \xc3\xbc -> read as cp1252 -> "Ã¼"
```

## Использование

### Как библиотека
```python
from encoding_fix import sanitize_outbound

clean = sanitize_outbound("WÃ¼rge")  # -> "Wuerge"
```

### Вывод подпроцесса
```python
from encoding_fix import sanitize_subprocess_output

text = sanitize_subprocess_output(process.stdout)
```

### CLI
```bash
python encoding_fix.py "WÃ¼rge"    # Check a single string
python encoding_fix.py              # Self-test
```

## Возможности

- **Идемпотентность:** Корректно закодированный текст не изменяется
- **До 3 раундов:** Восстанавливает даже строки с тройным кодированием
- **Декодер подпроцессов:** Резервный механизм (fallback) UTF-8/cp1252 для вывода процессов
- **Нуль зависимостей:** Только стандартная библиотека Python

## История изменений

### 1.0.0 (2026-03-12)
- Перенесено из BACH system/tools/encoding_fix.py
