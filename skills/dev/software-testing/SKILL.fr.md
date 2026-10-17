---
name: software-testing
version: 1.0.1
type: knowledge-protocol
author: Lukas Geiger
created: 2026-08-22
updated: 2026-08-22
description: "Conseiller en stratégie de test pour projets logiciels — choisit les niveaux de test appropriés (unitaire/intégration/système/recette), les types de test (fonctionnel, non fonctionnel, lié aux modifications) et les techniques de conception de tests (classes d'équivalence, valeurs limites, tables de décision, exploratoire) pour la situation donnée et la phase SDLC/CI, y compris la pyramide de tests, les portes CI/CD, le Shift-Left et les bonnes pratiques. Utilise toujours cette compétence lorsque des tests doivent être écrits, planifiés, priorisés ou évalués — pour « écris des tests », « stratégie de test », « plan de test », « concept de test », « que/comment dois-je tester », « quels tests manquent », « améliorer la couverture de test », « mettre en place l'AQ », questions sur les tests de régression/smoke/sanity/charge/stress/sécurité, ou lors de la mise en place d'un pipeline de test — même si le mot « test » n'apparaît que incidemment. Délimitation — pour la boucle TDD elle-même, superpowers:test-driven-development ; pour le diagnostic de bugs, bugfix-protocol ; pour la recherche systématique de bugs, bugsweep."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [testing, teststrategie, qa, unit-test, integration, regression, testpyramide, shift-left, ci-cd, istqb]
language: fr
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'claude-code-recherche', 'origin_version': '1.0.0', 'created_from': 'Online-Recherche 2026-08-22 (ISTQB-Systematik, Testpyramide, Agile Testing Quadrants, moderne Verfahren); Quellen siehe testarten-katalog.md'}
translated_from_sha256: 85a9672454c8df2d2e0dfd1a87d5468a7ebc030e45a1fa2843f361bba80c8b80
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:43.791127+00:00"
---
<img src="banner.png" width="100%" alt="software-testing banner">

# Test logiciel : stratégie de test et sélection des tests

Cette compétence répond à la question « De quels tests ai-je besoin ici, maintenant, et dans quel but ? » — de façon systématique plutôt qu'au hasard. Elle fournit la logique de décision ; le catalogue complet de tous les types de tests, techniques et définitions se trouve dans `testarten-katalog.md` dans le même dossier (pour les questions de détail, s'y référer).

---

## 1. Cadre d'ordre : penser en trois dimensions

Avant de planifier ou d'écrire des tests, situe la tâche selon trois axes (ISTQB). Celui qui ne tient qu'« une liste de tests » mélange les axes et planifie de manière lacunaire :

| Axe | Question | Formes |
|---|---|---|
| **Niveau de test** | À quel niveau ? | Unitaire → Intégration → Système → Recette |
| **Type de test** | Quelle propriété ? | fonctionnel / non fonctionnel / structurel / lié aux modifications |
| **Technique de test** | Comment les cas de test sont-ils obtenus ? | Boîte noire / Boîte blanche / basée sur l'expérience |

Transversalement : **statique** (revues, analyse statique — sans exécution, détection d'erreurs la plus précoce et la moins coûteuse) vs. **dynamique** (le code est exécuté).

---

## 2. Routeur de situations : que se passe-t-il ?

Choisis le point d'entrée selon la situation concrète :

| Situation | Démarche |
|---|---|
| **Construire une nouvelle fonctionnalité** | Clarifier les critères d'acceptation AVANT le code (mentalité ATDD/BDD). Tests unitaires en parallèle de l'implémentation (classes d'équivalence + valeurs limites). Test d'intégration pour les nouvelles interfaces. Un parcours E2E nominal, pas davantage. |
| **Corriger un bug** | D'abord un test reproduisant le bug (rouge), puis le correctif (vert) = **re-test**. Ensuite la **régression** de l'environnement. Le diagnostic lui-même → `bugfix-protocol`. |
| **Refactoring** | AUCUN nouveau test de fonctionnalité — la suite existante est le filet de sécurité. Vérifier au préalable si la suite couvre réellement le comportement (le cas échéant, ajouter des tests de caractérisation). Couverture/mutation comme indicateur de lacunes. |
| **Code legacy sans tests** | Ne pas commencer par des tests unitaires de chaque fonction. D'abord des tests de caractérisation au niveau système/API autour du comportement actuel, puis ajouter des tests unitaires au fil des modifications de parties individuelles. |
| **API / microservices** | Accent sur les tests d'API au niveau du service (niveau médian de la pyramide). Avec des équipes/déploiements séparés : **Contract Testing** (p. ex. Pact) plutôt que des tests d'intégration communs en staging. |
| **Préparer une mise en production** | Ordre : smoke (build stable ?) → régression complète → tests non fonctionnels (charge, sécurité) → UAT/recette → smoke sur le candidat de release. |
| **Inquiétude sur la performance** | Définir d'abord un objectif mesurable (p. ex. « P95 < 300 ms pour 1 000 utilisateurs »), sans quoi aucun test n'est exploitable. Test de charge = charge normale, test de stress = point de rupture + récupération. Environnement proche de la production obligatoire. |
| **Mettre en place un pipeline de test** | Implémenter les portes CI/CD de la section 4 ; commencer par unitaires + lint à chaque commit, puis étendre progressivement. |
| **Rédiger une stratégie/un concept de test** | Structure le long des 3 dimensions + correspondance par phase (section 4) + priorisation basée sur les risques (section 6, point 10). |

---

## 3. Niveaux de test : objet, objectif, moment

| Niveau | Vérifie | Quand | Règle empirique |
|---|---|---|---|
| **Unitaire/composant** | Fonction/classe individuelle isolée (mocks/stubs) | Pendant l'implémentation, chaque commit | Base large de la pyramide ; rapide (< secondes), déterministe |
| **Intégration** | Interaction, interfaces, connexion à la BDD | Après les tests unitaires, à chaque fusion | Intégrer progressivement (descendant/ascendant), jamais de big bang pour les grands systèmes |
| **Système** | Système complet face aux exigences techniques | Dès qu'un build intégré existe | Fonctionnel ET non fonctionnel ; des testeurs indépendants sont précieux |
| **Recette** | Attentes métier, usage réel | Dernier niveau avant la mise en service | UAT par le métier ; ne pas oublier l'exploitation (sauvegarde/déploiement/monitoring) ; le cas échéant alpha/bêta |

**Pyramide de tests** comme rapport de proportions : beaucoup de tests unitaires, des tests d'intégration/API ciblés, peu de tests E2E (règle empirique ~70/20/10 comme point de départ — à ajuster selon l'origine réelle des erreurs). Pyramide inversée (beaucoup de tests d'interface) = lente + instable → à éviter.

---

## 4. Correspondance par phase : quand tester quoi ?

### Portes CI/CD (correspondance standard moderne)

| Étape du pipeline | Porte |
|---|---|
| Chaque commit | Tests unitaires, linters, analyse statique (secondes–minutes) |
| Pull Request | Revue de code, SAST/SCA, tests de composants ciblés |
| Fusion | Tests d'intégration/API/contrat, smoke sur l'environnement de test |
| Nightly / pré-release | Régression complète, E2E, tests de performance/charge, DAST |
| Candidat de release | Smoke en staging, UAT, recette |
| Production (Shift-Right) | Monitoring/observabilité, canary/blue-green, feature flags, le cas échéant expériences de chaos |

**Budgets temporels et règles de blocage (valeurs indicatives tirées de la pratique) :**

- **Commit-à-retour < 10 minutes** pour le chemin rapide (lint + unitaires + tests d'intégration critiques) ; pipeline complet jusqu'au staging **< 30–45 minutes** ; régression complète nightly ou avant release. Une boucle de régulation qui cadence plus lentement sera contournée.
- **Bloquant vs. signalant :** les portes unitaires, d'intégration et smoke bloquent TOUJOURS (en cas de rouge, pas de fusion/déploiement). Les étapes nightly (régression, charge, DAST) signalent via ticket/correctif, sans bloquer chaque commit. Après le déploiement en production : smoke + monitoring — en cas de rouge, rollback + incident.
- **Point de transfert :** le commit (git push) sépare la boucle interne (locale : TDD, unitaires, itération rapide) de la boucle externe (pipeline partagé avec portes). Ce qui peut être déplacé vers la boucle interne y est détecté au moindre coût (Shift-Left).

### Classique (modèle en V) : concevoir les tests lors de la spécification

Exigences ↔ test de recette · conception système ↔ test système · architecture ↔ test d'intégration · code ↔ test unitaire. Idée centrale : les tests d'un niveau sont conçus **lors de la rédaction de la spécification correspondante** — et non seulement à la fin. Les revues des exigences/conceptions (test statique) sont la détection d'erreurs la plus précoce de toutes.

### Agile Testing Quadrants (grille de planification pour les sprints)

Q1 Unitaire/TDD + Q2 tests de récit/BDD fonctionnent en continu et **préviennent** les erreurs ; Q3 exploratoire/utilisabilité/UAT + Q4 performance/sécurité **évaluent** le produit, dès qu'il existe suffisamment de produit. Détails dans le catalogue.

---

## 5. Choisir la technique de conception de tests

| Si la base de test … | … alors technique |
|---|---|
| comporte des plages de saisie/ensembles de valeurs | **Classes d'équivalence** (un représentant par classe) + **analyse des valeurs limites** (sur et juste au-delà de chaque limite : pour 5–50, tester 4, 5, 50, 51) — l'équipement de base pour presque tout test unitaire |
| comporte des règles métier complexes/combinaisons de conditions | **Test par table de décision** |
| décrit des états et transitions (workflow, session, appareil) | **Test de transition d'état** (tester aussi les transitions interdites) |
| décrit des parcours utilisateurs | **Test de cas d'utilisation/scénario** incl. chemins d'erreur et d'exception |
| est du code et la couverture doit être mesurée | **Couverture des instructions/branches** — comme indicateur de lacunes, pas comme objectif (100 % de couverture ≠ correct) |
| est flou/lacunaire ou le temps manque | **Test exploratoire** (sessions à durée limitée avec charter) + **Error Guessing** (nul, chaîne vide, caractères spéciaux, fuseaux horaires, conditions de concurrence) |

Techniques systématiques d'abord, techniques basées sur l'expérience **en complément** délibéré — elles trouvent ce que les scripts manquent.

---

## 6. Bonnes pratiques (checklist pour planifier/relire des tests)

1. **Shift-Left :** revues + analyse statique dès la phase des exigences — plus une erreur est trouvée tard, plus elle coûte cher (règle empirique répandue d'après Boehm ; la direction est incontestée, les facteurs exacts sont débattus).
2. **Respecter la pyramide de tests** — tests E2E parcimonieux, base unitaire large.
3. **Automatiser ce qui se répète** (smoke, régression, API, unitaires) et l'ancrer dans les portes CI/CD ; réserver la capacité manuelle à l'exploratoire et à l'utilisabilité.
4. **Concevoir les cas de test systématiquement** (section 5), pas au hasard.
5. **Rendre les exigences non fonctionnelles mesurables** — sans objectif chiffré, pas de test de performance/charge exploitable.
6. **Re-test ≠ régression :** d'abord confirmer le correctif, puis les effets de bord. Ordre smoke → sanity/re-test → régression.
7. **Traiter immédiatement les tests instables (flaky)** — mettre en quarantaine, corriger la cause ou supprimer ; des suites instables détruisent la confiance dans le pipeline.
8. **Gérer les données et environnements de test :** reproductibles (conteneurs/IaC), proches de la production, données anonymisées ou synthétiques.
9. **Mesurer la qualité des tests eux-mêmes :** couverture comme indicateur de lacunes ; **test de mutation** là où les chiffres de couverture pourraient tromper.
10. **Prioriser selon les risques :** profondeur de test selon l'impact de la défaillance × probabilité d'erreur — pas uniformément réparti.
11. **La qualité est une affaire d'équipe** (approche Whole-Team) : impliquer les testeurs tôt dans les exigences ; BDD/ATDD comme véhicule commun avec le métier.
12. **Ne pas oublier le Shift-Right :** monitoring, canary, feature flags ; l'ingénierie du chaos seulement avec une observabilité mature.

---

## 7. Méthodes modernes — quand les ajouter

| Méthode | À utiliser quand … |
|---|---|
| **Contract Testing** (Pact) | Microservices avec déploiements/équipes séparés |
| **Mutation Testing** (Stryker, PIT, mutmut) | La qualité d'une suite de tests existante doit être évaluée |
| **Property-Based Testing** (Hypothesis, fast-check) | Des invariants existent (« trier est idempotent ») et les cas limites sont redoutés |
| **Fuzzing** | Analyseurs, désérialisation, entrées critiques pour la sécurité |
| **Chaos Engineering** | Systèmes distribués + observabilité mature + rollbacks propres |

---

## Compétences voisines (ne pas dupliquer)

- **`superpowers:test-driven-development`** — la boucle concrète Red-Green-Refactor lors de l'écriture de code.
- **`bugfix-protocol`** — diagnostic en 6 phases d'un bug concret.
- **`bugsweep`** — parcours systématique de recherche de bugs sur une base de code.
- **`dev-cycle`** — cycle global en 8 phases (à partir de sa v1.2.0 : les tests sont conçus dans les phases 1/3/5, rédigés en phase 6 et exécutés en phase 7 ; cette compétence précise QUELS tests doivent s'exécuter OÙ).

## Référence

Catalogue complet (tous les niveaux de test, types de test avec tableau détaillé des tests non fonctionnels, toutes les techniques de conception, Agile Quadrants, statique/dynamique, modèle en V, sources) :
→ `testarten-katalog.md` (dans le même dossier)

Carte visuelle d'ensemble — phases, boucles de régulation, rôles et portes de test sous forme de « schéma de circuit du développement logiciel » (feuille BL-5 = intégration des tests, BL-2 = cadence des boucles de régulation) :
→ `../dev-cycle/SCHALTPLAN-SOFTWAREENTWICKLUNG.html` (à ouvrir dans le navigateur)

---

## Journal des modifications

### 1.0.1 (2026-08-22)
- Budgets temporels et règles de blocage pour les portes CI/CD ajoutés (< 10 min chemin rapide, < 30–45 min pipeline ; bloquant vs. signalant ; rollback après rouge en production) ainsi que le commit comme point de transfert boucle interne/externe
- Renvoi vers l'annexe schéma de circuit de la compétence dev-cycle ; délimitation avec dev-cycle adaptée à sa v1.2.0 (Shift-Left : concevoir 1/3/5, rédiger 6, exécuter 7)

### 1.0.0 (2026-08-22)
- Version initiale issue de recherches en ligne (systématique ISTQB, pyramide de tests, Agile Testing Quadrants, portes CI/CD, méthodes modernes)
