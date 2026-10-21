---
name: reiseroute
version: 1.0.0
type: assist
author: ellmos-ai
created: 2026-07-23
updated: 2026-08-23
category: assist
description: "Planejamento de rotas de A até B via OSRM (Open Source Routing Machine). Suporta carro, bicicleta e pedestre. Não é necessária chave de API."
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
language: pt
visibility: public
translated_from_sha256: 598018ba8fdf3068a89280c1782ab9dbccaabc08409765e920015816bda81aef
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="reiseroute banner">

# Rota de Viagem

**Planejamento de rotas via OSRM (Open Source Routing Machine)**

---

## Visão geral

Planeja rotas entre dois locais (nomes ou coordenadas) por meio do serviço público
OSRM (`router.project-osrm.org`). Exibe distância, tempo de viagem e meio de transporte.
Não requer chave de API nem conta.

---

## Gatilhos

| Frase | Ação |
|---|---|
| „Plan die Route von Berlin nach Hamburg" / „Planeje a rota de Berlim para Hamburgo" | Rota de carro, geocodificar nomes de locais |
| „Wie lange dauert die Fahrt von München nach Wien mit dem Auto?" / „Quanto tempo leva a viagem de Munique a Viena de carro?" | Rota de carro + indicação de tempo |
| „Route mit dem Fahrrad von Potsdam nach Berlin" / „Rota de bicicleta de Potsdam a Berlim" | Modo bicicleta |
| „Zu Fuß von Kreuzberg nach Mitte Berlin" / „A pé de Kreuzberg a Mitte, Berlim" | Modo pedestre |
| „Strecke von 52.52,13.41 nach 53.55,9.99" / „Trajeto de 52.52,13.41 a 53.55,9.99" | Coordenadas diretas |

---

## Fluxo de trabalho

1. **Extrair local de partida e de destino** da entrada do usuário.
2. **Identificar o modo:** carro (padrão), bicicleta, a pé.
3. **Geocodificar:** nomes de locais → coordenadas via Nominatim.
4. **Consultar o OSRM:** retorna distância (km) + duração (formatada).
5. **Apresentar o resultado:** resumo textual claro.

---

## CLI

```bash
# Auto-Route zwischen zwei Orten
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Berlin" "Hamburg"

# Fahrrad
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Potsdam" "Berlin" --modus fahrrad

# Zu Fuß
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Kreuzberg, Berlin" "Mitte, Berlin" --modus fuss

# Koordinaten direkt (lat,lon)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "52.5200,13.4050" "53.5500,9.9937"

# JSON-Ausgabe
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "München" "Wien" --json

# Hilfe
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py --help
```

---

## Modos

| Modo | Alias | Perfil OSRM |
|---|---|---|
| auto (padrão) | car, pkw, fahren | driving |
| fahrrad | bike, rad, radfahren | cycling |
| fuss | foot, laufen, gehen, zu fuss | foot |

---

## Store

Sem armazenamento persistente. As rotas não são salvas.

---

## Postura

- Sempre nomear a partida e o destino antes do cálculo.
- Esclarecer quando um local for ambíguo (por exemplo, „Viena" = Áustria ou uma cidade homônima?).
- Aviso: o OSRM fornece a rota mais rápida sem tráfego em tempo real.
- Para rotas pedestres muito longas (> 20 km), exibir um aviso.

---

## Privacidade

As solicitações são enviadas para `nominatim.openstreetmap.org` (geocodificação) e
`router.project-osrm.org` (roteamento). Sem login, sem chave de API,
sem armazenamento persistente de dados.

---

## Recursos relacionados

- `location-suche` — Busca de POIs (também usa Nominatim)
- `wetter` — Clima no destino da viagem

---

## Changelog

| Versão | Data | Alteração |
|---|---|---|
| 1.0.0 | 2026-06-22 | Criado a partir de BACH routing_service.py v1.0; geocodificação integrada |
