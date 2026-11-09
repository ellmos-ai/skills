---
name: mcp-config-sync
version: 2.0.0
type: skill
author: Lukas Geiger + Claude + Codex
created: 2026-05-16
updated: 2026-11-09
description: "Используйте для поиска, планирования и синхронизации конфигураций серверов Model Context Protocol (MCP) между несколькими агентами (например, 'синхронизировать MCP-серверы', 'согласовать настройки MCP', 'перенести MCP-серверы', /mcp-config-sync). Находит установленные серверы MCP и согласует конфигурации без жесткого центрального узла. НЕ используйте при необходимости полной синхронизации навыков и правил (используйте agent-config-sync)."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [mcp, config, sync, provider-neutral, discovery, multi-agent]
language: ru
status: active
dependencies: {'tools': ['python'], 'services': [], 'protocols': ['agent-config-sync'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'skills/infrastructure/mcp-config-sync/', 'origin_version': '2.0.0', 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---


<img src="banner.png" width="100%" alt="mcp-config-sync banner">

> **Русский** — Официальная русская версия `mcp-config-sync`.


# MCP Config Sync (Русский)

Это ориентированная на MCP точка входа в `agent-config-sync`. Она не предполагает
наличия какого-либо определенного провайдера, приложения или мастер-файла.

1. Уточнить, какие именно конечные точки или оси нужны пользователю: в рамках одного провайдера
   между классами приложений, в рамках одного класса приложений между провайдерами, явный список
   или все обнаруженные провайдеры и классы.
2. Выполнить `agent-config-sync/scripts/sync.py --discover`, затем `--offer`.
3. Представить обнаруженные конечные точки отдельно от непроверенных кандидатов.
4. Предоставить пользователю выбор источника правды, целей, направления и политики конфликтов.
5. Материализовать `registry.json`, проверить `--plan`, и только после этого использовать
   `--apply --yes`.

Обнаружение и предложения работают только на чтение. Не существует неявного хаба и неявной
«полной синхронизации». Прежние скрипты Claude Code↔Claude Desktop являются устаревшим профилем,
а не универсальным стандартом по умолчанию.