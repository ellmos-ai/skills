---
name: tageszeitung
version: 0.2.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-11-27
description: "Utiliser pour assembler un journal quotidien personnalisé ou une revue de presse à partir de flux RSS et de sources web (ex. 'créer le journal du jour', 'synthétiser les actualités du matin', 'exporter la revue de presse en PDF', /tageszeitung). Centralise les flux dans une base SQLite locale et produit des éditions HTML, Markdown et PDF via Edge Headless. Ne PAS utiliser pour les revues de littérature académique (utiliser research/research-agent)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [zeitung, news, rss, feed, pdf, tageszeitung]
language: fr
status: stable
dependencies: {'tools': [{'name': 'msedge.exe', 'optional': True, 'purpose': 'HTML → PDF (Edge Headless); without Edge: HTML output only'}], 'services': [], 'protocols': [], 'python': [{'name': 'feedparser', 'optional': True, 'install': 'pip install feedparser', 'purpose': 'RSS parsing (main backend). Fallback: defusedxml → regex'}, {'name': 'defusedxml', 'optional': True, 'install': 'pip install defusedxml', 'purpose': 'XXE-safe XML parser as fallback when feedparser is missing. Without defusedxml a regex fallback is used (no ET.fromstring on network data).'}]}
provenance: {'origin': 'bach-port', 'origin_path': 'BACH/system/hub/news.py + hub/_services/newspaper/newspaper_generator.py', 'origin_version': 'news.py v1.x, newspaper_generator.py v1.x', 'origin_repo': 'ellmos-ai/bach (privat)', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'notes': 'Schema (news_sources + news_items) 1:1 aus BACH news.py portiert. BaseHandler-Abhängigkeit entfernt. Origin-DB-Pfad entfernt. DB-Pfad konfigurierbar. newspaper_generator.py-Logik (HTML-Render + Edge-PDF) userneutral übernommen.\\n'}
---


<img src="banner.png" width="100%" alt="tageszeitung banner">

> **Français** — Version française officielle de la compétence `tageszeitung`.

# Quotidien (`tageszeitung`)

## Objectif

Récupérer des articles depuis des flux RSS et des sources web configurés, les
trier par catégorie et les générer sous forme de journal quotidien HTML/PDF. Les
articles sont enregistrés localement dans `tageszeitung/store.db` et marqués comme lus.

---

## Déclencheurs

| Formulation | Action |
|---|---|
| « Crée mon journal du jour » | Récupérer les articles + générer le PDF |
| « Journal du jour pour aujourd'hui » | Générer le journal d'aujourd'hui |
| « Ajoute un flux [URL] » | Enregistrer une source RSS |
| « Montre mes sources » | Afficher la liste des sources |
| « Fetch News » | Récupérer toutes les sources (sans rendu) |

---

## Flux de travail

1. **Vérifier les sources** : lire toutes les sources actives depuis `news_sources`.
2. **Récupération** : RSS via feedparser (ou repli xml.etree), web via urllib.
3. **Déduplication** : UNIQUE(source_id, url) empêche les doublons.
4. **Rendu** : regrouper les articles non lus par catégorie → HTML → PDF.
5. **Livraison** : déposer le HTML/PDF dans le dossier de sortie (chemin configurable).

---

## Point d'entrée CLI

```bash
# Ajouter une source
python tageszeitung_core.py add-source "Heise" rss https://www.heise.de/rss/heise-atom.xml --category tech

# Récupérer toutes les sources
python tageszeitung_core.py fetch

# Générer le quotidien (HTML + PDF si Edge est disponible)
python tageszeitung_core.py render [--date 2026-06-22] [--out /chemin/]

# Lister les sources
python tageszeitung_core.py sources

# Articles non lus
python tageszeitung_core.py items [--limit 50] [--category tech]

# Marquer un article comme lu
python tageszeitung_core.py read <item_id>

# Stockage alternatif (p. ex. pour les tests)
python tageszeitung_core.py --store /tmp/t.db sources --dry-run
```

---

## Stockage

| Propriété | Valeur |
|---|---|
| Type | SQLite |
| Chemin (par défaut) | `skills/assist/tageszeitung/store.db` |
| Surcharge | `--store <pfad>` ou variable d'env `TAGESZEITUNG_STORE` |
| Tables | `news_sources`, `news_items` |

### Schéma (porté depuis BACH news.py)

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

## Posture

- `feedparser` est privilégié ; sans `feedparser`, un repli `xml.etree` prend en charge les flux RSS 2.0 simples.
- La génération PDF requiert `msedge.exe` dans le PATH système ou la variable d'environnement `MSEDGE_PATH`. Sans Edge, seul du HTML est généré.
- Nombre maximal d'articles par catégorie : configurable via `assist/prefs.json` (`tageszeitung_max_per_category`, par défaut : 5).

---

## Confidentialité

- Le contenu des articles reste en local dans `store.db`.
- Aucun service d'analyse externe — seules les sources RSS/web configurées sont appelées.

---

## Ressources associées

- BACH `hub/news.py` — origine (lecture seule)
- BACH `hub/_services/newspaper/newspaper_generator.py` — origine (lecture seule)

---

## Configuration et modèles (`zeitung-config.json`, `templates/`)

Les rubriques (`sections`), limites d'articles (`max_per_category`, `summary_max_chars`, `fetch_limit`), délais réseau et options de mise en page résident dans [zeitung-config.json](zeitung-config.json) (auto-réparation vers les valeurs par défaut + `.corrupt.<ts>.bak` avec `--repair` ; les entrées existantes de `assist/prefs.json` restent compatibles). Le rendu utilise des modèles remplaçables sous [templates/ausgabe.template.html](templates/ausgabe.template.html) (`html`/PDF) et [templates/ausgabe.template.md](templates/ausgabe.template.md) (`--format md`).

---

## Journal des modifications

| Version | Date | Modification |
|---|---|---|
| 0.2.0 | 2026-11-27 | Ajout de `zeitung-config.json` (rubriques, limites, mise en page, auto-réparation), des modèles `templates/ausgabe.template.{html,md}` et de `tests/test_tageszeitung.py` |
| 0.1.1 | 2026-11-22 | Avis de langue corrigé |
| 0.1.0 | 2026-06-22 | Création initiale — schéma BACH porté, stockage propre, feedparser optionnel |