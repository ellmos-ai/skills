---
name: reiseroute
version: 1.0.0
category: assist
description: Planificación de rutas de A a B a través de OSRM (Open Source Routing Machine). Admite coche, bicicleta y peatón. No requiere clave de API.
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
language: es
---

> **Español** — Versión oficial en español de `reiseroute`.


# Travel Route (Español)

**Planificación de rutas a través de OSRM (Open Source Routing Machine)**

---

## Descripción general y propósito

Planifica rutas entre dos ubicaciones (nombres o coordenadas) a través del servicio
público de OSRM (`router.project-osrm.org`). Devuelve la distancia, el tiempo de viaje y
el modo de transporte. Sin clave de API, sin necesidad de cuenta.

---

## Activadores

| Frase | Acción |
|---|---|
| "Planifica la ruta de Berlín a Hamburgo" | Ruta en coche, geocodificar nombres de lugares |
| "¿Cuánto se tarda en coche de Múnich a Viena?" | Ruta en coche + tiempo |
| "Ruta en bicicleta de Potsdam a Berlín" | Modo bicicleta |
| "Ir a pie de Kreuzberg a Mitte, Berlín" | Modo peatonal |
| "Ruta de 52.52,13.41 a 53.55,9.99" | Coordenadas directas |

---

## Flujo de trabajo y procedimiento

1. **Extraer origen y destino** de la entrada del usuario.
2. **Detectar modo:** coche (predeterminado), bicicleta, a pie.
3. **Geocodificar:** nombres de lugares → coordenadas a través de Nominatim.
4. **Consultar OSRM:** devuelve la distancia (km) + duración (formateada).
5. **Mostrar resultado:** resumen de texto conciso.

---

## CLI

```bash
# Ruta en coche entre dos lugares (Español)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Berlin" "Hamburg"

# Bicicleta (Español)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Potsdam" "Berlin" --modus fahrrad

# A pie (Español)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Kreuzberg, Berlin" "Mitte, Berlin" --modus fuss

# Coordenadas directamente (lat,lon) (Español)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "52.5200,13.4050" "53.5500,9.9937"

# Salida en JSON (Español)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Munich" "Vienna" --json

# Ayuda (Español)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py --help
```

---

## Modos

| Modo | Alias | Perfil OSRM |
|---|---|---|
| auto (predeterminado) | car, pkw, fahren | driving |
| fahrrad | bike, rad, radfahren | cycling |
| fuss | foot, laufen, gehen, zu fuss | foot |

---

## Almacenamiento

Sin almacenamiento permanente. Las rutas no se guardan.

---

## Actitud

- Indicar siempre el origen y el destino antes de realizar el cálculo.
- Aclarar si un lugar es ambiguo (p. ej., "¿Viena?" = ¿Austria o una ciudad del mismo nombre?).
- Nota: OSRM proporciona la ruta más rápida sin datos de tráfico en tiempo real.
- Mostrar una advertencia para rutas peatonales muy largas (> 20 km).

---

## Privacidad

Las solicitudes se envían a `nominatim.openstreetmap.org` (geocodificación) y
`router.project-osrm.org` (enrutamiento). Sin inicio de sesión, sin clave de API,
sin almacenamiento persistente de datos.

---

## Recursos relacionados

- `location-suche` — Búsqueda de POI (también utiliza Nominatim)
- `wetter` — Tiempo atmosférico en el destino

---

## Registro de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 2026-06-22 | Creado a partir de BACH routing_service.py v1.0; geocodificación integrada |