---
name: decision-shot
version: 1.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-24
updated: 2026-09-18
description: "Format de sortie extrêmement court et substantiel pour UNE décision ou un groupe de décisions, lorsque l'analyse sous-jacente existe déjà (produite dans le chat, issue de `decide`, de `decision-briefing`, d'un ticket ou d'un document) : contexte en 2 à 3 lignes, avantages/inconvénients par option sous forme de puces au style réduit paveman/caveman, éléments de discussion, une recommandation motivée, et un chemin/lien vers l'analyse complète pour une lecture détaillée. Utilisez cette compétence pour « donne-moi ceci brièvement avec avantages, inconvénients et recommandation », « résumé exécutif de la décision », « contexte court sur <Thema> », « résume la décision X sous une forme courte », /decision-shot, ou lorsqu'un résultat doit être transmis à quelqu'un qui n'a besoin que de l'essentiel, et non de la démonstration complète. NE PAS l'utiliser pour COLLECTER plusieurs décisions ouvertes et les interroger par lettre : c'est le rôle de decision-briefing ; NE PAS l'utiliser pour ANALYSER une décision d'abord : c'est le rôle de decide. decision-shot suppose une analyse achevée et ne fait que compresser sa présentation."
visibility: public
language: fr
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: utilities
tags: [entscheidung, executive-summary, kurzform, pro-contra, talking-points, empfehlung]
status: active

dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, knappform, paveman]

provenance:
  origin: "custom"
  decision_ref: "T-20260824-673115956 (Ticket-Master, User-Auftrag 2026-08-24)"
translated_from_sha256: 26ff135e844d526543d9f5df212d36e408a427a71cc13a9e744a55abdb5ed991
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T12:49:09.278961+00:00"
---
<img src="banner.png" width="100%" alt="decision-shot banner">

# decision-shot

> L'analyse est faite. Ce qui est nécessaire maintenant n'est pas une seconde
> démonstration, mais l'essentiel plus le chemin de retour vers le complet.

## Quand l'utiliser

- Une décision (ou un groupe étroitement lié de décisions, p. ex. plusieurs
  sous-questions d'un même thème) est déjà réfléchie — dans le chat, dans un
  ticket, via le cadre `decide` ou dans la phase 2 de `decision-briefing` — et
  doit maintenant être rendue accessible en quelques secondes à quelqu'un (à
  l'utilisateur, à un autre agent, à un document de passation).
- Mots déclencheurs : « version courte avec avantages et inconvénients »,
  « résumé exécutif », « contexte court », « éléments de discussion à ce sujet »,
  « donne-moi ceci condensé avec recommandation », `/decision-shot`.
- **Pas** lorsque plusieurs points encore ouverts et non tranchés doivent être
  traités successivement ou en lot par lettre — c'est
  [decision-briefing](../decision-briefing/SKILL.md). **Pas** pour élaborer d'abord une
  décision — c'est [decide](../decide/SKILL.md). decision-shot est uniquement
  la PRÉSENTATION d'une analyse déjà disponible.

## Délimitation (version courte)

| Compétence | Fait quoi | Quand c'est terminé |
|---|---|---|
| `decide` | Élabore UNE décision avec un cadre (matrice avantages/inconvénients, notation pondérée, arbre de décision, ...) | L'analyse reste à faire |
| `decision-briefing` | Recueille PLUSIEURS décisions ouvertes d'un thème, les présente en lot A/B/C/D et accepte des réponses par lettre | Plusieurs points restent non tranchés |
| `decision-shot` | Condense UNE analyse achevée (quelle qu'en soit l'origine) en une forme exécutive courte avec lien vers la version complète | L'analyse existe déjà, seule la présentation manque |
| `knappform` | Modificateur général du style de réponse pour TOUTE réponse de la session | Valable pour la session entière, indépendamment du sujet |
| `paveman` | Raccourcit de manière déterministe des FICHIERS EN PROSE existants (fichiers de règles/mémoire) | Raccourcit un fichier, pas une sortie de chat |

`decision-shot` n'entre en concurrence avec aucune des quatre — c'est le FORMAT
qui intervient après `decide` ou à côté de `decision-briefing`, dès que
l'essentiel doit être transmis. Le style de langue réduit s'inspire de
`knappform`/`paveman` (voir là-bas pour la liste complète des suppressions),
mais est appliqué ici de manière systématique dans un format fixe en cinq parties.

## Format (contraignant, cinq parties)

```
## <Entscheidungstitel>

**Kontext:** <2-3 Zeilen -- worum es geht, warum jetzt, was auf dem Spiel steht>

**<Option A>**
+ <staerkstes Pro-Argument>
+ <zweites Pro-Argument, nur falls es traegt>
- <staerkstes Contra-Argument>

**<Option B>**
+ <Pro>
- <Contra>
- <Contra>

**Talking Points:**
- <Punkt, der im Gespraech/in einer Mail sofort zieht>
- <Punkt, der einen typischen Einwand vorwegnimmt>

**Empfehlung:** <Option> -- <ein Satz Begruendung, keine Wiederholung der Pro-Liste>

**Vollanalyse:** <Pfad oder Link -- Ticket-Datei, Dokument, Chat-Referenz>
```

## Règles

- **Textes destinés à l'utilisateur sans numéros/sigles techniques (forme « je », langage courant) :**
  Dans le texte visible pour l'humain (titre, contexte, options, éléments de discussion, recommandation), figurent **aucun** sigle interne, aucun numéro de ticket (`T-...`), aucune référence D ni de chemin relatif.
  Le contexte décrit la situation et l'action prévue à la forme « je » (« Je propose de... »).
  Les références techniques (identifiant de ticket, chemin exact) figurent exclusivement dans la ligne finale `**Vollanalyse:**` ou dans un tableau de références.
- **Les lignes sont un budget, non un objectif.** 2 à 3 lignes de contexte, 2 à 4 puces par option,
  2 à 3 éléments de discussion, 1 phrase de recommandation — tout excédent est supprimé, et non
  raccourci en étant conservé. Si une option ne tient pas en 4 puces, elle n'appartient pas à
  cette compétence mais à l'analyse complète.
- **Style réduit comme `knappform`/`paveman` :** pas de mots de remplissage, pas de
  formules toutes faites, pas d'esquive. Les négations (`nicht`, `nie`, `kein`, `nur`,
  `außer`) restent intactes — les supprimer inverserait l'énoncé.
- **Avantages/inconvénients sous forme de puces, non de phrases.** `+`/`-` en préfixe, une
  idée par ligne, sans proposition complémentaire.
- **Les éléments de discussion sont communicatifs, non analytiques.** Ils répondent à
  « que dire si l'on me demande » — et non « que dit l'analyse ». Les doublons de la liste
  avantages/inconvénients signalent une condensation insuffisante.
- **La recommandation se justifie elle-même en une phrase.** Pas de répétition de la liste
  des avantages, pas de « voir ci-dessus » — cette phrase doit tenir seule, sans le reste du bloc.
- **Le lien/chemin vers l'analyse complète est obligatoire, non facultatif.** decision-shot
  ne remplace pas l'analyse, il la rend rapidement accessible. S'il n'existe aucune source
  tangible (issue uniquement d'une discussion orale dans le chat, sans document), indiquer
  la référence au chat/à la session aussi précisément que possible (p. ex. « cette session,
  réponse à F4 ») plutôt que de laisser le champ vide.
- **Plusieurs décisions liées** (groupe, p. ex. plusieurs sous-questions d'un thème) : un bloc par
  décision, séparés par `---` ; contexte commun une seule fois en tête, uniquement s'il
  vaut réellement pour toutes.

### Horodatage de session des decision-shots enregistrés

Lorsque le decision-shot est enregistré comme artefact nouveau, important et durable, le fichier se termine par :

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

L'identifiant de session provient d'abord d'une indication explicite à l'exécution / en ligne de commande,
puis d'un environnement fournisseur faisant autorité ou d'un hook ; si les deux manquent, on écrit `unbekannt`. Ne jamais
deviner de valeurs. Les sous-agents utilisent la session parente. Les échanges de routine, sources, politiques, `CLAUDE.md`,
README et anciens fichiers ne sont pas horodatés ni rétro-horodatés de manière générale.

## Exemple

```
## Wo laeuft der naechtliche Backup-Job?

**Kontext:** Ich beobachte wiederholte Ausfälle auf dem Laptop, weil das Gerät nachts
schläft. Ich schlage vor, den Job auf den Mac Studio umzuziehen, der rund um die Uhr läuft.

**Laptop (Status quo)**
+ Keine Netzwerkabhaengigkeit
- Job faellt regelmaessig aus, wenn das Geraet schlaeft
- Kein zentraler Log-Ueberblick

**Mac Studio**
+ Laeuft 24/7, keine Ausfaelle durch Schlafmodus
+ Zentrale Logs an einem Ort
- Braucht funktionierendes Tailscale/SSH als Voraussetzung

**Talking Points:**
- "Der Ausfall ist kein Bug im Skript, sondern eine Standortfrage."
- "Tailscale laeuft schon fuer andere Jobs stabil -- kein neues Risiko."

**Empfehlung:** Mac Studio -- einzige Option ohne den bekannten Schlafmodus-
Ausfall, und die Abhaengigkeit (Tailscale) ist bereits im Betrieb bewaehrt.

**Vollanalyse:** `.SYNC/MAC_STUDIO_COMPUTE_HANDOFF.md`, Abschnitt "Backup-Jobs" (Ticket T-20260620-42)
```

## Journal des modifications

### 1.2.0 (2026-09-18)
- Règle de style pour des textes de décision compréhensibles ancrée (T-20260913-883789445, instruction de l'utilisateur du 2026-09-13) :
  - Aucun numéro de ticket, aucune référence D ni chemin interne dans le texte visible (titre, contexte, éléments de discussion).
  - Contexte et recommandation en langage courant, à la forme « je ».
  - Références techniques de ticket et de chemin strictement limitées à la ligne finale de l'analyse complète.

### 1.1.0 (2026-09-09)
- P-018 ajoute l'horodatage de session pour les decision-shots importants nouvellement enregistrés, avec une priorité
  stricte des sources et des exclusions.

### 1.0.0 (2026-08-24)
- Version initiale.
