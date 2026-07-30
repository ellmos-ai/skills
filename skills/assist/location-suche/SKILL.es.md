---
name: location-suche
version: 1.0.0
category: assist
description: Búsqueda de ubicaciones, restaurantes y hoteles a través de OpenStreetMap (Nominatim + Overpass API). Devuelve Puntos de Interés (POI) cerca de una ubicación o realiza búsquedas por texto libre.
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
language: es
---

> **Español** — Versión oficial en español de `location-suche`.


# Búsqueda de Ubicaciones (Español)

**Búsqueda de ubicaciones, restaurantes y hoteles a través de OpenStreetMap**

---

## Visión general y propósito

Busca restaurantes, hoteles, cafeterías y otros lugares utilizando los
servicios de OpenStreetMap: Nominatim (geocodificación) y Overpass (búsqueda de POI).
No se requiere clave de API. Sin almacenamiento persistente.

---

## Activadores

| Frase | Acción |
|---|---|
| "Encuentra un restaurante en Múnich" | Búsqueda de POI: category=restaurant, near=Munich |
| "Hoteles cerca de Viena" | Búsqueda de POI: category=hotel, near=Vienna |
| "¿Dónde está la Torre Eiffel?" | Búsqueda por texto libre en Nominatim |
| "Encuentra cafeterías en Berlín" | Búsqueda de POI: category=cafe, near=Berlin |
| "Buscar farmacia cerca de Potsdam" | Búsqueda de POI: category=pharmacy, near=Potsdam |

---

## Flujo de trabajo y procedimiento

1. **Detectar activador:** ¿Contiene la solicitud una categoría (restaurante, hotel, etc.)
   y una ubicación? → paso 2. De lo contrario, texto libre → paso 4.
2. **Geocodificar ubicación:** Nominatim proporciona las coordenadas para la ubicación indicada.
3. **Buscar POI:** La API de Overpass busca lugares de la categoría dentro del radio especificado.
4. **Mostrar resultado:** Lista con nombre, dirección y distancia (m).
5. **Búsqueda por texto libre (alternativa):** La búsqueda directa por texto libre en Nominatim proporciona coincidencias directas.

---

## CLI

```bash
# POI search (category + location) (Español)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py restaurant München

# Geocode location (Español)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py --geocode "Brandenburg Gate Berlin"

# Adjust radius (default: 1000 m) (Español)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py hotel Wien --radius 2000

# Help (Español)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py --help
```

---

## Almacenamiento

Sin almacenamiento persistente. Los resultados solo se muestran, no se guardan.

---

## Categorías compatibles

restaurant, cafe, bar, pub, fast_food, hotel, hostel, guest_house, supermarket,
pharmacy, hospital, bank, atm, fuel, parking, bus_stop, train_station, museum,
cinema, theatre, library, school, university, church

---

## Actitud y comportamiento

- Solicite siempre una ubicación al usuario si no se ha proporcionado ninguna.
- Con más de 10 resultados, muestre únicamente los 5 más cercanos y el resto solo a petición.
- Indique la distancia en metros y, a partir de 1 km, en kilómetros (con 1 decimal).
- Privacidad: no se almacenan ni transmiten datos de ubicación, excepto a las
  API públicas de Nominatim/Overpass (openstreetmap.org).

---

## Privacidad

Las solicitudes de búsqueda se envían a `nominatim.openstreetmap.org` y `overpass-api.de`.
Sin inicio de sesión, sin clave de API, sin almacenamiento persistente de datos.
El User-Agent está configurado según la política de Nominatim.

---

## Recursos relacionados

- `reiseroute` — planificación de rutas de A a B (también utiliza Nominatim para geocodificación)
- `wetter` — tiempo meteorológico en la ubicación actual

---

## Registro de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 2026-06-22 | Creado a partir de BACH location_search.py v1.1.0; almacenamiento eliminado |