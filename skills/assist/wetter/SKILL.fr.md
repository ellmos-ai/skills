---
name: wetter
version: 0.1.1
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-11-22
description: "Utiliser pour consulter la météo actuelle ou les prévisions à 3 jours pour une ville ou des coordonnées (ex. 'quel temps fait-il à...', 'prévisions météo pour demain', 'risque de pluie aujourd'hui', /wetter). Récupère la météo en direct et les prévisions via wttr.in sans clé d'API. Ne PAS utiliser pour des données climatiques historiques ou des calculs astronomiques."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [wetter, wttr, vorschau, assist]
language: fr
status: active
dependencies: {'tools': ['wetter_core.py'], 'services': [], 'protocols': [], 'python': ['urllib', 'json']}
provenance: {'origin': 'bach', 'origin_path': 'system/hub/_services/weather/weather_service.py', 'origin_version': '1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
---


<img src="banner.png" width="100%" alt="wetter banner">

> **Français** — Version française officielle de la compétence `wetter`.

# Météo (`wetter`)

Renseignements météo rapides et sans clé d'API pour le quotidien.

## Objectif

Répond aux questions « Quel temps fera-t-il ? » sans clé d'API (source de données : wttr.in).
Fournit la météo actuelle (température, ressenti, vent, humidité de l'air, UV) ainsi
qu'une prévision compacte sur 3 jours. **Neutre envers l'utilisateur :** aucun lieu fixe
dans le code — le lieu provient de la requête ou de `assist/prefs.json`
(`wetter_default_location`), que le LLM renseigne interactivement avec l'utilisateur.

## Déclencheurs

| Entrée utilisateur | Action |
|---|---|
| « Météo pour Potsdam ? » / « Quel temps fera-t-il à Hambourg ? » | `wetter_core.py "<Ort>"` |
| « Météo demain ? » (sans lieu) | `wetter_core.py --default` (lieu depuis prefs) |
| « Mon lieu météo par défaut est Potsdam » | `wetter_core.py --set-default "Potsdam"` |
| Coordonnées connues | `wetter_core.py <lat> <lon>` |

## Flux de travail

```
1. Ort bestimmen: aus Anfrage; sonst prefs.json (wetter_default_location);
   sonst Nutzer interaktiv fragen + optional als Default speichern.
2. wetter_core.py abfragen (wttr.in, 2 Versuche, 30-min-Cache).
3. Lesbaren Wetter-Text + 3-Tage-Vorschau praesentieren.
```

## Point d'entrée CLI (`wetter_core.py`)

```bash
python wetter_core.py "Potsdam"          # Ort
python wetter_core.py 52.6789 13.5878   # Koordinaten
python wetter_core.py --default         # Ort aus prefs.json
python wetter_core.py --set-default "Potsdam"
```

## Stockage (optionnel)

- **Aucun stockage obligatoire.** Cache court optionnel `assist/wetter/.cache.json`
  (TTL 30 min, best-effort) — évite les appels réseau répétés.
- Préférence de lieu dans `assist/prefs.json` (`wetter_default_location`).

## Posture

Nous utilisons wttr.in comme source par défaut sans clé d'API, mais restons ouverts à
d'autres backends météo (p. ex. DWD/OpenWeather) si l'utilisateur le souhaite.

## Confidentialité

- Seuls le nom du lieu ou les coordonnées sont transmis à wttr.in (nécessaires pour la requête).
- Aucune télémétrie, aucun compte. Le cache et la préférence restent locaux.

## Ressources associées

- `assist/AGENTS.md` — Routeur principal
- `assist/reiseroute/` — utilise éventuellement la météo pour la planification de trajets (prévu)

## Journal des modifications

### 0.1.1 (2026-11-22)
- Avis de langue corrigé

### 0.1.0 (2026-06-22)
- Version initiale. Portée depuis BACH `hub/_services/weather/weather_service.py` (MIT).
- Étendue : prise en charge des noms de lieux (pas seulement des coordonnées), prévision à 3 jours,
  cache optionnel, lieu par défaut basé sur prefs. Neutre envers l'utilisateur.