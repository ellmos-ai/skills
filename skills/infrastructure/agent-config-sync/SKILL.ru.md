---
name: agent-config-sync
version: 0.3.0
type: protocol
author: Lukas Geiger + Claude + Codex
created: 2026-06-20
updated: 2026-11-09
description: "Используйте для планирования и синхронизации настроек MCP-серверов, навыков и файлов правил между разными фреймворками агентов (например, 'синхронизировать настройки агентов', 'согласовать MCP между инструментами', 'зеркалировать навыки', /agent-config-sync). Находит локальные конфигурации и дает пользователю выбрать источник правды и разрешение конфликтов. НЕ используйте для синхронизации только MCP (используйте mcp-config-sync)."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, skills, rules, sync, provider-neutral, discovery, multi-agent]
language: ru
status: active
aliases: [mcp-skill-sync, multi-agent-sync, tool-config-sync, agent-sync]
dependencies: {'tools': ['python'], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/agent-config-sync/', 'origin_version': '0.3.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---


<img src="banner.png" width="100%" alt="agent-config-sync banner">

> **Русский** — Официальная русская версия `agent-config-sync`.


# Agent Config Sync (Русский)

Данный навык разделяет выбор конечных точек (endpoints), ресурсы и источник истины (truth). Запуск:

```bash
python scripts/sync.py --discover
python scripts/sync.py --offer
```

Пользователь может выбрать явный список конечных точек, одного провайдера для всех классов приложений, один класс приложений для всех провайдеров или все обнаруженные конечные точки. Обнаружение является подтверждением наличия (evidence), а не авторизацией.

Источником истины (truth) может быть одна конечная точка, один файл, упорядоченный набор файлов (например, несколько уровней `AGENTS.md`) или каталог навыков. Ни одно имя файла или провайдер не является неявным хабом. Без выбранного источника истины планирование остается заблокированным.

Проверьте `--status` и `--plan`; используйте `--apply --yes` только после одобрения. Реализована поддержка блоков MCP и каталогов навыков. Топологии файлов правил остаются закрытыми при сбое (fail-closed), пока пользователь не выберет адаптер слияния/перенаправления.