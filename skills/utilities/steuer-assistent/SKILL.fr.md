---
name: steuer-assistent
version: 0.1.1
type: skill
author: Lukas Geiger
created: 2026-07-23
updated: 2026-11-22
description: "Utilisez cette compétence lorsque des justificatifs de frais professionnels allemands (Werbungskosten) doivent être préparés de manière structurée via le module autonome steuer-assistent : enregistrement local, somme au centime près, export ZIP privé. Limite stricte : aucun conseil fiscal ni dépôt via ELSTER."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance: {'origin': 'external', 'origin_repo': 'https://github.com/ellmos-ai/steuer-assistent', 'origin_path': 'SKILL.md, steuer_assistent/ (CLI module)', 'origin_version': None, 'last_sync_from_origin': '2026-07-23', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
category: utilities
tags: [tax, germany, receipts, finance, wrapper, pointer-skill]
language: fr
status: active
visibility: public
---

<img src="banner.png" width="100%" alt="steuer-assistent banner">

> **Français** — Version française officielle de la compétence `steuer-assistent`.

# steuer-assistent — Compétence de renvoi

Cette compétence est un **renvoi léger (wrapper)** vers le dépôt de module autonome et public [`ellmos-ai/steuer-assistent`](https://github.com/ellmos-ai/steuer-assistent) (licence MIT, public). La véritable compétence réside là-bas — ce dépôt ne fait que référencer et documenter l'installation.

## Ce que fait le module

`steuer-assistent` est un petit module Python offline-first destiné aux justificatifs de frais professionnels auto-catégorisés (Werbungskosten de salariés allemands) :

- Enregistrer des justificatifs (catégorie, montant, date, note optionnelle).
- Additionner les frais professionnels enregistrés au centime près par année.
- Exporter un document de travail ZIP privé et non officiel (CSV + récapitulatif + mention de caractère non officiel, sans les fichiers de justificatifs).
- Stockage local (par défaut `%USERPROFILE%\.steuer-assistent\steuer.db`), aucun accès réseau, aucun envoi vers le cloud, aucun accès à des bases de données tierces.

## Limites (important)

- **Aucun conseil fiscal.** Le module ne vérifie pas la déductibilité fiscale des différents postes et n'établit ni ne transmet de déclaration fiscale.
- La transmission électronique officielle s'effectue exclusivement via ELSTER ou un logiciel agréé — jamais via ce module.
- Périmètre : document de travail privé pour les frais professionnels de salariés (`Werbungskosten`) ; aucune saisie de dépenses commerciales ou d'exploitation.

## Installation (générique, sans chemins locaux concrets)

1. Cloner le module :
   ```bash
   git clone https://github.com/ellmos-ai/steuer-assistent.git <chemin-clone>
   ```
2. Installer et vérifier le module :
   ```bash
   cd <chemin-clone>
   python -m pip install -e .
   python -B -m pytest tests -q -p no:cacheprovider
   ```
3. Reprendre `<chemin-clone>/SKILL.md` dans votre propre environnement de compétences (par ex. `~/.claude/skills/steuer-assistent/`). Ne committez JAMAIS de chemins locaux réels ou de noms d'hôtes dans un environnement de compétences versionné.
4. Adapter le chemin de stockage au besoin via `STEUER_ASSISTENT_DB=<chemin>` ou `--store <chemin>` ; la valeur par défaut est le répertoire utilisateur.
5. Détails sur les commandes CLI, la confidentialité et les limites : voir le README du dépôt du module.

## Origine de cette compétence de renvoi

Ce wrapper a été préparé le 2026-07-23 comme entrée vitrine pour le dépôt `ellmos-ai/skills`. Il n'y a **aucune duplication de code** — la maintenance et le versionnement restent exclusivement dans le dépôt du module `ellmos-ai/steuer-assistent`.

## Journal des modifications

### 0.1.1 (2026-11-22)
- Indication de langue corrigée

### 0.1.0 (2026-07-23)
- Compétence de renvoi initiale vers `ellmos-ai/steuer-assistent`.
