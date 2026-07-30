---
name: encoding-fix
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Восстановление кракозябр (mojibake) при двойном/тройном кодировании UTF-8. Исправляет ошибки интерпретации Windows cp1252/Latin-1. Нулевые зависимости.

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

<img src="banner.png" width="100%" alt="encoding-fix banner">

> **Русский** — Официальная русская версия `encoding-fix`.


# Encoding Fix (Русский)

Исправляет кракозябры (mojibake, двойное/тройное кодирование UTF-8), вызванные неправильной интерпретацией Windows cp1252/Latin-1. Нулевые внешние зависимости — только стандартная библиотека Python.

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

### Интерфейс командной строки (CLI)
```bash
python encoding_fix.py "WÃ¼rge"    # Check a single string
python encoding_fix.py              # Self-test
```

## Особенности

- **Идемпотентность:** Корректно закодированный текст не изменяется
- **До 3 проходов:** Восстанавливает даже трижды закодированные строки
- **Декодер подпроцессов:** Резервный механизм UTF-8/cp1252 для вывода процессов
- **Нулевые зависимости:** Только стандартная библиотека Python

## Журнал изменений

### 1.0.0 (2026-03-12)
- Перенесено из BACH system/tools/encoding_fix.py