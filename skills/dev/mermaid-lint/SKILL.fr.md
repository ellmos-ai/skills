---
name: mermaid-lint
version: 1.0.0
type: tool
author: Lukas Geiger + Claude
created: 2026-09-20
updated: 2026-09-20
aliases: [mermaid, mermaid-fehler, diagramm-render-fehler, unable-to-render-rich-display, schaltplan-fehler]
description: "Trouve et corrige les diagrammes Mermaid que GitHub ne rend pas (\"Unable to render rich display\"). Vérifie chaque bloc ```mermaid avec le véritable analyseur Mermaid, sans navigateur, puis confirme le résultat sur la page GitHub en ligne."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: dev
tags: [mermaid, markdown, github, readme, diagramm, lint, dokumentation]
language: fr
status: active
visibility: public
dependencies: {'tools': ['node', 'git'], 'services': ['GitHub'], 'protocols': [], 'python': [], 'npm': ['mermaid', 'jsdom', 'playwright-core']}
translated_from_sha256: a1286c3571792da726aea23967c12360cb0daadb8d3d0bce2208ff27fc14bce9
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.164575+00:00"
---
<img src="banner.png" width="100%" alt="mermaid-lint banner">

# mermaid-lint

Un diagramme Mermaid avec une erreur de syntaxe affiche sur GitHub, à la place de la figure, la boîte
**"Unable to render rich display"**. En local, cela ne se remarque pas, car aucun outil ne vérifie le bloc.
Cette compétence comble cette lacune.

## Quand l'appliquer

- Un README ou un document affiche une erreur de rendu sur GitHub au lieu d'un diagramme.
- Avant une publication ou une version comportant des diagrammes dans la documentation.
- Après chaque remaniement de Markdown qui touche des blocs Mermaid.
- À l'échelle de plusieurs dépôts, lorsqu'on ne sait pas où se trouvent les erreurs.

## Les deux outils

### 1. `mermaid_lint.mjs` — Vérification de la syntaxe sans navigateur

```
node mermaid_lint.mjs <repo-pfad> [...] [--json]
node mermaid_lint.mjs --from <liste.txt> [--json]
```

Recherche récursivement tous les fichiers `.md`, extrait chaque bloc ```mermaid et le fait
passer dans `mermaid.parse()` — **le même analyseur que GitHub utilise dans le navigateur**.
Sortie 0 = tout s'analyse, sortie 1 = au moins un bloc défectueux. La sortie indique le fichier,
le numéro de bloc, la ligne et le message d'erreur de l'analyseur, mot pour mot.

`--from <datei>` lit une liste de chemins, un par ligne. Utilise-la plutôt que de nombreux arguments :
les chemins Windows avec des barres obliques inverses sont silencieusement altérés dans le shell Bash
(de `D:\code\my-repo`, on obtient `D:codemy-repo`). Écris les chemins avec des barres obliques droites.

Un seul processus traite des centaines de dépôts, car Mermaid n'est chargé qu'une fois.
Ni Puppeteer, ni téléchargement de Chromium.

### 2. `readback.mjs` — Preuve sur la page en ligne

```
node readback.mjs <github-url> [...]
```

Ouvre les pages dans Edge déjà installé (aucun téléchargement de navigateur) et compte les vraies
erreurs de rendu. Verdict par page : `OK`, `DEFEKT`, `UNKLAR` ou `KEIN-MERMAID`.

## Trois pièges qui rendent cette compétence nécessaire

**GitHub rend Mermaid dans des iframes sandbox** issues de `viewscreen.githubusercontent.com`.
La page principale ne voit pas leur contenu. Quiconque n'évalue que `document.body.innerText` ou
`msedge --dump-dom` obtient zéro erreur signalée sur **chaque** page, y compris sur une page dont on sait
qu'elle est défectueuse. `readback.mjs` évalue donc toutes les frames.

**Un seul constat DEFEKT n'est pas fiable.** Pendant le chargement, GitHub affiche brièvement un
espace réservé qui ressemble à une erreur de rendu. Mesure du 2026-09-20 : la même page a d'abord signalé
`ERR=1`, puis deux fois `ERR=0`. `readback.mjs` répète donc automatiquement les constats
négatifs ; un `OK` n'est jamais répété.

**`mermaid.parse()` a besoin d'un DOM**, faute de quoi il échoue sur `DOMPurify.addHook` et
signale à tort des diagrammes de flux valides comme défectueux. `mermaid_lint.mjs` fournit au préalable
une fenêtre jsdom. Si une erreur d'environnement subsiste, elle est consignée séparément sous
`envIssues` et **n'est pas** comptée comme erreur de syntaxe.

## Toujours vérifier avec un contrôle négatif

Avant de faire confiance à un résultat vert, fais tourner l'outil une fois sur un état dont tu sais qu'il
est défectueux — par exemple le commit précédant ton correctif :

```
node readback.mjs "https://github.com/<org>/<repo>/blob/<alter-sha>/README.md"
```

Si celui-ci signale aussi `OK`, ta relecture ne mesure rien. C'est ainsi que le piège
des iframes décrit plus haut a été découvert.

## Causes fréquentes d'erreurs et corrections minimales

| Symptôme dans l'erreur d'analyse | Cause | Correction |
|---|---|---|
| `Expecting '+', '-', '()', 'ACTOR', got 'loop'` | Un participant porte le nom d'un mot réservé : `loop`, `alt`, `opt`, `par`, `end`, `critical`, `break`, `rect`, `note` | Déclarer un alias : `participant L as Loop`, les messages utilisent `L`. Le **nom affiché reste inchangé** — ne pas le renommer. |
| `got 'PS'` dans un diagramme de flux | Parenthèses rondes dans l'étiquette d'un nœud | Mettre l'étiquette entre guillemets : `A["Start (hier)"]` |
| `Lexical error ... Unrecognized text` | Accents graves ou deux-points dans l'étiquette | Mettre l'étiquette entre guillemets, supprimer les accents graves |
| `Expecting 'SEMI', 'NEWLINE', 'EOF'` dans `graph`/`flowchart` | `Note:` n'existe que dans les diagrammes de séquence et de classes | Retirer le texte explicatif du bloc et le placer en ligne Markdown en dessous, afin que l'information reste visible |
| `Expecting 'SOLID_OPEN_ARROW' ... got 'NEWLINE'` dans un diagramme de séquence | **Entité HTML** dans le texte d'un message (`&lambda;`, `&Delta;`, `&ge;`). Ici, ni les parenthèses ni le `=` ne posent problème — le `;` de fin de l'entité est lu par l'analyseur lexical comme terminateur d'instruction, et tout ce qui suit devient une nouvelle instruction. | Remplacer l'entité par le caractère littéral (λ, Δ, ≥), sans modifier le reste du texte. Les parenthèses peuvent rester. Ne jamais modifier les valeurs numériques ni leur écriture. |
| Point-virgule dans un message de séquence | Lu comme fin d'instruction | Le remplacer par ` - ` |

Dans les **étiquettes de diagramme de flux entre guillemets**, les entités ne posent aucun problème — la règle ne
s'applique qu'aux messages de séquence. `mermaid_lint.mjs` signale ces entités sur une ligne `[WARN]` distincte
(champ `warnings` dans le JSON), en plus de l'erreur d'analyse : l'analyseur indique seulement
`got 'NEWLINE'` et ne donne pas la cause.

**Principe :** minimalement invasif. Mise en page, identifiants de nœuds, ordre et texte visible restent,
dans la mesure du possible, inchangés. Dans les dépôts scientifiques, cela vaut en particulier pour les
valeurs numériques et leur écriture. Pour la parité EN/DE, garde les deux versions structurellement identiques.

## Déroulement sur plusieurs dépôts

1. Inventaire avec `gh repo list <org> --limit 200 --json name,isArchived,isPrivate,defaultBranchRef`.
2. Mettre les clones **à jour par rapport au dépôt distant** et prendre les divergences au sérieux. Une
   vérification sur un clone obsolète mesure le mauvais état. Si `git pull --ff-only` échoue, vérifie
   par rapport à `origin` plutôt que par rapport à l'arbre de travail :
   `git archive origin/<branch> | tar -x -C <tempdir>`, puis vérifie le dossier temporaire.
3. **Des dépôts homonymes d'organisations différentes** (typiquement `.github`) ne doivent pas être
   associés au même clone — sinon on vérifie neuf fois le même dépôt. En cas de nom en double, cloner à plat
   dans `<org>__<repo>` et vérifier la version fraîche.
4. Avant chaque modification, contrôler les verrous (`lock_scan.py`, `LOCK*.txt` dans le clone **et**
   dans le chemin du projet OneDrive), poser son propre verrou et le retirer après le push.
   **Lire la portée, pas seulement l'existence :** un `LOCK.team.*` dont le `expires_after` a expiré peut être ignoré ;
   `LOCK.user.zenodo-upload.txt` ne bloque que l'opération d'écriture externe vers Zenodo et autorise expressément les modifications
   de documentation. En revanche, un `LOCK.user.until-winners-announcement.txt` (jugement) bloque tout push — là, il faut seulement
   vérifier en lecture seule et consigner le constat dans un ticket.
5. Réparer, vérifier jusqu'au vert, committer, `git pull --rebase`, pousser.
6. Relecture avec contrôle négatif. Ce n'est qu'alors que la tâche est considérée comme terminée.

## Installation

```
npm install mermaid jsdom playwright-core
```

Dans le dossier des scripts ou globalement ; `playwright-core` utilise Edge installé
(`channel: 'msedge'`) et ne télécharge pas de navigateur propre. Nécessaire uniquement pour la relecture —
la vérification de la syntaxe fonctionne sans lui.

## Voir aussi

- `_tools/lint_mermaid.py` dans GithubBot : ancien linter basé sur des expressions régulières avec `--fix`.
  Il répare automatiquement les motifs connus, mais **ne connaît pas les mots réservés** et ne remplace pas
  cette compétence. Ordre conseillé : d'abord `mermaid_lint.mjs` pour le diagnostic, puis éventuellement `lint_mermaid.py --fix`
  pour les motifs récurrents, puis une nouvelle vérification.
- `github-repo-care` : protocole général pour la maintenance des dépôts et la publication.
