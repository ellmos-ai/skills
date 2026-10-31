---
name: sec-report
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Формирует отчёт по безопасности report.md (с группировкой по серьёзности, раздел покрытия с пробелами, отклонённые находки отдельно, сводка без приукрашивания) и findings.sarif (SARIF 2.1.0) из findings.json и coverage.json с помощью скрипта render_report.py. Использовать для 'написать отчёт по безопасности', 'подвести итог сканирования', 'экспортировать SARIF', 'отчёт для code scanning'. Прерывается при некорректных данных; частичное сканирование сообщается как частичное. Новые находки: sec-scan / sec-diff-scan. Проверка: sec-validate. Классификация: sec-triage."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, report, sarif, coverage, findings]
language: ru
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-report

Завершающая фаза семейства навыков безопасности ellmos. Контракт: `sec-scan/references/contract.md` (файлы 1, серьёзность 3, покрытие 5, правила 6). Скрипт импортирует `seclib` из соседней папки `sec-scan/scripts` (в репозитории `skills/dev/` и при плоском развёртывании `~/.claude/skills/`; обе папки должны лежать рядом). Только стандартная библиотека.

## Использование

```
python scripts/render_report.py FINDINGS COVERAGE OUTDIR [--lang de|en]
```

Интерпретатор вызывать явно. `OUTDIR` - каталог сканирования; сначала проверить блокировку, как на шаге 2 `sec-scan` (fail-closed). Результат: `OUTDIR/report.md` и `OUTDIR/findings.sarif`. Коды возврата: 0 = записано, 1 = вход нечитаем или некорректен (**ничего** не записано), 2 = неверное использование. Показать код возврата и вывод. Язык отчёта по умолчанию - немецкий; для английского использовать `--lang en`.

## Поведение

- **Сначала валидирует** (`seclib.validate_findings`). Ошибки перечисляются, и из повреждённых данных отчёт не создаётся. Сначала устранить причину (`sec-scan`, `sec-validate`), затем отрендерить снова.
- **report.md:** заголовок (цель, ref, сканер) · сводка · предупреждения · находки по серьёзности (от critical до info) с расположением, уверенностью, статусом, валидатором, доказательствами, описанием, воздействием, рекомендацией, тикетом · **отклонённые находки отдельно** с причиной · покрытие (отсканировано с глубиной, не отсканировано с причиной, ограничения).
- **Честность (контракт 5, 6.9):** `complete: false` отображается в самом начале как «PARTIAL SCAN». Отсутствие находок при неполном покрытии читается как «NOT a clean result». Лишь «No findings with complete coverage» может читаться как чистый результат. Предупреждения, например тот же провайдер для нашедшего и валидатора, отображаются в отчёте.
- **findings.sarif:** SARIF 2.1.0 через `seclib.to_sarif`; отклонённые находки остаются в журнале как `suppressions`. Пригоден напрямую для загрузки в code scanning. Загрузка - это публикация вовне и требует распоряжения пользователя.

## Перед передачей дальше

Перечитать отчёт: без секретных значений (валидатор ловит лишь распространённые шаблоны; контракт 6.4), только расположения. Отчёты в системах тикетов и чатах - также без значений. Об уязвимостях в публичных репозиториях сообщают через приватный канал (SECURITY.md), а не через публичный issue.

## Тест

`python -m pytest tests -q -p no:cacheprovider` в папке навыка (отчёт, SARIF, частичное сканирование, доказательства с обратными кавычками, негативный случай без вывода).

## Changelog

### 0.1.0 (2026-10-31)

- Первая версия с `render_report.py`: report.md и findings.sarif из валидированных данных.
