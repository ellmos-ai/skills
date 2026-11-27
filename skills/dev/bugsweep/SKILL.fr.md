---
name: bugsweep
version: 1.1.1
type: protocol
author: Lukas Geiger
created: 2026-06-01
updated: 2026-11-22
description: "Utilisez cette compétence pour /bugsweep ou chaque fois que l'utilisateur demande un passage systématique de détection et correction de bugs. Effectue un balayage systématique avec un objectif proportionnel à la base de code, une escalade par doublement, un suivi des zones inspectées et une vérification finale."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [bugs, debugging, sweep, quality-assurance, workflow, convergence]
language: fr
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': ['bugfix-protocol'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/bugsweep/', 'origin_version': '1.0.0', 'last_sync_from_origin': '2026-06-13', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="bugsweep banner">

> **Français** — Version française officielle de la compétence `bugsweep`.

# /bugsweep — Flux de travail systématique de chasse aux bugs

Recherche itérative de bugs avec critère d'arrêt convergent. S'adapte à la taille de la base de code, escalade en cas de soupçon de recherche superficielle et évite les répétitions grâce au suivi des zones.

## 1. Calculer le taux de base

```
LOC = lignes de code source productives (src/, lib/ — sans tests, configs, docs, fichiers générés)
x = max(1, ceil(LOC / 1500))
Taux_de_base = x * 3
```

| LOC | x | Taux de base |
|-----|---|--------------|
| ~1500 | 1 | 3 |
| ~3000 | 2 | 6 |
| ~4500 | 3 | 9 |
| ~10000 | 7 | 21 |

Informer l'utilisateur : « Base de code : {LOC} LOC → Taux de base = {Taux_de_base} passes propres. »

## 2. Boucle de recherche

```
compteur = 0
objectif = Taux_de_base
bug_deja_trouve = False
verifies = []  # (nom_zone, type: code|tache)

LOOP:
  zone = choisir_nouvelle_zone()  # Voir les règles de zone
  verifies.append(zone)
  
  Effectuer une recherche approfondie de bugs
  
  IF Bug trouvé :
    bug_deja_trouve = True
    Correction selon bugfix-protocol (Phase 4+5)
    Revue : voir la règle de modèle (classes de modèles récentes : pas de revue externe requise)
    Commit + Push
    compteur = 0  # RÉINITIALISATION
  ELSE:
    compteur += 1
    Signaler : "✓ Propre : {zone} — {compteur}/{objectif}"
  
  IF compteur >= objectif :
    IF NOT bug_deja_trouve :
      # Escalade par doublement : aucun bug trouvé → recherche trop superficielle ?
      objectif = Taux_de_base * 2
      bug_deja_trouve = True  # Escalade UNE SEULE fois
      Signaler : "⚠ Aucun bug en {Taux_de_base} passes → objectif doublé à {objectif}."
      CONTINUE LOOP
    ELSE:
      GOTO Vérification finale
```

### Conseils pratiques sur la boucle de recherche (tirés des sweeps)

- **Dépôts sans Git :** Là où `git` n'est pas disponible (par ex. dossiers de projet synchronisés dans le cloud), une **sauvegarde versionnée** remplace « Commit + Push » : avant la première correction, créer `fichier_<ts>.bak`. **Attention — la sauvegarde pré-correction n'est PAS une sauvegarde du travail :** après la dernière correction, créer une nouvelle sauvegarde `_FINAL_`, sinon tout le travail de correction est perdu en cas d'incident de synchronisation.
- **Nombreux bugs connus à l'avance :** Si N bugs sont déjà connus au départ (par ex. issus d'une exécution précédente), « par bug : Correction → Revue → Commit → Réinitialisation » est impraticable. Traiter alors les bugs connus comme UN seul bloc de correction (avec une revue commune à la fin) et compter le taux de base / la boucle à partir du premier NOUVEAU bug découvert. La logique de réinitialisation continue de s'appliquer aux nouveaux bugs trouvés pendant le sweep.
- **Même bug à plusieurs endroits :** Un défaut découvert (par ex. une regex erronée ou une hypothèse de format défaillante) est souvent copié ailleurs. Après chaque correction, rechercher si le même motif apparaît à d'autres endroits — cela constitue une « zone » dédiée très rentable.

## 3. Règles de zone (anti-contournement)

Une « zone » est soit un **focus code**, soit une **tâche** (finalité du code).

### Focus code
- Peut être **élargi** (plus de fichiers) ou **déplacé** (autre partie) entre les passes.
- Ne doit PAS être exactement la même sélection que lors d'une passe précédente.
- Exemple OK : Passe 1 = `maintenance.py`, Passe 5 = `maintenance.py + orchestrator.py` (élargi).
- Exemple NON OK : Passe 1 = `maintenance.py`, Passe 5 = `maintenance.py` (identique).

### Tâche (finalité)
- Peut être rendue plus **granulaire** (vérifier une sous-fonction) ou plus **large** (fonctions liées).
- Ne doit PAS être exactement la même tâche.
- Exemple OK : Passe 1 = « Thread-safety dans le watchdog », Passe 5 = « Thread-safety globale du tray » (plus large).
- Exemple OK : Passe 1 = « Détection de processus », Passe 5 = « Correspondance des marqueurs de store dans la détection de processus » (plus granulaire).
- Exemple NON OK : Passe 1 = « Thread-safety dans le watchdog », Passe 5 = « Thread-safety dans le watchdog » (identique).

### Nommage
- La zone DOIT être nommée AVANT la recherche (pas d'attribution rétroactive).
- Format : `"{Nom}" ({type}: code|tache)`

## 4. Vérification finale

Une fois que `compteur >= objectif` ET `bug_deja_trouve` :

**Étape A — bugfix-protocol Phase 5 :**
- [ ] Suite de tests complète au vert (`pytest`)
- [ ] **Exécuter réellement le chemin d'exécution modifié au moins une fois** — pas seulement les tests. Des tests unitaires verts sur du code qui n'appelle même pas l'endroit modifié donnent une fausse sécurité. Exécuter le chemin réellement modifié (dry-run, test de fumée, appel CLI) et vérifier l'absence de tracebacks / erreurs de signature / erreurs de nom. `py_compile` ou un simple import ne vérifie QUE la syntaxe, pas que le chemin fonctionne.
- [ ] **Chaque correction possède au moins un test qui la sollicite** — une correction sans test déclenchant réellement la branche modifiée est considérée comme non vérifiée (pour les chemins d'orchestration/réseau, combiner si nécessaire mock + dry-run).
- [ ] Vérification des types (si configurée)
- [ ] Lint (si configuré)
- [ ] Cas limites des corrections de la session vérifiés

**Étape B — Revue (règle de modèle) :**
- **Classes de modèles récentes (par ex. classe Claude 5 / Fable) :** AUCUNE revue externe par conseiller ou second modèle requise. L'étape A (tests + exécution réelle de fumée) constitue la vérification. En cas de doute réel, optionnellement faire appel à un sous-agent de revue neuf — mais vérifier empiriquement ses constats (test contre le code non modifié) avant de les compter comme bugs. Contexte (retour d'expérience sweep 2026-06-11) : le second réviseur était indisponible, le sous-agent de remplacement a signalé 1 constat (confiance 85) qui s'est révélé ne pas être un bug par test — la revue externe n'a pas changé le résultat.
- **Modèles plus anciens :** Discussion finale avec le conseiller (solution de repli : second modèle comme réviseur) ; le conseiller confirme ou identifie les lacunes.

**Si un bug est trouvé lors de la vérification :**
→ Correction + Test + Commit
→ RÉINITIALISATION : `compteur = 0`, `objectif = Taux_de_base` (neuf, PAS de doublement)
→ Retour à la boucle de recherche (la liste `verifies` est conservée, `bug_deja_trouve = True`)

**Si la vérification est propre :**
→ TERMINÉ. Commit + Push. Produire le rapport.

## 5. Rapport (à la fin)

```markdown
## Résultat du Bug-Sweep

- **Base de code :** {LOC} LOC
- **Taux de base :** {Taux_de_base} (escaladé : {objectif})
- **Zones vérifiées :** {len(verifies)}
- **Bugs trouvés :** {nombre}
- **Réinitialisations :** {nombre_resets}
- **Doublement déclenché :** oui/non
- **Corrections :**
  - {titre} — {commit_hash}
  - ...
- **Suite de tests finale :** {passed}/{total} au vert
- **Verdict de revue :** Auto-vérification (classe de modèle récente) / Confirmé par le conseiller / Lacunes signalées
```

## Quand utiliser ce flux de travail

- Après le développement d'une fonctionnalité (assurance qualité)
- Avant une release (balayage de réception)
- Périodiquement comme contrôle d'hygiène
- Lorsque l'utilisateur saisit `/bugsweep`

## Interaction avec d'autres compétences

- **bugfix-protocol :** Procédure de correction (Phase 4+5) pour chaque bug trouvé
- **systematic-debugging :** Pour les bugs difficiles à reproduire au sein du sweep
- **code-review :** Peut être utilisé comme zone de type tâche

---

## Journal des modifications

### 1.1.1 (2026-11-22)
- Indication de langue corrigée

### 1.1.0 (2026-06-13)
- Règle de modèle pour l'étape B rétroportée (depuis l'installation locale de la compétence, état au 2026-06-11) : les classes de modèles récentes vérifient elles-mêmes via les tests + un vrai test de fumée, aucune revue externe nécessaire ; champ « Verdict de revue » du rapport étendu en conséquence

### 1.0.0 (2026-06-13)
- Publication initiale dans la bibliothèque de compétences (reprise depuis l'installation locale, état au 2026-06-01)
