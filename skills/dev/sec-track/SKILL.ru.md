---
name: sec-track
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Делает валидированные находки безопасности отслеживаемыми: после предпросмотра и подтверждения создаёт тикет (ticket_writer.py), GitHub issue или черновик security advisory (gh), сначала проверяет дубликаты по id находки, не допускает секретов в тексте и записывает ссылку обратно в finding.ticket. Триггеры: 'отследить эту находку', 'тикет для SEC-...', 'создать advisory', 'занести находки в бэклог'. Без Linear/Jira. Не для технических отчётов (sec-report) и не для раскрытия вовне (sec-writeup)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, tickets, tracking, github, advisory]
language: ru
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-track - сделать находки отслеживаемыми

Фаза «track». Контракт: `sec-scan/references/contract.md` (правило 4 секреты, правило 8 тикеты в §6; поле `ticket` в `schemas/finding.schema.json`). Только находки со статусом `validated` и выше - `candidate` не отслеживается.

## Выбрать цель

| Цель | Когда | Инструмент |
|---|---|---|
| Тикет в системе тикетов пользователя | по умолчанию, приватно, без эффекта вовне | `ticket_writer.py` из ticket-master |
| GitHub issue | только **приватные** репозитории или чисто hardening-пробелы без пути эксплуатации | `gh issue create` |
| Черновик security advisory | уязвимость в **публичном** репозитории | `gh api` (repository security advisories, черновик) |

**Публичный репозиторий + эксплуатируемая находка: никогда публичный issue** - это было бы раскрытием (egress, правило 6). Там использовать черновик advisory или приватный тикет. Без Linear, без Jira.

## Процедура

1. **Выбрать:** какие находки, какая цель. По одной, а не массовым тикетом, чтобы у каждого id была собственная ссылка.
2. **Проверка дубликатов по id находки** (`SEC-<12 hex>`): установлен ли уже `finding.ticket`? Искать id в каталогах тикетов; на GitHub `gh issue list --state all --search "<id>"`. При совпадении использовать существующую ссылку и ничего нового не создавать.
3. **Составить текст:** id, заголовок, правило/CWE, серьёзность, расположение (`path:line`), краткое воздействие, рекомендация, указание на файл патча, если он есть. **Никогда секретное значение** (правило 4): только расположение. Деталей эксплойта не больше необходимого.
4. **Показать предпросмотр и дождаться подтверждения.** Только затем создавать - тикеты, issue и advisory имеют эффект вовне или не могут быть отозваны.
5. **Создать:**
   - Тикет (id никогда не выбирать вручную, правило 8): `python <ticket-master>/lib/ticket_writer.py --title "<SEC-id> <заголовок>" --body "<текст>" --project <проект> --priority <уровень>`; CLI выводит путь созданного файла тикета. В документации модуля иногда указано `--urgency`; сама CLI знает `--priority` - перед использованием прочитать `--help`.
   - Issue: `gh issue create --repo <owner/repo> --title ... --body-file <файл>`.
   - Advisory: черновик через REST-интерфейс GitHub для repository security advisories (`gh api`); точные поля перед использованием проверить в документации GitHub (открыто, здесь не зафиксировано). Оставить как черновик, не публиковать.
6. **Записать ссылку обратно:** `finding.ticket` = путь/id тикета, `owner/repo#nr` или ссылка на advisory; затем `python scripts/secfind.py validate findings.json coverage.json` (скрипт в `sec-scan`).

## Changelog

### 0.1.0 (2026-10-31)
- Первая версия.
