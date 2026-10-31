---
name: wetter
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: "Responde perguntas sobre o tempo para um local ou coordenadas via wttr.in (gratuito, sem chave de API). Tempo atual + previsão de 3 dias. O local vem da solicitação do usuário ou das preferências; cache curto opcional."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [wetter, wttr, vorschau, assist]
language: pt
status: active
visibility: public
dependencies: {'tools': ['wetter_core.py'], 'services': [], 'protocols': [], 'python': ['urllib', 'json']}
provenance: {'origin': 'bach', 'origin_path': 'system/hub/_services/weather/weather_service.py', 'origin_version': '1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 77159e7ab4dc0541cb58d038cfb353076dc2d32699dba8cd2e69761042b86b8c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="wetter banner">

# Wetter

Consulta rápida e sem chave sobre o tempo para o dia a dia.

## Finalidade

Responde perguntas do tipo „Como vai estar o tempo?" sem chave de API (fonte de dados: wttr.in).
Fornece o tempo atual (temperatura, sensação térmica, vento, umidade do ar, UV) mais uma
previsão compacta de 3 dias. **Neutro quanto ao usuário:** não há local fixo no código — o local
vem da solicitação ou de `assist/prefs.json` (`wetter_default_location`),
que o LLM preenche interativamente com o usuário.

## Gatilhos

| Entrada do usuário | Ação |
|---|---|
| „Tempo para Potsdam?" / „Como vai estar o tempo em Hamburgo?" | `wetter_core.py "<Ort>"` |
| „Tempo amanhã?" (sem local) | `wetter_core.py --default` (local vindo das preferências) |
| „Meu local padrão de tempo é Potsdam" | `wetter_core.py --set-default "Potsdam"` |
| Coordenadas conhecidas | `wetter_core.py <lat> <lon>` |

## Fluxo de trabalho

```
1. Ort bestimmen: aus Anfrage; sonst prefs.json (wetter_default_location);
   sonst Nutzer interaktiv fragen + optional als Default speichern.
2. wetter_core.py abfragen (wttr.in, 2 Versuche, 30-min-Cache).
3. Lesbaren Wetter-Text + 3-Tage-Vorschau praesentieren.
```

## Ponto de entrada CLI (wetter_core.py)

```bash
python wetter_core.py "Potsdam"          # Ort
python wetter_core.py 52.6789 13.5878   # Koordinaten
python wetter_core.py --default         # Ort aus prefs.json
python wetter_core.py --set-default "Potsdam"
```

## Armazenamento (opcional)

- **Nenhum armazenamento obrigatório.** Cache curto opcional `assist/wetter/.cache.json`
  (TTL de 30 min, em regime de melhor esforço) — evita consultas de rede repetidas.
- Preferência de local em `assist/prefs.json` (`wetter_default_location`).

## Postura

Usamos o wttr.in como fonte padrão sem chave, mas estamos abertos a
outros backends meteorológicos (por exemplo, DWD/OpenWeather), caso o usuário assim o deseje.

## Privacidade

- Apenas o nome do local/as coordenadas são enviados ao wttr.in (necessário para a consulta).
- Sem telemetria, sem conta. Cache e preferências permanecem locais.

## Recursos relacionados

- `assist/AGENTS.md` — roteador guarda-chuva
- `assist/reiseroute/` — pode usar o tempo para planejamento de viagens (planejado)

## Changelog

### 0.1.0 (2026-06-22)
- Versão inicial. Portada de BACH `hub/_services/weather/weather_service.py` (MIT).
- Ampliada: suporte a nome de local (não apenas coordenadas), previsão de 3 dias,
  cache opcional, local padrão baseado em preferências. Neutra quanto ao usuário.
