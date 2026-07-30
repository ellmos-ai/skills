---
name: tageszeitung
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: Создает персональную ежедневную газету из RSS-лент и веб-источников. Перенесено из новостной системы BACH (news.py + newspaper_generator.py). Собственное хранилище SQLite (без Origin-DB). feedparser опционален — XML-фоллбэк через stdlib. Экспорт в PDF через Edge Headless (msedge.exe).

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [zeitung, news, rss, feed, pdf, tageszeitung]
language: ru
status: stable
dependencies: {'tools': [{'name': 'msedge.exe', 'optional': True, 'purpose': 'HTML → PDF (Edge Headless); without Edge: HTML output only'}], 'services': [], 'protocols': [], 'python': [{'name': 'feedparser', 'optional': True, 'install': 'pip install feedparser', 'purpose': 'RSS parsing (main backend). Fallback: defusedxml → regex'}, {'name': 'defusedxml', 'optional': True, 'install': 'pip install defusedxml', 'purpose': 'XXE-safe XML parser as fallback when feedparser is missing. Without defusedxml a regex fallback is used (no ET.fromstring on network data).'}]}
provenance: {'origin': 'bach-port', 'origin_path': 'BACH/system/hub/news.py + hub/_services/newspaper/newspaper_generator.py', 'origin_version': 'news.py v1.x, newspaper_generator.py v1.x', 'origin_repo': 'ellmos-ai/bach (privat)', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'notes': 'Schema (news_sources + news_items) 1:1 aus BACH news.py portiert. BaseHandler-Abhängigkeit entfernt. Origin-DB-Pfad entfernt. DB-Pfad konfigurierbar. newspaper_generator.py-Logik (HTML-Render + Edge-PDF) userneutral übernommen.\n'}
---

<img src="banner.png" width="100%" alt="tageszeitung banner">

> **Русский** — Официальная русская версия `tageszeitung`.


## Обзор и назначение

Загружает статьи из настроенных RSS-лент и веб-источников, сортирует их по категориям и отображает в виде daily newspaper в формате HTML/PDF. Статьи сохраняются локально в `tageszeitung/store.db` и отмечаются как прочитанные.

---

## Триггеры

| Фраза | Действие |
|---|---|
| "Создать мою ежедневную газету" | Загрузить статьи + сгенерировать PDF |
| "Ежедневная газета на сегодня" | Сгенерировать газету на сегодня |
| "Добавить ленту [URL]" | Зарегистрировать RSS-источник |
| "Показать мои источники" | Вывести список источников |
| "Загрузить новости" | Загрузить все источники (без генерации) |

---

## Рабочий процесс и порядок действий

1. **Проверка источников**: чтение всех активных источников из `news_sources`.
2. **Загрузка**: RSS через feedparser (или фоллбэк xml.etree), веб через urllib.
3. **Дедупликация**: UNIQUE(source_id, url) предотвращает дублирование.
4. **Генерация (Render)**: группировка непрочитанных статей по категориям → HTML → PDF.
5. **Доставка**: размещение HTML/PDF в папке назначения (настраиваемый путь).

---

## Точка входа CLI

```bash
# Add source (Deutsch)
python tageszeitung_core.py add-source "Heise" rss https://www.heise.de/rss/heise-atom.xml --category tech

# Fetch all sources (Deutsch)
python tageszeitung_core.py fetch

# Render daily newspaper (HTML + PDF if Edge available) (Deutsch)
python tageszeitung_core.py render [--date 2026-06-22] [--out /path/]

# List sources (Deutsch)
python tageszeitung_core.py sources

# Unread articles (Deutsch)
python tageszeitung_core.py items [--limit 50] [--category tech]

# Mark article as read (Deutsch)
python tageszeitung_core.py read <item_id>

# Alternative store (e.g. for tests) (Deutsch)
python tageszeitung_core.py --store /tmp/t.db sources --dry-run
```

---

## Хранилище

| Свойство | Значение |
|---|---|
| Тип | SQLite |
| Путь (по умолчанию) | `skills/assist/tageszeitung/store.db` |
| Переопределение | `--store <path>` или пер. окружения `TAGESZEITUNG_STORE` |
| Таблицы | `news_sources`, `news_items` |

### Схема (перенесено из BACH news.py)

```sql
CREATE TABLE IF NOT EXISTS news_sources (
    id           TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    type         TEXT NOT NULL DEFAULT 'rss',  -- rss | web
    url          TEXT NOT NULL UNIQUE,
    category     TEXT DEFAULT 'Allgemein',
    schedule     TEXT DEFAULT 'daily',
    is_active    INTEGER DEFAULT 1,
    last_fetched TEXT,
    fetch_count  INTEGER DEFAULT 0,
    error_count  INTEGER DEFAULT 0,
    last_error   TEXT,
    created_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS news_items (
    id           TEXT PRIMARY KEY,
    source_id    TEXT NOT NULL REFERENCES news_sources(id),
    title        TEXT NOT NULL,
    content      TEXT,
    summary      TEXT,
    url          TEXT,
    author       TEXT,
    published_at TEXT,
    fetched_at   TEXT NOT NULL,
    is_read      INTEGER DEFAULT 0,
    category     TEXT,
    UNIQUE(source_id, url)
);
```

---

## Принципы работы

- Предпочтительно использование feedparser; при отсутствии feedparser используется фоллбэк на xml.etree для обработки простых RSS 2.0 лент.
- Для генерации PDF требуется `msedge.exe` в системном PATH или в переменной окружения `MSEDGE_PATH`. Без Edge создается только HTML.
- Максимальное количество статей на категорию: настраивается через `assist/prefs.json` (`tageszeitung_max_per_category`, по умолчанию: 5).

---

## Конфиденциальность

- Содержимое статей остается локально в `store.db`.
- Никаких внешних сервисов аналитики — обращение происходит только к настроенным RSS/веб-источникам.

---

## Связанные ресурсы

- BACH `hub/news.py` — оригинал (только для чтения)
- BACH `hub/_services/newspaper/newspaper_generator.py` — оригинал (только для чтения)

---

## История изменений

| Версия | Дата | Изменение |
|---|---|---|
| 0.1.0 | 2026-06-22 | Начальное создание — перенесена схема BACH, собственное хранилище, feedparser опционален |