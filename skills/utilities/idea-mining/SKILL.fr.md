---
name: idea-mining
version: 1.2.1
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-11-22
description: "Utilisez cette compétence lorsqu'un problème difficile stagne depuis longtemps et que de nouvelles pistes doivent être trouvées, filtrées contre ce qui a déjà été tenté, puis poussées jusqu'au bout : recherche, preuves, blocages d'architecture, /idea-mining. Ne PAS utiliser pour une liste rapide d'idées sans filtre (brainstorm) ni pour choisir entre des options déjà prêtes (decide)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [ideen, kreativität, forschung, beweis, analogie, allegorie, recherche, innovation]
language: fr
status: active
visibility: public
dependencies:
  tools: []
  services: [websearch]
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="idea-mining banner">

> **Français** — Version française officielle de la compétence `idea-mining`.

# Idea-Mining — Extraire des idées, filtrer, en mener une à terme

## Vue d'ensemble et finalité

Face aux problèmes difficiles, la recherche d'idées échoue rarement par manque d'inspiration, mais pour trois raisons : les idées ne sont pas **consignées**, elles ne sont pas vérifiées par rapport à **ce qui a déjà été tenté** (on s'engouffre dans les mêmes impasses) et aucune n'est poursuivie **jusqu'au bout**. Ce flux de travail sépare strictement les trois phases : d'abord extraire de manière divergente (sans évaluation), ensuite filtrer (contre la documentation du projet), puis explorer substantiellement UNE idée.

Origine : distillé à partir d'une exécution productive d'automatisation de recherche sur des problèmes mathématiques ouverts ; fonctionne tout aussi bien pour les blocages d'architecture, de design et de conception.

## Phase A — Remplir le réservoir d'idées (divergent, sans évaluation)

Consigner toutes les trouvailles dans un fichier `IDEENSPEICHER.md` dans le dossier du projet (mots-clés + 2 à 3 phrases, noter la source/déclencheur). Parcourir successivement les huit techniques — elles ciblent des espaces associatifs différents ; sur des problèmes réellement enlisés, n'en sauter aucune (pour des blocages plus légers ou sous contrainte de temps, un sous-ensemble justifié suffit, mais au moins une technique souple parmi 3–5 plus la recherche documentaire) :

1. **Reconnaissance :** Est-ce que cela me dit quelque chose ? Ai-je déjà vu cette structure dans un autre contexte ?
2. **Discipline lointaine :** Existe-t-il un problème similaire ou une formule analogue dans une discipline très éloignée (physique ↔ économie, biologie ↔ informatique, …) ? Où se situe exactement le pont ?
3. **Allégorie du quotidien :** Raconter le problème sous forme d'allégorie proche de la nature (vagues, sable, courant, croissance…). Très efficace : faire inventer l'allégorie par un **sous-agent vierge de contexte** puis observer où elle mène — son propre regard est déjà déformé par le problème.
4. **Inconfort / Crapaud → Prince :** Qu'est-ce qui me gêne dans l'état actuel, qu'est-ce que je trouve laid ? Que faudrait-il changer pour que je le trouve soudain beau ? Le malaise esthétique pointe souvent vers une mauvaise représentation choisie.
5. **Recadrage en conte :** Raconter le problème comme un conte : qui est le héros, qui sont les méchants, quels dangers rôdent, qu'est-ce qui pourrait aider le héros ? L'attribution de rôles impose une structure causale qui reste invisible dans le formalisme.
6. **Recherche documentaire :** Explorer le web, les bases scientifiques, les serveurs de prépublications et les forums (Reddit/ResearchGate/GitHub) à la recherche de publications récentes, scripts et approches. Télécharger les sources pertinentes dans un dossier `_sources/` et y chercher les innovations — rester critique envers les prépublications.
7. **Projets frères :** Examiner ses propres projets apparentés pour y trouver des idées de solutions rétro-transférables (sous-problèmes résolus là-bas, outils construits là-bas).
8. **Balayage transversal du portefeuille :** Passer en revue tout son parc de projets (pipeline) à la recherche d'approches susceptibles de s'appliquer à CE problème.

## Phase B — Filtre (contre ce qui a déjà été tenté)

Comparer le réservoir d'idées à la documentation du projet : notes de preuve, journaux de décisions, TODO/DONE, anciens réservoirs d'idées. **Est éliminé ce qui est documenté comme déjà tenté et clos** — et non ce qui « semble seulement improbable » (l'évaluation selon l'attractivité n'intervient qu'en phase C). Enregistrer les survivantes dans `IDEENSPEICHER_FILTERED.md`.

Le prérequis est une documentation des essais tenue à jour — s'il n'en existe aucune, la première étape consiste à la créer (sinon chaque exécution future produira des répétitions).

## Phase C — Choisir et mener à terme

1. Pré-explorer brièvement une à trois idées issues du filtrat (un paragraphe chacune : quel serait le premier pas concret, quel serait le signal de succès ?).
2. En choisir **une** — celle qui exerce la plus forte attraction. L'attraction est ici un critère légitime : sur des problèmes ardus, seule tient la route une idée qu'on a *envie* d'explorer.
3. Mener ce choix jusqu'au bout ou du moins de manière substantielle — ne pas sauter à l'idée suivante au premier obstacle (ce serait importer le comportement de la phase A dans la phase C).

## Phase D — Documenter

- Consigner les enseignements dans la documentation du projet (note de preuve, journal de décisions, ADR) — **y compris les échecs**, car ils constituent le filtre de la prochaine exécution.
- Renvoyer les idées dérivées ouvertes dans `IDEENSPEICHER.md` ou dans le TODO.
- Bilan synthétique : extraites (nombre) | filtrées (survivantes) | explorées | résultat | prochaine étape.

## Phase E — Essaimage (rétro-transfert optionnel vers l'extérieur)

La technique 7 fait ENTRER des idées depuis les projets frères — la phase E inverse le sens : lorsque l'exploration a produit quelque chose de transférable (méthode, outil, schéma de solution), passer rapidement en revue son portefeuille de projets : à qui cela profiterait-il ?

- **Semer de manière ciblée, pas dispersée :** doter au plus ~3 projets destinataires directement d'une entrée TODO concrète (quoi reprendre, où cela se trouve, pourquoi cela convient) ; noter les autres candidats seulement comme liste priorisée dans le projet d'origine.
- Raison de la limite : un semis trop large crée dans de nombreux projets des tâches vagues dont personne ne s'empare — trois graines précises battent dix graines diffuses.

## En exécution périodique

Ce flux convient comme automatisation récurrente sur un projet fixe (cycle d'innovation). Pour cela, le combiner avec l'ossature de rotation (compétence `rotation-check`) : le registre empêche que les mêmes idées soient « redécouvertes » à plusieurs reprises — le réservoir d'idées et la documentation des essais jouent ici le rôle de mémoire.

## Exemple et application

```text
Problème : Une démonstration de convergence bloque depuis des semaines sur une majoration.

A) Extraction → IDEENSPEICHER.md : entre autres (2) structure similaire dans la théorie
   des files d'attente ? ; (3) allégorie d'un sous-agent « du sable s'écoule à travers des
   tamis de plus en plus fins » → idée : majoration par paliers plutôt que globale ; (6)
   prépublication de 2026 avec un nouveau lemme, chargée dans _sources/ ; (7) un projet
   voisin possède un script de vérification numérique rétro-transférable.
B) Filtre contre BEWEISNOTIZ.md : « resserrer la majoration globale » a été tenté 2× et
   écarté par écrit → éliminé. 3 idées survivent → IDEENSPEICHER_FILTERED.md.
C) Choix principal : l'idée du tamis (plus forte attraction) — poursuivie jusqu'à un
   résultat partiel.
D) BEWEISNOTIZ.md mis à jour (y compris l'échec de l'idée 2), bilan synthétique.
```

## Signaux d'alerte (Red Flags)

| Pensée | Réalité |
| --- | --- |
| « Les techniques 3 à 5 sont un jeu inutile » | Les techniques souples fournissent les idées que la recherche documentaire ne peut pas livrer — elles adressent d'autres espaces associatifs. |
| « J'évalue déjà pendant la collecte » | Évaluer en phase A tue la richesse divergente. Stocker d'abord, filtrer ensuite. |
| « Le filtre est trop long, je m'en souviens bien » | La mémoire lisse les essais infructueux — seule la documentation fait foi. |
| « L'idée coince, je passe à la suivante » | En phase C, on va jusqu'au bout ; ne revenir en A qu'avec une justification documentée. |

## Compétences apparentées

- `brainstorm` — méthodes créatives larges (SCAMPER, Six Hats) sans pipeline de filtrage/exploration.
- `think` / `decide` — analyse et choix décisionnel, utilisables au sein de la phase C.
- `rotation-check` — ossature pour l'usage périodique.
- `swarm-operations` — sous-agents vierges pour la technique 3 et l'exploration parallèle.

## Journal des modifications

### 1.2.1 (2026-11-22)
- Indication de langue corrigée

### 1.2.0 (2026-11-06)
- Description reformulée avec déclencheur clair et délimitation (règle issue de `docs/CONVENTIONS.md`) : situation d'usage, formulations typiques et commande slash en tête, compétences voisines dans une clause « Ne PAS utiliser ».

### 1.1.0 (2026-07-03)
- Phase E « Essaimage » : transfert sortant optionnel de résultats transférables vers des projets frères (max. ~3 destinataires directs) — intégrée au lieu d'en faire une compétence distincte `cross-project-transfer` (décision de déduplication).

### 1.0.0 (2026-07-03)
- Version initiale. Abstraite de l'automatisation Codex `ultra-deep-idea-search-single-project` (réservoir d'idées → filtre → choix principal → exploration) et généralisée de façon neutre vis-à-vis de l'utilisateur.
