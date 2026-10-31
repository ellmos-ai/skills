---
name: build-your-users-mind
version: 1.0.0
type: skill
author: ellmos contributors
created: 2026-07-30
updated: 2026-07-30
description: "Renvoie au module public et neutre vis-à-vis des fournisseurs build-your-users-mind : une procédure respectueuse de la vie privée permettant de construire un modèle empirique de théorie de l'esprit (Theory of Mind) des préférences d'un utilisateur autorisé, à partir de ses propres journaux d'interaction. À utiliser lorsqu'une personne responsable souhaite créer, valider, connecter ou maintenir un profil d'avatar décisionnel, sans publier le profil personnel ni ses justificatifs."
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [theory-of-mind, user-model, decision-avatar, feedback, privacy, pointer-skill]
language: fr
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "external"
  origin_path: "SKILL.md, templates/, scripts/, schemas/, TAXONOMY.md"
  origin_version: "1.0.0"
  origin_repo: "https://github.com/ellmos-ai/build-your-users-mind"
  last_sync_from_origin: "2026-07-30"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 50187ac74941737bc5831d58dafc99f662904adaa573192e2a0a4ae8841bc607
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T15:41:56.704466+00:00"
---
<img src="banner.png" width="100%" alt="build-your-users-mind banner">

# build-your-users-mind — renvoi public et neutre vis-à-vis des fournisseurs

Cette compétence est un renvoi allégé vers le module public
[`ellmos-ai/build-your-users-mind`](https://github.com/ellmos-ai/build-your-users-mind).
Le module contient la procédure complète, les modèles, les schémas, les scripts, les tests
et la documentation des adaptateurs de sources. Ce catalogue ne duplique pas
le code.

## Ce que fait le module

Avec l'autorisation explicite de la personne responsable, le module aide un
agent à :

1. extraire, à partir des journaux d'interaction de l'utilisateur, les contributions authentiques rédigées par celui-ci ;
2. caviarder les contenus sensibles avant tout stockage durable ;
3. réduire et classifier les preuves relatives aux préférences et décisions récurrentes ;
4. construire un modèle local de préférences assorti de niveaux de confiance et de traces de provenance ;
5. intégrer un bref renvoi dans l'environnement d'exécution d'agent choisi ; et
6. calibrer les prédictions à partir de retours réels ultérieurs.

Le module public est une procédure destinée à tout utilisateur et aux environnements d'exécution d'agents pris en charge. Il ne contient aucun modèle d'une personne déterminée.

## Frontière de sécurité et de confidentialité

- Avant de lire les journaux d'interaction, l'autorisation de la personne responsable est requise.
- Les profils personnels, les journaux bruts, les corpus de preuves et les chemins locaux restent privés.
- Les prédictions sont des hypothèses incertaines, et non une lecture des pensées, un diagnostic ni des déclarations de l'utilisateur.
- Une prédiction de préférence n'étend jamais les pouvoirs de l'agent.
- Les actions externes, irréversibles, critiques pour la sécurité, juridiques, médicales, professionnelles, financières ou de conséquences comparables nécessitent une confirmation explicite.
- Les prédictions produites par l'agent ne doivent jamais devenir des preuves primaires concernant l'utilisateur.

## Installation

```bash
git clone https://github.com/ellmos-ai/build-your-users-mind.git <clone-path>
```

Suivre les fichiers actuels `README.md`, `SKILL.md`,
`SOURCE-ADAPTERS.md` ainsi que les consignes de confidentialité du module. Conserver le
profil utilisateur généré en dehors des dépôts publics. Pour l'implémentation et le
versionnage, le dépôt du module fait foi.

## Noyau public et profils privés

`build-your-users-mind` est le nom public et neutre du module.
`decision-avatar` est le protocole d'exécution public de ce catalogue. L'avatar
d'une personne nommée, les fichiers de preuves, les commandes locales et
les consignes propres à un profil sont des extensions privées et ne doivent pas être publiés sous
un nom de compétence personnel.

## Journal des modifications

### 1.0.0 (2026-07-30)

- Ajout d'un renvoi neutre vers le module public autonome.
- Remplacement du profil d'avatar personnel précédemment publié par une frontière stricte
  entre noyau public et profil privé.
