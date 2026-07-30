---
name: skill-family-care
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-07-30
description: >
  Навык обслуживания, который поддерживает семейства навыков в актуальном состоянии без запуска полного
  аудита skill-explorer. Используйте этот навык при назначении нового навыка в правильное семейство,
  обновлении роутера заголовка семейства после изменений или удалении осиротевшего роутера. Также вызывает
  при командах "обслужить семейства", "назначить новый навык в семейство", "обновить роутер", "установить/удалить заголовок семейства".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, familien, pflege, routing, meta]
language: ru
status: active

dependencies:
  tools: []
  services: []
  protocols: [skill-explorer, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-family-care/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="skill-family-care banner">
# Обслуживание семейств навыков (Skill-Family-Care)

## Назначение

Поддерживает **семейства** навыков в актуальном состоянии — без запуска полного цикла аудита `skill-explorer`. Выделен по принципу инсталлятора (компактный поднавык вместо монолита). Ссылается на скрипты из `skill-explorer`, не копируя их.

## Источники (не дублировать)

- **Список семейств:** `<USER_HOME>\OneDrive\.USR\SKILL-MAP.md` (каноническая карта семейств и маршрутизации).
- **Инвентарь (текущее состояние):** `skill-explorer/scripts/inventory_skills.py`.
- **Установка/Удаление роутера:** `skill-explorer/scripts/inject_family_header.py`.
- **Конфигурация (связанные семейства):** `~/.claude/skills/skill-explorer/config.json`.

## Задачи

### A — Назначение нового навыка в семейство
1. Заново собрать инвентарь:
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
2. Выбрать подходящее семейство из `SKILL-MAP.md` (Оси: Фаза/Широта/Жесткость/Воздействие/Сырье).
3. Зарегистрировать навык как участника в `config.json` (`families[<fam>].members`) и в `SKILL-MAP.md`.

### B — Обновление роутера заголовка после изменения семейства
```bash
PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inject_family_header.py \
    --family <Familie> --skills s1,s2,s3 --router "<Wegweiser>" --inventory ~/.skill-inventory.json
```
- Идемпотентно: существующий блок того же семейства заменяется.
- Изменяются только навыки типа `editable`/`source=user` (защитный шлюз внутри скрипта).

### C — Удаление осиротевшего роутера
Тот же скрипт с флагом `--remove` (параметр `--router` не требуется).

## Железные правила

- **Обследование ≠ Мутация (Survey ≠ Mutation):** только собственные навыки пользователя получают заголовки. Никогда не трогать плагины или внешние навыки.
- После каждого изменения обновлять `config.json` (`families[*].linked`, `updated`).
- Не копировать содержимое из карты семейств в отдельные навыки — только вставлять блок указателя.

## История изменений

### 0.1.0 (2026-06-17)
- Первоначальная версия. Создана в режиме аудита (P1).
