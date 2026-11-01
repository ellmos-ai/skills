---
name: protection-shield
version: 1.0.0
type: skill
author: Lukas Geiger + Codex
created: 2026-10-25
updated: 2026-10-25
description: "Координирует разрешённую срочную защиту и периодические проверки журналов и стека с доказательствами и возвратом."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [defense, incident-response, server, logs, monitoring]
language: ru
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [tech-detect, security-tech-stack-check], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="protection-shield banner">

# protection-shield

Только для собственных или явно разрешённых систем, сетей и серверов. Перед изменением проверить актив, владельца, полномочия, блокировки, последствия и откат. Сигнал тревоги не даёт права менять продуктивную сеть. Никаких контратак, чужих активов и неразрешённого сканирования.

При инциденте сохранить время UTC, ограниченные нужные журналы и хеши конфигурации; скрыть секреты, отличить симптомы от подтверждённого взлома. Прочитать runbook, действующие решения и частное действие для актива. При конкретном разрешении использовать существующие локальные инструменты для указанного сервиса, правила межсетевого экрана, одобренной ротации доступа либо патча через security-tech-stack-check. Зафиксировать цель и возврат; отдельно проверить результат, работу, эффект в логах, последствия и откат.

Для периодической проверки частный профиль перечисляет активы, разрешённые читатели логов/API, окно, фильтры, срок хранения, снимок tech-detect, расписание и адресата. Подключить существующий планировщик, не создавать новый демон. Каждый запуск ограничивает источники и время, удаляет дубликаты и проверяет текущие рекомендации через security-tech-stack-check. Отражать покрытие и ошибки; только фактические записи планировщика и результата подтверждают работу.

Для периодической проверки одного сервера сравнивать прошлый и текущий tech-detect снимки без смены slot и hostname. Проверить axis=same-host-time, chronology, оба времени, покрытие и неизвестные версии. Не переименовывать хост ради обхода проверки; при отсутствии происхождения — HOLD.
