---
name: grilling
description: "Soumettez l'utilisateur à un interrogatoire implacable au sujet d'un plan, d'une décision ou d'une idée. À utiliser lorsque l'utilisateur souhaite mettre à l'épreuve sa réflexion, ou lorsqu'il emploie une formule déclenchante de type « grill » — y compris des formules françaises comme « cuisine-moi », « cuisine-moi sur ce plan » ou « démonte mon plan en mode gril », ainsi que des formules allemandes comme « grill mich », « grill mich zu diesem Plan » ou « zerpflück meinen Plan im Grill-Modus ». Point d'entrée pour la commande /grill-me ; peut aussi être invoqué directement."
third_party: true
license: MIT
upstream: https://github.com/mattpocock/skills
category: utilities
language: fr
translated_from_sha256: 7f0fe16de62ea366d79b723cbf52cd65c3f237415352cfa870ba0b12cf4fef53
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
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

<!--
Vendored from mattpocock/skills (skills/productivity/grilling/SKILL.md, MIT
License, Copyright (c) 2026 Matt Pocock -- see LICENSE next to this file).

Modification vs. upstream: the `description` field was extended with German
trigger phrases ("grill mich"). The `category` and `language` fields and this
comment were added; all are local convention (recommended, not one of the
nine house fields), not upstream content, and `language: en` reflects that
the vendored body is unmodified English. The body (the design tree / frontier
/ rounds method) is unchanged from upstream.

Adopted 2026-08-24 per Ticket T-20260824-594031458 alongside skills/third-
party/grill-me/ (the thin, explicit-only entry point that calls this skill).
-->
