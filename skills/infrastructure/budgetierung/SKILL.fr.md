---
name: budgetierung
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-10-03
updated: 2026-10-03
description: "Concept de compte pour l'utilisation budgétée de modèles coûteux ou rares (conseiller, relecteur, modèles spécialisés, travailleurs permanents) dans de longues exécutions d'agents. Commence par une négociation commune entre l'utilisateur et le modèle sur les modèles disponibles, les rôles et les quotas par fenêtre temporelle, tient un compte pour chaque utilisation, applique une procédure préalable en pièces de puzzle avant toute escalade et permet des ajustements en cours d'exécution. À utiliser pour « budget », « quota », « tenir un compte », « une seule fois par heure », « utiliser le relecteur avec parcimonie », « Fable/Codex/Sol/Astra/Luna/Advisor seulement de façon limitée », « /budgetierung », et chaque fois qu'une exécution d'opérateur, de recherche ou d'automatisation doit combiner plusieurs modèles aux coûts différents — même si l'utilisateur ne prononce pas le mot budget, mais fixe des limites d'utilisation pour des modèles."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: infrastructure
tags: [budget, kontingent, modellwahl, eskalation, reviewer, advisor, operator, konto]
language: fr
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: ae8346a5144eac699936053f5ca7e12be53014cde4b7826264e2f5fd1e986b0c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T12:49:14.794284+00:00"
---
# Budgétisation — négocier, tenir et ajuster les quotas de modèles

## Pourquoi

Les longues exécutions d'agents combinent aujourd'hui souvent plusieurs modèles aux prix et aux
disponibilités très différents : un agent principal qui réfléchit et décide, des travailleurs
permanents bon marché pour l'exécution, et quelques spécialistes coûteux pour les relectures, les
audits ou les percées. Sans accord préalable, deux erreurs se produisent : les modèles coûteux sont
gaspillés pour des tâches de routine, ou bien ils ne sont jamais utilisés par excès de prudence. Le
compte rend l'utilisation **visible et négociable** : ce qui est permis est fixé à l'avance, chaque
utilisation est enregistrée, et l'utilisateur peut ajuster à tout moment.

Les modèles, les prix et les quotas changent constamment, car de nouveaux modèles apparaissent, les
abonnements évoluent et les projets n'ont pas tous la même importance. C'est pourquoi cette
compétence ne contient **aucun chiffre fixe**, mais une procédure permettant de les définir
ensemble, pour chaque utilisation et chaque projet.

## Phase 1 — Négociation au départ

Avant de déléguer un travail, clarifier le budget avec l'utilisateur. Ce qu'il a déjà précisé ne doit
pas être redemandé ; il faut seulement combler les lacunes et faire confirmer brièvement le résultat
une fois.

1. **Recenser l'existant :** quels modèles et quels accès sont réellement appelables sur cet hôte ?
   Vérifier plutôt que deviner : fichiers de configuration, listes de modèles des CLI, types de
   sous-agents disponibles. Noter les noms de modèles exactement tels qu'ils sont appelés.
2. **Proposer des rôles :** chaque modèle reçoit un rôle :
   - *Penseur/Décideur* (agent principal),
   - *Travailleur permanent* (exécution, sans budget ou avec un budget large),
   - *Relecteur/Auditeur* (contrôle indépendant, idéalement d'un autre fournisseur que l'auteur),
   - *Escalade* (sous-problèmes très complexes, tentatives de percée),
   - *Conseiller/Advisor* (correction de cap de l'agent principal).
3. **Fixer les quotas :** pour chaque ressource, un budget et une fenêtre temporelle, par exemple
   « 2 requêtes par heure » ou « en permanence, sans limite ». Clarifier explicitement :
   - **Expiration ou report ?** Les unités non utilisées expirent en général ; le noter ainsi.
   - **Pots communs ou séparés ?** Deux modèles partagent-ils une même unité (« Fable *ou* Astra ») ?
   - **L'Advisor est-il compté ?** Les appels à l'Advisor sont coûteux et faciles à oublier ; s'ils ont
     un quota propre, s'ils font partie d'un pot ou s'ils sont hors budget, cela figure dans le compte.
   - **Niveau d'effort :** pour les modèles disposant de niveaux de raisonnement, le niveau fait partie
     du budget (xhigh ≠ low).
4. **Convenir de la procédure préalable** (phase 3), sauf si l'utilisateur souhaite autre chose.
5. **Ouvrir le compte** (phase 2) et indiquer à l'utilisateur son chemin.

Forme courte de la question lorsque des informations manquent : une seule question accompagnée d'une
proposition plutôt qu'une liste ouverte, par exemple « Proposition : Sonnet comme travailleur
permanent, relecture Codex 1×/heure, Advisor seulement sur demande — cela convient-il ? »

## Phase 2 — Le compte

Un fichier Markdown dans le projet, par exemple `_operator/KONTINGENT.md` ou à l'emplacement prévu par les
conventions du projet. Modèle : [references/konto-vorlage.md](references/konto-vorlage.md).

Le compte contient :
- **Bloc de règles :** les quotas négociés sous forme de tableau (Ressource | appel/nom de modèle exact
  | budget par fenêtre | expiration oui/non).
- **Journal des modifications de règles :** chaque ajustement demandé par l'utilisateur est ajouté avec
  sa date, sans écraser l'existant. Ainsi, on peut retracer sous quelle règle une écriture antérieure
  a été faite.
- **Tableau des écritures :** une ligne par utilisation d'une ressource budgetée, avec n°, heure de
  début réelle, **modèle réellement exécuté**, objectif, procédure préalable suivie, chemin du résultat
  et prochaine fenêtre disponible au plus tôt.

Important :
- **Enregistrer le modèle réel, pas celui qu'on voulait.** Sans indication explicite du modèle, les CLI
  retombent sur leur modèle par défaut. Il faut donc toujours définir le modèle explicitement et, en cas
  de doute, le justifier à partir de la configuration ou de la réponse. S'il apparaît après coup qu'un
  autre modèle a tourné, **reclasser** l'écriture et noter l'erreur.
- **Heure de début tirée d'une preuve** (fichier d'horodatage, journal), et non estimée.
- **Utilisations hors budget** (déclenchées par l'utilisateur ou expressément exemptées) : les inscrire
  tout de même, avec la mention « aucune unité enregistrée », afin que la vue d'ensemble reste complète.
- Les travailleurs permanents illimités n'ont pas besoin d'une écriture individuelle. Une ligne suffit,
  indiquant qu'ils tournent et à quoi ils servent.

## Phase 3 — Procédure préalable avant toute escalade

Les unités coûteuses sont réservées aux exceptions. Avant d'en enregistrer une :

1. **Définir la pièce manquante :** qu'est-ce qui manque exactement ? Quelles propriétés devraient
   avoir la solution, la source ou le résultat de contrôle ? Par écrit, en quelques lignes.
2. **Chercher à bas coût :** web, bases de données spécialisées, fonds du projet, avec les travailleurs
   permanents.
3. **Outils d'idées :** par exemple `/idea-mining`, puis `/skill-finder`, si une compétence existe
   pour la tâche.
4. **Seulement ensuite enregistrer**, et noter dans le compte quelles étapes ont été parcourues. Si une
   étape ne convient pas sur le fond (par exemple la recherche d'idées alors qu'il faut un *contrôle*),
   le justifier par écrit au lieu de l'exécuter pour la forme.

Un quota qui expire **n'est pas une raison** de le consommer. À l'inverse, une économie mal placée est
aussi une erreur : si une validation indépendante est nécessaire pour l'étape suivante (par exemple un
registre de revendications avec changement de fournisseur), c'est précisément le cas d'exception pour
lequel le budget existe.

## Phase 4 — Ajustements en cours d'exécution

L'utilisateur peut modifier les règles à tout moment : nouveaux modèles, plus ou moins d'unités, un
Advisor qui compte désormais. Dans ce cas :
- reporter la nouvelle règle datée dans le bloc de règles et conserver l'ancienne,
- vérifier si les écritures antérieures doivent être classées autrement selon la nouvelle règle, et le noter,
- vérifier s'il existe une tâche ouverte adaptée à la nouvelle ressource, et si oui l'utiliser. S'il n'y en
  a pas, elle peut rester inutilisée jusqu'à ce qu'un besoin apparaisse : un quota est un cadre, non une
  mission. L'utilisateur a pu surestimer le besoin, et occuper une ressource pour elle-même coûte aussi,
- confirmer à l'utilisateur en une phrase ce qui s'applique désormais.

Si le modèle lui-même propose un ajustement (par exemple parce qu'une ressource reste durablement inutilisée
ou qu'un goulot d'étranglement apparaît), il le formule comme une proposition motivée. La décision revient
à l'utilisateur.

## Phase 5 — Clôture

À la fin d'une exécution ou d'un bloc, indiquer dans le rapport à l'utilisateur une ligne sur la
consommation : quelles unités ont été utilisées, pour quoi et avec quel résultat, et ce qui a expiré
inutilisé. Le compte reste dans le projet ; une session ultérieure le lit en premier.

## Exemple

L'utilisateur dit : « Travaille en tant qu'opérateur, utilise des travailleurs Sonnet, n'utilise Fable ou
Codex qu'une fois par heure, et tiens un compte. » Plus tard : « Sol peut relire deux fois par heure, Luna
en permanence, et l'Advisor reçoit un quota supplémentaire. »

→ La phase 1 confirme brièvement les rôles, la phase 2 ouvre le compte avec la première règle. Au second
message, la phase 4 complète le bloc de règles et constate que deux audits « Codex » antérieurs, sans
indication de modèle, ont en réalité tourné sur le modèle par défaut. Les écritures sont donc reclassées.
Pour Luna, il existe justement une tâche d'exploration ouverte appropriée : elle est donc utilisée ; sans
une telle tâche, elle resterait inutilisée.

## Compétences associées

- `operator` — modèle de rôles opérateur/travailleur, dans lequel ce compte est intégré.
- `model-strategy` — quel modèle convient sur le fond ; cette compétence règle *combien* on en utilise.
- `idea-mining`, `skill-finder` — éléments constitutifs de la procédure préalable.
- `advisor-skill` — conseil sélectif ; ses appels doivent figurer dans le compte.
- `orchestrator` — lots de travail, profils (parallélisme), réception.
- `choose-your-orchestrator` — contrat de session, dans les emplacements budgétaires duquel ce compte est inscrit.

## Journal des modifications

### 1.0.0 (2026-10-03)
- Version initiale : négociation, compte, procédure préalable, ajustements en cours d'exécution, clôture.
