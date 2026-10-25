---
name: tageszeitung
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: "Cria um jornal diário personalizado a partir de feeds RSS e fontes da web. Portado do sistema de notícias BACH (news.py + newspaper_generator.py). Armazenamento próprio em SQLite (sem Origin-DB). feedparser opcional — fallback XML via stdlib. Exportação para PDF via Edge Headless (msedge.exe)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [zeitung, news, rss, feed, pdf, tageszeitung]
language: pt
status: stable
visibility: public
dependencies: {'tools': [{'name': 'msedge.exe', 'optional': True, 'purpose': 'HTML → PDF (Edge Headless); without Edge: HTML output only'}], 'services': [], 'protocols': [], 'python': [{'name': 'feedparser', 'optional': True, 'install': 'pip install feedparser', 'purpose': 'RSS parsing (main backend). Fallback: defusedxml → regex'}, {'name': 'defusedxml', 'optional': True, 'install': 'pip install defusedxml', 'purpose': 'XXE-safe XML parser as fallback when feedparser is missing. Without defusedxml a regex fallback is used (no ET.fromstring on network data).'}]}
provenance: {'origin': 'bach-port', 'origin_path': 'BACH/system/hub/news.py + hub/_services/newspaper/newspaper_generator.py', 'origin_version': 'news.py v1.x, newspaper_generator.py v1.x', 'origin_repo': 'ellmos-ai/bach (privat)', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'notes': 'Schema (news_sources + news_items) 1:1 aus BACH news.py portiert. BaseHandler-Abhängigkeit entfernt. Origin-DB-Pfad entfernt. DB-Pfad konfigurierbar. newspaper_generator.py-Logik (HTML-Render + Edge-PDF) userneutral übernommen.\n'}
translated_from_sha256: e42d847ea203fa764315a96678ddf6b5814633dd363b9ee8f9fbf87a4af5cce8
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:49.872870+00:00"
---
<img src="banner.png" width="100%" alt="tageszeitung banner">

## Finalidade

Obter artigos de feeds RSS e fontes da web configurados, ordená-los por categorias
e renderizá-los como jornal diário em HTML/PDF. Os artigos são armazenados localmente em
`tageszeitung/store.db` e marcados como lidos.

---

## Gatilhos

| Frase | Ação |
|---|---|
| „Erstell meine Tageszeitung" / „Crie meu jornal diário" | Obter artigos + renderizar PDF |
| „Tageszeitung für heute" / „Jornal diário de hoje" | Renderizar o jornal de hoje |
| „Füge Feed hinzu [URL]" / „Adicione o feed [URL]" | Registrar fonte RSS |
| „Zeig meine Quellen" / „Mostre minhas fontes" | Exibir lista de fontes |
| „Fetch News" / „Buscar notícias" | Obter todas as fontes (sem renderização) |

---

## Fluxo de trabalho

1. **Verificar fontes**: Ler todas as fontes ativas de `news_sources`.
2. **Obter**: RSS via feedparser (ou fallback xml.etree), web via urllib.
3. **Deduplicação**: UNIQUE(source_id, url) impede duplicatas.
4. **Renderizar**: Agrupar artigos não lidos por categoria → HTML → PDF.
5. **Entregar**: Salvar HTML/PDF na pasta de saída (caminho configurável).

---

## Entrada via CLI

```bash
# Quelle hinzufügen
python tageszeitung_core.py add-source "Heise" rss https://www.heise.de/rss/heise-atom.xml --category tech

# Alle Quellen abrufen
python tageszeitung_core.py fetch

# Tageszeitung rendern (HTML + PDF wenn Edge verfügbar)
python tageszeitung_core.py render [--date 2026-06-22] [--out /pfad/]

# Quellen auflisten
python tageszeitung_core.py sources

# Ungelesene Artikel
python tageszeitung_core.py items [--limit 50] [--category tech]

# Artikel als gelesen markieren
python tageszeitung_core.py read <item_id>

# Alternativer Store (z.B. für Tests)
python tageszeitung_core.py --store /tmp/t.db sources --dry-run
```

---

## Armazenamento

| Propriedade | Valor |
|---|---|
| Tipo | SQLite |
| Caminho (padrão) | `skills/assist/tageszeitung/store.db` |
| Substituição | `--store <pfad>` ou variável de ambiente `TAGESZEITUNG_STORE` |
| Tabelas | `news_sources`, `news_items` |

### Esquema (portado de news.py do BACH)

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

## Diretrizes

- feedparser é preferido; sem feedparser, aplica-se um fallback xml.etree para feeds RSS 2.0 simples.
- A geração de PDF requer `msedge.exe` no PATH do sistema ou a variável de ambiente `MSEDGE_PATH`. Sem o Edge, apenas HTML é renderizado.
- Máximo de artigos por categoria: configurável via `assist/prefs.json` (`tageszeitung_max_per_category`, padrão: 5).

---

## Privacidade

- O conteúdo dos artigos permanece local em `store.db`.
- Nenhum serviço externo de análise — apenas as fontes RSS/web configuradas são acessadas.

---

## Recursos relacionados

- BACH `hub/news.py` — Origin (somente leitura)
- BACH `hub/_services/newspaper/newspaper_generator.py` — Origin (somente leitura)

---

## Registro de alterações

| Versão | Data | Alteração |
|---|---|---|
| 0.1.0 | 2026-06-22 | Criação inicial — esquema BACH portado, armazenamento próprio, feedparser opcional |
