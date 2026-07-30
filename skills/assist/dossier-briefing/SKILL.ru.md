---
name: dossier-briefing
version: 1.0.0
category: assist
description: Генерирует структурированный исследовательский брифинг по теме или человеку в виде Markdown-шаблона (stdout или файл). Без постоянного хранилища.
tags: [briefing, dossier, recherche, markdown, research]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['datetime', 'pathlib', 'textwrap']}
runtime: python3
entry_point: dossier_briefing_core.py
provenance: {'origin': 'BACH persoenlicher-assistent', 'origin_path': 'system/agents/persoenlicher-assistent/tools/dossier_generator.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': 'Alle Origin-DB-Abhaengigkeiten entfernt (create_dossier, update_dossier, DOSSIERS_DIR, DossierGenerator-Klasse mit DB-Methoden). Nur _create_markdown-Logik portiert und verallgemeinert (Person→Subjekt). Kein Store. One-Shot-Scaffold-Generator. Headless, nur Stdlib.\n'}
language: ru
---

> **Русский** — Официальная русская версия `dossier-briefing`.


# Dossier-Briefing (Русский)

**Структурированный исследовательский брифинг по теме или человеку**

---

## Обзор и назначение

Генерирует пустой структурированный Markdown-брифинг для любого объекта
(человек, компания, событие, концепция). Каркас (шаблон) служит отправной точкой для
последующего исследования с помощью `research-agent` или `web-reading`.

---

## Триггеры

| Фраза | Действие |
|---|---|
| "Создать брифинг по Мари Кюри" / "Create a briefing on Marie Curie" | Каркас: человек, type=person |
| "Досье на OpenAI" / "Dossier on OpenAI" | Каркас: компания, type=organization |
| "Брифинг по квантовым вычислениям" / "Briefing on quantum computing" | Каркас: тема, type=topic |
| "Подготовить исследовательский брифинг по COP30" / "Prepare a research briefing on COP30" | Каркас: событие, type=event |

---

## Рабочий процесс и порядок действий

1. **Определение объекта:** Извлечь имя/название брифинга из пользовательского ввода.
2. **Определение типа:** person, organization, topic, event (или unspecified).
3. **Генерация каркаса:** Создать Markdown-документ со всеми релевантными разделами.
4. **Вывод:** stdout или опциональная запись в файл (`-o file.md`).
5. **Начало исследования:** Передать каркас в `research-agent` или `web-reading`
   для заполнения отсутствующих разделов.

---

## CLI

```bash
# Briefing to stdout (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Marie Curie" --typ person

# Write to file (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "OpenAI" --typ organization -o briefing_openai.md

# Topic briefing (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Quantum computing" --typ topic

# Event (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "COP30" --typ event

# Without type (generic) (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "My topic"

# Help (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py --help
```

---

## Типы брифингов и разделы

| Тип | Разделы |
|---|---|
| `person` | Основные данные, биография/предыстория, работа и вклад, источники, заметки |
| `organization` | Профиль, история, продукты/услуги, ключевые фигуры, источники, заметки |
| `topic` | Обзор, предыстория/контекст, текущие события, ключевые источники, открытые вопросы, заметки |
| `event` | Ключевые факты, участники, предыстория/хронология, значение, источники, заметки |
| `unspecified` | Обзор, предыстория, детали, источники, заметки |

---

## Хранилище

Без постоянного хранилища. Каркас только выводится (в stdout или файл)
и не сохраняется в базе данных.

---

## Принципы работы

- Всегда подчеркивать, что каркас пуст и должен быть заполнен в ходе исследования.
- Никогда не выдумывать контент и не галлюцинировать — предоставлять только структуру.
- Если тип непонятен, уточнить у пользователя или использовать `unspecified`.

---

## Конфиденциальность

Без доступа к сети. Без хранилища. Исключительно локальная обработка.

---

## Связанные ресурсы

- `research-agent` — заполняет каркас брифинга результатами исследований
- `web-reading` — считывает веб-страницы и извлекает контент для брифинга

---

## Журнал изменений

| Версия | Дата | Изменение |
|---|---|---|
| 1.0.0 | 2026-06-22 | Создано из BACH dossier_generator.py v1.0.0; хранилище удалено, обобщено |