---
name: mcp-config-sync
version: 2.0.0
type: skill
author: Lukas Geiger + Claude + Codex
created: 2026-05-16
updated: 2026-07-27
description: Нейтральная к провайдерам точка входа для обнаружения, планирования и синхронизации конфигурации MCP между выбранными пользователем провайдерами и классами приложений. Пользователь выбирает источник правды, цели и область охвата; ни один провайдер не является неявным хабом.

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