---
name: wayfinding-routing
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: Compétence universelle de navigation, d'orientation et de résilience d'urgence pour les agents LLM. Fournit des heuristiques actives de repérage, d'auto-orientation et de récupération lorsque les agents font face à une dérive de contexte, des échecs d'outils, des boucles ou des impasses.
standalone: true
anthropic_compatible: true
bach_compatible: true
category: infrastructure
tags: [wayfinding, wayfinding-routing, survival-routing, dead-reckoning, pathfinder-routing, celestial-routing, auto-orientation, resilience, recuperation, heuristiques]
language: fr
status: active
---

> **Français** — Documentation officielle complète traduite en français pour la compétence `wayfinding-routing`.

# Navigation et Orientation (Wayfinding-Routing)

La compétence **Wayfinding-Routing** (également connue sous les noms **`survival-routing`**, **`dead-reckoning`**, **`pathfinder-routing`** et **`celestial-routing`**) sert de cadre ultime de navigation et de récupération d'urgence pour les agents LLM.

Elle dote les agents d'heuristiques de repérage proactives pendant l'exécution normale et de protocoles d'urgence lorsqu'ils rencontrent une dérive de contexte, des erreurs d'exécution récurrentes, des échecs d'API ou des impasses.

---

## Aperçu des Synonymes et Stratégies

| Stratégie Synonyme | Métaphore et Principe Clé | Cas d'Usage Appliqué |
| :--- | :--- | :--- |
| **`wayfinding-routing`** (Principal) | **Orientation Spatiale:** Naviguer sans GPS externe en lisant les panneaux de signalisation et les indices environnementaux. | Boucle de navigation principale pour sidecars, `workflowhooker` et `automation-self-care`. |
| **`survival-routing`** | **Navigation de Survie:** Interruption de circuit et dégradation progressive en cas de défaillance des outils. | Récupération d'urgence lorsque les commandes expirent, échouent de manière répétée ou heurtent des permissions. |
| **`dead-reckoning`** | **Navigation à l'Estime (Koppelnavigation):** Reconstitution de l'état exact étape par étape à partir du fil d'Ariane. | Suivi des étapes d'exécution dans des fichiers de travail ou `TODO.md` pour permettre un retour en arrière précis. |
| **`pathfinder-routing`** | **Éclaireur / Pionnier:** Inspection préalable et ouverture de voies pour les équipes multi-agents. | Inspection préalable des arborescences de répertoires, des verrous et des dépendances de tâches. |
| **`celestial-routing`** | **Navigation Astronomique:** Alignement avec les documents ancres immuables lorsque le contexte local est bruyant. | Retour de secours à `CLAUDE.md`, `AGENTS.md`, `START.md` lorsque les instructions de prompt entrent en conflit. |

---

## Les 5 Protocoles Majeurs de Secours et d'Orientation

### 1. `PROTOCOL-ANCHOR-RESET` (Réinitialisation d'Ancre / Navigation Astronomique)
- **Déclencheur (Trigger):** Dérive de contexte, instructions contradictoires de l'utilisateur ou perte d'orientation lors de longues sessions.
- **Règle Heuristique:** Arrêter la génération de texte libre. Effacer les hypothèses transitoires. Relire les documents ancres racines (`CLAUDE.md`, `AGENTS.md`, `START.md`). Réinitialiser l'état de l'objectif à la directive racine autorisée avant toute autre action.

### 2. `PROTOCOL-STOP-EXPLAIN` (Boucle de Réflexion et d'Explication)
- **Déclencheur (Trigger):** Une commande de terminal, une modification de fichier ou une requête d'API échoue deux fois avec une erreur identique.
- **Règle Heuristique:** **Bloquer l'exécution des commandes.** L'agent DOIT émettre une réflexion écrite formalisée avant de tenter un 3e essai:
  1. *Quelle erreur exacte s'est produite lors des essais 1 et 2?*
  2. *Pourquoi l'hypothèse de diagnostic précédente a-t-elle échoué?*
  3. *Quelle est la nouvelle approche alternative?*
  L'exécution est débloquée UNIQUEMENT après avoir écrit cette justification explicite.

### 3. `PROTOCOL-GRACEFUL-DEGRADATION` (Cascade de Dégradation Progressive)
- **Déclencheur (Trigger):** L'outil principal, le serveur MCP ou l'API externe est indisponible ou renvoie des erreurs.
- **Règle Heuristique:** Ne jamais échouer brutalement ni entrer dans des boucles à l'aveugle. Dégrader progressivement par niveaux:
  - **Niveau 1 (Optimal):** API native complète / Outil MCP
  - **Niveau 2 (Outil de Secours):** CLI locale Python / Script
  - **Niveau 3 (État en Lecture Seule):** Analyse directe des fichiers (`view_file` / texte brut)
  - **Niveau 4 (Transfert):** Présenter un rapport d'état structuré et des options ouvertes à l'utilisateur.

### 4. `PROTOCOL-BREADCRUMB-BACKTRACK` (Retour en Arrière par Fil d'Ariane)
- **Déclencheur (Trigger):** Une refactorisation complexe ou un flux de travail multi-étapes atteint un blocage insurmontable à l'étape N.
- **Règle Heuristique:** Enregistrer les fils d'Ariane avant d'effectuer des modifications destructrices. Si une voie échoue:
  1. Annuler les modifications non confirmées (`git checkout` / restaurer l'état).
  2. Sauter au dernier point de contrôle propre du fil d'Ariane.
  3. Marquer la route défaillante comme bloquée dans `TODO.md`.
  4. Tenter la voie alternative B.

### 5. `PROTOCOL-CIRCUIT-BREAKER` (Disjoncteur et Sortie Sécurisée)
- **Déclencheur (Trigger):** Les limites d'exécution sont atteintes, une boucle infinie est détectée ou une erreur critique survient.
- **Règle Heuristique:** Exécuter la séquence d'arrêt d'urgence:
  1. Libérer tous les verrous de fichiers et git acquis (`python -m workflowhooker check`).
  2. Enregistrer l'état partiel actuel dans `.SYNC/SURVIVAL_STATE.json` ou `AUTOMATIONS-MEMORY.md`.
  3. Consigner l'incident dans `ANTIGRAVITY-LOG.txt`.
  4. Quitter proprement avec un résumé exécutable pour l'utilisateur ou l'orchestrateur.