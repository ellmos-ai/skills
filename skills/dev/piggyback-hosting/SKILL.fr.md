---
name: piggyback-hosting
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-02
updated: 2026-08-07
description: "Modèle d'hébergement permettant d'héberger de manière sûre une application construite localement (base de données propre, clé API propre, état en processus) sans développer de gestion des utilisateurs. Principe central : l'hôte ne stocke rien, le navigateur du visiteur stocke tout ; ainsi, les comptes par visiteur, les contrôles d'accès et les délais de suppression deviennent sans objet au lieu d'avoir à être résolus. À utiliser lorsqu'une application construite localement doit être hébergée pour plusieurs visiteurs, pour « rends-le hébergeable sans connexion », « ne pas construire de comptes utilisateurs », « réduire la politique de confidentialité d'un outil hébergé », « qui est responsable si nous ne stockons rien », ou lors du choix ou de la mise en œuvre d'un mode serveur (`local`, `huckepack-gift`, `huckepack-only-host`, `pay-membership`). Fournit en référence un modèle de plan de flux de données, un modèle de politique de confidentialité et une évaluation juridique préliminaire (RGPD/TDDDG/UWG, allemand)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: dev
tags: [hosting, privacy, gdpr, dsgvo, byok, client-side-storage, deployment, no-login]
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
translated_from_sha256: e4e1a66b0d6e62ff17a5a883b8eef0ca1f59b984e64d8d29030b76b4ffbcebda
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:43.826638+00:00"
---
<img src="banner.png" width="100%" alt="piggyback-hosting banner">

# piggyback-hosting

**Un modèle d'hébergement pour les applications qui, par conception, n'acceptent jamais les données d'autrui.**

> Schéma directeur établi le 2026-08-02 lors de la construction de trois agents d'appel.
> Réutilisable pour toute application conçue pour un seul utilisateur local, mais qui doit aussi pouvoir être hébergée pour d'autres.

## À propos du nom

En anglais, ce modèle s'appelle **piggyback** — « voyager sur l'infrastructure d'autrui » y est déjà le terme technique consacré. Le texte anglais de ce skill utilise donc *piggyback* ; **« huckepack » est le titre de travail allemand** sous lequel le modèle a été construit, et aussi le nom du dépôt à partir duquel ce skill a été migré. **Les valeurs de mode littérales restent `huckepack-gift` et `huckepack-only-host`** — ce sont celles qui sont livrées dans le code et la configuration, écrites exactement ainsi, quelle que soit la langue du texte environnant.

## Le problème

Une application est construite localement : une base de données, une clé API, un état qui vit dans le processus. Sur sa propre machine, c'est tout à fait correct. Dès qu'on l'héberge pour d'autres, chacune de ces trois hypothèses devient un bogue — chaque visiteur partage le même état, la même base de données, la même clé. Quiconque ouvre la page voit les données de tous les autres.

La solution habituelle consiste à gérer les utilisateurs : comptes, connexion, contrôles d'accès, délais de suppression, politique de confidentialité, contrat de sous-traitance. Il s'agit souvent d'un chantier plus important que l'application elle-même.

## L'idée

**Le visiteur conserve tout sur son propre appareil. L'hôte ne conserve rien.**

Cela ne résout pas la gestion des utilisateurs — cela la rend **sans objet**. Là où aucune donnée étrangère ne se trouve sur le serveur, il n'y a rien à isoler entre visiteurs, rien à supprimer selon un calendrier, et la politique de confidentialité se réduit à ce que le service fait réellement.

## Les trois modes

| Mode | Clé API | Données | Gestion des utilisateurs |
|---|---|---|---|
| **`huckepack-gift`** | fournie par l'hôte | sur l'appareil du visiteur | aucune |
| **`huckepack-only-host`** | fournie par le visiteur | sur l'appareil du visiteur | aucune |
| **`pay-membership`** | celle de l'hôte, facturée | serveur | requise |

- **`huckepack-gift`** — l'hôte fournit sa propre clé et offre l'exécution. Une invitation sans friction à essayer l'outil.
- **`huckepack-only-host`** — le visiteur apporte sa propre clé. L'hôte ne paie rien et ne stocke rien.
- **`pay-membership`** — volontairement laissé à l'état de stub. Ici, tout ce que les deux autres évitent redevient nécessaire : comptes, facturation, stockage côté serveur. Un chantier à part entière, pas un interrupteur à basculer.

Il existe toujours un **`local`** par défaut : qui ne configure rien obtient l'application exactement telle qu'elle fonctionnait auparavant, sur sa propre machine.

## Les briques

| Brique | Rôle |
|---|---|
| Mode défini comme réglage au moment de l'installation | une propriété du déploiement, non de la session |
| Couche de stockage interchangeable | la même base de données, un autre emplacement |
| SQLite dans le navigateur (WASM + OPFS) | même schéma, mêmes requêtes, autre lieu d'exécution |
| Champ de clé masqué | uniquement en mode `only-host`, jamais journalisé |
| Export et import | **non optionnels** — les données du navigateur sont volatiles |
| Reçu sous forme de fichier téléchargeable, dossier de destination au choix | aucun serveur impliqué dans la livraison |

L'effort d'ingénierie proprement dit consiste à rendre la couche de stockage interchangeable : l'application écrit de toute façon dans SQLite, mais une couche intermédiaire décide si cette écriture aboutit sur le serveur ou dans le navigateur du visiteur (`sql.js` / la version officielle WASM de SQLite, persistée via l'Origin Private File System). Si WASM s'avère trop lourd, hiérarchiser les options de stockage navigateur par poids : SQLite-WASM + OPFS (une vraie base de données, capacité maximale) > IndexedDB (structuré, modèle de requêtes propre) > `localStorage` (adapté uniquement aux petites choses comme la langue et le thème).

## Ce que ce modèle ne résout pas — dit franchement

- **Des données de navigateur effacées signifient que tout est perdu.** Il n'existe aucune copie côté serveur. C'est pourquoi l'export est une condition, non un simple confort.
- **Pas de changement d'appareil** sans export et import.
- **La clé vivant dans le navigateur** (`only-host`) est moins protégée que celle d'un serveur. Elle appartient cependant au visiteur, et l'alternative consisterait à la confier à l'hôte — ce qui n'est pas évidemment le choix le plus sûr.
- **L'exécution passe toujours par l'hôte.** Pour les services qui atteignent un tiers — par exemple un appel téléphonique — l'hôte traite les données de ce tiers indépendamment de l'endroit où se trouvent les propres enregistrements du visiteur. Une politique de confidentialité n'en devient donc pas superflue, seulement plus courte.

## Ce qu'a donné l'examen juridique

Une évaluation juridique préliminaire (`references/RECHT.md`, en allemand — elle examine les dispositions allemandes et européennes, si bien qu'une citation en traduction serait moins précise, non plus accessible) a confronté le modèle au RGPD, au TDDDG et à la UWG. **Évaluation préliminaire avec références, pas un conseil juridique.** Trois constats, chacun en une ligne :

- **L'hôte reste responsable du traitement, même s'il ne stocke rien.** L'article 4(7) du RGPD rattache la responsabilité à la détermination des finalités et des moyens, non au stockage ; la CJUE l'a explicitement affirmé (C-683/21). Ce qui devient sans objet, c'est la **gestion des utilisateurs**, non la responsabilité.
- **Pour la personne contactée, rien ne diminue.** Les obligations d'information de l'article 14, une mise en balance documentée de la base juridique, un contrat de sous-traitance avec le service qui exécute le contact — ce sont généralement les sections les plus longues d'une politique de confidentialité, et le modèle n'y touche pas.
- **L'exception domestique profite au visiteur, non à l'hôte.** Elle couvre l'usage strictement personnel par une personne physique ; un service proposé à d'autres n'est pas une activité strictement personnelle. C'est précisément là que commence l'hébergement piggyback.

Le gain réside dans l'**étendue des obligations et la taille de la surface d'attaque**, non dans leur nature — ce qui constitue en même temps l'énoncé le plus honnête sur ce modèle.

## Comment appliquer ce modèle

1. Lire `references/DATA-FLOW-TEMPLATE.md` et le remplir pour l'application réelle, en s'appuyant sur les preuves (chaque ligne nécessite un `file:line` ou « non trouvé »). Cela met précisément au jour les hypothèses locales qui cassent sous l'hébergement multi-visiteurs, avant toute modification du code.
2. Décider quels modes l'application nécessite réellement — `local` est toujours la valeur par défaut ; `huckepack-gift` et `huckepack-only-host` sont les deux qui évitent la gestion des utilisateurs ; `pay-membership` reste un stub tant qu'aucune raison concrète d'avoir de vrais comptes n'existe.
3. Rendre la couche de stockage interchangeable (l'étape centrale décrite plus haut), ajouter le champ de clé masqué pour `only-host` et câbler export/import avant toute livraison — c'est le filet de sécurité pour le stockage navigateur volatil.
4. Remplir `references/PRIVACY-TEMPLATE.md` pour le déploiement concret ; supprimer les blocs non pertinents, vérifier chaque indication sur les prestataires au regard des contrats actuels et obtenir un examen juridique propre au cas avant de traiter de véritables données. Le modèle est un point de départ, non une déclaration prête à l'emploi.
5. Pour toute installation impliquant de vrais tiers (appels téléphoniques, messages à des personnes qui ne se sont pas inscrites elles-mêmes) ou des participants à la recherche, traiter les recommandations de `references/RECHT.md` comme une liste de contrôle, non comme une autorisation — faire intervenir un avocat avant la première exécution publique.

## Références

- `references/DATA-FLOW-TEMPLATE.md` — modèle et procédure pour un plan de flux de données : chaque ligne nécessite un file:line, sinon il s'agit d'une supposition, non d'une constatation.
- `references/PRIVACY-TEMPLATE.md` — politique de confidentialité type avec des espaces réservés balisés pour une installation piggyback.
- `references/RECHT.md` — évaluation juridique préliminaire (allemand) avec références au RGPD, au TDDDG et à la UWG.

Les deux modèles sont des **exemples, non des conseils juridiques**. Qui héberge une application l'adapte et reste responsable du résultat.

## Origine

Né lors de la construction de HungryCall, Ringedingeding et ResearchCall — trois agents d'appel pour lesquels un audit des flux de données a montré qu'un hébergement inchangé aurait été un incident de confidentialité avec un nom attaché. Migré depuis le dépôt autonome `huckepack` vers cette bibliothèque de skills.
