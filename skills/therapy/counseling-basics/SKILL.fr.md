---
name: counseling-basics
version: 1.0.1
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-11-22
description: "À utiliser lorsque les bases de la communication thérapeutique centrée sur la personne et du conseil sont nécessaires (ex. 'écoute active', 'pratiquer le reflet', 'poser des questions ouvertes', /counseling-basics). Transmet les fondamentaux de Rogers : compréhension empathique, reformulation, validation et questions de clarification constructives. Ne PAS utiliser pour des interventions psychothérapeutiques spécifiques à un trouble (utiliser guideline-therapies-overview)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [counseling, active-listening, communication, therapy]
language: fr
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/therapie/gespraechsfuehrung_basis.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---


<img src="banner.png" width="100%" alt="counseling-basics banner">

> **Français** — Version française officielle de la compétence `counseling-basics`.

# Bases de l'entretien d'aide (Counseling Basics)

> Fondamentaux de la communication thérapeutique : écoute active, reflet, reformulation

Voir : [ETHICS.md](../ETHICS.md)

---

## Contexte

Ce modèle décrit les techniques fondamentales de communication thérapeutique. Il sert de cadre contextuel pour l'accompagnement et le soutien relationnel.

**Remarque :** ces techniques apportent un soutien, mais ne remplacent pas une thérapie professionnelle. En situation de crise aiguë, toujours orienter vers une aide professionnelle.

**Ne jamais implémenter :** EMDR, Exposition prolongée (PE), Thérapie d'exposition narrative (NET).

---

## 1. Écoute active

**Objectif :** témoigner d'une compréhension complète, accueillir véritablement ce qui est exprimé.

**Techniques :**

- **Accusé de réception verbal :** « Je comprends », « Mm-hmm », « Cela semble difficile »
- **Approfondissement :** « Pouvez-vous décrire cela plus en détail ? » / « Qu'entendez-vous par là ? »
- **Synthèse :** à la fin d'une séquence, résumer brièvement ce qui a été entendu
- **Écoute non directive :** aucun conseil avant que la personne ait terminé

**Attitude :** pleine attention, aucune interruption, aucun jugement.

**Formule d'entretien :**
> « Ce que j'ai entendu, c'est [résumé]. Est-ce exact ? »

---

## 2. Reflet (Mirroring)

**Objectif :** renvoyer les émotions perçues, rendre les ressentis visibles.

**Techniques :**

- **Reflet simple :** reprendre le dernier mot ou la dernière phrase en la reformulant légèrement
- **Reflet émotionnel :** nommer les émotions exprimées ou sous-jacentes
  > « On dirait que vous êtes très épuisé(e) en ce moment. »
- **Reflet corporel :** (en présentiel) ajuster sa posture

**Prudence :**
- Ne pas en abuser — trop de reflets paraît artificiel
- Ne pas sur-interpréter

**Exemples :**
> Personne : « Je ne sais plus quoi faire. »
> Reflet : « Vous ne savez plus quoi faire — on dirait que tout devient accablant en ce moment. »

---

## 3. Reformulation (Paraphrase)

**Objectif :** restituer le contenu central avec ses propres mots, vérifier la compréhension.

**Différence avec le reflet :** le reflet renvoie l'émotion, la reformulation restitue le contenu/le sens.

**Structure :**
1. Résumer brièvement le contenu
2. Mettre en évidence le message central
3. Demander confirmation

**Formule :**
> « Si je vous comprends bien, vous dites que [reformulation]. Est-ce bien cela ? »

**Exemples :**
> Personne : « Ma mère me harcèle tous les jours avec les mêmes reproches et je n'en peux plus. »
> Reformulation : « Cela ressemble donc à une boucle sans fin dont vous ne voyez actuellement aucune issue ? »

---

## 4. Questions ouvertes

**Objectif :** encourager l'exploration sans imposer de réponses.

**Caractéristiques des questions ouvertes :**
- Commencent par : Comment, Quoi, De quelle manière, Décrivez, Expliquez
- Laissent place à des réponses personnelles
- Ne peuvent pas être résolues par oui/non

**Exemples :**
- « Qu'avez-vous ressenti à ce moment-là ? »
- « Que se passe-t-il en vous lorsque cela arrive ? »
- « Comment gérez-vous cela d'habitude ? »

**Éviter les questions fermées :**
- « Est-ce que ça a fait mal ? » -> mieux : « Qu'avez-vous ressenti ? »
- « Êtes-vous triste ? » -> mieux : « Qu'est-ce qui vous traverse l'esprit en ce moment ? »

---

## 5. Validation

**Objectif :** confirmer les émotions et réactions comme compréhensibles et légitimes.

**Important :** valider ne signifie pas être d'accord, mais comprendre.

**Formule :**
> « Il est tout à fait compréhensible que vous ressentiez cela au vu de [situation]. »

**Niveaux de validation (d'après Linehan) :**
1. Écoute attentive (montrer sa présence)
2. Reflet exact (qu'est-ce qui a été dit ?)
3. Reconnaître ce qui n'est pas formulé explicitement
4. Comprendre la cause dans son contexte
5. Reconnaître la réaction comme compréhensible
6. Authenticité radicale (réponse sincère, d'égal à égal)

---

## 6. Phases de l'entretien

| Phase | Objectif | Techniques |
|-------|----------|------------|
| Ouverture | Arriver, créer un climat de sécurité | Accueil, questions ouvertes, posture sans jugement |
| Exploration | Explorer le thème | Écoute active, approfondissement, reformulation |
| Approfondissement | Accéder aux niveaux plus profonds | Reflet, validation, résonance émotionnelle |
| Intégration | Relier, étapes suivantes | Synthèse, mise à l'épreuve d'hypothèses, perspectives |
| Clôture | Conclure, assurer la transition | Rétrospective, tâches entre séances, au revoir |

---

## Éthique et limites

**Un assistant IA peut :**
- Expliquer et illustrer les techniques d'entretien
- Guider l'écoute active, le reflet et la reformulation
- Poser des questions ouvertes et proposer une validation
- Fournir une psychoéducation sur les compétences d'entretien

**Un assistant IA ne doit PAS :**
- Remplacer des entretiens thérapeutiques professionnels
- Poser des diagnostics ni émettre de recommandations de traitement
- Mener d'intervention de crise
- Appliquer l'EMDR, l'exposition prolongée (PE) ou la thérapie d'exposition narrative (NET)

**En cas de crise aiguë, TOUJOURS orienter vers :**
- 988 Suicide & Crisis Lifeline (US) : 988
- Crisis Text Line (US) : envoyer HOME au 741741
- Samaritans (UK) : 116 123
- Telefonseelsorge (DE) : 0800 111 0 111 / 0800 111 0 222
- Services d'urgence : 911 (US) / 112 (UE)

---

## Références

- Rogers, C. R. (1951). *Client-Centered Therapy.* Houghton Mifflin.
- Rogers, C. R. (1961). *On Becoming a Person.* Houghton Mifflin.
- Linehan, M. M. (1993). *Cognitive-Behavioral Treatment of Borderline Personality Disorder.* Guilford Press.

---

*Porté depuis BACH v3.8.0 | Version autonome*
*Sources : Rogers (1951, 1961), Linehan (1993) — Ne remplace pas une thérapie professionnelle*

## Journal des modifications

### 1.0.1 (2026-11-22)
- Mention linguistique corrigée.
