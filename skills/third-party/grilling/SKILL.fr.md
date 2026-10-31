---
name: grilling
description: "Interrogez l'utilisateur sans relâche au sujet d'un plan, d'une décision ou d'une idée. Utilisez ce skill lorsque l'utilisateur souhaite mettre sa réflexion à l'épreuve, dit « grill me » ou « grill-me » (l'ancienne commande /grill-me a été remplacée par /grilling), ou emploie une autre formule déclenchante de type « grill », notamment les expressions françaises « cuisine-moi », « cuisine-moi sur ce plan » et « démonte mon plan en mode gril », ainsi que les expressions allemandes « grill mich », « grill mich zu diesem Plan » et « zerpflück meinen Plan im Grill-Modus ». Utilisez-le aussi à la fin d'une session de planification si l'utilisateur demande s'il reste des points ouverts."
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: fr
translated_from_sha256: 5d1b8c01ac7dc1437fe7c47e90506f755b22bdd9df0555a5f556e96921337a3b
translator: "claude-haiku-5-5 + Codex GPT-6 (Luna)"
translated_at: "2026-10-25T11:15:53+00:00"
---
<img src="banner.png" width="100%" alt="grilling banner">

Interrogez l'utilisateur sans relâche jusqu'à atteindre une compréhension partagée. Représentez ceci comme un **arbre de conception** : chaque décision se ramifie en décisions qui en dépendent.

Parcourez l'arbre par **tours**. La **frontière** est constituée de toutes les décisions dont les prérequis sont déjà réglés : les questions que vous pouvez poser _maintenant_ sans deviner des réponses que vous n'avez pas encore entendues. Posez toute la frontière en un seul tour : numérotez chaque question et donnez votre réponse recommandée. Attendez ensuite les réponses de l'utilisateur avant le tour suivant.

Mettez en forme un tour ainsi :

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```


Chaque réponse de l'utilisateur remodèle l'arbre : les décisions réglées repoussent la frontière et débloquent les questions qui en dépendaient. Recalculez la frontière et posez le tour suivant. Une question dont la réponse dépend d'une autre question encore ouverte dans ce tour appartient à un tour _ultérieur_, et non à celui-ci.

La recherche de _faits_ vous incombe, jamais à l'utilisateur. Lorsqu'une question de la frontière nécessite un fait issu de l'environnement (système de fichiers, outils, etc.), lancez un sous-agent pour le trouver ; ne demandez rien que vous pouvez vous-même rechercher. Ne bloquez pas sur ce point : une exploration en cours est un prérequis non réglé, donc seules les questions en aval attendent le rapport du sous-agent ; posez le reste de la frontière immédiatement. Les _décisions_ appartiennent à l'utilisateur : soumettez-les-lui et attendez.

La session est terminée lorsque la frontière est vide : chaque branche de l'arbre de conception a été visitée, et rien n'est resté silencieusement supposé. N'agissez pas tant que l'utilisateur n'a pas confirmé que vous êtes parvenus à une compréhension partagée.

## Ajouts locaux

Ces règles complètent la méthode d'origine sans la modifier.

1. **Partez de ce qui est déjà écrit.** Avant le premier tour, lisez le plan et l'endroit où le projet consigne ses décisions. Relevez tous les points encore ouverts, proposés ou non confirmés. Ne reposez pas une question déjà tranchée : citez plutôt la décision consignée.
2. **Consignez chaque réponse avant le tour suivant.** Inscrivez chaque réponse dans le registre des décisions du projet comme étant décidée, avec sa date et sa source. Une réponse présente uniquement dans le chat se perd à la prochaine réinitialisation du contexte.
3. **Faites une pause, sans recommencer, en cas d'interruption.** Si l'utilisateur demande d'abord autre chose, faites-le puis reprenez à partir des questions encore ouvertes. Les points réglés le restent.
4. **Appuyez chaque recommandation sur une seule raison.** Donnez la réponse recommandée et l'unique fait ou règle qui la fonde. Une recommandation ne devient une décision qu'après confirmation de l'utilisateur.
5. **Montrez les faits vérifiés.** Lorsqu'une question dépend d'un fait recherché dans l'environnement, indiquez le résultat et sa source pour que l'utilisateur décide à partir des éléments disponibles.
6. **Posez les questions dans la langue de l'utilisateur.** Formulez questions et recommandations dans sa langue ; les identifiants restent inchangés.
7. **Terminez par un relevé.** Lorsque la frontière est vide, listez ce qui a été décidé et ce qui a été laissé ouvert délibérément, puis demandez confirmation de la compréhension partagée.

<!--
Vendored from mattpocock/skills (skills/productivity/grilling/SKILL.md, MIT
License, Copyright (c) 2026 Matt Pocock -- see LICENSE next to this file).

Improved fork. Modifications vs. upstream:
- `description`: German trigger phrases ("grill mich"), the "grill me" /
  "grill-me" phrases, and the end-of-planning trigger were added.
- `category`, `language` and this comment were added (local convention).
- "Local additions" (rules 1-7) were appended after the upstream body. The
  upstream body above that heading is unchanged, so a resync only needs to
  replace that part.

Adopted 2026-08-24 per Ticket T-20260824-594031458, together with the thin
entry point skills/third-party/grill-me/ (upstream
skills/productivity/grill-me, `disable-model-invocation: true`, body
"Call the Skill tool with grilling"). On 2026-10-25 grill-me was removed at
the user's request: one skill instead of two, the phrase triggers moved into
this description. The native /grill-me command no longer exists; /grilling
replaces it. The description only adds semantic matching and registers no
alias command. Rules 1-7 come from a planning session of the same day.
-->
