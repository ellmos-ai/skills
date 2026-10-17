---
name: repo-publish-check
description: "Examen neutre des dépôts (repositories) avant une publication ou lors d'un nouvel examen public. Vérifie la confidentialité, les secrets, les licences, les contenus tiers, la documentation et le statut d'autorisation de publication, sans effectuer la publication elle-même."
version: 1.6.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-09-27
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [release, privacy, license, repository, publication]
language: fr
status: active
visibility: public
dependencies:
  tools: [git, gh]
  services: []
  protocols: []
  python: []
translated_from_sha256: b96efd5a0ae9aa276c3f093eea2f4e712f485ab59d30cc9196d3277224b6f1a2
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T22:17:49.701000+00:00"
---
<img src="banner.png" width="100%" alt="repo-publish-check banner">

# Repo Publish Check

## Objectif

Examine un dépôt avant la première publication ou lors d'un contrôle ultérieur. Un résultat négatif est admissible. Ne modifie la visibilité qu'une fois que le propriétaire du dépôt l'a expressément autorisé.

Le skill ne produit pas d'avis juridiques. En cas de domaine juridiquement sensible ou de cas particulier peu clair, le skill public `law-checker` est consulté. Même dans ce cas, il ne remplace pas un conseil juridique professionnel.

## Confidentialité des rapports d'examen

Les rapports d'examen et les évaluations des risques ne sont pas committés dans le dépôt examiné. Place-les dans un espace d'examen privé, séparé du projet, ou utilise un dossier ignoré par git, tel que `<private-review-dir>`.
Seules les corrections nécessaires sont rendues publiques, par exemple une mention de licence, une note sur la protection des données ou une description plus précise.

## Déroulement de l'examen

1. **Définir le périmètre de publication**
   - Examine l'arborescence réellement suivie par git avec `git ls-files`.
   - Exclus les notes internes, les rapports, les données de test, les configurations locales et les fichiers de verrouillage.
   - Examine `.gitignore` et les listes d'autorisation des paquets avant le commit.
   - Pour les bibliothèques de skills (présence de fichiers `SKILL*.md`) : chaque frontmatter doit pouvoir être analysé comme YAML. Si `testing/skill_frontmatter_gate.py` existe dans le dépôt, exécute-le (`--fix` ajoute mécaniquement les guillemets sans modifier le libellé) ; sinon, effectue un contrôle par sondage avec `yaml.safe_load`.

2. **Analyse de confidentialité et de secrets**
   - Recherche dans l'arbre de travail ET dans tout l'historique Git accessible (`git log -p --all`) les adresses e-mail, identifiants, jetons, clés privées, chemins d'utilisateurs locaux (`C:\Users\<name>`, `_Local_DEV`, `OneDrive`, `CREDENTIALS`) et données personnelles.
   - Charge impérativement les motifs de recherche depuis un fichier (`grep -f`), jamais sous forme de chaînes en ligne sujettes aux erreurs ; effectue au préalable un contrôle positif avec un chemin de test.
   - Classe chaque résultat comme intentionnel, à supprimer ou comme risque résiduel documenté.
   - Nettoie le contenu historique problématique avant la publication : un résultat dans l'historique n'est JAMAIS corrigé par un simple commit de nettoyage ; il exige une réécriture de l'historique (`git filter-repo`) ou une recréation du dépôt ou l'accord de l'utilisateur.

3. **Licence et provenance**
   - Un fichier `LICENSE` approprié doit être présent.
   - Documente si la licence couvre le code, les prompts, la documentation et les médias.
   - Inventorie les composants tiers et les contenus repris, avec leur provenance et leur licence.
   - Ne publie des éléments tiers que si la licence et la décision éditoriale de publication le permettent.

4. **Objectif et domaines sensibles**
   - Décris clairement ce que le projet fait et ce qu'il ne fait pas.
   - Pour le droit, la santé, les finances, la sécurité ou les données personnelles : documente les limites, les flux de données et les usages exclus.
   - Pour les questions juridiques, obtiens une première évaluation actuelle via `law-checker`.

5. **Protection des données et utilisation du cloud**
   - Réduis au minimum les données traitées.
   - Signale les services externes et le traitement dans le cloud.
   - Invite les utilisateurs à ne pas publier de données de dossiers confidentiels dans des tickets ou discussions publics.

6. **Remarques sur l'IA et le produit**
   - En cas de lien avec l'IA, documente la finalité, le rôle du fournisseur, les limites essentielles et les avis de transparence pertinents.
   - N'affirme aucune homologation, certification ou qualité d'examen qui ne soit pas démontrée.

7. **Nom, bannière et présentation externe**
   - Vérifie le slug et les noms de paquets ainsi que d'éventuels chevauchements de marques.
   - Une simple recherche sur le web ou sur une plateforme ne remplace pas une recherche officielle de marques.
   - Le README, la description et les badges doivent refléter l'étendue réelle des fonctions.
   - **Contrôle obligatoire de la bannière avant passage en public :**
     * Vérifie si une bannière existe déjà (`assets/banner*` ou à la racine `banner.*`) et si elle est intégrée dans le `README.md`.
     * Si la bannière manque : génération obligatoire AVANT la publication !
     * Voie de génération : Antigravity / Gemini (`generate_image` ou CLI agy — règle standard : bannière/visuel via agy ; par défaut), voie de remplacement : Codex.
     * Stockage sous `assets/banner.png` (resp. `banner.svg`) ; vérifie directement sur le disque l'existence et la taille du fichier (ne te fie pas uniquement au message de réussite du modèle).
     * Intègre la bannière en haut (centrée) dans le `README.md`.

8. **Clôture et contrôle visuel**
   - Ouvre activement la bannière, le logo et les vues web (comme la page d'accueil du dépôt ou le profil de l'organisation) à l'utilisateur pour contrôle visuel (`Invoke-Item` resp. `Start-Process msedge`) ; ne les laisse pas uniquement en lien dans le rapport.
   - Documente les résultats, corrections, risques ouverts et un résultat par feux tricolores dans le rapport d'examen privé.
   - Vérifie à nouveau le commit final.
   - Obtiens l'accord explicite du propriétaire du dépôt.
   - Ce n'est qu'ensuite qu'une étape distincte et autorisée peut modifier la visibilité en public (`gh repo edit <org>/<repo> --visibility public`).

## Données d'exemple et de preuve (numéros de téléphone, transcriptions, identifiants) [C 2026-09-05]

Les preuves issues d'essais sur le terrain et de tests sont la voie la plus fréquente par laquelle de vraies données arrivent dans un dépôt public, bien plus que les identifiants. Contrôle-les dans le code, les tests, les fixtures, la documentation **et l'historique Git accessible** :

- **Numéros de téléphone :** uniquement les plages fictives ou de démonstration réservées par la norme du pays concerné (DE : réservations de la Bundesnetzagentur ; aucun bloc mobile ou fixe plausible). Analyse par regex avec **contrôle positif** (un numéro d'exemple inséré doit être trouvé par l'analyse), faute de quoi un résultat négatif n'a aucune valeur. Les formes masquées (`+49 17x XXXX`, `+491 ••• •`) sont admissibles.
- **Transcriptions et extraits de conversations :** uniquement sous forme de reproductions synthétiques clairement signalées ; pas de transcriptions brutes, pas de noms, pas d'horodatages exacts, pas de fragments de numéros.
- **Identifiants des fournisseurs :** pas d'identifiants de run, d'appel ou de commande (motif hexadécimal de 32 caractères), pas de liens vers des tableaux de bord.
- **Historique :** si de tels éléments ont jamais été committés, un commit de nettoyage ne suffit pas : il faut une réécriture (`git filter-repo`) et une purge auprès du support des objets orphelins (dangling). Vérifie ensuite que les anciennes URL de commit renvoient bien une erreur 404 en ligne. Rapporte le résultat sans les valeurs (fichier, ligne, compteur).

Niveaux de résultat comme pour l'analyse des identifiants : *bloqué* (découverte réelle) · *à examiner* (suspect, éventuellement un exemple) · *propre*. Cas d'école : CALL-E 2026-08-24/25 (la revue par le mainteneur a imposé trois réécritures de l'historique).

## Étapes obligatoires après le passage en public

Dès que la visibilité d'un dépôt a été réglée sur `public` (`gh repo edit <org>/<repo> --visibility public`), les étapes obligatoires suivantes doivent être effectuées :

1. **Vérifier que la bannière est complète dans la version ou le commit final :**
   - Contrôle sur GitHub que la bannière se charge correctement dans le README (pas de 404, chemin de branche ou d'asset accessible).

2. **Mettre à jour le README du profil de l'organisation (bannière + entrée dans le répertoire) :**
   - Chaque dépôt nouvellement publié avec bannière doit être répertorié sur la page de profil de l'organisation (`<org>/.github/profile/README.md` et `profile/README_de.md`).
   - Contrôle mécanique via la porte de contrôle du profil d'organisation :
     ```bash
     python testing/org_profile_gate.py --org <org>
     ```
   - Si l'entrée manque, le script génère un extrait HTML/Markdown adapté. Insère-le dans la galerie de bannières de la catégorie correspondante (par ex. applications métier, modules, orchestration) et ajoute le dépôt au tableau correspondant des README de profil.
   - Soumets la modification via une branche et une Pull Request vers `<org>/.github` (voir aussi `github-repo-care`, étape 14).

3. **Mettre sa propre étoile :**
   - Après la publication, pour chaque dépôt public personnel, vérifie si le compte a déjà mis une étoile et pose-la le cas échéant (par ex. via `.GITHUBBOT` `run.py --self-star --repo <org>/<name>` ou `gh api`). Détails : voir `github-repo-care`, étape 14.

## Nouvel examen de dépôts déjà publics

Vérifie au minimum la confidentialité et les secrets, la couverture de licence, les contenus tiers, les avertissements (disclaimers) et la présentation externe. Les découvertes critiques dans l'historique sont immédiatement signalées au propriétaire du dépôt et ne sont pas écrasées silencieusement.

Une organisation peut tenir sa propre file d'attente privée et son stockage de rapports. Ceux-ci n'ont pas leur place dans le skill public. Les examens en retard peuvent être priorisés selon le risque, la visibilité et l'âge du dernier rapport d'examen privé.

## Format des résultats

```markdown
# Veröffentlichungsprüfung — <Repository>
- Stand: <Commit>
- Modus: vor Veröffentlichung | Nachprüfung
- Privacy/Secrets: grün | gelb | rot
- Lizenz/Drittinhalte: grün | gelb | rot
- Dokumentation/Außendarstellung: grün | gelb | rot
- Korrekturen: <Liste>
- Offene Risiken: <Liste>
- Freigabe: ausstehend | erteilt
```

## Limites

- Le skill ne publie rien par lui-même.
- Il ne remplace ni un conseil juridique ni une recherche officielle de marques.
- Un scan de code source sans résultat ne prouve pas que d'anciennes copies publiques, registres de paquets ou caches ont été nettoyés.

## Journal des modifications

Détails dans [CHANGELOG.md](CHANGELOG.md).
