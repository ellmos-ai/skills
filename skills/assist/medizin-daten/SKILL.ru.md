---
name: medizin-daten
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: Локальная, конфиденциальная фиксация медицинских данных: диагнозы, история симптомов и планы обследования. Без происхождения от BACH — индивидуальный проект со собственным хранилищем SQLite. Строго локально, без передачи в облако.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [medizin, diagnose, symptome, gesundheit, privat, lokal]
language: ru
status: stable
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin. Skill vollständig neu konzipiert. Kein bestehendes Implementierungs-Vorbild im Ökosystem gefunden.\n'}
---

> **Русский** — Официальная русская версия `medizin-daten`.


## Обзор и назначение

Безопасная и локальная фиксация личных медицинских данных: диагнозы (код МКБ-10 опционально), история симптомов со временными рядами и планы обследований. Все данные хранятся исключительно локально в `medizin-daten/store.db`.

Скилл не заменяет медицинскую консультацию и не делает медицинских заключений — это структурированный блокнот для личных данных о здоровье.

---

## Триггеры (Triggers)

| Фраза | Действие |
|---|---|
| "Record a diagnosis" / "Записать диагноз" | Создать новый диагноз |
| "Add diagnosis [name]" / "Добавить диагноз [название]" | Создать поименованный диагноз |
| "Symptom history" / "История симптомов" | Зафиксировать сегодняшние симптомы |
| "Record symptom [name]" / "Записать симптом [название]" | Зафиксировать один симптом |
| "Examination plan" / "План обследования" | Показать предстоящие приемы/обследования |
| "Add appointment" / "Добавить запись" | Внести запись на обследование |
| "Show my diagnoses" / "Показать мои диагнозы" | Вывести список диагнозов |

---

## Рабочий процесс и порядок действий

1. **Определение режима**: диагноз / симптом / план обследования
2. **Структурирование ввода**: дата, название, примечания, опциональный код МКБ-10
3. **Сохранение**: в `store.db` (локально, без доступа к сети)
4. **Вывод**: понятная сводка для контекста LLM

---

## Точка входа CLI

```bash
# Create diagnosis (Deutsch)
python medizin_daten_core.py add-diagnosis "Hypertension" [--icd I10] [--note "note"]

# List diagnoses (Deutsch)
python medizin_daten_core.py diagnoses

# Record symptom (Deutsch)
python medizin_daten_core.py add-symptom "Headache" [--severity 7] [--date 2026-06-22] [--note "..."]

# Symptom history for a name (Deutsch)
python medizin_daten_core.py symptom-history "Headache" [--limit 30]

# Plan examination (Deutsch)
python medizin_daten_core.py add-exam "Blood count" [--date 2026-07-01] [--note "fasting"]

# Upcoming examinations (Deutsch)
python medizin_daten_core.py exams [--upcoming]

# Alternative store (e.g. for tests) (Deutsch)
python medizin_daten_core.py --store /tmp/med_test.db diagnoses --dry-run
```

---

## Хранилище (Store)

| Свойство | Значение |
|---|---|
| Тип | SQLite |
| Путь (по умолчанию) | `skills/assist/medizin-daten/store.db` |
| Переопределение | `--store <path>` или пер. окружения `MEDIZIN_STORE` |
| Таблицы | `diagnoses`, `symptoms`, `examination_plans` |

### Схема (Schema)

```sql
CREATE TABLE IF NOT EXISTS diagnoses (
    id          TEXT PRIMARY KEY,     -- UUID (short: 8 hex)
    name        TEXT NOT NULL,        -- name (e.g. "Hypertension")
    icd_code    TEXT,                 -- ICD-10 code optional (e.g. "I10")
    onset_date  TEXT,                 -- onset (ISO-8601, optional)
    status      TEXT DEFAULT 'aktiv', -- aktiv | remission | abgeschlossen
    note        TEXT,                 -- free-text note
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS symptoms (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optional: assignment
    name         TEXT NOT NULL,       -- name (e.g. "Headache")
    severity     INTEGER,             -- 1–10 scale (optional)
    recorded_at  TEXT NOT NULL,       -- ISO-8601 timestamp
    note         TEXT
);

CREATE TABLE IF NOT EXISTS examination_plans (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optional: assignment
    exam_name    TEXT NOT NULL,       -- examination name
    planned_date TEXT,                -- planned date (ISO-8601)
    done_date    TEXT,                -- completed on (NULL = pending)
    note         TEXT,
    created_at   TEXT NOT NULL
);
```

---

## Подход и принципы

- Никаких медицинских рекомендаций и постановки диагнозов со стороны скилла.
- Коды МКБ-10 сохраняются как свободный текст — без проверки по внешней базе данных.
- Шкала тяжести от 1 до 10 является субъективной оценкой пользователя.
- Отсутствующие значения (дата, тяжесть) всегда допускаются — применяется принцип блокнота.

---

## Конфиденциальность (Privacy Gate)

> **ПРЕДУПРЕЖДЕНИЕ: Медицинские данные особенно чувствительны.**

- `store.db` содержит конфиденциальные данные о здоровье — **никогда не коммитьте в Git**.
- **Без доступа к сети** — все операции выполняются исключительно локально.
- **Без передачи** внешним сервисам, без синхронизации с облачными бэкендами.
- Рекомендация по резервному копированию: зашифрованная локальная копия (например, `age`/`gpg`).
- При запуске скилл проверяет, находится ли `store.db` за пределами локальной файловой системы, и выводит предупреждение, если путь находится в папке синхронизации (OneDrive и т.д.).
- `~/.gitignore_global` или локальный `.gitignore` должны исключать `store.db`.

---

## Связанные ресурсы

- Скилл `assist/gesundheit` — общая помощь по здоровью (не медицинские данные)
- MediPlaner (`tools/module-installer` → `mediplaner`) — управление медикаментами (отдельная программа)

---

## История изменений

| Версия | Дата | Изменение |
|---|---|---|
| 0.1.0 | 2026-06-22 | Первоначальное создание — индивидуальный проект, фильтр конфиденциальности, схема из 3 таблиц |