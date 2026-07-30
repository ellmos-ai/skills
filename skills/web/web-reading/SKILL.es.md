---
name: web-reading
version: 1.1.0
type: protocol
author: BACH Team
created: 2026-03-12
updated: 2026-07-05
description: Router y protocolo para leer y extraer contenido web. Decide primero QUÉ se necesita (texto principal vs. estructura vs. captura de pantalla) y luego QUÉ herramienta disponible en el sistema lo ofrece. Si no hay nada adecuado presente, recomienda instalar el módulo web-scraper.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: web
tags: [web-scraping, content-extraction, research, router]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['requests', 'beautifulsoup4']}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/webseiten-lesen.md', 'origin_version': '3.8.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
bach_integration: {'handler': 'web-parse, web-scrape', 'db_tables': [], 'hooks': [], 'bach_origin_path': 'system/skills/workflows/'}
---

> **Español** — Versión oficial en español de `web-reading`.


# Lectura Web (Router)

## Descripción general y propósito

Obtenga y procese contenido web, pero no elija una herramienta a ciegas. Esta habilidad enruta: **primero el propósito, luego la mejor herramienta disponible.** La implementación real reside en el **módulo `web-scraper`**; esta habilidad solo muestra lo que está presente actualmente y cómo usarlo.

## Paso 1 — ¿Qué se necesita?

```
Process a web page?
  |
  +-- Main text (article / prose)   → "Content"     → Step 2A
  +-- Links / forms / headers       → "Structure"   → Step 2B
  +-- Rendered image of the page    → "Screenshot"  → Step 2C
```

## Paso 2 — ¿Qué herramienta? (Router)

Utilice la **primera herramienta disponible** de cada lista. "Disponible" significa que la herramienta/habilidad/módulo está realmente presente en esta sesión.

### 2A — Contenido (texto principal, markdown limpio)

| Prioridad | Herramienta | Disponible cuando… | Uso |
|---|---|---|---|
| 1 | Habilidad **`defuddle`** | la habilidad `defuddle` está en la lista | markdown limpio a partir de páginas web normales |
| 2 | **`WebFetch`** integrado | el agente tiene la herramienta WebFetch | lectura/resumen rápido de una URL |
| 3 | **`fc_web_fetch`** (MCP) | FileCommander MCP cargado | `mode: "extract"` |
| 4 | Módulo **`web-scraper`** | módulo instalado/importable | `web-scraper extract <url>` / `extract(url)` |

> Nota: Las URL de tipo `.md` ya están en markdown → use `WebFetch` directamente, sin extractor.

### 2B — Estructura (enlaces, formularios, encabezados)

`WebFetch`/`defuddle` **no** son adecuados aquí (devuelven texto procesado, no estructura sin procesar). Use en su lugar:

| Prioridad | Herramienta | Disponible cuando… | Uso |
|---|---|---|---|
| 1 | **`fc_web_fetch`** (MCP) | FileCommander MCP cargado | `mode: "links" \| "forms" \| "headers"` |
| 2 | Módulo **`web-scraper`** | módulo instalado/importable | `web-scraper links\|forms\|headers <url>` |

### 2C — Captura de pantalla

| Prioridad | Herramienta | Disponible cuando… | Uso |
|---|---|---|---|
| 1 | Módulo **`web-scraper`** | módulo con el extra `[screenshot]` | `web-scraper screenshot <url> --out img.png` |
| 2 | Herramienta de automatización de navegador | p. ej. Playwright/Computer-Use presente | dependiente de la página |

## Paso 3 — Alternativa: ¿no se encontró nada adecuado?

Si **ninguna** herramienta está disponible para el propósito, recomiende instalar el **módulo `web-scraper`** (completo: get/links/forms/headers/extract/screenshot):

```bash
# desde la carpeta de módulos local (.MODULES/.TOOLS/web-scraper)
pip install ".[http,extract]"          # + [screenshot] para capturas de pantalla

# luego:
web-scraper extract <url>
```

Como biblioteca:

```python
from web_scraper import WebScraper, extract
print(extract("https://example.com")["content"])
```

## Último recurso — fragmento independiente (sin dependencias más allá de requests/bs4)

```python
import requests
from bs4 import BeautifulSoup

def extract_content(url: str) -> str:
    """Simple content extraction."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)
```

## Historial de cambios

### 1.1.0 (2026-07-05)
- Reestructurado de un protocolo simple a un **router**: detecta las capacidades web disponibles (`defuddle`, `WebFetch`, `fc_web_fetch`, módulo `web-scraper`) y enruta según el propósito (contenido/estructura/captura de pantalla); de lo contrario, recomienda el módulo `web-scraper`.
- Nombre unificado a `web-reading` (anteriormente `webseiten-lesen` en la versión DE).
- Se eliminaron los ejemplos de la CLI de BACH del cuerpo (cumple con el funcionamiento independiente; el origen permanece documentado en los metadatos de `bach_integration`).

### 1.0.0 (2026-03-12)
- Exportación del flujo de trabajo de BACH v3.8.0 `webseiten-lesen.md`