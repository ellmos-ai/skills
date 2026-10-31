---
name: location-suche
version: 1.0.0
type: assist
author: ellmos-ai
created: 2026-07-23
updated: 2026-08-23
category: assist
description: "Pesquisa de localização, restaurantes e hotéis via OpenStreetMap (Nominatim + Overpass API). Retorna POIs (Pontos de Interesse) próximos a uma localização ou pesquisa por texto livre."
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
language: pt
visibility: public
translated_from_sha256: 93e16b5f7ddbd85797fd294d2251bb04189db2ac6f5f88f4061cc69b6189e0ba
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.775007+00:00"
---
<img src="banner.png" width="100%" alt="location-suche banner">

# Pesquisa de Localização

**Pesquisa de locais, restaurantes e hotéis via OpenStreetMap**

---

## Visão geral

Pesquisa restaurantes, hotéis, cafés e outros locais com a ajuda dos
serviços OpenStreetMap Nominatim (geocodificação) e Overpass (pesquisa de POIs).
Não é necessária chave de API. Sem armazenamento persistente.

---

## Gatilhos

| Frase | Ação |
|---|---|
| „Procure um restaurante em Munique" | Pesquisa de POIs: category=restaurant, near=München |
| „Hotéis perto de Viena" | Pesquisa de POIs: category=hotel, near=Wien |
| „Onde fica a Torre Eiffel?" | Pesquisa de texto livre no Nominatim |
| „Encontre cafés em Berlim" | Pesquisa de POIs: category=cafe, near=Berlin |
| „Procure farmácia perto de Potsdam" | Pesquisa de POIs: category=pharmacy, near=Potsdam |

---

## Fluxo de trabalho

1. **Identificar o gatilho:** Se a solicitação contiver uma categoria (restaurante, hotel etc.)
   e um local → passo 2. Caso contrário, texto livre → passo 4.
2. **Geocodificar o local:** O Nominatim fornece as coordenadas do local mencionado.
3. **Pesquisar POIs:** A API Overpass busca estabelecimentos da categoria no raio.
4. **Exibir resultado:** Mostrar lista com nome, endereço e distância (m).
5. **Pesquisa de texto livre (alternativa):** O texto livre do Nominatim retorna resultados diretos.

---

## CLI

```bash
# POI-Suche (Kategorie + Ort)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py restaurant München

# Ort geocodieren
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py --geocode "Brandenburger Tor Berlin"

# Radius anpassen (Standard: 1000 m)
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py hotel Wien --radius 2000

# Hilfe
PYTHONDONTWRITEBYTECODE=1 python location_suche_core.py --help
```

---

## Store

Sem armazenamento persistente. Os resultados são apenas exibidos, não salvos.

---

## Categorias suportadas

restaurant, cafe, bar, pub, fast_food, hotel, hostel, guest_house, supermarket,
pharmacy, hospital, bank, atm, fuel, parking, bus_stop, train_station, museum,
cinema, theatre, library, school, university, church

---

## Postura

- Sempre perguntar ao usuário pelo local, caso nenhum tenha sido informado.
- Com mais de 10 resultados, exibir apenas os 5 mais próximos; o restante sob demanda.
- Indicar a distância em metros; a partir de 1 km, em km (1 casa decimal).
- Privacidade: Nenhum dado de localização é armazenado ou transmitido, exceto à
  API pública Nominatim/Overpass (openstreetmap.org).

---

## Privacidade

As consultas de pesquisa são enviadas para `nominatim.openstreetmap.org` e `overpass-api.de`.
Sem login, sem chave de API, sem armazenamento persistente de dados.
O User-Agent é definido de acordo com a política do Nominatim.

---

## Recursos relacionados

- `reiseroute` — Planejamento de rota de A até B (também usa o Nominatim para geocodificação)
- `wetter` — Clima no local atual

---

## Changelog

| Versão | Data | Alteração |
|---|---|---|
| 1.0.0 | 2026-06-22 | Criado a partir de BACH location_search.py v1.1.0; Store removido |
