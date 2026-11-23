---
name: location-suche
version: 1.0.1
category: assist
description: "Utiliser pour rechercher des lieux, adresses, restaurants ou points d'intérêt (POI) via OpenStreetMap (ex. 'trouver un restaurant à proximité', 'géocoder une adresse', 'chercher des POI en ville', /location-suche). Récupère POI et coordonnées via Nominatim et Overpass API sans clé d'API requise. Ne PAS utiliser pour le calcul d'itinéraires détaillés point à point (utiliser assist/reiseroute)."
tags: [location, openstreetmap, poi, nominatim, overpass, restaurant, hotel]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['urllib.request', 'urllib.parse', 'urllib.error', 'json', 'time']}
runtime: python3
entry_point: location_suche_core.py
provenance: {'origin': 'BACH persoenlicher-assistent', 'origin_path': 'system/agents/persoenlicher-assistent/tools/location_search.py', 'origin_version': '1.1.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': 'None', 'local_changes_since_sync': 'Alle Origin-DB-Abhaengigkeiten entfernt (save_location, list_locations, _ensure_table, _get_db). Kein Store. Userneutral (keine privaten Pfade). Headless, nur Stdlib.\\n'}
language: fr
---


<img src="banner.png" width="100%" alt="location-suche banner">

> **Français** — Version française officielle de la compétence `location-suche`.

# Recherche de lieux (`location-suche`)

**Recherche de lieux, de restaurants et d'hôtels via OpenStreetMap**

---

## Aperçu

Recherche des restaurants, hôtels, cafés et autres lieux à l'aide des services
OpenStreetMap Nominatim (géocodage) et Overpass (recherche de POI).
Aucune clé d'API requise. Aucun stockage persistant.

---

## Déclencheurs

| Formulation | Action |
|---|---|
| « Trouve un restaurant à Munich » | Recherche POI : category=restaurant, near=München |
| « Hôtels près de Vienne » | Recherche POI : category=hotel, near=Wien |
| « Où se trouve la tour Eiffel ? » | Recherche texte libre Nominatim |
| « Trouve des cafés à Berlin » | Recherche POI : category=cafe, near=Berlin |
| « Cherche une pharmacie près de Potsdam » | Recherche POI : category=pharmacy, near=Potsdam |

---

## Flux de travail

1. **Détecter le déclencheur :** la demande contient-elle une catégorie (restaurant, hôtel, etc.)
   et un lieu → étape 2. Sinon texte libre → étape 4.
2. **Géocoder le lieu :** Nominatim fournit les coordonnées pour le lieu indiqué.
3. **Rechercher des POI :** l'API Overpass recherche les établissements de la catégorie dans le rayon.
4. **Afficher le résultat :** présenter la liste avec nom, adresse et distance (m).
5. **Recherche texte libre (repli) :** la recherche texte libre Nominatim fournit des résultats directs.

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

## Stockage

Aucun stockage persistant. Les résultats sont uniquement affichés, pas enregistrés.

---

## Catégories prises en charge

restaurant, cafe, bar, pub, fast_food, hotel, hostel, guest_house, supermarket,
pharmacy, hospital, bank, atm, fuel, parking, bus_stop, train_station, museum,
cinema, theatre, library, school, university, church

---

## Posture

- Toujours demander le lieu à l'utilisateur s'il n'en a pas indiqué.
- S'il y a plus de 10 résultats, n'afficher que les 5 plus proches, le reste sur demande.
- Indiquer la distance en mètres, puis en km à partir de 1 km (1 décimale).
- Confidentialité : aucune donnée de localisation n'est enregistrée ni transmise, excepté vers
  les API publiques Nominatim/Overpass (openstreetmap.org).

---

## Confidentialité

Les requêtes de recherche sont envoyées à `nominatim.openstreetmap.org` et `overpass-api.de`.
Aucune inscription, aucune clé d'API, aucun stockage persistant de données.
Le User-Agent est défini conformément à la politique de Nominatim.

---

## Ressources associées

- `reiseroute` — planification d'itinéraire de A à B (utilise également Nominatim pour le géocodage)
- `wetter` — météo au lieu actuel

---

## Journal des modifications

| Version | Date | Modification |
|---|---|---|
| 1.0.1 | 2026-11-22 | Avis de langue corrigé |
| 1.0.0 | 2026-06-22 | Créé depuis BACH location_search.py v1.1.0 ; stockage supprimé |