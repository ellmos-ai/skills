---
name: kalender
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: Навык календаря с адаптивным выбором бэкенда пользователем (Flag 3). По умолчанию: локальное хранилище SQLite. Опционально: Google Calendar MCP, Routinika или UpToday в качестве бэкенда — управляется через assist/prefs.json. Если предпочтение не задано, LLM опрашивает пользователя интерактивно.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [kalender, termine, events, ics, google-calendar, routinika]
language: ru
status: stable
dependencies: {'tools': [], 'services': [{'name': 'Google Calendar MCP', 'optional': True, 'purpose': 'Backend option when kalender_backend=google in prefs.json'}], 'protocols': [{'name': 'ICS / iCalendar', 'optional': True, 'purpose': 'Import/export of appointments (RFC 5545 subset)'}], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin gefunden (kein kalender-Service in BACH/system/). Skill vollständig neu konzipiert mit Flag-3-Logik (user-adaptive backend). ICS-Felder angelehnt an RFC 5545, kein externer ICS-Parser benötigt.\n'}
---

> **Русский** — Официальная русская версия `kalender`.


## Обзор и назначение

Запись, запрос и управление встречами — с возможностью выбора бэкенда. Ядро
(`kalender_core.py`) всегда использует **локальное хранилище SQLite** по умолчанию.
LLM при необходимости выбирает альтернативный бэкенд из `assist/prefs.json`.

**Flag 3 — Выбор бэкенда:**

| `kalender_backend` в prefs.json | Поведение |
|---|---|
| `local` (по умолчанию) | Хранилище SQLite в папке данного навыка |
| `google` | Google Calendar MCP (только путь LLM, не в core.py) |
| `routinika` | Календарь Routinika через module-installer (не реализ. в v0.1) |
| `uptoday` | Календарь UpToday через module-installer (не реализ. в v0.1) |
| не задан | LLM интерактивно опрашивает пользователя о предпочитаемом бэкенде |

> `kalender_core.py` реализует исключительно бэкенд `local`.
> Google Calendar MCP и другие бэкенды управляются LLM и документированы в SKILL.md, а не в ядре.

---

## Триггеры

| Фраза | Действие |
|---|---|
| "Добавить встречу" | Запись новой встречи |
| "Что запланировано на сегодня?" | Запрос встреч на сегодня |
| "Что запланировано на эту неделю?" | Обзор на 7 дней |
| "Встреча [название] [дата]" | Создание встречи с датой |
| "Все встречи в [месяц]" | Ежемесячный обзор |
| "Удалить встречу [ID]" | Удаление встречи |
| "Экспортировать встречу" | Экспорт в ICS всех/отдельных встреч |

---

## Рабочий процесс и порядок действий

1. **Проверка бэкенда**: чтение `assist/prefs.json` → `kalender_backend`.
2. **Без предпочтений**: LLM спрашивает пользователя: локальный календарь, Google Calendar или другой?
3. **Локальный бэкенд**: core.py — создание/запрос/удаление встречи в хранилище SQLite.
4. **Бэкенд Google**: LLM вызывает Google Calendar MCP напрямую (core.py не задействован).
5. **Вывод**: Понятный список встреч или подтверждение.

---

## Точка входа CLI

```bash
# Create appointment (Deutsch)
python kalender_core.py add "Dentist" --date 2026-07-01 --time 10:00 [--duration 60] [--location "Dr. X practice"]

# Today's appointments (Deutsch)
python kalender_core.py today

# Weekly overview (Deutsch)
python kalender_core.py week [--from 2026-06-22]

# Monthly overview (Deutsch)
python kalender_core.py month [--month 2026-07]

# All appointments (optionally with search term) (Deutsch)
python kalender_core.py list [--search "Dentist"] [--limit 50]

# Delete appointment (Deutsch)
python kalender_core.py delete <id>

# ICS export (Deutsch)
python kalender_core.py export [--id <id>] [--out calendar.ics]

# Backend check (Deutsch)
python kalender_core.py check-backend

# Alternative store (e.g. for tests) (Deutsch)
python kalender_core.py --store /tmp/kal_test.db today --dry-run
```

---

## Хранилище

| Свойство | Значение |
|---|---|
| Тип | SQLite (локальный бэкенд) |
| Путь (по умолчанию) | `skills/assist/kalender/store.db` |
| Переопределение | `--store <path>` или переменная окружения `KALENDER_STORE` |
| Таблицы | `events` |

### Схема

```sql
CREATE TABLE IF NOT EXISTS events (
    id           TEXT PRIMARY KEY,      -- UUID (short: 8 hex)
    title        TEXT NOT NULL,         -- appointment name
    date         TEXT NOT NULL,         -- ISO date YYYY-MM-DD
    time         TEXT,                  -- HH:MM (optional)
    duration_min INTEGER,               -- duration in minutes (optional)
    location     TEXT,                  -- location (optional)
    description  TEXT,                  -- note/description
    recurrence   TEXT,                  -- ICS RRULE (optional, e.g. "FREQ=WEEKLY")
    ics_uid      TEXT UNIQUE,           -- ICS UID for import/export
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);
```

---

## Принципы разработки

- Ядро реализует только бэкенд `local` — легкое решение без внешних зависимостей.
- Экспорт ICS генерирует допустимое подмножество RFC 5545 (VCALENDAR + VEVENT), импортируемое во все распространенные календарные приложения.
- Импорт ICS (парсер) еще не реализован в v0.1 — запланирован на v0.2.
- Правила повторения (`recurrence`/RRULE) сохраняются, но не оцениваются — оценка запланирована на v0.2.

---

## Конфиденциальность

- Локальные встречи остаются в `store.db` — в ядре нет сетевого доступа.
- При использовании бэкенда Google Calendar данные обрабатывает Google Calendar MCP — применяется политика конфиденциальности Google.
- Не коммитьте `store.db` в Git (рекомендуется: `.gitignore`).

---

## Связанные ресурсы

- Google Calendar MCP (`mcp__claude_ai_Google_Calendar__*`) — альтернативный бэкенд под управлением LLM
- Навык `assist/haushalt-manager` — интеграция Routinika (шаблон проверки присутствия)
- `tools/module-installer/module_installer.py` — для будущей интеграции бэкенда Routinika/UpToday

---

## Журнал изменений

| Версия | Дата | Изменение |
|---|---|---|
| 0.1.0 | 2026-06-22 | Первоначальное создание — логика Flag-3, локальный бэкенд, экспорт ICS |