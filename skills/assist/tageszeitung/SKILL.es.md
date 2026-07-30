---
name: tageszeitung
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: Crea un periódico diario personalizado a partir de fuentes RSS y fuentes web. Portado del sistema de noticias BACH (news.py + newspaper_generator.py). Almacenamiento SQLite propio (sin Origin-DB). feedparser opcional: fallback XML a través de stdlib. Exportación a PDF mediante Edge Headless (msedge.exe).

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [zeitung, news, rss, feed, pdf, tageszeitung]
language: es
status: stable
dependencies: {'tools': [{'name': 'msedge.exe', 'optional': True, 'purpose': 'HTML → PDF (Edge Headless); without Edge: HTML output only'}], 'services': [], 'protocols': [], 'python': [{'name': 'feedparser', 'optional': True, 'install': 'pip install feedparser', 'purpose': 'RSS parsing (main backend). Fallback: defusedxml → regex'}, {'name': 'defusedxml', 'optional': True, 'install': 'pip install defusedxml', 'purpose': 'XXE-safe XML parser as fallback when feedparser is missing. Without defusedxml a regex fallback is used (no ET.fromstring on network data).'}]}
provenance: {'origin': 'bach-port', 'origin_path': 'BACH/system/hub/news.py + hub/_services/newspaper/newspaper_generator.py', 'origin_version': 'news.py v1.x, newspaper_generator.py v1.x', 'origin_repo': 'ellmos-ai/bach (privat)', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'notes': 'Schema (news_sources + news_items) 1:1 aus BACH news.py portiert. BaseHandler-Abhängigkeit entfernt. Origin-DB-Pfad entfernt. DB-Pfad konfigurierbar. newspaper_generator.py-Logik (HTML-Render + Edge-PDF) userneutral übernommen.\n'}
---

> **Español** — Versión oficial en español de `tageszeitung`.


## Visión general y propósito

Obtiene artículos de fuentes RSS y fuentes web configuradas, los clasifica por categoría
y los renderiza como un periódico diario en HTML/PDF. Los artículos se almacenan localmente en
`tageszeitung/store.db` y se marcan como leídos.

---

## Disparadores

| Frase | Acción |
|---|---|
| "Crear mi periódico diario" | Obtener artículos + renderizar PDF |
| "Periódico diario de hoy" | Renderizar el periódico de hoy |
| "Añadir feed [URL]" | Registrar fuente RSS |
| "Mostrar mis fuentes" | Mostrar lista de fuentes |
| "Obtener noticias" | Obtener todas las fuentes (sin renderizar) |

---

## Flujo de trabajo y procedimiento

1. **Comprobar fuentes**: Leer todas las fuentes activas de `news_sources`.
2. **Obtener**: RSS a través de feedparser (o fallback de xml.etree), web a través de urllib.
3. **Deduplicación**: UNIQUE(source_id, url) previene duplicados.
4. **Renderizar**: Agrupar artículos no leídos por categoría → HTML → PDF.
5. **Entregar**: Colocar HTML/PDF en la carpeta de salida (ruta configurable).

---

## Punto de entrada CLI

```bash
# Add source (Deutsch)
python tageszeitung_core.py add-source "Heise" rss https://www.heise.de/rss/heise-atom.xml --category tech

# Fetch all sources (Deutsch)
python tageszeitung_core.py fetch

# Render daily newspaper (HTML + PDF if Edge available) (Deutsch)
python tageszeitung_core.py render [--date 2026-06-22] [--out /path/]

# List sources (Deutsch)
python tageszeitung_core.py sources

# Unread articles (Deutsch)
python tageszeitung_core.py items [--limit 50] [--category tech]

# Mark article as read (Deutsch)
python tageszeitung_core.py read <item_id>

# Alternative store (e.g. for tests) (Deutsch)
python tageszeitung_core.py --store /tmp/t.db sources --dry-run
```

---

## Almacenamiento

| Propiedad | Valor |
|---|---|
| Tipo | SQLite |
| Ruta (predeterminada) | `skills/assist/tageszeitung/store.db` |
| Sobrescribir | `--store <path>` o variable de entorno `TAGESZEITUNG_STORE` |
| Tablas | `news_sources`, `news_items` |

### Esquema (portado de BACH news.py)

```sql
CREATE TABLE IF NOT EXISTS news_sources (
    id           TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    type         TEXT NOT NULL DEFAULT 'rss',  -- rss | web
    url          TEXT NOT NULL UNIQUE,
    category     TEXT DEFAULT 'Allgemein',
    schedule     TEXT DEFAULT 'daily',
    is_active    INTEGER DEFAULT 1,
    last_fetched TEXT,
    fetch_count  INTEGER DEFAULT 0,
    error_count  INTEGER DEFAULT 0,
    last_error   TEXT,
    created_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS news_items (
    id           TEXT PRIMARY KEY,
    source_id    TEXT NOT NULL REFERENCES news_sources(id),
    title        TEXT NOT NULL,
    content      TEXT,
    summary      TEXT,
    url          TEXT,
    author       TEXT,
    published_at TEXT,
    fetched_at   TEXT NOT NULL,
    is_read      INTEGER DEFAULT 0,
    category     TEXT,
    UNIQUE(source_id, url)
);
```

---

## Actitud

- Se prefiere feedparser; sin feedparser, un fallback de xml.etree gestiona feeds RSS 2.0 simples.
- La generación de PDF requiere `msedge.exe` en el PATH del sistema o en la variable de entorno `MSEDGE_PATH`. Sin Edge, solo se renderiza HTML.
- Artículos máximos por categoría: configurable mediante `assist/prefs.json` (`tageszeitung_max_per_category`, predeterminado: 5).

---

## Privacidad

- El contenido de los artículos permanece local en `store.db`.
- Sin servicios de análisis externos: solo se llama a las fuentes RSS/web configuradas.

---

## Recursos relacionados

- BACH `hub/news.py` — origen (solo lectura)
- BACH `hub/_services/newspaper/newspaper_generator.py` — origen (solo lectura)

---

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-06-22 | Creación inicial: esquema BACH portado, almacenamiento propio, feedparser opcional |