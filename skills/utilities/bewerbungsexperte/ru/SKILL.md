---
name: bewerbungsexperte
version: 1.1.0
type: expert
author: BACH Team / ellmos (standalone port)
created: 2026-01-25
updated: 2026-06-22
description: Специалист по всему процессу подачи заявок на работу. Анализирует вакансии, оптимизирует профили (LinkedIn/CV) и создает индивидуальные сопроводительные письма. Генерирует резюме в формате ASCII из базы данных SQLite и структуры папок. cv_generator.py перенесен автономно -- среда выполнения BACH не требуется.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [bewerbung, cv, anschreiben, linkedin]
language: ru
status: active
dependencies: {'tools': ['cv_generator.py'], 'services': [], 'protocols': [], 'python': ['sqlite3', 'pathlib', 'argparse', 're']}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/_experts/bewerbungsexperte/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
---

> **Русский** — Официальная русская версия `bewerbungsexperte`.


<img src="banner.png" width="100%" alt="bewerbungsexperte banner">
# BEWERBUNGSEXPERTE v1.1 (Русский)

> Ваш стратегический партнер для следующего шага в карьере.

## АКТИВАЦИЯ

```bash
# Пример резюме без доступа к базе данных (Русский)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --dry-run

# Генерация резюме из базы данных SQLite (Русский)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad/zu/daten.db>

# Сохранение резюме в файл (Русский)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad> --output lebenslauf.txt

# С сканированием папок (Русский)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad> --career-path <ordner>
```

## КАТАЛОГ УСЛУГ

### 1. Генерация резюме (`cv_generator.py`)
- **Личные данные:** Чтение из таблицы `assistant_user_profile` (ключ/значение)
- **Опыт работы:** Сканирование папки работодателя (рекомендации, контракты)
- **Образование:** Сканирование папки дипломов/аттестатов
- **Повышение квалификации:** Сканирование папки сертификатов
- **Рекомендации:** Из таблицы `contacts` (category='beruflich')
- **Тестовый прогон (Dry-Run):** Без базы данных -- примерные данные для тестирования

### 2. Диагностика вакансии
- **Сопоставление ключевых слов:** Сравнение резюме с требованиями вакансии (ATS-Safe)
- **Проверка компании:** Исследование корпоративной культуры и льгот

### 3. Сервис документов
- **Оптимизация резюме:** Структурирование и акцентирование опыта
- **Сопроводительное письмо:** Создание индивидуальных, убедительных писем
- **Портфолио:** Консультации по образцам работ и рекомендациям

## ТАБЛИЦЫ БАЗЫ ДАННЫХ (опционально)

`cv_generator.py` считывает данные из этих таблиц, если они существуют:

- `assistant_user_profile` (key TEXT, value TEXT) — Личные данные
  - Поля: name, full_name, email, phone, address, birthday, nationality, marital_status
- `contacts` (name, organization, position, phone, email, is_active, category) — Рекомендации

Отсутствующие таблицы игнорируются (пустые секции в резюме).

## СТРУКТУРА ПАПОК (для --career-path и т. д.)

```
_Arbeitgeber/
  Firma_A_2020-2023/
    Arbeitsvertrag.pdf
    Arbeitszeugnis.pdf
  Firma_B_2018-2020/
    ...
_Abschluesse/
  Universitaet/
    Bachelor_Zeugnis.pdf
_Fortbildungen/
  Zertifikat_Cloud_AWS_2024.pdf
```

## CLI-ОПЦИИ

```
--db <pfad>           Путь к базе данных SQLite (обязательно без --dry-run)
--output, -o          Выходной файл (иначе stdout)
--career-path         Путь к папке работодателя
--education-path      Путь к папке дипломов/образования
--certs-path          Путь к папке сертификатов
--dry-run             Пример резюме без доступа к базе данных
```

## РАБОЧИЙ ПРОЦЕСС: ГЕНЕРАЦИЯ РЕЗЮМЕ

1. **Подготовка**
   - Предоставить БД SQLite (БД BACH или собственную)
   - Создать структуру папок с документами (опционально)

2. **Тест без БД**
   - `python cv_generator.py --dry-run` -- проверяет работоспособность инструмента

3. **Генерация**
   - `python cv_generator.py --db <pfad> --career-path <arbeitgeber>`
   - Проверить вывод и при необходимости скорректировать

4. **Экспорт**
   - `python cv_generator.py --db <pfad> --output lebenslauf.txt`

## ЗАВИСИМОСТИ

Только стандартная библиотека Python: `sqlite3`, `pathlib`, `argparse`, `re`, `datetime`.
Установка через pip не требуется, импорт среды выполнения BACH не требуется.

## ЖУРНАЛ ИЗМЕНЕНИЙ

### 1.1.0 (2026-06-22)
- Автономный перенос из BACH v1.0.0
- `--db <pfad>` вместо жестко запрограммированного пути к исходной БД
- Добавлен режим `--dry-run`
- Удален `--scan-folders` (требовалась таблица user_data_folders из BACH)
- Нейтрализован текст подвала
- Проверена независимость от среды выполнения BACH

### 1.0.0 (2026-01-25, внутренний BACH)
- Начальная версия в BACH system/agents/_experts/bewerbungsexperte/

---
Статус: АКТИВЕН
Область: Карьерное консультирование
