---
name: reissverschluss-merge
version: 1.0.0
type: skill
language: fr
visibility: public
author: Claude (extrahiert aus einer Live-Merge-Session, Multi-Repo-PR-Abarbeitung)
created: 2026-08-07
provenance:
  origin: live-session-extraction
  extracted: 2026-08-07
  method: skill-extractor
updated: 2026-08-07
description: "Procédé de fusion en fermeture éclair (en anglais : zipper merge) pour les fusions très conflictuelles : lorsque deux branches divergentes, ou une PR et sa branche cible, contiennent CHACUNE des modifications précieuses et apparemment incompatibles, on ne choisit pas un côté de façon générale. On compare section par section, on retient la version démontrablement meilleure selon un tableau de décision (Prendre/Pourquoi), on valide section par section (commit) et on ne pousse qu'à la fin. Dernier niveau d'escalade : reconstruire plutôt que fusionner — ne reprendre que l'intention/la fonctionnalité de la branche et la réimplémenter sur l'état actuel. Utile lors de : « conflit de fusion », « branches divergentes », « main vs. master », « PR conflictuelle », « zipper merge », « fermeture éclair », « les deux côtés ont raison », « la PR est trop ancienne pour être fusionnée »."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
aliases:
  - zipper-merge
  - zipper-verfahren
  - reissverschluss
tags: [git, merge, konflikt, pull-request, branch, rebase, dev-workflow]
translated_from_sha256: 6a31c500a8da2c6d19255bf7601125cf9f2fed39f9387fa0c8e45b11260468ee
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:03.139962+00:00"
---
<img src="banner.png" width="100%" alt="reissverschluss-merge banner">

# Fusion en fermeture éclair (zipper merge)

## Quand utiliser ce procédé

Deux branches du même dépôt sont **fortement divergentes** et **portent toutes deux de la valeur** —
typiquement : `main` contre `master` après une maintenance parallèle, une ancienne PR face à une branche cible
qui a continué d'évoluer, deux états d'agents/d'équipes avec chacun leurs propres correctifs.
Une fusion normale écraserait alors un côté (« ours » / « theirs ») ou produirait
un enchevêtrement de conflits impossible à démêler. Le procédé en fermeture éclair résout cela
en faisant **s'engrener les dents des deux côtés section par section** :
pour chaque section, la version démontrablement meilleure l'emporte — ou un mélange justifié.

**Inutile** pour les conflits triviaux (une branche manifestement obsolète,
peu de blocs modifiés) : une fusion normale suffit alors. Le procédé devient pertinent
dès qu'il faut pondérer sérieusement plusieurs fichiers ou sections.

## Phase 0 — État des lieux et choix de la base

1. **Examiner intégralement les deux côtés** (pas seulement les marqueurs de conflit) :
   `git log --oneline A..B` et `B..A`, `git diff A...B --stat`, puis lire les fichiers divergents des deux versions.
2. **Choisir la base selon la réalité, non selon la date.** La base est la branche
   qui correspond à la **réalité publiée** : état du registre (npm/PyPI/…),
   version déployée, CI verte, tags de publication. Une branche plus récente
   mais sans correspondance avec le monde extérieur constitue une matière première, pas une base.
3. **Vérifier la cohérence interne des deux côtés** — il arrive que LES DEUX soient
   incohérentes (par ex. la base porte la version X sans entrée de changelog correspondante,
   tandis que l'autre côté tient le changelog mais accuse un retard sur la version). De tels constats
   doivent figurer dans le tableau, et non être passés sous silence.

## Phase 1 — Tableau de décision (le cœur du procédé)

Pour chaque section divergente (fichier, bloc, champ — aussi fine que nécessaire), une
ligne :

| Section | Prendre | Pourquoi |
|---|---|---|
| `package.json` → version | Base | correspond au registre |
| Bloc `overrides` | Autre côté | contient des mises à jour de sécurité absentes de la base |
| ↳ dans celui-ci l'entrée `X` | **mélanger** | reprendre l'entrée de l'autre côté, mais la ramener à la version plus récente de la base |
| Changelog `[Unreleased]` | **mélanger** | fusionner les deux blocs, supprimer les doublons |

Règles :

- **Des faits, pas des suppositions.** Chaque cellule « Pourquoi » s'appuie sur
  quelque chose de vérifiable : interrogation du registre, exécution de tests, base de
  vulnérabilités (advisories), installation d'essai isolée du fichier litigieux. Qui devine
  fusionne des suppositions.
- **« Mélanger » est un verdict légitime** — la fermeture éclair peut
  faire engrener les deux côtés à l'intérieur d'une même section.
- **Rejeter est un verdict légitime** — ce qui ne tient sur aucun côté
  (badge mort, fonctionnalité à moitié introduite) est supprimé. L'état intermédiaire
  (« fonctionnalité à moitié présente ») est la pire option : tout entier ou rien.
- Le tableau final est le **document contractuel** de la mise en œuvre — en cas de changement
  de session ou de passation, il suffit pour poursuivre mécaniquement.

## Phase 2 — Mise en œuvre : commit par section, push à la fin

1. Lancer sur la base une véritable fusion : `git merge <gegenseite>`
   (volontairement SANS `-X ours/theirs` — les conflits doivent rester visibles).
2. Résoudre les conflits **section par section**, strictement selon le tableau.
3. **Un commit par section logique** (ou, pour un unique commit de fusion :
   une étape de résolution documentée par section dans le message de commit).
   Chaque message de commit nomme le verdict du tableau (« overrides : autre côté +
   vitest rehaussé à l'état de la base »). Ainsi, chaque dent de la fermeture reste
   traçable et réversible individuellement.
4. **Tests après la mise en œuvre** (suite, build, installabilité) — d'abord au vert,
   puis on continue.
5. **Pousser seulement à la fin** — l'historique local peut être remanié pendant le
   procédé, le distant ne voit que le résultat final.
6. **Clore la divergence sans supprimer :** amener la branche perdante au résultat par
   avance rapide (fast-forward) (`git checkout <gegenseite> &&
   git merge --ff-only <basis>`). Les deux noms pointent ensuite vers le même
   état ; aucun historique n'est perdu.

## Voie d'escalade — reconstruire plutôt que fusionner (dernier niveau)

Lorsque la fermeture éclair ne fonctionne plus, on **ne fusionne pas, on reconstruit** :
on extrait l'**intention/la fonctionnalité** de la branche ou de la PR
(CE qu'elle voulait atteindre — pas COMMENT) et on l'implémente à neuf sur l'état
actuel. L'ancienne branche ou PR est fermée avec renvoi vers la reconstruction.

Déclencheurs de l'escalade (un seul suffit) :

- Le côté adverse est **démontrablement défectueux** (par ex. jamais installable,
  build qui échoue) — il n'y a alors jamais eu d'état fonctionnel à fusionner.
- Masse de conflits ≫ substance : la modification est petite, mais diluée sur des centaines
  de lignes déplacées (vagues de renommage/formatage intercalées).
- L'historique est empoisonné (par ex. le même numéro de version attribué à des contenus
  **différents** sur les deux côtés — une fusion hériterait du mensonge).
- La PR est si ancienne que son contexte (API, structure) n'existe plus.

Démarche : formuler l'intention en 2 à 5 phrases (à partir de la description de PR, des commits,
de la substance du diff) → réimplémenter sur l'état actuel → tests → documenter dans l'ancienne
PR/branche CE qui a été repris et CE qui a été volontairement écarté, puis fermer. Mentionner
l'auteur de l'idée dans le texte du commit/de la PR.

## Pièges (issus de la session d'origine, payés cher)

- **Bloc de changelog `[Unreleased]` en double** : c'est le point chaud le plus fréquent
  des branches maintenues en parallèle — toujours fusionner, ne jamais en écarter un en silence.
- **Les deux côtés attribuent le même numéro de version à des contenus différents :**
  avant la fusion, déterminer quel numéro connaît le registre ; l'autre côté
  reçoit une correction dans le changelog fusionné.
- **Une fusion est une occasion d'audit :** en lisant section par section, on remarque
  des choses qu'aucune des branches n'avait vues (advisories ouverts, liens morts,
  épinglages incohérents). Retenir et traiter ces constats, mais dans des commits distincts — ne pas
  les mêler aux décisions de fermeture éclair.
- **Reprendre « parce que c'est plus récent » :** la date n'est pas un argument. Chaque reprise
  exige une raison vérifiable.
- **Réflexe du push forcé :** le procédé se passe de push forcé (fusion +
  avance rapide). Si un push forcé semble nécessaire, le choix de la base est généralement erroné.

## Signaux d'alerte

| Pensée | Réalité |
|---|---|
| « Je prends simplement le côté le plus récent » | Date ≠ qualité. Construire le tableau. |
| « Je règle tous les conflits d'un coup » | Un commit global rend chaque décision individuelle irrévocable. |
| « Je pousse déjà entre-temps » | Des fermetures éclair à moitié faites sur le distant déroutent tout lecteur. Pousser seulement à la fin. |
| « Fusionner marche toujours d'une manière ou d'une autre » | Avec un côté défectueux ou un historique empoisonné, reconstruire est plus honnête et plus rapide. |
| « Le tableau est excessif » | Sans tableau, après le troisième fichier on oublie pourquoi la section 1 a été tranchée ainsi. |

## Skills associés

- `bugfix-protocol` — si la fusion révèle un défaut réel, poursuivre là-bas.
- `skill-extractor` — origine de ce skill (synthèse d'une session de fusion en direct).
- `human-loop-audit` — ne partage que l'image de la fermeture éclair, mais n'a rien à voir avec les fusions Git
  (procédé interactif de test d'applications/d'interfaces graphiques avec l'utilisateur).

## Journal des modifications

### 1.0.0 (2026-08-07)
- Version initiale. Extraite d'une session de fusion en direct du 2026-08-06
  (fusion main/master de plusieurs dépôts avec tableau de décision, découverte d'un
  côté adverse jamais installable, clôture par avance rapide ; cas d'escalade
  « reprendre l'intention, reconstruire »).
