---
name: choose-your-orchestrator
version: 1.1.0
type: skill
author: Lukas Geiger + Codex
created: 2026-08-20
updated: 2026-10-03
description: "Choisit, avec l'utilisateur, une orchestration appropriée et limitée avant un travail multi-agents complexe, puis génère un contrat de session compact. Utilise ce skill sur /choose-your-orchestrator, lorsque la combinaison d'orchestrateur, d'essaim, de routage de modèles ou de modèle de préférences utilisateur est incertaine, ainsi que pour les programmes d'agents qui doivent expressément fixer les emplacements de modèles, le parallélisme, la profondeur de création, les limites d'écriture, la validation et l'escalade."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [orchestrierung, multi-agent, delegation, routing, budget, matruschka, session-vertrag]
aliases: [choose-your-orchestrator]
language: fr
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [orchestrator, swarm-operations, model-strategy, decision-avatar, budgetierung]
  python: []

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: github.com/ellmos-ai/skills
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 0b3feaa40d5c9d5310977fbc0e9c92572c1504e201baad19e7b73c7b64e4e846
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.875424+00:00"
---
<img src="banner.png" width="100%" alt="choose-your-orchestrator banner">

# Choose Your Orchestrator

## Objectif

Clarifier, avant un travail multi-agents complexe, les conditions cadres, recommander la plus petite combinaison efficace de skills existants et produire un contrat d'orchestration de session contraignant. Charge les skills sélectionnés via le mécanisme de skills du runtime actuel et suis leurs instructions en direct. Ne copie pas leurs procédures dans ce skill.

La délégation n'élargit jamais l'autorité. Les actions externes ou irréversibles, comme publier, envoyer, supprimer, payer ou effectuer des modifications en production, restent soumises à l'accord de l'utilisateur, sauf si la tâche en cours les autorise explicitement.

## Briques

| Brique | Rôle dans le contrat | Hors de son rôle |
|---|---|---|
| `orchestrator` | Lots de travail, périmètres, preuves et validation | Inventer le choix de modèle ou le schéma d'essaim |
| `swarm-operations` | Schéma d'essaim, porte de coût et échelonnement Matriochka optionnel | Paralléliser artificiellement des tâches individuelles |
| `model-strategy` | Route selon les capacités et les modèles, d'après la disponibilité en direct | Imposer des versions de modèles fixes ou des autorisations |
| `clutch` | Proposition de routage externe optionnelle | Autorité unique pour la répartition ou le périmètre |
| `decision-avatar` | Signal de préférence autorisé optionnel pour les incertitudes réversibles | Remplacer les accords de l'utilisateur ou étendre l'autorité |
| `budgetierung` | Quotas négociés par fenêtre temporelle pour les modèles, relecteurs et conseillers coûteux, avec compte et vérification préalable avant les escalades | Choisir les modèles sur le fond (c'est le rôle de `model-strategy`) ni fixer les quotas unilatéralement |

Utilise `clutch route "<kurze Aufgabenbeschreibung>" --json` uniquement si `clutch` est réellement disponible. Traite la réponse JSON comme une proposition et confronte-la aux emplacements d'exécution disponibles, au budget, aux règles du projet et aux limites de l'utilisateur. Si `clutch` est indisponible ou si sa sortie est illisible, utilise `model-strategy` et les capacités en direct du runtime. N'inscris jamais de noms ou de versions de modèles actuels en dur dans le contrat.

## Dialogue de recommandation

### 1. Qualifier la tâche

Détermine l'objectif, le type de tâche, les critères de réussite, les périmètres exclus, les autorisations actuelles, les verrous existants et les lots de travail indépendants. Choisis d'abord la route la plus petite et pertinente dans le tableau ci-dessous.

### 2. Proposer le contrat

Présente une ébauche compacte comprenant :

1. les briques et les rôles,
2. les emplacements de modèles et de budget (pour les exécutions de plusieurs heures ou les modèles rares/coûteux, négocier via `budgetierung` et tenir un compte),
3. le parallélisme maximal et la profondeur de création,
4. les limites d'écriture et les verrous,
5. la validation et les preuves,
6. l'escalade et les questions à l'utilisateur,
7. la limite d'autorité.

Recommande des valeurs concrètes et nomme en une phrase le principal compromis. Ne pose des questions que sur les décisions qui modifient matériellement le résultat. Regroupe les questions ouvertes en trois groupes au maximum, clairement séparés ; présente à chaque fois l'option recommandée en premier. Si toutes les dimensions sont déjà expressément fixées, ne repose pas la question.

### 3. Confirmer ou réduire

Ne lance aucune répartition multi-agents tant qu'une question matérielle de budget, d'écriture ou d'autorité reste ouverte. Si seul l'intérêt du parallélisme est incertain, réduis à un exécutant unique. Une tâche explicitement autorisée peut démarrer avec les valeurs par défaut sûres si aucune décision matérielle de l'utilisateur ne manque.

### 4. Produire le contrat

Affiche le contrat confirmé dans le chat. Si une commande `usmc` est disponible, consulte d'abord son aide, puis écris en plus, via une commande note/écriture documentée à cet endroit, une note de session respectueuse de la vie privée. N'invente aucune sous-commande et n'enregistre ni prompts bruts, ni secrets, ni contenus privés. Sans voie d'écriture USMC disponible, le contrat dans le chat fait foi.

## Tableau de routage

| Type de tâche | Recommandation | Découpage par défaut |
|---|---|---|
| Audit / balayage | `orchestrator` + `swarm-operations` ; `model-strategy` si les classes de capacités diffèrent | domaines indépendants, petit groupe `parallel-chunks` ou `specialist`, fusion centrale |
| Programme de construction | `orchestrator` + `model-strategy` ; essaim seulement pour des flux réellement indépendants | le chef planifie et valide, les workers construisent dans des domaines disjoints |
| Construction unitaire | Exécutant unique ; `model-strategy` ou `clutch` facultatif pour la route | pas de surcharge d'essaim ou de hiérarchie |
| Exploitation de tickets | Le système de tickets reste en tête ; `orchestrator` complète les contrats de travail et les preuves | ne pas remplacer le régime de routeur/score existant, respecter le cycle de vie du ticket |

## Valeurs par défaut sûres

Utilise ces valeurs, sauf si l'utilisateur, le runtime ou les règles du projet imposent plus de rigueur :

- au maximum deux workers actifs ; commence par un seul et démontre l'intérêt du second,
- Matriochka désactivé, profondeur de création maximale `0`,
- aucun sous-agent propre aux workers sans autorisation explicite,
- un seul rédacteur par dépôt ou par domaine clairement délimité,
- revendications de fichiers disjointes et verrous habituels du projet avant toute écriture,
- le chef/orchestrateur vérifie lui-même les artefacts, les diffs et les tests,
- les déclarations de fin ne valent qu'après validation par les preuves,
- les actions irréversibles ou externes restent soumises à l'accord de l'utilisateur,
- les incertitudes sont regroupées plutôt que signalées comme de nombreuses interruptions isolées.

N'active Matriochka que si l'utilisateur le confirme expressément et si le contrat précise, pour chaque niveau, la classe de modèle/capacité, la limite de créneaux actifs, les sous-tâches autorisées et la profondeur maximale. Compte les agents actifs, et non simplement ceux qui existent. Même dans ce cas, il ne reste qu'un seul rédacteur par domaine.

## Format du contrat

```text
SESSION-ORCHESTRIERUNGSVERTRAG
Ziel und Typ: <Ergebnis; Audit/Bauprogramm/Einzelbau/Ticket-Betrieb>
Bausteine: <geladene Skills und optionale Router>
Chef: <Planung, Denkarbeit, Integration, Evidenzabnahme>
Worker-Slots: <Rolle/Fähigkeitsklasse je Slot; Budgetgrenze; Budget/Konto: <budgetierung-Konto, Pfad>>
Parallelität: <maximal aktiv>; Spawn-Tiefe: <0..N>; Matruschka: <aus/an>
Schreibgrenzen: <ein Schreiber je Bereich; Claims; Locks; negative Scopes>
Abnahme: <Artefakte, Tests, Diffs, Quellen; wer prüft>
Eskalation: <Stopps; höchstens drei gebündelte Nutzerfragen>
Autorität: <zulässige Aktionen; extern/irreversibel user-gegatet>
Persistenz: <Chat autoritativ; USMC-Notiz ja/nein und privacy-neutral>
```

## Exemple

```text
Auftrag: Drei unabhängige Komponenten prüfen und einen Fix integrieren.
Empfehlung: orchestrator + swarm-operations; zwei aktive Read-only-Reviewer,
danach genau ein Integrationsschreiber. Matruschka aus, Tiefe 0. Der Chef prüft
Fundstellen, Diff und Gesamttests. Push oder Veröffentlichung nur im ausdrücklich
autorisierten Scope.
Offene Frage: Ist die zweite parallele Review-Spur den zusätzlichen Verbrauch wert?
Empfehlung: ja, weil die Komponenten unabhängig sind.
```

## Conditions d'arrêt

Arrête ou réduis l'orchestration si les périmètres se chevauchent, si les verrous ne sont pas clairs, si le runtime ne propose pas l'emplacement recommandé, si le budget n'est pas confirmé ou si la validation ne peut pas être démontrée de façon indépendante. Demande à l'utilisateur plutôt que de deviner une nouvelle décision de produit, de confidentialité ou d'autorité.

## Journal des modifications

### 1.1.0 (2026-10-03)
- Ajout de `budgetierung` comme brique pour les quotas de modèles négociés par compte (tableau des briques, emplacements de modèles et de budget dans le dialogue de contrat, ligne du format de contrat pour les emplacements de workers).

### 1.0.0 (2026-08-20)
- Introduction du dialogue de recommandation, du tableau de routage et du contrat de session compact.
- Définition des valeurs par défaut sûres pour le parallélisme, Matriochka, les limites d'écriture, les preuves et les actions externes.
- Description de l'intégration optionnelle de `clutch` et d'un modèle de préférences autorisé, sans liaison fixe à un modèle ni extension d'autorité.
