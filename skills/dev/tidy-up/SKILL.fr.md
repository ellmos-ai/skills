---
name: tidy-up
version: 1.1.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-08-19
updated: 2026-08-19
description: "Passage unique Tasksolver+Writer+Maintainer pour le dossier de projet dans lequel la session travaillait de toute façon (sous-dossiers inclus), pas de balayage à l'échelle du système. Résout les points de registre ouverts triviaux et autonomes, met la documentation à jour sur l'état mesuré (dans le projet ET à la racine du pipeline où se trouve le projet) et range les fichiers orphelins et temporaires selon le principe de la corbeille. Utilise ce skill pour /tidy-up, « range le projet », « nettoie ici avant qu'on continue », à la fin d'une session de travail sur un projet, ou comme tâche autonome échue au sein de /work-autonomous + /goal."
# Kompatibilitaet
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: dev
tags: [hygiene, maintenance, cleanup, documentation, tasksolver, writer, maintainer, autonomy, goal, work-autonomous, ticket-master]
language: fr
status: active
visibility: public

# Abhaengigkeiten
dependencies:
  tools: []
  services: []
  protocols: [work-autonomous, bilingual-doc-sync]
  python: []

# Provenance (Herkunfts-Tracking)
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 27510ce60a4dd2defe9ee4686aeae6378ce8aea2f2376b98163d1d1340960233
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T22:17:49.701000+00:00"
---
<img src="banner.png" width="100%" alt="tidy-up banner">

# Tidy Up — Passage Tasksolver+Writer+Maintainer pour le dossier de projet actif

## Objet

À la fin d'une session de travail sur un projet, il reste généralement des petites choses en suspens : un point de TODO terminé qui n'a jamais été coché ; un README qui affiche l'ancien état au lieu de l'état mesuré ; quelques fichiers de test dont plus personne n'a besoin. `tidy-up` est un **passage unique et auto-limité** qui règle exactement cela pour **un** dossier de projet, celui dans lequel la session travaillait de toute façon. Pas de boucle permanente, pas de balayage à l'échelle du système.

Le passage comprend trois rôles, que le modèle endosse lui-même l'un après l'autre :

1. **TASKSOLVER** : résoudre ou classer correctement les points ouverts, triviaux et autonomes, du registre du projet.
2. **WRITER** : mettre la documentation à jour selon l'état mesuré, dans le projet ET à la racine du pipeline où se trouve le projet.
3. **MAINTAINER** : hygiène : rassembler les fichiers orphelins et temporaires (principe de la corbeille), entretenir le registre et le catalogue, déposer les restes ouverts au lieu de simplement les mentionner dans le chat.

**Vérifié avant la création de ce skill :** il n'existe dans cette bibliothèque (état au 2026-08-19) **aucun** skill autonome ni aucun rôle nommé `tasksolver`/`writer`/`maintainer`, ni comme nom de skill ni comme rôle documenté dans un autre skill (recherche plein texte sur `skills/**/SKILL.md`, aucun résultat hormis un nom sans rapport, `privat-mail-writer`). Les trois rôles sont donc définis directement ci-dessous sous forme de sections, et non orchestrés depuis l'extérieur. Si des skills autonomes `tasksolver`/`writer`/`maintainer` devaient voir le jour plus tard, `tidy-up` les reprendrait par renvoi au lieu de continuer à dupliquer la logique (vérification obligatoire à chaque évolution de ce skill).

## Périmètre : que compte-t-on comme « le dossier de projet actif » ?

- Le dossier de projet dans lequel la session a travaillé dans ce contexte, **sous-dossiers inclus**. Pas de saut vers les projets voisins, pas de balayage d'un pipeline entier ni de `.TOPICS/` dans son ensemble.
- **Une seule exception ciblée** : la mise à jour de la documentation ou du registre peut en plus toucher la **racine du pipeline** où se trouve le projet (par exemple une ligne d'état pour ce projet dans un tableau de vue d'ensemble valable pour tout le pipeline), mais uniquement la ligne ou la section qui concerne ce projet, sans réordonner toute la racine du pipeline.
- En cas de doute sur ce qu'est « le dossier de projet actif » (par exemple si la session a travaillé dans plusieurs dossiers), prendre la racine commune la plus proche du projet (là où se trouvent README/TODO/CLAUDE.md du projet). En cas de doute, mieux vaut un périmètre plus étroit qu'un périmètre trop large.

## Rôle 1 — TASKSOLVER

Objectif : mettre le registre du projet (`TODO.md`/`AUFGABEN.txt`/convention locale équivalente) dans un état correct et à jour.

1. Localiser le registre du projet (la convention locale prime sur la création d'un nouveau fichier ; voir la règle « Les tâches restantes doivent être déposées, non simplement mentionnées » dans le règlement global).
2. Évaluer chaque point ouvert séparément :
   - **Déjà terminé** (par exemple grâce à la session qui vient de se clore) → le marquer comme terminé ou le déplacer vers `DONE.md`, ou selon la convention locale des points terminés.
   - **Trivial et résoluble en autonomie** (aucune décision, validation, donnée, matériel ou session de l'utilisateur n'est nécessaire, voir le tableau de délimitation dans `work-autonomous`) → le résoudre maintenant, puis le classer comme terminé.
   - **Non trivial ou non autonome** → NE PAS y toucher, mais le laisser correctement classé (ne pas le laisser en suspens sans commentaire lorsqu'un meilleur emplacement existe, par exemple un point qui aurait depuis longtemps mérité une catégorie de ticket `USER/*`).
3. N'inventer aucune nouvelle tâche : `tidy-up` résout les restes existants, il ne crée pas de nouvel agenda.

## Rôle 2 — WRITER

Objectif : la documentation présente l'état **mesuré**, et non l'état dont on se souvient ou que l'on espère.

1. Dans le projet : vérifier README/CHANGELOG/lignes d'état par rapport à la situation réelle du code et des dossiers (par exemple : les fichiers mentionnés existent-ils encore, le numéro de version indiqué est-il exact, la mention « en cours » n'est-elle pas depuis longtemps dépassée).
2. Dans la racine du pipeline : s'il existe à cet endroit un registre ou un tableau d'état qui répertorie ce projet (par exemple `.TOPICS/<Pipeline>/ROADMAP.md`, `STATUS.md`, un tableau de projets dans le README du pipeline), mettre à jour la ligne ou la section pour CE projet précis.
3. **Ne jamais remplacer les contenus soignés, seulement mesurer et mettre à jour.** Les tableaux, changelogs ou sections formulés avec soin conservent leur forme et leur ton ; seuls les faits (chiffres, statut, noms de fichiers, versions) sont corrigés. En cas de doute sur le caractère soigné d'une section, ajouter plutôt une remarque que réécrire une formulation existante.
4. Pas de réécriture complète lorsqu'une mise à jour suffit.
5. **Rattrapage des traductions** (complément du 2026-08-19, demande en direct de l'utilisateur) : si une version linguistique qui, selon la **politique P-006** (`.SYNC/_policies/library/P-006_sprachstufen.md`), est obligatoire pour son niveau manque au projet, ou si une version existante est manifestement obsolète, l'étape WRITER procède au rattrapage. P-006 en bref : le **jeu de base (DE+EN) est obligatoire** pour tout dépôt publié ou objet catalogué (dépôt : `README.md` EN + `README_de.md` ; skill : `SKILL.md` DE + `SKILL.en.md`) ; le jeu complet ou mondial (ES/ZH/JA/RU, ou +FR/HI/AR/BN/PT) constitue l'objectif, mais il est rattrapé **progressivement**, et non dans une campagne unique menée par `tidy-up`.
   **Outil : le skill existant `bilingual-doc-sync` est orchestré (appelé), sa logique n'est PAS dupliquée** : il couvre déjà exactement « rattraper une version manquante » + la vérification de parité des sections + la correction des divergences. `tidy-up` ne lui fournit que le déclencheur (quel objet, quelle langue obligatoire manquante selon P-006) pour le dossier de projet actif ; la qualité de la traduction, la parité de structure et la règle de la langue de référence restent de la responsabilité de `bilingual-doc-sync`. **Limites identiques à celles de P-006** : traduire uniquement jusqu'à l'état mesuré, ne rien inventer, respecter les diacritiques et les umlauts réels, respecter le délai de refroidissement du dépôt (moins de 24 h depuis le dernier commit) ainsi que les verrous actifs ; dans ce cas, laisser ce point non traduit et le déposer comme point ouvert (rôle 3) au lieu de forcer.

## Rôle 3 — MAINTAINER

Objectif : l'hygiène, sans que rien ne soit perdu.

1. **Rassembler les fichiers orphelins et temporaires** (restes de scripts, `*.tmp`, copies en double, sorties de débogage oubliées) : principe de la corbeille, les déplacer vers un dossier local `_archive/` (le créer et l'inscrire dans `.gitignore` s'il n'existe pas encore), **ne jamais les supprimer directement**. Pour les trouvailles dont l'origine ou la finalité est inconnue : déterminer activement leur finalité (lire le fichier), ne pas les ranger sans les avoir lus ; voir la convention « Recertifier les modifications externes ».
2. **Entretien du registre et du catalogue :** si le projet fait partie d'un catalogue ou d'un registre plus large (registre de skills, manifeste de module, vue d'ensemble du pipeline), vérifier que l'entrée correspondant à ce projet est toujours exacte ; ne pas reconstruire tout le registre, seulement cette seule entrée.
3. **Déposer les restes ouverts au lieu de les mentionner dans le chat :** ce qui subsiste à la fin de ce passage (points non résolvables en autonomie, défauts découverts mais non corrigés, éléments volontairement reportés) est déposé selon la règle « Les tâches restantes doivent être déposées, non simplement mentionnées » : d'abord localement, à l'endroit où ils ont été trouvés (convention TODO.md/AUFGABEN.txt du projet), sinon de manière centralisée (`ticket-master`/`TASKPLAN`), chacun avec son contexte (ce qui est concerné, pourquoi c'est resté ouvert, prochaine étape).
4. **Respecter les verrous :** avant chaque modification, vérifier qu'aucun `LOCK.txt`/`LOCK.<scope>.txt`/`LOCK.user.*` actif ne se trouve dans le dossier de projet. Un `LOCK.user.*` arrête entièrement `tidy-up` pour la zone concernée : pas de contournement, pas de tidy-up partiel sur la zone verrouillée.
5. **Commit et push uniquement selon la convention de dépôt propre à chaque projet** : lorsque les espaces de planification et de développement sont séparés, effectuer les modifications dans le clone local autorisé du projet, et non dans une copie de planification ou de projection.
   Les modifications propres sont traitées selon la convention globale « committer et pousser soi-même immédiatement », lorsque le projet le prévoit.

## Auto-limitation

`tidy-up` est **un passage, non une boucle**. Après le rôle 3, le skill se termine par un bref récapitulatif (ce qui a été résolu, mis à jour, rangé et déposé comme ouvert) puis revient à la session appelante. Un nouvel appel de `/tidy-up` dans le même projet peu après est autorisé, mais n'a pas automatiquement de sens : voir le critère d'échéance ci-dessous.

## Relation avec work-autonomous

Les passages `tidy-up` **comptent comme tâche exécutable en autonomie au sens de `work-autonomous` niveau 1** (travail normal et visible, aucune raison de passer au contrôle d'épuisement coûteux du niveau 2 tant qu'un passage `tidy-up` échu est en attente). Concrètement : si `/work-autonomous` est utilisé avec `/tidy-up` au sein d'un `/goal`, le goal n'est considéré comme achevé que lorsque les points `tidy-up` échus sont également traités, dans la mesure où ils peuvent être exécutés en autonomie (voir le tableau de délimitation dans `work-autonomous` ; un point `tidy-up` qui requiert une décision de l'utilisateur ne compte pas davantage comme autonome que toute autre tâche liée à `USER/*`).

**Critère d'échéance** (quand un passage `tidy-up` est-il « échu » ?) :

1. La session a déjà travaillé sur un dossier de projet concret dans ce contexte de session (et non : seulement de la recherche ou de la lecture sans modification ; dans ce cas, il n'y a rien à ranger).
2. Depuis le dernier passage `tidy-up` journalisé pour CE projet précis, le délai de refroidissement est écoulé (par défaut : 1 fois par clôture de session sur ce projet ; pas de passage multiple **au sein** d'une même session sans nouvelle modification depuis le dernier passage).
3. Aucun `LOCK.user.*` actif ne bloque le dossier de projet (voir rôle 3, point 4).

Journalisation du dernier passage (analogue au modèle de garde de `work-autonomous`, mais volontairement plus simple : `tidy-up` n'a pas besoin d'une chaîne à quatre étapes, seulement d'un horodatage par projet) :

```bash
usmc --agent <agent> note "tidy-up: project=<projekt-pfad-oder-slug> at=<ISO-Zeit> result=<done|nothing-to-do>" \
  --type context --priority 2 --tags "tidy-up-log,<projekt-slug>"
```

Avant un nouveau passage, relire les entrées du même tag (`usmc --agent <agent> working --limit 20` filtré par `tidy-up-log,<projekt-slug>`) pour vérifier le critère 2.

Une construction `/goal` (si elle existe ou est créée : `work-autonomous` lui-même n'appelle aucun `/goal`, voir la section correspondante « Volontairement sans `/goal` intégré ») lit ce critère d'échéance de la même façon qu'elle lit son propre signal d'arrêt `work-autonomous` : si un passage `tidy-up` est échu ET exécutable en autonomie, le goal n'est pas encore terminé, indépendamment du fait que la chaîne en quatre étapes propre à `work-autonomous` signale déjà « épuisé ».

La contrepartie minimale et adaptée, dans le skill `work-autonomous` lui-même (niveau 1, nouvelle source « passages tidy-up échus du projet actif »), fait partie de cette extension : voir l'entrée de changelog correspondante.

## Skills associés

- **`work-autonomous`** : voir ci-dessus ; `tidy-up` est l'une des sources que traite le niveau 1 de `work-autonomous`, il ne remplace pas la vérification d'épuisement de celui-ci.
- **`bilingual-doc-sync`** : orchestré par le rôle 2 (WRITER) pour le rattrapage des traductions (voir ci-dessus), non dupliqué. `tidy-up` décide seulement CE qui manque selon P-006, `bilingual-doc-sync` décide COMMENT traduire et synchroniser.
- **`bugsweep`** : recherche systématique de bugs avec escalade par doublement. Objectif différent (trouver des erreurs, et non entretenir le registre, la documentation ou l'hygiène) ; en cas de chevauchement (une trouvaille de balayage de bugs aboutit dans le registre), `tidy-up` ne prend en charge que l'entretien du registre, non la recherche de bugs elle-même.
- **`dev-cycle`** : cadre en 8 phases pour le développement de nouvelles fonctionnalités. `tidy-up` n'est pas un cadre de développement, mais un passage de clôture et d'hygiène après un travail déjà accompli.
- **`folder-flattening`** : restructure les hiérarchies de dossiers imbriquées. `tidy-up` range les fichiers à l'intérieur de la structure existante, sans modifier la structure elle-même.

## Exemples

```
User: "/tidy-up"
(Session hat gerade am autorisierten lokalen Checkout von `beispiel-projekt` gearbeitet)

→ TASKSOLVER: TODO.md gelesen — 2 Punkte bereits durch die Sitzung erledigt (nach DONE.md
  verschoben), 1 trivialer Punkt ("README-Tippfehler in Zeile 12") autonom geloest, 1 Punkt
  braucht Nutzerentscheidung (unveraendert stehen gelassen).
→ WRITER: README-Versionsangabe war 1.2.0, tatsaechlich 1.3.0 (package.json) — korrigiert.
  Pipeline-Root-Statustabelle: Zeile fuer "beispiel-projekt" von "in Arbeit" auf "aktiv" gesetzt.
→ MAINTAINER: 3 Debug-Skripte im Projektroot gefunden, nach _archive/ verschoben (Zweck geprueft:
  einmalige Testskripte, nicht mehr referenziert). Skill-Registry-Eintrag geprueft: stimmt.
  1 offener Punkt (Nutzerentscheidung) in AUFGABEN.txt belassen, dort bereits korrekt einsortiert.
→ USMC-Log geschrieben: tidy-up: project=beispiel-projekt at=2026-08-19T14:30 result=done
→ Zusammenfassung an Nutzer: 3 geloest, 2 Doku-Stellen aktualisiert, 3 Dateien archiviert, 1 Punkt
  offen (Nutzerentscheidung noetig).
```

```
Kombiniert mit /goal + /work-autonomous:

/goal "Projekt X fertigstellen" mit /work-autonomous + /tidy-up als Bedingungen
→ work-autonomous Ebene 1 findet: ACTIONABLE-Ticket erledigt, dann kein weiteres Ticket mehr,
  ABER tidy-up-Faelligkeitskriterium erfuellt (Session hat an Projekt X gearbeitet, kein
  protokollierter Lauf seit Sitzungsbeginn, kein LOCK.user aktiv) → tidy-up-Durchlauf ausgefuehrt.
→ Erst NACHDEM tidy-up "done" meldet UND work-autonomous Ebene 2 "exhausted" meldet, gilt das
  Goal als abgeschlossen.
```


## Journal des modifications

### 1.1.0 (2026-08-19)
- Complément issu d'un ajout en direct au ticket T-20260819-461890468 (utilisateur, littéralement : « bis zu einer uebersetzung nachzuziehen die noch nicht existiert soll auch zum skill gehoeren », soit en français : jusqu'à rattraper une traduction qui n'existe pas encore doit aussi appartenir au skill) : le rôle 2 (WRITER) reçoit un cinquième point, le rattrapage des traductions selon la **politique P-006** (niveaux linguistiques : jeu de base DE+EN obligatoire, jeu complet/mondial progressivement). L'outil est le skill existant `bilingual-doc-sync` : il est orchestré, non dupliqué. Dépendance ajoutée dans le frontmatter ainsi qu'une entrée « Skills associés ».

### 1.0.0 (2026-08-19)
- Version initiale issue du ticket T-20260819-461890468. Trois rôles (Tasksolver/Writer/Maintainer) définis sous forme de sections dans le skill, après qu'une recherche plein texte dans la bibliothèque a confirmé qu'il n'existe aucun skill autonome `tasksolver`/`writer`/`maintainer` (sinon il aurait été orchestré au lieu d'être dupliqué). Périmètre limité au dossier de projet actif + à la ligne d'état de la racine du pipeline. Intégration au goal : les passages `tidy-up` comptent comme source de niveau 1 de `work-autonomous`, avec un journal USMC d'échéance propre et allégé (pas de garde à quatre étapes comme dans `work-autonomous` lui-même, car `tidy-up` est trop simple pour cela). Contrepartie minimale et adaptée ajoutée dans `work-autonomous` 1.3.0 (voir son journal des modifications).
