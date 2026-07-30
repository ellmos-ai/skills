---
name: reiseroute
version: 1.0.0
category: assist
description: Планирование маршрута из A в B с помощью OSRM (Open Source Routing Machine). Поддерживает автомобиль, велосипед и пешеходный режим. API-ключ не требуется.
tags: [routing, navigation, osrm, openstreetmap, reise]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['urllib.request', 'urllib.parse', 'urllib.error', 'json']}
runtime: python3
entry_point: reiseroute_core.py
provenance: {'origin': 'BACH hub routing-service', 'origin_path': 'system/hub/_services/routing/routing_service.py', 'origin_version': '1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': 'urllib.parse-Import an den Kopf verschoben (war im Original nur im else-Zweig). geocode_place (Nominatim) integriert. Keine Origin-DB. Kein Store. Userneutral, headless, nur Stdlib.\n'}
language: ru
---

<img src="banner.png" width="100%" alt="reiseroute banner">

> **Русский** — Официальная русская версия `reiseroute`.


# Travel Route (Русский)

**Планирование маршрута с помощью OSRM (Open Source Routing Machine)**

---

## Обзор и назначение

Планирует маршруты между двумя точками (названиями или координатами) через публичный
сервис OSRM (`router.project-osrm.org`). Возвращает расстояние, время в пути и
способ передвижения. Без API-ключа, без аккаунта.

---

## Триггеры

| Фраза | Действие |
|---|---|
| «Спланируй маршрут из Берлина в Гамбург» | Автомобильный маршрут, геокодирование названий мест |
| «Сколько времени займет поездка на машине из Мюнхена в Вену?» | Автомобильный маршрут + время |
| «Веломаршрут из Потсдама в Берлин» | Велосипедный режим |
| «Пешком из Кройцберга в Митте, Берлин» | Пешеходный режим |
| «Маршрут от 52.52,13.41 до 53.55,9.99» | Прямые координаты |

---

## Рабочий процесс и порядок действий

1. **Извлечь пункт отправления и назначения** из пользовательского ввода.
2. **Определить режим:** автомобиль (по умолчанию), велосипед, пешком.
3. **Геокодировать:** названия мест → координаты через Nominatim.
4. **Запросить OSRM:** возвращает расстояние (км) + продолжительность (отформатированную).
5. **Вывести результат:** краткую текстовую сводку.

---

## CLI

```bash
# Автомобильный маршрут между двумя пунктами (Русский)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Berlin" "Hamburg"

# Велосипед (Русский)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Potsdam" "Berlin" --modus fahrrad

# Пешком (Русский)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Kreuzberg, Berlin" "Mitte, Berlin" --modus fuss

# Прямое использование координат (lat,lon) (Русский)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "52.5200,13.4050" "53.5500,9.9937"

# Вывод в JSON (Русский)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Munich" "Vienna" --json

# Справка (Русский)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py --help
```

---

## Режимы

| Режим | Псевдонимы | Профиль OSRM |
|---|---|---|
| auto (по умолчанию) | car, pkw, fahren | driving |
| fahrrad | bike, rad, radfahren | cycling |
| fuss | foot, laufen, gehen, zu fuss | foot |

---

## Хранилище

Без постоянного хранилища. Маршруты не сохраняются.

---

## Поведение

- Всегда указывайте пункт отправления и назначения перед расчетом.
- Уточняйте при неоднозначности названия места (например, «Вена» = Австрия или город с таким же названием?).
- Примечание: OSRM предоставляет кратчайший маршрут без учета дорожной ситуации в реальном времени.
- Выводите предупреждение для очень длинных пешеходных маршрутов (> 20 км).

---

## Конфиденциальность

Запросы отправляются в `nominatim.openstreetmap.org` (геокодирование) и
`router.project-osrm.org` (маршрутизация). Без входа в систему, без API-ключа,
без постоянного хранения данных.

---

## Связанные ресурсы

- `location-suche` — Поиск POI (также использует Nominatim)
- `wetter` — Погода в пункте назначения

---

## Журнал изменений

| Версия | Дата | Изменение |
|---|---|---|
| 1.0.0 | 2026-06-22 | Создано на основе BACH routing_service.py v1.0; интегрировано геокодирование |