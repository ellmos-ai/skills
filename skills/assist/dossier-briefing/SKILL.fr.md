---
name: dossier-briefing
version: 1.0.1
category: assist
description: "Utiliser pour générer un dossier de recherche structuré ou une note de synthèse sur un sujet ou une personne en Markdown (ex. 'créer un dossier de recherche', 'note de cadrage sur un sujet', 'dossier de synthèse', /dossier-briefing). Produit un modèle clair avec faits essentiels, sources et questions en suspens sans stockage permanent. Ne PAS utiliser pour condenser une décision immédiate (utiliser decision-shot) ou pour la recherche scientifique (utiliser research/research-agent)."
tags: [briefing, dossier, recherche, markdown, research]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['datetime', 'pathlib', 'textwrap']}
runtime: python3
entry_point: dossier_briefing_core.py
provenance: {'origin': 'BACH persoenlicher-assistent', 'origin_path': 'system/agents/persoenlicher-assistent/tools/dossier_generator.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': 'None', 'local_changes_since_sync': 'Alle Origin-DB-Abhaengigkeiten entfernt (create_dossier, update_dossier, DOSSIERS_DIR, DossierGenerator-Klasse mit DB-Methoden). Nur _create_markdown-Logik portiert und verallgemeinert (Person→Subjekt). Kein Store. One-Shot-Scaffold-Generator. Headless, nur Stdlib.\\n'}
language: fr
---


<img src="banner.png" width="100%" alt="dossier-briefing banner">

> **Français** — Version française officielle de la compétence `dossier-briefing`.

# Dossier-Briefing

**Note de recherche structurée sur un sujet ou une personne**

---

## Aperçu

Génère un dossier de recherche Markdown vide et structuré sur un sujet quelconque
(personne, entreprise, événement, concept). Cette trame sert de point de départ à
une recherche ultérieure avec `research-agent` ou `web-reading`.

---

## Déclencheurs

| Formulation | Action |
|---|---|
| « Crée un dossier sur Marie Curie » | Trame : personne, typ=person |
| « Dossier sur OpenAI » | Trame : entreprise, typ=organization |
| « Note de synthèse sur l'informatique quantique » | Trame : sujet, typ=topic |
| « Prépare un dossier de recherche sur la COP30 » | Trame : événement, typ=event |

---

## Flux de travail

1. **Nommer le sujet :** extraire le nom/titre du dossier depuis l'entrée utilisateur.
2. **Détecter le type :** person, organization, topic, event (ou unspecified).
3. **Générer la trame :** produire le Markdown avec toutes les sections pertinentes.
4. **Sortie :** stdout ou écriture optionnelle dans un fichier (`-o datei.md`).
5. **Lancer la recherche :** transmettre la trame à `research-agent` ou `web-reading`
   pour compléter les sections manquantes.

---

## CLI

```bash
# Briefing zu stdout
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Marie Curie" --typ person

# In Datei schreiben
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "OpenAI" --typ organization -o briefing_openai.md

# Themen-Briefing
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Quantencomputing" --typ topic

# Ereignis
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "COP30" --typ event

# Ohne Typ-Angabe (generisch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Mein Thema"

# Hilfe
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py --help
```

---

## Types de dossier et sections

| Type | Sections |
|---|---|
| `person` | Données de base, biographie/parcours, œuvre & contributions, sources, notes |
| `organization` | Profil, histoire, produits/services, personnes clés, sources, notes |
| `topic` | Aperçu, contexte/historique, évolution actuelle, sources clés, questions ouvertes, notes |
| `event` | Données clés, participants, déroulement/contexte, portée, sources, notes |
| `unspecified` | Aperçu, contexte, détails, sources, notes |

---

## Stockage

Aucun stockage persistant. La trame est uniquement affichée (stdout ou fichier),
et n'est pas enregistrée dans une base de données.

---

## Posture

- Toujours souligner que la trame est vide et doit être complétée par la recherche.
- Ne jamais inventer ou halluciner de contenu — fournir uniquement la structure.
- En cas de doute sur le type, demander ou utiliser `unspecified`.

---

## Confidentialité

Aucun accès réseau. Aucun stockage. Traitement purement local.

---

## Ressources associées

- `research-agent` — complète la trame du dossier avec les résultats de recherche
- `web-reading` — lit les pages web et en extrait le contenu pour le dossier

---

## Journal des modifications

| Version | Date | Modification |
|---|---|---|
| 1.0.1 | 2026-11-22 | Avis de langue corrigé |
| 1.0.0 | 2026-06-22 | Créé depuis BACH dossier_generator.py v1.0.0 ; stockage supprimé, généralisé |