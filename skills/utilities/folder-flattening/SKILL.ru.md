---
name: folder-flattening
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Реструктуризация вложенных иерархий папок в плоские, машиночитаемые структуры. На базе Bash с интеллектуальной логикой объединения.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [folder, flattening, filesystem, bash, reorganization, cleanup]
language: ru
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/ordner-flattening.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="folder-flattening banner">

> **Русский** — Официальная русская версия `folder-flattening`.

# Рабочий процесс: Folder Flattening

Цель: Преобразовать вложенные структуры папок в плоскую, машиночитаемую структуру.
Преимущество: Больше никакого ручного перехода по каталогам — поиск через базу данных (`Verzeichnis.db`).
Дубликаты допускаются, если они оправданы тематически.

---

## Обзор фаз

| Фаза | Что происходит | Раздел скрипта |
|-------|-------------|----------------|
| 1 | Сплющивание (Flatten): Перенос всех подпапок на один уровень | `phase_flatten` |
| 2 | Сокращение (Shorten): Усечение длинных путей до последнего сегмента, объединение при конфликтах | `phase_shorten` |
| 3 | Очистка: Устранение множественных подчеркиваний (`___`), удаление концевого `_` | `phase_cleanup_underscores` |
| 4 | Группировка: Перемещение числовых папок, CD-папок и коротких имен в сборные папки | `phase_group_problematic` |
| 5 | Анализ триплетов: Скользящие группы по 3, кратчайшее имя как цель объединения | `phase_tripel_merge` |
| 6 | Объединение по формату медиа: Консолидация папок по типу файлов (шаблон) | `phase_media_merge` |
| 7 | Очистка: Удаление пустых папок | `phase_cleanup_empty` |

---

## Важные правила

### Сопоставление в анализе триплетов
- **Подстрока**: `Education` в `EducationalBrochures` -> объединить в `Education`
- **Множественное число/умлаут**: `Room` = `Rooms`, `Part` = `Parts`, `Book` = `Books`
- **Первое слово**: `Autism ADHD` совпадает с `Autism Career` (одинаковое начало)

### Минимальная длина
- Односложное имя без пробелов: **не менее 8 символов** (предотвращает случайное объединение `Hand`, `House`, `Form`)
- С пробелами (например, `ICF Catalog`): **от 3 символов OK**
- Это позволяет сохранить `ICF`, `ASD Women` и т.д.

### Перезапуск после объединения
После каждого объединения список папок перезагружается и перезапускается с целевой папки объединения.
Таким образом, например, `Autism` собирает все расширения перед тем, как двигаться дальше.

---

## Объединение по формату медиа (Система шаблонов)

Фаза 6 использует массив шаблонов `MEDIA_TYPES`. Каждая запись определяет:
- Целевую папку (с префиксом `_`)
- Расширения файлов, относящиеся к этому типу

```bash
MEDIA_TYPES=(
    "_Audio|mp3|m4a|wav|flac|ogg|wma|aac|opus|aiff"
    "_Video|mp4|avi|mkv|mov|wmv|flv|webm|m4v|mpg|mpeg|3gp"
    "_Images|jpg|jpeg|png|gif|bmp|tiff|tif|webp|svg|ico|heic|heif|raw|cr2|nef"
    # Extensible:
    # "_Spreadsheets|xlsx|xls|csv|ods"
    # "_Presentations|pptx|ppt|odp"
    # "_Code|py|js|ts|sh|bat|ps1"
    # "_CAD|dwg|dxf|step|stl"
    # "_3D|obj|fbx|blend|gltf|glb"
    # "_Fonts|ttf|otf|woff|woff2"
)
```

Перемещаются только папки, содержащие **исключительно** файлы одного типа.
Папки с подпапками пропускаются.

### Добавление нового типа медиа

Просто добавьте новую строку в массив `MEDIA_TYPES`:
```bash
"_TargetFolder|ext1|ext2|ext3"
```

---

## Выполнение

```bash
# Complete run:
cd /path/to/target/directory
bash ordner_flattening_komplett.sh

# Or individual phases:
bash ordner_flattening_komplett.sh --phase flatten
bash ordner_flattening_komplett.sh --phase tripel
bash ordner_flattening_komplett.sh --phase media
bash ordner_flattening_komplett.sh --phase cleanup
```

---

## Опытные данные (Сессия 2026-01-26)

- Старт: 206 папок + 252 отдельных файла, ~5600 вложенных подпапок
- После сплющивания: ~2200 папок на одном уровне
- После сокращения и очистки: ~2005 папок
- После группировки (числа, CD): ~2005 -> созданы сборные папки
- После триплетов v1: ~1561 папка
- После триплетов v2 (правило 8 символов): дальнейшее сокращение
- Фаза медиаформатов: Папки аудио/видео/изображений консолидированы