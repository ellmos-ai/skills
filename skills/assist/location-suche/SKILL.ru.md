---
name: location-suche
version: 1.0.0
category: assist
description: Поиск мест, ресторанов и отелей через OpenStreetMap (Nominatim + Overpass API). Возвращает POI (точки интереса) неподалеку от указанного места или выполняет поиск по произвольному тексту.
tags: [location, openstreetmap, poi, nominatim, overpass, restaurant, hotel]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['urllib.request', 'urllib.parse', 'urllib.error', 'json', 'time']}
runtime: python3
entry_point: location_suche_core.py
provenance: {'origin': 'BACH persoenlicher-assistent', 'origin_path': 'system/agents/persoenlicher-assistent/tools/location_search.py', 'origin_version': '1.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': 'Alle Origin-DB-Abhaengigkeiten entfernt (save_location, list_locations, _ensure_table, _get_db). Kein Store. Userneutral (keine privaten Pfade). Headless, nur Stdlib.\n'}
language: ru
---

<img src="banner.png" width="100%" alt="location-suche banner">

> **Русский** — Официальная русская версия `location-suche`.


# Поиск мест (Русский)

**Поиск мест, ресторанов и отелей через OpenStreetMap**

---

## Обзор и назначение

Выполняет поиск ресторанов, отелей, кафе и других мест с использованием
сервисов OpenStreetMap: Nominatim (геокодирование) и Overpass (поиск POI).
API-ключ не требуется. Без постоянного хранилища.

---

## Триггеры

| Фраза | Действие |
|---|---|
| "Find a restaurant in Munich" («Найди ресторан в Мюнхене») | Поиск POI: category=restaurant, near=Munich |
| "Hotels near Vienna" («Отели рядом с Веной») | Поиск POI: category=hotel, near=Vienna |
| "Where is the Eiffel Tower?" («Где находится Эйфелева башня?») | Поиск по произвольному тексту в Nominatim |
| "Find cafes in Berlin" («Найди кафе в Берлине») | Поиск POI: category=cafe, near=Berlin |
| "Search for pharmacy near Potsdam" («Найти аптеку рядом с Потсдамом») | Поиск POI: category=pharmacy, near=Potsdam |

---

## Рабочий процесс и порядок действий

1. **Определение триггера:** Содержит ли запрос категорию (ресторан, отель и т. д.)
   и местоположение → шаг 2. В противном случае поиск по произвольному тексту → шаг 4.
2. **Геокодирование местоположения:** Nominatim предоставляет координаты для указанного места.
3. **Поиск POI:** Overpass API ищет заведения выбранной категории в заданном радиусе.
4. **Отображение результатов:** Список с названием, адресом и расстоянием (м).
5. **Поиск по произвольному тексту (резервный вариант):** Прямой поиск Nominatim по произвольному тексту дает точные совпадения.

---

## CLI

```bash
# POI search (category + location) (Русский)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py restaurant München

# Geocode location (Русский)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py --geocode "Brandenburg Gate Berlin"

# Adjust radius (default: 1000 m) (Русский)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py hotel Wien --radius 2000

# Help (Русский)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py --help
```

---

## Хранилище

Без постоянного хранилища. Результаты только отображаются, но не сохраняются.

---

## Поддерживаемые категории

restaurant, cafe, bar, pub, fast_food, hotel, hostel, guest_house, supermarket,
pharmacy, hospital, bank, atm, fuel, parking, bus_stop, train_station, museum,
cinema, theatre, library, school, university, church

---

## Поведение

- Всегда запрашивайте у пользователя местоположение, если оно не было указано.
- Если результатов больше 10, показывайте только 5 ближайших, остальные — по запросу.
- Указывайте расстояние в метрах, начиная с 1 км — в км (с 1 десятичным знаком).
- Конфиденциальность: данные о местоположении не сохраняются и не передаются никуда,
  кроме публичных API Nominatim/Overpass (openstreetmap.org).

---

## Конфиденциальность

Поисковые запросы отправляются на `nominatim.openstreetmap.org` и `overpass-api.de`.
Без входа в систему, без API-ключа, без постоянного хранения данных.
User-Agent настроен в соответствии с политикой Nominatim.

---

## Связанные ресурсы

- `reiseroute` — планирование маршрута от A до B (также использует Nominatim для геокодирования)
- `wetter` — погода в текущем местоположении

---

## История изменений

| Версия | Дата | Изменение |
|---|---|---|
| 1.0.0 | 2026-06-22 | Создано на основе BACH location_search.py v1.1.0; хранилище удалено |