---
name: web-reading
version: 1.1.0
type: protocol
author: BACH Team
created: 2026-03-12
updated: 2026-07-05
description: "Roteador e protocolo para leitura e extração de conteúdo da web. Decide primeiro O QUE é necessário (texto principal vs. estrutura vs. captura de tela) e depois QUAL ferramenta disponível no sistema entrega isso. Se nada adequado estiver presente, recomenda a instalação do módulo web-scraper."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: web
tags: [web-scraping, content-extraction, research, router]
language: pt
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['requests', 'beautifulsoup4']}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/webseiten-lesen.md', 'origin_version': '3.8.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
bach_integration: {'handler': 'web-parse, web-scrape', 'db_tables': [], 'hooks': [], 'bach_origin_path': 'system/skills/workflows/'}
translated_from_sha256: 13dd3196759f5a7bb4beca61b933139ae31924c478b553bcd9d91e2c2d6049bf
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="web-reading banner">

# Ler páginas da web (Roteador)

## Finalidade

Obter e processar conteúdo da web — mas sem escolher uma ferramenta às cegas.
Esta skill faz o roteamento: **primeiro a finalidade, depois a melhor ferramenta disponível.**
A implementação em si vive no **módulo `web-scraper`**; esta skill
apenas mostra o que está disponível no momento e como usá-lo.

## Passo 1 — O que é necessário?

```
Webseite verarbeiten?
  |
  +-- Haupttext (Artikel/Fließtext) → "Content"      → Schritt 2A
  +-- Links / Formulare / Headers   → "Struktur"     → Schritt 2B
  +-- Gerendertes Bild der Seite    → "Screenshot"   → Schritt 2C
```

## Passo 2 — Qual ferramenta? (Roteador)

Use a **primeira ferramenta disponível** na lista correspondente. "Disponível"
significa: a ferramenta/skill/módulo realmente existe nesta sessão.

### 2A — Conteúdo (texto principal, Markdown limpo)

| Prioridade | Ferramenta | Disponível quando … | Uso |
|---|---|---|---|
| 1 | Skill **`defuddle`** | Skill `defuddle` listada | Markdown limpo de páginas web comuns |
| 2 | **`WebFetch`** integrada | Agente possui a ferramenta WebFetch | leitura/resumo rápido de uma URL |
| 3 | **`fc_web_fetch`** (MCP) | MCP FileCommander carregado | `mode: "extract"` |
| 4 | Módulo **`web-scraper`** | Módulo instalado/importável | `web-scraper extract <url>` ou `extract(url)` |

> Observação: URLs `.md` já são Markdown → diretamente `WebFetch`, sem extrator.

### 2B — Estrutura (links, formulários, cabeçalhos)

Aqui `WebFetch`/`defuddle` **não** servem (entregam texto processado,
não estrutura bruta). Use, portanto:

| Prioridade | Ferramenta | Disponível quando … | Uso |
|---|---|---|---|
| 1 | **`fc_web_fetch`** (MCP) | MCP FileCommander carregado | `mode: "links" \| "forms" \| "headers"` |
| 2 | Módulo **`web-scraper`** | Módulo instalado/importável | `web-scraper links\|forms\|headers <url>` |

### 2C — Captura de tela

| Prioridade | Ferramenta | Disponível quando … | Uso |
|---|---|---|---|
| 1 | Módulo **`web-scraper`** | Módulo com extra `[screenshot]` | `web-scraper screenshot <url> --out bild.png` |
| 2 | Ferramenta de automação de navegador | p. ex. Playwright/Computer-Use presente | depende da página |

## Passo 3 — Alternativa: nada adequado encontrado?

Se **nenhuma** ferramenta estiver disponível para a finalidade, recomende a instalação do
**módulo `web-scraper`** (completo: get/links/forms/headers/extract/screenshot):

```bash
# aus dem lokalen Modulordner (.MODULES/.TOOLS/web-scraper)
pip install ".[http,extract]"          # + [screenshot] für Screenshots

# danach:
web-scraper extract <url>
```

Como biblioteca:

```python
from web_scraper import WebScraper, extract
print(extract("https://example.com")["content"])
```

## Solução de emergência — snippet autônomo (sem nada)

Se realmente só a biblioteca padrão + `requests`/`bs4` estiverem disponíveis:

```python
import requests
from bs4 import BeautifulSoup

def extract_content(url: str) -> str:
    """Einfache Content-Extraktion."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)
```

## Registro de alterações

### 1.1.0 (2026-07-05)
- Reestruturação de protocolo puro para **Roteador**: detecta capacidades web
  existentes (`defuddle`, `WebFetch`, `fc_web_fetch`, módulo `web-scraper`) e roteia
  conforme a finalidade (conteúdo/estrutura/captura de tela); caso contrário, recomenda o
  módulo `web-scraper`.
- Nome unificado como `web-reading` (antes DE `webseiten-lesen`).
- Exemplos de CLI BACH removidos do corpo (conforme o padrão autônomo; a origem permanece
  documentada no frontmatter `bach_integration`).

### 1.0.0 (2026-03-12)
- Exportado do workflow `webseiten-lesen.md` do BACH v3.8.0
