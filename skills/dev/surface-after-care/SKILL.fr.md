---
name: surface-after-care
version: 1.6.0
type: protocol
author: Lukas Geiger + Claude
created: 2026-07-24
updated: 2026-07-24
aliases: [repo-after-care, repo-pflege, after-care, repo-nachpflege, repo-wartung]
description: "Passage de maintenance régulier pour un dépôt GitHub déjà publié (niveau 1, peu coûteux et souvent reproductible) : identifier d'abord toutes les surfaces de distribution du projet (npm, PyPI, registres, marketplaces, stores, site web) et y répercuter ensuite les modifications, puis définir les topics, effectuer le contrôle de confidentialité, vérifier que les documents sont destinés à la publication et ignorer après coup les fichiers de planification internes, ajouter une bannière, confronter les affirmations du README à l'état réel du code, améliorer la présentation, compléter les versions linguistiques du README, mettre en œuvre les mesures de visibilité, vérifier l'entrée sur la page de l'organisation ainsi que traiter les issues et pull requests ouvertes. Utilisez cette compétence lorsqu'un dépôt existant doit être entretenu, nettoyé, mis à jour, embelli ou « revu une fois de plus », lorsqu'un dépôt paraît obsolète ou désordonné, pour des formulations telles que « entretien du dépôt », « after care », « suivi post-publication », « remettre le dépôt à niveau », « nettoyer et pousser », ou pour des cycles de contrôle qualité tournants sur plusieurs dépôts. Pour le passage approfondi incluant la vérification juridique et les renvois transversaux entre organisations, utilisez plutôt full-after-care ; pour la première publication, github-repo-care."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false

category: dev
tags: [github, repo, maintenance, privacy, i18n, documentation, visibility, issues]
language: fr
status: active
visibility: public

dependencies:
  tools: [git, gh, rg]
  services: [GitHub]
  protocols: []
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: null
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: bc9d83148b0f265a9304d21d1ec9efaea306584890f1516e21dec9b6958a9026
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:43.944365+00:00"
---
<img src="banner.png" width="100%" alt="surface-after-care banner">
# Surface After Care — la ronde d'entretien régulière d'un dépôt publié

## Quand cette compétence s'applique

Utilisez-la pour un dépôt **déjà public** qui doit être revu périodiquement. C'est le niveau économique : tout ce qui peut être décidé sur le dépôt lui-même, sans inventorier des dépôts tiers ni déclencher une expertise juridique.

Délimitation avec les compétences voisines :

| Situation | Compétence |
|---|---|
| Le dépôt est publié pour la première fois | `github-repo-care` |
| Le dépôt est public, ronde d'entretien régulière | **la présente compétence** |
| En plus : vérification juridique + renvois entre toutes les organisations + i18n de l'application | `full-after-care` (alias `deep-after-care`) |
| Vérification pure juridique / confidentialité / licence avant la mise en public | `repo-publish-check` |
| Maintenir les versions linguistiques synchronisées sur le fond | `bilingual-doc-sync` |
| Répartition de cette ronde sur de nombreux dépôts, en rotation équitable | `rotation-check` |

## Idée centrale

Un dépôt publié dérive dans deux directions : **la documentation décrit un logiciel plus ancien que celui qui se trouve dans le dépôt**, et **des fichiers s'accumulent qui n'ont jamais été destinés à des yeux étrangers**. Les deux cas sont rarement dramatiques, mais ils coûtent précisément aux utilisateurs qu'on cherche à gagner — l'un abandonne parce que la procédure d'installation ne correspond plus, l'autre parce qu'il tombe à la racine sur `AUFGABEN.txt` et `Plan.txt` et a l'impression que quelqu'un travaille ici seulement pour lui-même.

Cette ronde range les deux. Elle est volontairement reproductible : mieux vaut une demi-heure quatre fois par an qu'un grand nettoyage unique.

## Déroulement

L'ordre n'est pas arbitraire. L'étape 0 est placée au début parce qu'elle détermine le périmètre de toutes les étapes suivantes. L'étape 2 doit précéder tout ce qui pousse des modifications — sinon on empile des améliorations sur un état qui doit encore être nettoyé. L'étape 1 est purement côté serveur et ne perturbe rien.

### 0. Inventorier les surfaces de distribution

**Avant de modifier quoi que ce soit : établir où ce projet existe partout.** Le dépôt GitHub est rarement la seule surface. Un README corrigé ne sert pas à grand-chose si la page du paquet npm affiche encore l'ancienne version avec la mauvaise instruction d'installation — et c'est justement là qu'atterrissent la plupart des utilisateurs, car les registres de paquets se classent souvent mieux dans les moteurs de recherche que le dépôt.

```bash
# Manifeste verraten die Kanäle
cat package.json pyproject.toml setup.py Cargo.toml 2>/dev/null | rg -n "name|version|keywords|repository|homepage"
rg -n "npmjs.com|pypi.org|marketplace|registry|crates.io|hub.docker|zenodo|doi" README* docs/ .github/ 2>/dev/null

# Veröffentlichten Stand der Kanäle abfragen (nur was zutrifft)
npm view <paket> version description keywords 2>/dev/null
pip index versions <paket> 2>/dev/null
gh release list --repo ORG/REPO --limit 5
```

Surfaces typiques : npm, PyPI, Crates, Docker Hub, registre MCP, répertoires de plugins/skills, marketplaces VS Code ou navigateur, stores d'applications, Zenodo/DOI, site du projet, profil d'organisation, `llms.txt`, dépôts miroirs sur d'autres hébergeurs.

Consignez la liste trouvée dans le journal d'exécution. Elle constitue désormais l'**ensemble cible** : chaque modification des étapes suivantes sera reportée à la fin sur cette liste (voir « Parité sur toutes les surfaces »). Si vous trouvez une surface que plus personne n'entretient et qui pointe vers un état périmé, c'est un constat à part entière — la mettre à jour ou la retirer délibérément, mais ne pas la laisser en l'état.

### 1. Définir les topics

Les topics sont la surface de recherche la plus importante à l'intérieur de GitHub, et ils ne coûtent presque rien.

```bash
gh repo view ORG/REPO --json nameWithOwner,description,repositoryTopics,homepageUrl,visibility
gh repo edit ORG/REPO --add-topic <topic> --add-topic <topic>
```

Visez environ 5 à 12 topics dans trois directions : **ce que c'est** (`cli`, `mcp-server`, `python-library`), **de quoi il traite** (`file-management`, `tax`, `note-taking`) et **comment il fonctionne** (`local-first`, `offline`, `privacy`). Inspirez-vous des topics réellement utilisés par des projets comparables — les topics inventés ne trouvent aucun utilisateur. Vérifiez aussi la description et la page d'accueil, qui figurent dans la même vue.

Les topics ont un équivalent sur les autres surfaces de l'étape 0 : `keywords` dans `package.json`, `keywords`/`classifiers` dans `pyproject.toml`, catégories et tags dans les marketplaces et stores. Gardez-les cohérents sur le fond — c'est la même décision, simplement appliquée à plusieurs endroits.

### 2a. Contrôle de confidentialité — toujours exécuté

Cette étape n'est jamais omise, même pour une ronde qui paraît anodine. La recherche porte sur l'**ensemble suivi**, non sur l'arbre de travail visible, car c'est précisément la différence entre « ça a l'air propre » et « c'est propre ».

```bash
git ls-files
rg -n "C:\\\\Us[e]rs\\\\|/home/[a-z]|s[k]-[A-Za-z0-9]{16}|gh[p]_|gh[o]_|AKIA[0-9A-Z]{16}|API[_-]?KEY|TO[K]EN|PASS[W]ORD|SEC[R]ET|BEGIN [A-Z ]*PRIVATE KEY" $(git ls-files)
rg -n "\x{C3}\x{83}|\x{C2}\x{A0}|\x{FFFD}" $(git ls-files -- '*.md' '*.txt' '*.json')
```

Complétez le motif par les **noms de vos propres espaces internes** — dossiers de pipeline, répertoires thématiques, espaces de travail privés :

```bash
rg -n "\.SOFTWARE|\.RESEARCH|_control-center|<weitere eigene Ordnernamen>" $(git ls-files)
```

De telles références ne sont pas des secrets et ne déclenchent aucune alerte, c'est pourquoi elles passent à travers — mais elles sont **impossibles à résoudre** pour un lecteur (« transféré depuis le pipeline .SOFTWARE » ne dit rien à un inconnu) et elles révèlent la structure interne. Elles doivent être remplacées ou retirées, pas simplement tolérées. Une recherche qui ne traque que `C:\Users\…` et les motifs de jetons ne les trouvera jamais.

Si vous trouvez quelque chose : c'est la **nature** de la découverte qui détermine la marche à suivre — voir la section « Règle du force-push ». Un secret qui a un jour été committé est compromis : le retirer de `HEAD` ne suffit pas, il doit être révoqué.

### 2b. Vérifier la destination des documents

C'est le cœur de cette ronde. Parcourez les `.md`, `.txt` et `.json` suivis et posez-vous pour chaque fichier la question : **était-il destiné à des étrangers ?**

```bash
git ls-files -- '*.md' '*.txt' '*.json' | sort
```

Ne devinez pas d'après le nom du fichier — ouvrez-le brièvement. Un `PLAN.md` peut être une feuille de route publique, un `notes.md` d'apparence anodine peut contenir la stratégie tarifaire interne. Trois catégories :

**Doit figurer dans le dépôt** — README, LICENSE, CHANGELOG, SECURITY, CONTRIBUTING, `docs/`, références d'API, exemples de configuration, feuilles de route réelles, manifestes (`package.json`, `pyproject.toml`), lockfiles, configuration CI.

**Ne doit pas figurer dans le dépôt, mais sans danger** — le cas normal de cette ronde. Fichiers de tâches et de planification (`AUFGABEN.txt`, `Plan.txt`, `TODO-intern.md`), notes de session et transmissions (`HANDOFF`, `BRIEFING`, `_handoff/`), fichiers d'état du pipeline propre, journaux de développement, `_archive/`, JSON de registre et d'index contenant des chemins locaux, états intermédiaires et artefacts générés, fichiers de travail d'agents. Ces fichiers ne sont pas dangereux, mais ils créent du désordre et l'impression d'un chantier étranger. Traitement : ajouter `.gitignore`, les retirer de l'index avec `git rm --cached <datei>` et **pousser normalement**.

**Ne doit pas figurer dans le dépôt et est sensible** — identifiants, données personnelles, données clients, calculs internes, stratégies de prix et de négociation, plans d'affaires non publiés, projets de contrats, tout élément ayant une valeur concurrentielle. Ici, un commit ordinaire ne suffit pas, voir la règle du force-push.

Pour `.json`, un second regard s'impose : les manifestes et lockfiles restent, mais les configurations locales, fichiers de tâches/registre, exports de données et tout ce qui contient des chemins absolus ou des noms d'hôtes sont des passagers clandestins typiques.

Si vous supprimez un fichier que quelqu'un pourrait rechercher (une feuille de route par exemple), mentionnez brièvement dans le commit ou le README où l'information se trouve désormais — sinon cela ressemble à un recul.

### 3. Bannière

Une bannière contribue à décider si quelqu'un commence seulement à lire. Vérifiez si elle existe et si elle est intégrée en premier élément du README.

Si elle manque, trois voies existent — dans cet ordre de pertinence :

1. **Générateur d'images d'un agent** (p. ex. agy ; le mot « génère » y déclenche la création réelle d'un PNG), lorsqu'un motif visuel convient mieux que la typographie.
2. **Codex**, lorsque la bannière doit être produite à partir de code et qu'il existe un modèle de style dont elle peut s'inspirer.
3. **Soi-même en SVG**, lorsque la bannière est essentiellement une wordmark plus un langage de formes — c'est souvent la variante la plus rapide et la mieux contrôlable, et le SVG reste modifiable ensuite.

Respectez la famille si le projet appartient à un groupe : même couleur de base, même esthétique, même traitement de la wordmark. Une bannière qui sort du rang paraît pire qu'aucune. Taille usuelle 1200x300 ; en PNG dans le dépôt, le SVG à côté comme source.

### 4. Confronter les affirmations à l'état réel

C'est ici que l'on crée le plus de valeur. Le README affirme des choses — vérifiez-les au lieu de les croire :

- **Version** dans le README/badge face à `pyproject.toml`/`package.json`/`__version__` et au dernier tag de release. S'il existe plusieurs porteurs de version, tous les vérifier, pas seulement un.
- **Voie d'installation** réellement parcourue, au moins en lecture : le paquet existe-t-il sous le nom indiqué ? Les commandes et options sont-elles correctes ?
- **Liste des fonctionnalités** face au code : tout ce qui est cité existe-t-il, et manque-t-il quelque chose de nouveau dans la liste ?
- **Chiffres** (nombre d'outils, formats pris en charge, couverture de tests) recomptés à la source plutôt que recopiés. Les chiffres du README deviennent faux silencieusement.
- **Captures d'écran** face à l'interface actuelle.
- **Prérequis** (versions Python/Node, dépendances) face aux manifestes.
- **Liens** vers les projets voisins, la documentation et les registres : fonctionnent-ils encore ?

**Une correction vaut pour toutes les surfaces, pas seulement pour celle où elle a été repérée.** Si une affirmation de fond s'avère fausse — surtout si le commanditaire la rectifie —, cette même affirmation se trouve très probablement encore ailleurs : dans le profil d'organisation, dans la `llms.txt`, dans la seconde version linguistique, dans le README d'un projet voisin. Recherchez-la ciblément avant de cocher le point :

```bash
gh search code "<prägnante Formulierung>" --owner ORG
```

Sinon vous corrigez une occurrence et en laissez trois — et la contradiction ne se remarque qu'au passage du dépôt suivant. Cela coûte non seulement du temps, mais ruine la confiance dans la documentation : qui trouve deux descriptions de la même chose ne croit plus aucune des deux.

Améliorez ensuite la **présentation** là où elle est faible : les longues énumérations d'options gagnent à être présentées en tableau ; les blocs de code ont besoin d'étiquettes de langage ; un aperçu de structure ou de déroulement se saisit plus vite sous forme de diagramme Mermaid ou d'arborescence ASCII qu'en prose ; le premier écran doit montrer l'objet, l'installation et un exemple d'utilisation, non les badges et l'historique. Si le README dépasse ~400 lignes, externalisez les détails dans `docs/` et renvoyez-y.

**Règle linguistique pour les README :** le standard est un **README anglais `README.md`** plus une **version allemande**. Exception : si le domaine de l'application est lui-même allemand (droit allemand, fiscalité ou aides allemandes, public germanophone) ou s'il n'existe jusqu'ici qu'une version allemande — alors l'allemand reste la langue principale. Pour chaque autre langue déjà prise en charge par le projet, il faut une version README distincte. Respectez la convention de nommage déjà utilisée dans le dépôt (`README_de.md`, `README.de.md`, `docs/README.de.md`) et n'en inventez pas une seconde à côté. Reliez les versions entre elles dans l'en-tête.

### 6. Créer les langues standard manquantes

Complétez les README qui manquent dans les **langues standard** : allemand, anglais, espagnol, chinois simplifié, japonais, russe. Le but est la portée, donc cela concerne avant tout les projets orientés utilisateurs finaux — pour une bibliothèque destinée aux développeurs au public purement anglophone, un README russe n'apporte rien, il ne fait qu'ajouter de la charge d'entretien. Décidez en connaissance de cause et consignez la décision dans le journal d'exécution afin que la prochaine ronde ne la rediscute pas.

Les nouvelles versions sont **remplies, jamais créées vides** — un squelette « TODO: translate » est pire qu'aucun fichier, car il simule une exhaustivité inexistante. La parité de contenu et la resynchronisation sont traitées par `bilingual-doc-sync` ; lorsqu'il existe plus de deux versions, il est judicieux de faire appel à cette compétence pour la vérification de concordance.

### 7. Visibilité et promotion

Réfléchissez aux mesures qui apportent réellement des utilisateurs à **ce** projet, et mettez-les en œuvre :

- **Registres** auxquels le projet appartient techniquement : registres de paquets (npm, PyPI), registre MCP, répertoires de plugins/skills, marketplaces.
- **Listes sélectionnées** (`awesome-*` et collections thématiques), à condition que les critères d'admission soient réellement remplis. Une PR vers une liste dont les critères ne sont pas atteints coûte de la réputation.
- **Surfaces propres** : profil d'organisation, `llms.txt`, site du projet, README de l'écosystème, renvois depuis des dépôts propres apparentés.
- **Notes de version** comme occasion : une release sans nouveauté racontée n'est pas remarquée.

**Barrière d'autorisation :** tout ce qui sort — PR vers des dépôts tiers, entrées dans des listes externes, publications, soumissions — est **proposé puis exécuté seulement après accord explicite**, sauf autorisation permanente pour ce canal. Les modifications sur les surfaces propres n'ont pas besoin de cette barrière. La raison est simple : une PR retirée vers un dépôt tiers reste visible publiquement et rejaillit sur le projet.

### 8. Entrées sur les pages d'organisation

Commencez par votre propre organisation : le dépôt figure-t-il dans le README de profil (`ORG/.github` → `profile/README.md`), dans la bonne rubrique, avec une description à jour ?

```bash
gh api user/orgs --jq '.[].login'
```

Parcourez ensuite **toutes** les organisations et répondez pour chacune à une seule question : un visiteur de cette page d'organisation profiterait-il de ce dépôt ? Le plus souvent la réponse est non — « ne pas renvoyer » est alors le bon résultat et non une lacune. Lorsque la réponse est oui (proximité thématique, utilisateurs communs, un outil qui complète les projets de l'organisation), placez le renvoi avec une ligne qui explique l'utilité, et pas seulement le nom.

Le profil se trouve dans un dépôt propre (`ORG/.github`). Les modifications y sont entretenues et poussées — selon la règle du répertoire sale de l'étape 11.

### 10. Issues et pull requests

```bash
gh issue list --repo ORG/REPO --state open --limit 50
gh pr list --repo ORG/REPO --state open --limit 30
```

Traitez-les au lieu de simplement les compter :

- **Bugs corrigibles** : corrigez-les directement — le contexte est de toute façon chargé dans cette ronde. Petites corrections clairement délimitées, avec test et référence au numéro d'issue.
- **Issues déjà résolues** : fermez-les avec une phrase expliquant ce qui les a réglées.
- **Signalements peu clairs** : posez une question ciblée (version, système d'exploitation, étapes de reproduction).
- **PR** : lisez réellement le diff, lancez les tests, puis fusionnez ou refusez en motivant. Une PR laissée sans réponse pendant des mois coûte plus de bienveillance qu'un refus poli.
- **Cas périmés** : résolvez-les au lieu de les traîner.

**Barrière d'autorisation :** les commentaires publics, les fermetures motivées et les fusions de contributions tierces sont des communications externes — à présenter avant exécution, sauf autorisation permanente. Les simples corrections de code dans votre propre dépôt ne sont pas concernées.

### 11. Committer, pousser, vérifier

La ronde ne s'achève pas avec les modifications, mais avec le fait qu'elles sont **dehors**. Un arbre de travail rempli d'améliorations non poussées est le pire résultat : la session suivante — peut-être un autre agent ou un autre appareil — doit d'abord se réinstaller dans un état étranger et à moitié fini, et sur les surfaces publiques rien ne s'est amélioré.

Avant le push, assurez-vous de ce qui peut être vérifié : lancez les tests et les smoke tests, pour les modifications de documentation contrôlez les liens et l'aperçu rendu. Regroupez ensuite en **commits thématiquement séparés** plutôt que tout jeter dans un commit fourre-tout — le nettoyage, la mise à jour de la documentation et les corrections de bugs sont trois choses différentes, et celui qui voudra en annuler une plus tard vous en sera reconnaissant :

```bash
git add .gitignore && git rm --cached <interne dateien>
git commit -m "chore: interne Arbeitsdateien aus dem Repo nehmen"
git commit -am "docs: README auf aktuellen Stand (Version, Toolzahl, Screenshots)"
git commit -am "fix: <Issue-Nummer> ..."

git pull --rebase        # bei divergiertem Branch, vor dem Push
git push
```

Vérifiez ensuite au lieu de supposer : README distant dans l'aperçu rendu, exécution CI, état des releases et des tags.

```bash
gh run list --repo ORG/REPO --limit 3
gh repo view ORG/REPO --json description,repositoryTopics,url
```

**Si la CI est rouge alors que votre commit ne touchait que la documentation**, la cause n'est presque jamais votre commit. Le cas de loin le plus fréquent — rencontré trois fois en une seule journée dans cette famille de dépôts — est un **linter non épinglé sans jeu de règles figé**. Vérifiez cela **en premier**, avant de soupçonner quoi que ce soit dans votre commit.

Le mécanisme : si le workflow lance `ruff check` (ou flake8, eslint …) contre une dépendance non épinglée (`ruff>=0.12`, ou sans version du tout), et qu'il manque une sélection explicite de règles (`[tool.ruff.lint] select = [...]` ; en l'absence de `pyproject.toml`, une `ruff.toml` propre), alors le linter suit le comportement par défaut de la version **fraîchement installée**. Une nouvelle version du linter déplace ce défaut, et une base de code inchangée passe au rouge. Les coupables :

- Des codes de règles que le projet n'a jamais eus (`UP045`, `UP006`, `BLE001`, `RUF100`, `DTZ005`, `N999` …), parfois par centaines.
- La rupture se produit souvent **de façon dépendante de la plateforme** : les runners avec une version plus ancienne en cache restent verts, les versions fraîches passent au rouge.
- Parfois une règle signale quelque chose d'irréparable (`N999` le nom même du paquet) — signe sûr qu'elle n'a jamais été le standard.

Correctif : figez le jeu de règles qui était vert auparavant — `select = ["E4","E7","E9","F"]` sont les valeurs par défaut classiques de ruff. S'il n'existe pas de `pyproject.toml`, créez-en une `ruff.toml`. Vérifiez contre la **nouvelle** version du linter elle-même (l'installer, reproduire les signalements sans configuration, constater « passed » avec la configuration). Les nouvelles règles deviennent une **tâche** du projet — accepter délibérément des règles est une décision, pas un effet secondaire d'une mise à jour d'outil. C'est un constat réel et récurrent : sans l'épinglage, la CI casse à la prochaine version du linter, et ce dans **chaque** dépôt configuré ainsi.

Deux cas dans lesquels on ne pousse **pas** : lorsqu'une interdiction de publication ou de soumission s'applique au projet, ou lorsque l'état est délibérément inachevé. Ce sont des exceptions à motiver — le cas normal est : committer et pousser.

En cas d'interdiction de publication, la ronde n'est pas interrompue mais **détournée** : committer localement sur une branche propre (`judging-hold/…`, `freeze/…`), laisser la branche principale intacte dans l'état soumis, consigner le motif de l'interdiction dans le journal d'exécution et rattraper après levée. Il faut être conséquent : ce qui est bloqué n'est pas seulement le `git push`, mais **toute modification visible à distance** — topics, description, page d'accueil, releases, actions sur les issues et PR modifient tout autant le projet publié.

S'il existe d'autres clones du même dépôt (second appareil, copie de déploiement, miroir), mettez-les à jour immédiatement après le push. Un clone en retard de dix commits produira, lors de la prochaine recherche d'erreur, des diagnostics sur un état qui n'existe plus.

#### Modifications dans d'autres dépôts — exception du répertoire sale

Cette ronde produit régulièrement des modifications **en dehors** du dépôt entretenu : une ligne dans le profil d'organisation (étape 8), plus tard dans la ronde approfondie un renvoi dans un dépôt apparenté. Ces modifications sont également committées et poussées — un renvoi non publié n'est pas un renvoi.

Avant de toucher un dépôt tiers, vérifiez brièvement son état :

```bash
git -C <pfad> status --porcelain
```

**Arbre de travail propre** → effectuez la modification, committez-la dans un **commit propre et thématiquement clair** (`docs: link <projekt>`) et poussez-la. Ne la mélangez pas aux commits du dépôt entretenu : c'est un autre dépôt, avec son historique propre et ses lecteurs propres.

**Sale, mais les modifications étrangères portent sur d'autres fichiers** → votre propre modification reste faisable proprement. Indexez et committez **uniquement votre fichier, par chemin**, pour que du travail étranger non vérifié ne soit pas embarqué :

```bash
git -C <pfad> add README.md
git -C <pfad> commit -m "docs: link <projekt>"     # nur der gestagte Pfad
```

Mais **ne poussez pas**. Le commit est localement inoffensif ; un push ne l'est pas forcément : vous ne savez pas vers quoi tend l'autre travail en cours — il est peut-être en train d'être amendé, rebasé ou redécoupé, et votre commit l'obligerait à s'en occuper. Le commit local sécurise le travail sans imposer quoi que ce soit à personne ; l'exécution qui se consacrera plus tard à ce dépôt le trouvera et l'intégrera.

**Sale dans le fichier même que vous devriez modifier** → n'y touchez pas. Il faudrait alors vous greffer sur un état intermédiaire étranger et le committer avec ; comprendre cela coûte plus que ce seul renvoi ne vaut.

**Verrou actif (`LOCK*.txt`) dans le dépôt cible** → **lisez d'abord le verrou au lieu de le traiter comme une interdiction générale.** Un verrou décrit son propre périmètre, et celui-ci est souvent plus étroit que « rien du tout ». Cas typiques :

- **Verrou d'édition** (« quelqu'un travaille ici en ce moment ») → ne rien toucher, pas même un fichier annexe.
- **Verrou purement de publication / de push** (soumission, jugement, gel) → le travail local reste permis, seul le contact distant est bloqué. Travaillez alors sur une branche propre et committez localement ; **les étapes agissant à distance tombent** — non seulement le push, mais aussi topics, description, page d'accueil, releases et actions sur issues/PR, car elles modifient également le projet publié.

Lire un verrou qui ne bloque que le push comme une interdiction totale fait perdre toute la partie locale de la ronde sans gain de sécurité. Inversement, il ne suffit pas de s'abstenir du push tout en modifiant les métadonnées. Dans le doute, citez le verrou et demandez.

#### Le souhait ne doit pas se perdre

Si la modification n'est **pas** exécutée pour l'une de ces raisons, elle passe dans la liste des tâches du dépôt cible — `AUFGABEN.txt`, `TODO.md` ou `TODO.txt`, selon ce qui existe. Une entrée avec date, modification souhaitée et motif :

```markdown
- [ ] [2026-07-24, after-care] Rückverweis auf <projekt> im README ergänzen
      (übersprungen: README hatte uncommittete Fremdänderungen)
```

C'est la différence entre « reporté » et « oublié » : la liste des tâches se trouve là où le prochain intervenant de ce dépôt regarde de toute façon — plus fiable qu'une mention dans le journal d'un passage étranger. S'il n'existe pas de liste de tâches, n'en créez pas ; le point ouvert dans votre propre journal suffit alors.

En cas de **verrou actif**, cette règle ne s'applique pas — le fichier n'est alors pas touché et la mention reste dans votre propre journal. Notez-la dans les deux cas aussi dans votre journal, afin que la rotation connaisse le point ouvert.

Enfin, traitez les surfaces de l'étape 0 — voir la section suivante.

## Parité sur toutes les surfaces de distribution

Pour conclure la ronde, parcourez la liste de l'étape 0 : **toute modification qu'un utilisateur verrait doit arriver sur chaque surface où il la cherche.** Un dépôt dont la page npm raconte une autre histoire est moins bien loti qu'un dépôt n'ayant qu'une seule surface.

Le mécanisme décisif : **les registres de paquets affichent le README de la dernière publication, non l'état actuel du dépôt.** Une correction du README n'apparaît sur npm ou PyPI qu'avec une nouvelle version. Si la correction est importante sur le fond (mauvaise installation, mauvaise version, liste de fonctionnalités périmée), il faut une release de correctif — sinon la correction reste sans effet.

| Surface | Ce qui y est entretenu | Comment cela arrive |
|---|---|---|
| npm | README, `description`, `keywords`, lien vers le dépôt | Uniquement par `npm publish` (version de correctif) ; les métadonnées proviennent de `package.json` |
| PyPI | README (`long_description`), classifiers, URL du projet | Uniquement par nouvel envoi ; métadonnées issues de `pyproject.toml` |
| Registre MCP / répertoires de plugins | Description, version, liste des outils, documentation d'entrée | Selon le registre : mise à jour du manifeste ou nouvelle soumission |
| Marketplace / store | Description, captures d'écran, catégories, versions linguistiques | Via l'interface de gestion propre ; les captures y vieillissent particulièrement vite |
| Docker Hub / registre de conteneurs | Description, tags, exemple d'utilisation | Description du dépôt plus nouveau tag |
| Zenodo / DOI | Métadonnées, auteurs, version | Édition sur place pour les métadonnées, nouvelle version pour le contenu |
| Site / profil d'organisation / `llms.txt` | Description courte, lien, positionnement | Directement modifiable — les surfaces les moins coûteuses, donc à ne jamais oublier |

Lorsqu'une version est relevée, **tous les porteurs de version** doivent être mis à jour simultanément : manifeste, constante dans le code, badge du README, changelog, tag de release, `llms.txt`. Un relevé de version à moitié effectué est plus difficile à diagnostiquer qu'un état uniformément ancien.

Si une mise à jour n'est pas possible ou pas judicieuse sur une surface (p. ex. une release uniquement pour une faute de frappe), consignez-le dans le journal d'exécution afin que la ronde suivante ne prenne pas l'écart pour un oubli.

## Règle du force-push

Le standard est **pas de force-push**. Ignorer après coup des fichiers de planification internes ne justifie pas de réécrire l'historique : l'effort est élevé, chaque clone et chaque fork se casse, les PR ouvertes deviennent inutilisables — et le gain est faible, puisque le contenu est anodin. Voie normale :

```bash
git rm --cached <datei>            # aus dem Tracking, bleibt lokal erhalten
# .gitignore ergänzen
git commit -m "chore: interne Arbeitsdateien aus dem Repo nehmen"
git push
```

Réécrire l'historique (et donc pousser `--force-with-lease`) ne se justifie que pour de **vraies fuites** : identifiants et clés, données personnelles ou clients, ainsi que documents ayant une valeur concurrentielle réelle — calculs internes, stratégies de prix, plans non publiés, éléments internes de contrats. Dans ce cas :

1. **Révoquer d'abord** les secrets concernés — l'historique a déjà été copié, forké et mis en cache à ce stade. La révocation agit, la suppression n'est que cosmétique.
2. Nettoyer l'historique (`git filter-repo` ou BFG), puis pousser `--force-with-lease`.
3. Vérifier forks et caches ; si nécessaire, contacter le support GitHub pour les objets orphelins.
4. Consigner l'opération dans le journal d'exécution : quoi, quand, quelle révocation.

En cas de doute entre « non critique » et « sensible » : traitez comme sensible et soumettez. Les coûts sont asymétriques.

## Les constats deviennent des tâches, pas seulement des lignes de journal

Une ronde d'entretien trouve régulièrement plus qu'elle ne peut ou ne veut corriger au cours de la même ronde : une version linguistique manquante, un retard de modernisation, une publication qui n'a jamais eu lieu. **De tels constats deviennent des tâches au moment de leur découverte** — sinon ils restent dans le journal d'une exécution terminée, où le prochain intervenant du projet ne regarde pas.

La tâche appartient au **système de tâches local au dossier du projet** — là où regarde celui qui travaillera ensuite sur ce projet. Il s'agit généralement de `AUFGABEN.txt` ou `TODO.md` dans le dossier du projet, qui se trouve souvent **hors du clone Git**, dans l'espace où vit la planification. Le clone contient le code, le dossier du projet contient le pilotage ; une entrée dans le clone qui disparaît au prochain `git clean` n'est pas une tâche.

Trois points à respecter :

1. **Séparer la liste interne de la feuille de route publique.** Un `TODO.md` peut être une feuille de route publique entretenue — ce n'est alors pas un lieu de dépôt pour le travail interne. Regardez-y avant d'ajouter quoi que ce soit : si une rubrique « Public roadmap » s'y trouve, notez dans le fichier interne à côté (`AUFGABEN.txt`) et marquez-le comme interne.
2. **Vérifier les entrées existantes au lieu de dupliquer.** Souvent le constat existe déjà. Il n'est alors pas recréé, mais **enrichi** de la preuve empirique de cette exécution (« confirmé : `--help` produit des sorties entièrement en allemand »). Un point connu avec une preuve fraîche vaut plus qu'une seconde entrée à côté.
3. **Consigner aussi ce qui est fait.** Ce que la ronde a corrigé figure comme point coché avec le hash de commit. Cela explique à la ronde suivante pourquoi un constat a disparu et l'empêche de le « redécouvrir ».

Formulez la tâche de façon compréhensible sans le contexte de cette exécution : ce qui a été trouvé, pourquoi cela compte, quelle serait l'étape suivante. « i18n incomplet » n'est pas une tâche ; « le catalogue ne contient que `status.title`, les autres langues sont vides — d'abord transférer les chaînes CLI dans le catalogue, puis remplir les six langues » en est une.

## Journal d'exécution

Consignez le résultat dans `_after-care/LOG.md` (le dossier appartient à la `.gitignore` — c'est du matériel de pipeline, non du contenu du dépôt, conformément à la règle de l'étape 2b). Une ligne par exécution avec date, niveau et décisions prises en connaissance de cause :

```markdown
## 2026-07-24 — surface
- Flächen: GitHub, npm (<paket>), MCP-Registry, Org-Profil, llms.txt
- Topics: +local-first, +mcp-server; keywords in package.json angeglichen
- Entfernt: AUFGABEN.txt, _handoff/ (gitignored, kein Force-Push nötig)
- README: Version 0.9 -> 1.2 korrigiert, Toolzahl 23 -> 26 nachgezählt
- Sprachen: EN + DE gepflegt; ES/ZH/JA/RU bewusst nicht (entwicklernahes Publikum)
- Issues: #12 gefixt, #7 geschlossen (erledigt), #15 Rückfrage gestellt
- Push: 3 Commits, CI grün; npm-Republish 1.2.1 wegen README-Korrektur
- Offen: Store-Screenshots veraltet, brauchen neuen Build
```

Le journal évite à la ronde suivante de reprendre les mêmes décisions et sert de base aux passages d'entretien tournants sur de nombreux dépôts (`rotation-check`).

## Erreurs fréquentes

| Erreur | Correction |
|---|---|
| Seul l'arbre de travail examiné, pas `git ls-files` | Toujours contrôler l'ensemble suivi — le problème s'y trouve |
| Contrôle de confidentialité limité aux chemins et aux jetons | Rechercher aussi les noms de ses propres pipelines/dossiers — ils ne déclenchent aucune alerte et passent à travers |
| Fichier interne supprimé avec réécriture de l'historique | Pour les fichiers non critiques, `git rm --cached` + push normal suffisent |
| Secret retiré de `HEAD` et opération considérée comme close | Révoquer le secret ; le reste n'est que cosmétique |
| Fichiers classés d'après leur nom | Ouvrir brièvement — le nom ne porte pas l'intention de manière fiable |
| Chiffres du README mis à jour par recopie au lieu d'être recomptés | Compter à la source (liste d'outils, exécution des tests, manifeste) |
| Nouvelle version linguistique créée comme squelette vide | La remplir ou y renoncer — un squelette simule une exhaustivité inexistante |
| Seconde convention de nommage du README introduite à côté de l'existante | Reprendre la convention en vigueur |
| PR vers une liste tierce publiée sans accord | Présenter les communications externes ; seules les surfaces propres sont libres |
| Issues comptées au lieu d'être traitées | Corriger, fermer ou demander précisément — chaque cas reçoit un état |
| Bannière créée seul dans un style étranger | Respecter la famille de design de l'écosystème |
| README corrigé dans le dépôt, mais la page npm/PyPI affiche encore l'ancienne version | Les pages des registres proviennent de la dernière publication — publier un correctif |
| Version relevée seulement dans le manifeste | Tous les porteurs de version simultanément : manifeste, code, badge, changelog, tag, `llms.txt` |
| Modifications terminées mais laissées non poussées | Committer et pousser fait partie de la ronde ; seuls les verrous justifient une exception |
| Tout dans un commit fourre-tout | Séparer nettoyage, documentation et corrections — sinon rien ne peut être annulé isolément |
| CI rouge après un commit de documentation, soupçon porté sur soi-même | Un linter non épinglé sans `select` suit le défaut de la nouvelle version — figer le jeu de règles |
| Une affirmation fausse corrigée seulement à l'endroit où elle a été repérée | Rechercher la formulation à l'échelle de l'organisation — elle figure généralement aussi dans le profil, dans `llms.txt` et dans la seconde version linguistique |
| Travail dans un dépôt tiers sale avec `commit -a` | Indexer et committer par chemin, ne pas pousser — le travail étranger reste intact |
| Modification faite dans le dépôt propre du profil d'organisation, mais non poussée | Les dépôts tiers propres reçoivent un commit propre **et** un push propre |
| Modification reportée mentionnée seulement dans son propre journal | Inscrire aussi dans la liste des tâches du dépôt cible, si elle existe |
| Constat écrit seulement dans le journal d'exécution | Il devient une tâche dans le système de tâches local au dossier — personne ne regarde plus tard dans le journal |
| Travail interne rattaché à une feuille de route publique | Regarder d'abord ; « Public roadmap » signifie : utiliser le fichier interne à côté |
| Constat déjà connu dupliqué comme nouvelle entrée | Enrichir le point existant avec la preuve empirique de cette exécution |
| En cas de verrou d'édition, une ligne TODO écrite dans le dépôt verrouillé | Ce verrou couvre tout le projet — ne rien toucher du tout |
| Verrou de push lu comme une interdiction totale, dépôt entièrement ignoré | Lire le verrou : s'il ne bloque que la publication, la ronde locale continue sur une branche propre |
| Pas de push sous verrou, mais topics ou description modifiés | Les métadonnées sont aussi visibles à distance — sous interdiction de publication, elles tombent aussi |

## Liste de contrôle finale

- [ ] Surfaces de distribution identifiées et consignées dans le journal d'exécution.
- [ ] Topics, description et page d'accueil définis et contrôlés.
- [ ] Contrôle de confidentialité exécuté sur l'ensemble suivi, constats traités.
- [ ] `.md`/`.txt`/`.json` contrôlés quant à l'intention de publication, fichiers internes ignorés.
- [ ] Aucun force-push sans véritable fuite ; en cas de fuite, révocation effectuée.
- [ ] Bannière présente et intégrée au README.
- [ ] Version, fonctionnalités, chiffres, captures d'écran, liens contrôlés par rapport à l'état réel.
- [ ] Présentation améliorée (tableaux, diagrammes, premier écran).
- [ ] Matrice linguistique du README complète ; décisions concernant d'autres langues documentées.
- [ ] Mesures de visibilité mises en œuvre ou soumises à accord.
- [ ] Entrée dans le profil de sa propre organisation contrôlée, renvois pertinents vers les autres organisations posés.
- [ ] Modifications dans des dépôts tiers : propres → committées et poussées ; sales → committées localement ;
      non exécutées → inscrites dans la liste des tâches du dépôt cible.
- [ ] Issues et PR amenées dans un état défini.
- [ ] Commits séparés créés, poussés, CI et vue distante vérifiées.
- [ ] Toutes les surfaces de distribution mises au même état (le cas échéant, release de correctif).
- [ ] Constats non corrigés inscrits comme tâches dans le système de tâches local au dossier.
- [ ] Journal d'exécution rédigé dans `_after-care/LOG.md`.

## Journal des modifications

### 1.6.0 (2026-07-24)
- Règle ajoutée : une correction de fond vaut pour toutes les surfaces. Enseignement empirique — une
  rectification de l'utilisateur, corrigée dans le hub dès la première exécution, figurait encore
  cinq fois sans que cela soit remarqué dans le profil d'organisation (EN, DE, `llms.txt`) et
  n'a été repérée que neuf exécutions plus tard.

### 1.5.0 (2026-07-24)
- Diagnostic du linter renforcé après que le motif est apparu trois fois en une journée
  (n8n-workflow-manager ruff 0.15, clirec + swarm-ai ruff 0.16) : « vérifier d'abord », les codes de
  règles révélateurs, la fracture selon la plateforme, `ruff.toml` comme correctif en l'absence de
  `pyproject.toml`, vérification contre la nouvelle version du linter.

### 1.4.0 (2026-07-24)
- Diagnostic ajouté : si la CI passe au rouge après un commit purement documentaire, la cause la plus
  fréquente est un linter non épinglé sans jeu de règles figé — une nouvelle version de l'outil déplace
  le défaut et fait échouer un code inchangé. Correctif : épingler le jeu de règles, traiter les nouvelles
  règles comme une tâche. Survenu deux fois de suite (n8n-workflow-manager avec ruff 0.15, clirec avec 0.16).

### 1.3.0 (2026-07-24)
- Nouvelle section « Les constats deviennent des tâches » : ce que la ronde ne corrige pas elle-même
  devient, au moment de sa découverte, une entrée dans le système de tâches local au projet — là où
  regarde le prochain intervenant, et non dans le journal d'une exécution terminée. Y compris la séparation
  entre liste interne et feuille de route publique, l'enrichissement plutôt que la duplication, et ce qui
  est fait avec le commit.

### 1.2.0 (2026-07-24)
- Le contrôle de confidentialité recherche en outre les noms des propres espaces internes. Ce ne sont pas
  des secrets, ils ne déclenchent donc aucune alerte et passent à travers un contrôle qui ne vise que les
  chemins et les jetons — tout en restant incompréhensibles pour le lecteur et en révélant la structure interne.

### 1.1.0 (2026-07-24)
- Les verrous sont lus au lieu d'être traités comme une interdiction générale : un verrou purement de
  publication / de push fait basculer la ronde sur une branche locale au lieu de l'interrompre. Précision
  supplémentaire : sous un tel verrou, les métadonnées, releases et actions sur issues/PR tombent également —
  elles sont aussi visibles à distance qu'un push.

### 1.0.0 (2026-07-24)
- Version initiale. Niveau 1 de l'entretien de dépôt, dérivé de `github-repo-care`.
