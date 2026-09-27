---
language: fr
description: Retirer les artefacts d'IA, les résidus de conversation, les espaces réservés et les tics de style LLM des textes finalisés, et auditer les mentions de divulgation d'IA.
---

<img src="banner.png" width="100%" alt="llm-text-hygiene banner">

> **Français** — Version française officielle de `llm-text-hygiene`.

# LLM-Text-Hygiene — Retirer les résidus d'IA des textes finalisés

## Présentation et objectif

Les textes produits avec l'aide de l'IA accumulent des résidus qui restent invisibles au brouillon et ne deviennent gênants que dans le document publié : bribes de conversation issues de la session de chat, indications de mise en scène qui sortent de la structure argumentative, remerciements adressés au modèle de langage, espaces réservés oubliés, tics de style LLM envahissants — et une divulgation d'IA absente, mal placée ou qui n'est plus exacte. Cette compétence est la passe de nettoyage systématique avant publication : vérifier, nettoyer avec prudence, corriger la divulgation. **Elle ne modifie jamais le fond** — elle retire ce qui n'appartient pas à l'œuvre.

## Catalogue de vérification

Cinq classes de constats, du plus évident (corriger directement) au plus délicat (seulement signaler) :

### 1. Résidus de conversation et indications de mise en scène (évident → supprimer/corriger)

Phrases qui appartiennent à la GENÈSE du texte, pas au texte lui-même : « Comme convenu, nous gardons ce passage dans l'article, car… », « Voici la section révisée : », « Je rajoute volontiers… », fragments de prompt oubliés, commentaires méta adressés au commanditaire.
**Principe de détection :** la phrase sort de la structure textuelle et argumentative — elle s'adresse à une situation de conversation plutôt qu'au lecteur. Avant de supprimer, vérifier si un élément de fond doit être sauvé (transférer la justification en note de bas de page/dans le texte).

### 2. Espaces réservés et marqueurs de chantier (évident → résoudre)

`[TODO : …]`, `[insérer référence]`, `XXX`, `<exemple ici>`, sections vides avec titre, « (source ?) ». Les résoudre ou — si impossible — les transférer comme véritable tâche ouverte dans le TODO du projet et les retirer du livrable.

### 3. Remerciements au LLM et anthropomorphisme (évident → supprimer)

Les remerciements adressés à ChatGPT/Claude/Gemini & Cie n'ont pas leur place dans les remerciements — on ne remercie pas des outils, leur usage se déclare dans la divulgation d'IA. À supprimer également : les formulations anthropomorphiques sur l'outil (« l'IA a gentiment suggéré »).

### 4. Divulgation d'IA (vérifier → corriger)

- **Présente ?** Si le document a été produit avec l'aide de l'IA et que la venue/le projet exige ou prévoit une divulgation : la section existe-t-elle ?
- **Correcte ?** Décrit-elle l'usage réel (ni sous-estimé, ni exagéré) ? Utilise-t-elle le schéma de divulgation du projet/de la venue s'il en existe un (p. ex. niveaux échelonnés) ?
- **Bien placée ?** À l'endroit habituel de la venue (zone méthodes/remerciements, section dédiée), identique dans toutes les versions linguistiques.

### 5. Tics de style LLM (délicat → ne corriger que les cas clairs, signaler le reste)

Transitions toutes faites (« En résumé, on peut dire que », « Il est important de souligner que »), inflation de listes à puces là où un texte suivi conviendrait, chaînes « non seulement… mais aussi », densité de tirets, formules d'atténuation, et en anglais les marqueurs bien connus (notamment « delve », « tapestry », « it's worth noting »). **Attention :** le style appartient à l'auteur — ne lisser que les formules sans ambiguïté, présenter tout le reste comme une liste de constats à l'auteur plutôt que de réécrire le texte. Un texte qui sonne humain n'est pas l'objectif de cette compétence ; l'objectif est un texte sans corps étrangers.

## Déroulement

1. **Clarifier le périmètre :** quels livrables (fichiers), quelles versions linguistiques ? Appliquer les changements TOUJOURS de façon synchrone sur toutes les versions (recoupement : `bilingual-doc-sync`).
2. **Scan mécanique :** recherche plein texte selon les motifs signal (tableau ci-dessous) — peu coûteux, trouve fiablement les classes 2/3 et une partie de la classe 1.
3. **Passe de lecture :** lire le document le long de la structure argumentative — les constats de classe 1 ne se reconnaissent que structurellement (la phrase s'adresse à une conversation plutôt qu'au lecteur). Vérifier particulièrement : débuts/fins de sections, remerciements, introduction/conclusion (c'est là que le résidu atterrit en premier).
4. **Nettoyer :** corriger directement les classes 1–3 (avec prudence, en préservant le fond), corriger la classe 4, restituer la classe 5 sous forme de liste de constats ; ne lisser directement que les cas sans ambiguïté.
5. **Documenter :** consigner ce qui a été trouvé/modifié/seulement signalé — pour les articles soumis à obligation de versionnage, noter si une nouvelle version/un nouveau dépôt est nécessaire.
6. **Passe périodique sur un ensemble :** combiner avec `rotation-check` (un document/projet par passe, le registre comme mémoire).

**Outil optionnel pour la classe 5 et la divulgation d'IA :** sur demande expresse de
l'utilisateur — jamais automatiquement — [`pasta-press`](https://github.com/ellmos-ai/pasta-press)
(dépôt public, 100 % local via Ollama) peut être utilisé pour le raffinement stylistique :
`pastapress process <fichier>` ou `pastapress text "…"`. Limite tirée des signaux
d'alerte ci-dessus : cette compétence ne polit pas elle-même le style — pasta-press ne
remplace pas la passe de lecture, et le nettoyage des marqueurs (classes 1–4) reste une
décision de vérification propre à cette compétence, que pasta-press soit utilisé ou non.

## Motifs signal pour le scan mécanique

| Classe | Motif de recherche (DE) | Motif de recherche (EN) |
| --- | --- | --- |
| Résidu de conversation | « wie besprochen », « wie gewünscht », « hier ist », « gerne », « im Chat », « wie du sagtest », « lassen wir » | "as discussed", "as requested", "here is the", "I have added", "per your" |
| Espaces réservés | `TODO`, `XXX`, `[…einfügen]`, `<…>`, « Quelle? » | `TBD`, `[insert`, `placeholder`, `citation needed` |
| Remerciement LLM | « Dank an ChatGPT/Claude/Gemini », « mithilfe von KI erstellt » (hors divulgation) | "thanks to ChatGPT/Claude", "grateful to the AI" |
| Marqueurs de style | « zusammenfassend lässt sich », « es ist wichtig zu betonen », « nicht nur … sondern auch » | "delve", "tapestry", "it's worth noting", "in conclusion" |

Le tableau est un point de départ, pas un substitut de filtre : les motifs livrent des candidats, la décision se prend en contexte (étapes 3–4). Pour l'hygiène purement mécanique des caractères (scan d'émojis, caractères de contrôle, umlauts cassés), utiliser les outils existants — les dégâts d'encodage relèvent d'`encoding-fix`, pas de cette compétence.

## Exemple et application

```text
Demande : « Vérifie l'article avant le dépôt pour d'éventuels résidus d'IA. »

1. Périmètre : paper_de.tex + paper_en.tex.
2. Scan : 1× "as discussed" (EN, section 4), 1× "[TODO: insérer référence Smith]" (les deux),
   les remerciements mentionnent « l'aide précieuse de Claude ».
3. Passe de lecture : dans l'introduction, une phrase s'adresse directement au relecteur
   (« Nous traitons cette objection comme demandé en 3.2 ») → indication de mise en scène.
4. Corrections : indication de mise en scène supprimée (le contenu figurait déjà en 3.2),
   TODO transféré comme tâche dans TODO.md + espace réservé retiré, remerciement LLM
   supprimé, section de divulgation d'IA précisée sur l'usage réel — le tout en DE et EN.
5. Note : changement de fond → nouvelle version de l'article nécessaire, consigné dans TODO.md.
```

## Signaux d'alerte

| Pensée | Réalité |
| --- | --- |
| « Je vais rendre le texte plus fluide tant que j'y suis » | Le fond et la voix appartiennent à l'auteur — la compétence retire les corps étrangers, elle ne polit pas le style. |
| « Marqueur de style trouvé → supprimer » | La classe 5 est signalée, pas réécrite automatiquement ; ne lisser que les formules sans ambiguïté. |
| « La version allemande suffit » | Le résidu ne se trouve souvent que dans UNE seule version — toujours vérifier toutes les versions linguistiques et les garder synchronisées. |
| « Retirer la divulgation, et c'est propre » | À l'envers : retirer les remerciements au LLM, INSÉRER une divulgation correcte — dissimuler n'est pas de l'hygiène. |

## Compétences et outils associés

- `encoding-fix` — Réparation d'octets/d'encodage (mojibake) ; cette compétence-ci travaille au niveau du contenu.
- `bilingual-doc-sync` — Maintien de la synchronisation des versions linguistiques dans lesquelles les corrections sont intégrées.
- `rotation-check` — Charpente pour la passe périodique sur un ensemble de documents.
- `textproduction` — Génération de texte (cette compétence en est le contrôle qualité en aval).
- [`pasta-press`](https://github.com/ellmos-ai/pasta-press) — outil externe et public (pas
  une compétence de cette bibliothèque) : presse à texte IA locale via Ollama pour le
  raffinement stylistique, la traduction et le retrait de marqueurs. Optionnel pour la
  classe 5, uniquement sur demande de l'utilisateur — cette compétence ne polit pas
  elle-même le style (voir Signaux d'alerte et Déroulement).

## Journal des modifications

### 1.1.0 (2026-09-27)
- Ajout de `pasta-press` (dépôt public `ellmos-ai/pasta-press`) comme outil optionnel
  pour la classe 5 (tics de style) et le raffinement de la divulgation d'IA — uniquement
  sur demande de l'utilisateur, le nettoyage des marqueurs reste une décision de
  vérification propre à cette compétence. « Compétences associées » étendu à
  « Compétences et outils associés ». Les sept versions linguistiques ont été mises à
  jour de façon synchrone ; `SKILL.fr.md` s'est révélé être en réalité du texte allemand
  non traduit sous une couverture française — retraduit ici en français véritable.

### 1.0.0 (2026-07-04)
- Version initiale. Extraite de l'automatisation Codex « research-llm-muster-check »
  (fragments de conversation dans les articles, remerciements au LLM, divulgation d'IA)
  et généralisée à des textes livrables quelconques ; catalogue de vérification étendu
  aux espaces réservés, aux tics de style et au tableau de motifs signal.
