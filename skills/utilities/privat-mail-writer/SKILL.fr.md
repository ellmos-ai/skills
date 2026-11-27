---
name: privat-mail-writer
version: 0.2.1
type: skill
author: Lukas Geiger + GPT
created: 2026-06-19
updated: 2026-11-22
description: "À utiliser lorsque des e-mails privés ou semi-formels doivent être rédigés, répondus ou formulés avec justesse de ton (ex. 'écris un mail à...', 'rédiger un refus poli', 'raccourcir le mail et relancer', /privat-mail-writer). Rédige des messages précis et adaptés à chaque contact. Ne PAS utiliser pour des campagnes marketing commerciales ou des envois en masse (utiliser dev/community-outreach)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [mail, email, privat, antwort, absage, termin, schreibstil, kontaktprofil]
language: fr
status: active
visibility: public
dependencies: {'tools': [], 'optional_tools': [{'name': 'mail-connector', 'path': '.AI/.MODULES/mail-connector/', 'cli': 'mailc', 'python_module': 'mail_connector.cli', 'usage': 'mailc context <kontakt> --mode reply --json  # Liefert Mail-Kontext als JSON für Profilaufbau', 'note': 'Optionales lokales IMAP-CLI-Tool. Nur nutzen wenn installiert (`pip install -e .` im Modulordner). Ohne dieses Tool arbeitet der Skill ohne Mailzugriff.'}], 'services': ['mail-backend-optional'], 'protocols': ['kontaktprofil', 'usecase-registry'], 'python': []}
provenance: {'origin': 'custom', 'origin_path': 'None', 'origin_version': 'None', 'origin_repo': 'None', 'last_sync_from_origin': 'None', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
---



<img src="banner.png" width="100%" alt="privat-mail-writer banner">

> **Français** — Version française officielle de la compétence `privat-mail-writer`.

# Privat-Mail-Writer — Rédacteur d'e-mails personnels

## Vue d'ensemble et Objectif

`privat-mail-writer` rédige des brouillons d'e-mails courts, cordiaux et adaptés à chaque destinataire. La compétence est conçue de manière neutre vis-à-vis de l'utilisateur : elle ne contient aucun vrai contact, aucune vraie signature et aucun véritable contenu d'e-mail.

Le cœur du fonctionnement est paresseux (*lazy*) et empirique : ce n'est que lorsque l'utilisateur souhaite écrire un e-mail concret à un contact précis qu'on crée ou met à jour le profil de ce contact exact. Ne jamais générer de profils à l'avance. Si aucun historique d'e-mails n'est disponible, ne pas inventer d'affirmations sur le style, mais rédiger brièvement de façon neutre ou demander des exemples ciblés.

## Ressources

- `CONFIG.md` — préférences centrales, règles si-alors, portes de permission et interrupteurs de liste noire.
- `BLACKLIST.md` — exclusions pour newsletters, expéditeurs système et contacts sans profil.
- `USECASES.md` — registre des cas d'usage et règles pour les nouveaux cas d'usage.
- `SIGNATURES.md` — règles neutres de signature et formules de politesse.
- `MUSTER-BLOCKS.md` — courts blocs de texte réutilisables.
- `kontaktprofile.json` — schéma vide et neutre pour les profils de contacts. Ne conserver les vrais profils que localement et avec parcimonie des données.

## Flux de travail

1. **Charger la configuration :** lire `CONFIG.md`. Si la liste noire est active, consulter aussi `BLACKLIST.md`.
2. **Vérifier le déclencheur :** n'établir un profil que pour une demande de rédaction concrète destinée à un contact précis, ex. « écris un mail à mon frère Simon ». Pas de balayage de la boîte de réception uniquement pour créer des profils.
3. **Vérifier la liste noire :** newsletters, adresses no-reply, expéditeurs système et domaines/contacts exclus ne reçoivent pas de profil de contact. Pour ces cas, répondre de manière neutre ou ne pas répondre.
4. **Identifier la tâche de messagerie :** déterminer l'objectif, le destinataire, l'occasion, la brièveté souhaitée, la langue, le ton et les faits nécessaires.
5. **Déterminer le cas d'usage :** lire `USECASES.md` et sélectionner le cas d'usage le plus adapté. Si aucun ne convient, créer un nouveau cas d'usage réutilisable ou poser une brève question en cas d'informations obligatoires manquantes.
6. **Vérifier le profil de contact :** pour chaque destinataire non exclu, rechercher un profil existant dans `kontaktprofile.json` ou dans une copie locale privée des profils.
7. **Créer ou mettre à jour le profil :** s'il n'existe pas encore de profil fiable, lire jusqu'aux dix derniers e-mails pertinents avec ce contact précis depuis le backend mail disponible. Accorder plus de poids aux e-mails envoyés qu'aux e-mails reçus pour cerner le style d'écriture.
8. **Enregistrer les données empiriques :** ne sauvegarder dans le profil de contact que des signaux synthétiques et vérifiables de style, de relation et de catégorie. Ne déposer aucun e-mail brut, aucune longue citation et aucun détail personnel superflu.
9. **Appliquer la porte de permission :** avant l'envoi, en cas de contenu délicat ou d'informations obligatoires manquantes, respecter les garde-fous de `CONFIG.md`.
10. **Rédiger le brouillon :** combiner forme du cas d'usage, profil de contact et tâche actuelle. Reproduire le style sans inventer de fausse proximité, de fausses promesses ni de motifs non avérés.
11. **Fournir la sortie :** par défaut, produire l'objet et le corps du message. N'envoyer que si l'utilisateur a explicitement autorisé l'envoi et qu'un outil d'envoi adapté est disponible.

## Profils de contacts

Un profil de contact ne décrit pas la personne en soi, mais la relation de communication observée et le style d'écriture du titulaire du compte envers cette personne.

Les champs de profil doivent rester concis :

- date du dernier contact
- nombre et période des e-mails analysés
- formule d'appel et formule de politesse
- tutoiement/vouvoiement/degré de formalité
- longueur des phrases et brièveté typique
- degré de chaleur, franchise, engagement
- estimation de la relation avec indice de confiance
- catégorie de contact, ex. `family`, `inner-circle`, `friends`, `colleagues`, `services`, `official`, `unknown`
- source de la catégorie : déclaration de l'utilisateur, texte d'e-mail, carnet d'adresses, signature ou inférence
- degré de preuve de la catégorie : `user-confirmed`, `strong`, `medium`, `weak`
- courts justificatifs paraphrasés tels que « plusieurs e-mails envoyés se terminent par "Bien cordialement" » ou « les réponses restent sous cinq phrases »

Vérifier chaque mois si un contrôle d'ancienneté est dû. Si le mois de la date actuelle diffère du `last_age_check` enregistré, supprimer les profils dont `last_contact_at` remonte à plus d'un an et actualiser `last_age_check` à la date du jour. La valeur initiale dans le JSON neutre est `2026-06-18`.

## Règles de style

- Écrire court. Les e-mails privés nécessitent rarement de longs préambules.
- Rester aimable, sans sur-expliquer.
- N'indiquer de véritables motifs que s'ils ont été donnés par l'utilisateur ou sont certains d'après le contexte.
- Pour les refus officiels : poli, clair, sans roman justificatif.
- En cas d'incertitude sur les faits : poser une brève question de clarification avant de finaliser le brouillon.
- Rédiger les textes français avec une typographie et des accents corrects.

## Nouveaux cas d'usage

Lorsqu'une tâche de messagerie semble réutilisable et n'est pas encore couverte dans `USECASES.md`, compléter le cas d'usage :

- identifiant stable, ex. `UC-002`
- nom et déclencheurs typiques
- objectif de l'e-mail
- informations obligatoires et facultatives
- longueur et ton par défaut
- court modèle ou enchaînement de blocs
- questions ouvertes si des informations obligatoires manquent

Un cas particulier ponctuel ne doit pas être gonflé en cas d'usage. Dans ce cas, livrer uniquement le brouillon courant.

## Format de sortie

Pour les brouillons normaux :

```text
Objet : ...

Madame, Monsieur ...,

...

Cordialement,
[Signature]
```

Si l'utilisateur ne veut que le texte sans objet, ne fournir que le corps de l'e-mail. Si plusieurs variantes sont pertinentes, proposer au plus deux variantes : « très court » et « un peu plus chaleureux ».

## Limites

Ne jamais inventer de profil de contact. Ne pas copier inutilement de détails confidentiels issus d'e-mails dans la réponse. Ne jamais envoyer d'e-mail sans autorisation explicite. Ne formuler aucun engagement juridique, médical ou financier si l'utilisateur ne l'indique pas clairement.

## Journal des modifications

### 0.2.1 (2026-11-22)
- Mention linguistique corrigée.

### 0.2.0 (2026-06-19)
- Ajout de `CONFIG.md` et `BLACKLIST.md`.
- Création de profils limitée aux demandes concrètes de rédaction d'e-mails.
- Catégories de contacts avec source et niveau de preuve intégrées au schéma de profil.

### 0.1.0 (2026-06-19)
- Version initiale avec registre des cas d'usage, règles de signature, blocs modèles et JSON de profils de contacts vide.
