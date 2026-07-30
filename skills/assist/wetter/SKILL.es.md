---
name: wetter
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: Responde a preguntas sobre el tiempo para una ubicación o coordenadas a través de wttr.in (gratuito, sin clave API). Tiempo actual + pronóstico de 3 días. La ubicación proviene de la solicitud del usuario o preferencias; caché corto opcional.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [wetter, wttr, vorschau, assist]
language: es
status: active
dependencies: {'tools': ['wetter_core.py'], 'services': [], 'protocols': [], 'python': ['urllib', 'json']}
provenance: {'origin': 'bach', 'origin_path': 'system/hub/_services/weather/weather_service.py', 'origin_version': '1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="wetter banner">

> **Español** — Versión oficial en español de `wetter`.


# Tiempo (Español)

Información meteorológica rápida y sin necesidad de clave API para el uso diario.

## Descripción general y propósito

Responde a preguntas como "¿Qué tiempo hará?" sin necesidad de una clave API (fuente de datos: wttr.in).
Proporciona el tiempo actual (temperatura, sensación térmica, viento, humedad, UV) más un
pronóstico compacto de 3 días. **Neutro respecto al usuario:** sin ubicación fija en el código; la ubicación
proviene de la solicitud o de `assist/prefs.json` (`wetter_default_location`),
que el LLM completa de forma interactiva con el usuario.

## Activadores

| Entrada del usuario | Acción |
|---|---|
| "¿Tiempo en Potsdam?" / "¿Qué tiempo hará en Hamburgo?" | `wetter_core.py "<location>"` |
| "¿Tiempo mañana?" (sin ubicación) | `wetter_core.py --default` (ubicación desde prefs) |
| "Mi ubicación predeterminada para el tiempo es Potsdam" | `wetter_core.py --set-default "Potsdam"` |
| Coordenadas conocidas | `wetter_core.py <lat> <lon>` |

## Flujo de trabajo y procedimiento

```
1. Determinar ubicación: a partir de la solicitud; si no, prefs.json (wetter_default_location);
   si no, preguntar al usuario de forma interactiva + opcionalmente guardar como predeterminada.
2. Consultar wetter_core.py (wttr.in, 2 intentos, caché de 30 min).
3. Presentar texto de tiempo legible + pronóstico de 3 días.
```

## Punto de entrada CLI (wetter_core.py)

```bash
python wetter_core.py "Potsdam"          # ubicación
python wetter_core.py 52.6789 13.5878   # coordenadas
python wetter_core.py --default         # ubicación desde prefs.json
python wetter_core.py --set-default "Potsdam"
```

## Almacenamiento (opcional)

- **Sin almacenamiento obligatorio.** Caché corto opcional `assist/wetter/.cache.json`
  (TTL 30 min, best-effort) — evita llamadas repetidas a la red.
- Preferencia de ubicación en `assist/prefs.json` (`wetter_default_location`).

## Actitud

Usamos wttr.in como fuente predeterminada sin clave API, pero estamos abiertos a otros backends
de tiempo (p. ej., DWD/OpenWeather) si el usuario los prefiere.

## Privacidad

- Solo el nombre/coordenadas de la ubicación se envían a wttr.in (necesario para la consulta).
- Sin telemetría, sin cuenta. El caché y las preferencias permanecen locales.

## Recursos relacionados

- `assist/AGENTS.md` — Enrutador principal
- `assist/reiseroute/` — utiliza el tiempo para la planificación de viajes (planificado)

## Historial de cambios

### 0.1.0 (2026-06-22)
- Versión inicial. Portada desde BACH `hub/_services/weather/weather_service.py` (MIT).
- Ampliado: soporte para nombres de ubicación (no solo coordenadas), pronóstico de 3 días,
  caché opcional, ubicación predeterminada basada en preferencias. Neutro respecto al usuario.