---
name: rotation-check
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-07-03
description: "Gabarit standard pour les contrôles rotatifs de pipeline : à chaque exécution, choisir exactement une cible dans un ensemble (projets, dossiers, dépôts) — de préférence celle qui n'a pas été contrôlée depuis le plus longtemps —, effectuer le contrôle, et consigner le résultat dans un registre de contrôles et un journal d'historique. Utilisez cette compétence lorsqu'un contrôle récurrent doit être réparti sur de nombreux projets (« vérifier régulièrement tous les X pour Y »), lorsqu'une automatisation doit éviter les doubles contrôles, lorsqu'une structure de registre de contrôles / CHECKS-LOG est créée ou utilisée, ou lorsqu'un cycle périodique de qualité (contrôle des sources, contrôle de style, contrôle de santé, audit) doit être réparti équitablement sur une pipeline."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [automation, check, rotation, registry, pipeline, log, audit, wartung]
language: fr
status: active
visibility: public

dependencies:
  tools: []
  services: []
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
translated_from_sha256: b723f4d120407b938e8a8fdc10c5a6a7d6d4a8fe1fed2cf79b836daf0b729244
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.471192+00:00"
---
<img src="banner.png" width="100%" alt="rotation-check banner">
# Rotation-Check — une cible par exécution, couverture équitable, mémoire

## Objectif

Qui veut contrôler périodiquement une pipeline comportant de nombreux projets (sources, style, santé,
sécurité, traductions, …) se heurte à un problème de répartition : contrôler tous les projets à chaque
exécution coûte trop cher ; sans mémoire, chaque exécution contrôle au hasard les mêmes éléments. Le
motif de rotation résout les deux : **exactement une cible par exécution, sélection selon « non contrôlée
depuis le plus longtemps », registre comme mémoire.** Ainsi, même une cadence peu fréquente
(quotidienne/hebdomadaire) couvre toute la pipeline en quelques semaines — de façon vérifiable et sans
travail en double.

Éprouvé comme colonne vertébrale d'un parc croissant d'automatisations productives réparties sur
plusieurs pipelines de projets.

## Éléments constitutifs

### 1. Deux fichiers par pipeline (à créer une seule fois)

| Fichier | Contenu | Caractère |
| --- | --- | --- |
| `CHECKED-REGISTRY.md` | une ligne compacte par contrôle : cible, date, type de contrôle, résultat, étape suivante | Vue d'état — lue AVANT chaque sélection de cible |
| `CHECKS-LOG.txt` | brève entrée d'historique par exécution avec détails/preuves | Journal — ajout uniquement |

Les deux se trouvent à la racine de la pipeline (et non dans un projet individuel), afin qu'une exécution
puisse les récupérer en une seule lecture. Format de ligne du registre :

```text
| <ziel> | <YYYY-MM-DD> | <checktyp> | <ok|befund|übersprungen> | <nächster schritt> |
```

### 2. Règle de sélection

1. Lire le registre et le journal (obligatoire, AVANT la sélection — sinon double contrôle).
2. Candidats : les cibles jamais contrôlées pour CE type de contrôle, ou celles qui ne l'ont pas été depuis le plus longtemps.
3. Éviter une cible si elle a été traitée récemment par un contrôle **étroitement apparenté**
   (par ex. un contrôle des citations juste après un contrôle des sources n'apporte rien) ou si elle est
   actuellement verrouillée/en cours de traitement (respecter les verrous).
   **Délai de carence entre contrôles frères :** lorsque plusieurs contrôles apparentés portent sur le même
   ensemble de cibles (par ex. développement, recherche de bugs et revue d'une même pipeline), convenir
   d'un délai de carence (valeur d'expérience : ~24 h) pendant lequel une cible traitée par un contrôle frère
   n'est pas de nouveau sélectionnée — cela évite les collisions et les modifications parallèles contradictoires.
4. Ne traiter une cible hors de l'ordre que pour une raison valable (par ex. remaniement majeur depuis le
   dernier contrôle) — indiquer cette raison dans le journal.

### 3. Effectuer le contrôle — avec sortie en lecture seule

Appliquer le contrôle proprement dit (librement définissable : contrôle des sources, contrôle de style,
audit de sécurité, …) à la SEULE cible choisie. Deux issues valables :

- **Constat :** corriger ce qui relève du périmètre ; consigner dans le fichier TODO/AUFGABEN local au projet
  tout ce qui est plus important, sous forme de tâche de suivi (le contrôle n'a pas à tout résoudre lui-même).
- **Rien à faire :** le documenter brièvement et terminer. Une exécution sans résultat est un résultat, non
  un échec — ne jamais élargir le périmètre pour « avoir trouvé quelque chose ».

### 4. Documenter

- Compléter la ligne de registre (de façon compacte), écrire l'entrée de journal (détails/preuves).
- **Hygiène du journal :** lorsque le registre/le journal deviennent difficiles à lire (valeur d'expérience :
  plusieurs centaines de lignes), déplacer l'état ancien vers `_archiv/`, créer un fichier neuf et
  renvoyer dans son en-tête à son prédécesseur (chemin + date).
- **Dérive de chemin :** si un chemin attendu mène nulle part (cible déplacée/renommée), NE PAS le recréer —
  le corriger via le fichier d'état/le registre faisant autorité de la pipeline, et consigner le chemin
  erroné dans un journal des échecs.

### 5. Cadence

Coupler la fréquence au taux de changement de ce qui est contrôlé : les contrôles rotatifs sur des ensembles
stables fonctionnent bien en hebdomadaire (une cible par exécution ≈ la pipeline entière par trimestre pour
environ 12 cibles) ; les contrôles à évolution rapide (par ex. sur un travail actif) quotidiennement.
Retour d'expérience : des contrôles initialement horaires ont presque tous été ramenés à une cadence
quotidienne/hebdomadaire — la couverture a été conservée, les coûts ont baissé.

## Modèle de prompt (pour planificateur/automatisation)

```text
VORBEREITUNG: Lies <PIPELINE_ROOT>/<POLICY-DOKUMENTE> sowie <REGISTRY> und <LOG>.

AUFGABE: Wähle genau ein Ziel aus <ZIELMENGE>. Bevorzuge Ziele, die für den Check
"<CHECKTYP>" noch nie oder am längsten nicht geprüft wurden. Wurde ein Ziel kürzlich
von diesem oder einem eng verwandten Check geprüft oder ist es gesperrt: ausweichen
oder read-only mit Logeintrag enden.

CHECK: <konkrete Prüf-/Pflegeaufgabe und was bei Befund zu tun ist; Folgearbeiten in
die projektlokale TODO-Datei>.

Wenn keine Arbeit anfällt: kurz dokumentieren, Lauf beenden.

DOKUMENTATION: Registry-Zeile in <REGISTRY> (Ziel, Datum, Checktyp, Ergebnis, nächster
Schritt) + Verlaufseintrag in <LOG>. Bei Überlänge: alten Stand nach _archiv/ und
frische Datei mit Verweis.

ABSCHLUSS: Kurzbericht (Ziel | getan | Ergebnis | Folgeaufgaben).
```

## Signaux d'alerte

| Pensée | Réalité |
| --- | --- |
| « Je choisis simplement un projet intéressant » | La sélection passe uniquement par le registre — sinon biais vers les projets favoris et angles morts. |
| « Je lirai le registre après le contrôle » | Avant. Il est le critère de sélection, pas seulement le journal. |
| « Plusieurs cibles par exécution, c'est plus efficace » | Une seule cible garde les exécutions courtes, idempotentes et interruptibles ; le volume vient de la rotation. |
| « L'exécution sans résultat était inutile » | Une exécution sans résultat documentée met à jour la mémoire — c'est la moitié de la valeur du système. |

## Compétences apparentées

- `workflow-extract` — construit des automatisations à partir de sessions/d'automatisations externes ; utilise ce
  gabarit comme élément standard.
- `pipeline-optimizer` — pour la refonte structurelle d'une pipeline (le Rotation-Check assure la maintenance,
  l'Optimizer rénove).

## Journal des modifications

### 1.1.0 (2026-07-03)
- Délai de carence entre contrôles frères ajouté comme règle de sélection (anti-collision entre contrôles
  apparentés portant sur le même ensemble de cibles ; constat issu de la classification complète du parc
  d'automatisations).

### 1.0.0 (2026-07-03)
- Version initiale. Abstraite du parc d'automatisations Codex (motif de rotation dans
  ~40 automatisations sur 77 : contrôles recherche/logiciels/Roblox avec CHECKED-REGISTRY/CHECKS-LOG).
