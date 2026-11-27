---
name: reiseroute
version: 1.0.1
category: assist
description: "Utiliser pour calculer des itinéraires de déplacement, distances et temps de trajet d'un point A à un point B en voiture, vélo ou à pied (ex. 'calculer l'itinéraire de A à B', 'estimation du temps de trajet', 'planifier trajet à vélo', /reiseroute). Calcule les trajets et profils d'élévation via OSRM sans clé d'API. Ne PAS utiliser pour rechercher des POI à proximité (utiliser assist/location-suche)."
tags: [routing, navigation, osrm, openstreetmap, reise]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['urllib.request', 'urllib.parse', 'urllib.error', 'json']}
runtime: python3
entry_point: reiseroute_core.py
provenance: {'origin': 'BACH hub routing-service', 'origin_path': 'system/hub/_services/routing/routing_service.py', 'origin_version': '1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': 'None', 'local_changes_since_sync': 'urllib.parse-Import an den Kopf verschoben (war im Original nur im else-Zweig). geocode_place (Nominatim) integriert. Keine Origin-DB. Kein Store. Userneutral, headless, nur Stdlib.\\n'}
language: fr
---


<img src="banner.png" width="100%" alt="reiseroute banner">

> **Français** — Version française officielle de la compétence `reiseroute`.

# Itinéraire (`reiseroute`)

**Planification d'itinéraire via OSRM (Open Source Routing Machine)**

---

## Aperçu

Planifie des itinéraires entre deux lieux (noms ou coordonnées) via le service
public OSRM (`router.project-osrm.org`). Affiche la distance, la durée du trajet
et le mode de transport. Aucune clé d'API, aucun compte requis.

---

## Déclencheurs

| Formulation | Action |
|---|---|
| « Planifie l'itinéraire de Berlin à Hambourg » | Itinéraire en voiture, géocoder les noms de lieux |
| « Combien de temps dure le trajet de Munich à Vienne en voiture ? » | Itinéraire en voiture + indication de durée |
| « Itinéraire à vélo de Potsdam à Berlin » | Mode vélo |
| « À pied de Kreuzberg à Mitte, Berlin » | Mode piéton |
| « Trajet de 52.52,13.41 à 53.55,9.99 » | Coordonnées directes |

---

## Flux de travail

1. **Extraire le point de départ et la destination** depuis l'entrée utilisateur.
2. **Détecter le mode :** voiture (par défaut), vélo, à pied.
3. **Géocoder :** noms de lieux → coordonnées via Nominatim.
4. **Interroger OSRM :** renvoie la distance (km) + la durée (formatée).
5. **Afficher le résultat :** résumé textuel clair.

---

## CLI

```bash
# Itinéraire en voiture entre deux lieux
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Berlin" "Hamburg"

# À vélo
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Potsdam" "Berlin" --modus fahrrad

# À pied
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "Kreuzberg, Berlin" "Mitte, Berlin" --modus fuss

# Coordonnées directes (lat,lon)
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "52.5200,13.4050" "53.5500,9.9937"

# Sortie JSON
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py "München" "Wien" --json

# Aide
PYTHONDONTWRITEBYTECODE=1 python reiseroute_core.py --help
```

---

## Modes

| Mode | Alias | Profil OSRM |
|---|---|---|
| auto (par défaut) | car, pkw, fahren | driving |
| fahrrad | bike, rad, radfahren | cycling |
| fuss | foot, laufen, gehen, zu fuss | foot |

---

## Stockage

Aucun stockage persistant. Les itinéraires ne sont pas enregistrés.

---

## Posture

- Toujours nommer le départ et la destination avant le calcul.
- Clarifier si un lieu est ambigu (p. ex. « Vienne » = Autriche ou une autre ville homonyme ?).
- Remarque : OSRM fournit l'itinéraire le plus rapide sans trafic en temps réel.
- Afficher un avertissement pour les très longs trajets à pied (> 20 km).

---

## Confidentialité

Les requêtes sont envoyées à `nominatim.openstreetmap.org` (géocodage) et
`router.project-osrm.org` (calcul d'itinéraire). Aucune inscription, aucune clé d'API,
aucun stockage persistant de données.

---

## Ressources associées

- `location-suche` — recherche de POI (utilise également Nominatim)
- `wetter` — météo à destination

---

## Journal des modifications

| Version | Date | Modification |
|---|---|---|
| 1.0.1 | 2026-11-22 | Avis de langue corrigé |
| 1.0.0 | 2026-06-22 | Créé depuis BACH routing_service.py v1.0 ; géocodage intégré |