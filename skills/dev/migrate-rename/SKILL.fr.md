---
name: migrate-rename
version: 1.1.1
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-11-22
description: "Utilisez cette compétence lorsque des fichiers, modules ou dossiers doivent être renommés ou déplacés sans casser brutalement les imports et dépendances de chemins existants (par ex. 'renommer fichier sans breaking changes', 'déplacer module', 'créer un wrapper', /migrate-rename). Crée des fichiers wrapper et des stubs MOVED pour une migration évolutive sans rupture. Ne PAS utiliser pour de simples déplacements Git sans pont de compatibilité."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [migration, renaming, wrapper, evolutionary, refactoring]
language: fr
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/migrate-rename.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="migrate-rename banner">

> **Français** — Version française officielle de la compétence `migrate-rename`.

# Renommage de fichiers avec wrapper (migration évolutive)

> Permet de renommer des fichiers SANS ruptures brutales. Les références sont mises à jour organiquement au fil de l'utilisation quotidienne.

---

## Principe : migration évolutive

```
AVANT :                          APRÈS :
ancien_fichier.md                nouveau_fichier.md (renommé)
   |                                |
   +-- Référence A                  +-- ancien_fichier.md (Wrapper)
   +-- Référence B                         |
   +-- Référence C                         +-- Tableau de journal
                                           +-- Instructions
                                           +-- Lien vers nouveau_fichier.md
```

Quiconque appelle l'ancien chemin :
1. Arrive sur le fichier wrapper
2. S'inscrit dans le journal de migration
3. Corrige la référence qui l'y a envoyé
4. Accède au véritable fichier cible

---

## Étape par étape

### 1. Renommer le fichier

```bash
mv ancien_fichier.md nouveau_fichier.md
```

### 2. Créer le fichier wrapper

Créer `ancien_fichier.md` avec le contenu suivant :

```markdown
# ANCIEN_FICHIER.md - REDIRIGÉ

**Statut :** Ce fichier a été renommé en `nouveau_fichier.md`

---

## Journal de migration

| Date | Qui | Provenance | Référence corrigée ? |
|------|-----|------------|----------------------|
| YYYY-MM-DD | [Nom] | Migration initiale | n/a (wrapper créé) |

---

## Instructions

1. **Laisser une entrée dans le journal** (dans le tableau ci-dessus)
2. **Vérifier la provenance** : Qu'est-ce qui vous a envoyé ici ?
3. **Corriger la référence** : Changer `ancien_fichier.md` -> `nouveau_fichier.md`
4. **Aller au véritable fichier** : `nouveau_fichier.md`

---

**Fichier cible :** `nouveau_fichier.md`
```

### 3. Corriger immédiatement les références critiques
- Fichiers d'aide (documentation primaire)
- Références dans les prompts système
- Code CLI qui utilise directement le chemin

### 4. Migrer les autres références de manière évolutive
Le reste est corrigé automatiquement lors de l'utilisation.

---

## Quand utiliser la méthode du wrapper ?

**OUI — Wrapper pertinent :**
- Nombreuses références potentielles
- Fichier référencé par différents partenaires ou outils
- Pas un fichier système critique

**NON — Tout modifier directement :**
- Références peu nombreuses et connues
- Fichiers système critiques (configuration, schéma de base de données)
- Chemins critiques pour les performances

---

## Déplacement de dossier ou fichier avec stub MOVED

> Formalisé le 2026-09-06 (Ticket T-20260906-688261413). Précédent apparu spontanément avec
> `.ELLMOS.MIGRATED.md` (2026-08-11) et les stubs `_control-center/_CONTROL` (2026-09-06).

Autre situation que le wrapper ci-dessus : ici, un **dossier entier** ou un **fichier sans nombreuses références actives** déménage complètement vers un nouvel emplacement (consolidation, renommage, réorganisation de pipeline). Il n'y a ni journal de migration, ni « corriger la référence » — seulement un pointeur concis qui indique : voici où il se trouve désormais.

**Différence avec la procédure de wrapper ci-dessus :**

| | Wrapper (étapes 1 à 4 ci-dessus) | Stub MOVED |
|---|---|---|
| Usage | Fichier unique, nombreuses références actives à mettre à jour organiquement | Dossier ou fichier, déménagement complet |
| Contenu | Tableau de journal de migration, croît avec l'usage | Métadonnées statiques, 1 à 3 lignes de texte brut |
| Durée de vie | Jusqu'à ce que le journal montre qu'il n'y a plus de nouvelles entrées | Jusqu'à ce que `remove_when` soit rempli |

### Nom, emplacement, champs obligatoires

Le schéma complet, un exemple et la sémantique des champs figurent dans le modèle ellmos `MOVED-STUB.md` (`.TOPICS/.AI/_templates/project-docs/MOVED-STUB.md`, qui ne fait pas partie de ce dépôt autonome — un résumé suffit ici) :

- **Nom/Emplacement :** `<ancien-nom>.MOVED.md` se place là où le dossier ou le fichier se trouvait **auparavant**.
- **Champs obligatoires** (`key: value`, dans cet ordre) : `moved_to`, `moved_on`, `ticket`, `reason`, `moved_by`, `remove_when` (par défaut : `90 jours ET 0 référence vivante`).
- **Ensuite** 1 à 3 lignes de texte brut pour les humains. Pas de journal, pas de tableau, pas d'historique — celui-ci figure dans le ticket référencé.
- **Suppression :** Le stub est **supprimé**, jamais archivé.

### Règle (Policy)

Applicable en tant que `.SYNC/_policies/library/P-017_umzugs-stub.md`.

### Script de vérification

`scripts/moved_stub_check.py` (dans ce dossier de compétence) répertorie tous les stubs `*.MOVED.md`/`*.MIGRATED.md` sous un répertoire racine, signale les champs obligatoires manquants et marque les stubs arrivés à échéance de suppression (plus anciens que les jours indiqués dans `remove_when`). Appel :

```bash
python scripts/moved_stub_check.py <repertoire_racine>
```

---

## Nettoyage

Après environ 30 jours ou lorsque le journal montre qu'il n'y a plus de nouvelles entrées :
1. Déplacer le fichier wrapper vers `_archive/deprecated/`
2. Ou le supprimer complètement (s'il n'y a plus d'entrées)

---

## Journal des modifications

### 1.1.1 (2026-11-22)
- Indication de langue corrigée

### 1.1.0 (2026-09-06)
- Ajout de la section « Déplacement de dossier ou fichier avec stub MOVED » (Ticket T-20260906-688261413) : formalise le pointeur de déplacement concis pour dossiers/fichiers complets (standard `<ancien-nom>.MOVED.md`, champs obligatoires `moved_to`/`moved_on`/`ticket`/`reason`/`moved_by`/`remove_when`), distingué de la méthode de wrapper ci-dessus. Ajout du script de vérification `scripts/moved_stub_check.py`.

### 1.0.0 (2026-03-15)
- Porté depuis BACH v3.8.0

---

*Porté depuis BACH v3.8.0 | Version autonome*
