---
name: bewerbungsexperte
version: 1.1.0
type: expert
author: BACH Team / ellmos (standalone port)
created: 2026-01-25
updated: 2026-06-22
description: Специалист по всему процессу подачи заявок на работу. Анализирует вакансии, оптимизирует профили (LinkedIn/CV) и генерирует персональные сопроводительные письма. Генерирует ASCII-резюме из базы данных SQLite и структуры папок. cv_generator.py перенесен в автономном режиме -- среда выполнения BACH не требуется.
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

<img src="banner.png" width="100%" alt="bewerbungsexperte banner">

> **Русский** — Официальная русская версия `bewerbungsexperte`.


# BEWERBUNGSEXPERTE v1.1 (Русский)

> Ваш стратегический партнер для следующего карьерного шага.

## АКТИВАЦИЯ

```bash
# Пример CV без доступа к базе данных (Русский)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --dry-run

# Генерация CV из базы данных SQLite (Русский)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <путь/к/данным.db>

# Сохранение CV в файл (Русский)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <путь> --output lebenslauf.txt

# Со сканированием папок (Русский)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <путь> --career-path <папка>
```

## КАТАЛОГ УСЛУГ

### 1. Генерация CV (`cv_generator.py`)
- **Личные данные:** чтение из таблицы `assistant_user_profile` (ключ/значение)
- **Опыт работы:** сканирование папки работодателей (рекомендации, контракты)
- **Образование:** сканирование папки дипломов
- **Повышение квалификации:** сканирование папки сертификатов
- **Рекомендации:** из таблицы `contacts` (category='beruflich')
- **Dry-Run:** без базы данных -- тестовые данные для проверки

### 2. Диагностика вакансии
- **Совпадение ключевых слов:** сопоставление CV с требованиями вакансии (ATS-Safe)
- **Проверка компании:** исследование корпоративной культуры и льгот

### 3. Сервис документов
- **Настройка CV:** структурирование и акцентирование опыта
- **Сопроводительные письма:** создание индивидуальных и убедительных писем
- **Портфолио:** консультации по примерам работ и рекомендациям

## ТАБЛИЦЫ БАЗЫ ДАННЫХ (опционально)

`cv_generator.py` читает из этих таблиц, если они существуют:

- `assistant_user_profile` (key TEXT, value TEXT) — Личные данные
  - Поля: name, full_name, email, phone, address, birthday, nationality, marital_status
- `contacts` (name, organization, position, phone, email, is_active, category) — Рекомендации

Отсутствующие таблицы игнорируются (пустые секции в CV).

## СТРУКТУРА ПАПОК (для --career-path и т.д.)

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

## ОПЦИИ CLI

```
--db <путь>           Путь к базе данных SQLite (обязательно без --dry-run)
--output, -o          Выходной файл (иначе stdout)
--career-path         Путь к папке работодателей
--education-path      Путь к папке дипломов
--certs-path          Путь к папке сертификатов
--dry-run             Пример CV без доступа к базе данных
```

## РАБОЧИЙ ПРОЦЕСС: ГЕНЕРАЦИЯ CV

1. **Подготовка**
   - Подготовить БД SQLite (БД BACH или собственную)
   - Создать структуру папок с документами (опционально)

2. **Тест без БД**
   - `python cv_generator.py --dry-run` -- проверяет работу инструмента

3. **Генерация**
   - `python cv_generator.py --db <путь> --career-path <работодатель>`
   - Проверить результат и при необходимости скорректировать

4. **Экспорт**
   - `python cv_generator.py --db <путь> --output lebenslauf.txt`

## ЗАВИСИМОСТИ

Только стандартная библиотека Python: `sqlite3`, `pathlib`, `argparse`, `re`, `datetime`.
Установка через pip не требуется, импорт среды выполнения BACH не требуется.

## ЖУРНАЛ ИЗМЕНЕНИЙ

### 1.1.0 (2026-06-22)
- Автономный перенос из BACH v1.0.0
- Использование `--db <путь>` вместо жестко запрограммированного исходного пути к БД
- Добавлен режим `--dry-run`
- Удален параметр `--scan-folders` (требовалась таблица user_data_folders из BACH)
- Нейтрализован текст подвала
- Проверена независимость от среды выполнения BACH

### 1.0.0 (2026-01-25, внутренний BACH)
- Начальная версия в BACH system/agents/_experts/bewerbungsexperte/

---
Статус: АКТИВЕН
Домен: Карьерное консультирование