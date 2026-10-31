---
name: agent-role-scaffolder
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-25
updated: 2026-08-25
description: "Construit et vérifie de nouveaux rôles d'agents dans l'écosystème ellmos : sous-agents natifs de Claude Code (définition de rôle persistante) et workers compagnons (instance réutilisée via SendMessage pour une série de tickets/tâches). Formalise le savoir-faire jusqu'ici non formalisé issu de la construction en cours de rôles d'agents (ati-agent, bueroassistent, versicherungs-agent, etc.) en un processus réutilisable de scaffold puis de vérification. Utilise cette compétence lorsqu'un nouveau rôle doit être créé (« construire un nouveau rôle d'agent », « créer un sous-agent », « lancer un worker compagnon ») ou lorsqu'un rôle existant doit être contrôlé par rapport aux conventions de la maison (« cet agent est-il correctement configuré ? »)."
visibility: public
language: fr
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
translated_from_sha256: 55b76ad25a5d65f61987662e674bc9c74ea0f6a8586ad4748268bc9441711db5
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.234921+00:00"
---
<img src="banner.png" width="100%" alt="agent-role-scaffolder banner">

# agent-role-scaffolder

<!-- FAMILY-ROUTER:Agenten-Orchestrierung START -->
> **Famille Orchestration d'agents — Guide :** choisir/échelonner le modèle -> `model-strategy` ; choisir un modèle d'orchestration -> `choose-your-orchestrator` ; opérations en essaim (5 modèles de base + 2 modes) -> `swarm-operations` ; décomposer/déléguer/réceptionner une tâche -> `orchestrator` ; messagerie inter-fournisseurs/présence/verrous -> `agents-bridge` ; **construire ou vérifier un nouveau rôle -> cette compétence (agent-role-scaffolder)**.
<!-- FAMILY-ROUTER:Agenten-Orchestrierung END -->

## Objectif

Cet écosystème dispose déjà d'une famille mature de compétences d'orchestration
(`model-strategy`, `swarm-operations`, `orchestrator`, `choose-your-orchestrator`,
`agents-bridge`) — mais **aucune d'entre elles ne traite la question « comment
créer correctement un nouveau rôle ».** C'est cette lacune que comble
`agent-role-scaffolder`. Il ne duplique pas les compétences citées, mais **renvoie vers
elles** dès que l'échelonnement, le modèle d'orchestration ou la messagerie
inter-fournisseurs sont nécessaires.

**Origine :** décision utilisateur M5 issue du ticket `T-20260825-935905816`
(revue complète du marketplace) : verdict (b) — le savoir-faire propre sur la
construction d'agents existait, mais n'était pas formalisé. Le plugin officiel
Claude Code `agent-sdk-dev` (claude-plugins-official, Apache-2.0) a servi de
**modèle structurel** : un fichier de commande de scaffolding plus deux sous-agents
vérificateurs thématiques dotés d'une checklist et d'un format de rapport
PASS / PASS-WITH-WARNINGS / FAIL. C'est la **forme** qui a été reprise
(catalogue de questions de scaffold → construction → checklist de vérification
avec rapport structuré), pas le texte ni l'objet : ce plugin construit des
applications Claude Agent SDK brutes (Python/TypeScript), tandis que cette
compétence construit des **rôles d'agents propres à ellmos** (définitions de
sous-agents et workers compagnons). L'original n'est PAS installé ; il se trouve
en lecture seule dans le cache local du marketplace et n'a été que lu
(`.PLUGINS/CLAUDE.md` règle 5 : idées librement, formulations non). Entrée de
registre : `.AI/.PLUGINS/PLUGIN-REGISTER.md`, statut `zitiert`.

## Deux voies de construction — toutes deux relèvent d'ici

Dans l'écosystème ellmos, de nouveaux rôles naissent selon deux voies
structurellement différentes qu'il ne faut pas confondre (analogue à la séparation
TS/Python du plugin modèle — ici, toutefois, le long de la véritable frontière
du système) :

| | **Sous-agent natif** | **Worker compagnon** |
|---|---|---|
| Ce qui est créé | une définition de rôle persistante (`~/.claude/agents/<name>.md`, démarrable via l'outil `Agent`) | une instance nommée ad hoc, réutilisée via `SendMessage` pour UNE série de tâches |
| Durée de vie | persistante, réutilisable d'une session à l'autre | pour la durée d'une série de tickets/thèmes, puis supprimée |
| Exemples existants | `ati-agent`, `bueroassistent`, `versicherungs-agent`, `gesundheitsassistent`, `persoenlicher-assistent`, `production`, `research-agent`, `reflection-agent`, `test-agent`, `entwickler-agent` | ce modèle de session lui-même (p. ex. `skillcreator-bau`, `policyreg-decisions`, `workflowhooker-ausbau` — workers nommés dans le système de tickets) |
| Couche de cycle de vie | registre d'agents propre à Claude Code | **COMA** (`.MODULES/.ORCHESTRATION/coma`) — s'il est lancé entre processus, et non seulement au sein de l'outil |
| Guide de construction ici | `references/subagent-role-scaffold.md` | `references/companion-worker-scaffold.md` |

**Règle empirique :** si la capacité requiert un nom propre et réutilisable sur de
nombreuses sessions, avec une description de déclenchement fixe (p. ex. « chaque fois
qu'il est question de justificatifs fiscaux ») → sous-agent natif. S'il s'agit d'une
série limitée mais cohérente de tâches qu'un coordinateur délègue en ce moment
(chaîne de tickets, changement de thème) → worker compagnon.

## Déroulement

1. **Choisir la voie de construction** (tableau ci-dessus) — en cas de doute, demander
   à l'utilisateur plutôt que deviner.
2. **Parcourir les questions de scaffold** (voir `references/*.md` correspondant) — comme
   le plugin modèle, une à une et non toutes à la fois : objectif/déclencheur,
   besoin en outils (`Tools:`), choix du modèle (→ **étape 3**), besoin de
   coordination (agent chef avec experts ou rôle unique ?).
3. **Ne PAS décider du modèle ici — déléguer à `model-strategy`.** La sélection
   fondée sur un score, la délégation inter-agents, l'appariement conseiller et les
   déclencheurs d'escalade y sont déjà traités ; ici, seul le renvoi. Règle empirique
   issue de l'existant : les sous-agents n'héritent **pas systématiquement** du modèle
   principal (voir la mémoire de retour `feedback_subagenten_modellstaffelung`).
4. **Vérifier le modèle d'orchestration**, si le nouveau rôle doit collaborer avec
   plusieurs autres — `choose-your-orchestrator` choisit le modèle, `swarm-operations` fournit les
   5 modèles de base + 2 modes, `orchestrator` le protocole de décomposition /
   délégation / réception.
5. **Respecter les conventions d'équipe et de messagerie** (`references/
   model-staffing-and-messaging.md`) :
   `SendMessage` pour la communication inter-agents, réservation de ticket par nom de
   fichier lors de la délégation de tickets, « renvoyer plutôt que répéter » lors de la
   mission (ne pas réénoncer dans le prompt les règles centrales, seulement ce qui est
   propre à la tâche).
6. **Vérifier** — parcourir la checklist correspondante dans le fichier
   `references/*.md` choisi, puis établir le rapport au format `PASS / PASS MIT WARNUNGEN / FAIL` (structure
   ci-dessous).
7. **Cataloguer si nécessaire** — un rôle persistant nouveau va dans le registre
   approprié (`~/.claude/agents/`, le cas échéant regroupement en plugin) ; un worker
   compagnon ne nécessite pas d'entrée de registre, seulement une transmission
   initiale claire de la tâche.

## Format du rapport de vérification (pour les deux voies)

Structure reprise volontairement du plugin modèle (forme, non texte) — quatre sections,
concises :

- **Statut :** PASS | PASS AVEC AVERTISSEMENTS | FAIL
- **Points critiques :** ce qui rend le rôle inutilisable (description de déclenchement
  absente, `Tools:` trop large ou trop étroit, modèle non justifié par `model-strategy`,
  délimitation par rapport à un rôle existant non vérifiée)
- **Avertissements :** sous-optimal mais fonctionnel (p. ex. modèle principal hérité au
  lieu d'être échelonné, absence de critère de rotation pour un worker compagnon de
  longue durée)
- **Contrôles réussis + recommandations :** ce qui est conforme, et la suite

## Compétences associées

- `model-strategy` — choix/échelonnement du modèle (étape 3, seulement référencée ici).
- `swarm-operations` — modèles d'essaim pour la collaboration de plusieurs rôles.
- `choose-your-orchestrator` — choisit le modèle d'orchestration adapté.
- `orchestrator` — protocole de décomposition / délégation / réception.
- `agents-bridge` — messagerie inter-fournisseurs/présence/verrous, si le nouveau
  rôle doit communiquer au-delà de Claude Code avec Codex/Gemini/Kimi.
- `skill-explorer` — vérifie si une capacité existe déjà AVANT de construire un
  nouveau rôle (évitement des doublons).

## Journal des modifications

### 1.0.0 (2026-08-25)
- Première version. Construite suite à la décision utilisateur M5 (`T-20260825-935905816`) via
  `ellmos-skill-creator`. Formalise le modèle de worker compagnon (source principale :
  `_control-center/_TICKETS/README.md`, section « Principe directeur (économie de contexte) »), le cycle de vie
  COMA (source principale : `.MODULES/.ORCHESTRATION/coma/README.md`), et le modèle « agent chef coordonne des
  experts » observé dans les rôles existants. Renvoie délibérément vers
  `model-strategy`/`swarm-operations`/`orchestrator`/`choose-your-orchestrator`/`agents-bridge` au lieu de les
  dupliquer. Modèle `agent-sdk-dev` (claude-plugins-official) NON installé, seulement lu et
  cité structurellement (`.PLUGINS/CLAUDE.md` règle 5).
