---
name: staircase-routing
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: >
  Изолированная стратегия навигации и маршрутизации, которая выполняет поиск вверх и вниз
  по иерархии директорий для обнаружения указательных документов (CLAUDE.md, AGENTS.md,
  README.md, RULES.md) и настраиваемых пользователем ключевых слов (через staircase-config.json
  или config.json). Также известна как Up-and-Down Routing или Walking Bass Routing.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [routing, staircase-routing, up-and-down-routing, walking-bass-routing, signpost, navigation, directory-traversal]
language: ru
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
---

<img src="banner.png" width="100%" alt="staircase-routing banner">

> **Русский** — Официальная русская версия `staircase-routing`.

# Staircase-Routing (Up-and-Down / Walking Bass Маршрутизация)

Навык **Staircase-Routing** (также называемый *Up-and-Down Routing* или *Walking Bass Routing*) изолирует стратегию проверки документов в директориях для ИИ-агентов.

Когда агент переходит в директорию или работает с файлом, он использует эту стратегию для поиска авторитетного контекста, правил и указательных документов перед изменением кода или выполнением действий.

---

## 1. Стандарты указательных документов

По умолчанию Staircase-Routing ищет стандартные указательные документы:
- **Глобальные настройки и управление проектом:** `CLAUDE.md`, `AGENTS.md`, `START.md`, `RULES.md`
- **Обзор проекта и задачи:** `README.md`, `TODO.md`, `NOTIZ.md`, `BEWEISNOTIZ.md`
- **Пользовательские ключевые слова:** Настраиваются через `staircase-config.json` или `config.json`.

---

## 2. Алгоритм обхода

```
                           [ Root / Workspace Level ]
                           ┌────────────────────────┐
                           │   CLAUDE.md / RULES.md │ ◄── (Step 2: Read Root Signpost)
                           └───────────▲────────────┘
                                       │ (Staircase Up)
                           ┌───────────┴────────────┐
                           │ Subfolder / Target Dir │ ◄── (Step 1: Start at CWD)
                           └───────────┬────────────┘
                                       │ (Staircase Down)
                           ┌───────────▼────────────┐
                           │ Child / Module Dir     │ ◄── (Step 3: Discover Sub-Signposts)
                           │   module-rules.md      │
                           └────────────────────────┘
```

### Шаг 1: Проверка текущей рабочей директории (CWD)
- Проверить директорию целевого файла или активную рабочую директорию.
- Если указательные документы существуют, немедленно прочитать их.

### Шаг 2: Обход вверх (Staircase Up)
- Если в CWD **не** найдено ни одного указательного документа, подняться в родительскую директорию (`..`).
- Пошагово повторять перемещение вверх до тех пор, пока не будет найден корневой указательный документ (`CLAUDE.md` или `AGENTS.md`) или достигнута граница рабочей области.
- Прочитать все обнаруженные корневые указатели для установления глобальных директив и правил проекта.

### Шаг 3: Проверка вниз (Staircase Down)
- Из установленной корневой директории спуститься в дочерние директории, относящиеся к задаче.
- Обнаружить специализированные указатели уровня модулей, правила домена или конфигурации компонентов и прочитать их.

---

## 3. Пользовательские ключевые слова (`staircase-config.json`)

Агенты могут читать локальный или глобальный `staircase-config.json` для настройки целевых указателей:

```json
{
  "signpost_filenames": [
    "CLAUDE.md",
    "AGENTS.md",
    "START.md",
    "RULES.md",
    "README.md",
    "TODO.md"
  ],
  "custom_buzzwords": [
    "SECURITY",
    "POLICY",
    "GOVERNANCE",
    "PIPELINE"
  ],
  "max_upward_depth": 10,
  "exclude_directories": [
    "node_modules",
    ".git",
    "__pycache__",
    "dist",
    "build",
    "archive"
  ]
}
```

---

## 4. Интеграция с `letter-hooker` и запланированными задачами

`staircase-routing` встроен как базовый предполётный загрузчик (preflight bootloader) в навык **`letter-hooker`** и запланированную задачу **`antigravity-kontext-and-workflow-loader-and-divider`**, гарантируя, что агенты всегда находят и соблюдают указательные документы перед началом внесения изменений.