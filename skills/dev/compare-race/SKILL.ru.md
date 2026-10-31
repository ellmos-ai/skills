---
name: compare-race
version: 1.0.0
type: pointer
author: Lukas Geiger
created: 2026-08-16
updated: 2026-08-16
description: "Используйте, когда пользователь хочет отправить один и тот же промпт нескольким LLM и сравнить их ответы — последовательно (секундомер, отдельный точный замер времени для каждой дорожки) или параллельно (настоящая гонка), с необязательными повторами для каждой модели. Стартовая модель оценивает качество, правильность, полноту, следование инструкциям и задержку (время — лишь один из критериев). Вызывается командами /compare-race, «model race», «сравни модели», «отправь один и тот же промпт нескольким моделям»."
standalone: true
anthropic_compatible: true
bach_compatible: false
category: dev
tags: [model-comparison, race, benchmark, multi-agent, judge, workflow]
language: ru
status: active
visibility: public
pointer: {'module_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race', 'prompt_de': 'prompts/RACE-STARTER.de.md', 'prompt_en': 'prompts/RACE-STARTER.en.md', 'config': 'config/compare-race.config.example.json', 'repo': 'github.com/ellmos-ai/compare-race'}
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['system-auditor'], 'optional_tools': [{'name': 'coma', 'path': '.AI/.MODULES/.ORCHESTRATION/coma/', 'python_module': 'coma', 'usage': 'Ausfuehrungsschicht fuer compare-race run (Spawn/Polling/Dateiprotokoll)', 'note': 'Optional. Ohne coma laeuft der modellmanuelle Weg: Spuren selbst ausfuehren und mit compare-race record einreichen.'}]}
provenance: {'origin': 'module', 'origin_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race/prompts/RACE-STARTER.de.md', 'origin_version': '0.1.0', 'last_sync_from_origin': '2026-08-16', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
translated_from_sha256: eef2d1e681ca3ed6c7fe63a8a36535632cf48a7b990fd8d944c8ef42ea046750
translator: "claude-haiku-5-5; revision:gpt-6-sol"
translated_at: "2026-10-15T12:47:04.786270+00:00"
---
<img src="banner.png" width="100%" alt="compare-race banner">

# compare-race — скилл-указатель (немецкий)

> **Этот скилл служит только указателем. Источник истины — модуль.**

## Путь к модулю

```
<HOME>\OneDrive\.TOPICS\.AI\.MODULES\.ORCHESTRATION\compare-race\
```


Репозиторий: [github.com/ellmos-ai/compare-race](https://github.com/ellmos-ai/compare-race)

## Инструкция для агента

1. Прочитай ролевой промпт **`prompts/RACE-STARTER.de.md`** в папке модуля и следуй ему.
   Ты — RACE-STARTER и по умолчанию также **Judge** (решение пользователя
   от 2026-08-16).
2. Проверь конфигурацию (`compare-race config`; конфигурация хоста находится в `~/.compare-race/`).
   Выбери режим: `sequential` = секундомер (отдельный точный замер для каждой дорожки) ·
   `parallel` = настоящая гонка. **Секундомер — лишь образ**: время — один
   из критериев наряду с качеством, правильностью, полнотой, следованием инструкциям и стоимостью.
3. Запусти гонку (`compare-race run --prompt-file …`); без модуля coma сам выполни
   дорожки для каждой модели и отправь результаты через `compare-race record`.
4. Как Judge, заполни критерии оценки в `RACE.md` папки гонки — сам прочитай
   каждый файл RUN; укажи возможную предвзятость, если твоя собственная модель участвует.
5. Делай выводы о причине различий только в том случае, если варьируется ровно одна ось
   (model = гонка · run = разброс · time = дрейф модели).

## Предупреждение о квотах

Гонки расходуют квоту **каждого** задействованного провайдера (claude/codex/agy/kimi).
Перед крупными гонками (много дорожек × повторов) спроси пользователя.
