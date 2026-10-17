---
name: cron-tuner
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-08-01
updated: 2026-08-23
language: fr
visibility: public
standalone: true
anthropic_compatible: true
category: infrastructure
tags: [cadence, scheduler, cooldown, backoff, self-tuning, cron]
status: active
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
description: "Boucle de régulation de cadence auto-ajustable pour les analyses récurrentes d'agents. À utiliser lorsqu'une analyse planifiée doit accélérer sa cadence en cas d'activité et ralentir en cas de silence, sans intervention de l'opérateur."

translated_from_sha256: 4872af1b0af7126a6e61179a521bfde60be8ab195522e48cf612f260b65b139c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:32:13.556981+00:00"
---
<img src="banner.png" width="100%" alt="cron-tuner banner">

# cron-tuner — boucle de régulation de cadence auto-ajustable

Une boucle de régulation **auto-ajustable** pour les travaux récurrents pilotés
par un calendrier (tâches cron, tâches planifiées, minuteurs). Au lieu d'un
intervalle fixe, la tâche ajuste elle-même sa cadence : elle accélère lorsqu'il
y a du travail et ralentit en cas de silence. Neutre vis-à-vis de l'hôte et de
la plateforme ; le modèle fonctionne avec n'importe quel ordonnanceur.

## Quand l'utiliser

- Une analyse récurrente (surveillance de boîte aux lettres, analyse de Sync-Yard,
  interrogation de file d'attente) doit réagir rapidement pendant une
  « correspondance » active et rester économique pendant les périodes d'inactivité.
- L'ajustement doit être **auditable** (un fichier d'état) plutôt qu'implicite
  dans une conversation ou dans la tête d'une personne.

## Concepts

- **Boucle de régulation** : mesurer → décider → agir → persister. Chaque
  exécution se termine par l'écriture de son état ; chaque exécution commence
  par sa lecture.
- **Activation** : nouveau travail détecté → passage immédiat à l'intervalle
  le plus rapide.
- **Échelle de refroidissement** : les exécutions vides descendent d'un
  palier sur l'échelle ; chaque palier ne s'applique que si l'intervalle change
  réellement.
- **Plafond** : ne jamais dépasser un intervalle maximal défini.

## Schéma de référence

| Condition | Nouvel intervalle |
|---|---|
| nouveau travail détecté | le plus rapide (p. ex. 15 min) |
| 4 exécutions vides consécutives | 30 min |
| 6 exécutions vides consécutives | 1 h |
| chaque exécution vide supplémentaire | doubler (2 h, 4 h, 8 h) |
| Plafond | 24 h (jamais davantage) |

Ajuster les seuils à la charge de travail ; garder le doublement simple et le
plafond explicite.

## Fichier d'état (obligatoire)

Un petit fichier JSON par worker, p. ex. `cron-tuner-state.json` :

```json
{
  "empty_runs": 0,
  "interval_minutes": 15,
  "note": "cron-tuner state"
}
```

Règles :

1. **Un fichier, pas la mémoire.** Le compteur doit survivre à la compaction du
   contexte, aux redémarrages de session et aux changements d'opérateur, et
   rester consultable par les humains et les autres agents. Ne pas suivre la
   cadence dans l'historique de conversation.
2. **Réécrire uniquement en cas de changement.** Persister l'état à chaque
   exécution, mais ne remplacer la tâche planifiée que si l'intervalle change
   réellement.
3. **Nouvelle tâche = nouveau calendrier, même état.** Un changement de cadence
   signifie supprimer l'ancienne tâche et en créer une nouvelle avec le nouvel
   intervalle ; le compteur continue.

## Règles d'exploitation

- **Le travail décide, pas l'humeur.** Seules les arrivées observées modifient
  la cadence — jamais les attentes ni les approximations.
- **Décalages anti-troupeau.** Éviter les repères pleine heure et demi-heure
  pour l'intervalle le plus rapide (p. ex. minutes 7/22/37/52), afin que les
  flottes ne se déclenchent pas en même temps.
- **Sécurité intégrée :** si un système partenaire se tait, la règle normale de
  vacance/absence s'applique — le régulateur n'escalade jamais vers des
  inondations d'interrogations.
- **Traçabilité :** chaque changement de cadence est consigné avec sa raison,
  l'ancien intervalle et le nouveau.

## Extensibilité (registre des types de boucles)

La compétence a vocation à accueillir, au fil du temps, d'autres types de
boucles auto-ajustables :

- **cooldown** (ce schéma : silence → plus lent)
- **backoff** (erreurs → plus lent, succès → plus rapide)
- **burst** (pic d'arrivées → mode rapide temporaire avec fin explicite)
- **wake-assist** (message de réveil externe → exécution immédiate hors cycle)

Chaque nouveau type de boucle reçoit ici une sous-section ainsi que son propre
schéma de fichier d'état.
